"""
ماژول مدیریت مخازن A, B, C
===========================

این ماژول شامل توابع مربوط به مدیریت مخازن است:
- توزیع مواد در مخازن A, B, C
- بررسی سازگاری شیمیایی
- قوانین توزیع
"""

from .distributor import (
    calculate_reservoir_data,
    RESERVOIR_RULES
)

from .compatibility import (
    check_reservoir_compatibility,
    get_compatibility_warnings,
    check_nutrient_interactions,
    check_manual_fertilizer_selection,
)

from .stock_instructions import (
    calculate_stock_instructions
)

__all__ = [
    'calculate_reservoir_data',
    'RESERVOIR_RULES',
    'check_reservoir_compatibility',
    'get_compatibility_warnings',
    'check_nutrient_interactions',
    'check_manual_fertilizer_selection',
    'calculate_stock_instructions',
]


