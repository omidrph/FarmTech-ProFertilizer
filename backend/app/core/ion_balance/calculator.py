"""
محاسبه تعادل یونی
================================

این فایل شامل توابع اصلی محاسبه تعادل یونی است:
- محاسبه کاتیون و آنیون از مقادیر عناصر
- بررسی تعادل یونی
- تولید وضعیت خوانا برای نمایش به کاربر
- محاسبه EC و pH نهایی
- تعادل یونی خودکار
"""

from typing import Dict, Tuple, Any, List, Optional
import math
from .constants import (
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    ALL_ELEMENTS,
    BALANCE_TOLERANCE,
    STANDARD_RANGES,
    VALENCES,
    MOLECULAR_WEIGHTS,
    ION_TO_EC_COEFFICIENTS,
    ACIDITY_COEFFICIENTS,
    EC_RANGES,
    PH_RANGES
)
from .converters import ppm_to_meq


# ============================================================
# توابع موجود
# ============================================================

def calculate_ion_balance(
    target_values: Dict[str, float],
    unit: str = "ppm"
) -> Tuple[float, float, bool, Dict[str, Any]]:
    """محاسبه تعادل کاتیون و آنیون"""
    cation_total = 0.0
    anion_total = 0.0
    
    details = {
        'cation_elements': {},
        'anion_elements': {},
        'neutral_elements': {},
        'zero_elements': [],
        'missing_elements': [],
        'element_details': []
    }
    
    for element, value in target_values.items():
        if value is None or value == 0:
            details['zero_elements'].append(element)
            continue
        
        if element not in ALL_ELEMENTS:
            continue
        
        if unit == "ppm":
            meq_value = ppm_to_meq(value, element)
        elif unit == "mmol":
            meq_value = value * abs(VALENCES.get(element, 0))
        elif unit == "meq":
            meq_value = value
        else:
            raise ValueError(f"واحد نامعتبر: {unit}")
        
        element_detail = {
            'name': element,
            'value': value,
            'unit': unit,
            'meq_value': meq_value,
            'valence': VALENCES.get(element, 0),
            'type': _get_element_type(element)
        }
        details['element_details'].append(element_detail)
        
        if element in CATION_ELEMENTS:
            cation_total += meq_value
            details['cation_elements'][element] = meq_value
        elif element in ANION_ELEMENTS:
            anion_total += meq_value
            details['anion_elements'][element] = meq_value
        else:
            details['neutral_elements'][element] = meq_value
    
    for element in ALL_ELEMENTS:
        if element not in target_values:
            details['missing_elements'].append(element)
    
    difference = abs(cation_total - anion_total)
    is_balanced = difference < BALANCE_TOLERANCE
    
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
    """تعیین نوع عنصر (داخلی)"""
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
    """دریافت وضعیت تعادل یونی به صورت خوانا"""
    difference = abs(cation - anion)
    
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


def _get_recommendation(cation: float, anion: float, is_balanced: bool) -> str:
    """تولید توصیه بر اساس وضعیت تعادل یونی"""
    if is_balanced:
        return "تعادل یونی برقرار است. ادامه دهید."
    
    difference = cation - anion
    
    if difference > 0:
        if cation > 0 and anion == 0:
            return "هیچ آنیونی در محلول وجود ندارد. لطفاً آنیون‌ها را اضافه کنید."
        elif cation > anion * 2:
            return "کاتیون‌ها به طور قابل توجهی بیشتر از آنیون‌ها هستند. لطفاً آنیون‌ها را افزایش دهید."
        else:
            return "کاتیون‌ها بیشتر از آنیون‌ها هستند. لطفاً تعادل را با افزودن آنیون‌ها برقرار کنید."
    else:
        if anion > 0 and cation == 0:
            return "هیچ کاتیونی در محلول وجود ندارد. لطفاً کاتیون‌ها را اضافه کنید."
        elif anion > cation * 2:
            return "آنیون‌ها به طور قابل توجهی بیشتر از کاتیون‌ها هستند. لطفاً کاتیون‌ها را افزایش دهید."
        else:
            return "آنیون‌ها بیشتر از کاتیون‌ها هستند. لطفاً تعادل را با افزودن کاتیون‌ها برقرار کنید."


def get_element_standard_range(element: str) -> Optional[Dict[str, float]]:
    """دریافت محدوده استاندارد یک عنصر در محلول غذایی"""
    return STANDARD_RANGES.get(element)


def check_element_status(
    element: str,
    value: float,
    unit: str = "ppm"
) -> Dict[str, Any]:
    """بررسی وضعیت یک عنصر نسبت به محدوده استاندارد"""
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


# ============================================================
# 🆕 توابع محاسبه EC و pH (اصلاح شده)
# ============================================================

def calculate_ec(
    concentrations: Dict[str, float],
    unit: str = "ppm"
) -> Dict[str, Any]:
    """
    محاسبه EC (هدایت الکتریکی) محلول نهایی
    
    EC = Σ (غلظت یون × ضریب تبدیل) / 100
    
    ✅ اصلاح: تقسیم بر 100 به جای 1000 برای دقت بیشتر
    
    Args:
        concentrations: غلظت عناصر (ppm یا meq/L)
        unit: واحد ورودی ('ppm', 'meq')
    
    Returns:
        Dict: شامل EC (dS/m)، وضعیت و توصیه
    """
    total_ec = 0.0
    element_contributions = {}
    active_elements = []
    
    for element, value in concentrations.items():
        if value is None or value == 0:
            continue
        
        if element not in ION_TO_EC_COEFFICIENTS:
            continue
        
        # تبدیل به MEQ اگر PPM باشد
        if unit == "ppm":
            meq_value = ppm_to_meq(value, element)
        else:
            meq_value = value
        
        coefficient = ION_TO_EC_COEFFICIENTS.get(element, 7.10)
        contribution = meq_value * coefficient
        total_ec += contribution
        
        element_contributions[element] = {
            'meq': round(meq_value, 4),
            'coefficient': coefficient,
            'contribution': round(contribution, 4)
        }
        active_elements.append(element)
    
    # ✅ اصلاح: تقسیم بر 100 به جای 1000
    ec_ds = total_ec / 100
    
    # تعیین وضعیت EC
    status_info = _get_ec_status(ec_ds)
    
    return {
        'ec': round(ec_ds, 3),
        'status': status_info['status'],
        'status_label': status_info['label'],
        'color': status_info['color'],
        'recommendation': status_info['recommendation'],
        'contributions': element_contributions,
        'active_elements': active_elements,
        'total_meq': round(sum(c['meq'] for c in element_contributions.values()), 4),
        'range_min': status_info.get('range_min', 0),
        'range_max': status_info.get('range_max', 0)
    }


def _get_ec_status(ec: float) -> Dict[str, Any]:
    """تعیین وضعیت EC بر اساس محدوده‌ها"""
    for key, range_info in EC_RANGES.items():
        if range_info['min'] <= ec < range_info['max']:
            return {
                'status': key,
                'label': range_info['label'],
                'color': range_info['color'],
                'range_min': range_info['min'],
                'range_max': range_info['max'],
                'recommendation': _get_ec_recommendation(key, ec)
            }
    return {
        'status': 'unknown',
        'label': 'نامشخص',
        'color': 'gray',
        'range_min': 0,
        'range_max': 0,
        'recommendation': 'EC در محدوده نامشخص است. لطفاً بررسی کنید.'
    }


def _get_ec_recommendation(status: str, ec: float) -> str:
    """تولید توصیه بر اساس وضعیت EC"""
    recommendations = {
        'low': f'EC پایین است ({ec:.2f} dS/m). ممکن است نیاز به افزایش غلظت کودها باشد.',
        'optimal': f'EC در محدوده مطلوب است ({ec:.2f} dS/m).',
        'high': f'EC بالا است ({ec:.2f} dS/m). ممکن است خطر شوری وجود داشته باشد.',
        'critical': f'EC بسیار بالا است ({ec:.2f} dS/m). خطر شوری جدی است!'
    }
    return recommendations.get(status, 'EC در محدوده نامشخص است.')


def calculate_ph(
    concentrations: Dict[str, float],
    unit: str = "ppm",
    water_ph: Optional[float] = None
) -> Dict[str, Any]:
    """
    محاسبه pH تقریبی محلول نهایی
    
    pH = pH_water + Σ (غلظت × ضریب اسیدی/بازی)
    
    ✅ اصلاح: ضرایب اسیدی/بازی اصلاح شده‌اند
    
    Args:
        concentrations: غلظت عناصر (ppm یا meq/L)
        unit: واحد ورودی ('ppm', 'meq')
        water_ph: pH آب (اختیاری، پیش‌فرض ۷.۰)
    
    Returns:
        Dict: شامل pH، وضعیت و توصیه
    """
    if water_ph is None:
        water_ph = 7.0
    
    ph_shift = 0.0
    element_contributions = {}
    active_elements = []
    
    for element, value in concentrations.items():
        if value is None or value == 0:
            continue
        
        if element not in ACIDITY_COEFFICIENTS:
            continue
        
        # تبدیل به MEQ اگر PPM باشد
        if unit == "ppm":
            meq_value = ppm_to_meq(value, element)
        else:
            meq_value = value
        
        coefficient = ACIDITY_COEFFICIENTS.get(element, 0)
        contribution = meq_value * coefficient
        ph_shift += contribution
        
        element_contributions[element] = {
            'meq': round(meq_value, 4),
            'coefficient': coefficient,
            'contribution': round(contribution, 4)
        }
        active_elements.append(element)
    
    # pH نهایی (محدود به بازه ۰-۱۴)
    ph = water_ph + ph_shift
    ph = max(0, min(14, ph))
    
    # تعیین وضعیت pH
    status_info = _get_ph_status(ph)
    
    return {
        'ph': round(ph, 2),
        'ph_shift': round(ph_shift, 2),
        'water_ph': water_ph,
        'status': status_info['status'],
        'status_label': status_info['label'],
        'color': status_info['color'],
        'recommendation': status_info['recommendation'],
        'contributions': element_contributions,
        'active_elements': active_elements,
        'range_min': status_info.get('range_min', 0),
        'range_max': status_info.get('range_max', 0)
    }


def _get_ph_status(ph: float) -> Dict[str, Any]:
    """تعیین وضعیت pH بر اساس محدوده‌ها"""
    for key, range_info in PH_RANGES.items():
        if range_info['min'] <= ph < range_info['max']:
            return {
                'status': key,
                'label': range_info['label'],
                'color': range_info['color'],
                'range_min': range_info['min'],
                'range_max': range_info['max'],
                'recommendation': _get_ph_recommendation(key, ph)
            }
    return {
        'status': 'unknown',
        'label': 'نامشخص',
        'color': 'gray',
        'range_min': 0,
        'range_max': 0,
        'recommendation': 'pH در محدوده نامشخص است. لطفاً بررسی کنید.'
    }


def _get_ph_recommendation(status: str, ph: float) -> str:
    """تولید توصیه بر اساس وضعیت pH"""
    recommendations = {
        'critical_low': f'pH بسیار پایین است ({ph:.2f}). خطر اسیدیته شدید! از کودهای قلیایی یا اسیدشویی استفاده کنید.',
        'low': f'pH پایین است ({ph:.2f}). ممکن است جذب برخی عناصر کاهش یابد. pH را افزایش دهید.',
        'optimal': f'pH در محدوده مطلوب است ({ph:.2f}).',
        'high': f'pH بالا است ({ph:.2f}). ممکن است جذب ریزمغذی‌ها کاهش یابد. pH را کاهش دهید.',
        'critical_high': f'pH بسیار بالا است ({ph:.2f}). خطر قلیائیت شدید! از اسید فسفریک یا اسید نیتریک استفاده کنید.'
    }
    return recommendations.get(status, 'pH در محدوده نامشخص است.')


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
    issues = []
    recommendations = []
    
    # بررسی EC
    ec_status = _get_ec_status(ec)
    if ec_status['status'] in ['low', 'high', 'critical']:
        issues.append(ec_status['label'].lower())
        recommendations.append(ec_status['recommendation'])
    
    # بررسی pH
    ph_status = _get_ph_status(ph)
    if ph_status['status'] in ['low', 'high', 'critical_low', 'critical_high']:
        issues.append(ph_status['label'].lower())
        recommendations.append(ph_status['recommendation'])
    
    # بررسی ترکیبی
    if ec < 0.8 and ph < 5.0:
        recommendations.append('محلول بسیار رقیق و اسیدی است. هم غلظت و هم pH را تنظیم کنید.')
    elif ec > 3.0 and ph > 7.0:
        recommendations.append('محلول بسیار غلیظ و قلیایی است. خطر رسوب و شوری وجود دارد.')
    elif ec > 3.0 and ph < 5.0:
        recommendations.append('محلول غلیظ و اسیدی است. خطر خوردگی و سمیت وجود دارد.')
    elif ec < 0.8 and ph > 7.0:
        recommendations.append('محلول رقیق و قلیایی است. ممکن است کمبود عناصر رخ دهد.')
    
    # تعیین وضعیت کلی
    if not issues:
        status = 'optimal'
        status_label = 'مطلوب'
        color = 'success'
        message = 'EC و pH در محدوده مطلوب هستند.'
    elif len(issues) == 1:
        status = 'warning'
        status_label = 'نیاز به توجه'
        color = 'warning'
        message = f'{issues[0]}. {recommendations[0]}'
    else:
        status = 'critical'
        status_label = 'نیاز به اصلاح'
        color = 'danger'
        message = f'{" و ".join(issues)}. {" و ".join(recommendations)}'
    
    return {
        'status': status,
        'status_label': status_label,
        'color': color,
        'message': message,
        'issues': issues,
        'recommendations': list(set(recommendations)),
        'ec': ec,
        'ph': ph,
        'water_ec': water_ec,
        'water_ph': water_ph,
        'ec_status': ec_status['status'],
        'ec_label': ec_status['label'],
        'ph_status': ph_status['status'],
        'ph_label': ph_status['label']
    }


# ============================================================
# 🆕 تابع تعادل یونی خودکار (اصلاح شده - تکمیل شده)
# ============================================================

def auto_balance_ion(
    concentrations: Dict[str, float],
    target_cation: Optional[float] = None,
    target_anion: Optional[float] = None,
    unit: str = "ppm"
) -> Dict[str, Any]:
    """
    تعادل یونی خودکار با اضافه کردن یون‌های پادبار
    
    اگر کاتیون بیشتر باشد → کلر (Cl) اضافه می‌شود
    اگر آنیون بیشتر باشد → سدیم (Na) اضافه می‌شود
    
    ✅ اصلاح شده: مقدار دقیق‌تری برای یون‌های پادبار محاسبه می‌شود
    ✅ از اضافه شدن بیش از حد جلوگیری می‌شود
    ✅ تابع به طور کامل تکمیل شده است
    
    Args:
        concentrations: دیکشنری غلظت عناصر فعلی
        target_cation: مقدار هدف کاتیون (اختیاری)
        target_anion: مقدار هدف آنیون (اختیاری)
        unit: واحد ورودی
    
    Returns:
        Dict: شامل غلظت‌های جدید و اطلاعات تعادل
    """
    result = concentrations.copy()
    
    # محاسبه تعادل فعلی
    cation, anion, is_balanced, details = calculate_ion_balance(result, unit)
    
    if is_balanced:
        return {
            'concentrations': result,
            'cation': cation,
            'anion': anion,
            'is_balanced': True,
            'added_element': None,
            'added_amount': 0,
            'message': 'تعادل یونی از قبل برقرار است.',
            'original_cation': cation,
            'original_anion': anion,
            'difference': 0.0
        }
    
    # محاسبه اختلاف
    difference = abs(cation - anion)
    
    # ✅ اصلاح: ضریب 0.8 برای جلوگیری از اضافه شدن بیش از حد
    compensation_factor = 0.8
    
    if cation > anion:
        # کاتیون بیشتر است → کلر (Cl) اضافه می‌شود
        cl_meq = difference * compensation_factor
        cl_ppm = cl_meq * MOLECULAR_WEIGHTS['Cl'] / abs(VALENCES['Cl'])
        result['Cl'] = result.get('Cl', 0) + round(cl_ppm, 2)
        added_element = 'Cl'
        added_amount = round(cl_ppm, 2)
    else:
        # آنیون بیشتر است → سدیم (Na) اضافه می‌شود
        na_meq = difference * compensation_factor
        na_ppm = na_meq * MOLECULAR_WEIGHTS['Na'] / abs(VALENCES['Na'])
        result['Na'] = result.get('Na', 0) + round(na_ppm, 2)
        added_element = 'Na'
        added_amount = round(na_ppm, 2)
    
    # بررسی مجدد تعادل
    new_cation, new_anion, new_balanced, new_details = calculate_ion_balance(result, unit)
    new_difference = abs(new_cation - new_anion)
    
    # تعیین پیام مناسب
    if new_balanced:
        message = f'✅ تعادل یونی با اضافه کردن {added_element} برقرار شد.'
    elif new_difference < difference:
        message = f'⚠️ تعادل کامل برقرار نشد اما اختلاف از {difference:.2f} به {new_difference:.2f} meq/L کاهش یافت.'
    else:
        message = f'⚠️ تعادل برقرار نشد. اختلاف: {new_difference:.2f} meq/L'
    
    return {
        'concentrations': result,
        'cation': new_cation,
        'anion': new_anion,
        'is_balanced': new_balanced,
        'added_element': added_element,
        'added_amount': added_amount,
        'message': message,
        'original_cation': cation,
        'original_anion': anion,
        'difference': new_difference,
        'original_difference': difference,
        'details': new_details
    }


# ============================================================
# توابع کمکی اضافی
# ============================================================

def calculate_balance_percentage(cation: float, anion: float) -> float:
    """
    محاسبه درصد تعادل یونی
    
    Args:
        cation: مجموع کاتیون‌ها (meq/L)
        anion: مجموع آنیون‌ها (meq/L)
    
    Returns:
        float: درصد تعادل (0-100)
    """
    if cation == 0 and anion == 0:
        return 100.0
    
    total = (cation + anion) / 2
    if total == 0:
        return 0.0
    
    diff = abs(cation - anion)
    balance_percent = 100 - (diff / total * 100)
    return max(0, min(100, balance_percent))


def get_balance_summary(
    cation: float,
    anion: float,
    is_balanced: bool
) -> Dict[str, Any]:
    """
    دریافت خلاصه کامل تعادل یونی
    
    Args:
        cation: مجموع کاتیون‌ها (meq/L)
        anion: مجموع آنیون‌ها (meq/L)
        is_balanced: وضعیت تعادل
    
    Returns:
        Dict: خلاصه کامل تعادل
    """
    balance_percent = calculate_balance_percentage(cation, anion)
    difference = abs(cation - anion)
    
    return {
        'cation_total': round(cation, 4),
        'anion_total': round(anion, 4),
        'difference': round(difference, 4),
        'balance_percent': round(balance_percent, 2),
        'is_balanced': is_balanced,
        'status': 'balanced' if is_balanced else 'unbalanced',
        'tolerance': BALANCE_TOLERANCE,
        'recommendation': _get_recommendation(cation, anion, is_balanced)
    }


def validate_concentrations(
    concentrations: Dict[str, float],
    unit: str = "ppm"
) -> Dict[str, Any]:
    """
    اعتبارسنجی غلظت‌های ورودی
    
    Args:
        concentrations: دیکشنری غلظت عناصر
        unit: واحد ورودی
    
    Returns:
        Dict: نتایج اعتبارسنجی
    """
    errors = []
    warnings = []
    
    for element, value in concentrations.items():
        if value is None:
            errors.append(f'مقدار {element} نامعتبر است (None)')
            continue
        
        if not isinstance(value, (int, float)):
            errors.append(f'مقدار {element} باید عددی باشد')
            continue
        
        if value < 0:
            errors.append(f'مقدار {element} نمی‌تواند منفی باشد')
            continue
        
        # بررسی محدوده استاندارد (در صورت وجود)
        standard_range = get_element_standard_range(element)
        if standard_range:
            if value < standard_range['min'] * 0.1:
                warnings.append(f'{element} بسیار کم است (ممکن است خطا در ورودی داشته باشید)')
            elif value > standard_range['max'] * 10:
                warnings.append(f'{element} بسیار زیاد است (ممکن است خطا در ورودی داشته باشید)')
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'element_count': len(concentrations),
        'valid_elements': len([v for v in concentrations.values() if v is not None and v >= 0])
    }