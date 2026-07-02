"""
محاسبه تعادل یونی
================================

این فایل شامل توابع اصلی محاسبه تعادل یونی است:
- محاسبه کاتیون و آنیون از مقادیر عناصر
- بررسی تعادل یونی
- تولید وضعیت خوانا برای نمایش به کاربر
"""

from typing import Dict, Tuple, Any, List, Optional
from .constants import (
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    ALL_ELEMENTS,
    BALANCE_TOLERANCE,
    STANDARD_RANGES,
    VALENCES
)
from .converters import ppm_to_meq


def calculate_ion_balance(
    target_values: Dict[str, float],
    unit: str = "ppm"
) -> Tuple[float, float, bool, Dict[str, Any]]:
    """
    محاسبه تعادل کاتیون و آنیون
    
    این تابع اصلی محاسبه تعادل یونی است. ابتدا تمام عناصر را بررسی می‌کند،
    آنها را به MEQ/L تبدیل می‌کند و سپس مجموع کاتیون‌ها و آنیون‌ها را محاسبه می‌کند.
    
    Args:
        target_values: دیکشنری مقادیر عناصر به صورت {نام_عنصر: مقدار}
        unit: واحد ورودی ('ppm', 'meq', 'mmol') - پیش‌فرض 'ppm'
    
    Returns:
        Tuple شامل:
            - float: مجموع کاتیون‌ها (meq/L)
            - float: مجموع آنیون‌ها (meq/L)
            - bool: آیا تعادل برقرار است (اختلاف < 0.5)
            - Dict: جزئیات کامل محاسبه
    
    مثال:
        >>> elements = {'K': 200, 'Ca': 150, 'Mg': 50, 'N-NO3': 200, 'P': 40}
        >>> cation, anion, balanced, details = calculate_ion_balance(elements)
        >>> print(f"Cation: {cation:.2f}, Anion: {anion:.2f}, Balanced: {balanced}")
        Cation: 16.23, Anion: 4.52, Balanced: False
    """
    cation_total = 0.0
    anion_total = 0.0
    
    # دیکشنری‌های ذخیره جزئیات
    details = {
        'cation_elements': {},      # {عنصر: مقدار_meq}
        'anion_elements': {},       # {عنصر: مقدار_meq}
        'neutral_elements': {},     # {عنصر: مقدار_meq}
        'zero_elements': [],        # [عنصرهای با مقدار صفر]
        'missing_elements': [],     # [عنصرهای موجود در ALL_ELEMENTS ولی در target_values نیستند]
        'element_details': []       # لیست کامل جزئیات هر عنصر
    }
    
    # بررسی عناصر موجود در target_values
    for element, value in target_values.items():
        # اگر مقدار صفر یا None باشد، رد کن
        if value is None or value == 0:
            details['zero_elements'].append(element)
            continue
        
        # اگر عنصر در لیست عناصر معتبر نیست، رد کن
        if element not in ALL_ELEMENTS:
            continue
        
        # تبدیل به MEQ بر اساس واحد ورودی
        if unit == "ppm":
            meq_value = ppm_to_meq(value, element)
        elif unit == "mmol":
            meq_value = value * abs(VALENCES.get(element, 0))
        elif unit == "meq":
            meq_value = value
        else:
            raise ValueError(f"واحد نامعتبر: {unit}. واحدهای معتبر: ppm, meq, mmol")
        
        # ذخیره جزئیات عنصر
        element_detail = {
            'name': element,
            'value': value,
            'unit': unit,
            'meq_value': meq_value,
            'valence': VALENCES.get(element, 0),
            'type': _get_element_type(element)
        }
        details['element_details'].append(element_detail)
        
        # اضافه کردن به جمع‌های مربوطه
        if element in CATION_ELEMENTS:
            cation_total += meq_value
            details['cation_elements'][element] = meq_value
        elif element in ANION_ELEMENTS:
            anion_total += meq_value
            details['anion_elements'][element] = meq_value
        else:
            details['neutral_elements'][element] = meq_value
    
    # بررسی عناصری که در target_values نیستند ولی در ALL_ELEMENTS هستند
    for element in ALL_ELEMENTS:
        if element not in target_values:
            details['missing_elements'].append(element)
    
    # محاسبه تعادل
    difference = abs(cation_total - anion_total)
    is_balanced = difference < BALANCE_TOLERANCE
    
    # اضافه کردن آمار کلی به details
    details['summary'] = {
        'total_cation_meq': cation_total,
        'total_anion_meq': anion_total,
        'difference': difference,
        'tolerance': BALANCE_TOLERANCE,
        'is_balanced': is_balanced,
        'cation_count': len(details['cation_elements']),
        'anion_count': len(details['anion_elements']),
        'neutral_count': len(details['neutral_elements']),
        'zero_count': len(details['zero_elements']),
        'missing_count': len(details['missing_elements'])
    }
    
    return cation_total, anion_total, is_balanced, details


def _get_element_type(element: str) -> str:
    """
    تعیین نوع عنصر (داخلی)
    
    Args:
        element: نام عنصر
    
    Returns:
        str: 'cation', 'anion', یا 'neutral'
    """
    if element in CATION_ELEMENTS:
        return 'cation'
    elif element in ANION_ELEMENTS:
        return 'anion'
    else:
        return 'neutral'


def get_ion_balance_status(
    cation: float,
    anion: float,
    is_balanced: bool
) -> Dict[str, Any]:
    """
    دریافت وضعیت تعادل یونی به صورت خوانا برای نمایش به کاربر
    
    Args:
        cation: مجموع کاتیون‌ها (meq/L)
        anion: مجموع آنیون‌ها (meq/L)
        is_balanced: آیا تعادل برقرار است
    
    Returns:
        Dict: شامل وضعیت، پیام، رنگ و آمار
    
    مثال:
        >>> status = get_ion_balance_status(16.23, 4.52, False)
        >>> print(status['message'])
        'تعادل یونی برقرار نیست (اختلاف: 11.71 meq/L)'
    """
    difference = abs(cation - anion)
    
    # تعیین وضعیت
    if is_balanced:
        status = 'balanced'
        message = 'تعادل یونی برقرار است'
        color = 'success'
        icon = '✅'
    else:
        status = 'unbalanced'
        message = f'تعادل یونی برقرار نیست (اختلاف: {difference:.2f} meq/L)'
        color = 'danger'
        icon = '⚠️'
    
    # تعیین سطح اختلاف
    if difference < 0.5:
        level = 'excellent'
        level_label = 'عالی'
    elif difference < 1.0:
        level = 'good'
        level_label = 'خوب'
    elif difference < 2.0:
        level = 'moderate'
        level_label = 'متوسط'
    elif difference < 5.0:
        level = 'poor'
        level_label = 'ضعیف'
    else:
        level = 'critical'
        level_label = 'بحرانی'
    
    return {
        'status': status,
        'message': message,
        'color': color,
        'icon': icon,
        'cation': cation,
        'anion': anion,
        'difference': difference,
        'tolerance': BALANCE_TOLERANCE,
        'level': level,
        'level_label': level_label,
        'is_balanced': is_balanced,
        'recommendation': _get_recommendation(cation, anion, is_balanced)
    }


def _get_recommendation(
    cation: float,
    anion: float,
    is_balanced: bool
) -> str:
    """
    تولید توصیه بر اساس وضعیت تعادل یونی (داخلی)
    
    Args:
        cation: مجموع کاتیون‌ها
        anion: مجموع آنیون‌ها
        is_balanced: آیا تعادل برقرار است
    
    Returns:
        str: توصیه مناسب
    """
    if is_balanced:
        return "تعادل یونی برقرار است. ادامه دهید."
    
    difference = cation - anion
    
    if difference > 0:
        # کاتیون بیشتر از آنیون است
        if cation > 0 and anion == 0:
            return "هیچ آنیونی در محلول وجود ندارد. لطفاً آنیون‌ها (نیترات، فسفات، سولفات) را اضافه کنید."
        elif cation > anion * 2:
            return "کاتیون‌ها به طور قابل توجهی بیشتر از آنیون‌ها هستند. لطفاً آنیون‌ها را افزایش دهید یا کاتیون‌ها را کاهش دهید."
        else:
            return "کاتیون‌ها بیشتر از آنیون‌ها هستند. لطفاً تعادل را با افزودن آنیون‌ها برقرار کنید."
    else:
        # آنیون بیشتر از کاتیون است
        if anion > 0 and cation == 0:
            return "هیچ کاتیونی در محلول وجود ندارد. لطفاً کاتیون‌ها (پتاسیم، کلسیم، منیزیم) را اضافه کنید."
        elif anion > cation * 2:
            return "آنیون‌ها به طور قابل توجهی بیشتر از کاتیون‌ها هستند. لطفاً کاتیون‌ها را افزایش دهید یا آنیون‌ها را کاهش دهید."
        else:
            return "آنیون‌ها بیشتر از کاتیون‌ها هستند. لطفاً تعادل را با افزودن کاتیون‌ها برقرار کنید."


def get_element_standard_range(element: str) -> Optional[Dict[str, float]]:
    """
    دریافت محدوده استاندارد یک عنصر در محلول غذایی
    
    Args:
        element: نام عنصر
    
    Returns:
        Optional[Dict]: محدوده استاندارد شامل min, max, optimal
    """
    return STANDARD_RANGES.get(element)


def check_element_status(
    element: str,
    value: float,
    unit: str = "ppm"
) -> Dict[str, Any]:
    """
    بررسی وضعیت یک عنصر نسبت به محدوده استاندارد
    
    Args:
        element: نام عنصر
        value: مقدار عنصر
        unit: واحد مقدار
    
    Returns:
        Dict: شامل وضعیت، پیام و محدوده
    """
    standard_range = get_element_standard_range(element)
    if not standard_range:
        return {
            'status': 'unknown',
            'message': f'محدوده استاندارد برای {element} تعریف نشده است',
            'value': value,
            'unit': unit
        }
    
    min_val = standard_range['min']
    max_val = standard_range['max']
    optimal = standard_range['optimal']
    
    if value < min_val:
        status = 'deficient'
        message = f'{element}: کمبود ({value:.2f} {unit} < {min_val} {unit})'
    elif value > max_val:
        status = 'excessive'
        message = f'{element}: بیش‌بود ({value:.2f} {unit} > {max_val} {unit})'
    else:
        status = 'optimal'
        message = f'{element}: مطلوب ({value:.2f} {unit})'
    
    return {
        'status': status,
        'message': message,
        'value': value,
        'unit': unit,
        'min': min_val,
        'max': max_val,
        'optimal': optimal,
        'is_optimal': status == 'optimal'
    }