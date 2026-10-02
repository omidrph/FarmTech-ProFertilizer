# backend/app/core/ph_calculator/adjusters.py
"""
مشخصات شیمیایی اسیدها و بازهای تنظیم‌کنندهٔ pH
============================================================
توابع این ماژول «خالص» هستند (بدون وابستگی به دیتابیس یا HTTP).

نقش این ماژول در منطق جدید:
  • مبنای محاسبهٔ عناصر واردشده به محلول، «درصد عناصر» همان کودی است که
    کاربر در پایگاه‌داده‌ی کود خودش ثبت کرده است (Fertilizer.elements)؛ مثل
    بقیهٔ برنامه. فقط اگر این درصدها ثبت نشده باشند، از روی فرمول شیمیایی و
    خلوص محاسبه می‌شود (derive_elements_pct).
  • چگالی (برای تبدیل mL به گرم) از جدول مرجع تقریبی برداشته می‌شود و کاربر
    می‌تواند مقدار دقیق برگهٔ مشخصات (SDS) را جایگزین کند.
  • «معادل بر مول» (z) فقط برای هشدارهای کمکی (مقایسه با آلکالینیتی آب)
    استفاده می‌شود، نه برای محاسبهٔ دوز؛ دوز از آزمون واقعی/رسپی می‌آید.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Tuple

AdjusterKind = Literal["acid", "base"]


@dataclass(frozen=True)
class AdjusterSpec:
    formula: str
    name_fa: str
    kind: AdjusterKind
    mw: float                 # جرم مولی (g/mol)
    element: str              # کلید عنصر در برنامه (مثلاً N-NO3)
    atomic_weight: float      # جرم اتمی عنصر
    atoms: int                # تعداد اتم عنصر در یک مولکول
    z: float                  # معادل (eq) بر مول؛ اسیدیته یا بازیته‌ی مؤثر در pH کشت
    note: Optional[str] = None


KNOWN_ADJUSTERS: Dict[str, AdjusterSpec] = {
    "HNO3": AdjusterSpec("HNO₃", "اسید نیتریک", "acid", 63.01, "N-NO3", 14.007, 1, 1.0),
    "H2SO4": AdjusterSpec("H₂SO₄", "اسید سولفوریک", "acid", 98.08, "S", 32.065, 1, 2.0),
    "H3PO4": AdjusterSpec(
        "H₃PO₄", "اسید فسفریک", "acid", 97.99, "P", 30.9738, 1, 1.0,
        note="در pH حدود ۶ تا ۷ فسفات به‌صورت H₂PO₄⁻ و HPO₄²⁻ است؛ معادل مؤثر کمی بیشتر از ۱ است.",
    ),
    "HCl": AdjusterSpec(
        "HCl", "اسید کلریدریک", "acid", 36.46, "Cl", 35.453, 1, 1.0,
        note="کلر در هیدروپونیک تجمع می‌یابد و توصیه نمی‌شود.",
    ),
    "KOH": AdjusterSpec("KOH", "پتاسیم هیدروکسید", "base", 56.11, "K", 39.0983, 1, 1.0),
    "K2CO3": AdjusterSpec("K₂CO₃", "پتاسیم کربنات", "base", 138.21, "K", 39.0983, 2, 2.0),
    "KHCO3": AdjusterSpec("KHCO₃", "پتاسیم بی‌کربنات", "base", 100.12, "K", 39.0983, 1, 1.0),
    "NaOH": AdjusterSpec(
        "NaOH", "سدیم هیدروکسید", "base", 40.00, "Na", 22.9898, 1, 1.0,
        note="سدیم در محیط کشت تجمع می‌یابد؛ تا حد امکان از پتاسیم هیدروکسید استفاده کنید.",
    ),
}

# موادی که مصرف آن‌ها در هیدروپونیک نیاز به هشدار دارد (کلید → متن هشدار)
DISCOURAGED: Dict[str, str] = {
    "HCl": "اسید کلریدریک کلر وارد محلول می‌کند و در هیدروپونیک به‌دلیل تجمع کلر توصیه نمی‌شود.",
    "NaOH": "سدیم هیدروکسید سدیم وارد محلول می‌کند که در سیستم‌های بازچرخشی تجمع می‌یابد.",
}

# ------------------------------------------------------------
# جدول مرجع چگالی محلول تجاری (g/mL در حدود ۲۰°C) بر حسب درصد وزنی - تقریبی
# ------------------------------------------------------------
_DENSITY_TABLE: Dict[str, List[Tuple[float, float]]] = {
    "HCl": [(10, 1.047), (20, 1.098), (30, 1.149), (32, 1.159), (35, 1.174), (37, 1.185), (38, 1.190)],
    "HNO3": [(10, 1.054), (20, 1.115), (30, 1.180), (40, 1.246), (50, 1.310), (60, 1.367),
             (63, 1.383), (65, 1.391), (68, 1.405), (70, 1.413)],
    "H2SO4": [(10, 1.066), (20, 1.139), (30, 1.219), (40, 1.303), (50, 1.395), (60, 1.498),
              (70, 1.611), (80, 1.727), (90, 1.814), (93, 1.835), (96, 1.836), (98, 1.840)],
    "H3PO4": [(10, 1.053), (25, 1.151), (35, 1.210), (50, 1.335), (61, 1.410), (75, 1.579),
              (85, 1.689), (100, 1.874)],
    "NaOH": [(10, 1.109), (20, 1.219), (25, 1.269), (30, 1.332), (40, 1.430), (50, 1.525)],
    "KOH": [(10, 1.092), (20, 1.188), (30, 1.290), (40, 1.399), (45, 1.456), (50, 1.514)],
    "K2CO3": [(10, 1.090), (20, 1.190), (30, 1.298), (40, 1.414), (50, 1.539)],
}


def get_spec(acid_type: Optional[str]) -> Optional[AdjusterSpec]:
    if not acid_type:
        return None
    return KNOWN_ADJUSTERS.get(acid_type.strip())


def resolve_density_g_ml(acid_type: Optional[str], concentration_pct: float) -> Tuple[Optional[float], bool]:
    """
    چگالی تقریبی (g/mL) با میان‌یابی خطی روی جدول مرجع.
    Returns: (density یا None برای نوع ناشناخته، is_extrapolated)
    """
    table = _DENSITY_TABLE.get((acid_type or "").strip())
    if not table or concentration_pct is None or concentration_pct <= 0:
        return None, False

    xs = [p[0] for p in table]
    ys = [p[1] for p in table]

    if concentration_pct < xs[0]:
        slope = (ys[1] - ys[0]) / (xs[1] - xs[0])
        # کمتر از آب خالص نشود
        return max(1.0, ys[0] + slope * (concentration_pct - xs[0])), True
    if concentration_pct > xs[-1]:
        slope = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        return ys[-1] + slope * (concentration_pct - xs[-1]), True

    for i in range(len(xs) - 1):
        if xs[i] <= concentration_pct <= xs[i + 1]:
            frac = (concentration_pct - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + frac * (ys[i + 1] - ys[i]), False
    return None, False


def derive_elements_pct(acid_type: Optional[str], purity_pct: float) -> Optional[Dict[str, float]]:
    """
    درصد وزنی عنصر در محصول تجاری از روی فرمول و خلوص (فقط وقتی در پایگاه‌داده
    ثبت نشده باشد). همان مبنای «عنصر خالص» که در سراسر برنامه استفاده می‌شود
    (مثلاً N-NO3 بر مبنای وزن اتمی N؛ نه وزن یون NO3⁻).
    """
    spec = get_spec(acid_type)
    if not spec or not (0 < purity_pct <= 100):
        return None
    pct = (purity_pct / 100.0) * (spec.atoms * spec.atomic_weight / spec.mw) * 100.0
    return {spec.element: pct}


def default_dose_unit(form: Optional[str], kind: AdjusterKind) -> Literal["ml", "g"]:
    """
    واحد مقدار مصرفی: مایع → میلی‌لیتر، جامد → گرم.
    اگر فرم ثبت نشده باشد: اسیدها مایع و بازها جامد فرض می‌شوند.
    """
    f = (form or "").strip().lower()
    if f == "liquid":
        return "ml"
    if f in ("powder", "crystal", "granular", "solid", "flake"):
        return "g"
    return "ml" if kind == "acid" else "g"
