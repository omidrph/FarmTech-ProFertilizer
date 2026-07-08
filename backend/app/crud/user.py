# backend/app/crud/user.py
"""
عملیات CRUD برای مدل User (کاربر)
"""

from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.security import get_password_hash, delete_user_sessions

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای User (کاربر)
# ============================================================

def create_user(db: Session, user_data: UserCreate) -> User:
    """ایجاد کاربر جدید"""
    try:
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            password_hash=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created: {db_user.id} - {db_user.phone_number}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise e


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