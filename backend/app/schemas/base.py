# backend/app/schemas/base.py
"""
کلاس‌های پایه و Validatorهای مشترک برای همه طرح‌ها
"""

from typing import Any
from pydantic import BaseModel, validator
import re


# ============================================================
# 🔐 کلاس SecureString برای اعتبارسنجی رشته‌های امن
# ============================================================

class SecureString(str):
    """
    کلاس کمکی برای اعتبارسنجی رشته‌های امن
    جلوگیری از XSS و SQL Injection
    """
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            return v
        
        # لیست کاراکترهای خطرناک
        dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/', '\\x00']
        for char in dangerous_chars:
            if char in v:
                raise ValueError(f'رشته حاوی کاراکترهای غیرمجاز است: {char}')
        
        return v.strip()


# ============================================================
# 🔐 توابع اعتبارسنجی مشترک
# ============================================================

def validate_phone_number(phone: str) -> str:
    """
    اعتبارسنجی شماره تلفن ایران
    
    Args:
        phone: شماره تلفن
    
    Returns:
        str: شماره تلفن معتبر
    
    Raises:
        ValueError: اگر شماره تلفن نامعتبر باشد
    """
    if not re.match(r'^09[0-9]{9}$', phone):
        raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
    return phone


def validate_password_strength(password: str) -> str:
    """
    اعتبارسنجی قدرت رمز عبور
    
    Args:
        password: رمز عبور
    
    Returns:
        str: رمز عبور معتبر
    
    Raises:
        ValueError: اگر رمز عبور ضعیف باشد
    """
    if len(password) < 8:
        raise ValueError('رمز عبور باید حداقل ۸ کاراکتر باشد')
    
    if not any(c.isupper() for c in password):
        raise ValueError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد')
    
    if not any(c.islower() for c in password):
        raise ValueError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
    
    if not any(c.isdigit() for c in password):
        raise ValueError('رمز عبور باید حداقل یک عدد داشته باشد')
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
        raise ValueError('رمز عبور باید حداقل یک کاراکتر خاص داشته باشد')
    
    return password


def validate_name(name: str) -> str:
    """
    اعتبارسنجی نام (جلوگیری از XSS)
    
    Args:
        name: نام
    
    Returns:
        str: نام معتبر
    
    Raises:
        ValueError: اگر نام حاوی کاراکترهای غیرمجاز باشد
    """
    if any(char in name for char in ['<', '>', '"', "'", ';', '--']):
        raise ValueError('نام حاوی کاراکترهای غیرمجاز است')
    return name.strip()


def validate_element_name(element: str) -> str:
    """
    اعتبارسنجی نام عنصر
    
    Args:
        element: نام عنصر
    
    Returns:
        str: نام عنصر معتبر
    
    Raises:
        ValueError: اگر نام عنصر نامعتبر باشد
    """
    if not re.match(r'^[A-Za-z0-9\-]+$', element):
        raise ValueError(f'نام عنصر {element} نامعتبر است')
    return element


def validate_code(code: str) -> str:
    """
    اعتبارسنجی کد تأیید (۶ رقمی عددی)
    
    Args:
        code: کد تأیید
    
    Returns:
        str: کد معتبر
    
    Raises:
        ValueError: اگر کد نامعتبر باشد
    """
    if not code.isdigit():
        raise ValueError('کد باید عددی باشد')
    if len(code) != 6:
        raise ValueError('کد باید ۶ رقمی باشد')
    return code