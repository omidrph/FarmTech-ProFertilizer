# backend/app/routes/calculations/ph_adjustment.py
"""
مسیر ماشین‌حساب اصلاح pH
============================

🆕 محاسبه دوز اسید/باز لازم بر اساس pH واقعی اندازه‌گیری‌شده با دستگاه،
pH هدف، قلیائیت آب و حجم مخزن. برخلاف تخمین pH محلول کودی (که فقط یک
شاخص تقریبی است)، این مسیر بر مبنای عدد واقعی pH که کاربر خودش اندازه
گرفته کار می‌کند - دقیقاً طبق توصیهٔ استاندارد صنعت: «pH هرگز صرفاً
محاسبه نمی‌شود، همیشه اندازه‌گیری و سپس با فرمول اصلاح می‌شود.»
"""

import logging
import traceback

from fastapi import HTTPException, status

from app.schemas import PHAdjustmentRequest, PHAdjustmentResponse
from app.core.ph_adjustment import calculate_ph_adjustment_dose, ACID_BASE_SPECS

logger = logging.getLogger(__name__)


def calculate_ph_adjustment_endpoint(request: PHAdjustmentRequest):
    """
    🆕 محاسبه مقدار اسید/باز لازم برای رساندن محلول از pH فعلی (اندازه‌گیری‌شده) به pH هدف.
    """
    try:
        if request.acid_or_base_type not in ACID_BASE_SPECS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"نوع اسید/باز نامعتبر است. گزینه‌های مجاز: {list(ACID_BASE_SPECS.keys())}"
            )

        result = calculate_ph_adjustment_dose(
            current_ph=request.current_ph,
            target_ph=request.target_ph,
            alkalinity_ppm_caco3=request.alkalinity_ppm_caco3,
            tank_volume_liters=request.tank_volume,
            acid_or_base_type=request.acid_or_base_type,
            product_concentration_percent=request.product_concentration_percent,
            product_price_per_kg=request.product_price_per_kg
        )

        if 'error' in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result['error'])

        return PHAdjustmentResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in calculate_ph_adjustment_endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه اصلاح pH: {str(e)}"
        )
