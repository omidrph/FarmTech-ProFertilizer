# backend/app/seeds/__init__.py
"""
ماژول Seed برای داده‌های اولیه سیستم
"""
from .fertilizer_seeds import SYSTEM_FERTILIZERS, seed_system_fertilizers, get_system_fertilizers_count

__all__ = ['SYSTEM_FERTILIZERS', 'seed_system_fertilizers', 'get_system_fertilizers_count']