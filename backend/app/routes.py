# backend/app/routes.py
"""همه مسیرهای API در یک فایل"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import timedelta

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import *
from app.crud import *
from app.security import (
    create_access_token,
    verify_password,
    get_current_user,
    get_current_active_user
)
from app.services import (
    calculate_ion_balance,
    calculate_final_solution,
    calculate_total_fertilizer_contribution,
    calculate_reservoir_data,
    generate_interpretation,
    format_decimal
)

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
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    ثبت‌نام کاربر جدید
    """
    # بررسی وجود کاربر با شماره تلفن
    existing_user = get_user_by_phone(db, user_data.phone_number)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این شماره تلفن قبلاً ثبت شده است"
        )
    
    # ایجاد کاربر
    user = create_user(db, user_data)
    
    return user


@auth_router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    ورود کاربر و دریافت توکن
    """
    # پیدا کردن کاربر
    user = get_user_by_phone(db, login_data.phone_number)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="شماره تلفن یا رمز عبور اشتباه است"
        )
    
    # بررسی رمز عبور
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
    
    # ایجاد توکن
    access_token = create_access_token(
        data={
            "sub": user.id,
            "phone": user.phone_number
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@auth_router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    دریافت اطلاعات کاربر فعلی
    """
    return current_user


# ============================================================
# مسیرهای کاربران (Users)
# ============================================================

@users_router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت لیست کاربران (فقط برای ادمین)
    """
    # TODO: اضافه کردن نقش ادمین
    return get_users(db, skip, limit)


@users_router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی اطلاعات کاربر فعلی
    """
    updated_user = update_user(db, current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر پیدا نشد"
        )
    
    return updated_user


# ============================================================
# مسیرهای گزارش‌ها (Reports)
# ============================================================

@reports_router.post("/", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد گزارش جدید
    """
    report = create_report(db, report_data, current_user.id)
    return report


@reports_router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت گزارش‌های کاربر فعلی
    """
    return get_reports_by_user(db, current_user.id, skip, limit)


@reports_router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت یک گزارش
    """
    report = get_report_by_id(db, report_id)
    
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


@reports_router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی گزارش
    """
    report = get_report_by_id(db, report_id)
    
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
    
    updated_report = update_report(db, report_id, report_data)
    return updated_report


@reports_router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف گزارش
    """
    report = get_report_by_id(db, report_id)
    
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
    
    delete_report(db, report_id)
    
    return {"message": "گزارش با موفقیت حذف شد", "success": True}


# ============================================================
# مسیرهای کودها (Fertilizers)
# ============================================================

@fertilizers_router.post("/", response_model=FertilizerResponse)
async def create_fertilizer(
    fertilizer_data: FertilizerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد کود جدید
    """
    fertilizer = create_fertilizer(db, fertilizer_data, current_user.id)
    return fertilizer


@fertilizers_router.get("/", response_model=List[FertilizerResponse])
async def get_fertilizers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت کودهای کاربر فعلی
    """
    return get_fertilizers_by_user(db, current_user.id, skip, limit)


@fertilizers_router.get("/{fertilizer_id}", response_model=FertilizerResponse)
async def get_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت یک کود
    """
    fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    
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


@fertilizers_router.put("/{fertilizer_id}", response_model=FertilizerResponse)
async def update_fertilizer(
    fertilizer_id: int,
    fertilizer_data: FertilizerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی کود
    """
    fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    
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
    
    updated_fertilizer = update_fertilizer(db, fertilizer_id, fertilizer_data)
    return updated_fertilizer


@fertilizers_router.delete("/{fertilizer_id}")
async def delete_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف کود
    """
    fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    
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
    
    delete_fertilizer(db, fertilizer_id)
    
    return {"message": "کود با موفقیت حذف شد", "success": True}


# ============================================================
# مسیرهای آنالیز آب (Water Analysis)
# ============================================================

@water_analysis_router.post("/{report_id}", response_model=WaterAnalysisResponse)
async def create_water_analysis(
    report_id: int,
    analysis_data: WaterAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد آنالیز آب برای یک گزارش
    """
    # بررسی وجود گزارش
    report = get_report_by_id(db, report_id)
    
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
    
    # بررسی اینکه آیا آنالیز قبلاً وجود دارد
    existing = get_water_analysis_by_report(db, report_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این گزارش قبلاً آنالیز آب دارد"
        )
    
    analysis = create_water_analysis(db, analysis_data, report_id)
    return analysis


@water_analysis_router.get("/{report_id}", response_model=WaterAnalysisResponse)
async def get_water_analysis(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت آنالیز آب یک گزارش
    """
    report = get_report_by_id(db, report_id)
    
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
    
    analysis = get_water_analysis_by_report(db, report_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="آنالیز آب برای این گزارش پیدا نشد"
        )
    
    return analysis


@water_analysis_router.put("/{analysis_id}", response_model=WaterAnalysisResponse)
async def update_water_analysis(
    analysis_id: int,
    analysis_data: WaterAnalysisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی آنالیز آب
    """
    analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="آنالیز آب پیدا نشد"
        )
    
    # بررسی دسترسی از طریق گزارش
    report = get_report_by_id(db, analysis.report_id)
    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما دسترسی به این آنالیز ندارید"
        )
    
    updated_analysis = update_water_analysis(db, analysis_id, analysis_data)
    return updated_analysis


# ============================================================
# مسیرهای محاسبات (Calculations)
# ============================================================

@calculations_router.post("/{report_id}", response_model=CalculationResponse)
async def create_calculation(
    report_id: int,
    calc_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد محاسبات برای یک گزارش
    """
    # بررسی وجود گزارش
    report = get_report_by_id(db, report_id)
    
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
    
    # بررسی اینکه آیا محاسبات قبلاً وجود دارد
    existing = get_calculation_by_report(db, report_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این گزارش قبلاً محاسبات دارد"
        )
    
    calculation = create_calculation(db, calc_data, report_id)
    return calculation


@calculations_router.get("/{report_id}", response_model=CalculationResponse)
async def get_calculation(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت محاسبات یک گزارش
    """
    report = get_report_by_id(db, report_id)
    
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
    
    calculation = get_calculation_by_report(db, report_id)
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محاسبات برای این گزارش پیدا نشد"
        )
    
    return calculation


@calculations_router.put("/{calc_id}", response_model=CalculationResponse)
async def update_calculation(
    calc_id: int,
    calc_data: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    به‌روزرسانی محاسبات
    """
    calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محاسبات پیدا نشد"
        )
    
    # بررسی دسترسی از طریق گزارش
    report = get_report_by_id(db, calculation.report_id)
    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما دسترسی به این محاسبات ندارید"
        )
    
    updated_calculation = update_calculation(db, calc_id, calc_data)
    return updated_calculation


# ============================================================
# مسیرهای محاسبات تخصصی
# ============================================================

@calculations_router.post("/{report_id}/calculate", response_model=InterpretationResponse)
async def calculate_and_interpret(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    انجام محاسبات کامل و تولید تفسیر برای یک گزارش
    """
    # دریافت گزارش
    report = get_report_by_id(db, report_id)
    
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
    
    # دریافت آنالیز آب
    water_analysis = get_water_analysis_by_report(db, report_id)
    
    if not water_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لطفاً ابتدا آنالیز آب را وارد کنید"
        )
    
    # دریافت محاسبات
    calculation = get_calculation_by_report(db, report_id)
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لطفاً ابتدا محاسبات را انجام دهید"
        )
    
    # انجام محاسبات
    target_values = calculation.target_values or {}
    final_values = calculation.final_values or {}
    water_data = {
        'water_salinity': water_analysis.water_salinity,
        'water_percentage': water_analysis.water_percentage,
        'wastewater_percentage': water_analysis.wastewater_percentage
    }
    
    # محاسبه تعادل یونی
    cation, anion, is_balanced = calculate_ion_balance(target_values)
    
    # تولید تفسیر
    interpretation = generate_interpretation(
        target_values=target_values,
        final_values=final_values,
        water_analysis=water_data,
        ion_balance=(cation, anion, is_balanced)
    )
    
    # ذخیره تفسیر
    calculation.interpretation = interpretation['summary']
    db.commit()
    
    return interpretation


# ============================================================
# افزودن همه Routerها به Router اصلی
# ============================================================

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(reports_router)
router.include_router(fertilizers_router)
router.include_router(water_analysis_router)
router.include_router(calculations_router)