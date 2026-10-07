# backend/app/core/ph_calculator/__init__.py
"""
موتور محاسباتی «اصلاح pH» (نسخهٔ جدید - روش نسبتی/آزمون روی نمونه)
============================================================
جایگزین کامل نسخهٔ قبلی (مدل تئوریک کربنات + تیتراسیون چندنقطه‌ای).

ماژول‌ها:
    adjusters.py     - مشخصات اسید/باز، چگالی مرجع، درصد عناصر
    engine.py        - حل منحنی آزمون روی نمونه، مقیاس‌دهی به مخزن
    contributions.py - عناصر واردشده (ppm)، meq/L، ΔEC، مقایسه با آلکالینیتی
"""
from .adjusters import (
    AdjusterSpec,
    DISCOURAGED,
    KNOWN_ADJUSTERS,
    default_dose_unit,
    derive_elements_pct,
    get_spec,
    resolve_density_g_ml,
)
from .contributions import (
    alkalinity_check,
    ec_delta_ds_m,
    element_contributions_mg_l,
    ion_meq_l,
    neutralization_strength_meq_l,
)
from .integration import load_active_for_cycle, merge_into_water, summary_from_record
from .engine import (
    AdjustmentError,
    TankDose,
    TrialSolution,
    TrialStep,
    check_direction,
    direction_of,
    scale_to_tank,
    solve_trial,
)

__all__ = [
    "AdjusterSpec", "DISCOURAGED", "KNOWN_ADJUSTERS", "default_dose_unit", "derive_elements_pct",
    "get_spec", "resolve_density_g_ml",
    "alkalinity_check", "ec_delta_ds_m", "element_contributions_mg_l", "ion_meq_l",
    "neutralization_strength_meq_l",
    "AdjustmentError", "TankDose", "TrialSolution", "TrialStep", "check_direction",
    "direction_of", "scale_to_tank", "solve_trial",
    "load_active_for_cycle", "merge_into_water", "summary_from_record",
]
