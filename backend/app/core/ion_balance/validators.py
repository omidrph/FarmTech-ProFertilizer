"""
اعتبارسنجی نتایج تعادل یونی
================================

این فایل شامل توابع اعتبارسنجی و بررسی نتایج محاسبات است:
- اعتبارسنجی نتایج تعادل یونی
- بررسی رسوب احتمالی
- تولید هشدارها و پیشنهادات
"""

from typing import Dict, List, Any, Optional
from .constants import (
    BALANCE_TOLERANCE,
    KSP_VALUES,
    MOLECULAR_WEIGHTS,
    ALL_ELEMENTS
)


def validate_ion_balance_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    اعتبارسنجی نتایج تعادل یونی
    
    این تابع نتایج محاسبه تعادل یونی را بررسی می‌کند و خطاها و هشدارهای احتمالی را شناسایی می‌کند.
    
    Args:
        result: دیکشنری نتیجه محاسبه تعادل یونی (خروجی calculate_ion_balance)
    
    Returns:
        Dict: شامل وضعیت اعتبار، خطاها و هشدارها
    
    مثال:
        >>> result = {'cation': 16.23, 'anion': 4.52, 'is_balanced': False}
        >>> validation = validate_ion_balance_result(result)
        >>> print(validation['warnings'])
        ['تعادل یونی برقرار نیست (اختلاف: 11.71 meq/L)']
    """
    errors = []
    warnings = []
    suggestions = []
    
    # استخراج مقادیر
    cation = result.get('total_cation_meq', 0)
    anion = result.get('total_anion_meq', 0)
    is_balanced = result.get('is_balanced', False)
    difference = abs(cation - anion)
    
    # بررسی ۱: وجود کاتیون و آنیون
    if cation == 0 and anion == 0:
        warnings.append('هیچ کاتیون یا آنیونی در محاسبات وجود ندارد')
        suggestions.append('لطفاً حداقل یک کاتیون و یک آنیون به عناصر هدف اضافه کنید')
    
    if cation > 0 and anion == 0:
        warnings.append('فقط کاتیون وجود دارد، آنیون صفر است')
        suggestions.append('لطفاً آنیون‌ها (نیترات، فسفات، سولفات) را به عناصر هدف اضافه کنید')
    
    if anion > 0 and cation == 0:
        warnings.append('فقط آنیون وجود دارد، کاتیون صفر است')
        suggestions.append('لطفاً کاتیون‌ها (پتاسیم، کلسیم، منیزیم) را به عناصر هدف اضافه کنید')
    
    # بررسی ۲: تعادل یونی
    if not is_balanced:
        warnings.append(f'تعادل یونی برقرار نیست (اختلاف: {difference:.2f} meq/L)')
        
        if difference > BALANCE_TOLERANCE * 2:
            suggestions.append('اختلاف قابل توجه است. لطفاً عناصر را تنظیم کنید تا تعادل برقرار شود.')
        else:
            suggestions.append('اختلاف جزئی است. با تنظیم اندک عناصر می‌توان تعادل را برقرار کرد.')
        
        # پیشنهاد دقیق‌تر
        if cation > anion:
            suggestions.append(f'کاتیون‌ها ({cation:.2f}) بیشتر از آنیون‌ها ({anion:.2f}) هستند. آنیون‌ها را افزایش دهید.')
        else:
            suggestions.append(f'آنیون‌ها ({anion:.2f}) بیشتر از کاتیون‌ها ({cation:.2f}) هستند. کاتیون‌ها را افزایش دهید.')
    
    # بررسی ۳: عناصر با مقدار صفر
    zero_elements = result.get('zero_elements', [])
    if zero_elements:
        warnings.append(f'{len(zero_elements)} عنصر با مقدار صفر: {", ".join(zero_elements[:5])}')
        if len(zero_elements) > 5:
            warnings[-1] += f' و {len(zero_elements) - 5} عنصر دیگر'
    
    # بررسی ۴: عناصر از دست رفته
    missing_elements = result.get('missing_elements', [])
    if missing_elements:
        warnings.append(f'{len(missing_elements)} عنصر در داده‌ها وجود ندارد')
    
    return {
        'is_valid': len(errors) == 0,
        'has_errors': len(errors) > 0,
        'has_warnings': len(warnings) > 0,
        'errors': errors,
        'warnings': warnings,
        'suggestions': suggestions
    }


def check_precipitation(concentrations: Dict[str, float]) -> Dict[str, Any]:
    """
    بررسی رسوب احتمالی در ترکیب عناصر با استفاده از ثابت‌های حلالیت (Ksp)
    
    این تابع با استفاده از ثابت‌های حلالیت، احتمال تشکیل رسوب در محلول را بررسی می‌کند.
    رسوب‌های رایج شامل CaSO4، Ca3(PO4)2، Fe(OH)3 و ... هستند.
    
    Args:
        concentrations: دیکشنری غلظت عناصر به صورت {نام_عنصر: مقدار_ppm}
    
    Returns:
        Dict: شامل وضعیت ایمنی، خطرات و پیشنهادات
    
    مثال:
        >>> conc = {'Ca': 200, 'S': 150, 'P': 50, 'Fe': 5}
        >>> result = check_precipitation(conc)
        >>> print(result['is_safe'])
        False
        >>> print(result['risks'][0]['compound'])
        'CaSO4'
    """
    risks = []
    suggestions = []
    is_safe = True
    
    # تبدیل ppm به mol/L
    def ppm_to_mol(ppm: float, element: str) -> float:
        mw = MOLECULAR_WEIGHTS.get(element, 0)
        if mw == 0:
            return 0
        return ppm / (mw * 1000)
    
    # استخراج غلظت‌ها
    ca = ppm_to_mol(concentrations.get('Ca', 0), 'Ca')
    so4 = ppm_to_mol(concentrations.get('S', 0), 'S')
    po4 = ppm_to_mol(concentrations.get('P', 0), 'P')
    mg = ppm_to_mol(concentrations.get('Mg', 0), 'Mg')
    fe = ppm_to_mol(concentrations.get('Fe', 0), 'Fe')
    
    # ============================================================
    # بررسی CaSO4 (کلسیم سولفات)
    # ============================================================
    if ca > 0 and so4 > 0:
        ion_product = ca * so4
        if ion_product > KSP_VALUES['CaSO4']:
            is_safe = False
            risks.append({
                'compound': 'CaSO4',
                'name': 'کلسیم سولفات (گچ)',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['CaSO4'],
                'is_risky': True,
                'severity': 'high' if ion_product > KSP_VALUES['CaSO4'] * 10 else 'medium',
                'suggestion': 'کلسیم و سولفات را در مخازن جداگانه قرار دهید (مخزن A و B)',
                'formula': 'Ca²⁺ + SO₄²⁻ → CaSO₄↓'
            })
            suggestions.append('کلسیم و سولفات را در مخازن جداگانه قرار دهید')
    
    # ============================================================
    # بررسی Ca3(PO4)2 (کلسیم فسفات)
    # ============================================================
    if ca > 0 and po4 > 0:
        ion_product = (ca ** 3) * (po4 ** 2)
        if ion_product > KSP_VALUES['Ca3(PO4)2']:
            is_safe = False
            risks.append({
                'compound': 'Ca3(PO4)2',
                'name': 'کلسیم فسفات',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Ca3(PO4)2'],
                'is_risky': True,
                'severity': 'critical' if ion_product > KSP_VALUES['Ca3(PO4)2'] * 100 else 'high',
                'suggestion': 'کلسیم و فسفات را در مخازن جداگانه قرار دهید (مخزن A و B)',
                'formula': '3Ca²⁺ + 2PO₄³⁻ → Ca₃(PO₄)₂↓'
            })
            suggestions.append('کلسیم و فسفات را در مخازن جداگانه قرار دهید')
    
    # ============================================================
    # بررسی Mg(OH)2 (منیزیم هیدروکسید)
    # ============================================================
    if mg > 0:
        oh = 1e-7
        ion_product = mg * (oh ** 2)
        if ion_product > KSP_VALUES['Mg(OH)2']:
            is_safe = False
            risks.append({
                'compound': 'Mg(OH)2',
                'name': 'منیزیم هیدروکسید',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Mg(OH)2'],
                'is_risky': True,
                'severity': 'medium',
                'suggestion': 'pH را کاهش دهید یا منیزیم را با کلات استفاده کنید',
                'formula': 'Mg²⁺ + 2OH⁻ → Mg(OH)₂↓'
            })
            suggestions.append('pH را کاهش دهید یا منیزیم را با کلات استفاده کنید')
    
    # ============================================================
    # بررسی Fe(OH)3 (آهن هیدروکسید)
    # ============================================================
    if fe > 0:
        oh = 1e-7
        ion_product = fe * (oh ** 3)
        if ion_product > KSP_VALUES['Fe(OH)3']:
            is_safe = False
            risks.append({
                'compound': 'Fe(OH)3',
                'name': 'آهن هیدروکسید',
                'ion_product': ion_product,
                'ksp': KSP_VALUES['Fe(OH)3'],
                'is_risky': True,
                'severity': 'high' if ion_product > KSP_VALUES['Fe(OH)3'] * 100 else 'medium',
                'suggestion': 'از آهن کلاته استفاده کنید (Fe-EDTA یا Fe-EDDHA)',
                'formula': 'Fe³⁺ + 3OH⁻ → Fe(OH)₃↓'
            })
            suggestions.append('از آهن کلاته استفاده کنید')
    
    if is_safe:
        summary = 'محلول از نظر رسوب ایمن است'
    else:
        summary = f'{len(risks)} خطر رسوب شناسایی شده است'
    
    return {
        'is_safe': is_safe,
        'summary': summary,
        'risks': risks,
        'suggestions': list(set(suggestions)),
        'risk_count': len(risks),
        'has_risks': len(risks) > 0
    }


def generate_optimization_warnings(
    ion_balance_result: Dict[str, Any],
    precipitation_result: Dict[str, Any],
    achievement: Dict[str, float]
) -> List[str]:
    """
    تولید هشدارهای جامع بر اساس نتایج مختلف
    
    Args:
        ion_balance_result: نتیجه تعادل یونی
        precipitation_result: نتیجه بررسی رسوب
        achievement: درصد تحقق عناصر هدف
    
    Returns:
        List[str]: لیست هشدارها
    """
    warnings = []
    
    # هشدارهای تعادل یونی
    if not ion_balance_result.get('is_balanced', False):
        cation = ion_balance_result.get('total_cation_meq', 0)
        anion = ion_balance_result.get('total_anion_meq', 0)
        difference = abs(cation - anion)
        warnings.append(f'تعادل یونی برقرار نیست (اختلاف: {difference:.2f} meq/L)')
    
    # هشدارهای رسوب
    if not precipitation_result.get('is_safe', True):
        risk_count = precipitation_result.get('risk_count', 0)
        warnings.append(f'{risk_count} خطر رسوب شناسایی شده است')
        for risk in precipitation_result.get('risks', []):
            warnings.append(f'رسوب {risk["name"]} ممکن است تشکیل شود')
    
    # هشدارهای تحقق عناصر
    for element, pct in achievement.items():
        if pct < 70:
            warnings.append(f'عنصر {element}: تنها {pct:.0f}% از هدف تامین شده است')
        elif pct > 130:
            warnings.append(f'عنصر {element}: {pct:.0f}% از هدف تامین شده است (بیش‌بود)')
    
    return warnings


def generate_optimization_suggestions(
    ion_balance_result: Dict[str, Any],
    precipitation_result: Dict[str, Any],
    achievement: Dict[str, float]
) -> List[str]:
    """
    تولید پیشنهادات بر اساس نتایج مختلف
    
    Args:
        ion_balance_result: نتیجه تعادل یونی
        precipitation_result: نتیجه بررسی رسوب
        achievement: درصد تحقق عناصر هدف
    
    Returns:
        List[str]: لیست پیشنهادات
    """
    suggestions = []
    
    # پیشنهادات تعادل یونی
    if not ion_balance_result.get('is_balanced', False):
        cation = ion_balance_result.get('total_cation_meq', 0)
        anion = ion_balance_result.get('total_anion_meq', 0)
        
        if cation > anion:
            suggestions.append('برای برقراری تعادل، آنیون‌ها (نیترات، فسفات، سولفات) را افزایش دهید')
        else:
            suggestions.append('برای برقراری تعادل، کاتیون‌ها (پتاسیم، کلسیم، منیزیم) را افزایش دهید')
    
    # پیشنهادات رسوب
    for risk in precipitation_result.get('risks', []):
        suggestions.append(risk['suggestion'])
    
    # پیشنهادات تحقق عناصر
    for element, pct in achievement.items():
        if pct < 70:
            suggestions.append(f'عنصر {element} را با استفاده از کود مناسب افزایش دهید')
        elif pct > 130:
            suggestions.append(f'عنصر {element} را کاهش دهید یا از کود با درصد کمتر استفاده کنید')
    
    return list(set(suggestions))