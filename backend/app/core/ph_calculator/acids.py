# backend/app/core/ph_calculator/acids.py
"""
ثابت‌های شیمیایی اسید/باز برای ماشین‌حساب pH
============================================================
این ماژول جایگزین لیست ثابت و هاردکدِ قبلی (widgets/ph/phDose.ts ->
CHEMICALS) می‌شود. تفاوت مهم:

  نسخه‌ی قبلی: یک لیست بسته و مجزا از پایگاه‌داده‌ی کود که هیچ ربطی
  به اسیدهای واقعیِ ثبت‌شده‌ی کاربر (مخزن C / is_acid=True) نداشت -
  همان چیزی که باعث پیشنهاد نادرست اسید می‌شد.

  نسخه‌ی جدید: کاربر از بین اسیدهای *واقعی* ثبت‌شده در پایگاه‌داده‌ی
  خودش (routes/ph_calculator.py -> GET /ph-calculator/acids) یک مورد
  را انتخاب می‌کند. مقدار «خلوص» مستقیماً از فیلد concentration همان
  کود خوانده می‌شود. آنچه در پایگاه‌داده‌ی کود ذخیره نشده (چگالی محلول
  تجاری) از این جدول مرجع resolve می‌شود و کاربر می‌تواند آن را در
  همان صفحه‌ی ماشین‌حساب pH (بدون دست‌کاری صفحه‌ی پایگاه‌داده‌ی کود)
  به مقدار دقیق برگه‌ی مشخصات (SDS) محصول خودش ویرایش کند.

⚠️ مقادیر چگالی این جدول از منابع صنعتی عمومی و *تقریبی* هستند و باید
   همیشه در صورت وجود، با برگه‌ی مشخصات فنی (SDS) محصول واقعی جایگزین
   شوند. اینها فقط یک مقدار پیش‌فرض معقول برای شروع محاسبه‌اند.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Tuple, Union

ChemicalKind = Literal["acid", "base"]

# نوع‌های شناخته‌شده - باید با acid_type در models.Fertilizer هم‌خوان باشد
KnownAcidType = Literal["HCl", "HNO3", "H2SO4", "H3PO4", "NaOH"]


@dataclass(frozen=True)
class ChemicalSpec:
    """ثابت‌های ذاتی یک ترکیب شیمیایی (وابسته به فرمول، نه به محصول تجاری خاص)"""

    formula: str
    name_fa: str
    kind: ChemicalKind
    mw: float  # جرم مولی g/mol
    z: Union[float, Literal["phosphoric"]]  # ظرفیت مؤثر (اکی‌والان بر مول)


KNOWN_ACID_BASE_CONSTANTS: Dict[str, ChemicalSpec] = {
    "HCl": ChemicalSpec("HCl", "اسید کلریدریک", "acid", mw=36.46, z=1),
    "HNO3": ChemicalSpec("HNO₃", "اسید نیتریک", "acid", mw=63.01, z=1),
    "H2SO4": ChemicalSpec("H₂SO₄", "اسید سولفوریک", "acid", mw=98.08, z=2),
    "H3PO4": ChemicalSpec("H₃PO₄", "اسید فسفریک", "acid", mw=97.99, z="phosphoric"),
    "NaOH": ChemicalSpec("NaOH", "سدیم هیدروکسید", "base", mw=40.00, z=1),
}

# ------------------------------------------------------------
# جدول مرجعِ چگالیِ محلول تجاری بر حسب درصد خلوص وزنی (g/mL @ ~20°C)
# منبع: جداول عمومی صنعتی (CRC / تولیدکنندگان اسید صنعتی) - تقریبی.
# هر ردیف: (درصد وزنی, چگالی g/mL)
# ------------------------------------------------------------
_DENSITY_TABLE: Dict[str, List[Tuple[float, float]]] = {
    "HCl": [
        (10, 1.047), (15, 1.073), (20, 1.098), (25, 1.124),
        (30, 1.149), (32, 1.159), (35, 1.174), (37, 1.185), (38, 1.190),
    ],
    "HNO3": [
        (10, 1.054), (20, 1.115), (30, 1.180), (40, 1.246),
        (50, 1.310), (60, 1.367), (63, 1.383), (65, 1.391),
        (68, 1.405), (70, 1.413),
    ],
    "H2SO4": [
        (10, 1.066), (20, 1.139), (30, 1.219), (40, 1.303),
        (50, 1.395), (60, 1.498), (70, 1.611), (80, 1.727),
        (90, 1.814), (93, 1.835), (96, 1.836), (98, 1.840),
    ],
    "H3PO4": [
        (10, 1.053), (25, 1.151), (35, 1.210), (50, 1.335),
        (61, 1.410), (75, 1.579), (85, 1.689), (100, 1.874),
    ],
    "NaOH": [
        (10, 1.109), (20, 1.219), (25, 1.269), (30, 1.332),
        (40, 1.430), (50, 1.525),
    ],
}


def resolve_density_g_ml(acid_type: str, concentration_pct: float) -> Tuple[Optional[float], bool]:
    """
    چگالی تقریبی (g/mL) محلول تجاری را بر اساس نوع اسید/باز و درصد خلوص
    وزنی آن، با میان‌یابی خطی روی جدول مرجع برمی‌گرداند.

    Returns:
        (density_g_ml یا None اگر نوع ناشناخته باشد، is_extrapolated)
        is_extrapolated=True یعنی درصد وارد شده خارج از بازه‌ی جدول مرجع
        بوده و نتیجه با برون‌یابی به‌دست آمده (باید با احتیاط بیشتری
        استفاده شود و بهتر است کاربر مقدار واقعی را وارد کند).
    """
    table = _DENSITY_TABLE.get(acid_type)
    if not table:
        return None, False

    xs = [p[0] for p in table]
    ys = [p[1] for p in table]

    if concentration_pct <= xs[0]:
        extrapolated = concentration_pct < xs[0]
        # برون‌یابی خطی با شیب اولین بازه
        if extrapolated and len(xs) > 1:
            slope = (ys[1] - ys[0]) / (xs[1] - xs[0])
            return ys[0] + slope * (concentration_pct - xs[0]), True
        return ys[0], False

    if concentration_pct >= xs[-1]:
        extrapolated = concentration_pct > xs[-1]
        if extrapolated and len(xs) > 1:
            slope = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
            return ys[-1] + slope * (concentration_pct - xs[-1]), True
        return ys[-1], False

    for i in range(len(xs) - 1):
        if xs[i] <= concentration_pct <= xs[i + 1]:
            if xs[i + 1] == xs[i]:
                return ys[i], False
            fraction = (concentration_pct - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + fraction * (ys[i + 1] - ys[i]), False

    return None, False
