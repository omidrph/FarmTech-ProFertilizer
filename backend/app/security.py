# backend/app/security.py
"""امنیت و احراز هویت - Session-based با توکن در دیتابیس"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User, UserSession

# ===== تنظیمات Header =====
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

import logging
logger = logging.getLogger(__name__)


# ============================================================
# توابع هش کردن و بررسی رمز عبور
# ============================================================

def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((salt + password).encode('utf-8'))
    hash_str = hash_obj.hexdigest()
    return f"{salt}:{hash_str}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if ':' not in hashed_password:
            return False
        salt, stored_hash = hashed_password.split(':')
        hash_obj = hashlib.sha256((salt + plain_password).encode('utf-8'))
        computed_hash = hash_obj.hexdigest()
        return computed_hash == stored_hash
    except (ValueError, AttributeError):
        return False


# ============================================================
# توابع توکن تصادفی
# ============================================================

def create_session_token(user_id: int, db: Session, expires_in_hours: int = 24) -> str:
    """ایجاد توکن تصادفی و ذخیره در دیتابیس"""
    # غیرفعال کردن توکن‌های قبلی کاربر
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).update({"is_active": False})
    db.commit()
    
    token = secrets.token_urlsafe(64)
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    session = UserSession(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        is_active=True
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"✅ توکن تصادفی برای کاربر {user_id} ایجاد شد: {token[:10]}...")
    return token


def get_session_by_token(token: str, db: Session) -> Optional[UserSession]:
    """دریافت نشست فعال از دیتابیس"""
    if not token:
        return None
    
    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if session:
        logger.info(f"✅ نشست پیدا شد: user_id={session.user_id}")
    else:
        logger.warning(f"❌ نشست معتبری برای توکن پیدا نشد: {token[:10]}...")
    
    return session


def delete_session(token: str, db: Session) -> bool:
    """غیرفعال کردن نشست"""
    session = db.query(UserSession).filter(UserSession.token == token).first()
    if session:
        session.is_active = False
        db.commit()
        logger.info(f"✅ توکن غیرفعال شد: {token[:10]}...")
        return True
    return False


def delete_user_sessions(user_id: int, db: Session) -> None:
    """غیرفعال کردن تمام نشست‌های کاربر"""
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).update({"is_active": False})
    db.commit()
    logger.info(f"✅ تمام توکن‌های کاربر {user_id} غیرفعال شد")


# ============================================================
# توابع دریافت کاربر فعلی
# ============================================================

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    دریافت کاربر فعلی از هدر Authorization
    """
    # دریافت توکن از هدر
    auth_header = request.headers.get("Authorization")
    logger.info(f"🔍 هدر Authorization: {auth_header[:30] if auth_header else 'None'}...")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="هدر Authorization یافت نشد",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # حذف "Bearer " از ابتدای توکن
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    else:
        token = auth_header
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن خالی است",
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
    
    logger.info(f"✅ کاربر پیدا شد: {user.phone_number}")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="حساب کاربری غیرفعال است")
    return current_user