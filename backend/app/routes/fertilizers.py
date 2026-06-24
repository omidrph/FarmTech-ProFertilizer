# backend/app/routes/fertilizers.py
"""مسیرهای کودها (Fertilizers)"""
from typing import List
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
# 🆕 endpoint ثابت - بارگذاری کودهای سیستمی
# ⚠️ باید قبل از endpoint های پارامتری باشد
# ============================================================
@fertilizers_router.post("/load-system-fertilizers")
def load_system_fertilizers_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🆕 بارگذاری کودهای سیستمی از seed - برای شروع سریع کاربر"""
    try:
        from app.seeds.fertilizer_seeds import seed_system_fertilizers, get_system_fertilizers_count
        
        # بررسی تعداد کودهای سیستمی موجود
        count = get_system_fertilizers_count(db)
        
        if count > 0:
            return {
                "message": f"کودهای سیستمی قبلاً بارگذاری شده‌اند ({count} مورد)",
                "count": count,
                "already_loaded": True,
                "success": True
            }
        
        # اجرای seed
        logger.info(f"🌱 کاربر {current_user.id} در حال بارگذاری کودهای سیستمی...")
        stats = seed_system_fertilizers(db)
        
        return {
            "message": "کودهای سیستمی با موفقیت بارگذاری شدند",
            "stats": stats,
            "already_loaded": False,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error loading system fertilizers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بارگذاری کودهای سیستمی: {str(e)}"
        )

# ============================================================
# endpoint های پارامتری
# ============================================================

@fertilizers_router.post("/", response_model=FertilizerResponse)
def create_fertilizer(
    fertilizer_data: FertilizerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد کود جدید"""
    try:
        logger.info(f"Creating fertilizer for user {current_user.id}: {fertilizer_data.name}")
        fertilizer = crud.create_fertilizer(db, fertilizer_data, current_user.id)
        if fertilizer is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="خطا در ایجاد کود: نتیجه None است"
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت کودهای کاربر فعلی + کودهای سیستمی"""
    try:
        # دریافت کودهای کاربر
        user_fertilizers = crud.get_fertilizers_by_user(db, current_user.id, skip, limit)
        
        # دریافت کودهای سیستمی (user_id = None)
        system_fertilizers = db.query(Fertilizer).filter(
            Fertilizer.is_system_default == True
        ).all()
        
        # ترکیب لیست‌ها (کودهای کاربر + کودهای سیستمی)
        all_fertilizers = user_fertilizers + system_fertilizers
        
        logger.info(f"Found {len(all_fertilizers)} fertilizers for user {current_user.id} (user: {len(user_fertilizers)}, system: {len(system_fertilizers)})")
        return all_fertilizers
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
    """دریافت یک کود"""
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        # کاربر می‌تواند کود سیستمی یا کود خودش را ببیند
        if fertilizer.user_id is not None and fertilizer.user_id != current_user.id:
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
    """به‌روزرسانی کود - کاربر می‌تواند کود سیستمی را برای خودش شخصی‌سازی کند"""
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        # اگر کود سیستمی است، یک کپی برای کاربر بساز
        if fertilizer.is_system_default and fertilizer.user_id is None:
            # ایجاد کپی از کود سیستمی برای کاربر
            new_fertilizer = Fertilizer(
                user_id=current_user.id,
                name=fertilizer.name,
                brand=fertilizer.brand,
                category=fertilizer.category,
                form=fertilizer.form,
                price_per_kg=fertilizer.price_per_kg,
                elements=fertilizer.elements,
                is_acid=fertilizer.is_acid,
                acid_type=fertilizer.acid_type,
                description=fertilizer.description,
                is_system_default=False,
                solubility=fertilizer.solubility,
                ph_level=fertilizer.ph_level,
                application_method=fertilizer.application_method,
                packaging=fertilizer.packaging,
                registration_code=fertilizer.registration_code,
                npk_ratio=fertilizer.npk_ratio,
                organic_matter=fertilizer.organic_matter,
                chelating_agent=fertilizer.chelating_agent
            )
            db.add(new_fertilizer)
            db.commit()
            db.refresh(new_fertilizer)
            
            # حالا تغییرات را روی کپی اعمال کن
            update_data = fertilizer_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(new_fertilizer, key, value)
            db.commit()
            db.refresh(new_fertilizer)
            logger.info(f"Fertilizer {fertilizer_id} copied and updated as user fertilizer: {new_fertilizer.id}")
            return new_fertilizer
        
        # اگر کود متعلق به کاربر است، مستقیم به‌روزرسانی کن
        if fertilizer.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این کود ندارید"
            )
        
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
    """حذف کود - فقط کودهای کاربر قابل حذف است، کود سیستمی فقط مخفی می‌شود"""
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
        
        # اگر کود سیستمی است، آن را حذف نکن (فقط اگر کپی کاربر است)
        if fertilizer.is_system_default and fertilizer.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="کودهای سیستمی قابل حذف نیستند. می‌توانید آن‌ها را ویرایش کنید تا یک کپی شخصی بسازید."
            )
        
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