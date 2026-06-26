# backend/app/routes/fertilizers.py
"""مسیرهای کودها (Fertilizers)"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models import User, Fertilizer
from app.schemas import FertilizerCreate, FertilizerUpdate, FertilizerResponse
import app.crud as crud
from app.security import get_current_user

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
fertilizers_router = APIRouter(prefix="/fertilizers", tags=["Fertilizers"])


# ============================================================
# 🆕 APIهای مربوط به کودهای سیستمی
# ============================================================

@fertilizers_router.get("/system", response_model=List[FertilizerResponse])
def get_system_fertilizers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت لیست کودهای سیستمی
    
    این کودها فقط برای نمایش و کپی کردن هستند.
    کاربر نمی‌تواند آنها را ویرایش یا حذف کند.
    """
    try:
        fertilizers = crud.get_system_fertilizers(db, skip, limit)
        logger.info(f"Found {len(fertilizers)} system fertilizers")
        return fertilizers
    except Exception as e:
        logger.error(f"Error in get_system_fertilizers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت کودهای سیستمی: {str(e)}"
        )


@fertilizers_router.post("/system/copy-all")
def copy_all_system_fertilizers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    کپی کردن همه کودهای سیستمی به عنوان کودهای شخصی کاربر
    
    این عملیات همه کودهای سیستمی را به بخش شخصی کاربر اضافه می‌کند.
    اگر کاربر قبلاً بعضی از آنها را کپی کرده باشد، از کپی مجدد جلوگیری می‌شود.
    """
    try:
        stats = crud.copy_all_system_fertilizers_to_user(db, current_user.id)
        
        return {
            "message": "کودهای سیستمی با موفقیت به بخش شخصی شما اضافه شدند",
            "stats": stats,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in copy_all_system_fertilizers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در کپی کودهای سیستمی: {str(e)}"
        )


@fertilizers_router.post("/system/{system_fertilizer_id}/copy")
def copy_system_fertilizer(
    system_fertilizer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    کپی کردن یک کود سیستمی خاص به عنوان کود شخصی کاربر
    
    Args:
        system_fertilizer_id: شناسه کود سیستمی
    """
    try:
        # بررسی وجود کود سیستمی
        system_fert = crud.get_fertilizer_by_id(db, system_fertilizer_id)
        if not system_fert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود سیستمی پیدا نشد"
            )
        
        if not system_fert.is_system_default:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این کود یک کود سیستمی نیست"
            )
        
        # کپی کردن
        new_fertilizer = crud.copy_system_fertilizer_to_user(db, system_fertilizer_id, current_user.id)
        
        if not new_fertilizer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="خطا در کپی کود سیستمی"
            )
        
        return {
            "message": f"کود '{system_fert.name}' با موفقیت به بخش شخصی شما اضافه شد",
            "fertilizer": new_fertilizer,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in copy_system_fertilizer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در کپی کود سیستمی: {str(e)}"
        )


@fertilizers_router.get("/check-system-copy-status")
def check_system_copy_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    بررسی وضعیت کپی کودهای سیستمی برای کاربر
    
    Returns:
        {
            "has_system_fertilizers": bool,
            "has_copied_system_fertilizers": bool,
            "system_count": int,
            "copied_count": int
        }
    """
    try:
        # دریافت تعداد کودهای سیستمی
        system_fertilizers = crud.get_system_fertilizers(db)
        system_count = len(system_fertilizers)
        
        # دریافت تعداد کودهای کپی شده توسط کاربر
        copied_count = db.query(Fertilizer).filter(
            Fertilizer.user_id == current_user.id,
            Fertilizer.source_system_id.isnot(None)
        ).count()
        
        return {
            "has_system_fertilizers": system_count > 0,
            "has_copied_system_fertilizers": copied_count > 0,
            "system_count": system_count,
            "copied_count": copied_count
        }
    except Exception as e:
        logger.error(f"Error in check_system_copy_status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بررسی وضعیت: {str(e)}"
        )


# ============================================================
# APIهای مربوط به کودهای شخصی کاربر
# ============================================================

@fertilizers_router.post("/", response_model=FertilizerResponse)
def create_fertilizer(
    fertilizer_data: FertilizerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد کود شخصی جدید"""
    try:
        # جلوگیری از ایجاد مستقیم کود سیستمی توسط کاربر
        if fertilizer_data.is_system_default:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="شما نمی‌توانید به طور مستقیم کود سیستمی ایجاد کنید"
            )
        
        logger.info(f"Creating fertilizer for user {current_user.id}: {fertilizer_data.name}")
        fertilizer = crud.create_fertilizer(db, fertilizer_data, current_user.id)
        
        if fertilizer is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="خطا در ایجاد کود"
            )
        
        logger.info(f"Fertilizer created successfully: ID={fertilizer.id}, Name={fertilizer.name}")
        return fertilizer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating fertilizer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد کود: {str(e)}"
        )


@fertilizers_router.get("/", response_model=List[FertilizerResponse])
def get_fertilizers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_system: bool = Query(True, description="آیا کودهای سیستمی نیز نمایش داده شوند؟"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت کودهای کاربر + کودهای سیستمی (اختیاری)
    
    Args:
        include_system: اگر True باشد، کودهای سیستمی نیز در لیست نمایش داده می‌شوند
    """
    try:
        # دریافت کودهای شخصی کاربر
        user_fertilizers = crud.get_fertilizers_by_user(db, current_user.id, skip, limit)
        
        result = list(user_fertilizers)
        
        # اگر کاربر درخواست نمایش کودهای سیستمی را داشته باشد
        if include_system:
            system_fertilizers = crud.get_system_fertilizers(db, skip, limit)
            result = result + system_fertilizers
        
        logger.info(f"Found {len(result)} fertilizers for user {current_user.id}")
        return result
    except Exception as e:
        logger.error(f"Error in get_fertilizers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت کودها: {str(e)}"
        )


@fertilizers_router.get("/{fertilizer_id}", response_model=FertilizerResponse)
def get_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت یک کود با شناسه"""
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        
        # اگر کود سیستمی است، همه کاربران می‌توانند آن را ببینند
        if fertilizer.is_system_default and fertilizer.user_id is None:
            return fertilizer
        
        # اگر کود شخصی است، فقط خود کاربر می‌تواند آن را ببیند
        if fertilizer.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این کود ندارید"
            )
        
        return fertilizer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_fertilizer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت کود: {str(e)}"
        )


@fertilizers_router.put("/{fertilizer_id}", response_model=FertilizerResponse)
def update_fertilizer(
    fertilizer_id: int,
    fertilizer_data: FertilizerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی کود
    
    توجه: کودهای سیستمی قابل ویرایش نیستند.
    برای تغییر یک کود سیستمی، ابتدا آن را کپی کرده و سپس ویرایش کنید.
    """
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        
        # کودهای سیستمی قابل ویرایش نیستند
        if fertilizer.is_system_default and fertilizer.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="کودهای سیستمی قابل ویرایش نیستند. لطفاً ابتدا آن را کپی کنید."
            )
        
        # فقط کاربر صاحب کود می‌تواند آن را ویرایش کند
        if fertilizer.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این کود ندارید"
            )
        
        # جلوگیری از تغییر is_system_default توسط کاربر
        if fertilizer_data.is_system_default is not None:
            logger.warning(f"User {current_user.id} tried to change is_system_default of fertilizer {fertilizer_id}")
            fertilizer_data.is_system_default = False
        
        updated_fertilizer = crud.update_fertilizer(db, fertilizer_id, fertilizer_data)
        return updated_fertilizer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_fertilizer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی کود: {str(e)}"
        )


@fertilizers_router.delete("/{fertilizer_id}")
def delete_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف کود شخصی"""
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        
        # کودهای سیستمی قابل حذف نیستند
        if fertilizer.is_system_default and fertilizer.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="کودهای سیستمی قابل حذف نیستند"
            )
        
        # فقط کاربر صاحب کود می‌تواند آن را حذف کند
        if fertilizer.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این کود ندارید"
            )
        
        crud.delete_fertilizer(db, fertilizer_id)
        return {"message": "کود با موفقیت حذف شد", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_fertilizer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در حذف کود: {str(e)}"
        )