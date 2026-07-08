# backend/app/models.py
"""همه مدل‌های دیتابیس (SQLAlchemy) - نسخه امنیتی کامل"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from app.database import Base


# ============================================================
# مدل User (کاربر) - نسخه امنیتی
# ============================================================
class User(Base):
    """مدل کاربران سیستم - نسخه امنیتی با قفل حساب و 2FA"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # ===== 🔐 فیلدهای امنیتی =====
    # قفل حساب
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # 2FA
    is_2fa_enabled = Column(Boolean, default=False)
    totp_secret = Column(String(255), nullable=True)
    backup_codes = Column(JSON, nullable=True)  # لیست کدهای پشتیبان
    
    # تاریخچه
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_ip = Column(String(45), nullable=True)
    last_user_agent = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ===== روابط =====
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    fertilizers = relationship("Fertilizer", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    optimizations = relationship("OptimizationLog", back_populates="user", cascade="all, delete-orphan")
    security_logs = relationship("SecurityLog", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def full_name(self) -> str:
        """نام کامل کاربر"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_locked(self) -> bool:
        """بررسی آیا حساب قفل شده است"""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def __repr__(self):
        return f"<User {self.phone_number}>"


# ============================================================
# مدل UserSession (نشست کاربر) - نسخه امنیتی
# ============================================================
class UserSession(Base):
    """مدل نشست‌های کاربر (توکن‌های تصادفی) - نسخه امنیتی"""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    
    # 🔐 اطلاعات نشست
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # ===== روابط =====
    user = relationship("User", back_populates="sessions")
    
    @property
    def is_expired(self) -> bool:
        """بررسی آیا نشست منقضی شده است"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f"<UserSession {self.user_id} - {self.token[:10]}...>"


# ============================================================
# 🔐 مدل SecurityLog (لاگ امنیتی)
# ============================================================
class SecurityLog(Base):
    """مدل ثبت رویدادهای امنیتی"""
    
    __tablename__ = "security_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    # ===== اطلاعات رویداد =====
    event_type = Column(String(50), nullable=False)  # LOGIN_SUCCESS, LOGIN_FAILED, LOGOUT, PASSWORD_CHANGE, etc.
    severity = Column(String(20), default="INFO")  # INFO, WARNING, ERROR, CRITICAL
    
    # ===== اطلاعات درخواست =====
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    endpoint = Column(String(255), nullable=True)
    method = Column(String(10), nullable=True)
    
    # ===== جزئیات =====
    details = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ===== روابط =====
    user = relationship("User", back_populates="security_logs")
    
    def __repr__(self):
        return f"<SecurityLog {self.event_type} - {self.created_at}>"


# ============================================================
# 🔐 مدل PasswordResetToken (فراموشی رمز عبور)
# ============================================================
class PasswordResetToken(Base):
    """مدل توکن‌های یکبار مصرف برای فراموشی رمز عبور"""
    
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # ===== توکن =====
    token = Column(String(255), unique=True, nullable=False, index=True)
    is_used = Column(Boolean, default=False)
    
    # ===== اطلاعات =====
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # ===== روابط =====
    user = relationship("User", back_populates="password_reset_tokens")
    
    @property
    def is_expired(self) -> bool:
        """بررسی آیا توکن منقضی شده است"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f"<PasswordResetToken {self.user_id} - {self.token[:10]}...>"


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
# مدل Fertilizer (کود)
# ============================================================
class Fertilizer(Base):
    """مدل کودها"""
    
    __tablename__ = "fertilizers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False, index=True)
    brand = Column(String(100), nullable=True)
    category = Column(String(50), nullable=True)
    form = Column(String(20), nullable=True)
    concentration = Column(Float, default=100.0)
    elements = Column(JSON, nullable=True)
    price_per_kg = Column(Float, default=0.0)
    is_acid = Column(Boolean, default=False)
    acid_type = Column(String(10), nullable=True)
    ph_level = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    is_system_default = Column(Boolean, default=False)
    source_system_id = Column(Integer, nullable=True)
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
    __tablename__ = "water_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    water_percentage = Column(Float, default=80.0)
    wastewater_percentage = Column(Float, default=20.0)
    water_salinity = Column(Float, default=0.0)
    wastewater_values = Column(JSON, nullable=True)
    water_values = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    report = relationship("Report", back_populates="water_analysis")
    
    def __repr__(self):
        return f"<WaterAnalysis {self.id}>"


# ============================================================
# مدل Calculation (محاسبات)
# ============================================================
class Calculation(Base):
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    target_values = Column(JSON, nullable=True)
    final_values = Column(JSON, nullable=True)
    reservoir_data = Column(JSON, nullable=True)
    calc_rows = Column(JSON, nullable=True)
    interpretation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    report = relationship("Report", back_populates="calculation")
    
    def __repr__(self):
        return f"<Calculation {self.id}>"


# ============================================================
# مدل Recipe (رسپی)
# ============================================================
class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    target_values = Column(JSON, nullable=False)
    category = Column(String(50), nullable=True)
    stage = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="recipes")
    
    def __repr__(self):
        return f"<Recipe {self.name}>"


# ============================================================
# مدل WaterAnalysisTemplate
# ============================================================
class WaterAnalysisTemplate(Base):
    __tablename__ = "water_analysis_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    water_percentage = Column(Float, default=100.0)
    wastewater_percentage = Column(Float, default=0.0)
    water_salinity = Column(Float, default=0.8)
    water_salinity_unit = Column(String(10), default='dS/m')
    water_ph = Column(Float, nullable=True)
    water_values = Column(JSON, nullable=True)
    wastewater_values = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="water_templates")
    
    def __repr__(self):
        return f"<WaterAnalysisTemplate {self.name}>"


# ============================================================
# مدل OptimizationLog
# ============================================================
class OptimizationLog(Base):
    __tablename__ = "optimization_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=True)
    target_values = Column(JSON, nullable=False)
    water_values = Column(JSON, nullable=True)
    fertilizers_selected = Column(JSON, nullable=True)
    optimization_options = Column(JSON, nullable=True)
    optimized_weights = Column(JSON, nullable=True)
    final_concentrations = Column(JSON, nullable=True)
    residual_error = Column(Float, nullable=True)
    cost_total = Column(Float, nullable=True)
    iterations = Column(Integer, nullable=True)
    convergence_time_ms = Column(Float, nullable=True)
    ion_balance = Column(JSON, nullable=True)
    warnings = Column(JSON, nullable=True)
    suggestions = Column(JSON, nullable=True)
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="optimizations")
    report = relationship("Report", back_populates="optimizations")
    
    def __repr__(self):
        return f"<OptimizationLog {self.id}>"