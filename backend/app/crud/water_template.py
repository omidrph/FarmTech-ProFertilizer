# backend/app/crud/water_template.py
"""
عملیات CRUD برای مدل WaterAnalysisTemplate (قالب آنالیز آب)
"""

from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from app.models import WaterAnalysisTemplate
from app.schemas import WaterAnalysisTemplateCreate, WaterAnalysisTemplateUpdate

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای WaterAnalysisTemplate (قالب آنالیز آب)
# ============================================================

def create_water_template(db: Session, template_data: WaterAnalysisTemplateCreate, user_id: int) -> WaterAnalysisTemplate:
    """ایجاد قالب آنالیز آب جدید"""
    try:
        db_template = WaterAnalysisTemplate(
            user_id=user_id,
            name=template_data.name,
            description=template_data.description,
            water_percentage=template_data.water_percentage,
            wastewater_percentage=template_data.wastewater_percentage,
            water_salinity=template_data.water_salinity,
            water_salinity_unit=template_data.water_salinity_unit,
            water_ph=template_data.water_ph,
            water_values=template_data.water_values or {},
            wastewater_values=template_data.wastewater_values or {}
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        logger.info(f"Water template created: {db_template.id} - {db_template.name}")
        return db_template
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating water template: {e}")
        raise e


def get_water_templates_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[WaterAnalysisTemplate]:
    """دریافت قالب‌های آنالیز آب کاربر"""
    try:
        return db.query(WaterAnalysisTemplate).filter(
            WaterAnalysisTemplate.user_id == user_id
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting water templates: {e}")
        return []


def get_water_template_by_id(db: Session, template_id: int) -> Optional[WaterAnalysisTemplate]:
    """دریافت قالب آنالیز آب با شناسه"""
    try:
        return db.query(WaterAnalysisTemplate).filter(
            WaterAnalysisTemplate.id == template_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting water template by id: {e}")
        return None


def update_water_template(db: Session, template_id: int, template_data: WaterAnalysisTemplateUpdate) -> Optional[WaterAnalysisTemplate]:
    """به‌روزرسانی قالب آنالیز آب"""
    try:
        db_template = get_water_template_by_id(db, template_id)
        if db_template is None:
            return None
        
        update_data = template_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_template, key, value)
        
        db.commit()
        db.refresh(db_template)
        logger.info(f"Water template updated: {template_id}")
        return db_template
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating water template: {e}")
        raise e


def delete_water_template(db: Session, template_id: int) -> bool:
    """حذف قالب آنالیز آب"""
    try:
        db_template = get_water_template_by_id(db, template_id)
        if db_template is None:
            return False
        
        db.delete(db_template)
        db.commit()
        logger.info(f"Water template deleted: {template_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting water template: {e}")
        raise e