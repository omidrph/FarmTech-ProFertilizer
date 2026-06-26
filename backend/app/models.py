# backend/app/models.py
"""همه مدل‌های دیتابیس (SQLAlchemy) - نسخه نهایی با OptimizationLog"""

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
    optimizations = relationship("OptimizationLog", back_populates="user", cascade="all, delete-orphan")
    
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
    optimizations = relationship("OptimizationLog", back_populates="report", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Report {self.id} - {self.report_name}>"


# ============================================================
# مدل Fertilizer (کود) - نسخه نهایی با فیلدهای بهینه‌شده
# ============================================================
class Fertilizer(Base):
    """
    مدل کودها - نسخه نهایی با فیلدهای ضروری
    
    فیلدهای جدید:
    - concentration: درصد خلوص/غلظت (برای محاسبات دقیق)
    - source_system_id: برای ردیابی کپی از کودهای سیستمی
    - ph_level: برای محاسبات تعادل یونی و pH
    """
    
    __tablename__ = "fertilizers"
    
    # ===== فیلدهای اصلی =====
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False, index=True)
    
    # ===== فیلدهای اطلاعاتی =====
    brand = Column(String(100), nullable=True)          # برند (مثلاً: رازاک شیمی، اطلس)
    category = Column(String(50), nullable=True)        # دسته‌بندی: NPK, کلات, سولفات, اسید, ریزمغذی, ...
    form = Column(String(20), nullable=True)            # فرم فیزیکی: liquid, powder, crystal, granular
    
    # ===== فیلدهای محاسباتی (مهم) =====
    concentration = Column(Float, default=100.0)        # درصد خلوص/غلظت (برای مایعات و جامدات)
    elements = Column(JSON, nullable=True)              # {"N-NO3": 15.5, "P": 20, ...}
    price_per_kg = Column(Float, default=0.0)           # قیمت هر کیلوگرم
    
    # ===== فیلدهای اسید و pH =====
    is_acid = Column(Boolean, default=False)
    acid_type = Column(String(10), nullable=True)       # H3PO4, HNO3, H2SO4
    ph_level = Column(Float, nullable=True)             # pH محلول (برای محاسبات)
    
    # ===== توضیحات =====
    description = Column(Text, nullable=True)           # توضیحات کوتاه و مفید
    
    # ===== سیستم =====
    is_system_default = Column(Boolean, default=False)  # آیا کود سیستمی است؟
    source_system_id = Column(Integer, nullable=True)   # اگر از کود سیستمی کپی شده باشد (ID منبع)
    
    # ===== تاریخ‌ها =====
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    user = relationship("User", back_populates="fertilizers")
    
    def __repr__(self):
        return f"<Fertilizer {self.name} (ID:{self.id})>"


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
    

# ============================================================
# مدل Recipe (رسپی/فرمول غذایی)
# ============================================================
class Recipe(Base):
    """مدل رسپی‌های غذایی (فرمول‌های از پیش تعیین شده)"""
    
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # ===== نوع رسپی =====
    is_system = Column(Boolean, default=False)  # True: رسپی سیستمی، False: رسپی شخصی کاربر
    
    # ===== کاربر سازنده (فقط برای رسپی‌های شخصی) =====
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    # ===== مقادیر هدف عناصر (JSON) =====
    target_values = Column(JSON, nullable=False)  # {"N-NO3": 320, "P": 103, ...}
    
    # ===== دسته‌بندی =====
    category = Column(String(50), nullable=True)  # مثلاً: "گوجه فرنگی", "خیار", "کاهو"
    stage = Column(String(50), nullable=True)    # مرحله رشد: "گلدهی", "رویشی", "میوه‌دهی"
    
    # ===== تاریخ‌ها =====
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    user = relationship("User", backref="recipes")
    
    def __repr__(self):
        return f"<Recipe {self.name}>"
    

# ============================================================
# مدل WaterAnalysisTemplate (قالب آنالیز آب کاربر)
# ============================================================
class WaterAnalysisTemplate(Base):
    """مدل قالب‌های آنالیز آب کاربر (برای ذخیره و استفاده مجدد)"""
    
    __tablename__ = "water_analysis_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)  # نام قالب (مثلاً: "آب چاه شماره ۱")
    description = Column(Text, nullable=True)  # توضیحات
    
    # مقادیر آنالیز
    water_percentage = Column(Float, default=100.0)
    wastewater_percentage = Column(Float, default=0.0)
    water_salinity = Column(Float, default=0.8)  # EC
    water_salinity_unit = Column(String(10), default='dS/m')  # واحد EC
    water_ph = Column(Float, nullable=True)  # pH آب
    
    # مقادیر عناصر
    water_values = Column(JSON, nullable=True)  # {"N-NO3": 10, "P": 2, ...}
    wastewater_values = Column(JSON, nullable=True)  # {"N-NO3": 20, "P": 5, ...}
    
    # تاریخ‌ها
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    user = relationship("User", backref="water_templates")
    
    def __repr__(self):
        return f"<WaterAnalysisTemplate {self.name}>"


# ============================================================
# 🆕 مدل OptimizationLog (برای ثبت تاریخچه بهینه‌سازی)
# ============================================================
class OptimizationLog(Base):
    """مدل ثبت تاریخچه بهینه‌سازی فرمول کود"""
    
    __tablename__ = "optimization_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=True)
    
    # ===== ورودی‌ها =====
    target_values = Column(JSON, nullable=False)  # عناصر هدف
    water_values = Column(JSON, nullable=True)    # کیفیت آب
    fertilizers_selected = Column(JSON, nullable=True)  # لیست کودهای انتخاب شده
    
    # ===== تنظیمات بهینه‌سازی =====
    optimization_options = Column(JSON, nullable=True)  # تنظیمات (وزن‌ها، روش، ...)
    
    # ===== خروجی‌ها =====
    optimized_weights = Column(JSON, nullable=True)  # وزن‌های بهینه هر کود
    final_concentrations = Column(JSON, nullable=True)  # غلظت نهایی عناصر
    residual_error = Column(Float, nullable=True)  # خطای باقی‌مانده
    cost_total = Column(Float, nullable=True)  # هزینه کل
    
    # ===== متریک‌های عملکرد =====
    iterations = Column(Integer, nullable=True)  # تعداد تکرارها
    convergence_time_ms = Column(Float, nullable=True)  # زمان همگرایی (میلی‌ثانیه)
    
    # ===== تحلیل =====
    ion_balance = Column(JSON, nullable=True)  # {"cation": 12.3, "anion": 12.1, "is_balanced": True}
    warnings = Column(JSON, nullable=True)  # لیست هشدارها
    suggestions = Column(JSON, nullable=True)  # لیست پیشنهادات
    
    # ===== وضعیت =====
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # ===== تاریخ‌ها =====
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ===== روابط =====
    user = relationship("User", back_populates="optimizations")
    report = relationship("Report", back_populates="optimizations")
    
    def __repr__(self):
        return f"<OptimizationLog {self.id}>"