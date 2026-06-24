# backend/app/routes/water_analysis.py
"""مسیرهای آنالیز آب (Water Analysis)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User, WaterAnalysis
from app.schemas import WaterAnalysisCreate, WaterAnalysisUpdate, WaterAnalysisResponse
import app.crud as crud
from app.security import get_current_user

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
water_analysis_router = APIRouter(prefix="/water-analysis", tags=["Water Analysis"])

# ============================================================
# مسیرهای آنالیز آب
# ============================================================

@water_analysis_router.post("/{report_id}", response_model=WaterAnalysisResponse)
def create_water_analysis(
    report_id: int,
    analysis_data: WaterAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد آنالیز آب برای یک گزارش"""
    try:
        report = crud.get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="گزارش پیدا نشد"
            )
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این گزارش ندارید"
            )
        existing = crud.get_water_analysis_by_report(db, report_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این گزارش قبلاً آنالیز آب دارد"
            )
        analysis = crud.create_water_analysis(db, analysis_data, report_id)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_water_analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد آنالیز آب: {str(e)}"
        )

@water_analysis_router.get("/{report_id}", response_model=WaterAnalysisResponse)
def get_water_analysis(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت آنالیز آب یک گزارش"""
    try:
        report = crud.get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="گزارش پیدا نشد"
            )
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این گزارش ندارید"
            )
        analysis = crud.get_water_analysis_by_report(db, report_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="آنالیز آب برای این گزارش پیدا نشد"
            )
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_water_analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت آنالیز آب: {str(e)}"
        )

@water_analysis_router.put("/{analysis_id}", response_model=WaterAnalysisResponse)
def update_water_analysis(
    analysis_id: int,
    analysis_data: WaterAnalysisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی آنالیز آب"""
    try:
        analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="آنالیز آب پیدا نشد"
            )
        report = crud.get_report_by_id(db, analysis.report_id)
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این آنالیز ندارید"
            )
        updated_analysis = crud.update_water_analysis(db, analysis_id, analysis_data)
        return updated_analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_water_analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی آنالیز آب: {str(e)}"
        )