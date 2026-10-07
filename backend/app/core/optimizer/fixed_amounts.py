# backend/app/core/optimizer/fixed_amounts.py
"""
مقدار «ثابت» تعیین‌شده توسط کاربر برای بعضی کودها (معمولاً اسید/باز)
============================================================
کاربر در انتخاب کود برای یک اسید/باز مقدار دقیق را مشخص می‌کند (مثلاً ۲ لیتر برای کل مخزن).
بهینه‌ساز این مقدار را تغییر نمی‌دهد؛ عناصرش از هدف کسر می‌شود و بقیهٔ کودها همان مقدار
باقی‌مانده را تأمین می‌کنند.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

UNIT_TO_GRAMS = {"g": 1.0, "kg": 1000.0}
UNIT_TO_ML = {"ml": 1.0, "l": 1000.0}


class FixedAmountError(ValueError):
    pass


def amount_to_grams(amount: float, unit: Optional[str], density_g_ml: Optional[float], name: str = "") -> float:
    """مقدار (g/kg/ml/L) → گرم محصول تجاری."""
    u = (unit or "g").strip().lower()
    if u in UNIT_TO_GRAMS:
        return float(amount) * UNIT_TO_GRAMS[u]
    if u in UNIT_TO_ML:
        if not density_g_ml or density_g_ml <= 0:
            raise FixedAmountError(
                f"برای «{name}» مقدار به صورت حجمی داده شده ولی چگالی کود ثبت نشده است؛ "
                "چگالی را در پایگاه‌داده کود وارد کنید."
            )
        return float(amount) * UNIT_TO_ML[u] * float(density_g_ml)
    raise FixedAmountError(f"واحد «{unit}» پشتیبانی نمی‌شود (g, kg, ml, l).")


def apply_fixed_amounts(fertilizers: List[Dict[str, Any]], tank_volume: float) -> List[Dict[str, Any]]:
    """
    برای کودهایی که fixed_amount دارند، fixed_weight (گرم برای هر ۱۰۰۰ لیتر) را پر می‌کند.
    ورودی را تغییر نمی‌دهد؛ لیست جدید برمی‌گرداند.
    """
    out: List[Dict[str, Any]] = []
    for f in fertilizers:
        g = dict(f)
        amount = g.get("fixed_amount")
        if amount is not None and amount > 0:
            grams_total = amount_to_grams(amount, g.get("fixed_unit"), g.get("density_g_ml"), g.get("name", ""))
            g["fixed_weight"] = grams_total * 1000.0 / float(tank_volume)
            g["fixed_total_g"] = grams_total
        out.append(g)
    return out
