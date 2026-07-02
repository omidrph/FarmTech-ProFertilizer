"""
ماژول محاسبات تعادل یونی
================================

این ماژول شامل تمام توابع مربوط به محاسبه تعادل یونی است:
- تبدیل واحدها (PPM ↔ MEQ ↔ MMOL)
- محاسبه کاتیون و آنیون
- بررسی تعادل یونی
- اعتبارسنجی نتایج
- بررسی رسوب احتمالی
- محاسبه EC و pH
- 🆕 تعادل یونی خودکار
"""

from .constants import (
    MOLECULAR_WEIGHTS,
    VALENCES,
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    NEUTRAL_ELEMENTS,
    ALL_ELEMENTS,
    BALANCE_TOLERANCE,
    ION_TO_EC_COEFFICIENTS,
    ACIDITY_COEFFICIENTS,
    EC_RANGES,
    PH_RANGES
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
    get_ion_balance_status,
    calculate_ec,
    calculate_ph,
    get_ec_ph_status,
    check_element_status,
    get_element_standard_range,
    # 🆕 تابع جدید
    auto_balance_ion
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
    'ION_TO_EC_COEFFICIENTS',
    'ACIDITY_COEFFICIENTS',
    'EC_RANGES',
    'PH_RANGES',
    # Converters
    'ppm_to_meq',
    'meq_to_ppm',
    'ppm_to_mmol',
    'mmol_to_ppm',
    'convert_units',
    # Calculator
    'calculate_ion_balance',
    'get_ion_balance_status',
    'calculate_ec',
    'calculate_ph',
    'get_ec_ph_status',
    'check_element_status',
    'get_element_standard_range',
    'auto_balance_ion',
    # Validators
    'validate_ion_balance_result',
    'check_precipitation'
]