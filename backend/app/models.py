# backend/app/models.py
"""همه مدل‌های دیتابیس (SQLAlchemy) - نسخه اصلاح شده"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from app.database import Base


# ============================================================
# مدل User (کاربر)
# ============================================================
class User(Base):
    """مدل کاربران سیستم"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    fertilizers = relationship("Fertilizer", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def full_name(self) -> str:
        """نام کامل کاربر"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.phone_number}>"


# ============================================================
# مدل UserSession (نشست کاربر - توکن تصادفی)
# ============================================================
class UserSession(Base):
    """مدل نشست‌های کاربر (توکن‌های تصادفی)"""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # ===== روابط =====
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession {self.user_id} - {self.token[:10]}...>"


# ============================================================
# مدل Report (گزارش)
# ============================================================
class Report(Base):
    """مدل گزارش‌های تغذیه"""
    
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_name = Column(String(100), nullable=True)
    plant_name = Column(String(50), nullable=True)
    season = Column(String(20), nullable=True)
    growth_stage = Column(String(50), nullable=True)
    report_date = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    user = relationship("User", back_populates="reports")
    water_analysis = relationship("WaterAnalysis", back_populates="report", uselist=False, cascade="all, delete-orphan")
    calculation = relationship("Calculation", back_populates="report", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Report {self.id} - {self.report_name}>"


# ============================================================
# مدل Fertilizer (کود) - اصلاح شده با فیلدهای جدید
# ============================================================
class Fertilizer(Base):
    """مدل کودها و اسیدها - نسخه کامل"""
    
    __tablename__ = "fertilizers"
    
    # ===== فیلدهای اصلی =====
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # ✅ nullable شد
    name = Column(String(100), nullable=False)  # ✅ تنها فیلد اجباری
    
    # ===== فیلدهای مالی =====
    price_per_kg = Column(Float, default=0.0)
    
    # ===== فیلدهای عناصر =====
    elements = Column(JSON, nullable=True)  # {"N-NO3": 15.5, "Ca": 19, ...}
    
    # ===== فیلدهای اسیدی =====
    is_acid = Column(Boolean, default=False)
    acid_type = Column(String(10), nullable=True)  # H3PO4, HNO3, H2SO4
    
    # ===== 🆕 فیلدهای جدید - همه اختیاری =====
    is_system_default = Column(Boolean, default=False)  # آیا کود سیستمی است؟
    brand = Column(String(100), nullable=True)  # برند/شرکت (مثلاً: اطلس، رازاک شیمی)
    category = Column(String(50), nullable=True)  # دسته‌بندی (NPK, کلات, سولفات, ...)
    form = Column(String(20), nullable=True)  # حالت فیزیکی (powder, liquid, crystal)
    solubility = Column(String(50), nullable=True)  # حلالیت (مثلاً: 250 g/L)
    ph_level = Column(String(20), nullable=True)  # pH محلول (مثلاً: 6-7)
    description = Column(Text, nullable=True)  # توضیحات کامل
    application_method = Column(String(100), nullable=True)  # روش مصرف (محلول‌پاشی، آبیاری)
    packaging = Column(String(50), nullable=True)  # بسته‌بندی (1 کیلویی، 10 کیلویی)
    registration_code = Column(String(20), nullable=True)  # کد ثبت ماده کودی
    npk_ratio = Column(String(20), nullable=True)  # نسبت NPK (مثلاً: 20-20-20)
    organic_matter = Column(Float, nullable=True)  # درصد مواد آلی
    chelating_agent = Column(String(20), nullable=True)  # عامل کلات‌کننده (EDTA, EDDHA, ...)
    
    # ===== تاریخ‌ها =====
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    user = relationship("User", back_populates="fertilizers")
    
    def __repr__(self):
        return f"<Fertilizer {self.name}>"


# ============================================================
# مدل WaterAnalysis (آنالیز آب)
# ============================================================
class WaterAnalysis(Base):
    """مدل آنالیز آب و پساب"""
    
    __tablename__ = "water_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    water_percentage = Column(Float, default=80.0)
    wastewater_percentage = Column(Float, default=20.0)
    water_salinity = Column(Float, default=0.0)
    wastewater_values = Column(JSON, nullable=True)
    water_values = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ===== روابط =====
    report = relationship("Report", back_populates="water_analysis")
    
    def __repr__(self):
        return f"<WaterAnalysis {self.id}>"


# ============================================================
# مدل Calculation (محاسبات)
# ============================================================
class Calculation(Base):
    """مدل محاسبات و نتایج"""
    
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    target_values = Column(JSON, nullable=True)
    final_values = Column(JSON, nullable=True)
    reservoir_data = Column(JSON, nullable=True)
    calc_rows = Column(JSON, nullable=True)
    interpretation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ===== روابط =====
    report = relationship("Report", back_populates="calculation")
    
    def __repr__(self):
        return f"<Calculation {self.id}>"