# backend/app/core/ph_adjustment/calculator.py
"""
ماشین‌حساب اصلاح pH (محاسبه دوز اسید/باز)
================================================

🆕 این ماژول جدید، ویژگی «ماشین‌حساب اصلاح pH» را پیاده می‌کند: برخلاف
تخمین pH محلول کودی (که در app.core.ion_balance.calculator.calculate_ph
انجام می‌شود و صرفاً یک شاخص/بازهٔ تقریبی است)، این ماژول از یک عدد
pH واقعی که کاربر با دستگاه pH‑متر اندازه‌گیری کرده استفاده می‌کند و
مقدار دقیق اسید یا باز لازم برای رساندن محلول به pH هدف را، بر اساس
شیمی واقعی تعادل کربنات/بی‌کربنات آب (قلیائیت)، محاسبه می‌کند.

مبنای علمی: سیستم کربنات آب (H2CO3 ⇌ HCO3⁻ ⇌ CO3²⁻) یک بافر اسید-باز
است. برای عبور از pH فعلی به pH هدف (هر دو معمولاً زیر pKa2=10.33، یعنی
عملاً فقط تعادل اول اهمیت دارد: H2CO3 ⇌ HCO3⁻ + H⁺ با pKa1=6.35)، مقدار
اسید/باز لازم برابر است با تغییر در غلظت HCO3⁻ بین دو pH، که با فرمول
هندرسون-هاسلبالخ محاسبه می‌شود. این یک اصل استاندارد و شناخته‌شدهٔ شیمی
تعادلی است (نه یک فرمول تجربی/حدسی).

⚠️ محدودیت‌های صادقانه:
- این محاسبه فرض می‌کند تقریباً کل قلیائیت به‌صورت بی‌کربنات (HCO3⁻) است؛
  این فرض در pH طبیعی آب کشاورزی (۶.۵ تا ۸.۵) دقت خوبی دارد.
- برای اسید فسفریک (H3PO4)، به‌دلیل نزدیکی pKa2 آن (۷.۲) به بازهٔ هدف،
  به‌صورت محافظه‌کارانه فقط تفکیک پروتون اول محاسبه می‌شود (تخمین کمی
  محافظه‌کارانه‌تر، یعنی واقعاً کمی اسید کمتر از مقدار محاسبه‌شده لازم
  خواهد بود - ایمن‌تر از دست کم‌گرفتن مقدار).
- نتیجه یک نقطهٔ شروع دقیق علمی است، نه جایگزین اندازه‌گیری مجدد. طبق
  دستورالعمل ایمنی، همیشه نصف مقدار پیشنهادی اضافه، صبر و دوباره
  اندازه‌گیری شود.
"""

from typing import Dict, Any, Optional
import math

# وزن مولکولی و مشخصات اسیدها/بازهای رایج فرتیگیشن
ACID_BASE_SPECS = {
    'HNO3': {'mw': 63.01, 'protons': 1, 'name': 'اسید نیتریک', 'is_acid': True},
    'H3PO4': {'mw': 97.994, 'protons': 1, 'name': 'اسید فسفریک', 'is_acid': True},  # محافظه‌کارانه: فقط پروتون اول
    'H2SO4': {'mw': 98.079, 'protons': 2, 'name': 'اسید سولفوریک', 'is_acid': True},
    'KOH': {'mw': 56.11, 'protons': 1, 'name': 'پتاس کاستیک (هیدروکسید پتاسیم)', 'is_acid': False},
}

PKA1_CARBONATE = 6.35  # H2CO3 ⇌ HCO3⁻ + H⁺


def _hco3_fraction(ph: float, pka1: float = PKA1_CARBONATE) -> float:
    """کسر (α1) کربنات کل که به‌صورت HCO3⁻ (نه H2CO3) است، در pH داده‌شده."""
    ratio = 10 ** (ph - pka1)
    return ratio / (1 + ratio)


def calculate_ph_adjustment_dose(
    current_ph: float,
    target_ph: float,
    alkalinity_ppm_caco3: float,
    tank_volume_liters: float,
    acid_or_base_type: str = 'HNO3',
    product_concentration_percent: float = 100.0,
    product_price_per_kg: Optional[float] = None
) -> Dict[str, Any]:
    """
    محاسبه دوز اسید یا باز لازم برای رساندن محلول از pH فعلی به pH هدف.

    Args:
        current_ph: pH فعلی که کاربر با دستگاه اندازه‌گیری کرده
        target_ph: pH هدف (معمولاً از تنظیمات رسیپی، مثلاً ۶.۰)
        alkalinity_ppm_caco3: قلیائیت آب بر حسب ppm CaCO3
        tank_volume_liters: حجم مخزن اصلی (لیتر)
        acid_or_base_type: نوع اسید/باز ('HNO3', 'H3PO4', 'H2SO4', 'KOH')
        product_concentration_percent: درصد خلوص/غلظت محصول تجاری (مثلاً ۶۳ برای اسید نیتریک ۶۳٪)
        product_price_per_kg: قیمت هر کیلوگرم محصول (اختیاری، برای نمایش هزینه)

    Returns:
        Dict: شامل جهت (اسید/باز لازم است یا خیر)، مقدار گرم محصول لازم،
            توضیح روش محاسبه و دستورالعمل ایمنی
    """
    spec = ACID_BASE_SPECS.get(acid_or_base_type)
    if not spec:
        return {
            'error': f'نوع اسید/باز «{acid_or_base_type}» پشتیبانی نمی‌شود',
            'supported_types': list(ACID_BASE_SPECS.keys())
        }

    if alkalinity_ppm_caco3 is None or alkalinity_ppm_caco3 < 0:
        alkalinity_ppm_caco3 = 0.0

    # تبدیل قلیائیت به غلظت کل کربنات (تقریباً معادل HCO3⁻ در pH طبیعی آب)
    alkalinity_meq_l = alkalinity_ppm_caco3 / 50.045
    total_carbonate_mol_l = alkalinity_meq_l / 1000.0

    # کسر HCO3⁻ در pH فعلی و pH هدف
    frac_current = _hco3_fraction(current_ph)
    frac_target = _hco3_fraction(target_ph)

    # مثبت = نیاز به اسید (H+) برای کاهش pH؛ منفی = نیاز به باز برای افزایش pH
    net_h_mol_per_l = total_carbonate_mol_l * (frac_current - frac_target)

    # 🆕 اگر قلیائیت صفر/خیلی کم باشد (مثل آب تصفیه‌شده RO)، بافر کربناتی
    # ناچیز است و همان مقدار کوچک اسید محلول را سریع به pH پایین می‌برد؛
    # در این حالت فرمول بالا مقدار خیلی کوچک/نزدیک صفر می‌دهد که واقع‌بینانه
    # است (آب کم‌بافر کمترین مقدار اسید را برای اصلاح لازم دارد).

    needs_acid = net_h_mol_per_l > 0
    total_h_or_oh_mol = abs(net_h_mol_per_l) * tank_volume_liters

    direction_type = acid_or_base_type if needs_acid == spec['is_acid'] else None

    # اگر جهت درخواستی (اسید/باز انتخابی کاربر) با جهت واقعی نیاز همخوانی نداشته باشد
    type_mismatch_warning = None
    if needs_acid and not spec['is_acid']:
        type_mismatch_warning = (
            f'برای رساندن pH از {current_ph:.2f} به {target_ph:.2f} به اسید نیاز است، '
            f'اما «{spec["name"]}» یک باز است. نوع محصول را به یک اسید (HNO3/H3PO4/H2SO4) تغییر دهید.'
        )
    elif not needs_acid and spec['is_acid']:
        type_mismatch_warning = (
            f'برای رساندن pH از {current_ph:.2f} به {target_ph:.2f} به باز نیاز است، '
            f'اما «{spec["name"]}» یک اسید است. نوع محصول را به یک باز (مثلاً KOH) تغییر دهید.'
        )

    moles_pure_product = total_h_or_oh_mol / spec['protons']
    grams_pure = moles_pure_product * spec['mw']
    grams_product = grams_pure / (product_concentration_percent / 100.0) if product_concentration_percent > 0 else grams_pure

    cost = None
    if product_price_per_kg:
        cost = (grams_product / 1000.0) * product_price_per_kg

    ph_diff = abs(current_ph - target_ph)

    return {
        'needs_acid': needs_acid,
        'needs_base': not needs_acid,
        'ph_current': current_ph,
        'ph_target': target_ph,
        'ph_difference': round(ph_diff, 2),
        'alkalinity_ppm_caco3': alkalinity_ppm_caco3,
        'product_type': acid_or_base_type,
        'product_name': spec['name'],
        'grams_needed': round(grams_product, 2) if ph_diff > 0.02 else 0.0,
        'estimated_cost': round(cost, 0) if cost is not None else None,
        'type_mismatch_warning': type_mismatch_warning,
        'method': (
            'محاسبه بر اساس تعادل شیمیایی سیستم بی‌کربنات آب (pKa1=6.35) با استفاده از '
            'قلیائیت اندازه‌گیری‌شده، pH فعلی و pH هدف - نه یک فرمول تجربی حدسی.'
        ),
        'safety_instruction': (
            'این مقدار بر اساس pH اندازه‌گیری‌شدهٔ شما محاسبه شده، اما به‌دلیل واکنش‌های '
            'شیمیایی لحظه‌ای و تفاوت غلظت واقعی محصول، توصیه می‌شود: ابتدا نصف مقدار '
            'پیشنهادی را اضافه کنید، ۵ دقیقه هم بزنید، دوباره با دستگاه اندازه‌گیری کنید و '
            'در صورت نیاز باقیمانده را گام‌به‌گام اضافه کنید.'
        )
    }
