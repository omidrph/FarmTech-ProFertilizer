# backend/app/crud/optimization_log.py
"""
عملیات CRUD برای مدل OptimizationLog (تاریخچه بهینه‌سازی)
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from app.models import OptimizationLog

logger = logging.getLogger(__name__)


# ============================================================
# 🆕 CRUD برای OptimizationLog (تاریخچه بهینه‌سازی)
# ============================================================

def save_optimization_log(
    db: Session,
    user_id: int,
    report_id: Optional[int],
    target_values: Dict[str, float],
    water_values: Optional[Dict[str, float]],
    fertilizers_selected: List[Dict[str, Any]],
    optimization_options: Optional[Dict[str, Any]],
    result: Dict[str, Any]
) -> OptimizationLog:
    """
    ذخیره تاریخچه بهینه‌سازی
    
    Args:
        db: Session دیتابیس
        user_id: شناسه کاربر
        report_id: شناسه گزارش (اختیاری)
        target_values: عناصر هدف
        water_values: کیفیت آب
        fertilizers_selected: لیست کودهای انتخاب شده
        optimization_options: تنظیمات بهینه‌سازی
        result: نتیجه بهینه‌سازی
    
    Returns:
        OptimizationLog: شیء ذخیره شده
    """
    try:
        log = OptimizationLog(
            user_id=user_id,
            report_id=report_id,
            target_values=target_values,
            water_values=water_values or {},
            fertilizers_selected=fertilizers_selected,
            optimization_options=optimization_options or {},
            optimized_weights=result.get('weights', {}),
            final_concentrations=result.get('concentrations', {}),
            residual_error=result.get('residual_error', 0),
            cost_total=result.get('cost_total', 0),
            iterations=result.get('iterations', 0),
            convergence_time_ms=result.get('convergence_time_ms', 0),
            ion_balance=result.get('ion_balance', {}),
            warnings=result.get('warnings', []),
            suggestions=result.get('suggestions', []),
            is_successful=True,
            error_message=None
        )
        
        db.add(log)
        db.commit()
        db.refresh(log)
        
        logger.info(f"Optimization log saved: {log.id}")
        return log
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving optimization log: {e}")
        raise e


def get_optimization_history(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    report_id: Optional[int] = None
) -> List[OptimizationLog]:
    """
    دریافت تاریخچه بهینه‌سازی کاربر
    
    Args:
        db: Session دیتابیس
        user_id: شناسه کاربر
        skip: تعداد رد شدن
        limit: تعداد دریافت
        report_id: فیلتر بر اساس گزارش (اختیاری)
    
    Returns:
        List[OptimizationLog]: لیست تاریخچه
    """
    try:
        query = db.query(OptimizationLog).filter(OptimizationLog.user_id == user_id)
        
        if report_id is not None:
            query = query.filter(OptimizationLog.report_id == report_id)
        
        return query.order_by(desc(OptimizationLog.created_at)).offset(skip).limit(limit).all()
        
    except Exception as e:
        logger.error(f"Error getting optimization history: {e}")
        return []


def get_optimization_log_by_id(db: Session, log_id: int) -> Optional[OptimizationLog]:
    """دریافت یک تاریخچه بهینه‌سازی با شناسه"""
    try:
        return db.query(OptimizationLog).filter(OptimizationLog.id == log_id).first()
    except Exception as e:
        logger.error(f"Error getting optimization log: {e}")
        return None


def delete_optimization_log(db: Session, log_id: int) -> bool:
    """حذف یک تاریخچه بهینه‌سازی"""
    try:
        log = get_optimization_log_by_id(db, log_id)
        if not log:
            return False
        
        db.delete(log)
        db.commit()
        
        logger.info(f"Optimization log deleted: {log_id}")
        return True
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting optimization log: {e}")
        raise e