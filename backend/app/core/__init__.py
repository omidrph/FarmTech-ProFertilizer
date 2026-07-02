"""
Core Module - هسته اصلی محاسبات FarmTech
========================================

این ماژول شامل تمام محاسبات اصلی برنامه است:
- تعادل یونی (Ion Balance)
- بهینه‌سازی NNLS (Fertilizer Optimization)
- مدیریت مخازن (Reservoir Management)
- محاسبه EC و pH
- 🆕 تعادل یونی خودکار
"""

from .ion_balance import (
    # Constants
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
    PH_RANGES,
    # Converters
    ppm_to_meq,
    meq_to_ppm,
    ppm_to_mmol,
    mmol_to_ppm,
    convert_units,
    # Calculator
    calculate_ion_balance,
    get_ion_balance_status,
    calculate_ec,
    calculate_ph,
    get_ec_ph_status,
    check_element_status,
    get_element_standard_range,
    # 🆕 تابع جدید
    auto_balance_ion,
    # Validators
    validate_ion_balance_result,
    check_precipitation
)

from .optimizer import (
    # Matrix Builder
    build_optimization_matrix,
    # NNLS Solver
    optimize_with_nnls,
    optimize_with_lsq_linear,
    optimize_with_cost,
    # Result Processor
    calculate_final_concentrations,
    calculate_target_achievement,
    generate_optimization_summary,
    validate_optimization_result,
    # Main Function
    optimize_fertilizers
)

from .reservoir import (
    calculate_reservoir_data,
    check_reservoir_compatibility,
    RESERVOIR_RULES
)

__all__ = [
    # Ion Balance - Constants
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
    # Ion Balance - Converters
    'ppm_to_meq',
    'meq_to_ppm',
    'ppm_to_mmol',
    'mmol_to_ppm',
    'convert_units',
    # Ion Balance - Calculator
    'calculate_ion_balance',
    'get_ion_balance_status',
    'calculate_ec',
    'calculate_ph',
    'get_ec_ph_status',
    'check_element_status',
    'get_element_standard_range',
    'auto_balance_ion',
    # Ion Balance - Validators
    'validate_ion_balance_result',
    'check_precipitation',
    # Optimizer
    'build_optimization_matrix',
    'optimize_with_nnls',
    'optimize_with_lsq_linear',
    'optimize_with_cost',
    'calculate_final_concentrations',
    'calculate_target_achievement',
    'generate_optimization_summary',
    'validate_optimization_result',
    'optimize_fertilizers',
    # Reservoir
    'calculate_reservoir_data',
    'check_reservoir_compatibility',
    'RESERVOIR_RULES'
]