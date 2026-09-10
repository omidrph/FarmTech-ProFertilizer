"""
بررسی سازگاری شیمیایی در مخازن
===============================

این فایل شامل توابع بررسی سازگاری شیمیایی مواد در مخازن است.
"""

from typing import Dict, List, Any, Optional, Tuple
from .distributor import RESERVOIR_RULES


def check_reservoir_compatibility(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    بررسی سازگاری شیمیایی مواد در هر مخزن
    
    قوانین:
    - مخزن A: نباید حاوی فسفات یا سولفات باشد (رسوب با کلسیم)
    - مخزن B: نباید حاوی کلسیم باشد (با فسفات و سولفات رسوب می‌دهد)
    - مخزن C: فقط اسیدها
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        Dict: شامل وضعیت سازگاری و هشدارها
    """
    warnings = []
    issues = []
    is_compatible = True
    
    # دریافت قوانین
    rules = RESERVOIR_RULES
    
    # بررسی مخزن A
    for item in reservoir_data.get('A', []):
        fert_id = item.get('fertilizer_id')
        fert = next((f for f in fertilizers if str(f.get('id', '')) == fert_id), None)
        if fert:
            elements = fert.get('elements', {})
            # بررسی عناصر ممنوع در مخزن A
            for forbidden in rules['A']['forbidden_elements']:
                if elements.get(forbidden, 0) > 0:
                    is_compatible = False
                    issues.append({
                        'reservoir': 'A',
                        'fertilizer': item['name'],
                        'issue': f'حاوی {forbidden} است که با کلسیم رسوب می‌دهد',
                        'suggestion': f'کود {item["name"]} را به مخزن B منتقل کنید'
                    })
                    warnings.append(f'کود {item["name"]} حاوی {forbidden} است و باید به مخزن B منتقل شود')
    
    # بررسی مخزن B
    for item in reservoir_data.get('B', []):
        fert_id = item.get('fertilizer_id')
        fert = next((f for f in fertilizers if str(f.get('id', '')) == fert_id), None)
        if fert:
            elements = fert.get('elements', {})
            # بررسی وجود کلسیم در مخزن B
            if elements.get('Ca', 0) > 0:
                # این مورد معمولاً نباید اتفاق بیفتد چون کلسیم‌ها به مخزن A می‌روند
                is_compatible = False
                issues.append({
                    'reservoir': 'B',
                    'fertilizer': item['name'],
                    'issue': 'کلسیم در مخزن B قرار دارد',
                    'suggestion': f'کود {item["name"]} را به مخزن A منتقل کنید'
                })
                warnings.append(f'کود {item["name"]} حاوی کلسیم است و باید به مخزن A منتقل شود')
    
    # بررسی مخزن C
    for item in reservoir_data.get('C', []):
        if not item.get('is_acid', False):
            is_compatible = False
            issues.append({
                'reservoir': 'C',
                'fertilizer': item['name'],
                'issue': 'مخزن C فقط برای اسیدها است',
                'suggestion': f'کود {item["name"]} را به مخزن B منتقل کنید'
            })
            warnings.append(f'کود {item["name"]} اسید نیست و نباید در مخزن C باشد')
    
    return {
        'is_compatible': is_compatible,
        'has_issues': len(issues) > 0,
        'has_warnings': len(warnings) > 0,
        'issues': issues,
        'warnings': warnings,
        'suggestions': [issue['suggestion'] for issue in issues]
    }


def get_compatibility_warnings(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> List[str]:
    """
    دریافت هشدارهای سازگاری به صورت لیست ساده
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        List[str]: لیست هشدارها
    """
    result = check_reservoir_compatibility(reservoir_data, fertilizers)
    return result.get('warnings', [])


def get_reservoir_recommendation(
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    fertilizers: List[Dict[str, Any]]
) -> str:
    """
    دریافت توصیه کلی برای بهبود توزیع مخازن
    
    Args:
        reservoir_data: داده‌های توزیع مخازن
        fertilizers: لیست کامل کودها
    
    Returns:
        str: توصیه کلی
    """
    result = check_reservoir_compatibility(reservoir_data, fertilizers)
    
    if result['is_compatible']:
        return "✅ توزیع مخازن از نظر شیمیایی سازگار است"
    
    suggestions = result.get('suggestions', [])
    if suggestions:
        return "⚠️ " + " | ".join(suggestions[:3])
    
    return "⚠️ برخی مشکلات در توزیع مخازن وجود دارد. لطفاً بررسی کنید."


# ============================================================
# 🆕 بانک قوانین تداخل شیمیایی/تغذیه‌ای (فراتر از رسوب کلسیم-فسفات/سولفات)
# ============================================================
# این قوانین مستقل از توزیع مخازن هستند و روی «غلظت نهایی محلول در مخزن
# اصلی» اعمال می‌شوند. هدف: هشدار حرفه‌ای دربارهٔ ترکیب‌ها/غلظت‌هایی که
# از نظر تغذیه گیاهی یا شیمیایی مشکل‌سازند، حتی اگر در مخازن مختلف
# باشند (چون در نهایت همه در یک مخزن اصلی مخلوط می‌شوند).
NUTRIENT_INTERACTION_RULES = [
    {
        'id': 'fe_p_lockout',
        'check': lambda c: (c.get('Fe', 0) > 3 and c.get('P', 0) > 60),
        'message': lambda c: (
            f'⚠️ آهن ({c.get("Fe",0):.1f} ppm) و فسفر ({c.get("P",0):.1f} ppm) '
            f'هر دو بالا هستند. آهن غیرکلاته با فسفات رسوب می‌دهد و کمبود آهن '
            f'ایجاد می‌کند. از آهن کلاته (Fe-EDTA/DTPA) استفاده کنید و زمان تزریق '
            f'را از فسفر جدا کنید.'
        )
    },
    {
        'id': 'high_ph_micronutrient_lockout',
        'check': lambda c, ph=None: (ph is not None and ph > 7.0 and (
            c.get('Fe', 0) > 0 or c.get('Mn', 0) > 0 or c.get('Zn', 0) > 0 or c.get('Cu', 0) > 0
        )),
        'message': lambda c, ph=None: (
            f'⚠️ pH تخمینی بالا ({ph:.1f}) باعث کاهش شدید جذب ریزمغذی‌ها '
            f'(آهن، منگنز، روی، مس) می‌شود، حتی اگر غلظت آن‌ها کافی باشد. '
            f'pH را با اسید کاهش دهید یا از فرم کلاته مقاوم به pH بالا (مثل Fe-DTPA) استفاده کنید.'
        )
    },
    {
        'id': 'excess_chloride',
        'check': lambda c: c.get('Cl', 0) > 150,
        'message': lambda c: (
            f'⚠️ کلر ({c.get("Cl",0):.0f} ppm) از حد معمول (۱۵۰ ppm) بیشتر است. '
            f'برای گیاهان حساس به کلر (مثل توت‌فرنگی، برخی سبزیجات برگی) خطر سمیت وجود دارد.'
        )
    },
    {
        'id': 'excess_sodium',
        'check': lambda c: c.get('Na', 0) > 50,
        'message': lambda c: (
            f'⚠️ سدیم ({c.get("Na",0):.0f} ppm) از حد معمول (۵۰ ppm) بیشتر است. '
            f'سدیم اضافی جذب کلسیم و پتاسیم را مختل می‌کند و در آب/خاک تجمع می‌یابد.'
        )
    },
    {
        'id': 'boron_toxicity',
        'check': lambda c: c.get('B', 0) > 1.0,
        'message': lambda c: (
            f'⚠️ بور ({c.get("B",0):.2f} ppm) به محدوده سمیت نزدیک یا وارد شده است '
            f'(دامنه بین کمبود و سمیت بور بسیار باریک است). دقت در دوزاژ ضروری است.'
        )
    },
    {
        'id': 'excess_ammonium',
        'check': lambda c: c.get('N-NH4', 0) > 0 and (c.get('N-NH4', 0) / max(c.get('N-NO3', 0) + c.get('N-NH4', 0), 1)) > 0.30,
        'message': lambda c: (
            f'⚠️ سهم نیتروژن آمونیومی از کل نیتروژن بیش از ۳۰٪ است. '
            f'خطر مسمومیت آمونیومی (سوختگی ریشه، رشد رویشی بیش‌ازحد) به‌خصوص در دمای پایین ریشه.'
        )
    },
    {
        'id': 'low_calcium_high_potassium',
        'check': lambda c: c.get('K', 0) > 0 and c.get('Ca', 0) > 0 and (c.get('K', 0) / c.get('Ca', 0)) > 3.0,
        'message': lambda c: (
            f'⚠️ نسبت پتاسیم به کلسیم (K/Ca) بالا است ({c.get("K",0)/max(c.get("Ca",0),0.01):.1f}). '
            f'پتاسیم زیاد می‌تواند جذب کلسیم را محدود کند و خطر پوسیدگی گلگاه (Blossom End Rot) '
            f'در گوجه/فلفل و ترک میوه را افزایش دهد.'
        )
    },
]


def check_nutrient_interactions(
    concentrations: Dict[str, float],
    ph_estimate: Optional[float] = None
) -> List[str]:
    """
    🆕 بررسی تداخلات تغذیه‌ای/شیمیایی بر اساس غلظت نهایی محلول (مخزن اصلی).

    این فراتر از بررسی رسوب Ksp (که در check_precipitation انجام
    می‌شود) است؛ اینجا تداخلات «تغذیه‌ای» (قفل‌شدن جذب عناصر، سمیت،
    عدم تعادل نسبت عناصر) که هنوز به‌صورت رسوب فیزیکی ظاهر نشده‌اند هم
    پوشش داده می‌شوند.

    Args:
        concentrations: غلظت نهایی عناصر در مخزن اصلی (ppm)
        ph_estimate: pH تخمینی محلول (برای قوانین وابسته به pH)

    Returns:
        List[str]: پیام‌های هشدار (خالی اگر مشکلی نباشد)
    """
    warnings = []
    for rule in NUTRIENT_INTERACTION_RULES:
        try:
            if rule['id'] == 'high_ph_micronutrient_lockout':
                triggered = rule['check'](concentrations, ph_estimate)
            else:
                triggered = rule['check'](concentrations)

            if triggered:
                if rule['id'] == 'high_ph_micronutrient_lockout':
                    warnings.append(rule['message'](concentrations, ph_estimate))
                else:
                    warnings.append(rule['message'](concentrations))
        except Exception:
            # یک قانون خراب نباید کل بررسی را متوقف کند
            continue

    return warnings


def check_manual_fertilizer_selection(
    fertilizers: List[Dict[str, Any]]
) -> List[str]:
    """
    🆕 هشدار زمانی که کاربر خودش (نه الگوریتم) مجموعه‌ای از کودها را
    دستی انتخاب کرده که از نظر شیمیایی با هم مشکل دارند — پیش از حتی
    اجرای بهینه‌سازی. این جدا از بررسی مخازن است چون آن‌جا فرض بر این
    است که سیستم خودش کودها را در مخازن جدا می‌ریزد؛ اینجا هدف این است
    که به کاربر در همان مرحلهٔ انتخاب کود، پیش از دیدن نتیجه، آگاهی بدهیم.

    Args:
        fertilizers: لیست کودهای انتخاب‌شده توسط کاربر (شامل name, elements, is_acid)

    Returns:
        List[str]: هشدارهای مربوط به ترکیب انتخابی کاربر
    """
    warnings = []

    has_calcium_source = any(f.get('elements', {}).get('Ca', 0) > 0 for f in fertilizers)
    has_sulfate_source = any(f.get('elements', {}).get('S', 0) > 0 for f in fertilizers)
    has_phosphate_source = any(f.get('elements', {}).get('P', 0) > 0 for f in fertilizers)

    if has_calcium_source and has_sulfate_source:
        warnings.append(
            '⚠️ در میان کودهای انتخابی شما، هم منبع کلسیم و هم منبع سولفات وجود دارد. '
            'این دو در غلظت بالا و تماس مستقیم (حالت غلیظ در سطل استوک) رسوب سولفات کلسیم '
            'می‌دهند. سیستم به‌طور خودکار آن‌ها را در سطل‌های جداگانه قرار می‌دهد، اما '
            'هرگز این دو گروه کود را مستقیماً با هم در یک سطل حل نکنید.'
        )
    if has_calcium_source and has_phosphate_source:
        warnings.append(
            '⚠️ در میان کودهای انتخابی شما، هم منبع کلسیم و هم منبع فسفات وجود دارد. '
            'این دو در حالت غلیظ رسوب فسفات کلسیم می‌دهند. سیستم آن‌ها را در سطل‌های '
            'جداگانه قرار می‌دهد؛ هرگز این دو گروه را مستقیماً با هم مخلوط نکنید.'
        )

    acid_count = sum(1 for f in fertilizers if f.get('is_acid', False))
    if acid_count > 1:
        warnings.append(
            f'⚠️ شما {acid_count} نوع اسید مختلف انتخاب کرده‌اید. مخلوط‌کردن مستقیم اسیدهای '
            f'مختلف (بدون رقیق‌سازی جداگانه) می‌تواند واکنش گرمازا و خطرناک ایجاد کند. '
            f'هر اسید را جداگانه و با احتیاط در آب رقیق کنید.'
        )

    return warnings


