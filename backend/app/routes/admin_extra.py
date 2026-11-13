# backend/app/routes/admin_extra.py
"""
👑 امکانات تکمیلی پنل مدیریت
دسترسی نقش‌ها، کدهای فراموشی رمز، ورود به‌جای کاربر (impersonate)، تنظیمات و سفارش‌های فروشگاه،
تنظیمات فروشِ هر کود سیستمی.
"""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import AppSetting, Fertilizer, PasswordResetToken, ShopOrder, User, UserSession
from app.permissions import KEY as PERM_KEY, PERMISSIONS, defaults as perm_defaults, load_matrix
from app.routes.admin import _iso, _page, _paged, _put_setting, audit
from app.schemas.base import validate_password_strength
from app.security import (delete_user_sessions, get_current_user, get_password_hash, require_admin)
from app.security_logger import log_security_event
from app.shop_common import (DEFAULT_SHOP, ORDER_STATUSES, SHOP_KEY, load_shop_settings, order_row)
from app.sms import generate_reset_token, generate_verification_code, sms_provider

router = APIRouter(prefix="/admin", tags=["Admin Extra"], dependencies=[Depends(require_admin)])
public_router = APIRouter(tags=["Admin Extra Public"])


# ============================================================
# 🔑 دسترسی‌های نقش‌ها
# ============================================================
class PermBody(BaseModel):
    matrix: Dict[str, Dict[str, bool]]


@router.get("/permissions")
def get_permissions(db: Session = Depends(get_db)):
    return {
        "definitions": [{"key": k, "label": v["label"], "hint": v["hint"]} for k, v in PERMISSIONS.items()],
        "matrix": load_matrix(db),
        "defaults": perm_defaults(),
    }


@router.put("/permissions")
def put_permissions(body: PermBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    clean: Dict[str, Dict[str, bool]] = {}
    for role in ("user", "plus"):
        clean[role] = {k: bool(v) for k, v in (body.matrix.get(role) or {}).items() if k in PERMISSIONS}
    _put_setting(db, admin, PERM_KEY, clean)
    audit(db, admin, request, "permissions.update", "setting", None, "permissions", None)
    db.commit()
    return {"matrix": load_matrix(db), "definitions": get_permissions(db)["definitions"], "defaults": perm_defaults()}


# ============================================================
# 📱 کدهای فراموشی رمز (برای مواقعی که پیامک نمی‌رسد)
# ============================================================
def _reset_row(t: PasswordResetToken, u: Optional[User], now: datetime) -> dict:
    code = t.token.split(":", 1)[1] if ":" in (t.token or "") else None
    exp = t.expires_at.replace(tzinfo=timezone.utc) if t.expires_at and t.expires_at.tzinfo is None else t.expires_at
    expired = bool(exp and exp < now)
    return {
        "id": t.id, "user_id": t.user_id, "user_name": u.full_name if u else None,
        "phone_number": u.phone_number if u else None, "code": code,
        "is_used": bool(t.is_used), "is_expired": expired,
        "state": "used" if t.is_used else ("expired" if expired else "pending"),
        "ip": t.ip_address, "created_at": _iso(t.created_at), "expires_at": _iso(t.expires_at),
    }


@router.get("/reset-requests")
def reset_requests(state: Optional[str] = Query(None, pattern="^(pending|used|expired)$"), q: Optional[str] = None,
                   page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    query = db.query(PasswordResetToken, User).join(User, User.id == PasswordResetToken.user_id)
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(or_(User.phone_number.ilike(term), User.first_name.ilike(term), User.last_name.ilike(term)))
    if state == "pending":
        query = query.filter(PasswordResetToken.is_used == False, PasswordResetToken.expires_at > now)  # noqa: E712
    elif state == "used":
        query = query.filter(PasswordResetToken.is_used == True)  # noqa: E712
    elif state == "expired":
        query = query.filter(PasswordResetToken.is_used == False, PasswordResetToken.expires_at <= now)  # noqa: E712
    total = query.count()
    rows = query.order_by(PasswordResetToken.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    pending = db.query(func.count(PasswordResetToken.id)).filter(PasswordResetToken.is_used == False,  # noqa: E712
                                                                 PasswordResetToken.expires_at > now).scalar() or 0
    return {**_paged([_reset_row(t, u, now) for t, u in rows], total, page, page_size), "pending": pending}


class ResetCodeBody(BaseModel):
    send_sms: bool = False


@router.post("/users/{user_id}/reset-code")
def make_reset_code(user_id: int, body: ResetCodeBody, request: Request, db: Session = Depends(get_db),
                    admin: User = Depends(require_admin)):
    """ساخت کد بازیابی دستی برای کاربر (اختیاری: ارسال پیامک)؛ کاربر با همین کد در صفحهٔ فراموشی رمز را عوض می‌کند"""
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == u.id,
                                        PasswordResetToken.is_used == False).update({"is_used": True})  # noqa: E712
    code = generate_verification_code(6)
    rec = PasswordResetToken(user_id=u.id, token=f"{generate_reset_token()}:{code}", is_used=False,
                             expires_at=datetime.utcnow() + timedelta(minutes=30), ip_address="admin")
    db.add(rec)
    sent = False
    if body.send_sms:
        try:
            sent = bool(sms_provider.send_reset_password_code(phone_number=u.phone_number, code=code))
        except Exception:
            sent = False
    audit(db, admin, request, "user.reset_code", "user", u.id, u.full_name, {"sms": body.send_sms, "sent": sent})
    db.commit()
    return {"code": code, "phone_number": u.phone_number, "sms_sent": sent, "expires_in_minutes": 30}


@router.post("/reset-requests/{rid}/expire")
def expire_reset(rid: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    t = db.get(PasswordResetToken, rid)
    if not t:
        raise HTTPException(status_code=404, detail="درخواست پیدا نشد")
    t.is_used = True
    audit(db, admin, request, "user.reset_code_revoke", "user", t.user_id, None, None)
    db.commit()
    return {"ok": True}


# ============================================================
# 🎭 ورود به‌جای کاربر (Impersonate)
# ============================================================
IMP_COOKIE = "admin_backup_token"


def _cookie_kwargs(hours: float) -> dict:
    return dict(httponly=True, secure=False, samesite="lax", max_age=int(hours * 3600), path="/")


@router.post("/users/{user_id}/impersonate")
def impersonate(user_id: int, request: Request, response: Response, db: Session = Depends(get_db),
                admin: User = Depends(require_admin)):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    if target.id == admin.id:
        raise HTTPException(status_code=400, detail="نمی‌توانید به‌جای خودتان وارد شوید")
    if target.role == "admin":
        raise HTTPException(status_code=403, detail="ورود به‌جای مدیر دیگر مجاز نیست")
    if target.status != "active":
        raise HTTPException(status_code=400, detail="حساب این کاربر فعال نیست؛ ابتدا آن را بازیابی کنید")
    admin_token = request.cookies.get("access_token")
    if not admin_token:
        h = request.headers.get("Authorization", "")
        admin_token = h[7:] if h.startswith("Bearer ") else None
    if not admin_token:
        raise HTTPException(status_code=401, detail="توکن مدیر پیدا نشد")
    hours = 2
    token = secrets.token_urlsafe(64)
    db.add(UserSession(user_id=target.id, token=token, is_active=True,
                       expires_at=datetime.utcnow() + timedelta(hours=hours),
                       ip_address=request.client.host if request.client else None, user_agent="impersonation"))
    audit(db, admin, request, "user.impersonate", "user", target.id, target.full_name, None)
    db.commit()
    log_security_event(db=db, event_type="IMPERSONATION_START", user_id=target.id,
                       ip_address=request.client.host if request.client else None, severity="WARNING",
                       details={"admin_id": admin.id, "admin_name": admin.full_name})
    response.set_cookie(key=IMP_COOKIE, value=admin_token, **_cookie_kwargs(hours))
    response.set_cookie(key="access_token", value=token, **_cookie_kwargs(hours))
    return {"ok": True, "user": {"id": target.id, "full_name": target.full_name, "phone_number": target.phone_number}}


@public_router.post("/system/stop-impersonation")
def stop_impersonation(request: Request, response: Response, db: Session = Depends(get_db)):
    backup = request.cookies.get(IMP_COOKIE)
    if not backup:
        raise HTTPException(status_code=400, detail="در حالت ورود به‌جای کاربر نیستید")
    from app.security import get_session_by_token
    sess = get_session_by_token(backup, db)
    adm = db.get(User, sess.user_id) if sess else None
    if not adm or adm.role != "admin":
        response.delete_cookie(IMP_COOKIE, path="/")
        raise HTTPException(status_code=401, detail="نشست مدیر منقضی شده؛ دوباره وارد شوید")
    cur = request.cookies.get("access_token")
    if cur:
        db.query(UserSession).filter(UserSession.token == cur, UserSession.user_agent == "impersonation") \
            .update({"is_active": False})
        db.commit()
    response.set_cookie(key="access_token", value=backup, **_cookie_kwargs(settings.SESSION_EXPIRY_HOURS))
    response.delete_cookie(IMP_COOKIE, path="/")
    return {"ok": True}


# ============================================================
# 🛒 تنظیمات فروشگاه
# ============================================================
class ShopSettingsBody(BaseModel):
    enabled: Optional[bool] = None
    card_number: Optional[str] = Field(None, max_length=30)
    card_holder: Optional[str] = Field(None, max_length=80)
    bank_name: Optional[str] = Field(None, max_length=60)
    payment_note: Optional[str] = Field(None, max_length=600)
    shipping_fee: Optional[float] = Field(None, ge=0)
    free_shipping_over: Optional[float] = Field(None, ge=0)
    min_order_total: Optional[float] = Field(None, ge=0)
    receipt_required: Optional[bool] = None
    require_address: Optional[bool] = None
    currency_label: Optional[str] = Field(None, max_length=20)
    shop_note: Optional[str] = Field(None, max_length=600)


@router.get("/shop/settings")
def get_shop_settings(db: Session = Depends(get_db)):
    return load_shop_settings(db)


@router.put("/shop/settings")
def put_shop_settings(body: ShopSettingsBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    cur = load_shop_settings(db)
    new = {**cur, **{k: v for k, v in body.dict().items() if v is not None}}
    _put_setting(db, admin, SHOP_KEY, new)
    audit(db, admin, request, "shop.settings", "setting", None, "shop", {"keys": [k for k in new if new[k] != cur[k]]})
    db.commit()
    return load_shop_settings(db)


class FertShopBody(BaseModel):
    shop_enabled: Optional[bool] = None
    shop_price: Optional[float] = Field(None, ge=0)
    shop_stock: Optional[float] = Field(None, ge=0)
    shop_min_qty: Optional[float] = Field(None, ge=0)
    clear_price: bool = False
    clear_stock: bool = False


@router.put("/fertilizers/{fert_id}/shop")
def fert_shop(fert_id: int, body: FertShopBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    f = db.query(Fertilizer).filter(Fertilizer.id == fert_id, Fertilizer.is_system_default == True,  # noqa: E712
                                    Fertilizer.user_id == None).first()                               # noqa: E711
    if not f:
        raise HTTPException(status_code=404, detail="کود سیستمی پیدا نشد")
    if body.shop_enabled is not None:
        f.shop_enabled = body.shop_enabled
    if body.clear_price:
        f.shop_price = None
    elif body.shop_price is not None:
        f.shop_price = body.shop_price
    if body.clear_stock:
        f.shop_stock = None
    elif body.shop_stock is not None:
        f.shop_stock = body.shop_stock
    if body.shop_min_qty is not None:
        f.shop_min_qty = body.shop_min_qty or None
    audit(db, admin, request, "fertilizer.shop", "fertilizer", f.id, f.name, None)
    db.commit()
    return {"id": f.id, "shop_enabled": f.shop_enabled, "shop_price": f.shop_price, "shop_stock": f.shop_stock,
            "shop_min_qty": f.shop_min_qty}


# ============================================================
# 📦 سفارش‌ها
# ============================================================
@router.get("/orders")
def list_orders(status: Optional[str] = None, q: Optional[str] = None, page: int = Query(1, ge=1),
                page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    query = db.query(ShopOrder)
    if status:
        query = query.filter(ShopOrder.status == status)
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(or_(ShopOrder.code.ilike(term), ShopOrder.user_name.ilike(term), ShopOrder.phone_number.ilike(term)))
    total, rows = _page(query.order_by(ShopOrder.created_at.desc()), page, page_size)
    counts = {s: c for s, c in db.query(ShopOrder.status, func.count(ShopOrder.id)).group_by(ShopOrder.status).all()}
    return {**_paged([order_row(o) for o in rows], total, page, page_size), "counts": counts, "statuses": ORDER_STATUSES}


@router.get("/orders/{oid}")
def order_detail(oid: int, db: Session = Depends(get_db)):
    o = db.get(ShopOrder, oid)
    if not o:
        raise HTTPException(status_code=404, detail="سفارش پیدا نشد")
    return order_row(o, with_receipt=True)


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    admin_note: Optional[str] = Field(None, max_length=1000)
    reject_reason: Optional[str] = Field(None, max_length=500)
    tracking_code: Optional[str] = Field(None, max_length=60)


@router.put("/orders/{oid}")
def update_order(oid: int, body: OrderUpdate, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    o = db.get(ShopOrder, oid)
    if not o:
        raise HTTPException(status_code=404, detail="سفارش پیدا نشد")
    d = body.dict(exclude_unset=True)
    if "status" in d:
        if d["status"] not in ORDER_STATUSES:
            raise HTTPException(status_code=400, detail="وضعیت نامعتبر است")
        if d["status"] == "rejected" and not (d.get("reject_reason") or o.reject_reason):
            raise HTTPException(status_code=400, detail="دلیل رد سفارش را بنویسید")
        # کسر موجودی هنگام تأیید پرداخت (فقط یک‌بار)
        if d["status"] == "approved" and o.status not in ("approved", "processing", "shipped", "completed"):
            for it in o.items or []:
                f = db.get(Fertilizer, it.get("fertilizer_id"))
                if f is not None and f.shop_stock is not None:
                    f.shop_stock = max(0.0, f.shop_stock - float(it.get("qty") or 0))
        o.status = d["status"]
    for k in ("admin_note", "reject_reason", "tracking_code"):
        if k in d:
            setattr(o, k, d[k] or None)
    o.handled_by = admin.id
    audit(db, admin, request, "order.update", "order", o.id, o.code, {"status": o.status})
    db.commit()
    return order_row(o, with_receipt=False)


@router.get("/orders-stats/summary")
def orders_summary(db: Session = Depends(get_db)):
    paid = ("approved", "processing", "shipped", "completed")
    revenue = db.query(func.coalesce(func.sum(ShopOrder.total), 0)).filter(ShopOrder.status.in_(paid)).scalar() or 0
    waiting = db.query(func.count(ShopOrder.id)).filter(ShopOrder.status == "awaiting_review").scalar() or 0
    total = db.query(func.count(ShopOrder.id)).scalar() or 0
    return {"revenue": float(revenue), "waiting_review": waiting, "total": total}
