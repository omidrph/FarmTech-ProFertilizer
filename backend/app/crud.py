# backend/app/crud.py
"""عملیات پایه دیتابیس (CRUD) برای همه مدل‌ها"""

from typing import Optional, List, Dict, Any, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.models import User, Report, Fertilizer, WaterAnalysis, Calculation
from app.schemas import (
    UserCreate, UserUpdate,
    ReportCreate, ReportUpdate,
    FertilizerCreate, FertilizerUpdate,
    WaterAnalysisCreate, WaterAnalysisUpdate,
    CalculationCreate, CalculationUpdate
)
from app.security import get_password_hash


# ============================================================
# CRUD برای User (کاربر)
# ============================================================

def create_user(db: Session, user_data: UserCreate) -> User:
    """ایجاد کاربر جدید"""
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """دریافت کاربر با شناسه"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone(db: Session, phone_number: str) -> Optional[User]:
    """دریافت کاربر با شماره تلفن"""
    return db.query(User).filter(User.phone_number == phone_number).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """دریافت لیست کاربران"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """به‌روزرسانی اطلاعات کاربر"""
    db_user = get_user_by_id(db, user_id)
    
    if db_user is None:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """حذف کاربر"""
    db_user = get_user_by_id(db, user_id)
    
    if db_user is None:
        return False
    
    db.delete(db_user)
    db.commit()
    
    return True


# ============================================================
# CRUD برای Report (گزارش)
# ============================================================

def create_report(db: Session, report_data: ReportCreate, user_id: int) -> Report:
    """ایجاد گزارش جدید"""
    db_report = Report(
        user_id=user_id,
        **report_data.model_dump()
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report


def get_report_by_id(db: Session, report_id: int) -> Optional[Report]:
    """دریافت گزارش با شناسه"""
    return db.query(Report).filter(Report.id == report_id).first()


def get_reports_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Report]:
    """دریافت گزارش‌های یک کاربر"""
    return db.query(Report).filter(Report.user_id == user_id).offset(skip).limit(limit).all()


def update_report(db: Session, report_id: int, report_data: ReportUpdate) -> Optional[Report]:
    """به‌روزرسانی گزارش"""
    db_report = get_report_by_id(db, report_id)
    
    if db_report is None:
        return None
    
    update_data = report_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_report, key, value)
    
    db.commit()
    db.refresh(db_report)
    
    return db_report


def delete_report(db: Session, report_id: int) -> bool:
    """حذف گزارش"""
    db_report = get_report_by_id(db, report_id)
    
    if db_report is None:
        return False
    
    db.delete(db_report)
    db.commit()
    
    return True


# ============================================================
# CRUD برای Fertilizer (کود)
# ============================================================

def create_fertilizer(db: Session, fertilizer_data: FertilizerCreate, user_id: int) -> Fertilizer:
    """ایجاد کود جدید"""
    db_fertilizer = Fertilizer(
        user_id=user_id,
        **fertilizer_data.model_dump()
    )
    
    db.add(db_fertilizer)
    db.commit()
    db.refresh(db_fertilizer)
    
    return db_fertilizer


def get_fertilizer_by_id(db: Session, fertilizer_id: int) -> Optional[Fertilizer]:
    """دریافت کود با شناسه"""
    return db.query(Fertilizer).filter(Fertilizer.id == fertilizer_id).first()


def get_fertilizers_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Fertilizer]:
    """دریافت کودهای یک کاربر"""
    return db.query(Fertilizer).filter(Fertilizer.user_id == user_id).offset(skip).limit(limit).all()


def update_fertilizer(db: Session, fertilizer_id: int, fertilizer_data: FertilizerUpdate) -> Optional[Fertilizer]:
    """به‌روزرسانی کود"""
    db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    
    if db_fertilizer is None:
        return None
    
    update_data = fertilizer_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_fertilizer, key, value)
    
    db.commit()
    db.refresh(db_fertilizer)
    
    return db_fertilizer


def delete_fertilizer(db: Session, fertilizer_id: int) -> bool:
    """حذف کود"""
    db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    
    if db_fertilizer is None:
        return False
    
    db.delete(db_fertilizer)
    db.commit()
    
    return True


# ============================================================
# CRUD برای WaterAnalysis (آنالیز آب)
# ============================================================

def create_water_analysis(db: Session, analysis_data: WaterAnalysisCreate, report_id: int) -> WaterAnalysis:
    """ایجاد آنالیز آب"""
    db_analysis = WaterAnalysis(
        report_id=report_id,
        **analysis_data.model_dump()
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return db_analysis


def get_water_analysis_by_report(db: Session, report_id: int) -> Optional[WaterAnalysis]:
    """دریافت آنالیز آب بر اساس گزارش"""
    return db.query(WaterAnalysis).filter(WaterAnalysis.report_id == report_id).first()


def update_water_analysis(db: Session, analysis_id: int, analysis_data: WaterAnalysisUpdate) -> Optional[WaterAnalysis]:
    """به‌روزرسانی آنالیز آب"""
    db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
    
    if db_analysis is None:
        return None
    
    update_data = analysis_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_analysis, key, value)
    
    db.commit()
    db.refresh(db_analysis)
    
    return db_analysis


def delete_water_analysis(db: Session, analysis_id: int) -> bool:
    """حذف آنالیز آب"""
    db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
    
    if db_analysis is None:
        return False
    
    db.delete(db_analysis)
    db.commit()
    
    return True


# ============================================================
# CRUD برای Calculation (محاسبات)
# ============================================================

def create_calculation(db: Session, calc_data: CalculationCreate, report_id: int) -> Calculation:
    """ایجاد محاسبات جدید"""
    db_calculation = Calculation(
        report_id=report_id,
        **calc_data.model_dump()
    )
    
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    
    return db_calculation


def get_calculation_by_report(db: Session, report_id: int) -> Optional[Calculation]:
    """دریافت محاسبات بر اساس گزارش"""
    return db.query(Calculation).filter(Calculation.report_id == report_id).first()


def update_calculation(db: Session, calc_id: int, calc_data: CalculationUpdate) -> Optional[Calculation]:
    """به‌روزرسانی محاسبات"""
    db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    
    if db_calculation is None:
        return None
    
    update_data = calc_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_calculation, key, value)
    
    db.commit()
    db.refresh(db_calculation)
    
    return db_calculation


def delete_calculation(db: Session, calc_id: int) -> bool:
    """حذف محاسبات"""
    db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    
    if db_calculation is None:
        return False
    
    db.delete(db_calculation)
    db.commit()
    
    return True