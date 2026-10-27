
# backend/app/core/ph_calculator/integration.py
"""
اتصال «اصلاح pH فعال» به چرخهٔ محاسبهٔ کود
============================================================
اصل کار: عناصر واردشده از اسید/باز مثل «آب» یک منبع پایه‌اند. با افزودن آن‌ها
به water_values پیش از اجرای بهینه‌ساز:
  • هدف باقی‌مانده برای کودهای دیگر کم می‌شود (سهم کودها خودکار کاهش می‌یابد)
  • غلظت نهایی، تعادل یونی، EC و بررسی رسوب، همه با لحاظ اسید محاسبه می‌شوند
  • هیچ تغییری در خود بهینه‌ساز لازم نیست
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .contributions import CACO3_EQ_WEIGHT, neutralization_strength_meq_l

# کلیدهایی از water_values که «غلظت عنصر» نیستند
_NON_ELEMENT_KEYS = {"pH", "EC", "Alkalinity", "TDS", "Hardness"}


def merge_into_water(
    water_values: Optional[Dict[str, float]],
    contributions: Optional[Dict[str, float]],
    alkalinity_shift_ppm: Optional[float] = None,
) -> Dict[str, float]:
    """
    water_values + سهم اسید/باز (فقط عناصر؛ pH/EC دست‌نخورده می‌مانند).
    آلکالینیتی آب (ppm CaCO₃) با اسید کم و با باز زیاد می‌شود تا بررسی رسوب کربنات
    (که بعد از اصلاح pH اجرا می‌شود) واقعی‌تر باشد.
    """
    merged: Dict[str, float] = dict(water_values or {})
    if alkalinity_shift_ppm and (merged.get("Alkalinity") or 0) > 0:
        merged["Alkalinity"] = max(0.0, float(merged["Alkalinity"]) + float(alkalinity_shift_ppm))
    for el, val in (contributions or {}).items():
        if el in _NON_ELEMENT_KEYS:
            continue
        try:
            v = float(val)
        except (TypeError, ValueError):
            continue
        if v <= 0:
            continue
        merged[el] = float(merged.get(el, 0) or 0) + v
    return merged


def summary_from_record(record: Any) -> Dict[str, Any]:
    """خلاصهٔ JSON‌پذیر از یک رکورد PhAdjustment (برای پاسخ بهینه‌ساز و صفحهٔ محاسبه)."""
    contrib = dict(record.element_contributions or {})
    strength = neutralization_strength_meq_l(contrib, record.kind)
    shift = -strength * CACO3_EQ_WEIGHT if record.kind == "acid" else strength * CACO3_EQ_WEIGHT
    return {
        "id": record.id,
        "fertilizer_id": record.fertilizer_id,
        "chemical": {"density_g_ml": (record.chemical or {}).get("density_g_ml")},
        "chemical_name": record.chemical_name,
        "kind": record.kind,
        "mode": record.mode,
        "dose_unit": record.dose_unit,
        "dose_tank": float(record.dose_tank),
        "dose_per_1000l": float(record.dose_per_1000l),
        "tank_volume_l": float(record.tank_volume_l),
        "initial_ph": record.initial_ph,
        "target_ph": record.target_ph,
        "final_ph": record.final_ph,
        "element_contributions": contrib,
        "strength_meq_l": strength,
        "alkalinity_shift_ppm": shift,
        "ec_delta": record.ec_delta,
        "updated_at": record.updated_at.isoformat() if getattr(record, "updated_at", None) else None,
    }


def load_active_for_cycle(db: Any, crud_module: Any, user_id: int, report_id: Optional[int]):
    """
    (contributions, summary) اصلاح فعال گزارش؛ اگر نباشد ({}, None).
    خطای دیتابیس هرگز نباید محاسبهٔ اصلی را بشکند.
    """
    if not report_id:
        return {}, None
    try:
        record = crud_module.get_active_adjustment(db, user_id, report_id)
    except Exception:
        return {}, None
    if not record:
        return {}, None
    return dict(record.element_contributions or {}), summary_from_record(record)


def apply_ph_cost(db: Any, summary: Optional[Dict[str, Any]], tank_volume: Optional[float]) -> float:
    """
    هزینهٔ اسید/باز تب PH برای «حجم مخزن همین محاسبه».
    - مقدار برای هر ۱۰۰۰ لیتر (dose_per_1000l) × (حجم مخزن / ۱۰۰۰)
    - مایع (ml) با چگالی به گرم تبدیل می‌شود؛ قیمت کود همیشه به‌ازای کیلوگرم ذخیره است.
    خلاصهٔ ورودی (summary) درجا با فیلدهای cost / dose_total / price_per_kg تکمیل می‌شود.
    خطا یا نبودن قیمت هرگز محاسبهٔ اصلی را نمی‌شکند (هزینه = ۰).
    """
    if not summary:
        return 0.0
    try:
        from app.models import Fertilizer
        vol = float(tank_volume or 0) or 1000.0
        dose_total = float(summary.get("dose_per_1000l") or 0) * vol / 1000.0
        unit = summary.get("dose_unit") or "g"
        price = 0.0
        density = None
        fid = None
        try:
            fid = (summary.get("chemical") or {}).get("fertilizer_id")
        except Exception:
            fid = None
        fert = None
        if fid is None:
            fid = summary.get("fertilizer_id")
        if fid:
            fert = db.query(Fertilizer).filter(Fertilizer.id == fid).first()
        if fert is not None:
            price = float(fert.price_per_kg or 0)
            density = getattr(fert, "density_g_ml", None)
        grams = dose_total
        if unit == "ml":
            d = float(density or (summary.get("chemical") or {}).get("density_g_ml") or 0)
            grams = dose_total * d if d > 0 else 0.0
        cost = grams / 1000.0 * price
        summary["dose_total"] = round(dose_total, 3)
        summary["dose_total_g"] = round(grams, 3)
        summary["price_per_kg"] = price
        summary["cost"] = round(cost, 2)
        return cost
    except Exception:
        return 0.0
