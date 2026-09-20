
# backend/app/crud/base.py
"""
کلاس پایه و توابع مشترک برای ماژول CRUD
شامل توابع تبدیل JSON و عملیات پایه دیتابیس
"""

import json
import logging
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


# ============================================================
# توابع کمکی برای تبدیل JSON
# ============================================================

def safe_json_loads(value: Any, default: Any = None) -> Any:
    """
    تبدیل ایمن JSON رشته به دیکشنری یا لیست
    
    Args:
        value: مقدار ورودی (می‌تواند رشته JSON یا دیکشنری باشد)
        default: مقدار پیش‌فرض در صورت خطا
    
    Returns:
        Any: مقدار تبدیل شده
    """
    if value is None:
        return default if default is not None else {}
    
    if isinstance(value, (dict, list)):
        return value
    
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON: {value[:100]}...")
            return default if default is not None else {}
    
    return default if default is not None else {}


def safe_json_dumps(value: Any) -> Optional[str]:
    """
    تبدیل ایمن دیکشنری یا لیست به رشته JSON
    
    Args:
        value: مقدار ورودی
    
    Returns:
        Optional[str]: رشته JSON یا None
    """
    if value is None:
        return None
    
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except TypeError:
            logger.warning(f"Failed to serialize to JSON: {value}")
            return None
    
    return str(value) if value else None


# ============================================================
# توابع کمکی برای پردازش داده‌های محاسبات
# ============================================================

def process_calculation_data(calc: Any) -> Any:
    """
    پردازش داده‌های محاسبات و تبدیل JSON رشته‌ها به دیکشنری/لیست
    
    Args:
        calc: شیء Calculation از دیتابیس
    
    Returns:
        Any: شیء Calculation با داده‌های پردازش شده
    """
    if calc is None:
        return None
    
    # پردازش target_values
    if calc.target_values is not None:
        if isinstance(calc.target_values, str):
            try:
                calc.target_values = json.loads(calc.target_values)
                logger.info(f"Converted target_values from JSON string for calculation {calc.id}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse target_values JSON for calculation {calc.id}: {e}")
                calc.target_values = {}
        elif not isinstance(calc.target_values, dict):
            logger.warning(f"target_values is not a dict for calculation {calc.id}, type: {type(calc.target_values)}")
            calc.target_values = {}
    else:
        calc.target_values = {}
    
    # پردازش final_values
    if calc.final_values is not None:
        if isinstance(calc.final_values, str):
            try:
                calc.final_values = json.loads(calc.final_values)
            except json.JSONDecodeError:
                calc.final_values = {}
        elif not isinstance(calc.final_values, dict):
            calc.final_values = {}
    else:
        calc.final_values = {}
    
    # پردازش reservoir_data
    if calc.reservoir_data is not None:
        if isinstance(calc.reservoir_data, str):
            try:
                calc.reservoir_data = json.loads(calc.reservoir_data)
            except json.JSONDecodeError:
                calc.reservoir_data = {}
        elif not isinstance(calc.reservoir_data, dict):
            calc.reservoir_data = {}
    else:
        calc.reservoir_data = {}
    
    # پردازش calc_rows
    if calc.calc_rows is not None:
        if isinstance(calc.calc_rows, str):
            try:
                calc.calc_rows = json.loads(calc.calc_rows)
            except json.JSONDecodeError:
                calc.calc_rows = []
        elif not isinstance(calc.calc_rows, list):
            calc.calc_rows = []
    else:
        calc.calc_rows = []

    # 🆕 پردازش selected_fertilizer_ids
    if calc.selected_fertilizer_ids is not None:
        if isinstance(calc.selected_fertilizer_ids, str):
            try:
                calc.selected_fertilizer_ids = json.loads(calc.selected_fertilizer_ids)
            except json.JSONDecodeError:
                calc.selected_fertilizer_ids = []
        elif not isinstance(calc.selected_fertilizer_ids, list):
            calc.selected_fertilizer_ids = []
    else:
        calc.selected_fertilizer_ids = []

    # 🆕 پردازش optimization_options
    if calc.optimization_options is not None:
        if isinstance(calc.optimization_options, str):
            try:
                calc.optimization_options = json.loads(calc.optimization_options)
            except json.JSONDecodeError:
                calc.optimization_options = {}
        elif not isinstance(calc.optimization_options, dict):
            calc.optimization_options = {}
    else:
        calc.optimization_options = {}

    # 🆕 پردازش optimization_result (کل نتیجه محاسبه، برای بازیابی بدون محاسبه مجدد)
    if calc.optimization_result is not None:
        if isinstance(calc.optimization_result, str):
            try:
                calc.optimization_result = json.loads(calc.optimization_result)
            except json.JSONDecodeError:
                calc.optimization_result = {}
        elif not isinstance(calc.optimization_result, dict):
            calc.optimization_result = {}
    else:
        calc.optimization_result = {}

    return calc



