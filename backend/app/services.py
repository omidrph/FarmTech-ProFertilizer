# backend/app/services.py
"""منطق کسب‌وکار و محاسبات تخصصی نرم‌افزار تغذیه سبز"""
import math
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.models import User, Report, Fertilizer
from app.schemas import InterpretationResponse, IonBalanceResponse, ElementStatusResponse

# ============================================================
# لیست عناصر و ثابت‌های محاسباتی
# ============================================================
ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo']

# وزن مولکولی عناصر (برای تبدیل واحدها)
MOLECULAR_WEIGHTS = {
    'N-NO3': 62.0049,
    'P': 30.9738,
    'S': 32.065,
    'N-NH4': 18.0385,
    'K': 39.0983,
    'Ca': 40.078,
    'Mg': 24.305,
    'Na': 22.9898,
    'Cl': 35.453,
    'Fe': 55.845,
    'Mn': 54.938,
    'Zn': 65.38,
    'B': 10.81,
    'Cu': 63.546,
    'Mo': 95.95
}

# ظرفیت یونی عناصر
VALENCES = {
    'N-NO3': 1,
    'P': 1,
    'S': 1,
    'N-NH4': 1,
    'K': 1,
    'Ca': 2,
    'Mg': 2,
    'Na': 1,
    'Cl': 1,
    'Fe': 2,
    'Mn': 2,
    'Zn': 2,
    'B': 1,
    'Cu': 2,
    'Mo': 2
}

# ============================================================
# 🆕 ثابت‌های استاندارد EC (واحد پیش‌فرض: dS/m)
# ============================================================
EC_STANDARDS = {
    # حداقل مقدار معتبر EC
    'MIN_VALID_EC': 0.1,
    # مقدار پیش‌فرض منطقی برای آب طبیعی
    'DEFAULT_EC': 0.8,
    # محدوده‌های استاندارد (دقیق‌تر)
    'RANGES': [
        {'min': 0, 'max': 0.75, 'level': 'excellent', 'label': 'عالی', 'color': 'success', 'description': 'مناسب برای همه گیاهان'},
        {'min': 0.75, 'max': 2.0, 'level': 'good', 'label': 'قابل قبول', 'color': 'warning', 'description': 'نیاز به بررسی نوع گیاه'},
        {'min': 2.0, 'max': 3.0, 'level': 'moderate', 'label': 'نیاز به توجه', 'color': 'warning', 'description': 'فقط گیاهان مقاوم به شوری'},
        {'min': 3.0, 'max': float('inf'), 'level': 'critical', 'label': 'بحرانی', 'color': 'danger', 'description': 'نامناسب برای آبیاری'}
    ]
}

# ============================================================
# 🆕 توابع تبدیل واحد EC
# ============================================================
def convert_ec_unit(value: float, from_unit: str, to_unit: str) -> float:
    """
    تبدیل واحد EC
    واحدها: dS/m, mS/cm, μS/cm
    
    روابط:
    - 1 dS/m = 1 mS/cm
    - 1 dS/m = 1000 μS/cm
    """
    if from_unit == to_unit:
        return value
    
    # ابتدا به dS/m تبدیل می‌کنیم
    if from_unit == 'dS/m':
        ds_value = value
    elif from_unit == 'mS/cm':
        ds_value = value  # 1 mS/cm = 1 dS/m
    elif from_unit == 'μS/cm':
        ds_value = value / 1000
    else:
        return value
    
    # سپس به واحد مقصد تبدیل می‌کنیم
    if to_unit == 'dS/m':
        return ds_value
    elif to_unit == 'mS/cm':
        return ds_value  # 1 dS/m = 1 mS/cm
    elif to_unit == 'μS/cm':
        return ds_value * 1000
    else:
        return value

def calculate_tds(ec_ds: float) -> float:
    """
    محاسبه TDS از روی EC
    فرمول: TDS (mg/L) ≈ EC (dS/m) × 640
    
    Args:
        ec_ds: مقدار EC بر حسب dS/m
    
    Returns:
        مقدار TDS بر حسب mg/L
    """
    return ec_ds * 640

def get_ec_status(ec_value: float, unit: str = 'dS/m') -> Dict[str, Any]:
    """
    دریافت وضعیت EC بر اساس مقدار
    
    Args:
        ec_value: مقدار EC
        unit: واحد EC
    
    Returns:
        Dict با اطلاعات وضعیت
    """
    # تبدیل به dS/m برای مقایسه
    ec_ds = convert_ec_unit(ec_value, unit, 'dS/m')
    
    if ec_ds <= 0:
        return {
            'level': 'invalid',
            'label': 'نامعتبر',
            'description': 'EC نمی‌تواند صفر باشد',
            'color': 'danger'
        }
    
    for range_info in EC_STANDARDS['RANGES']:
        if ec_ds >= range_info['min'] and ec_ds < range_info['max']:
            return {
                'level': range_info['level'],
                'label': range_info['label'],
                'description': range_info['description'],
                'color': range_info['color']
            }
    
    return {
        'level': 'critical',
        'label': 'بحرانی',
        'description': 'نامناسب برای آبیاری',
        'color': 'danger'
    }

# ============================================================
# توابع تبدیل واحدها
# ============================================================
def ppm_to_meq(ppm: float, element: str) -> float:
    """تبدیل PPM به MEQ/L"""
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    valence = VALENCES.get(element, 0)
    if mw == 0 or valence == 0:
        return 0
    return (ppm * valence) / mw

def meq_to_ppm(meq: float, element: str) -> float:
    """تبدیل MEQ/L به PPM"""
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    valence = VALENCES.get(element, 0)
    if valence == 0:
        return 0
    return (meq * mw) / valence

def ppm_to_mmol(ppm: float, element: str) -> float:
    """تبدیل PPM به MMOLS/L"""
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    if mw == 0:
        return 0
    return ppm / mw

def mmol_to_ppm(mmol: float, element: str) -> float:
    """تبدیل MMOLS/L به PPM"""
    mw = MOLECULAR_WEIGHTS.get(element, 0)
    return mmol * mw

# ============================================================
# توابع محاسبه تعادل یونی
# ============================================================
def calculate_ion_balance(
    target_values: Dict[str, float],
    unit: str = "ppm"
) -> Tuple[float, float, bool]:
    """
    محاسبه تعادل کاتیون و آنیون
    """
    cation = 0.0
    anion = 0.0
    cations = ['K', 'Ca', 'Mg', 'Na']
    anions = ['N-NO3', 'P', 'S', 'N-NH4', 'Cl']
    
    for element, value in target_values.items():
        if value is None or value == 0:
            continue
        if element not in ELEMENTS:
            continue
        
        # تبدیل به MEQ برای محاسبه
        if unit == "ppm":
            meq_value = ppm_to_meq(value, element)
        elif unit == "mmol":
            meq_value = value * VALENCES.get(element, 0)
        else:  # meq
            meq_value = value
        
        if element in cations:
            cation += meq_value
        elif element in anions:
            anion += meq_value
    
    is_balanced = abs(cation - anion) < 0.5
    return cation, anion, is_balanced

# ============================================================
# توابع محاسبه محلول نهایی
# ============================================================
def calculate_final_solution(
    target_values: Dict[str, float],
    water_values: Dict[str, float],
    fertilizer_contributions: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه مقدار نهایی هر عنصر
    """
    final_values = {}
    for element in ELEMENTS:
        target = target_values.get(element, 0)
        water = water_values.get(element, 0)
        fertilizer = fertilizer_contributions.get(element, 0)
        final_values[element] = target - (water + fertilizer)
    return final_values

# ============================================================
# توابع محاسبه مقدار کود
# ============================================================
def calculate_fertilizer_amount(
    fertilizer: Fertilizer,
    weight: float,
    purity: float
) -> Dict[str, float]:
    """
    محاسبه سهم هر عنصر از یک کود
    """
    result = {}
    elements = fertilizer.elements or {}
    for element, percentage in elements.items():
        if element in ELEMENTS and percentage:
            result[element] = (weight * (percentage / 100) * (purity / 100))
    return result

def calculate_total_fertilizer_contribution(
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, float]:
    """
    محاسبه مجموع سهم همه کودها
    """
    total = {element: 0.0 for element in ELEMENTS}
    for item in fertilizers:
        fertilizer = item.get('fertilizer')
        weight = item.get('weight', 0)
        purity = item.get('purity', 100)
        if fertilizer and weight > 0:
            contributions = calculate_fertilizer_amount(fertilizer, weight, purity)
            for element, value in contributions.items():
                total[element] = total.get(element, 0) + value
    return total

# ============================================================
# توابع محاسبه اطلاعات مخازن
# ============================================================
def calculate_reservoir_data(
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    محاسبه اطلاعات مخازن A, B, C
    """
    reservoir_a = []
    reservoir_b = []
    reservoir_c = []
    
    for item in fertilizers:
        fertilizer = item.get('fertilizer')
        weight = item.get('weight', 0)
        if not fertilizer or weight <= 0:
            continue
        
        # اسیدها معمولاً در مخزن C
        if fertilizer.is_acid:
            reservoir_c.append({
                'name': fertilizer.name,
                'amount': weight
            })
        # نمک‌های کلسیم در مخزن A
        elif 'Ca' in fertilizer.name or 'کلسیم' in fertilizer.name:
            reservoir_a.append({
                'name': fertilizer.name,
                'amount': weight
            })
        # بقیه در مخزن B
        else:
            reservoir_b.append({
                'name': fertilizer.name,
                'amount': weight
            })
    
    return {
        'A': reservoir_a,
        'B': reservoir_b,
        'C': reservoir_c
    }

# ============================================================
# توابع تفسیر داده‌ها
# ============================================================
def generate_interpretation(
    target_values: Dict[str, float],
    final_values: Dict[str, float],
    water_analysis: Dict[str, Any],
    ion_balance: Tuple[float, float, bool]
) -> Dict[str, Any]:
    """
    تولید تفسیر کامل از داده‌ها
    """
    cation, anion, is_balanced = ion_balance
    
    # ===== وضعیت عناصر =====
    element_status = []
    for element in ELEMENTS:
        target = target_values.get(element, 0)
        actual = final_values.get(element, 0)
        diff = target - actual
        
        if diff > 5:
            status = 'deficient'
            message = f'کمبود {abs(diff):.2f} واحد'
        elif diff < -5:
            status = 'excessive'
            message = f'بیش‌بود {abs(diff):.2f} واحد'
        elif diff < -15:
            status = 'toxic'
            message = 'سمیت احتمالی'
        else:
            status = 'sufficient'
            message = 'وضعیت مطلوب'
        
        element_status.append({
            'element': element,
            'target': target,
            'actual': actual,
            'difference': diff,
            'status': status,
            'message': message
        })
    
    # ===== کیفیت آب =====
    salinity = water_analysis.get('water_salinity', 0)
    if salinity > 2.5:
        water_quality = {
            'impact': 'بالا',
            'recommendation': 'استفاده از آب با شوری کمتر توصیه می‌شود'
        }
    elif salinity > 1.5:
        water_quality = {
            'impact': 'متوسط',
            'recommendation': 'توجه به عناصر سمی در آب'
        }
    else:
        water_quality = {
            'impact': 'مناسب',
            'recommendation': 'نیازی به اقدام نیست'
        }
    
    # ===== توصیه‌های کودی =====
    recommendations = []
    if not is_balanced:
        recommendations.append({
            'issue': 'عدم تعادل یونی',
            'suggestion': 'مقادیر کاتیون و آنیون را تنظیم کنید تا برابر شوند',
            'priority': 'high'
        })
    
    for item in element_status:
        if item['status'] in ['deficient', 'toxic']:
            recommendations.append({
                'issue': f"عنصر {item['element']}: {item['message']}",
                'suggestion': (
                    'افزایش مقدار این عنصر در فرمول غذایی'
                    if item['status'] == 'deficient'
                    else 'کاهش مقدار این عنصر یا بررسی کیفیت آب'
                ),
                'priority': 'high' if item['status'] == 'toxic' else 'medium'
            })
    
    # ===== خلاصه =====
    problem_elements = [item['element'] for item in element_status if item['status'] != 'sufficient']
    summary = f"""
گزارش تفسیر تغذیه گیاه:
- تعادل یونی: {'برقرار ✅' if is_balanced else 'نامتعادل ⚠️'}
- عناصر دارای مشکل: {', '.join(problem_elements) if problem_elements else 'هیچکدام'}
- کیفیت آب: {water_quality['impact']}
- تعداد توصیه‌ها: {len(recommendations)}
"""
    
    return {
        'ion_balance': {
            'cation': cation,
            'anion': anion,
            'is_balanced': is_balanced,
            'message': 'تعادل یونی برقرار است' if is_balanced else 'تعادل یونی برقرار نیست'
        },
        'element_status': element_status,
        'water_quality': {
            'salinity': salinity,
            **water_quality
        },
        'fertilizer_recommendation': recommendations,
        'summary': summary
    }

# ============================================================
# توابع کمکی محاسباتی
# ============================================================
def convert_units(
    value: float,
    from_unit: str,
    to_unit: str,
    element: str
) -> float:
    """
    تبدیل واحدهای مختلف
    """
    if from_unit == to_unit:
        return value
    
    # ابتدا به PPM تبدیل می‌کنیم
    if from_unit == 'meq':
        ppm = meq_to_ppm(value, element)
    elif from_unit == 'mmol':
        ppm = mmol_to_ppm(value, element)
    else:
        ppm = value
    
    # سپس به واحد مقصد تبدیل می‌کنیم
    if to_unit == 'meq':
        return ppm_to_meq(ppm, element)
    elif to_unit == 'mmol':
        return ppm_to_mmol(ppm, element)
    else:
        return ppm

def format_decimal(value: float, decimals: int = 2) -> str:
    """فرمت کردن اعداد با تعداد اعشار مشخص"""
    if value is None:
        return '0.' + '0' * decimals
    return f"{value:.{decimals}f}"