"""
توابع تبدیل واحدها
================================

این فایل شامل توابع تبدیل بین واحدهای مختلف است:
- PPM ↔ MEQ
- PPM ↔ MMOL
- تبدیل عمومی با مشخص کردن واحد مبدا و مقصد
"""

from typing import Dict, Any
from .constants import MOLECULAR_WEIGHTS, VALENCES


def ppm_to_meq(ppm: float, element: str) -> float:
    """
    تبدیل PPM به MEQ/L
    
    فرمول: MEQ = (PPM × |بار|) ÷ وزن_مولکولی
    
    Args:
        ppm: مقدار بر حسب PPM
        element: نام عنصر (کلید در دیکشنری MOLECULAR_WEIGHTS)
    
    Returns:
        float: مقدار بر حسب MEQ/L
    
    مثال:
        >>> ppm_to_meq(100, 'K')
        2.5576  # 100 ppm پتاسیم = 2.56 meq/L
    """
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    valence = abs(VALENCES.get(element, 0))
    
    if mw == 0 or valence == 0:
        return 0.0
    
    return (ppm * valence) / mw


def meq_to_ppm(meq: float, element: str) -> float:
    """
    تبدیل MEQ/L به PPM
    
    فرمول: PPM = (MEQ × وزن_مولکولی) ÷ |بار|
    
    Args:
        meq: مقدار بر حسب MEQ/L
        element: نام عنصر (کلید در دیکشنری MOLECULAR_WEIGHTS)
    
    Returns:
        float: مقدار بر حسب PPM
    
    مثال:
        >>> meq_to_ppm(2.5576, 'K')
        100.0  # 2.56 meq/L پتاسیم = 100 ppm
    """
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    valence = abs(VALENCES.get(element, 0))
    
    if valence == 0:
        return 0.0
    
    return (meq * mw) / valence


def ppm_to_mmol(ppm: float, element: str) -> float:
    """
    تبدیل PPM به MMOL/L
    
    فرمول: MMOL = PPM ÷ وزن_مولکولی
    
    Args:
        ppm: مقدار بر حسب PPM
        element: نام عنصر (کلید در دیکشنری MOLECULAR_WEIGHTS)
    
    Returns:
        float: مقدار بر حسب MMOL/L
    
    مثال:
        >>> ppm_to_mmol(100, 'K')
        2.5576  # 100 ppm پتاسیم = 2.56 mmol/L
    """
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    
    if mw == 0:
        return 0.0
    
    return ppm / mw


def mmol_to_ppm(mmol: float, element: str) -> float:
    """
    تبدیل MMOL/L به PPM
    
    فرمول: PPM = MMOL × وزن_مولکولی
    
    Args:
        mmol: مقدار بر حسب MMOL/L
        element: نام عنصر (کلید در دیکشنری MOLECULAR_WEIGHTS)
    
    Returns:
        float: مقدار بر حسب PPM
    
    مثال:
        >>> mmol_to_ppm(2.5576, 'K')
        100.0  # 2.56 mmol/L پتاسیم = 100 ppm
    """
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    
    return mmol * mw


def convert_units(
    value: float,
    from_unit: str,
    to_unit: str,
    element: str
) -> float:
    """
    تبدیل واحدهای مختلف به یکدیگر
    
    واحدهای پشتیبانی شده:
        - 'ppm': قسمت در میلیون
        - 'meq': میلی‌اکی والان در لیتر
        - 'mmol': میلی‌مول در لیتر
    
    Args:
        value: مقدار ورودی
        from_unit: واحد مبدا ('ppm', 'meq', 'mmol')
        to_unit: واحد مقصد ('ppm', 'meq', 'mmol')
        element: نام عنصر (کلید در دیکشنری MOLECULAR_WEIGHTS)
    
    Returns:
        float: مقدار تبدیل شده
    
    Raises:
        ValueError: اگر واحد پشتیبانی نشود یا عنصر نامعتبر باشد
    
    مثال:
        >>> convert_units(100, 'ppm', 'meq', 'K')
        2.5576  # 100 ppm پتاسیم = 2.56 meq/L
    """
    # اعتبارسنجی واحدها
    valid_units = ['ppm', 'meq', 'mmol']
    if from_unit not in valid_units:
        raise ValueError(f"واحد مبدا نامعتبر: {from_unit}. واحدهای معتبر: {valid_units}")
    if to_unit not in valid_units:
        raise ValueError(f"واحد مقصد نامعتبر: {to_unit}. واحدهای معتبر: {valid_units}")
    
    # اگر واحدها یکسان هستند، همان مقدار را برگردان
    if from_unit == to_unit:
        return value
    
    # اعتبارسنجی عنصر
    if element not in MOLECULAR_WEIGHTS:
        raise ValueError(f"عنصر نامعتبر: {element}. عناصر معتبر: {list(MOLECULAR_WEIGHTS.keys())}")
    
    # مرحله ۱: تبدیل به PPM (واحد پایه)
    if from_unit == 'meq':
        ppm_value = meq_to_ppm(value, element)
    elif from_unit == 'mmol':
        ppm_value = mmol_to_ppm(value, element)
    else:  # from_unit == 'ppm'
        ppm_value = value
    
    # مرحله ۲: تبدیل از PPM به واحد مقصد
    if to_unit == 'meq':
        return ppm_to_meq(ppm_value, element)
    elif to_unit == 'mmol':
        return ppm_to_mmol(ppm_value, element)
    else:  # to_unit == 'ppm'
        return ppm_value


def get_conversion_factor(from_unit: str, to_unit: str, element: str) -> float:
    """
    دریافت ضریب تبدیل بین دو واحد
    
    Args:
        from_unit: واحد مبدا ('ppm', 'meq', 'mmol')
        to_unit: واحد مقصد ('ppm', 'meq', 'mmol')
        element: نام عنصر
    
    Returns:
        float: ضریب تبدیل (مقدار در واحد مقصد = مقدار در واحد مبدا × ضریب)
    
    مثال:
        >>> get_conversion_factor('ppm', 'meq', 'K')
        0.025576  # هر 1 ppm پتاسیم = 0.0256 meq/L
    """
    # تبدیل 1 واحد مبدا به واحد مقصد
    return convert_units(1.0, from_unit, to_unit, element)


# ============================================================
# دیکشنری کمکی برای تبدیل سریع
# ============================================================
def get_all_conversion_factors(element: str) -> Dict[str, Dict[str, float]]:
    """
    دریافت تمام ضرایب تبدیل برای یک عنصر خاص
    
    Args:
        element: نام عنصر
    
    Returns:
        Dict: دیکشنری ضرایب تبدیل بین همه واحدها
    
    مثال:
        >>> get_all_conversion_factors('K')
        {
            'ppm': {'ppm': 1.0, 'meq': 0.025576, 'mmol': 0.025576},
            'meq': {'ppm': 39.0983, 'meq': 1.0, 'mmol': 1.0},
            'mmol': {'ppm': 39.0983, 'meq': 1.0, 'mmol': 1.0}
        }
    """
    units = ['ppm', 'meq', 'mmol']
    factors = {}
    
    for from_unit in units:
        factors[from_unit] = {}
        for to_unit in units:
            factors[from_unit][to_unit] = get_conversion_factor(
                from_unit, to_unit, element
            )
    
    return factors