# backend/app/schemas/auth.py
"""
طرح‌های مربوط به احراز هویت (Authentication)
شامل: User, Login, Register, Token, 2FA, Reset Password
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator

from .base import (
    validate_phone_number,
    validate_password_strength,
    validate_name,
    validate_code
)


# ============================================================
# طرح‌های مربوط به User (کاربر)
# ============================================================

class UserCreate(BaseModel):
    """طرح ثبت‌نام کاربر جدید"""
    first_name: str = Field(..., min_length=1, max_length=50, description="نام")
    last_name: str = Field(..., min_length=1, max_length=50, description="نام خانوادگی")
    phone_number: str = Field(..., min_length=11, max_length=15, description="شماره تلفن")
    password: str = Field(..., min_length=8, max_length=100, description="رمز عبور")

    @validator('phone_number')
    def validate_phone(cls, v):
        return validate_phone_number(v)
    
    @validator('password')
    def validate_password(cls, v):
        return validate_password_strength(v)
    
    @validator('first_name', 'last_name')
    def validate_name_fields(cls, v):
        return validate_name(v)


class UserLogin(BaseModel):
    """طرح ورود کاربر"""
    phone_number: str = Field(..., description="شماره تلفن")
    password: str = Field(..., description="رمز عبور")

    @validator('phone_number')
    def validate_phone(cls, v):
        return validate_phone_number(v)


class UserResponse(BaseModel):
    """طرح پاسخ اطلاعات کاربر"""
    id: int
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    full_name: str
    created_at: datetime
    is_2fa_enabled: bool = False

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """طرح به‌روزرسانی اطلاعات کاربر"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=11, max_length=15)

    @validator('phone_number')
    def validate_phone(cls, v):
        if v:
            return validate_phone_number(v)
        return v
    
    @validator('first_name', 'last_name')
    def validate_name_fields(cls, v):
        if v:
            return validate_name(v)
        return v


# ============================================================
# طرح‌های مربوط به Token (توکن تصادفی)
# ============================================================

class Token(BaseModel):
    """طرح پاسخ توکن"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """طرح داده‌های توکن"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = None


# ============================================================
# 🔐 طرح‌های امنیتی - تغییر رمز عبور
# ============================================================

class ChangePasswordRequest(BaseModel):
    """درخواست تغییر رمز عبور"""
    current_password: str = Field(..., min_length=8, description="رمز عبور فعلی")
    new_password: str = Field(..., min_length=8, description="رمز عبور جدید")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        return validate_password_strength(v)


class ChangePasswordResponse(BaseModel):
    """پاسخ تغییر رمز عبور"""
    message: str
    success: bool


# ============================================================
# 🔐 طرح‌های فراموشی رمز عبور (با پیامک)
# ============================================================

class ForgotPasswordRequest(BaseModel):
    """درخواست فراموشی رمز عبور"""
    phone_number: str = Field(..., description="شماره تلفن")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        return validate_phone_number(v)


class ForgotPasswordResponse(BaseModel):
    """پاسخ فراموشی رمز عبور"""
    message: str
    success: bool
    reset_id: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    """درخواست بازنشانی رمز عبور"""
    phone_number: str = Field(..., description="شماره تلفن")
    code: str = Field(..., min_length=6, max_length=6, description="کد تأیید ۶ رقمی")
    new_password: str = Field(..., min_length=8, description="رمز عبور جدید")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        return validate_phone_number(v)
    
    @validator('code')
    def validate_code_field(cls, v):
        return validate_code(v)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        return validate_password_strength(v)


class ResetPasswordResponse(BaseModel):
    """پاسخ بازنشانی رمز عبور"""
    message: str
    success: bool


# ============================================================
# 🔐 طرح‌های 2FA (تأیید دو مرحله‌ای)
# ============================================================

class Enable2FARequest(BaseModel):
    """درخواست فعال‌سازی 2FA"""
    phone_number: str = Field(..., description="شماره تلفن")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        return validate_phone_number(v)


class Enable2FAResponse(BaseModel):
    """پاسخ فعال‌سازی 2FA"""
    secret: str
    backup_codes: List[str]
    qr_code_url: Optional[str] = None
    message: str
    success: bool


class Verify2FARequest(BaseModel):
    """درخواست تأیید 2FA"""
    code: str = Field(..., min_length=6, max_length=6, description="کد ۶ رقمی")
    
    @validator('code')
    def validate_code_field(cls, v):
        return validate_code(v)


class Verify2FAResponse(BaseModel):
    """پاسخ تأیید 2FA"""
    message: str
    success: bool


class Disable2FARequest(BaseModel):
    """درخواست غیرفعال‌سازی 2FA"""
    code: str = Field(..., min_length=6, max_length=6, description="کد ۶ رقمی")
    
    @validator('code')
    def validate_code_field(cls, v):
        return validate_code(v)


class Disable2FAResponse(BaseModel):
    """پاسخ غیرفعال‌سازی 2FA"""
    message: str
    success: bool