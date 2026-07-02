"""
منطق کسب‌وکار و محاسبات تخصصی - Facade
=======================================

این فایل به عنوان لایه واسط (Facade) بین ماژول‌های core و بقیه برنامه عمل می‌کند.
تمام توابع محاسباتی از طریق این فایل در دسترس هستند.
"""

import time
import logging
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

from app.core import (
    # Ion Balance
    calculate_ion_balance as core_calculate_ion_balance,
    get_ion_balance_status,
    check_precipitation,
    convert_units,
    ppm_to_meq as core_ppm_to_meq,
    meq_to_ppm as core_meq_to_ppm,
    ALL_ELEMENTS,
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    BALANCE_TOLERANCE,
    # 🆕 توابع EC و pH
    calculate_ec as core_calculate_ec,
    calculate_ph as core_calculate_ph,
    get_ec_ph_status as core_get_ec_ph_status,
    # Optimizer
    optimize_fertilizers as core_optimize_fertilizers,
    # Reservoir
    calculate_reservoir_data,
    check_reservoir_compatibility
)

logger = logging.getLogger(__name__)

# ============================================================
# EXPORT CONSTANTS
# ============================================================

ELEMENTS = ALL_ELEMENTS
CATIONS = CATION_ELEMENTS
ANIONS = ANION_ELEMENTS
ION_BALANCE_TOLERANCE = BALANCE_TOLERANCE


# ============================================================
# توابع تبدیل واحدها (Wrapper)
# ============================================================

def ppm_to_meq(ppm: float, element: str) -> float:
    """
    تبدیل PPM به MEQ/L
    
    Args:
        ppm: مقدار بر حسب PPM
        element: نام عنصر
    
    Returns:
        float: مقدار بر حسب MEQ/L
    """
    return core_ppm_to_meq(ppm, element)


def meq_to_ppm(meq: float, element: str) -> float:
    """
    تبدیل MEQ/L به PPM
    
    Args:
        meq: مقدار بر حسب MEQ/L
        element: نام عنصر
    
    Returns:
        float: مقدار بر حسب PPM
    """
    return core_meq_to_ppm(meq, element)


def convert_units(value: float, from_unit: str, to_unit: str, element: str) -> float:
    """
    تبدیل واحدهای مختلف
    
    Args:
        value: مقدار ورودی
        from_unit: واحد مبدا (ppm, meq, mmol)
        to_unit: واحد مقصد (ppm, meq, mmol)
        element: نام عنصر
    
    Returns:
        float: مقدار تبدیل شده
    """
    return convert_units(value, from_unit, to_unit, element)


# ============================================================
# توابع تعادل یونی (Wrapper)
# ============================================================

def calculate_ion_balance(
    target_values: Dict[str, float],
    unit: str = "ppm"
) -> Tuple[float, float, bool]:
    """
    محاسبه تعادل کاتیون و آنیون - نسخه ساده برای سازگاری با کدهای قدیمی
    
    Args:
        target_values: مقادیر عناصر
        unit: واحد ورودی (ppm, meq, mmol)
    
    Returns:
        Tuple[float, float, bool]: (کاتیون, آنیون, آیا متعادل است)
    """
    cation, anion, is_balanced, _ = core_calculate_ion_balance(
        target_values, unit
    )
    return cation, anion, is_balanced


def get_ion_balance_status(cation: float, anion: float, is_balanced: bool) -> Dict[str, Any]:
    """
    دریافت وضعیت تعادل یونی به صورت خوانا
    
    Args:
        cation: مجموع کاتیون‌ها (meq/L)
        anion: مجموع آنیون‌ها (meq/L)
        is_balanced: آیا تعادل برقرار است
    
    Returns:
        Dict: شامل وضعیت، پیام و آمار
    """
    return get_ion_balance_status(cation, anion, is_balanced)


def check_precipitation(concentrations: Dict[str, float]) -> Dict[str, Any]:
    """
    بررسی رسوب احتمالی در ترکیب عناصر
    
    Args:
        concentrations: غلظت عناصر (ppm)
    
    Returns:
        Dict: شامل وضعیت ایمنی و خطرات
    """
    return check_precipitation(concentrations)


# ============================================================
# 🆕 توابع EC و pH (Wrapper)
# ============================================================

def calculate_ec(concentrations: Dict[str, float], unit: str = "ppm") -> Dict[str, Any]:
    """
    محاسبه EC (هدایت الکتریکی) محلول نهایی
    
    Args:
        concentrations: غلظت عناصر (ppm یا meq/L)
        unit: واحد ورودی ('ppm', 'meq')
    
    Returns:
        Dict: شامل EC (dS/m)، وضعیت و توصیه
    """
    return core_calculate_ec(concentrations, unit)


def calculate_ph(
    concentrations: Dict[str, float],
    unit: str = "ppm",
    water_ph: Optional[float] = None
) -> Dict[str, Any]:
    """
    محاسبه pH تقریبی محلول نهایی
    
    Args:
        concentrations: غلظت عناصر (ppm یا meq/L)
        unit: واحد ورودی ('ppm', 'meq')
        water_ph: pH آب (اختیاری، پیش‌فرض ۷.۰)
    
    Returns:
        Dict: شامل pH، وضعیت و توصیه
    """
    return core_calculate_ph(concentrations, unit, water_ph)


def get_ec_ph_status(
    ec: float,
    ph: float,
    water_ec: Optional[float] = None,
    water_ph: Optional[float] = None
) -> Dict[str, Any]:
    """
    دریافت وضعیت ترکیبی EC و pH
    
    Args:
        ec: مقدار EC (dS/m)
        ph: مقدار pH
        water_ec: EC آب (اختیاری)
        water_ph: pH آب (اختیاری)
    
    Returns:
        Dict: وضعیت کلی و توصیه‌ها
    """
    return core_get_ec_ph_status(ec, ph, water_ec, water_ph)


# ============================================================
# توابع بهینه‌سازی (Wrapper)
# ============================================================

def optimize_fertilizers(
    target_values: Dict[str, float],
    fertilizers: List[Dict[str, Any]],
    water_values: Optional[Dict[str, float]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    🎯 بهینه‌سازی خودکار فرمول کود
    
    این تابع قلب تپنده FarmTech است. با استفاده از الگوریتم NNLS،
    بهترین ترکیب کودها را محاسبه می‌کند.
    
    Args:
        target_values: عناصر هدف (ppm)
        fertilizers: لیست کودها با عناصر و قیمت
        water_values: عناصر موجود در آب (اختیاری)
        options: تنظیمات بهینه‌سازی (اختیاری)
    
    Returns:
        Dict: شامل وزن‌ها، غلظت‌ها، خطا، تحلیل و توصیه‌ها
    """
    return core_optimize_fertilizers(
        target_values=target_values,
        fertilizers=fertilizers,
        water_values=water_values,
        options=options
    )


# ============================================================
# توابع مخازن (Wrapper)
# ============================================================

def calculate_reservoir_data_optimized(
    fertilizers: List[Dict[str, Any]],
    weights: Dict[str, float]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    محاسبه توزیع مواد در مخازن A, B, C (نسخه بهینه‌شده)
    
    Args:
        fertilizers: لیست کودها با مشخصات کامل
        weights: دیکشنری وزن‌های بهینه {fertilizer_id: weight}
    
    Returns:
        Dict: توزیع مواد در سه مخزن
    """
    return calculate_reservoir_data(fertilizers, weights)


def check_reservoir_compatibility(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    بررسی سازگاری شیمیایی مواد در مخازن
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        Dict: شامل وضعیت سازگاری و هشدارها
    """
    return check_reservoir_compatibility(reservoir_data, fertilizers)


# ============================================================
# توابع کمکی برای سازگاری با کدهای قدیمی
# ============================================================

def calculate_final_solution(
    target_values: Dict[str, float],
    water_values: Dict[str, float],
    fertilizer_contributions: Dict[str, float]
) -> Dict[str, Any]:
    """
    محاسبه محلول نهایی (سازگاری با کدهای قدیمی)
    
    Args:
        target_values: مقادیر هدف
        water_values: مقادیر آب
        fertilizer_contributions: سهم کودها
    
    Returns:
        Dict: شامل مقادیر نهایی و تعادل یونی
    """
    from app.core.optimizer.result_processor import calculate_final_concentrations
    
    # ایجاد ماتریس ساده برای محاسبه
    active_elements = list(target_values.keys())
    A = np.array([[1.0 if el in fertilizer_contributions else 0.0 for el in active_elements]])
    weights = np.array([1.0])
    
    final_values = calculate_final_concentrations(
        weights=weights,
        A=A,
        water_values=water_values,
        active_elements=active_elements
    )
    
    cation, anion, is_balanced = calculate_ion_balance(final_values)
    
    return {
        'final_values': final_values,
        'ion_balance': {
            'cation': cation,
            'anion': anion,
            'is_balanced': is_balanced
        }
    }


# ============================================================
# لاگ‌گیری و دیباگ
# ============================================================

def get_core_info() -> Dict[str, Any]:
    """
    دریافت اطلاعات درباره ماژول‌های core
    
    Returns:
        Dict: اطلاعات ماژول‌ها
    """
    return {
        'ion_balance': {
            'elements_count': len(ALL_ELEMENTS),
            'cations': CATION_ELEMENTS,
            'anions': ANION_ELEMENTS,
            'tolerance': BALANCE_TOLERANCE
        },
        'optimizer': {
            'methods': ['nnls', 'lsq_linear', 'lsq_linear_with_cost']
        },
        'reservoir': {
            'reservoirs': ['A', 'B', 'C']
        },
        'ec_ph': {
            'ec_coefficients_count': len(core_calculate_ec.__code__.co_consts) if hasattr(core_calculate_ec, '__code__') else 0,
            'ph_coefficients_count': len(core_calculate_ph.__code__.co_consts) if hasattr(core_calculate_ph, '__code__') else 0
        }
    }