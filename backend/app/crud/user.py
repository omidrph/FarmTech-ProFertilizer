# backend/app/crud/user.py
"""
عملیات CRUD برای مدل User (کاربر)
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.security import get_password_hash, delete_user_sessions

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای User (کاربر) - نسخه نهایی با مدیریت خطا
# ============================================================

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    ایجاد کاربر جدید
    
    Returns:
        User: کاربر ایجاد شده
    
    Raises:
        ValueError: اگر خطایی در ایجاد کاربر رخ دهد
    """
    try:
        # اعتبارسنجی ورودی
        if not user_data.phone_number:
            raise ValueError("شماره تلفن نمی‌تواند خالی باشد")
        
        if not user_data.password:
            raise ValueError("رمز عبور نمی‌تواند خالی باشد")
        
        if len(user_data.phone_number) != 11:
            raise ValueError("شماره تلفن باید ۱۱ رقم باشد")
        
        if not user_data.phone_number.startswith("09"):
            raise ValueError("شماره تلفن باید با 09 شروع شود")
        
        # هش کردن رمز عبور
        hashed_password = get_password_hash(user_data.password)
        
        # ایجاد کاربر
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            password_hash=hashed_password,
            is_active=True,
            failed_attempts=0
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"✅ User created: {db_user.id} - {db_user.phone_number}")
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        # خطای یکتایی (Duplicate)
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            logger.error(f"Duplicate phone number: {user_data.phone_number}")
            raise ValueError("این شماره تلفن قبلاً ثبت شده است")
        logger.error(f"Integrity error creating user: {e}")
        raise ValueError(f"خطا در ایجاد کاربر: {str(e)}")
        
    except ValueError:
        # خطاهای اعتبارسنجی را دوباره raise می‌کنیم
        db.rollback()
        raise
        
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating user: {e}")
        raise ValueError(f"خطا در ایجاد کاربر: {str(e)}")


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """دریافت کاربر با شناسه"""
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error getting user by id: {e}")
        return None


def get_user_by_phone(db: Session, phone_number: str) -> Optional[User]:
    """دریافت کاربر با شماره تلفن"""
    try:
        return db.query(User).filter(User.phone_number == phone_number).first()
    except Exception as e:
        logger.error(f"Error getting user by phone: {e}")
        return None


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """دریافت لیست کاربران"""
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return []


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """به‌روزرسانی اطلاعات کاربر"""
    try:
        db_user = get_user_by_id(db, user_id)
        
        if db_user is None:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User updated: {db_user.id}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        raise e


def delete_user(db: Session, user_id: int) -> bool:
    """حذف کاربر (همراه با حذف نشست‌ها)"""
    try:
        db_user = get_user_by_id(db, user_id)
        
        if db_user is None:
            return False
        
        delete_user_sessions(user_id, db)
        
        db.delete(db_user)
        db.commit()
        
        logger.info(f"User deleted: {user_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {e}")
        raise e