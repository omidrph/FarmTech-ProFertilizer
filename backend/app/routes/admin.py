# backend/app/routes/admin.py
"""
👑 پنل مدیریت — API مدیران (نقش admin)
============================================================
همهٔ مسیرها زیر /admin و پشت require_admin هستند. هر کار تغییردهنده در audit_logs ثبت می‌شود.
بخش‌ها: آمار، مدیریت کاربران (ویرایش/بلاک/بن/نقش/رمز/حذف/گروهی)، کودهای سیستمی،
لاگ محاسبه‌ها، لاگ امنیتی، لاگ مدیریتی، اعلان‌ها، تنظیمات (تعمیر/ثبت‌نام) و سلامت سیستم.
"""
from __future__ import annotations

import logging
import platform
import secrets
import string
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import (
    Announcement, AppSetting, AuditLog, Fertilizer, OptimizationLog, PhAdjustment,
    Report, SecurityLog, User, UserSession,
)
from app.schemas.auth import UserCreate
from app.schemas.base import validate_name, validate_password_strength, validate_phone_number
from app.schemas.fertilizer import FertilizerCreate, FertilizerUpdate
from app.security import (
    delete_user_sessions, get_password_hash, invalidate_settings_cache, require_admin,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin)])

ROLES = ("user", "plus", "admin")
_STARTED_AT = time.time()


# ============================================================
# ابزارهای مشترک
# ============================================================
def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def audit(db: Session, admin: User, request: Request, action: str, target_type: Optional[str] = None,
          target_id: Optional[int] = None, label: Optional[str] = None, details: Optional[dict] = None) -> None:
    """ثبت کار ادمین (همراه تراکنش اصلی commit می‌شود)"""
    db.add(AuditLog(
        admin_id=admin.id, admin_name=admin.full_name, action=action, target_type=target_type,
        target_id=target_id, target_label=(label or "")[:160] or None, details=details, ip_address=_ip(request),
    ))


def _page(q, page: int, page_size: int):
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def _paged(items: list, total: int, page: int, page_size: int) -> dict:
    return {"items": items, "total": total, "page": page, "page_size": page_size,
            "pages": max((total + page_size - 1) // page_size, 1)}


def _iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


# ============================================================
# 📊 آمار داشبورد
# ============================================================
def _trend(cur: float, prev: float) -> Optional[float]:
    """درصد تغییر نسبت به دورهٔ قبل (None وقتی دورهٔ قبل صفر بوده)"""
    if not prev:
        return None
    return round((cur - prev) / prev * 100, 1)


@router.get("/stats")
def stats(days: int = Query(14, ge=7, le=90), db: Session = Depends(get_db)):
    now = _now()
    d1, d7, d30 = now - timedelta(days=1), now - timedelta(days=7), now - timedelta(days=30)
    today0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start = today0 - timedelta(days=days - 1)
    prev_start = start - timedelta(days=days)

    by_role = {r: c for r, c in db.query(User.role, func.count(User.id)).group_by(User.role).all()}
    by_status = {s_: c for s_, c in db.query(User.status, func.count(User.id)).group_by(User.status).all()}
    total_users = sum(by_role.values())

    OL = OptimizationLog

    def calc_block(lo: datetime, hi: Optional[datetime] = None) -> dict:
        q = db.query(func.count(OL.id), func.count(func.distinct(OL.user_id)),
                     func.avg(OL.convergence_time_ms), func.avg(OL.cost_total)).filter(OL.created_at >= lo)
        qf = db.query(func.count(OL.id)).filter(OL.created_at >= lo, OL.is_successful == False)  # noqa: E712
        if hi is not None:
            q, qf = q.filter(OL.created_at < hi), qf.filter(OL.created_at < hi)
        total, active, avg_ms, avg_cost = q.one()
        failed = qf.scalar() or 0
        users_new_q = db.query(func.count(User.id)).filter(User.created_at >= lo)
        if hi is not None:
            users_new_q = users_new_q.filter(User.created_at < hi)
        return {"calculations": total or 0, "failed": failed, "active_users": active or 0,
                "avg_time_ms": float(avg_ms) if avg_ms is not None else None,
                "avg_cost": float(avg_cost) if avg_cost is not None else None,
                "new_users": users_new_q.scalar() or 0}

    cur, prev = calc_block(start), calc_block(prev_start, start)
    success_rate = round((cur["calculations"] - cur["failed"]) / cur["calculations"] * 100, 1) if cur["calculations"] else None
    prev_rate = round((prev["calculations"] - prev["failed"]) / prev["calculations"] * 100, 1) if prev["calculations"] else None

    day_list = [(start + timedelta(days=i)).date() for i in range(days)]

    def series(col, extra=None, distinct=None):
        agg = func.count(func.distinct(distinct)) if distinct is not None else func.count()
        q = db.query(func.date(col), agg).filter(col >= start)
        if extra is not None:
            q = q.filter(extra)
        got = {str(d): c for d, c in q.group_by(func.date(col)).all()}
        return [got.get(str(d), 0) for d in day_list]

    new_users_series = series(User.created_at)
    users_before = db.query(func.count(User.id)).filter(User.created_at < start).scalar() or 0
    cumulative, run = [], users_before
    for n in new_users_series:
        run += n
        cumulative.append(run)

    tz_hour = func.extract("hour", func.timezone("Asia/Tehran", OL.created_at))
    hours = {int(h): c for h, c in db.query(tz_hour, func.count()).filter(OL.created_at >= start).group_by(tz_hour).all()}
    tz_dow = func.extract("dow", func.timezone("Asia/Tehran", OL.created_at))
    dow = {int(h): c for h, c in db.query(tz_dow, func.count()).filter(OL.created_at >= start).group_by(tz_dow).all()}
    # ترتیب هفتهٔ ایرانی: شنبه … جمعه (dow در PG: یکشنبه=۰ … شنبه=۶)
    by_weekday = [{"label": lbl, "count": dow.get(i, 0)} for lbl, i in
                  [("شنبه", 6), ("یکشنبه", 0), ("دوشنبه", 1), ("سه‌شنبه", 2), ("چهارشنبه", 3), ("پنج‌شنبه", 4), ("جمعه", 5)]]

    top_users = [
        {"id": uid, "name": f"{fn} {ln}", "count": c}
        for uid, fn, ln, c in db.query(User.id, User.first_name, User.last_name, func.count(OL.id))
        .join(OL, OL.user_id == User.id).filter(OL.created_at >= start)
        .group_by(User.id, User.first_name, User.last_name).order_by(func.count(OL.id).desc()).limit(6).all()
    ]
    top_plants = [
        {"label": name, "count": c}
        for name, c in db.query(Report.plant_name, func.count(Report.id)).filter(Report.plant_name.isnot(None), Report.plant_name != "")
        .group_by(Report.plant_name).order_by(func.count(Report.id).desc()).limit(8).all()
    ]
    # پرمصرف‌ترین کودها (از ۴۰۰ محاسبهٔ اخیرِ همین بازه)
    fert_counter: Dict[str, int] = {}
    for sel, weights in db.query(OL.fertilizers_selected, OL.optimized_weights).filter(OL.created_at >= start, OL.is_successful == True)\
            .order_by(OL.created_at.desc()).limit(400).all():  # noqa: E712
        try:
            used = {str(k) for k, v in (weights or {}).items() if v and float(v) > 0}
            for f in (sel or []):
                if str(f.get("id")) in used and f.get("name"):
                    fert_counter[f["name"]] = fert_counter.get(f["name"], 0) + 1
        except Exception:
            continue
    top_fertilizers = [{"label": k, "count": v} for k, v in sorted(fert_counter.items(), key=lambda x: -x[1])[:8]]

    opt_total = db.query(func.count(OL.id)).scalar() or 0
    return {
        "range_days": days,
        "users": {
            "total": total_users, "by_role": by_role, "by_status": by_status,
            "new_7d": db.query(func.count(User.id)).filter(User.created_at >= d7).scalar() or 0,
            "new_30d": db.query(func.count(User.id)).filter(User.created_at >= d30).scalar() or 0,
            "active_24h": db.query(func.count(User.id)).filter(User.last_login >= d1).scalar() or 0,
            "active_7d": db.query(func.count(User.id)).filter(User.last_login >= d7).scalar() or 0,
        },
        "content": {
            "reports": db.query(func.count(Report.id)).scalar() or 0,
            "system_fertilizers": db.query(func.count(Fertilizer.id)).filter(
                Fertilizer.is_system_default == True, Fertilizer.user_id == None).scalar() or 0,  # noqa: E712,E711
            "user_fertilizers": db.query(func.count(Fertilizer.id)).filter(Fertilizer.user_id != None).scalar() or 0,  # noqa: E711
            "ph_adjustments": db.query(func.count(PhAdjustment.id)).scalar() or 0,
        },
        # سازگار با نسخهٔ قبل + فیلدهای جدید
        "calculations": {
            "total": opt_total,
            "last_24h": db.query(func.count(OL.id)).filter(OL.created_at >= d1).scalar() or 0,
            "last_7d": db.query(func.count(OL.id)).filter(OL.created_at >= d7).scalar() or 0,
            "failed_7d": db.query(func.count(OL.id)).filter(OL.created_at >= d7, OL.is_successful == False).scalar() or 0,  # noqa: E712
        },
        "period": {
            "current": {**cur, "success_rate": success_rate},
            "previous": {**prev, "success_rate": prev_rate},
            "trend": {
                "calculations": _trend(cur["calculations"], prev["calculations"]),
                "new_users": _trend(cur["new_users"], prev["new_users"]),
                "active_users": _trend(cur["active_users"], prev["active_users"]),
                "failed": _trend(cur["failed"], prev["failed"]),
            },
        },
        "series": {
            "days": [str(d) for d in day_list],
            "new_users": new_users_series,
            "total_users": cumulative,
            "calculations": series(OL.created_at),
            "failed": series(OL.created_at, OL.is_successful == False),  # noqa: E712
            "active_users": series(OL.created_at, None, OL.user_id),
        },
        "by_hour": [hours.get(h, 0) for h in range(24)],
        "by_weekday": by_weekday,
        "top_users": top_users,
        "top_plants": top_plants,
        "top_fertilizers": top_fertilizers,
        "recent_users": [
            {"id": u.id, "name": u.full_name, "phone": u.phone_number, "role": u.role, "created_at": _iso(u.created_at)}
            for u in db.query(User).order_by(User.created_at.desc()).limit(8).all()
        ],
        "recent_security": [
            {"id": l.id, "event_type": l.event_type, "severity": l.severity, "user_id": l.user_id,
             "ip": l.ip_address, "created_at": _iso(l.created_at)}
            for l in db.query(SecurityLog).filter(SecurityLog.severity.in_(["WARNING", "ERROR", "CRITICAL"]))
            .order_by(SecurityLog.created_at.desc()).limit(8).all()
        ],
    }


# ============================================================
# 👥 مدیریت کاربران
# ============================================================
def _user_row(u: User, reports: int = 0, calcs: int = 0) -> dict:
    return {
        "id": u.id, "first_name": u.first_name, "last_name": u.last_name, "full_name": u.full_name,
        "phone_number": u.phone_number, "role": u.role, "status": u.status, "is_active": u.is_active,
        "status_reason": u.status_reason, "status_until": _iso(u.status_until),
        "created_at": _iso(u.created_at), "last_login": _iso(u.last_login), "last_ip": u.last_ip,
        "is_2fa_enabled": bool(u.is_2fa_enabled), "reports_count": reports, "calculations_count": calcs,
    }


def _get_user(db: Session, user_id: int) -> User:
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    return u


def _guard_not_self(admin: User, user: User) -> None:
    if admin.id == user.id:
        raise HTTPException(status_code=400, detail="این کار را نمی‌توانید روی حساب خودتان انجام دهید")


def _guard_last_admin(db: Session, user: User) -> None:
    """حذف/مسدود/تنزل آخرین ادمین فعال ممنوع است"""
    if user.role == "admin":
        others = db.query(func.count(User.id)).filter(
            User.role == "admin", User.status == "active", User.id != user.id).scalar() or 0
        if others < 1:
            raise HTTPException(status_code=400, detail="این آخرین مدیر فعال سیستم است و نمی‌توان آن را تغییر داد")


@router.get("/users")
def list_users(
    q: Optional[str] = None, role: Optional[str] = None, status_: Optional[str] = Query(None, alias="status"),
    new_days: Optional[int] = Query(None, ge=1, le=365), never_logged_in: Optional[bool] = None,
    two_fa: Optional[bool] = None,
    sort: str = Query("created_at"), direction: str = Query("desc"),
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(or_(User.first_name.ilike(term), User.last_name.ilike(term),
                                 User.phone_number.ilike(term),
                                 (User.first_name + " " + User.last_name).ilike(term)))
    if role in ROLES:
        query = query.filter(User.role == role)
    if status_ in ("active", "blocked", "banned"):
        query = query.filter(User.status == status_)
    if new_days:
        query = query.filter(User.created_at >= _now() - timedelta(days=new_days))
    if never_logged_in:
        query = query.filter(User.last_login == None)  # noqa: E711
    if two_fa is not None:
        query = query.filter(User.is_2fa_enabled == two_fa)
    sort_col = {"created_at": User.created_at, "last_login": User.last_login,
                "name": User.last_name, "role": User.role}.get(sort, User.created_at)
    query = query.order_by(sort_col.asc().nullslast() if direction == "asc" else sort_col.desc().nullslast(), User.id.desc())
    total, users = _page(query, page, page_size)

    ids = [u.id for u in users]
    rep = dict(db.query(Report.user_id, func.count(Report.id)).filter(Report.user_id.in_(ids)).group_by(Report.user_id).all()) if ids else {}
    cal = dict(db.query(OptimizationLog.user_id, func.count(OptimizationLog.id)).filter(OptimizationLog.user_id.in_(ids)).group_by(OptimizationLog.user_id).all()) if ids else {}
    return _paged([_user_row(u, rep.get(u.id, 0), cal.get(u.id, 0)) for u in users], total, page, page_size)


@router.get("/users/{user_id}")
def user_detail(user_id: int, db: Session = Depends(get_db)):
    u = _get_user(db, user_id)
    row = _user_row(u)
    row.update({
        "admin_note": u.admin_note, "failed_attempts": u.failed_attempts or 0,
        "locked_until": _iso(u.locked_until), "last_user_agent": u.last_user_agent,
        "status_changed_at": _iso(u.status_changed_at), "status_changed_by": u.status_changed_by,
        "counts": {
            "reports": db.query(func.count(Report.id)).filter(Report.user_id == u.id).scalar() or 0,
            "fertilizers": db.query(func.count(Fertilizer.id)).filter(Fertilizer.user_id == u.id).scalar() or 0,
            "calculations": db.query(func.count(OptimizationLog.id)).filter(OptimizationLog.user_id == u.id).scalar() or 0,
            "ph_adjustments": db.query(func.count(PhAdjustment.id)).filter(PhAdjustment.user_id == u.id).scalar() or 0,
            "active_sessions": db.query(func.count(UserSession.id)).filter(
                UserSession.user_id == u.id, UserSession.is_active == True,  # noqa: E712
                UserSession.expires_at > _now()).scalar() or 0,
        },
        "recent_security": [
            {"id": l.id, "event_type": l.event_type, "severity": l.severity, "ip": l.ip_address,
             "created_at": _iso(l.created_at)}
            for l in db.query(SecurityLog).filter(SecurityLog.user_id == u.id)
            .order_by(SecurityLog.created_at.desc()).limit(10).all()
        ],
        "recent_calculations": [
            {"id": o.id, "is_successful": o.is_successful, "cost_total": o.cost_total,
             "created_at": _iso(o.created_at)}
            for o in db.query(OptimizationLog).filter(OptimizationLog.user_id == u.id)
            .order_by(OptimizationLog.created_at.desc()).limit(5).all()
        ],
    })
    return row


class AdminUserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: str = "user"


@router.post("/users", status_code=201)
def create_user(body: AdminUserCreate, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if body.role not in ROLES:
        raise HTTPException(status_code=400, detail="نقش نامعتبر است")
    try:
        data = UserCreate(first_name=body.first_name, last_name=body.last_name,
                          phone_number=body.phone_number, password=body.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=_first_error(e))
    if db.query(User).filter(User.phone_number == data.phone_number).first():
        raise HTTPException(status_code=400, detail="این شماره تلفن قبلاً ثبت شده است")
    u = User(first_name=data.first_name, last_name=data.last_name, phone_number=data.phone_number,
             password_hash=get_password_hash(data.password), role=body.role, status="active", is_active=True)
    db.add(u)
    db.flush()
    audit(db, admin, request, "user.create", "user", u.id, u.full_name, {"role": body.role, "phone": u.phone_number})
    db.commit()
    return _user_row(u)


def _first_error(e: Exception) -> str:
    try:
        errs = e.errors()  # type: ignore[attr-defined]
        msg = errs[0].get("msg", "") if errs else ""
        return msg.replace("Value error, ", "") or "اطلاعات نامعتبر است"
    except Exception:
        return str(e) or "اطلاعات نامعتبر است"


class AdminUserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = None
    admin_note: Optional[str] = Field(None, max_length=2000)


@router.put("/users/{user_id}")
def update_user(user_id: int, body: AdminUserUpdate, request: Request, db: Session = Depends(get_db),
                admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    changes: Dict[str, Any] = {}
    try:
        if body.first_name is not None and body.first_name != u.first_name:
            changes["first_name"] = [u.first_name, validate_name(body.first_name)]
            u.first_name = changes["first_name"][1]
        if body.last_name is not None and body.last_name != u.last_name:
            changes["last_name"] = [u.last_name, validate_name(body.last_name)]
            u.last_name = changes["last_name"][1]
        if body.phone_number is not None and body.phone_number != u.phone_number:
            phone = validate_phone_number(body.phone_number)
            if db.query(User).filter(User.phone_number == phone, User.id != u.id).first():
                raise HTTPException(status_code=400, detail="این شماره تلفن برای کاربر دیگری ثبت شده است")
            changes["phone_number"] = [u.phone_number, phone]
            u.phone_number = phone
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if body.admin_note is not None and body.admin_note != (u.admin_note or ""):
        u.admin_note = body.admin_note.strip() or None
        changes["admin_note"] = True
    if changes:
        audit(db, admin, request, "user.update", "user", u.id, u.full_name, changes)
        db.commit()
    return _user_row(u)


class RoleBody(BaseModel):
    role: str


def _do_role(db: Session, admin: User, request: Request, u: User, role: str) -> None:
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="نقش نامعتبر است")
    if u.role == role:
        return
    if u.role == "admin":
        _guard_not_self(admin, u)
        _guard_last_admin(db, u)
    old = u.role
    u.role = role
    audit(db, admin, request, "user.role", "user", u.id, u.full_name, {"from": old, "to": role})


@router.put("/users/{user_id}/role")
def set_role(user_id: int, body: RoleBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    _do_role(db, admin, request, u, body.role)
    db.commit()
    return _user_row(u)


class BlockBody(BaseModel):
    reason: Optional[str] = Field(None, max_length=500)
    hours: Optional[int] = Field(None, ge=1, le=24 * 365)   # خالی = نامحدود


def _do_status(db: Session, admin: User, request: Request, u: User, new_status: str,
               reason: Optional[str], hours: Optional[int]) -> None:
    _guard_not_self(admin, u)
    _guard_last_admin(db, u)
    u.status = new_status
    u.is_active = False
    u.status_reason = (reason or "").strip() or None
    u.status_until = _now() + timedelta(hours=hours) if (new_status == "blocked" and hours) else None
    u.status_changed_at = _now()
    u.status_changed_by = admin.id
    db.query(UserSession).filter(UserSession.user_id == u.id, UserSession.is_active == True).update({"is_active": False})  # noqa: E712
    audit(db, admin, request, "user.ban" if new_status == "banned" else "user.block", "user", u.id, u.full_name,
          {"reason": u.status_reason, "until": _iso(u.status_until)})


def _do_restore(db: Session, admin: User, request: Request, u: User) -> None:
    prev = u.status
    u.status = "active"
    u.is_active = True
    u.status_reason = None
    u.status_until = None
    u.status_changed_at = _now()
    u.status_changed_by = admin.id
    u.failed_attempts = 0
    u.locked_until = None
    audit(db, admin, request, "user.restore", "user", u.id, u.full_name, {"from": prev})


@router.post("/users/{user_id}/block")
def block_user(user_id: int, body: BlockBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    _do_status(db, admin, request, u, "blocked", body.reason, body.hours)
    db.commit()
    return _user_row(u)


@router.post("/users/{user_id}/ban")
def ban_user(user_id: int, body: BlockBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    _do_status(db, admin, request, u, "banned", body.reason, None)
    db.commit()
    return _user_row(u)


@router.post("/users/{user_id}/restore")
def restore_user(user_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    _do_restore(db, admin, request, u)
    db.commit()
    return _user_row(u)


class ResetPasswordBody(BaseModel):
    new_password: Optional[str] = Field(None, max_length=100)   # خالی ⇒ رمز تصادفی ساخته می‌شود


def _random_password(n: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(n - 1)) + secrets.choice("!@#$%&*")
        if any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
            return pw


@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: int, body: ResetPasswordBody, request: Request, db: Session = Depends(get_db),
                   admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    pw = body.new_password or _random_password()
    try:
        validate_password_strength(pw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    u.password_hash = get_password_hash(pw)
    u.failed_attempts = 0
    u.locked_until = None
    db.query(UserSession).filter(UserSession.user_id == u.id, UserSession.is_active == True).update({"is_active": False})  # noqa: E712
    audit(db, admin, request, "user.reset_password", "user", u.id, u.full_name, None)
    db.commit()
    # رمز فقط همین یک‌بار نمایش داده می‌شود
    return {"ok": True, "password": pw if not body.new_password else None}


@router.post("/users/{user_id}/revoke-sessions")
def revoke_sessions(user_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    delete_user_sessions(u.id, db)
    audit(db, admin, request, "user.revoke_sessions", "user", u.id, u.full_name, None)
    db.commit()
    return {"ok": True}


@router.post("/users/{user_id}/unlock")
def unlock_user(user_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    u.failed_attempts = 0
    u.locked_until = None
    audit(db, admin, request, "user.unlock", "user", u.id, u.full_name, None)
    db.commit()
    return _user_row(u)


@router.post("/users/{user_id}/disable-2fa")
def disable_2fa(user_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    u.is_2fa_enabled = False
    u.totp_secret = None
    u.backup_codes = None
    audit(db, admin, request, "user.disable_2fa", "user", u.id, u.full_name, None)
    db.commit()
    return _user_row(u)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    u = _get_user(db, user_id)
    _guard_not_self(admin, u)
    _guard_last_admin(db, u)
    label, phone = u.full_name, u.phone_number
    audit(db, admin, request, "user.delete", "user", u.id, label, {"phone": phone, "role": u.role})
    db.delete(u)   # گزارش‌ها، کودها، نشست‌ها و ... با cascade حذف می‌شوند
    db.commit()
    return {"ok": True}


class BulkBody(BaseModel):
    ids: List[int] = Field(..., min_length=1, max_length=200)
    action: str                      # block | ban | restore | set_role | delete | revoke_sessions
    reason: Optional[str] = None
    hours: Optional[int] = None
    role: Optional[str] = None


@router.post("/users/bulk")
def bulk_users(body: BulkBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if body.action not in ("block", "ban", "restore", "set_role", "delete", "revoke_sessions"):
        raise HTTPException(status_code=400, detail="عملیات نامعتبر است")
    done: List[int] = []
    skipped: List[dict] = []
    for uid in dict.fromkeys(body.ids):
        u = db.query(User).filter(User.id == uid).first()
        if not u:
            skipped.append({"id": uid, "reason": "کاربر پیدا نشد"})
            continue
        try:
            if body.action == "block":
                _do_status(db, admin, request, u, "blocked", body.reason, body.hours)
            elif body.action == "ban":
                _do_status(db, admin, request, u, "banned", body.reason, None)
            elif body.action == "restore":
                _do_restore(db, admin, request, u)
            elif body.action == "set_role":
                _do_role(db, admin, request, u, body.role or "")
            elif body.action == "revoke_sessions":
                db.query(UserSession).filter(UserSession.user_id == u.id).update({"is_active": False})
                audit(db, admin, request, "user.revoke_sessions", "user", u.id, u.full_name, None)
            elif body.action == "delete":
                _guard_not_self(admin, u)
                _guard_last_admin(db, u)
                audit(db, admin, request, "user.delete", "user", u.id, u.full_name, {"phone": u.phone_number, "bulk": True})
                db.delete(u)
            db.flush()
            done.append(uid)
        except HTTPException as e:
            skipped.append({"id": uid, "reason": e.detail})
    db.commit()
    return {"done": done, "skipped": skipped}


# ============================================================
# 🧪 کودهای سیستمی (فهرست شرکتی)
# ============================================================
def _fert_row(f: Fertilizer) -> dict:
    return {
        "id": f.id, "name": f.name, "brand": f.brand, "category": f.category, "form": f.form,
        "concentration": f.concentration, "elements": f.elements or {}, "price_per_kg": f.price_per_kg,
        "is_acid": bool(f.is_acid), "is_base": bool(f.is_base), "acid_type": f.acid_type, "formula": f.formula,
        "ph_params": f.ph_params, "label_values": f.label_values, "density_g_ml": f.density_g_ml,
        "price_unit": f.price_unit, "description": f.description,
        "updated_at": _iso(f.updated_at), "created_at": _iso(f.created_at),
    }


def _system_fert(db: Session, fert_id: int) -> Fertilizer:
    f = db.query(Fertilizer).filter(Fertilizer.id == fert_id, Fertilizer.is_system_default == True,  # noqa: E712
                                    Fertilizer.user_id == None).first()  # noqa: E711
    if not f:
        raise HTTPException(status_code=404, detail="کود سیستمی پیدا نشد")
    return f


@router.get("/fertilizers")
def list_system_fertilizers(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Fertilizer).filter(Fertilizer.is_system_default == True, Fertilizer.user_id == None)  # noqa: E712,E711
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(or_(Fertilizer.name.ilike(term), Fertilizer.brand.ilike(term), Fertilizer.formula.ilike(term)))
    items = query.order_by(Fertilizer.name.asc()).limit(1000).all()
    return {"items": [_fert_row(f) for f in items], "total": len(items)}


@router.post("/fertilizers", status_code=201)
def create_system_fertilizer(body: FertilizerCreate, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if db.query(Fertilizer).filter(Fertilizer.name == body.name, Fertilizer.is_system_default == True,  # noqa: E712
                                   Fertilizer.user_id == None).first():  # noqa: E711
        raise HTTPException(status_code=400, detail="کود سیستمی با این نام قبلاً وجود دارد")
    data = body.dict(exclude={"is_system_default", "source_system_id"})
    f = Fertilizer(**data, user_id=None, is_system_default=True, source_system_id=None)
    db.add(f)
    db.flush()
    audit(db, admin, request, "fertilizer.create", "fertilizer", f.id, f.name, {"price_per_kg": f.price_per_kg})
    db.commit()
    return _fert_row(f)


@router.put("/fertilizers/{fert_id}")
def update_system_fertilizer(fert_id: int, body: FertilizerUpdate, request: Request, db: Session = Depends(get_db),
                             admin: User = Depends(require_admin)):
    f = _system_fert(db, fert_id)
    data = body.dict(exclude_unset=True, exclude={"is_system_default", "source_system_id"})
    if "name" in data and data["name"] != f.name:
        if db.query(Fertilizer).filter(Fertilizer.name == data["name"], Fertilizer.is_system_default == True,  # noqa: E712
                                       Fertilizer.user_id == None, Fertilizer.id != f.id).first():  # noqa: E711
            raise HTTPException(status_code=400, detail="کود سیستمی دیگری با این نام وجود دارد")
    changed = {}
    for k, v in data.items():
        if getattr(f, k) != v:
            changed[k] = [getattr(f, k), v]
            setattr(f, k, v)
    if changed:
        audit(db, admin, request, "fertilizer.update", "fertilizer", f.id, f.name, {"fields": list(changed.keys())})
        db.commit()
    return _fert_row(f)


@router.delete("/fertilizers/{fert_id}")
def delete_system_fertilizer(fert_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    f = _system_fert(db, fert_id)
    audit(db, admin, request, "fertilizer.delete", "fertilizer", f.id, f.name, None)
    db.delete(f)
    db.commit()
    return {"ok": True}


class BulkPriceBody(BaseModel):
    percent: float = Field(..., ge=-90, le=500)       # +10 = ده درصد گران‌تر
    ids: Optional[List[int]] = None                   # خالی = همهٔ کودهای سیستمی
    form: Optional[str] = None                        # فقط یک شکل (مثلاً liquid)


@router.post("/fertilizers/bulk-price")
def bulk_price(body: BulkPriceBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    q = db.query(Fertilizer).filter(Fertilizer.is_system_default == True, Fertilizer.user_id == None)  # noqa: E712,E711
    if body.ids:
        q = q.filter(Fertilizer.id.in_(body.ids))
    if body.form:
        q = q.filter(Fertilizer.form == body.form)
    factor = 1 + body.percent / 100.0
    n = 0
    for f in q.all():
        if f.price_per_kg:
            f.price_per_kg = round(float(f.price_per_kg) * factor)
            n += 1
    audit(db, admin, request, "fertilizer.bulk_price", "fertilizer", None, f"{body.percent:+g}٪",
          {"percent": body.percent, "count": n, "ids": body.ids, "form": body.form})
    db.commit()
    return {"updated": n}


# ============================================================
# 🧮 لاگ محاسبه‌ها
# ============================================================
@router.get("/calculations")
def list_calculations(
    user_id: Optional[int] = None, success: Optional[bool] = None, has_warnings: Optional[bool] = None,
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db),
):
    q = db.query(OptimizationLog, User).join(User, User.id == OptimizationLog.user_id)
    if user_id:
        q = q.filter(OptimizationLog.user_id == user_id)
    if success is not None:
        q = q.filter(OptimizationLog.is_successful == success)
    if has_warnings is True:
        q = q.filter(OptimizationLog.warnings.isnot(None), func.json_array_length(OptimizationLog.warnings) > 0)
    q = q.order_by(OptimizationLog.created_at.desc())
    total = q.count()
    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    items = [{
        "id": o.id, "user_id": u.id, "user_name": u.full_name, "phone": u.phone_number,
        "is_successful": o.is_successful, "cost_total": o.cost_total, "residual_error": o.residual_error,
        "convergence_time_ms": o.convergence_time_ms, "fertilizers_count": len(o.fertilizers_selected or []),
        "warnings_count": len(o.warnings or []) if isinstance(o.warnings, list) else 0,
        "error_message": o.error_message, "created_at": _iso(o.created_at),
    } for o, u in rows]
    return _paged(items, total, page, page_size)


@router.get("/calculations/{log_id}")
def calculation_detail(log_id: int, db: Session = Depends(get_db)):
    o = db.query(OptimizationLog).filter(OptimizationLog.id == log_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="لاگ پیدا نشد")
    u = db.query(User).filter(User.id == o.user_id).first()
    return {
        "id": o.id, "user": {"id": o.user_id, "name": u.full_name if u else None, "phone": u.phone_number if u else None},
        "target_values": o.target_values, "water_values": o.water_values, "options": o.optimization_options,
        "fertilizers_selected": o.fertilizers_selected, "weights": o.optimized_weights,
        "final_concentrations": o.final_concentrations, "ion_balance": o.ion_balance,
        "warnings": o.warnings, "suggestions": o.suggestions, "residual_error": o.residual_error,
        "cost_total": o.cost_total, "iterations": o.iterations, "convergence_time_ms": o.convergence_time_ms,
        "is_successful": o.is_successful, "error_message": o.error_message, "created_at": _iso(o.created_at),
    }


# ============================================================
# 🔐 لاگ امنیتی و لاگ مدیریتی
# ============================================================
@router.get("/security-logs")
def security_logs(
    event_type: Optional[str] = None, severity: Optional[str] = None, user_id: Optional[int] = None,
    q: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(SecurityLog)
    if event_type:
        query = query.filter(SecurityLog.event_type == event_type)
    if severity:
        query = query.filter(SecurityLog.severity == severity)
    if user_id:
        query = query.filter(SecurityLog.user_id == user_id)
    if q:
        query = query.filter(or_(SecurityLog.ip_address.ilike(f"%{q}%"), SecurityLog.endpoint.ilike(f"%{q}%")))
    total, logs = _page(query.order_by(SecurityLog.created_at.desc()), page, page_size)
    types = [t for (t,) in db.query(SecurityLog.event_type).distinct().order_by(SecurityLog.event_type).all()]
    return {**_paged([{
        "id": l.id, "event_type": l.event_type, "severity": l.severity, "user_id": l.user_id, "ip": l.ip_address,
        "endpoint": l.endpoint, "method": l.method, "details": l.details, "error": l.error_message,
        "created_at": _iso(l.created_at)} for l in logs], total, page, page_size), "event_types": types}


@router.get("/audit")
def audit_log(
    action: Optional[str] = None, admin_id: Optional[int] = None,
    page: int = Query(1, ge=1), page_size: int = Query(30, ge=1, le=100), db: Session = Depends(get_db),
):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"{action}%"))
    if admin_id:
        query = query.filter(AuditLog.admin_id == admin_id)
    total, rows = _page(query.order_by(AuditLog.created_at.desc()), page, page_size)
    return _paged([{
        "id": a.id, "admin_id": a.admin_id, "admin_name": a.admin_name, "action": a.action,
        "target_type": a.target_type, "target_id": a.target_id, "target_label": a.target_label,
        "details": a.details, "ip": a.ip_address, "created_at": _iso(a.created_at)} for a in rows], total, page, page_size)


# ============================================================
# 📢 اعلان‌ها
# ============================================================
class AnnouncementBody(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    body: Optional[str] = Field(None, max_length=2000)
    level: str = Field("info", pattern="^(info|success|warning|danger)$")
    audience: str = Field("all", pattern="^(all|user|plus)$")
    is_active: bool = True
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


def _ann_row(a: Announcement) -> dict:
    return {"id": a.id, "title": a.title, "body": a.body, "level": a.level, "audience": a.audience,
            "is_active": a.is_active, "starts_at": _iso(a.starts_at), "ends_at": _iso(a.ends_at),
            "created_at": _iso(a.created_at)}


@router.get("/announcements")
def list_announcements(db: Session = Depends(get_db)):
    return {"items": [_ann_row(a) for a in db.query(Announcement).order_by(Announcement.created_at.desc()).limit(200).all()]}


@router.post("/announcements", status_code=201)
def create_announcement(body: AnnouncementBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    a = Announcement(**body.dict(), created_by=admin.id)
    db.add(a)
    db.flush()
    audit(db, admin, request, "announcement.create", "announcement", a.id, a.title, None)
    db.commit()
    return _ann_row(a)


@router.put("/announcements/{ann_id}")
def update_announcement(ann_id: int, body: AnnouncementBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    a = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="اعلان پیدا نشد")
    for k, v in body.dict().items():
        setattr(a, k, v)
    audit(db, admin, request, "announcement.update", "announcement", a.id, a.title, None)
    db.commit()
    return _ann_row(a)


@router.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    a = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="اعلان پیدا نشد")
    audit(db, admin, request, "announcement.delete", "announcement", a.id, a.title, None)
    db.delete(a)
    db.commit()
    return {"ok": True}


# ============================================================
# ⚙️ تنظیمات سیستم
# ============================================================
class SettingsBody(BaseModel):
    maintenance_enabled: Optional[bool] = None
    maintenance_message: Optional[str] = Field(None, max_length=300)
    registration_enabled: Optional[bool] = None
    registration_message: Optional[str] = Field(None, max_length=300)


def _read_settings(db: Session) -> dict:
    data = {r.key: r.value for r in db.query(AppSetting).all()}
    m, r = data.get("maintenance") or {}, data.get("registration") or {}
    return {
        "maintenance_enabled": bool(m.get("enabled")), "maintenance_message": m.get("message") or "",
        "registration_enabled": r.get("enabled") is not False, "registration_message": r.get("message") or "",
    }


def _put_setting(db: Session, admin: User, key: str, value: dict) -> None:
    row = db.query(AppSetting).filter(AppSetting.key == key).first()
    if row:
        row.value = value
        row.updated_by = admin.id
    else:
        db.add(AppSetting(key=key, value=value, updated_by=admin.id))


@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    return _read_settings(db)


@router.put("/settings")
def update_settings(body: SettingsBody, request: Request, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    cur = _read_settings(db)
    new = {**cur, **{k: v for k, v in body.dict().items() if v is not None}}
    _put_setting(db, admin, "maintenance", {"enabled": new["maintenance_enabled"], "message": new["maintenance_message"]})
    _put_setting(db, admin, "registration", {"enabled": new["registration_enabled"], "message": new["registration_message"]})
    changed = {k: new[k] for k in new if new[k] != cur[k]}
    if changed:
        audit(db, admin, request, "setting.update", "setting", None, ",".join(changed.keys()), changed)
    db.commit()
    invalidate_settings_cache()
    return _read_settings(db)


# ============================================================
# 🩺 سلامت سیستم
# ============================================================
@router.get("/system")
def system_info(db: Session = Depends(get_db)):
    db_ok, db_size = True, None
    try:
        db.execute(text("SELECT 1"))
        db_size = db.execute(text("SELECT pg_database_size(current_database())")).scalar()
    except Exception as e:  # pragma: no cover
        db_ok = False
        db.rollback()
        logger.error(f"health db check failed: {e}")
    return {
        "app_name": settings.APP_NAME, "version": settings.APP_VERSION, "debug": settings.DEBUG,
        "python": platform.python_version(), "uptime_seconds": int(time.time() - _STARTED_AT),
        "database": {"ok": db_ok, "size_bytes": db_size},
        "active_sessions": db.query(func.count(UserSession.id)).filter(
            UserSession.is_active == True, UserSession.expires_at > _now()).scalar() or 0,  # noqa: E712
        "server_time": _now().isoformat(),
    }
