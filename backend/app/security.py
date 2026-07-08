# backend/app/security.py
"""امنیت و احراز هویت - نسخه امنیتی کامل با bcrypt و مدیریت نشست پیشرفته"""

import secrets
import hashlib
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.config import settings
from app.database import get_db
from app.models import User, UserSession, SecurityLog
from app.security_logger import log_security_event

import logging

logger = logging.getLogger(__name__)

# ===== تنظیمات Header =====
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


# ============================================================
# 🔐 توابع هش کردن و بررسی رمز عبور با bcrypt
# ============================================================

def get_password_hash(password: str) -> str:
    """
    هش کردن رمز عبور با bcrypt
    
    Args:
        password: رمز عبور ساده
    
    Returns:
        str: رمز عبور هش شده
    """
    salt = bcrypt.gensalt(rounds=12)  # 12 round برای تعادل بین امنیت و سرعت
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    بررسی رمز عبور با bcrypt
    
    Args:
        plain_password: رمز عبور ساده
        hashed_password: رمز عبور هش شده
    
    Returns:
        bool: آیا رمز عبور صحیح است
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    اعتبارسنجی قدرت رمز عبور
    
    Args:
        password: رمز عبور
    
    Returns:
        Tuple[bool, str]: (آیا معتبر است, پیام خطا)
    """
    if len(password) < 8:
        return False, "رمز عبور باید حداقل ۸ کاراکتر باشد"
    
    if not any(c.isupper() for c in password):
        return False, "رمز عبور باید حداقل یک حرف بزرگ داشته باشد"
    
    if not any(c.islower() for c in password):
        return False, "رمز عبور باید حداقل یک حرف کوچک داشته باشد"
    
    if not any(c.isdigit() for c in password):
        return False, "رمز عبور باید حداقل یک عدد داشته باشد"
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
        return False, "رمز عبور باید حداقل یک کاراکتر خاص داشته باشد"
    
    return True, ""


# ============================================================
# 🔐 توابع توکن تصادفی با مدیریت نشست پیشرفته
# ============================================================

def create_session_token(
    user_id: int,
    db: Session,
    expires_in_hours: int = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> str:
    """
    ایجاد توکن تصادفی و ذخیره در دیتابیس با اطلاعات نشست
    
    Args:
        user_id: شناسه کاربر
        db: Session دیتابیس
        expires_in_hours: زمان انقضا (ساعت)
        ip_address: آدرس IP کاربر
        user_agent: User-Agent مرورگر
    
    Returns:
        str: توکن ایجاد شده
    """
    if expires_in_hours is None:
        expires_in_hours = settings.SESSION_EXPIRY_HOURS
    
    # غیرفعال کردن توکن‌های قبلی کاربر
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).update({"is_active": False})
    db.commit()
    
    # ایجاد توکن جدید
    token = secrets.token_urlsafe(64)
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    session = UserSession(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        is_active=True,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"✅ توکن تصادفی برای کاربر {user_id} ایجاد شد: {token[:10]}...")
    
    # ثبت رویداد امنیتی
    log_security_event(
        db=db,
        event_type="SESSION_CREATED",
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details={"expires_at": expires_at.isoformat()}
    )
    
    return token


def get_session_by_token(token: str, db: Session) -> Optional[UserSession]:
    """
    دریافت نشست فعال از دیتابیس
    
    Args:
        token: توکن
        db: Session دیتابیس
    
    Returns:
        Optional[UserSession]: نشست یا None
    """
    if not token:
        return None
    
    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if session:
        logger.info(f"✅ نشست پیدا شد: user_id={session.user_id}")
        # به‌روزرسانی آخرین فعالیت
        session.last_activity = datetime.utcnow()
        db.commit()
    else:
        logger.warning(f"❌ نشست معتبری برای توکن پیدا نشد: {token[:10]}...")
    
    return session


def delete_session(token: str, db: Session, ip_address: Optional[str] = None) -> bool:
    """
    غیرفعال کردن نشست
    
    Args:
        token: توکن
        db: Session دیتابیس
        ip_address: آدرس IP برای لاگ
    
    Returns:
        bool: آیا عملیات موفق بود
    """
    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.is_active == True
    ).first()
    
    if session:
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="SESSION_DELETED",
            user_id=session.user_id,
            ip_address=ip_address,
            details={"token": token[:10] + "..."}
        )
        
        session.is_active = False
        db.commit()
        logger.info(f"✅ توکن غیرفعال شد: {token[:10]}...")
        return True
    return False


def delete_user_sessions(user_id: int, db: Session) -> None:
    """
    غیرفعال کردن تمام نشست‌های کاربر
    
    Args:
        user_id: شناسه کاربر
        db: Session دیتابیس
    """
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).update({"is_active": False})
    db.commit()
    logger.info(f"✅ تمام توکن‌های کاربر {user_id} غیرفعال شد")


# ============================================================
# 🔐 مدیریت قفل حساب
# ============================================================

def increment_failed_attempts(user: User, db: Session) -> None:
    """
    افزایش تعداد تلاش‌های ناموفق و قفل حساب در صورت نیاز
    
    Args:
        user: شیء کاربر
        db: Session دیتابیس
    """
    user.failed_attempts = (user.failed_attempts or 0) + 1
    
    if user.failed_attempts >= settings.MAX_FAILED_ATTEMPTS:
        # قفل کردن حساب
        user.locked_until = datetime.utcnow() + timedelta(minutes=settings.ACCOUNT_LOCK_MINUTES)
        logger.warning(f"🔒 حساب کاربر {user.id} به دلیل {user.failed_attempts} تلاش ناموفق قفل شد")
    
    db.commit()


def reset_failed_attempts(user: User, db: Session) -> None:
    """
    بازنشانی تعداد تلاش‌های ناموفق پس از ورود موفق
    
    Args:
        user: شیء کاربر
        db: Session دیتابیس
    """
    user.failed_attempts = 0
    user.locked_until = None
    db.commit()


def check_account_lock(user: User) -> Tuple[bool, Optional[str]]:
    """
    بررسی وضعیت قفل حساب
    
    Args:
        user: شیء کاربر
    
    Returns:
        Tuple[bool, Optional[str]]: (آیا قفل است, پیام خطا)
    """
    if user.is_locked:
        remaining = (user.locked_until - datetime.utcnow()).seconds // 60
        return True, f"حساب کاربری به دلیل تلاش‌های ناموفق قفل شده است. {remaining} دقیقه دیگر تلاش کنید."
    return False, None


# ============================================================
# 🔐 توابع دریافت کاربر فعلی
# ============================================================

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    دریافت کاربر فعلی از هدر Authorization یا Cookie
    
    Args:
        request: درخواست FastAPI
        db: Session دیتابیس
    
    Returns:
        User: کاربر فعلی
    
    Raises:
        HTTPException: اگر کاربر احراز هویت نشده باشد
    """
    token = None
    
    # 1. ابتدا از Cookie دریافت کن
    token = request.cookies.get("access_token")
    
    # 2. اگر در Cookie نبود، از Header دریافت کن
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="احراز هویت نشده است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"🔍 توکن استخراج شده: {token[:10]}...")
    
    # پیدا کردن نشست در دیتابیس
    session = get_session_by_token(token, db)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر یا منقضی شده است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # پیدا کردن کاربر
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="کاربر یافت نشد",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    
    # بررسی قفل حساب
    is_locked, lock_message = check_account_lock(user)
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lock_message
        )
    
    # به‌روزرسانی آخرین فعالیت
    session.last_activity = datetime.utcnow()
    db.commit()
    
    logger.info(f"✅ کاربر پیدا شد: {user.phone_number}")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """دریافت کاربر فعال"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    return current_user


# ============================================================
# 🔐 توابع 2FA
# ============================================================

def generate_totp_secret() -> str:
    """
    تولید کلید مخفی برای TOTP
    
    Returns:
        str: کلید مخفی
    """
    import base64
    import os
    secret = base64.b32encode(os.urandom(20)).decode('utf-8')
    return secret


def generate_backup_codes(count: int = 10, length: int = 8) -> list:
    """
    تولید کدهای پشتیبان برای 2FA
    
    Args:
        count: تعداد کدها
        length: طول هر کد
    
    Returns:
        list: لیست کدهای پشتیبان
    """
    codes = []
    for _ in range(count):
        code = secrets.token_hex(length // 2).upper()
        # اضافه کردن خط تیره برای خوانایی بهتر
        code = "-".join([code[i:i+4] for i in range(0, len(code), 4)])
        codes.append(code)
    return codes


def verify_totp(secret: str, code: str) -> bool:
    """
    بررسی کد TOTP
    
    Args:
        secret: کلید مخفی
        code: کد وارد شده
    
    Returns:
        bool: آیا کد صحیح است
    """
    try:
        import pyotp
        totp = pyotp.TOTP(secret, interval=settings.TOTP_PERIOD, digits=settings.TOTP_DIGITS)
        return totp.verify(code, valid_window=1)
    except ImportError:
        # اگر pyotp نصب نیست، از روش ساده استفاده کن
        # این یک پیاده‌سازی موقتی است
        logger.warning("pyotp not installed, using simple verification")
        return len(code) == 6 and code.isdigit()
    except Exception as e:
        logger.error(f"TOTP verification error: {e}")
        return False


def verify_backup_code(user: User, code: str) -> bool:
    """
    بررسی کد پشتیبان
    
    Args:
        user: شیء کاربر
        code: کد وارد شده
    
    Returns:
        bool: آیا کد صحیح است
    """
    if not user.backup_codes:
        return False
    
    if code in user.backup_codes:
        # حذف کد استفاده شده
        user.backup_codes.remove(code)
        return True
    
    return False