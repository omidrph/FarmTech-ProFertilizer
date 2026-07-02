"""
ماژول محاسبات تعادل یونی
================================

این ماژول شامل تمام توابع مربوط به محاسبه تعادل یونی است:
- تبدیل واحدها (PPM ↔ MEQ ↔ MMOL)
- محاسبه کاتیون و آنیون
- بررسی تعادل یونی
- اعتبارسنجی نتایج
- بررسی رسوب احتمالی
"""

from .constants import (
    MOLECULAR_WEIGHTS,
    VALENCES,
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    NEUTRAL_ELEMENTS,
    ALL_ELEMENTS,
    BALANCE_TOLERANCE
)

from .converters import (
    ppm_to_meq,
    meq_to_ppm,
    ppm_to_mmol,
    mmol_to_ppm,
    convert_units
)

from .calculator import (
    calculate_ion_balance,
    get_ion_balance_status
)

from .validators import (
    validate_ion_balance_result,
    check_precipitation
)

__all__ = [
    # Constants
    'MOLECULAR_WEIGHTS',
    'VALENCES',
    'CATION_ELEMENTS',
    'ANION_ELEMENTS',
    'NEUTRAL_ELEMENTS',
    'ALL_ELEMENTS',
    'BALANCE_TOLERANCE',
    # Converters
    'ppm_to_meq',
    'meq_to_ppm',
    'ppm_to_mmol',
    'mmol_to_ppm',
    'convert_units',
    # Calculator
    'calculate_ion_balance',
    'get_ion_balance_status',
    # Validators
    'validate_ion_balance_result',
    'check_precipitation'
]