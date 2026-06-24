# backend/app/routes.py
"""همه مسیرهای API - نسخه کامل و نهایی"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from app.config import settings
from app.database import get_db
from app.models import User, WaterAnalysis, Calculation
from app.schemas import *
import app.crud as crud
from app.security import (
    create_session_token,
    delete_session,
    get_current_user,
    get_current_active_user,
    get_password_hash,
    verify_password
)
from app.services import (
    calculate_ion_balance,
    calculate_final_solution,
    calculate_total_fertilizer_contribution,
    calculate_reservoir_data,
    generate_interpretation,
    format_decimal,
    convert_units,
    ELEMENTS
)

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ============================================================
# ایجاد Routerها
# ============================================================
router = APIRouter()

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
users_router = APIRouter(prefix="/users", tags=["Users"])
reports_router = APIRouter(prefix="/reports", tags=["Reports"])
fertilizers_router = APIRouter(prefix="/fertilizers", tags=["Fertilizers"])
water_analysis_router = APIRouter(prefix="/water-analysis", tags=["Water Analysis"])
calculations_router = APIRouter(prefix="/calculations", tags=["Calculations"])

# ============================================================
# مسیرهای احراز هویت (Auth)
# ============================================================
@auth_router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """ثبت‌نام کاربر جدید"""
    try:
        existing_user = crud.get_user_by_phone(db, user_data.phone_number)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این شماره تلفن قبلاً ثبت شده است"
            )
        user = crud.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in register: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ثبت‌نام: {str(e)}"
        )

@auth_router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """ورود کاربر و دریافت توکن تصادفی"""
    try:
        user = crud.get_user_by_phone(db, login_data.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="حساب کاربری غیرفعال است"
            )
        access_token = create_session_token(user.id, db, expires_in_hours=24)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ورود: {str(e)}"
        )

@auth_router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """خروج از حساب (غیرفعال کردن توکن)"""
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            if delete_session(token, db):
                return {"message": "خروج با موفقیت انجام شد", "success": True}
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="توکن پیدا نشد"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در خروج: {str(e)}"
        )

@auth_router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """دریافت اطلاعات کاربر فعلی"""
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error in get_me: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت اطلاعات کاربر: {str(e)}"
        )

@auth_router.get("/test")
def test_auth(
    current_user: User = Depends(get_current_user)
):
    """تست احراز هویت"""
    try:
        return {
            "message": "✅ احراز هویت موفق",
            "user": {
                "id": current_user.id,
                "phone": current_user.phone_number,
                "full_name": current_user.full_name
            }
        }
    except Exception as e:
        logger.error(f"Error in test_auth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تست احراز هویت: {str(e)}"
        )

# ============================================================
# مسیرهای کاربران (Users)
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

# ============================================================
# مسیرهای گزارش‌ها (Reports)
# ============================================================
@reports_router.post("/", response_model=ReportResponse)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد گزارش جدید"""
    try:
        logger.info(f"Creating report for user {current_user.id}: {report_data.report_name}")
        report = crud.create_report(db, report_data, current_user.id)
        logger.info(f"Report created successfully: {report.id}")
        return report
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد گزارش: {str(e)}"
        )

@reports_router.get("/", response_model=List[ReportResponse])
def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت گزارش‌های کاربر فعلی"""
    try:
        reports = crud.get_reports_by_user(db, current_user.id, skip, limit)
        logger.info(f"Found {len(reports)} reports for user {current_user.id}")
        return reports
    except Exception as e:
        logger.error(f"Error in get_reports: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت گزارش‌ها: {str(e)}"
        )

@reports_router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت یک گزارش"""
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
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت گزارش: {str(e)}"
        )

@reports_router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی گزارش"""
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
        updated_report = crud.update_report(db, report_id, report_data)
        return updated_report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی گزارش: {str(e)}"
        )

@reports_router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف گزارش"""
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
        crud.delete_report(db, report_id)
        return {"message": "گزارش با موفقیت حذف شد", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در حذف گزارش: {str(e)}"
        )

# ============================================================
# مسیرهای کودها (Fertilizers)
# ⚠️ ترتیب endpoint ها مهم است!
# endpoint های ثابت (بدون پارامتر) باید قبل از endpoint های پارامتری باشند
# ============================================================

# 🆕 endpoint ثابت - بارگذاری کودهای سیستمی (قبل از /{fertilizer_id})
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

# endpoint های پارامتری - باید بعد از endpoint های ثابت باشند
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
        system_fertilizers = db.query(
            __import__('app.models', fromlist=['Fertilizer']).Fertilizer
        ).filter(
            __import__('app.models', fromlist=['Fertilizer']).Fertilizer.is_system_default == True
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
            from app.models import Fertilizer as FertilizerModel
            new_fertilizer = FertilizerModel(
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

# ============================================================
# مسیرهای آنالیز آب (Water Analysis)
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

# ============================================================
# مسیرهای محاسبات (Calculations)
# ⚠️ IMPORTANT: ترتیب endpoint ها بسیار مهم است!
# endpoint های ثابت (بدون پارامتر) باید قبل از endpoint های پارامتری باشند
# ============================================================

# 🆕 APIهای محاسباتی جدید (ثابت - بدون پارامتر)
@calculations_router.get("/home-summary", response_model=HomeSummaryResponse)
def get_home_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🆕 دریافت خلاصه داشبورد - تمام محاسبات در بک‌اند انجام می‌شود"""
    try:
        logger.info(f"Getting home summary for user {current_user.id}")
        
        # دریافت آخرین گزارش کاربر
        reports = crud.get_reports_by_user(db, current_user.id, skip=0, limit=1)
        if not reports:
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز گزارشی ایجاد نشده است"
            )
        
        report = reports[0]
        water_analysis = crud.get_water_analysis_by_report(db, report.id)
        water_salinity = water_analysis.water_salinity if water_analysis else 0
        calculation = crud.get_calculation_by_report(db, report.id)
        
        if not calculation:
            return HomeSummaryResponse(
                has_data=False,
                message="هنوز محاسباتی انجام نشده است"
            )
        
        target_values = calculation.target_values or {}
        final_values = calculation.final_values or {}
        reservoir_data = calculation.reservoir_data or {}
        
        # محاسبه تعادل یونی از طریق service
        cation, anion, is_balanced = calculate_ion_balance(target_values, unit="ppm")
        
        # محاسبه آمار
        active_elements_count = sum(1 for v in target_values.values() if v and v > 0)
        total_elements = len(ELEMENTS)
        
        active_reservoirs_count = 0
        if reservoir_data.get('A') and len(reservoir_data['A']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('B') and len(reservoir_data['B']) > 0:
            active_reservoirs_count += 1
        if reservoir_data.get('C') and len(reservoir_data['C']) > 0:
            active_reservoirs_count += 1
        
        # محاسبه مجموع هزینه
        total_cost = 0
        if calculation.calc_rows:
            for row in calculation.calc_rows:
                total_cost += row.get('cost', 0)
        
        # محاسبه مجموع وزن مخازن
        total_reservoir_weight = 0
        for reservoir_items in reservoir_data.values():
            if isinstance(reservoir_items, list):
                for item in reservoir_items:
                    total_reservoir_weight += item.get('amount', 0)
        
        # تولید توصیه‌ها در بک‌اند
        recommendations = []
        
        if not is_balanced:
            diff = abs(cation - anion)
            recommendations.append({
                'type': 'danger',
                'title': 'عدم تعادل یونی',
                'description': f'اختلاف کاتیون و آنیون {diff:.2f} meq/L است.'
            })
        
        deficient_elements = []
        excessive_elements = []
        for element in ELEMENTS:
            target = target_values.get(element, 0)
            actual = final_values.get(element, 0)
            if target == 0:
                continue
            percent = (actual / target) * 100 if target > 0 else 0
            if percent < 70:
                deficient_elements.append(element)
            elif percent > 130:
                excessive_elements.append(element)
        
        if deficient_elements:
            recommendations.append({
                'type': 'warning',
                'title': f'{len(deficient_elements)} عنصر با کمبود شدید',
                'description': f'عناصر {", ".join(deficient_elements[:3])}{" و..." if len(deficient_elements) > 3 else ""} کمتر از 70% مقدار هدف هستند.'
            })
        
        if excessive_elements:
            recommendations.append({
                'type': 'warning',
                'title': f'{len(excessive_elements)} عنصر با بیش‌بود',
                'description': f'عناصر {", ".join(excessive_elements[:3])}{" و..." if len(excessive_elements) > 3 else ""} بیشتر از 130% مقدار هدف هستند.'
            })
        
        if water_salinity > 2.5:
            recommendations.append({
                'type': 'danger',
                'title': 'شوری آب بالا',
                'description': f'شوری آب {water_salinity:.2f} dS/m است. استفاده از منابع آب با کیفیت‌تر توصیه می‌شود.'
            })
        elif water_salinity > 1.5:
            recommendations.append({
                'type': 'warning',
                'title': 'شوری آب متوسط',
                'description': f'شوری آب {water_salinity:.2f} dS/m است. مراقب تجمع عناصر سمی باشید.'
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'success',
                'title': 'وضعیت مطلوب',
                'description': 'تمام پارامترها در محدوده مناسب قرار دارند.'
            })
        
        # آماده‌سازی داده عناصر برای جدول
        elements_data = []
        for element in ELEMENTS:
            target = target_values.get(element, 0)
            actual = final_values.get(element, 0)
            diff = actual - target
            percent = (actual / target * 100) if target > 0 else 0
            elements_data.append({
                'element': element,
                'target': target,
                'actual': actual,
                'difference': diff,
                'progress_percent': min(percent, 150)
            })
        
        return HomeSummaryResponse(
            has_data=True,
            ion_balance={
                'cation': cation,
                'anion': anion,
                'is_balanced': is_balanced,
                'message': 'تعادل یونی برقرار است ✅' if is_balanced else 'تعادل یونی برقرار نیست ⚠️'
            },
            active_elements_count=active_elements_count,
            total_elements=total_elements,
            active_reservoirs_count=active_reservoirs_count,
            total_cost=total_cost,
            total_reservoir_weight=total_reservoir_weight,
            reservoir_data=reservoir_data,
            elements_data=elements_data,
            recommendations=recommendations,
            water_salinity=water_salinity
        )
    except Exception as e:
        logger.error(f"Error in get_home_summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت خلاصه: {str(e)}"
        )

@calculations_router.post("/calculate-ion-balance", response_model=IonBalanceResponse)
def api_calculate_ion_balance(
    data: IonBalanceRequest,
    current_user: User = Depends(get_current_user)
):
    """🆕 محاسبه تعادل یونی"""
    try:
        cation, anion, is_balanced = calculate_ion_balance(data.elements, unit=data.unit)
        message = "تعادل یونی برقرار است ✅" if is_balanced else "تعادل یونی برقرار نیست ⚠️"
        return IonBalanceResponse(
            cation=cation,
            anion=anion,
            is_balanced=is_balanced,
            message=message
        )
    except Exception as e:
        logger.error(f"Error in calculate_ion_balance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه تعادل یونی: {str(e)}"
        )

@calculations_router.post("/calculate-final-solution", response_model=FinalSolutionResponse)
def api_calculate_final_solution(
    data: FinalSolutionRequest,
    current_user: User = Depends(get_current_user)
):
    """🆕 محاسبه محلول نهایی"""
    try:
        final_values = calculate_final_solution(
            target_values=data.target_values,
            water_values=data.water_values,
            fertilizer_contributions=data.fertilizer_contributions
        )
        cation, anion, is_balanced = calculate_ion_balance(final_values, unit="ppm")
        return FinalSolutionResponse(
            final_values=final_values,
            ion_balance=IonBalanceResponse(
                cation=cation,
                anion=anion,
                is_balanced=is_balanced,
                message="متعادل" if is_balanced else "نامتعادل"
            )
        )
    except Exception as e:
        logger.error(f"Error in calculate_final_solution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه محلول نهایی: {str(e)}"
        )

@calculations_router.post("/calculate-reservoir", response_model=ReservoirResponse)
def api_calculate_reservoir(
    data: ReservoirRequest,
    current_user: User = Depends(get_current_user)
):
    """🆕 محاسبه توزیع مخازن"""
    try:
        reservoir_data = calculate_reservoir_data(data.fertilizers)
        totals = {
            'A': sum(item['amount'] for item in reservoir_data.get('A', [])),
            'B': sum(item['amount'] for item in reservoir_data.get('B', [])),
            'C': sum(item['amount'] for item in reservoir_data.get('C', []))
        }
        return ReservoirResponse(
            reservoir_data=reservoir_data,
            totals=totals
        )
    except Exception as e:
        logger.error(f"Error in calculate_reservoir: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در محاسبه مخازن: {str(e)}"
        )

@calculations_router.post("/convert-unit", response_model=UnitConversionResponse)
def api_convert_unit(
    data: UnitConversionRequest,
    current_user: User = Depends(get_current_user)
):
    """🆕 تبدیل واحد"""
    try:
        converted_value = convert_units(
            value=data.value,
            from_unit=data.from_unit,
            to_unit=data.to_unit,
            element=data.element
        )
        return UnitConversionResponse(
            original_value=data.value,
            converted_value=converted_value,
            from_unit=data.from_unit,
            to_unit=data.to_unit,
            element=data.element
        )
    except Exception as e:
        logger.error(f"Error in convert_unit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تبدیل واحد: {str(e)}"
        )

# ⚠️ endpoint های پارامتری (با پارامتر) - باید بعد از endpoint های ثابت باشند
@calculations_router.post("/{report_id}", response_model=CalculationResponse)
def create_calculation(
    report_id: int,
    calc_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد محاسبات برای یک گزارش"""
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
        existing = crud.get_calculation_by_report(db, report_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این گزارش قبلاً محاسبات دارد"
            )
        calculation = crud.create_calculation(db, calc_data, report_id)
        return calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد محاسبات: {str(e)}"
        )

@calculations_router.get("/{report_id}", response_model=CalculationResponse)
def get_calculation(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت محاسبات یک گزارش"""
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
        calculation = crud.get_calculation_by_report(db, report_id)
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="محاسبات برای این گزارش پیدا نشد"
            )
        return calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت محاسبات: {str(e)}"
        )

@calculations_router.put("/{calc_id}", response_model=CalculationResponse)
def update_calculation(
    calc_id: int,
    calc_data: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی محاسبات"""
    try:
        calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="محاسبات پیدا نشد"
            )
        report = crud.get_report_by_id(db, calculation.report_id)
        if report.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این محاسبات ندارید"
            )
        updated_calculation = crud.update_calculation(db, calc_id, calc_data)
        return updated_calculation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی محاسبات: {str(e)}"
        )

@calculations_router.post("/{report_id}/calculate", response_model=InterpretationResponse)
def calculate_and_interpret(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تولید تفسیر کامل"""
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
        water_analysis = crud.get_water_analysis_by_report(db, report_id)
        if not water_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="لطفاً ابتدا آنالیز آب را وارد کنید"
            )
        calculation = crud.get_calculation_by_report(db, report_id)
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="لطفاً ابتدا محاسبات را انجام دهید"
            )
        target_values = calculation.target_values or {}
        final_values = calculation.final_values or {}
        water_data = {
            'water_salinity': water_analysis.water_salinity,
            'water_percentage': water_analysis.water_percentage,
            'wastewater_percentage': water_analysis.wastewater_percentage
        }
        cation, anion, is_balanced = calculate_ion_balance(target_values)
        interpretation = generate_interpretation(
            target_values=target_values,
            final_values=final_values,
            water_analysis=water_data,
            ion_balance=(cation, anion, is_balanced)
        )
        calculation.interpretation = interpretation['summary']
        db.commit()
        return interpretation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in calculate_and_interpret: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تولید تفسیر: {str(e)}"
        )

# ============================================================
# افزودن همه Routerها به Router اصلی
# ============================================================
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(reports_router)
router.include_router(fertilizers_router)
router.include_router(water_analysis_router)
router.include_router(calculations_router)