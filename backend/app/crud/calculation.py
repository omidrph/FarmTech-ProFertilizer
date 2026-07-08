# backend/app/crud/calculation.py
"""
عملیات CRUD برای مدل Calculation (محاسبات)
"""

from typing import Optional
from sqlalchemy.orm import Session
import logging

from app.models import Calculation
from app.schemas import CalculationCreate, CalculationUpdate
from app.crud.base import process_calculation_data

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای Calculation (محاسبات) - نسخه اصلاح شده
# ============================================================

def create_calculation(db: Session, calc_data: CalculationCreate, report_id: int) -> Calculation:
    """ایجاد محاسبات جدید"""
    try:
        db_calculation = Calculation(
            report_id=report_id,
            target_values=calc_data.target_values or {},
            final_values=calc_data.final_values or {},
            reservoir_data=calc_data.reservoir_data or {},
            calc_rows=calc_data.calc_rows or [],
            interpretation=calc_data.interpretation
        )
        
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        
        logger.info(f"Calculation created: {db_calculation.id} for report {report_id}")
        return db_calculation
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating calculation: {e}")
        raise e


def get_calculation_by_report(db: Session, report_id: int) -> Optional[Calculation]:
    """
    دریافت محاسبات بر اساس گزارش
    
    این تابع اصلاح شده است تا مطمئن شود target_values به صورت دیکشنری برگردانده می‌شود
    """
    try:
        calc = db.query(Calculation).filter(Calculation.report_id == report_id).first()
        
        if calc:
            calc = process_calculation_data(calc)
        
        return calc
    except Exception as e:
        logger.error(f"Error getting calculation by report: {e}")
        return None


def update_calculation(db: Session, calc_id: int, calc_data: CalculationUpdate) -> Optional[Calculation]:
    """به‌روزرسانی محاسبات"""
    try:
        db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        
        if db_calculation is None:
            return None
        
        update_data = calc_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_calculation, key, value)
        
        db.commit()
        db.refresh(db_calculation)
        
        logger.info(f"Calculation updated: {calc_id}")
        return db_calculation
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating calculation: {e}")
        raise e


def delete_calculation(db: Session, calc_id: int) -> bool:
    """حذف محاسبات"""
    try:
        db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        
        if db_calculation is None:
            return False
        
        db.delete(db_calculation)
        db.commit()
        
        logger.info(f"Calculation deleted: {calc_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting calculation: {e}")
        raise e