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


def _phosphate_speciation_fraction(ph: float) -> float:
    """
    🆕 محاسبه کسر واقعی PO4³⁻ آزاد از کل فسفر محلول، بر اساس pH.

    چرا لازم است: نسخه قبلی کل غلظت فسفر (P) را معادل غلظت یون PO4³⁻
    در نظر می‌گرفت و آن را مستقیماً در Ksp کلسیم‌فسفات (که برای یون
    PO4³⁻ تعریف شده) قرار می‌داد. این یک خطای شیمیایی مهم است: در pH
    معمول محلول‌های غذایی (۵.۵ تا ۶.۵)، فسفر تقریباً به‌طور کامل به‌صورت
    H2PO4⁻ است و کسر واقعی PO4³⁻ ناچیز (در حد ۱۰⁻⁶ تا ۱۰⁻⁹) است. در
    نتیجه، نسخه قبلی تقریباً همیشه هشدار کاذب «رسوب فسفات کلسیم» تولید
    می‌کرد، حتی در غلظت‌های کاملاً معمول و ایمن.

    محاسبه بر اساس تعادل سه‌مرحله‌ای اسید فسفریک:
        H3PO4 ⇌ H2PO4⁻ ⇌ HPO4²⁻ ⇌ PO4³⁻
        pKa1 = 2.15, pKa2 = 7.20, pKa3 = 12.35 (مقادیر استاندارد شیمی)

    Args:
        ph: pH محلول

    Returns:
        float: کسر (بین ۰ و ۱) از کل فسفر که به‌صورت PO4³⁻ آزاد است
    """
    h = 10 ** (-ph)
    ka1, ka2, ka3 = 10 ** -2.15, 10 ** -7.20, 10 ** -12.35

    d = (h ** 3) + (ka1 * h ** 2) + (ka1 * ka2 * h) + (ka1 * ka2 * ka3)
    if d <= 0:
        return 0.0
    alpha3 = (ka1 * ka2 * ka3) / d
    return alpha3


def _carbonate_fraction_from_alkalinity(alkalinity_ppm_caco3: float, ph: float) -> float:
    """
    🆕 تخمین غلظت واقعی [CO3²⁻] (مول بر لیتر) از روی قلیائیت آب (ppm CaCO3) و pH.

    قلیائیت آب معمولاً تقریباً معادل غلظت بی‌کربنات [HCO3⁻] است (در pH
    طبیعی آب‌های کشاورزی، معمولاً کمتر از ۱٪ آن به‌صورت کربنات CO3²⁻
    است). با استفاده از تعادل دوم اسید کربنیک:

        HCO3⁻ ⇌ CO3²⁻ + H⁺   (pKa2 = 10.33)

    می‌توان کسر واقعی CO3²⁻ را از روی pH محلول محاسبه کرد.

    Args:
        alkalinity_ppm_caco3: قلیائیت بر حسب ppm معادل CaCO3
        ph: pH محلول

    Returns:
        float: غلظت [CO3²⁻] بر حسب mol/L
    """
    if not alkalinity_ppm_caco3 or alkalinity_ppm_caco3 <= 0:
        return 0.0

    # تبدیل قلیائیت (ppm as CaCO3) به meq/L: وزن هم‌ارز CaCO3 = 100.09/2 = 50.045
    alkalinity_meq_l = alkalinity_ppm_caco3 / 50.045
    # در pH طبیعی (زیر ۸.۳)، تقریباً کل قلیائیت به‌صورت HCO3⁻ (تک‌ظرفیتی) است
    hco3_mol_l = alkalinity_meq_l / 1000.0

    pka2 = 10.33
    co3_to_hco3_ratio = 10 ** (ph - pka2)
    co3_mol_l = hco3_mol_l * co3_to_hco3_ratio

    return co3_mol_l


def check_precipitation(
    concentrations: Dict[str, float],
    ph: Optional[float] = None,
    has_chelated_iron: bool = False,
    alkalinity_ppm_caco3: Optional[float] = None
) -> Dict[str, Any]:
    """
    بررسی رسوب احتمالی در ترکیب عناصر با استفاده از ثابت‌های حلالیت (Ksp)
    
    این تابع با استفاده از ثابت‌های حلالیت، احتمال تشکیل رسوب در محلول را بررسی می‌کند.
    رسوب‌های رایج شامل CaSO4، Ca3(PO4)2، Fe(OH)3 و ... هستند.

    🆕 رفع دو باگ علمی مهم:
    ۱) پیش‌تر [OH⁻] همیشه ثابت و معادل pH=7 فرض می‌شد؛ اکنون از pH واقعی
       (تخمینی محلول یا آب ورودی) استفاده می‌شود که برای رسوب هیدروکسیدها
       (Mg(OH)2 و به‌خصوص Fe(OH)3 با توان ۳) بسیار حساس است.
    ۲) پیش‌تر کل غلظت فسفر معادل [PO4³⁻] آزاد در نظر گرفته می‌شد؛ اکنون
       با معادلات تفکیک اسید فسفریک (pKa1/2/3)، فقط کسر واقعی PO4³⁻ در
       pH محلول محاسبه و استفاده می‌شود (رفع هشدار کاذب رسوب فسفات کلسیم).

    Args:
        concentrations: دیکشنری غلظت عناصر به صورت {نام_عنصر: مقدار_ppm}
        ph: pH محلول (اگر داده نشود، فرض محافظه‌کارانه ۶.۰ - معمول محلول
            غذایی - استفاده می‌شود، نه ۷.۰ خنثی)
        has_chelated_iron: 🆕 اگر True باشد، یعنی منبع آهن استفاده‌شده
            کلاته (Fe-EDTA/DTPA/EDDHA) است. تقریباً همه کودهای تجاری آهن
            کلاته هستند، دقیقاً به همین دلیل که آهن آزاد (غیرکلاته) طبق
            Ksp در تقریباً هر pH عملی رسوب می‌کند (Ksp این ترکیب به‌قدری
            کوچک است که حتی در pH اسیدی هم آستانه رد می‌شود). اگر این
            پارامتر True باشد، هشدار Fe(OH)3 نمایش داده نمی‌شود چون آهن
            کلاته در برابر این نوع رسوب مقاوم است (هدف اصلی کلات‌سازی).
        alkalinity_ppm_caco3: 🆕 قلیائیت آب منبع بر حسب ppm CaCO3 (فیلد
            جدید فرم آب). اگر داده شود، بررسی رسوب کربنات کلسیم (CaCO3)
            هم انجام می‌شود؛ در غیر این صورت (مثل قبل) این بررسی رد
            می‌شود چون بدون این عدد امکان محاسبهٔ درست وجود ندارد.
    
    Returns:
        Dict: شامل وضعیت ایمنی، خطرات و پیشنهادات
    
    مثال:
        >>> conc = {'Ca': 200, 'S': 150, 'P': 50, 'Fe': 5}
        >>> result = check_precipitation(conc, ph=6.0)
        >>> print(result['is_safe'])
        False
        >>> print(result['risks'][0]['compound'])
        'CaSO4'
    """
    risks = []
    suggestions = []
    is_safe = True

    if ph is None:
        ph = 6.0  # فرض محافظه‌کارانه: pH معمول محلول غذایی هیدروپونیک

    # تبدیل ppm به mol/L
    def ppm_to_mol(ppm: float, element: str) -> float:
        mw = MOLECULAR_WEIGHTS.get(element, 0)
        if mw == 0:
            return 0
        return ppm / (mw * 1000)
    
    # استخراج غلظت‌ها
    ca = ppm_to_mol(concentrations.get('Ca', 0), 'Ca')
    so4 = ppm_to_mol(concentrations.get('S', 0), 'S')
    p_total = ppm_to_mol(concentrations.get('P', 0), 'P')
    mg = ppm_to_mol(concentrations.get('Mg', 0), 'Mg')
    fe = ppm_to_mol(concentrations.get('Fe', 0), 'Fe')

    # 🆕 [OH-] واقعی بر اساس pH (نه فرض ثابت pH=7)
    oh = 10 ** (ph - 14)

    # 🆕 کسر واقعی PO4³⁻ آزاد از کل فسفر، بر اساس pH محلول
    po4_fraction = _phosphate_speciation_fraction(ph)
    po4 = p_total * po4_fraction
    
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
    # بررسی Ca3(PO4)2 (کلسیم فسفات) - 🆕 با کسر واقعی PO4³⁻ بر اساس pH
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
                'formula': '3Ca²⁺ + 2PO₄³⁻ → Ca₃(PO₄)₂↓',
                'note': f'در pH {ph:.1f}، فقط {po4_fraction*100:.4f}٪ از فسفر کل به‌صورت PO4³⁻ آزاد است'
            })
            suggestions.append('کلسیم و فسفات را در مخازن جداگانه قرار دهید')
    
    # ============================================================
    # بررسی Mg(OH)2 (منیزیم هیدروکسید) - 🆕 با [OH-] واقعی بر اساس pH
    # ============================================================
    if mg > 0:
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
    # بررسی Fe(OH)3 (آهن هیدروکسید) - 🆕 با [OH-] واقعی بر اساس pH
    # ============================================================
    # 🆕 اگر آهن کلاته باشد، این بررسی رد می‌شود چون کلات‌سازی دقیقاً
    # برای جلوگیری از این نوع رسوب طراحی شده و Ksp آهن آزاد در این‌جا
    # معنایی برای آهن کلاته ندارد.
    if fe > 0 and not has_chelated_iron:
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
                'formula': 'Fe³⁺ + 3OH⁻ → Fe(OH)₃↓',
                'note': 'آهن غیرکلاته در تقریباً هر pH عملی مستعد رسوب است؛ استفاده از فرم کلاته این خطر را برطرف می‌کند.'
            })
            suggestions.append('از آهن کلاته استفاده کنید')

    # ============================================================
    # 🆕 بررسی CaCO3 (کلسیم کربنات) - فقط اگر قلیائیت آب داده شده باشد
    # ============================================================
    if ca > 0 and alkalinity_ppm_caco3 and alkalinity_ppm_caco3 > 0:
        co3 = _carbonate_fraction_from_alkalinity(alkalinity_ppm_caco3, ph)
        if co3 > 0:
            ion_product = ca * co3
            if ion_product > KSP_VALUES['CaCO3']:
                is_safe = False
                risks.append({
                    'compound': 'CaCO3',
                    'name': 'کلسیم کربنات (رسوب آهک)',
                    'ion_product': ion_product,
                    'ksp': KSP_VALUES['CaCO3'],
                    'is_risky': True,
                    'severity': 'high' if ion_product > KSP_VALUES['CaCO3'] * 10 else 'medium',
                    'suggestion': 'قلیائیت آب بالاست؛ با اسیدی‌سازی pH آب پیش از اختلاط کود، یا استفاده از سیستم تصفیه (RO)، این ریسک کاهش می‌یابد',
                    'formula': 'Ca²⁺ + CO₃²⁻ → CaCO₃↓',
                    'note': f'بر اساس قلیائیت {alkalinity_ppm_caco3:.0f} ppm CaCO3 و pH {ph:.1f}'
                })
                suggestions.append('قلیائیت آب بالاست؛ اسیدی‌سازی پیش از اختلاط کود توصیه می‌شود')
    
    if is_safe:
        summary = 'محلول از نظر رسوب ایمن است'
    else:
        summary = f'{len(risks)} خطر رسوب شناسایی شده است'

    limitations = []
    if not alkalinity_ppm_caco3:
        limitations.append(
            'بررسی رسوب کلسیم کربنات (CaCO3) انجام نشد چون قلیائیت آب وارد نشده است. '
            'برای فعال‌شدن این بررسی، فیلد «قلیائیت» را در بخش آنالیز آب پر کنید.'
        )

    return {
        'is_safe': is_safe,
        'summary': summary,
        'risks': risks,
        'suggestions': list(set(suggestions)),
        'risk_count': len(risks),
        'has_risks': len(risks) > 0,
        'ph_used': ph,
        'limitations': limitations
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


