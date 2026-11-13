# backend/app/routes/shop.py
"""🛒 فروشگاه کاربر: کالاها (کودهای سیستمی)، سبد خرید، ثبت سفارش، رسید کارت‌به‌کارت"""
from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Fertilizer, ShopCart, ShopOrder, User
from app.permissions import require_perm
from app.shop_common import (effective_price, load_shop_settings, new_order_code, order_row,
                             shop_product, unit_label)

shop_router = APIRouter(prefix="/shop", tags=["Shop"])

MAX_RECEIPT_CHARS = 4_000_000   # حدود ۳ مگابایت تصویر


def _enabled(db: Session) -> dict:
    cfg = load_shop_settings(db)
    if not cfg["enabled"]:
        raise HTTPException(status_code=403, detail="فروشگاه موقتاً غیرفعال است")
    return cfg


def _products_query(db: Session):
    return db.query(Fertilizer).filter(Fertilizer.is_system_default == True, Fertilizer.user_id == None,  # noqa: E712,E711
                                       Fertilizer.shop_enabled == True)                                     # noqa: E712


class CartItem(BaseModel):
    fertilizer_id: int
    qty: float = Field(..., gt=0, le=100000)


class CartBody(BaseModel):
    items: List[CartItem] = Field(default_factory=list, max_length=80)
    note: Optional[str] = Field(None, max_length=500)


def _merge(items: List[CartItem]) -> dict:
    merged: dict = {}
    for it in items:
        merged[it.fertilizer_id] = round(merged.get(it.fertilizer_id, 0) + it.qty, 3)
    return merged


def _priced(db: Session, cfg: dict, merged: dict, strict: bool):
    """سطرهای قیمت‌گذاری‌شده؛ strict=True برای ثبت سفارش (خطا به‌جای حذف بی‌صدا)"""
    prods = {f.id: f for f in _products_query(db).filter(Fertilizer.id.in_(list(merged.keys()) or [0])).all()}
    lines, dropped = [], []
    for fid, qty in merged.items():
        f = prods.get(fid)
        if not f or effective_price(f) <= 0:
            if strict:
                raise HTTPException(status_code=400, detail="یکی از کودهای سبد دیگر در فروشگاه موجود نیست")
            dropped.append(fid)
            continue
        if f.shop_min_qty and qty < f.shop_min_qty:
            if strict:
                raise HTTPException(status_code=400, detail=f"حداقل سفارش «{f.name}» {f.shop_min_qty:g} {unit_label(f)} است")
        if f.shop_stock is not None and qty > f.shop_stock:
            if strict:
                raise HTTPException(status_code=400, detail=f"موجودی «{f.name}» فقط {f.shop_stock:g} {unit_label(f)} است")
        price = effective_price(f)
        lines.append({"fertilizer_id": f.id, "name": f.name, "formula": f.formula, "unit": unit_label(f),
                      "qty": qty, "unit_price": price, "line_total": round(price * qty)})
    subtotal = sum(l["line_total"] for l in lines)
    ship = float(cfg["shipping_fee"] or 0)
    if cfg["free_shipping_over"] and subtotal >= float(cfg["free_shipping_over"]):
        ship = 0.0
    if not lines:
        ship = 0.0
    return lines, dropped, subtotal, ship


@shop_router.get("/info")
def shop_info(db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    cfg = load_shop_settings(db)
    # شمارهٔ کارت فقط در مرحلهٔ پرداخت (از مسیر سفارش) داده می‌شود
    return {k: cfg[k] for k in ("enabled", "shipping_fee", "free_shipping_over", "min_order_total",
                                "currency_label", "shop_note", "require_address")}


@shop_router.get("/items")
def shop_items(q: Optional[str] = None, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    _enabled(db)
    query = _products_query(db)
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(Fertilizer.name.ilike(term) | Fertilizer.formula.ilike(term) | Fertilizer.brand.ilike(term))
    items = [shop_product(f) for f in query.order_by(Fertilizer.name.asc()).limit(500).all() if effective_price(f) > 0]
    return {"items": items, "total": len(items)}


@shop_router.get("/cart")
def get_cart(db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    cfg = _enabled(db)
    cart = db.get(ShopCart, user.id)
    merged = _merge([CartItem(**i) for i in (cart.items if cart else [])]) if cart else {}
    lines, dropped, subtotal, ship = _priced(db, cfg, merged, strict=False)
    return {"items": lines, "dropped": dropped, "subtotal": subtotal, "shipping": ship, "total": subtotal + ship,
            "note": cart.note if cart else None}


@shop_router.put("/cart")
def put_cart(body: CartBody, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    cfg = _enabled(db)
    merged = _merge(body.items)
    cart = db.get(ShopCart, user.id)
    payload = [{"fertilizer_id": k, "qty": v} for k, v in merged.items()]
    if cart:
        cart.items, cart.note = payload, body.note
    else:
        db.add(ShopCart(user_id=user.id, items=payload, note=body.note))
    db.commit()
    return get_cart(db, user)


class AddBody(BaseModel):
    items: List[CartItem] = Field(..., min_length=1, max_length=80)
    replace: bool = False


@shop_router.post("/cart/add")
def add_to_cart(body: AddBody, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    """افزودن گروهی (مثلاً از نتیجهٔ محاسبهٔ کود)؛ replace=True سبد قبلی را جایگزین می‌کند"""
    _enabled(db)
    cart = db.get(ShopCart, user.id)
    cur = {} if (body.replace or not cart) else _merge([CartItem(**i) for i in cart.items])
    for k, v in _merge(body.items).items():
        cur[k] = round(cur.get(k, 0) + v, 3)
    payload = [{"fertilizer_id": k, "qty": v} for k, v in cur.items()]
    if cart:
        cart.items = payload
    else:
        db.add(ShopCart(user_id=user.id, items=payload))
    db.commit()
    return get_cart(db, user)


class AddressBody(BaseModel):
    receiver: str = Field(..., min_length=2, max_length=80)
    phone: str = Field(..., min_length=7, max_length=15)
    province: Optional[str] = Field(None, max_length=40)
    city: Optional[str] = Field(None, max_length=40)
    address: str = Field(..., min_length=5, max_length=400)
    postal_code: Optional[str] = Field(None, max_length=12)


class CheckoutBody(BaseModel):
    address: Optional[AddressBody] = None
    customer_note: Optional[str] = Field(None, max_length=500)


@shop_router.post("/orders", status_code=201)
def checkout(body: CheckoutBody, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    cfg = _enabled(db)
    cart = db.get(ShopCart, user.id)
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="سبد خرید خالی است")
    if cfg["require_address"] and not body.address:
        raise HTTPException(status_code=400, detail="آدرس تحویل الزامی است")
    lines, _, subtotal, ship = _priced(db, cfg, _merge([CartItem(**i) for i in cart.items]), strict=True)
    if cfg["min_order_total"] and subtotal < float(cfg["min_order_total"]):
        raise HTTPException(status_code=400, detail=f"حداقل مبلغ سفارش {int(cfg['min_order_total']):,} {cfg['currency_label']} است")
    order = ShopOrder(code=new_order_code(db), user_id=user.id, user_name=user.full_name, phone_number=user.phone_number,
                      status="awaiting_payment", items=lines, subtotal=subtotal, shipping=ship, total=subtotal + ship,
                      customer_note=body.customer_note or cart.note,
                      address=body.address.dict() if body.address else None)
    db.add(order)
    cart.items, cart.note = [], None
    db.commit()
    return order_row(order)


@shop_router.get("/orders")
def my_orders(db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    rows = db.query(ShopOrder).filter(ShopOrder.user_id == user.id).order_by(ShopOrder.created_at.desc()).limit(100).all()
    return {"items": [order_row(o) for o in rows]}


def _mine(db: Session, user: User, order_id: int) -> ShopOrder:
    o = db.query(ShopOrder).filter(ShopOrder.id == order_id, ShopOrder.user_id == user.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="سفارش پیدا نشد")
    return o


@shop_router.get("/orders/{order_id}")
def my_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    o = _mine(db, user, order_id)
    d = order_row(o, with_receipt=True)
    if o.status in ("awaiting_payment", "awaiting_review", "rejected"):
        cfg = load_shop_settings(db)
        d["payment"] = {k: cfg[k] for k in ("card_number", "card_holder", "bank_name", "payment_note", "currency_label")}
    return d


class ReceiptBody(BaseModel):
    image: str = Field(..., min_length=50)
    last4: Optional[str] = Field(None, max_length=4)
    paid_amount: Optional[float] = Field(None, ge=0)
    note: Optional[str] = Field(None, max_length=300)


@shop_router.post("/orders/{order_id}/receipt")
def upload_receipt(order_id: int, body: ReceiptBody, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    o = _mine(db, user, order_id)
    if o.status not in ("awaiting_payment", "awaiting_review", "rejected"):
        raise HTTPException(status_code=400, detail="برای این سفارش دیگر نمی‌توان رسید ارسال کرد")
    if not re.match(r"^data:image/(png|jpe?g|webp);base64,[A-Za-z0-9+/=]+$", body.image) or len(body.image) > MAX_RECEIPT_CHARS:
        raise HTTPException(status_code=400, detail="تصویر رسید معتبر نیست یا حجم آن از ۳ مگابایت بیشتر است")
    o.receipt_image = body.image
    o.receipt_info = {"last4": body.last4, "paid_amount": body.paid_amount, "note": body.note}
    o.receipt_at = datetime.now(timezone.utc)
    o.status = "awaiting_review"
    o.reject_reason = None
    db.commit()
    return order_row(o)


@shop_router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    o = _mine(db, user, order_id)
    if o.status not in ("awaiting_payment", "awaiting_review", "rejected"):
        raise HTTPException(status_code=400, detail="این سفارش دیگر قابل لغو نیست")
    o.status = "cancelled"
    db.commit()
    return order_row(o)


@shop_router.post("/orders/{order_id}/reopen")
def reopen_to_cart(order_id: int, db: Session = Depends(get_db), user: User = Depends(require_perm("shop"))):
    """بازگرداندن اقلام یک سفارش لغو/ردشده به سبد برای ویرایش و ثبت دوباره"""
    o = _mine(db, user, order_id)
    if o.status not in ("cancelled", "rejected"):
        raise HTTPException(status_code=400, detail="فقط سفارش لغوشده یا ردشده به سبد برمی‌گردد")
    payload = [{"fertilizer_id": i["fertilizer_id"], "qty": i["qty"]} for i in (o.items or [])]
    cart = db.get(ShopCart, user.id)
    if cart:
        cart.items = payload
    else:
        db.add(ShopCart(user_id=user.id, items=payload))
    db.commit()
    return {"ok": True}
