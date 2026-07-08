# backend/app/crud/water_analysis.py
"""
عملیات CRUD برای مدل WaterAnalysis (آنالیز آب)
"""

from typing import Optional
from sqlalchemy.orm import Session
import logging

from app.models import WaterAnalysis
from app.schemas import WaterAnalysisCreate, WaterAnalysisUpdate

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای WaterAnalysis (آنالیز آب)
# ============================================================

def create_water_analysis(db: Session, analysis_data: WaterAnalysisCreate, report_id: int) -> WaterAnalysis:
    """ایجاد آنالیز آب"""
    try:
        db_analysis = WaterAnalysis(
            report_id=report_id,
            water_percentage=analysis_data.water_percentage,
            wastewater_percentage=analysis_data.wastewater_percentage,
            water_salinity=analysis_data.water_salinity,
            wastewater_values=analysis_data.wastewater_values or {},
            water_values=analysis_data.water_values or {}
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        logger.info(f"Water analysis created: {db_analysis.id} for report {report_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating water analysis: {e}")
        raise e


def get_water_analysis_by_report(db: Session, report_id: int) -> Optional[WaterAnalysis]:
    """دریافت آنالیز آب بر اساس گزارش"""
    try:
        return db.query(WaterAnalysis).filter(WaterAnalysis.report_id == report_id).first()
    except Exception as e:
        logger.error(f"Error getting water analysis by report: {e}")
        return None


def update_water_analysis(db: Session, analysis_id: int, analysis_data: WaterAnalysisUpdate) -> Optional[WaterAnalysis]:
    """به‌روزرسانی آنالیز آب"""
    try:
        db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
        
        if db_analysis is None:
            return None
        
        update_data = analysis_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_analysis, key, value)
        
        db.commit()
        db.refresh(db_analysis)
        
        logger.info(f"Water analysis updated: {analysis_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating water analysis: {e}")
        raise e


def delete_water_analysis(db: Session, analysis_id: int) -> bool:
    """حذف آنالیز آب"""
    try:
        db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
        
        if db_analysis is None:
            return False
        
        db.delete(db_analysis)
        db.commit()
        
        logger.info(f"Water analysis deleted: {analysis_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting water analysis: {e}")
        raise e