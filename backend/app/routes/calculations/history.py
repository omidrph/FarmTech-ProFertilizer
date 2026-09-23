# backend/app/routes/calculations/history.py
"""
مسیر دریافت تاریخچه بهینه‌سازی
"""

import logging
from typing import Optional, List
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import OptimizationLogResponse
import app.crud as crud
from app.security import get_current_user

logger = logging.getLogger(__name__)


def get_optimization_history_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    report_id: Optional[int] = Query(None, description="فیلتر بر اساس گزارش"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت تاریخچه بهینه‌سازی‌های انجام شده توسط کاربر"""
    try:
        logs = crud.get_optimization_history(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            report_id=report_id
        )
        
        return logs
    except Exception as e:
        logger.error(f"Error in get_optimization_history_endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت تاریخچه: {str(e)}"
        )



def count_optimization_history_endpoint(
    report_id: Optional[int] = Query(None, description="فیلتر بر اساس گزارش"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تعداد دقیق محاسبات/بهینه‌سازی‌های کاربر."""
    try:
        return {
            "count": crud.count_optimization_history(
                db=db,
                user_id=current_user.id,
                report_id=report_id
            )
        }
    except Exception as e:
        logger.error(f"Error in count_optimization_history_endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت تعداد محاسبات: {str(e)}"
        )
