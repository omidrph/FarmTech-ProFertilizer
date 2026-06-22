# backend/app/schemas.py
"""همه طرح‌های Pydantic برای اعتبارسنجی داده‌ها"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
# طرح‌های مربوط به User (کاربر)
# ============================================================

class UserCreate(BaseModel):
    """طرح ثبت‌نام کاربر جدید"""
    first_name: str = Field(..., min_length=1, max_length=50, description="نام")
    last_name: str = Field(..., min_length=1, max_length=50, description="نام خانوادگی")
    phone_number: str = Field(..., min_length=11, max_length=15, description="شماره تلفن")
    password: str = Field(..., min_length=6, max_length=100, description="رمز عبور")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        import re
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v


class UserLogin(BaseModel):
    """طرح ورود کاربر"""
    phone_number: str = Field(..., description="شماره تلفن")
    password: str = Field(..., description="رمز عبور")


class UserResponse(BaseModel):
    """طرح پاسخ اطلاعات کاربر"""
    id: int
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    full_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """طرح به‌روزرسانی اطلاعات کاربر"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=11, max_length=15)


# ============================================================
# طرح‌های مربوط به Token (توکن تصادفی)
# ============================================================

class Token(BaseModel):
    """طرح پاسخ توکن"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """طرح داده‌های توکن"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = None


# ============================================================
# طرح‌های مربوط به Report (گزارش)
# ============================================================

class ReportCreate(BaseModel):
    """طرح ایجاد گزارش جدید"""
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = Field(None, description="تاریخ شمسی")


class ReportUpdate(BaseModel):
    """طرح به‌روزرسانی گزارش"""
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = None


class ReportResponse(BaseModel):
    """طرح پاسخ گزارش"""
    id: int
    user_id: int
    report_name: Optional[str]
    plant_name: Optional[str]
    season: Optional[str]
    growth_stage: Optional[str]
    report_date: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============================================================
# طرح‌های مربوط به Fertilizer (کود)
# ============================================================

class FertilizerCreate(BaseModel):
    """طرح ایجاد کود جدید"""
    name: str = Field(..., min_length=1, max_length=100)
    price_per_kg: float = Field(0.0, ge=0)
    elements: Optional[Dict[str, float]] = Field(default_factory=dict)
    is_acid: bool = False
    acid_type: Optional[str] = Field(None, max_length=10)


class FertilizerUpdate(BaseModel):
    """طرح به‌روزرسانی کود"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_per_kg: Optional[float] = Field(None, ge=0)
    elements: Optional[Dict[str, float]] = None
    is_acid: Optional[bool] = None
    acid_type: Optional[str] = Field(None, max_length=10)


class FertilizerResponse(BaseModel):
    """طرح پاسخ کود"""
    id: int
    user_id: int
    name: str
    price_per_kg: float
    elements: Optional[Dict[str, float]]
    is_acid: bool
    acid_type: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============================================================
# طرح‌های مربوط به WaterAnalysis (آنالیز آب)
# ============================================================

class WaterAnalysisCreate(BaseModel):
    """طرح ایجاد آنالیز آب"""
    water_percentage: float = Field(80.0, ge=0, le=100)
    wastewater_percentage: float = Field(20.0, ge=0, le=100)
    water_salinity: float = Field(0.0, ge=0)
    wastewater_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict)


class WaterAnalysisUpdate(BaseModel):
    """طرح به‌روزرسانی آنالیز آب"""
    water_percentage: Optional[float] = Field(None, ge=0, le=100)
    wastewater_percentage: Optional[float] = Field(None, ge=0, le=100)
    water_salinity: Optional[float] = Field(None, ge=0)
    wastewater_values: Optional[Dict[str, float]] = None
    water_values: Optional[Dict[str, float]] = None


class WaterAnalysisResponse(BaseModel):
    """طرح پاسخ آنالیز آب"""
    id: int
    report_id: int
    water_percentage: float
    wastewater_percentage: float
    water_salinity: float
    wastewater_values: Optional[Dict[str, float]]
    water_values: Optional[Dict[str, float]]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# طرح‌های مربوط به Calculation (محاسبات)
# ============================================================

class CalculationCreate(BaseModel):
    """طرح ایجاد محاسبات"""
    target_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    final_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    reservoir_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    calc_rows: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    interpretation: Optional[str] = None


class CalculationUpdate(BaseModel):
    """طرح به‌روزرسانی محاسبات"""
    target_values: Optional[Dict[str, float]] = None
    final_values: Optional[Dict[str, float]] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    calc_rows: Optional[List[Dict[str, Any]]] = None
    interpretation: Optional[str] = None


class CalculationResponse(BaseModel):
    """طرح پاسخ محاسبات"""
    id: int
    report_id: int
    target_values: Optional[Dict[str, float]]
    final_values: Optional[Dict[str, float]]
    reservoir_data: Optional[Dict[str, Any]]
    calc_rows: Optional[List[Dict[str, Any]]]
    interpretation: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# طرح‌های مربوط به تفسیر داده‌ها (Interpretation)
# ============================================================

class IonBalanceResponse(BaseModel):
    """طرح پاسخ تعادل یونی"""
    cation: float
    anion: float
    is_balanced: bool
    message: str


class ElementStatusResponse(BaseModel):
    """طرح پاسخ وضعیت هر عنصر"""
    element: str
    target: float
    actual: float
    difference: float
    status: str  # deficient, sufficient, excessive, toxic
    message: str


class WaterQualityResponse(BaseModel):
    """طرح پاسخ کیفیت آب"""
    salinity: float
    impact: str
    recommendation: str


class RecommendationResponse(BaseModel):
    """طرح پاسخ توصیه کودی"""
    issue: str
    suggestion: str
    priority: str  # low, medium, high


class InterpretationResponse(BaseModel):
    """طرح پاسخ تفسیر کامل"""
    ion_balance: IonBalanceResponse
    element_status: List[ElementStatusResponse]
    water_quality: WaterQualityResponse
    fertilizer_recommendation: List[RecommendationResponse]
    summary: str


# ============================================================
# طرح‌های عمومی
# ============================================================

class MessageResponse(BaseModel):
    """طرح پیام ساده"""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    """طرح پاسخ صفحه‌بندی شده"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int