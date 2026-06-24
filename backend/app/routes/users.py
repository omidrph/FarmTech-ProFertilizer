# backend/app/routes/users.py
"""مسیرهای کاربران (Users)"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User
from app.schemas import UserUpdate, UserResponse
import app.crud as crud
from app.security import get_current_user

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
users_router = APIRouter(prefix="/users", tags=["Users"])

# ============================================================
# مسیرهای کاربران
# ============================================================

@users_router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت لیست کاربران"""
    try:
        return crud.get_users(db, skip, limit)
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت کاربران: {str(e)}"
        )

@users_router.put("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی اطلاعات کاربر فعلی"""
    try:
        updated_user = crud.update_user(db, current_user.id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کاربر پیدا نشد"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_me: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی کاربر: {str(e)}"
        )