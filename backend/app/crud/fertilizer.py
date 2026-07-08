# backend/app/crud/fertilizer.py
"""
عملیات CRUD برای مدل Fertilizer (کود)
"""

from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import logging

from app.models import Fertilizer
from app.schemas import FertilizerCreate, FertilizerUpdate

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای Fertilizer (کود) - نسخه نهایی
# ============================================================

def create_fertilizer(db: Session, fertilizer_data: FertilizerCreate, user_id: int) -> Fertilizer:
    """
    ایجاد کود جدید
    
    Args:
        db: Session دیتابیس
        fertilizer_data: داده‌های کود
        user_id: شناسه کاربر
    
    Returns:
        Fertilizer: شیء کود ایجاد شده
    """
    try:
        logger.info(f"Creating fertilizer: {fertilizer_data.name} for user {user_id}")
        
        db_fertilizer = Fertilizer(
            user_id=user_id,
            name=fertilizer_data.name,
            brand=fertilizer_data.brand,
            category=fertilizer_data.category,
            form=fertilizer_data.form,
            concentration=fertilizer_data.concentration or 100.0,
            elements=fertilizer_data.elements or {},
            price_per_kg=fertilizer_data.price_per_kg or 0.0,
            is_acid=fertilizer_data.is_acid,
            acid_type=fertilizer_data.acid_type,
            ph_level=fertilizer_data.ph_level,
            description=fertilizer_data.description,
            is_system_default=fertilizer_data.is_system_default,
            source_system_id=fertilizer_data.source_system_id
        )
        
        db.add(db_fertilizer)
        db.commit()
        db.refresh(db_fertilizer)
        
        logger.info(f"Fertilizer created successfully: ID={db_fertilizer.id}, Name={db_fertilizer.name}")
        return db_fertilizer
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating fertilizer: {e}")
        raise e


def get_fertilizer_by_id(db: Session, fertilizer_id: int) -> Optional[Fertilizer]:
    """دریافت کود با شناسه"""
    try:
        return db.query(Fertilizer).filter(Fertilizer.id == fertilizer_id).first()
    except Exception as e:
        logger.error(f"Error getting fertilizer by id: {e}")
        return None


def get_fertilizers_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Fertilizer]:
    """دریافت کودهای یک کاربر (فقط شخصی)"""
    try:
        return db.query(Fertilizer).filter(
            Fertilizer.user_id == user_id,
            Fertilizer.is_system_default == False
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting fertilizers by user: {e}")
        return []


def get_system_fertilizers(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Fertilizer]:
    """دریافت کودهای سیستمی (برای نمایش و کپی)"""
    try:
        return db.query(Fertilizer).filter(
            Fertilizer.is_system_default == True,
            Fertilizer.user_id == None
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting system fertilizers: {e}")
        return []


def get_all_fertilizers_for_user(db: Session, user_id: int) -> Dict[str, List[Fertilizer]]:
    """دریافت همه کودها (سیستمی + شخصی) برای یک کاربر"""
    try:
        system = get_system_fertilizers(db)
        user = get_fertilizers_by_user(db, user_id)
        return {
            "system_fertilizers": system,
            "user_fertilizers": user
        }
    except Exception as e:
        logger.error(f"Error getting all fertilizers for user: {e}")
        return {"system_fertilizers": [], "user_fertilizers": []}


def update_fertilizer(db: Session, fertilizer_id: int, fertilizer_data: FertilizerUpdate) -> Optional[Fertilizer]:
    """به‌روزرسانی کود"""
    try:
        db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
        
        if db_fertilizer is None:
            return None
        
        update_data = fertilizer_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_fertilizer, key, value)
        
        db.commit()
        db.refresh(db_fertilizer)
        
        logger.info(f"Fertilizer updated: {fertilizer_id}")
        return db_fertilizer
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating fertilizer: {e}")
        raise e


def delete_fertilizer(db: Session, fertilizer_id: int) -> bool:
    """حذف کود (فقط کودهای شخصی قابل حذف هستند)"""
    try:
        db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
        
        if db_fertilizer is None:
            return False
        
        # کودهای سیستمی قابل حذف نیستند (فقط توسط seed مدیریت می‌شوند)
        if db_fertilizer.is_system_default and db_fertilizer.user_id is None:
            logger.warning(f"Cannot delete system fertilizer: {fertilizer_id}")
            return False
        
        db.delete(db_fertilizer)
        db.commit()
        
        logger.info(f"Fertilizer deleted: {fertilizer_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting fertilizer: {e}")
        raise e


def copy_system_fertilizer_to_user(db: Session, system_fertilizer_id: int, user_id: int) -> Optional[Fertilizer]:
    """
    کپی کردن یک کود سیستمی به عنوان کود شخصی کاربر
    
    Args:
        db: Session دیتابیس
        system_fertilizer_id: شناسه کود سیستمی
        user_id: شناسه کاربر
    
    Returns:
        Fertilizer: کود شخصی ایجاد شده
    """
    try:
        # پیدا کردن کود سیستمی
        system_fert = get_fertilizer_by_id(db, system_fertilizer_id)
        
        if system_fert is None:
            logger.error(f"System fertilizer not found: {system_fertilizer_id}")
            return None
        
        if not system_fert.is_system_default or system_fert.user_id is not None:
            logger.error(f"Fertilizer {system_fertilizer_id} is not a system fertilizer")
            return None
        
        # بررسی اینکه کاربر قبلاً این کود را کپی نکرده باشد
        existing = db.query(Fertilizer).filter(
            Fertilizer.user_id == user_id,
            Fertilizer.source_system_id == system_fertilizer_id
        ).first()
        
        if existing:
            logger.info(f"User {user_id} already copied system fertilizer {system_fertilizer_id}")
            return existing
        
        # ایجاد کپی
        new_fertilizer = Fertilizer(
            user_id=user_id,
            name=system_fert.name,
            brand=system_fert.brand,
            category=system_fert.category,
            form=system_fert.form,
            concentration=system_fert.concentration,
            elements=system_fert.elements,
            price_per_kg=system_fert.price_per_kg,
            is_acid=system_fert.is_acid,
            acid_type=system_fert.acid_type,
            ph_level=system_fert.ph_level,
            description=system_fert.description,
            is_system_default=False,
            source_system_id=system_fertilizer_id
        )
        
        db.add(new_fertilizer)
        db.commit()
        db.refresh(new_fertilizer)
        
        logger.info(f"System fertilizer {system_fertilizer_id} copied to user {user_id} as {new_fertilizer.id}")
        return new_fertilizer
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error copying system fertilizer: {e}")
        raise e


def copy_all_system_fertilizers_to_user(db: Session, user_id: int) -> Dict[str, int]:
    """
    کپی کردن همه کودهای سیستمی به عنوان کودهای شخصی کاربر
    
    Returns:
        Dict: آمار عملیات
    """
    stats = {
        "copied": 0,
        "skipped": 0,
        "total": 0,
        "errors": []
    }
    
    try:
        system_fertilizers = get_system_fertilizers(db)
        stats["total"] = len(system_fertilizers)
        
        for fert in system_fertilizers:
            try:
                result = copy_system_fertilizer_to_user(db, fert.id, user_id)
                if result:
                    stats["copied"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as e:
                stats["errors"].append({
                    "fertilizer_id": fert.id,
                    "name": fert.name,
                    "error": str(e)
                })
                stats["skipped"] += 1
        
        logger.info(f"Copied {stats['copied']} system fertilizers to user {user_id}")
        return stats
        
    except Exception as e:
        logger.error(f"Error copying all system fertilizers: {e}")
        stats["errors"].append({"error": str(e)})
        return stats