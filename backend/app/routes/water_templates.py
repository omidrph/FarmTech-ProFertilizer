# backend/app/routes/water_templates.py
"""مسیرهای قالب‌های آنالیز آب (Water Analysis Templates)"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User, WaterAnalysisTemplate
from app.schemas import (
    WaterAnalysisTemplateCreate,
    WaterAnalysisTemplateUpdate,
    WaterAnalysisTemplateResponse
)
import app.crud as crud
from app.security import get_current_user

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
water_templates_router = APIRouter(prefix="/water-templates", tags=["Water Templates"])

# ============================================================
# مسیرهای قالب‌های آنالیز آب
# ============================================================
@water_templates_router.post("/", response_model=WaterAnalysisTemplateResponse)
def create_water_template(
    template_data: WaterAnalysisTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد قالب آنالیز آب جدید"""
    try:
        template = crud.create_water_template(db, template_data, current_user.id)
        return template
    except Exception as e:
        logger.error(f"Error in create_water_template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد قالب: {str(e)}"
        )

@water_templates_router.get("/", response_model=List[WaterAnalysisTemplateResponse])
def get_water_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت قالب‌های آنالیز آب کاربر فعلی"""
    try:
        templates = crud.get_water_templates_by_user(db, current_user.id, skip, limit)
        return templates
    except Exception as e:
        logger.error(f"Error in get_water_templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت قالب‌ها: {str(e)}"
        )

@water_templates_router.get("/{template_id}", response_model=WaterAnalysisTemplateResponse)
def get_water_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت یک قالب آنالیز آب"""
    try:
        template = crud.get_water_template_by_id(db, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="قالب پیدا نشد"
            )
        if template.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این قالب ندارید"
            )
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_water_template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت قالب: {str(e)}"
        )

@water_templates_router.put("/{template_id}", response_model=WaterAnalysisTemplateResponse)
def update_water_template(
    template_id: int,
    template_data: WaterAnalysisTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی قالب آنالیز آب"""
    try:
        template = crud.get_water_template_by_id(db, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="قالب پیدا نشد"
            )
        if template.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این قالب ندارید"
            )
        
        updated_template = crud.update_water_template(db, template_id, template_data)
        return updated_template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_water_template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی قالب: {str(e)}"
        )

@water_templates_router.delete("/{template_id}")
def delete_water_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف قالب آنالیز آب"""
    try:
        template = crud.get_water_template_by_id(db, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="قالب پیدا نشد"
            )
        if template.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این قالب ندارید"
            )
        
        crud.delete_water_template(db, template_id)
        return {"message": "قالب با موفقیت حذف شد", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_water_template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در حذف قالب: {str(e)}"
        )