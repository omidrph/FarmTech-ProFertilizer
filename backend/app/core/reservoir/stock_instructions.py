"""
دستورالعمل ساخت استوک برای هر کود
====================================

🆕 این فایل قلب ویژگی درخواستی است: برای هر کود که الگوریتم وزن آن را
(برای کل مخزن اصلی، مثلاً ۵۰۰۰ لیتر) محاسبه کرده، به کشاورز می‌گوید:

    «فلان کود: X گرم را بردار و در Y لیتر آب، در یک سطل جداگانه حل کن،
    سپس داخل مخزن اصلی بریز.»

اصول طراحی:
- هر کود (به‌جز مواردی که در یک مخزن مشترک قابل حل شدن‌اند) یک سطل
  استوک جداگانه می‌گیرد چون هدف اصلی، جلوگیری از تماس مستقیم دو مادهٔ
  ناسازگار (مثلاً کلسیم با فسفات/سولفات) در حالت غلیظ است؛ در غلظت
  پایین (داخل مخزن اصلیِ رقیق) خطر رسوب بسیار کمتر می‌شود.
- حجم آب سطل باید به‌قدری باشد که کود کاملاً حل شود (بر اساس حلالیت
  واقعی هر ترکیب در دمای معمول آب کشاورزی ~20°C) و در عین حال زیادتر
  از حد معقول نباشد (فضای اضافی، وزن جابه‌جایی).
"""

from typing import Dict, List, Any, Optional
import math
import logging

logger = logging.getLogger(__name__)

# ============================================================
# 🆕 حلالیت کودهای رایج در آب (گرم بر لیتر، در دمای ~20°C)
# ============================================================
# منبع: جداول حلالیت استاندارد شیمی معدنی/کشاورزی برای هر ترکیب.
# این مقادیر برای «فرمول شیمیایی» کود است، نه برای نام تجاری؛ تطبیق با
# نام کود در دیتابیس شما از طریق کلیدواژه‌های موجود در نام/دسته انجام
# می‌شود. اگر کودی در این جدول نبود، مقدار پیش‌فرض محافظه‌کارانه
# (200 g/L) استفاده می‌شود تا هشدار کاذب کمتر شود ولی هیچ‌گاه حلالیت
# نامحدود فرض نمی‌شود.
SOLUBILITY_G_PER_L = {
    # نیتراتی‌ها - حلالیت بسیار بالا
    'calcium nitrate': 1200,
    'کلسیم نیترات': 1200,
    'نیترات کلسیم': 1200,
    'potassium nitrate': 316,
    'نیترات پتاسیم': 316,
    'پتاسیم نیترات': 316,
    'ammonium nitrate': 1900,
    'نیترات آمونیوم': 1900,
    'magnesium nitrate': 1250,
    'نیترات منیزیم': 1250,

    # سولفات‌ها
    'potassium sulfate': 111,
    'سولفات پتاسیم': 111,
    'magnesium sulfate': 710,  # (اپسوم/ MgSO4.7H2O)
    'سولفات منیزیم': 710,
    'اپسوم': 710,
    'ammonium sulfate': 754,
    'سولفات آمونیوم': 754,
    'manganese sulfate': 980,
    'سولفات منگنز': 980,
    'zinc sulfate': 965,
    'سولفات روی': 965,
    'copper sulfate': 320,
    'سولفات مس': 320,
    'iron sulfate': 156,
    'سولفات آهن': 156,
    'ferrous sulfate': 156,

    # فسفات‌ها - معمولاً محدودتر
    'monopotassium phosphate': 230,
    'فسفات منو پتاسیم': 230,
    'mkp': 230,
    'map': 282,
    'monoammonium phosphate': 282,
    'فسفات آمونیوم': 282,
    'فسفات منو آمونیوم': 282,

    # کلات‌ها - حلالیت خیلی بالا (کلات EDTA/DTPA)
    'edta': 500,
    'کلات': 500,
    'chelate': 500,

    # اوره
    'urea': 1080,
    'اوره': 1080,

    # اسیدها (مایع - قابل‌حل کامل، محدودیت عملی ندارند)
    'acid': None,
    'اسید': None,
}

# مقدار پیش‌فرض وقتی کود در جدول بالا پیدا نشود
DEFAULT_SOLUBILITY_G_PER_L = 200

# حداقل و حداکثر منطقی حجم سطل استوک (لیتر) برای پیشنهاد خودکار
MIN_BUCKET_LITERS = 1
MAX_BUCKET_LITERS = 200


def _lookup_solubility(fert_name: str, is_acid: bool = False) -> Optional[float]:
    """
    پیدا کردن حلالیت یک کود بر اساس تطبیق کلیدواژه در نام آن.
    خروجی None یعنی محدودیت حلالیت عملی وجود ندارد (مثل اسیدهای مایع).
    """
    if is_acid:
        return None

    name_lower = (fert_name or '').strip().lower()
    for keyword, solubility in SOLUBILITY_G_PER_L.items():
        if keyword in name_lower:
            return solubility

    return DEFAULT_SOLUBILITY_G_PER_L


def calculate_stock_instructions(
    fertilizers: List[Dict[str, Any]],
    weights: Dict[str, float],
    reservoir_data: Dict[str, List[Dict[str, Any]]],
    default_bucket_volume: float = 20.0
) -> List[Dict[str, Any]]:
    """
    🆕 محاسبه دستورالعمل ساخت استوک برای هر کود، به تفکیک.

    برای هر کودی که وزن مثبت دارد:
    1. حجم آب لازم برای حل‌کردن کامل آن وزن، بر اساس حلالیت واقعی محاسبه می‌شود.
    2. اگر حجم لازم از `default_bucket_volume` (سطل پیش‌فرض کاربر) بیشتر
       شود، هشدار داده و حجم واقعی پیشنهادی نمایش داده می‌شود.
    3. مخزن مقصد (A/B/C) بر اساس `reservoir_data` مشخص می‌شود تا کشاورز
       بداند این کود را نباید با کودهای مخزن دیگر در یک سطل مخلوط کند.

    Args:
        fertilizers: لیست کودها (شامل id, name, is_acid)
        weights: وزن واقعی هر کود بر حسب گرم (برای کل مخزن اصلی)
        reservoir_data: خروجی calculate_reservoir_data (برای تعیین مخزن A/B/C هر کود)
        default_bucket_volume: حجم سطل استوک پیش‌فرض/دلخواه کاربر (لیتر)

    Returns:
        List[Dict]: هر آیتم شامل نام کود، وزن، مخزن، حجم آب پیشنهادی سطل،
            غلظت محلول استوک، و هشدار حلالیت (در صورت وجود).
    """
    # نگاشت fertilizer_id -> نام مخزن (A/B/C)
    fert_to_reservoir: Dict[str, str] = {}
    for reservoir_name, items in reservoir_data.items():
        if reservoir_name not in ('A', 'B', 'C'):
            continue
        for item in items:
            fid = item.get('fertilizer_id')
            if fid:
                fert_to_reservoir[str(fid)] = reservoir_name

    instructions = []

    for fert in fertilizers:
        fert_id = str(fert.get('id', ''))
        weight = weights.get(fert_id, 0)
        if not weight or weight <= 0:
            continue

        name = fert.get('name', 'نامشخص')
        is_acid = fert.get('is_acid', False)
        reservoir = fert_to_reservoir.get(fert_id, 'B')

        solubility = _lookup_solubility(name, is_acid)

        warning = None
        if solubility is None:
            # اسید مایع یا ماده بدون محدودیت حلالیت عملی
            recommended_volume = min(default_bucket_volume, max(1.0, weight / 500))
            concentration_g_per_l = weight / recommended_volume if recommended_volume else 0
        else:
            # حداقل حجم آب لازم برای حل کامل (با ۲۰٪ حاشیه اطمینان تا در دمای پایین‌تر هم حل شود)
            min_required_liters = (weight / solubility) * 1.2

            if min_required_liters <= default_bucket_volume:
                recommended_volume = default_bucket_volume
            else:
                # گرد کردن رو به بالا به نزدیک‌ترین عدد قابل‌فهم (مضرب ۵ لیتر)
                recommended_volume = min(
                    MAX_BUCKET_LITERS,
                    max(MIN_BUCKET_LITERS, math.ceil(min_required_liters / 5) * 5)
                )
                warning = (
                    f'⚠️ {name}: وزن {weight:.0f} گرم در سطل {default_bucket_volume:.0f} لیتری '
                    f'به‌طور کامل حل نمی‌شود. حداقل {min_required_liters:.1f} لیتر آب لازم است؛ '
                    f'سطل {recommended_volume:.0f} لیتری پیشنهاد می‌شود (یا وزن را در چند نوبت/سطل تقسیم کنید).'
                )

            concentration_g_per_l = weight / recommended_volume if recommended_volume else 0

        instructions.append({
            'fertilizer_id': fert_id,
            'fertilizer_name': name,
            'weight_grams': round(weight, 2),
            'reservoir': reservoir,
            'is_acid': is_acid,
            'recommended_bucket_liters': round(recommended_volume, 1),
            'stock_concentration_g_per_l': round(concentration_g_per_l, 2),
            'solubility_g_per_l': solubility,
            'warning': warning,
            'instruction_text': (
                f'{name}: {weight:.0f} گرم را در {recommended_volume:.1f} لیتر آب '
                f'(در یک سطل جداگانه) کاملاً حل کنید، سپس محلول را به مخزن اصلی اضافه کنید.'
                if not is_acid else
                f'{name} (اسید): {weight:.0f} گرم/میلی‌لیتر را با احتیاط و به‌آرامی '
                f'در {recommended_volume:.1f} لیتر آب رقیق کنید (همیشه اسید را به آب اضافه '
                f'کنید، نه برعکس)، سپس به مخزن اصلی اضافه کنید.'
            )
        })

    # مرتب‌سازی: ابتدا بر اساس مخزن (A, B, C)، سپس نام
    reservoir_order = {'A': 0, 'B': 1, 'C': 2}
    instructions.sort(key=lambda x: (reservoir_order.get(x['reservoir'], 9), x['fertilizer_name']))

    return instructions
