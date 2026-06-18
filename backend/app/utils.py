# backend/app/utils.py
"""ابزارهای کمکی و توابع عمومی"""

import re
from typing import Optional
from datetime import datetime


# ============================================================
# اعتبارسنجی‌ها
# ============================================================

def validate_phone_number(phone: str) -> bool:
    """
    اعتبارسنجی شماره تلفن ایران
    
    Args:
        phone: شماره تلفن
    
    Returns:
        bool: آیا شماره تلفن معتبر است
    """
    pattern = r'^09[0-9]{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """
    اعتبارسنجی ایمیل
    
    Args:
        email: آدرس ایمیل
    
    Returns:
        bool: آیا ایمیل معتبر است
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_national_code(code: str) -> bool:
    """
    اعتبارسنجی کد ملی ایران
    
    Args:
        code: کد ملی
    
    Returns:
        bool: آیا کد ملی معتبر است
    """
    if not code or len(code) != 10:
        return False
    
    # الگوریتم اعتبارسنجی کد ملی
    try:
        digits = [int(d) for d in code]
        if len(set(digits)) == 1:
            return False
        
        sum_ = sum(digits[i] * (10 - i) for i in range(9))
        remainder = sum_ % 11
        
        if remainder < 2:
            return digits[9] == remainder
        else:
            return digits[9] == 11 - remainder
    except:
        return False


# ============================================================
# توابع تاریخ و زمان
# ============================================================

def get_current_shamsi_date() -> str:
    """
    دریافت تاریخ شمسی فعلی
    
    Returns:
        str: تاریخ شمسی به فرمت YYYY/MM/DD
    """
    # این یک پیاده‌سازی ساده است
    # برای دقت بیشتر از کتابخانه‌های تخصصی استفاده کنید
    return datetime.now().strftime("%Y/%m/%d")


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    فرمت کردن تاریخ
    
    Args:
        date: شیء datetime
        format_str: فرمت مورد نظر
    
    Returns:
        str: تاریخ فرمت شده
    """
    if date is None:
        return ""
    return date.strftime(format_str)


# ============================================================
# توابع تولید شناسه
# ============================================================

def generate_id() -> str:
    """
    تولید یک شناسه یکتا
    
    Returns:
        str: شناسه یکتا
    """
    import uuid
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """
    تولید یک شناسه کوتاه
    
    Args:
        length: طول شناسه
    
    Returns:
        str: شناسه کوتاه
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ============================================================
# توابع تبدیل و فرمت
# ============================================================

def to_camel_case(snake_str: str) -> str:
    """
    تبدیل snake_case به camelCase
    
    Args:
        snake_str: رشته به فرمت snake_case
    
    Returns:
        str: رشته به فرمت camelCase
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """
    تبدیل camelCase به snake_case
    
    Args:
        camel_str: رشته به فرمت camelCase
    
    Returns:
        str: رشته به فرمت snake_case
    """
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


# ============================================================
# توابع logging
# ============================================================

def setup_logger(name: str, level: str = "INFO") -> None:
    """
    تنظیم logger برای برنامه
    
    Args:
        name: نام logger
        level: سطح لاگ (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    import logging
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)