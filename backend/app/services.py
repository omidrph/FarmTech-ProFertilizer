# backend/app/services.py
"""منطق کسب‌وکار و محاسبات تخصصی نرم‌افزار تغذیه سبز - نسخه پیشرفته با بهینه‌سازی"""

import math
import time
import logging
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session

from scipy.optimize import nnls, lsq_linear, minimize

logger = logging.getLogger(__name__)


# ============================================================
# لیست عناصر و ثابت‌های محاسباتی
# ============================================================
ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo']

# وزن مولکولی عناصر (g/mol)
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

# کاتیون‌ها و آنیون‌ها
CATIONS = ['K', 'Ca', 'Mg', 'Na']
ANIONS = ['N-NO3', 'P', 'S', 'N-NH4', 'Cl']

# ============================================================
# 🆕 ثابت‌های حلالیت (Ksp) برای بررسی رسوب
# ============================================================
KSP_VALUES = {
    'CaSO4': 2.4e-5,      # 25°C
    'Ca3(PO4)2': 2.0e-29,  # 25°C
    'CaCO3': 3.3e-9,       # 25°C
    'Mg(OH)2': 5.6e-12,    # 25°C
    'Fe(OH)3': 2.8e-39,    # 25°C
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


# ============================================================
# توابع تعادل یونی
# ============================================================

def calculate_ion_balance(target_values: Dict[str, float], unit: str = "ppm") -> Tuple[float, float, bool]:
    """
    محاسبه تعادل کاتیون و آنیون
    
    Args:
        target_values: مقادیر عناصر
        unit: واحد ورودی (ppm, meq, mmol)
    
    Returns:
        Tuple[float, float, bool]: (کاتیون, آنیون, آیا متعادل است)
    """
    cation = 0.0
    anion = 0.0
    
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
        
        if element in CATIONS:
            cation += meq_value
        elif element in ANIONS:
            anion += meq_value
    
    is_balanced = abs(cation - anion) < 0.5
    return cation, anion, is_balanced


# ============================================================
# 🆕 توابع بهینه‌سازی پیشرفته
# ============================================================

def build_optimization_matrix(
    target_values: Dict[str, float],
    fertilizers: List[Dict[str, Any]],
    water_values: Optional[Dict[str, float]] = None
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
    """
    ساخت ماتریس ضرایب برای بهینه‌سازی
    
    Args:
        target_values: عناصر هدف
        fertilizers: لیست کودها
        water_values: عناصر موجود در آب
    
    Returns:
        Tuple: (ماتریس A, بردار b, لیست عناصر فعال, لیست اسامی کودها)
    """
    water_values = water_values or {}
    
    # فیلتر کردن عناصر با هدف مثبت
    active_elements = [el for el in ELEMENTS if target_values.get(el, 0) > 0]
    
    if not active_elements:
        raise ValueError("هیچ عنصر هدفی تعریف نشده است")
    
    # ساخت ماتریس A و بردار b
    A = []
    b = []
    fertilizer_names = []
    
    for element in active_elements:
        target = target_values.get(element, 0)
        water = water_values.get(element, 0)
        b.append(max(0, target - water))  # کسر کیفیت آب
        
        row = []
        for fert in fertilizers:
            # محاسبه سهم عنصر از کود (با در نظر گرفتن خلوص)
            element_pct = fert.get('elements', {}).get(element, 0)
            purity = fert.get('purity', 100) / 100
            contribution = (element_pct / 100) * purity
            row.append(contribution)
        A.append(row)
    
    # جمع‌آوری اسامی کودها
    fertilizer_names = [fert.get('name', f'کود {i}') for i, fert in enumerate(fertilizers)]
    
    return np.array(A), np.array(b), active_elements, fertilizer_names


def optimize_with_nnls(
    A: np.ndarray,
    b: np.ndarray,
    element_weights: Optional[Dict[str, float]] = None,
    active_elements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    بهینه‌سازی با روش NNLS (Non-Negative Least Squares)
    
    مزیت: تضمین وزن‌های غیرمنفی
    """
    start_time = time.time()
    
    # اعمال وزن‌دهی به عناصر
    if element_weights and active_elements:
        weight_matrix = np.diag([element_weights.get(el, 1.0) for el in active_elements])
        A_weighted = np.dot(weight_matrix, A)
        b_weighted = np.dot(weight_matrix, b)
    else:
        A_weighted = A
        b_weighted = b
    
    try:
        weights, residual = nnls(A_weighted, b_weighted)
        iterations = 1  # NNLS مستقیم حل می‌کند
        is_converged = True
        
        return {
            'weights': weights,
            'residual': residual,
            'iterations': iterations,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': is_converged,
            'method': 'nnls'
        }
    except Exception as e:
        logger.error(f"Error in NNLS optimization: {e}")
        raise


def optimize_with_lsq_linear(
    A: np.ndarray,
    b: np.ndarray,
    max_iterations: int = 1000,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    بهینه‌سازی با روش Least Squares با کران‌ها
    
    مزیت: سرعت بالا برای مسائل بزرگ
    """
    start_time = time.time()
    
    try:
        result = lsq_linear(
            A, 
            b,
            bounds=(0, np.inf),
            max_iter=max_iterations,
            tol=tolerance
        )
        
        return {
            'weights': result.x,
            'residual': result.cost,
            'iterations': result.nit,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': result.success,
            'method': 'lsq_linear'
        }
    except Exception as e:
        logger.error(f"Error in lsq_linear optimization: {e}")
        raise


def optimize_with_cost(
    A: np.ndarray,
    b: np.ndarray,
    costs: np.ndarray,
    cost_weight: float = 0.01,
    max_iterations: int = 1000,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    بهینه‌سازی با در نظر گرفتن هزینه
    
    min ||Ax - b||^2 + λ * cost(x)
    
    مزیت: انتخاب ارزان‌ترین ترکیب در صورت وجود چند جواب
    """
    start_time = time.time()
    
    def objective(x):
        error = np.sum((np.dot(A, x) - b) ** 2)
        cost = np.sum(x * costs)
        return error + cost_weight * cost
    
    def gradient(x):
        grad_error = 2 * np.dot(A.T, np.dot(A, x) - b)
        grad_cost = costs
        return grad_error + cost_weight * np.array(grad_cost)
    
    try:
        result = minimize(
            objective,
            x0=np.zeros(A.shape[1]),
            method='L-BFGS-B',
            jac=gradient,
            bounds=[(0, None)] * A.shape[1],
            options={
                'maxiter': max_iterations,
                'ftol': tolerance,
                'gtol': tolerance
            }
        )
        
        return {
            'weights': result.x,
            'residual': result.fun,
            'iterations': result.nit,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': result.success,
            'method': 'lsq_linear_with_cost'
        }
    except Exception as e:
        logger.error(f"Error in cost optimization: {e}")
        raise


def calculate_final_concentrations(
    weights: np.ndarray,
    A: np.ndarray,
    water_values: Dict[str, float],
    active_elements: List[str]
) -> Dict[str, float]:
    """
    محاسبه غلظت نهایی عناصر
    
    Args:
        weights: وزن‌های بهینه
        A: ماتریس ضرایب
        water_values: عناصر موجود در آب
        active_elements: لیست عناصر فعال
    
    Returns:
        Dict[str, float]: غلظت نهایی هر عنصر
    """
    final_concentrations = {}
    for i, element in enumerate(active_elements):
        final_concentrations[element] = np.dot(A[i], weights) + water_values.get(element, 0)
    return final_concentrations


def calculate_target_achievement(
    target_values: Dict[str, float],
    final_concentrations: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه درصد تحقق هر عنصر
    
    Args:
        target_values: مقادیر هدف
        final_concentrations: مقادیر نهایی
    
    Returns:
        Dict[str, float]: درصد تحقق هر عنصر
    """
    achievement = {}
    for element, target in target_values.items():
        if target == 0:
            achievement[element] = 100.0
        else:
            actual = final_concentrations.get(element, 0)
            achievement[element] = min(100, (actual / target) * 100)
    return achievement


def check_precipitation(concentrations: Dict[str, float]) -> Dict[str, Any]:
    """
    بررسی رسوب احتمالی با استفاده از Ksp
    
    Args:
        concentrations: غلظت عناصر (ppm)
    
    Returns:
        Dict: شامل وضعیت ایمنی و خطرات
    """
    risks = []
    suggestions = []
    is_safe = True
    
    # تبدیل ppm به mol/L
    def ppm_to_mol(ppm: float, element: str) -> float:
        mw = MOLECULAR_WEIGHTS.get(element, 0)
        if mw == 0:
            return 0
        return ppm / (mw * 1000)  # ppm = mg/L, تقسیم بر 1000 برای تبدیل به g/L
    
    ca = ppm_to_mol(concentrations.get('Ca', 0), 'Ca')
    so4 = ppm_to_mol(concentrations.get('S', 0), 'S')
    po4 = ppm_to_mol(concentrations.get('P', 0), 'P')
    mg = ppm_to_mol(concentrations.get('Mg', 0), 'Mg')
    fe = ppm_to_mol(concentrations.get('Fe', 0), 'Fe')
    
    # بررسی CaSO4
    if ca > 0 and so4 > 0:
        ion_product = ca * so4
        if ion_product > KSP_VALUES['CaSO4']:
            is_safe = False
            risks.append({
                'compound': 'CaSO4',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['CaSO4'],
                'is_risky': True,
                'suggestion': 'کلسیم و سولفات را در مخازن جداگانه قرار دهید (A و B)'
            })
            suggestions.append('کلسیم و سولفات را در مخازن جداگانه قرار دهید')
    
    # بررسی Ca3(PO4)2
    if ca > 0 and po4 > 0:
        ion_product = (ca ** 3) * (po4 ** 2)
        if ion_product > KSP_VALUES['Ca3(PO4)2']:
            is_safe = False
            risks.append({
                'compound': 'Ca3(PO4)2',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Ca3(PO4)2'],
                'is_risky': True,
                'suggestion': 'کلسیم و فسفات را در مخازن جداگانه قرار دهید (A و B)'
            })
            suggestions.append('کلسیم و فسفات را در مخازن جداگانه قرار دهید')
    
    # بررسی Mg(OH)2
    if mg > 0:
        # OH- از آب خالص (10^-7) و همچنین از سایر منابع
        oh = 1e-7  # تقریب ساده
        ion_product = mg * (oh ** 2)
        if ion_product > KSP_VALUES['Mg(OH)2']:
            is_safe = False
            risks.append({
                'compound': 'Mg(OH)2',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Mg(OH)2'],
                'is_risky': True,
                'suggestion': 'pH را کاهش دهید یا منیزیم را با کلات استفاده کنید'
            })
            suggestions.append('pH را کاهش دهید یا منیزیم را با کلات استفاده کنید')
    
    # بررسی Fe(OH)3
    if fe > 0:
        oh = 1e-7  # تقریب ساده
        ion_product = fe * (oh ** 3)
        if ion_product > KSP_VALUES['Fe(OH)3']:
            is_safe = False
            risks.append({
                'compound': 'Fe(OH)3',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Fe(OH)3'],
                'is_risky': True,
                'suggestion': 'از آهن کلاته استفاده کنید (Fe-EDTA یا Fe-EDDHA)'
            })
            suggestions.append('از آهن کلاته استفاده کنید')
    
    return {
        'is_safe': is_safe,
        'risks': risks,
        'suggestions': suggestions
    }


def calculate_reservoir_data_optimized(
    fertilizers: List[Dict[str, Any]],
    weights: np.ndarray
) -> Dict[str, List[Dict[str, Any]]]:
    """
    محاسبه توزیع مواد در مخازن A, B, C (نسخه بهینه‌شده)
    
    قوانین:
    - مخزن A: کودهای کلسیمی (Ca)
    - مخزن B: سایر کودها (پتاسیم، منیزیم، فسفات، نیترات، ...)
    - مخزن C: اسیدها (H3PO4, HNO3, H2SO4)
    """
    reservoir_a = []
    reservoir_b = []
    reservoir_c = []
    
    for i, fert in enumerate(fertilizers):
        weight = weights[i]
        if weight <= 0:
            continue
        
        name = fert.get('name', 'نامشخص')
        is_acid = fert.get('is_acid', False)
        
        # اسیدها در مخزن C
        if is_acid:
            reservoir_c.append({
                'name': name,
                'amount': round(weight, 3)
            })
        # کودهای کلسیمی در مخزن A
        elif 'Ca' in fert.get('elements', {}) and fert['elements'].get('Ca', 0) > 0:
            reservoir_a.append({
                'name': name,
                'amount': round(weight, 3)
            })
        # بقیه در مخزن B
        else:
            reservoir_b.append({
                'name': name,
                'amount': round(weight, 3)
            })
    
    return {
        'A': reservoir_a,
        'B': reservoir_b,
        'C': reservoir_c
    }


def generate_optimization_summary(
    weights: Dict[str, float],
    concentrations: Dict[str, float],
    target_values: Dict[str, float],
    achievement: Dict[str, float],
    cost_total: float,
    ion_balance: Tuple[float, float, bool],
    warnings: List[str],
    suggestions: List[str]
) -> str:
    """
    تولید خلاصه متنی از نتیجه بهینه‌سازی
    """
    cation, anion, is_balanced = ion_balance
    
    summary_lines = [
        "📊 **خلاصه نتیجه بهینه‌سازی**",
        "",
        f"💰 **هزینه کل:** {cost_total:,.0f} تومان",
        f"⚖️ **تعادل یونی:** {'✅ متعادل' if is_balanced else '⚠️ نامتعادل'}",
        f"   کاتیون: {cation:.2f} meq/L | آنیون: {anion:.2f} meq/L",
        "",
        "📈 **درصد تحقق عناصر هدف:**"
    ]
    
    # عناصر با تحقق کمتر از ۷۰٪
    low_achievement = []
    for element, pct in achievement.items():
        if pct < 70:
            low_achievement.append(f"{element}: {pct:.0f}%")
        summary_lines.append(f"   - {element}: {pct:.0f}%")
    
    if low_achievement:
        summary_lines.append("")
        summary_lines.append(f"⚠️ **عناصر با تحقق کم:** {', '.join(low_achievement)}")
    
    if warnings:
        summary_lines.append("")
        summary_lines.append("⚠️ **هشدارها:**")
        for warning in warnings:
            summary_lines.append(f"   - {warning}")
    
    if suggestions:
        summary_lines.append("")
        summary_lines.append("💡 **پیشنهادات:**")
        for suggestion in suggestions:
            summary_lines.append(f"   - {suggestion}")
    
    return "\n".join(summary_lines)


# ============================================================
# 🆕 تابع اصلی بهینه‌سازی (Heart of the System)
# ============================================================

def optimize_fertilizers(
    target_values: Dict[str, float],
    fertilizers: List[Dict[str, Any]],
    water_values: Optional[Dict[str, float]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    🎯 تابع اصلی بهینه‌سازی ترکیب کودها
    
    این تابع قلب تپنده جدید FarmTech است.
    با استفاده از الگوریتم NNLS، بهترین ترکیب کودها را محاسبه می‌کند.
    
    Args:
        target_values: عناصر هدف (ppm)
        fertilizers: لیست کودها با عناصر و قیمت
        water_values: عناصر موجود در آب (اختیاری)
        options: تنظیمات بهینه‌سازی
    
    Returns:
        Dict: شامل وزن‌ها، غلظت‌ها، خطا، تحلیل و توصیه‌ها
    """
    start_time = time.time()
    
    # ===== ۱. آماده‌سازی =====
    water_values = water_values or {}
    options = options or {}
    
    method = options.get('method', 'nnls')
    element_weights = options.get('element_weights', {})
    max_iterations = options.get('max_iterations', 1000)
    tolerance = options.get('tolerance', 1e-6)
    cost_weight = options.get('cost_weight', 0.01)
    use_precipitation_check = options.get('use_precipitation_check', True)
    use_ion_balance_check = options.get('use_ion_balance_check', True)
    
    logger.info(f"🚀 Starting optimization with method: {method}")
    logger.info(f"   Targets: {len(target_values)} elements")
    logger.info(f"   Fertilizers: {len(fertilizers)} items")
    
    # ===== ۲. ساخت ماتریس =====
    try:
        A, b, active_elements, fertilizer_names = build_optimization_matrix(
            target_values, fertilizers, water_values
        )
    except ValueError as e:
        return {
            'error': str(e),
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': (0, 0, False),
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'reservoir_data': {'A': [], 'B': [], 'C': []},
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': f"❌ خطا: {str(e)}"
        }
    
    if A.shape[1] == 0:
        return {
            'error': 'هیچ کودی انتخاب نشده است',
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': (0, 0, False),
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'reservoir_data': {'A': [], 'B': [], 'C': []},
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': '❌ هیچ کودی انتخاب نشده است. لطفاً حداقل یک کود را انتخاب کنید.'
        }
    
    # ===== ۳. اجرای بهینه‌سازی =====
    costs = np.array([fert.get('price_per_kg', 0) / 1000 for fert in fertilizers])
    
    result = None
    
    try:
        if method == 'nnls':
            result = optimize_with_nnls(A, b, element_weights, active_elements)
        elif method == 'lsq_linear':
            result = optimize_with_lsq_linear(A, b, max_iterations, tolerance)
        elif method == 'lsq_linear_with_cost':
            result = optimize_with_cost(A, b, costs, cost_weight, max_iterations, tolerance)
        else:
            raise ValueError(f"روش {method} پشتیبانی نمی‌شود")
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        return {
            'error': f'خطا در بهینه‌سازی: {str(e)}',
            'weights': {},
            'concentrations': {},
            'residual_error': 0,
            'cost_total': 0,
            'ion_balance': (0, 0, False),
            'target_achievement': {},
            'warnings': [],
            'suggestions': [],
            'reservoir_data': {'A': [], 'B': [], 'C': []},
            'iterations': 0,
            'convergence_time_ms': (time.time() - start_time) * 1000,
            'is_converged': False,
            'summary': f"❌ خطا در بهینه‌سازی: {str(e)}"
        }
    
    weights = result['weights']
    residual = result['residual']
    iterations = result['iterations']
    convergence_time = result['convergence_time_ms']
    is_converged = result['is_converged']
    
    # ===== ۴. محاسبه نتایج =====
    # اطمینان از غیرمنفی بودن وزن‌ها
    weights = np.maximum(weights, 0)
    
    # محاسبه غلظت نهایی
    final_concentrations = calculate_final_concentrations(
        weights, A, water_values, active_elements
    )
    
    # محاسبه هزینه کل
    total_cost = np.sum(weights * costs)
    
    # محاسبه تعادل یونی
    cation, anion, is_balanced = calculate_ion_balance(final_concentrations)
    
    # محاسبه درصد تحقق - اصلاح شده برای نمایش اهداف صحیح
    achievement = calculate_target_achievement(target_values, final_concentrations)
    
    # ===== ۵. بررسی رسوب =====
    warnings = []
    suggestions = []
    
    if use_precipitation_check:
        precip_result = check_precipitation(final_concentrations)
        if not precip_result['is_safe']:
            warnings.extend([f"خطر رسوب: {risk['compound']}" for risk in precip_result['risks']])
            suggestions.extend(precip_result['suggestions'])
    
    # ===== ۶. بررسی تعادل یونی =====
    if use_ion_balance_check and not is_balanced:
        warnings.append(f"تعادل یونی برقرار نیست (اختلاف: {abs(cation - anion):.2f} meq/L)")
        suggestions.append("مقادیر کاتیون و آنیون را تنظیم کنید تا به تعادل برسید")
    
    # ===== ۷. بررسی عناصر با تحقق کم =====
    for element, pct in achievement.items():
        if pct < 70 and target_values.get(element, 0) > 0:
            warnings.append(f"عنصر {element}: {pct:.0f}% تحقق (هدف: {target_values.get(element, 0):.1f} ppm)")
            suggestions.append(f"افزایش {element} با استفاده از کود مناسب")
    
    # ===== ۸. محاسبه مخازن =====
    reservoir_data = calculate_reservoir_data_optimized(fertilizers, weights)
    
    # ===== ۹. تولید خلاصه =====
    weights_dict = {}
    for i, fert in enumerate(fertilizers):
        fert_id = fert.get('id', f'fert_{i}')
        weights_dict[fert_id] = round(weights[i], 3)
    
    summary = generate_optimization_summary(
        weights_dict,
        final_concentrations,
        target_values,
        achievement,
        total_cost,
        (cation, anion, is_balanced),
        warnings,
        suggestions
    )
    
    # ===== ۱۰. بازگشت نتیجه =====
    return {
        'weights': weights_dict,
        'concentrations': final_concentrations,
        'residual_error': residual,
        'cost_total': total_cost,
        'ion_balance': {
            'cation': cation,
            'anion': anion,
            'is_balanced': is_balanced,
            'message': 'تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️'
        },
        'target_achievement': achievement,
        'warnings': warnings,
        'suggestions': suggestions,
        'reservoir_data': reservoir_data,
        'iterations': iterations,
        'convergence_time_ms': convergence_time,
        'is_converged': is_converged,
        'summary': summary
    }


# ============================================================
# 🆕 تابع اعتبارسنجی نتایج بهینه‌سازی
# ============================================================

def validate_optimization_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    اعتبارسنجی نتایج بهینه‌سازی
    
    Args:
        result: نتیجه بهینه‌سازی
    
    Returns:
        Dict: شامل وضعیت اعتبار و خطاها
    """
    errors = []
    warnings = []
    
    # بررسی وجود وزن‌ها
    if not result.get('weights'):
        errors.append('وزن‌های بهینه محاسبه نشدند')
    
    # بررسی وجود غلظت‌ها
    if not result.get('concentrations'):
        errors.append('غلظت‌های نهایی محاسبه نشدند')
    
    # بررسی هزینه
    if result.get('cost_total', 0) < 0:
        errors.append('هزینه کل نمی‌تواند منفی باشد')
    
    # بررسی تعادل یونی
    ion_balance = result.get('ion_balance', {})
    if ion_balance.get('cation', 0) < 0 or ion_balance.get('anion', 0) < 0:
        errors.append('مقادیر کاتیون و آنیون نمی‌توانند منفی باشند')
    
    # بررسی همگرایی
    if not result.get('is_converged', False):
        warnings.append('الگوریتم به جواب کامل نرسید، نتایج ممکن است بهینه نباشند')
    
    # بررسی وزن‌های صفر
    weights = result.get('weights', {})
    zero_count = sum(1 for w in weights.values() if w == 0)
    if zero_count > 0:
        warnings.append(f'{zero_count} کود در ترکیب نهایی استفاده نشدند (وزن صفر)')
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'has_warnings': len(warnings) > 0
    }