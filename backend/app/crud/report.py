# backend/app/crud/report.py
"""
عملیات CRUD برای مدل Report (گزارش)
"""

from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from app.models import Report
from app.schemas import ReportCreate, ReportUpdate

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای Report (گزارش)
# ============================================================

def create_report(db: Session, report_data: ReportCreate, user_id: int) -> Report:
    """ایجاد گزارش جدید"""
    try:
        db_report = Report(
            user_id=user_id,
            report_name=report_data.report_name,
            plant_name=report_data.plant_name,
            season=report_data.season,
            growth_stage=report_data.growth_stage,
            report_date=report_data.report_date
        )
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        logger.info(f"Report created: {db_report.id} for user {user_id}")
        return db_report
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating report: {e}")
        raise e


def get_report_by_id(db: Session, report_id: int) -> Optional[Report]:
    """دریافت گزارش با شناسه"""
    try:
        return db.query(Report).filter(Report.id == report_id).first()
    except Exception as e:
        logger.error(f"Error getting report by id: {e}")
        return None


def get_reports_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Report]:
    """دریافت گزارش‌های یک کاربر"""
    try:
        return db.query(Report).filter(Report.user_id == user_id).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting reports by user: {e}")
        return []


def update_report(db: Session, report_id: int, report_data: ReportUpdate) -> Optional[Report]:
    """به‌روزرسانی گزارش"""
    try:
        db_report = get_report_by_id(db, report_id)
        
        if db_report is None:
            return None
        
        update_data = report_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_report, key, value)
        
        db.commit()
        db.refresh(db_report)
        
        logger.info(f"Report updated: {report_id}")
        return db_report
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating report: {e}")
        raise e


def delete_report(db: Session, report_id: int) -> bool:
    """حذف گزارش"""
    try:
        db_report = get_report_by_id(db, report_id)
        
        if db_report is None:
            return False
        
        db.delete(db_report)
        db.commit()
        
        logger.info(f"Report deleted: {report_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting report: {e}")
        raise e