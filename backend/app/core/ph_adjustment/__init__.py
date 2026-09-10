# backend/app/core/ph_adjustment/__init__.py
"""
ماژول ماشین‌حساب اصلاح pH
============================
محاسبه دوز اسید/باز لازم بر اساس pH اندازه‌گیری‌شده واقعی + قلیائیت آب.
"""

from .calculator import calculate_ph_adjustment_dose, ACID_BASE_SPECS

__all__ = [
    'calculate_ph_adjustment_dose',
    'ACID_BASE_SPECS',
]
