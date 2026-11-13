# backend/app/permissions.py
"""
🔑 دسترسی‌های نقش‌ها (قابل تنظیم از پنل مدیریت)
مقدارها در جدول app_settings با کلید «permissions» ذخیره می‌شوند: {role: {perm: bool}}.
نقش admin همیشه همهٔ دسترسی‌ها را دارد و قابل محدود شدن نیست.
"""
from __future__ import annotations

from typing import Dict

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AppSetting, User
from app.security import get_current_user

# کلید → (عنوان، توضیح، پیش‌فرض کاربر معمولی، پیش‌فرض کاربر پلاس)
PERMISSIONS: Dict[str, dict] = {
    "interpretation":      {"label": "تفسیر داده‌ها",            "hint": "دیدن تب تفسیر داده‌ها",                       "user": False, "plus": True},
    "manual_fertilizer":   {"label": "ورود دستی کود",             "hint": "افزودن کود شخصی با مودال پایگاه داده",         "user": False, "plus": True},
    "advanced_fertilizer": {"label": "حالت پیشرفتهٔ مودال کود",    "hint": "نوشتن ترکیب و استخراج عناصر در مودال کود",     "user": False, "plus": True},
    "widgets":             {"label": "ابزارک‌ها",                  "hint": "دیدن تب ابزارک‌ها",                            "user": True,  "plus": True},
    "widget_composition":  {"label": "ابزارک ترکیب کودی",          "hint": "ابزارک تحلیل ترکیب (نسخهٔ مستقل حالت پیشرفته)", "user": True,  "plus": True},
    "ph_calculator":       {"label": "ماشین‌حساب pH",              "hint": "دیدن تب pH",                                   "user": True,  "plus": True},
    "pdf_export":          {"label": "خروجی PDF",                  "hint": "دریافت PDF نتیجهٔ محاسبه",                     "user": True,  "plus": True},
    "recipes_personal":    {"label": "رسپی شخصی",                  "hint": "ساخت و ذخیرهٔ رسپی شخصی",                      "user": True,  "plus": True},
    "shop":                {"label": "فروشگاه و سبد خرید",         "hint": "دیدن فروشگاه و ثبت سفارش",                     "user": True,  "plus": True},
}

KEY = "permissions"


def defaults() -> Dict[str, Dict[str, bool]]:
    return {
        "user": {k: v["user"] for k, v in PERMISSIONS.items()},
        "plus": {k: v["plus"] for k, v in PERMISSIONS.items()},
    }


def load_matrix(db: Session) -> Dict[str, Dict[str, bool]]:
    """ماتریس نقش×دسترسی (پیش‌فرض‌ها + تنظیم‌های ذخیره‌شده)"""
    base = defaults()
    row = db.query(AppSetting).filter(AppSetting.key == KEY).first()
    saved = (row.value or {}) if row else {}
    for role in ("user", "plus"):
        for k, v in (saved.get(role) or {}).items():
            if k in PERMISSIONS and isinstance(v, bool):
                base[role][k] = v
    return base


def user_permissions(db: Session, user: User) -> Dict[str, bool]:
    if user.role == "admin":
        return {k: True for k in PERMISSIONS}
    matrix = load_matrix(db)
    return dict(matrix.get(user.role) or matrix["user"])


def require_perm(key: str):
    """وابستگی FastAPI برای قفل کردن یک مسیر پشت دسترسی"""
    def dep(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        if not user_permissions(db, user).get(key, False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="این امکان برای نوع حساب شما فعال نیست. برای دسترسی با پشتیبانی تماس بگیرید.")
        return user
    return dep
