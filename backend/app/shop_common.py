# backend/app/shop_common.py
"""ابزارهای مشترک فروشگاه (تنظیمات، قیمت مؤثر، ردیف سفارش) برای مسیرهای کاربر و ادمین"""
from __future__ import annotations

import secrets
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models import AppSetting, Fertilizer, ShopOrder

SHOP_KEY = "shop"

DEFAULT_SHOP: Dict[str, Any] = {
    "enabled": True,
    "card_number": "",
    "card_holder": "",
    "bank_name": "",
    "payment_note": "پس از واریز، تصویر رسید را در همین صفحه بارگذاری کنید. سفارش پس از بررسی تأیید می‌شود.",
    "shipping_fee": 0,
    "free_shipping_over": 0,
    "min_order_total": 0,
    "receipt_required": True,
    "require_address": True,
    "currency_label": "تومان",
    "shop_note": "",
}

ORDER_STATUSES = {
    "awaiting_payment": "در انتظار پرداخت",
    "awaiting_review": "در انتظار بررسی رسید",
    "approved": "پرداخت تأیید شد",
    "processing": "در حال آماده‌سازی",
    "shipped": "ارسال شد",
    "completed": "تکمیل شد",
    "rejected": "رد شد",
    "cancelled": "لغو شد",
}


def load_shop_settings(db: Session) -> Dict[str, Any]:
    row = db.query(AppSetting).filter(AppSetting.key == SHOP_KEY).first()
    out = dict(DEFAULT_SHOP)
    if row and isinstance(row.value, dict):
        for k, v in row.value.items():
            if k in DEFAULT_SHOP:
                out[k] = v
    return out


def effective_price(f: Fertilizer) -> float:
    return float(f.shop_price if f.shop_price is not None else (f.price_per_kg or 0))


def unit_label(f: Fertilizer) -> str:
    return "لیتر" if (f.price_unit or "").strip().lower() in ("l", "lit", "liter", "litre") else "کیلوگرم"


def shop_product(f: Fertilizer) -> dict:
    return {
        "id": f.id, "name": f.name, "brand": f.brand, "category": f.category, "form": f.form,
        "formula": f.formula, "elements": f.elements or {}, "concentration": f.concentration,
        "price": effective_price(f), "unit": unit_label(f), "stock": f.shop_stock,
        "min_qty": f.shop_min_qty, "description": f.description,
    }


def order_row(o: ShopOrder, with_receipt: bool = False) -> dict:
    d = {
        "id": o.id, "code": o.code, "user_id": o.user_id, "user_name": o.user_name, "phone_number": o.phone_number,
        "status": o.status, "status_label": ORDER_STATUSES.get(o.status, o.status), "items": o.items or [],
        "subtotal": o.subtotal, "shipping": o.shipping, "total": o.total, "customer_note": o.customer_note,
        "address": o.address, "has_receipt": bool(o.receipt_image), "receipt_info": o.receipt_info,
        "receipt_at": o.receipt_at.isoformat() if o.receipt_at else None, "admin_note": o.admin_note,
        "reject_reason": o.reject_reason, "tracking_code": o.tracking_code,
        "created_at": o.created_at.isoformat() if o.created_at else None,
        "updated_at": o.updated_at.isoformat() if o.updated_at else None,
    }
    if with_receipt:
        d["receipt_image"] = o.receipt_image
    return d


def new_order_code(db: Session) -> str:
    for _ in range(20):
        code = "FT-" + "".join(secrets.choice("0123456789") for _ in range(6))
        if not db.query(ShopOrder.id).filter(ShopOrder.code == code).first():
            return code
    return "FT-" + secrets.token_hex(4).upper()
