# backend/app/routes.py
"""همه مسیرهای API در یک فایل"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from app.config import settings
from app.database import get_db
# اصلاح: اضافه کردن WaterAnalysis و Calculation که در db.query استفاده شده‌اند
from app.models import User, WaterAnalysis, Calculation 
from app.schemas import *
# اصلاح: تغییر از from app.crud import * به import app.crud as crud
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
    format_decimal
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
# ============================================================
@fertilizers_router.post("/", response_model=FertilizerResponse)
def create_fertilizer(
    fertilizer_data: FertilizerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Creating fertilizer for user {current_user.id}: {fertilizer_data.name}")
        # فراخوانی صحیح تابع crud با پیشوند crud.
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
    try:
        fertilizers = crud.get_fertilizers_by_user(db, current_user.id, skip, limit)
        logger.info(f"Found {len(fertilizers)} fertilizers for user {current_user.id}")
        return fertilizers
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
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
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
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
            )
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
    try:
        fertilizer = crud.get_fertilizer_by_id(db, fertilizer_id)
        if not fertilizer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کود پیدا نشد"
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
    try:
        # استفاده از db.query به جای crud چون تابع get_by_id در crud وجود ندارد
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
# ============================================================
@calculations_router.post("/{report_id}", response_model=CalculationResponse)
def create_calculation(
    report_id: int,
    calc_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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