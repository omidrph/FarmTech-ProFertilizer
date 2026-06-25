# backend/app/routes/__init__.py
"""
ماژول مسیرهای API
این فایل تمام routerها را ترکیب و export می‌کند
"""
from fastapi import APIRouter
from .auth import auth_router
from .users import users_router
from .reports import reports_router
from .fertilizers import fertilizers_router
from .water_analysis import water_analysis_router
from .calculations import calculations_router
from .recipes import recipes_router  # 🆕 اضافه شد

# ایجاد router اصلی
router = APIRouter()

# افزودن همه routerها به router اصلی
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(reports_router)
router.include_router(fertilizers_router)
router.include_router(water_analysis_router)
router.include_router(calculations_router)
router.include_router(recipes_router)  # 🆕 اضافه شد

# Export برای استفاده در main.py
__all__ = ['router']