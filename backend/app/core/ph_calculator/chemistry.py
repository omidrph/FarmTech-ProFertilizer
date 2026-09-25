# backend/app/core/ph_calculator/chemistry.py
"""
شیمی پایه‌ی ماشین‌حساب pH (توابع خالص - بدون وابستگی به دیتابیس یا HTTP)
============================================================
پورت مستقیم و بدون تغییرِ ریاضی از نسخه‌ی قبلی فرانت‌اند
(frontend/.../widgets/ph/phChemistry.ts) به پایتون.

فرض‌های مدل (به کاربر هم در پاسخ API نمایش داده می‌شود):
  • سیستم بسته است (CO₂ با هوا تبادل نمی‌کند؛ C_T ثابت می‌ماند)
  • ضریب فعالیت = ۱ (از قدرت یونی صرف‌نظر شده است)
  • آلکالینیتی فقط از کربنات/بی‌کربنات/هیدروکسید می‌آید

⚠️ نکته‌ی مهم درباره‌ی واحد آلکالینیتی (منشأ خطای گزارش‌شده‌ی «۵۰ برابری»):
    ۱ meq/L آلکالینیتی = ۵۰ mg/L به صورت معادل CaCO₃
  (چون جرم اکی‌والان CaCO₃ برابر ۵۰ گرم بر اکی‌والان است: MW=100, z=2).
  یعنی اگر مقداری که در واقع meq/L است به‌اشتباه به عنوان mg/L CaCO₃
  به مدل داده شود، نتیجه دقیقاً ۵۰ برابر کوچک‌تر از واقعی می‌شود؛ و برعکس.
  به همین دلیل در این نسخه، واحد ورودی صراحتاً از کاربر گرفته می‌شود
  (normalize_alkalinity_to_mgl) و تبدیل به‌صورت مرکزی و تست‌شده انجام
  می‌شود، نه در چند جای پراکنده‌ی کد.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, Optional, Tuple

AlkalinityUnit = Literal["mg_l_caco3", "meq_l"]


@dataclass(frozen=True)
class CarbonateConstants:
    K1: float
    K2: float
    Kw: float
    pK1: float
    pK2: float
    pKw: float


def carbonate_constants(temperature_c: float) -> CarbonateConstants:
    """
    ثابت‌های تعادل کربنات و آب بر حسب دما (°C).
    pK1 و pK2: Plummer & Busenberg (1982)؛ pKw: رابطه‌ی Millero.
    """
    t = temperature_c + 273.15
    pk1 = 356.3094 + 0.06091964 * t - 21834.37 / t - 126.8339 * math.log10(t) + 1684915 / (t * t)
    pk2 = 107.8871 + 0.03252849 * t - 5151.79 / t - 38.92561 * math.log10(t) + 563713.9 / (t * t)
    pkw = 4470.99 / t - 6.0875 + 0.01706 * t
    return CarbonateConstants(
        K1=10 ** -pk1, K2=10 ** -pk2, Kw=10 ** -pkw, pK1=pk1, pK2=pk2, pKw=pkw
    )


def carbonate_fractions(ph: float, c: CarbonateConstants) -> Tuple[float, float, float]:
    """کسرهای گونه‌ای کربنات: (α₀ H₂CO₃*، α₁ HCO₃⁻، α₂ CO₃²⁻)"""
    h = 10 ** -ph
    d = h * h + c.K1 * h + c.K1 * c.K2
    return (h * h) / d, (c.K1 * h) / d, (c.K1 * c.K2) / d


def alkalinity_from_ct(ph: float, ct: float, c: CarbonateConstants) -> float:
    """آلکالینیتی (eq/L) در مدل کربناتی: C_T(α₁+2α₂) + Kw/H − H"""
    h = 10 ** -ph
    _, a1, a2 = carbonate_fractions(ph, c)
    return ct * (a1 + 2 * a2) + c.Kw / h - h


def total_carbon_from_alkalinity(ph: float, alk_eq_l: float, c: CarbonateConstants) -> float:
    """تخمین C_T (mol/L) از آلکالینیتی و pH اولیه (وارونِ رابطه‌ی بالا)"""
    h = 10 ** -ph
    _, a1, a2 = carbonate_fractions(ph, c)
    denom = a1 + 2 * a2
    if denom == 0:
        return float("nan")
    return (alk_eq_l - c.Kw / h + h) / denom


# pKa های اسید فسفریک در ۲۵°C
PK_PHOSPHATE = (2.15, 7.2, 12.35)


def phosphate_fractions(ph: float) -> Tuple[float, float, float, float]:
    """کسرهای گونه‌ای فسفات: (H₃PO₄، H₂PO₄⁻، HPO₄²⁻، PO₄³⁻)"""
    h = 10 ** -ph
    k1, k2, k3 = (10 ** -pk for pk in PK_PHOSPHATE)
    d = h ** 3 + k1 * h ** 2 + k1 * k2 * h + k1 * k2 * k3
    return (
        h ** 3 / d,
        (k1 * h ** 2) / d,
        (k1 * k2 * h) / d,
        (k1 * k2 * k3) / d,
    )


def phosphoric_effective_z(target_ph: float) -> float:
    """
    ظرفیت مؤثر (meq بر mmol) اسید فسفریک در pH هدف.
    با مرجع H₂PO₄⁻ برای آلکالینیتی، افزودن H₃PO₄ دقیقاً ۱ eq/mol آلکالینیتی
    می‌کاهد و خودِ گونه‌های فسفات نیز در pH هدف سهم دارند:
        z_eff = 1 + (α HPO₄²⁻ + 2·α PO₄³⁻ − α H₃PO₄)
    (در pH≈۷ حدود ۱٫۴ و در pH≈۶ حدود ۱٫۱؛ یعنی «۳» ثابت نیست.)
    """
    f0, _f1, f2, f3 = phosphate_fractions(target_ph)
    return 1 + f2 + 2 * f3 - f0


# ------------------------------------------------------------
# تبدیل واحد آلکالینیتی
# ------------------------------------------------------------
# جرم اکی‌والان CaCO₃ = ۱۰۰ (MW) / ۲ (ظرفیت) = ۵۰ گرم بر اکی‌والان
CACO3_EQUIVALENT_WEIGHT = 50.0


def mgl_caco3_to_meql(mg_l: float) -> float:
    """mg/L به‌صورت معادل CaCO₃ -> meq/L"""
    return mg_l / CACO3_EQUIVALENT_WEIGHT


def meql_to_mgl_caco3(meq_l: float) -> float:
    """meq/L -> mg/L به‌صورت معادل CaCO₃"""
    return meq_l * CACO3_EQUIVALENT_WEIGHT


def normalize_alkalinity_to_mgl(value: float, unit: AlkalinityUnit) -> float:
    """
    مقدار آلکالینیتی را به mg/L معادل CaCO₃ (واحد داخلی مدل) تبدیل می‌کند.
    این تابع تنها نقطه‌ی تبدیل واحد آلکالینیتی در کل سیستم است تا از خطای
    ۵۰ برابری (اشتباه گرفتن meq/L با mg/L CaCO₃) جلوگیری شود.
    """
    if unit == "meq_l":
        return meql_to_mgl_caco3(value)
    return value
