# backend/app/core/ph_calculator/contributions.py
"""
اثر دوز اسید/باز بر محلول: عناصر واردشده، meq/L، ΔEC و بررسی آلکالینیتی
============================================================
همه‌چیز بر مبنای غلظت «محلول نهایی داخل مخزن اصلی» است (mg/L = ppm)، دقیقاً
همان مبنایی که بهینه‌ساز، تعادل یونی و EC برنامه استفاده می‌کنند؛ پس خروجی
این ماژول مستقیماً به‌عنوان یک «منبع تأمین عنصر» (مثل آب) در چرخهٔ محاسبه
قابل استفاده است.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from app.core.ion_balance.calculator import calculate_ec
from app.core.ion_balance.constants import ANION_ELEMENTS, CATION_ELEMENTS, VALENCES
from app.core.ion_balance.converters import ppm_to_meq

CACO3_EQ_WEIGHT = 50.0  # mg CaCO3 per meq


def element_contributions_mg_l(
    commercial_mass_g: float, elements_pct: Optional[Dict[str, float]], tank_volume_l: float
) -> Dict[str, float]:
    """
    mg/L هر عنصر:  جرم تجاری (g) × درصد/۱۰۰ × ۱۰۰۰ ÷ حجم (L)
    (همان رابطه‌ای که در بقیهٔ برنامه برای محاسبهٔ عنصر از وزن کود استفاده می‌شود)
    """
    if not elements_pct or not (tank_volume_l > 0) or not (commercial_mass_g > 0):
        return {}
    out: Dict[str, float] = {}
    for el, pct in elements_pct.items():
        try:
            p = float(pct)
        except (TypeError, ValueError):
            continue
        if p <= 0:
            continue
        out[el] = commercial_mass_g * (p / 100.0) * 1000.0 / tank_volume_l
    return out


def ion_meq_l(contributions_mg_l: Dict[str, float]) -> Tuple[float, float]:
    """(کاتیون meq/L, آنیون meq/L) ناشی از دوز."""
    cat = ani = 0.0
    for el, v in contributions_mg_l.items():
        if el not in VALENCES or not v:
            continue
        meq = ppm_to_meq(v, el)
        if el in CATION_ELEMENTS:
            cat += meq
        elif el in ANION_ELEMENTS:
            ani += meq
    return cat, ani


def ec_delta_ds_m(contributions_mg_l: Dict[str, float]) -> float:
    """
    افزایش EC (dS/m) ناشی از دوز؛ با همان فرمول EC برنامه (میانگین meq کاتیون و
    آنیون × ۰٫۱) تا با EC نهایی محاسبه‌شدهٔ فرمول سازگار باشد.
    """
    if not contributions_mg_l:
        return 0.0
    return float(calculate_ec(contributions_mg_l, unit="ppm", water_ec=None)["ec"])


def neutralization_strength_meq_l(contributions_mg_l: Dict[str, float], kind: str) -> float:
    """قدرت خنثی‌سازی دوز بر حسب meq/L (مجموع آنیون برای اسید، کاتیون برای باز)."""
    cat, ani = ion_meq_l(contributions_mg_l)
    return ani if kind == "acid" else cat


def alkalinity_check(
    strength_meq_l: float, kind: str, water_alkalinity_ppm_caco3: Optional[float]
) -> Tuple[Optional[float], List[str]]:
    """
    مقایسهٔ قدرت اسید با آلکالینیتی آب (meq/L = ppm CaCO₃ ÷ ۵۰).
    خروجی: (آلکالینیتی meq/L یا None، هشدارها)
    """
    if not water_alkalinity_ppm_caco3 or water_alkalinity_ppm_caco3 <= 0:
        return None, []
    alk = water_alkalinity_ppm_caco3 / CACO3_EQ_WEIGHT
    warnings: List[str] = []
    if kind == "acid" and strength_meq_l > alk * 1.5:
        warnings.append(
            f"قدرت اسید مصرفی (≈{strength_meq_l:.1f} meq/L) از آلکالینیتی آب ({alk:.1f} meq/L) بیشتر است؛ "
            "بخشی از اسید توسط بافر کودها (فسفات/آمونیوم/کلات) خنثی می‌شود. اگر این مقدار با آزمون واقعی "
            "به‌دست نیامده، دوباره بررسی کنید."
        )
    return alk, warnings
