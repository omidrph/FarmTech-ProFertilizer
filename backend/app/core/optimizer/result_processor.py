"""
پردازش نتایج بهینه‌سازی
================================

این فایل شامل توابع پردازش و فرمت‌بندی نتایج بهینه‌سازی است:
- محاسبه غلظت نهایی عناصر
- محاسبه درصد تحقق اهداف
- تولید خلاصه متنی
- اعتبارسنجی نتایج
- 🆕 تعادل یونی خودکار
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging

from ..ion_balance import (
    calculate_ion_balance,
    get_ion_balance_status,
    check_precipitation,
    ALL_ELEMENTS,
    # 🆕 تابع تعادل یونی خودکار
    auto_balance_ion
)

logger = logging.getLogger(__name__)


def calculate_final_concentrations(
    weights: np.ndarray,
    A: np.ndarray,
    water_values: Dict[str, float],
    active_elements: List[str]
) -> Dict[str, float]:
    """
    محاسبه غلظت نهایی عناصر
    
    Args:
        weights: وزن‌های بهینه هر کود
        A: ماتریس ضرایب
        water_values: عناصر موجود در آب
        active_elements: لیست عناصر فعال
    
    Returns:
        Dict[str, float]: غلظت نهایی هر عنصر (ppm)
    """
    final_concentrations = {}
    
    for i, element in enumerate(active_elements):
        fertilizer_contribution = np.dot(A[i], weights)
        water_contribution = water_values.get(element, 0)
        final_concentrations[element] = fertilizer_contribution + water_contribution
    
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
        Dict[str, float]: درصد تحقق هر عنصر (۰ تا ۱۰۰)
    """
    achievement = {}
    
    for element, target in target_values.items():
        if target is None or target == 0:
            achievement[element] = 100.0
        else:
            actual = final_concentrations.get(element, 0)
            pct = min(100, max(0, (actual / target) * 100))
            achievement[element] = pct
    
    return achievement


def generate_optimization_summary(
    weights: Dict[str, float],
    concentrations: Dict[str, float],
    target_values: Dict[str, float],
    achievement: Dict[str, float],
    cost_total: float,
    ion_balance: Tuple[float, float, bool],
    warnings: List[str],
    suggestions: List[str],
    iterations: int,
    convergence_time_ms: float,
    is_converged: bool
) -> str:
    """تولید خلاصه متنی از نتیجه بهینه‌سازی"""
    cation, anion, is_balanced = ion_balance
    
    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("📊 **خلاصه نتیجه بهینه‌سازی**")
    summary_lines.append("=" * 60)
    summary_lines.append("")
    
    summary_lines.append(f"💰 **هزینه کل:** {cost_total:,.0f} تومان")
    summary_lines.append(f"⚖️ **تعادل یونی:** {'✅ متعادل' if is_balanced else '⚠️ نامتعادل'}")
    summary_lines.append(f"   کاتیون: {cation:.2f} meq/L | آنیون: {anion:.2f} meq/L")
    summary_lines.append(f"🔄 **تعداد تکرار:** {iterations}")
    summary_lines.append(f"⏱️ **زمان محاسبه:** {convergence_time_ms:.0f} ms")
    summary_lines.append(f"✅ **همگرایی:** {'موفق' if is_converged else 'ناموفق'}")
    summary_lines.append("")
    
    summary_lines.append("📈 **درصد تحقق عناصر هدف:**")
    
    low_achievement = []
    high_achievement = []
    
    for element, pct in achievement.items():
        if pct < 70:
            low_achievement.append(f"{element}: {pct:.0f}%")
        elif pct > 130:
            high_achievement.append(f"{element}: {pct:.0f}%")
        summary_lines.append(f"   - {element}: {pct:.0f}%")
    
    if low_achievement:
        summary_lines.append("")
        summary_lines.append(f"⚠️ **عناصر با تحقق کم:** {', '.join(low_achievement)}")
    
    if high_achievement:
        summary_lines.append("")
        summary_lines.append(f"⚠️ **عناصر با تحقق زیاد:** {', '.join(high_achievement)}")
    
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
    
    summary_lines.append("")
    summary_lines.append("=" * 60)
    
    return "\n".join(summary_lines)


def validate_optimization_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """اعتبارسنجی نتایج بهینه‌سازی"""
    errors = []
    warnings = []
    
    weights = result.get('weights', {})
    if not weights:
        errors.append('وزن‌های بهینه محاسبه نشدند')
    
    concentrations = result.get('concentrations', {})
    if not concentrations:
        errors.append('غلظت‌های نهایی محاسبه نشدند')
    
    cost = result.get('cost_total', 0)
    if cost < 0:
        errors.append('هزینه کل نمی‌تواند منفی باشد')
    
    ion_balance = result.get('ion_balance', {})
    if ion_balance.get('cation', 0) < 0 or ion_balance.get('anion', 0) < 0:
        errors.append('مقادیر کاتیون و آنیون نمی‌توانند منفی باشند')
    
    if not result.get('is_converged', False):
        warnings.append('الگوریتم به جواب کامل نرسید، نتایج ممکن است بهینه نباشند')
    
    weights = result.get('weights', {})
    zero_count = sum(1 for w in weights.values() if w == 0)
    if zero_count > 0:
        warnings.append(f'{zero_count} کود در ترکیب نهایی استفاده نشدند (وزن صفر)')
    
    residual = result.get('residual_error', 0)
    if residual > 100:
        warnings.append(f'خطای باقی‌مانده بالا است ({residual:.2f})')
    
    return {
        'is_valid': len(errors) == 0,
        'has_errors': len(errors) > 0,
        'has_warnings': len(warnings) > 0,
        'errors': errors,
        'warnings': warnings,
        'suggestions': _get_validation_suggestions(errors, warnings)
    }


def _get_validation_suggestions(errors: List[str], warnings: List[str]) -> List[str]:
    """تولید پیشنهادات بر اساس خطاها و هشدارها"""
    suggestions = []
    
    if "وزن‌های بهینه محاسبه نشدند" in errors:
        suggestions.append('کودهای بیشتری انتخاب کنید یا عناصر هدف را تنظیم کنید')
    
    if "غلظت‌های نهایی محاسبه نشدند" in errors:
        suggestions.append('دوباره بهینه‌سازی را اجرا کنید')
    
    if "هزینه کل نمی‌تواند منفی باشد" in errors:
        suggestions.append('قیمت کودها را بررسی کنید')
    
    if "الگوریتم به جواب کامل نرسید" in warnings:
        suggestions.append('تعداد تکرارها را افزایش دهید یا تلرانس را کاهش دهید')
    
    if "وزن صفر" in str(warnings):
        suggestions.append('کودهای بیشتری را برای بهینه‌سازی انتخاب کنید')
    
    if "خطای باقی‌مانده بالا است" in str(warnings):
        suggestions.append('عناصر هدف را با کودهای موجود تطبیق دهید یا کودهای جدید اضافه کنید')
    
    return suggestions


# ============================================================
# 🆕 تابع پردازش نتیجه با قابلیت تعادل یونی خودکار
# ============================================================

def process_optimization_result(
    solver_result: Dict[str, Any],
    A: np.ndarray,
    active_elements: List[str],
    fertilizer_names: List[str],
    fertilizers: List[Dict[str, Any]],
    target_values: Dict[str, float],
    water_values: Dict[str, float],
    costs: np.ndarray,
    options: Dict[str, Any]
) -> Dict[str, Any]:
    """
    پردازش کامل نتیجه بهینه‌سازی با قابلیت تعادل یونی خودکار
    
    Args:
        solver_result: نتیجه حل‌کننده بهینه‌سازی
        A: ماتریس ضرایب
        active_elements: لیست عناصر فعال
        fertilizer_names: لیست اسامی کودها
        fertilizers: لیست کودها
        target_values: مقادیر هدف
        water_values: مقادیر آب
        costs: هزینه هر کود
        options: تنظیمات بهینه‌سازی (شامل auto_balance)
    
    Returns:
        Dict: نتیجه پردازش شده کامل
    """
    weights = solver_result.get('weights', np.zeros(len(fertilizers)))
    weights = np.maximum(weights, 0)
    
    # محاسبه غلظت نهایی
    final_concentrations = calculate_final_concentrations(
        weights, A, water_values, active_elements
    )
    
    # ============================================================
    # 🆕 تعادل یونی خودکار (اگر فعال باشد)
    # ============================================================
    auto_balance = options.get('auto_balance', True)  # پیش‌فرض فعال
    
    if auto_balance:
        # بررسی تعادل فعلی
        cation, anion, is_balanced, _ = calculate_ion_balance(
            final_concentrations, unit="ppm"
        )
        
        if not is_balanced:
            logger.info(f"🔄 تعادل یونی خودکار فعال شد. اختلاف فعلی: {abs(cation - anion):.2f} meq/L")
            
            # اعمال تعادل یونی خودکار
            balance_result = auto_balance_ion(final_concentrations, unit="ppm")
            
            if balance_result['is_balanced']:
                final_concentrations = balance_result['concentrations']
                logger.info(f"✅ تعادل یونی با اضافه کردن {balance_result['added_element']} برقرار شد.")
                
                # اضافه کردن به هشدارها و پیشنهادات
                if 'warnings' not in options:
                    options['warnings'] = []
                if 'suggestions' not in options:
                    options['suggestions'] = []
                
                options['warnings'].append(f"🔧 تعادل یونی خودکار: {balance_result['added_element']} اضافه شد")
                options['suggestions'].append(f"برای برقراری تعادل یونی، {balance_result['added_element']} به ترکیب اضافه شد.")
    
    # محاسبه هزینه کل
    total_cost = np.sum(weights * costs)
    
    # محاسبه تعادل یونی نهایی
    cation, anion, is_balanced, ion_details = calculate_ion_balance(
        final_concentrations, unit="ppm"
    )
    
    # بررسی رسوب
    use_precipitation_check = options.get('use_precipitation_check', True)
    precipitation_result = None
    if use_precipitation_check:
        precipitation_result = check_precipitation(final_concentrations)
    
    # محاسبه درصد تحقق
    achievement = calculate_target_achievement(target_values, final_concentrations)
    
    # ساخت دیکشنری وزن‌ها
    weights_dict = {}
    for i, fert in enumerate(fertilizers):
        fert_id = fert.get('id', f'fert_{i}')
        weights_dict[fert_id] = float(weights[i])
    
    # جمع‌آوری هشدارها و پیشنهادات
    warnings = options.get('warnings', [])
    suggestions = options.get('suggestions', [])
    
    # هشدارهای تعادل یونی
    if not is_balanced:
        diff = abs(cation - anion)
        warnings.append(f'تعادل یونی برقرار نیست (اختلاف: {diff:.2f} meq/L)')
        if cation > anion:
            suggestions.append('برای برقراری تعادل، آنیون‌ها را افزایش دهید')
        else:
            suggestions.append('برای برقراری تعادل، کاتیون‌ها را افزایش دهید')
    
    # هشدارهای رسوب
    if precipitation_result and not precipitation_result.get('is_safe', True):
        for risk in precipitation_result.get('risks', []):
            warnings.append(f'خطر رسوب: {risk["compound"]}')
        suggestions.extend(precipitation_result.get('suggestions', []))
    
    # هشدارهای تحقق عناصر
    for element, pct in achievement.items():
        if pct < 70 and target_values.get(element, 0) > 0:
            warnings.append(f'عنصر {element}: {pct:.0f}% تحقق')
            suggestions.append(f'افزایش {element} با استفاده از کود مناسب')
        elif pct > 130 and target_values.get(element, 0) > 0:
            warnings.append(f'عنصر {element}: {pct:.0f}% تحقق (بیش‌بود)')
            suggestions.append(f'کاهش {element} یا استفاده از کود با درصد کمتر')
    
    # بررسی همگرایی
    if not solver_result.get('is_converged', False):
        warnings.append('الگوریتم به جواب کامل نرسید')
        suggestions.append('تعداد تکرارها را افزایش دهید')
    
    # حذف موارد تکراری
    warnings = list(set(warnings))
    suggestions = list(set(suggestions))
    
    # تولید خلاصه
    summary = generate_optimization_summary(
        weights_dict,
        final_concentrations,
        target_values,
        achievement,
        total_cost,
        (cation, anion, is_balanced),
        warnings,
        suggestions,
        solver_result.get('iterations', 0),
        solver_result.get('convergence_time_ms', 0),
        solver_result.get('is_converged', True)
    )
    
    return {
        'weights': weights_dict,
        'concentrations': final_concentrations,
        'residual_error': float(solver_result.get('residual', 0)),
        'cost_total': float(total_cost),
        'ion_balance': {
            'cation': cation,
            'anion': anion,
            'is_balanced': is_balanced,
            'message': 'تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️',
            'details': ion_details
        },
        'target_achievement': achievement,
        'warnings': warnings,
        'suggestions': suggestions,
        'precipitation': precipitation_result,
        'iterations': solver_result.get('iterations', 0),
        'convergence_time_ms': solver_result.get('convergence_time_ms', 0),
        'is_converged': solver_result.get('is_converged', True),
        'method': solver_result.get('method', 'nnls'),
        'summary': summary,
        'auto_balanced': auto_balance and is_balanced  # نشان‌دهنده اینکه تعادل خودکار انجام شده است
    }