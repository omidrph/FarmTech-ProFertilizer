"""
موتور محاسباتی «ماشین‌حساب pH»
============================================================
این پکیج جایگزین منطق قدیمیِ فرانت‌اندی (frontend/.../widgets/ph/*.ts)
است. تمام محاسبات شیمیایی اکنون در بک‌اند (پایتون) انجام می‌شود؛
فرانت‌اند فقط UI است و از طریق API این نتایج را می‌گیرد.

ماژول‌ها:
    chemistry.py - تعادل کربنات/فسفات، تبدیل واحد آلکالینیتی
    acids.py     - ثابت‌های شیمیایی اسید/باز (MW، ظرفیت، چگالی مرجع)
    dose.py      - محاسبه‌ی دوز (مسیر تئوریک و مسیر تیتراسیون واقعی)

مرجع: «گزارش فنی اصلاح‌شده – سیستم اصلاح pH» نسخه ۳٫۰ (همان مرجعی
که پیاده‌سازی قبلی فرانت‌اند بر اساس آن نوشته شده بود). فرمول‌های
تعادل کربنات و فسفات بدون تغییر پایتونی شدند و با تست واحد در برابر
پیاده‌سازی قبلی و مقادیر مرجع اعتبارسنجی شدند (به تست‌ها مراجعه کنید:
backend/tests/test_ph_calculator.py).
"""
from .chemistry import (
    CarbonateConstants,
    carbonate_constants,
    carbonate_fractions,
    alkalinity_from_ct,
    total_carbon_from_alkalinity,
    phosphate_fractions,
    phosphoric_effective_z,
    mgl_caco3_to_meql,
    meql_to_mgl_caco3,
    normalize_alkalinity_to_mgl,
)
from .acids import (
    ChemicalKind,
    ChemicalSpec,
    KNOWN_ACID_BASE_CONSTANTS,
    resolve_density_g_ml,
)
from .dose import (
    DoseInputBase,
    TheoreticalInput,
    TitrationInput,
    TitrationPoint,
    calculate_theoretical,
    calculate_titration,
    equivalents_to_commercial,
)

__all__ = [
    "CarbonateConstants",
    "carbonate_constants",
    "carbonate_fractions",
    "alkalinity_from_ct",
    "total_carbon_from_alkalinity",
    "phosphate_fractions",
    "phosphoric_effective_z",
    "mgl_caco3_to_meql",
    "meql_to_mgl_caco3",
    "normalize_alkalinity_to_mgl",
    "ChemicalKind",
    "ChemicalSpec",
    "KNOWN_ACID_BASE_CONSTANTS",
    "resolve_density_g_ml",
    "DoseInputBase",
    "TheoreticalInput",
    "TitrationInput",
    "TitrationPoint",
    "calculate_theoretical",
    "calculate_titration",
    "equivalents_to_commercial",
]
