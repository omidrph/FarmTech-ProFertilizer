# backend/app/schemas.py
"""همه طرح‌های Pydantic برای اعتبارسنجی داده‌ها - نسخه نهایی"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

# ============================================================
# طرح‌های مربوط به User (کاربر)
# ============================================================
class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="نام")
    last_name: str = Field(..., min_length=1, max_length=50, description="نام خانوادگی")
    phone_number: str = Field(..., min_length=11, max_length=15, description="شماره تلفن")
    password: str = Field(..., min_length=6, max_length=100, description="رمز عبور")

    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v

class UserLogin(BaseModel):
    phone_number: str = Field(..., description="شماره تلفن")
    password: str = Field(..., description="رمز عبور")

class UserResponse(BaseModel):
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
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=11, max_length=15)

# ============================================================
# طرح‌های مربوط به Token (توکن تصادفی)
# ============================================================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[int] = None
    phone_number: Optional[str] = None

# ============================================================
# طرح‌های مربوط به Report (گزارش)
# ============================================================
class ReportCreate(BaseModel):
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = Field(None, description="تاریخ شمسی")

class ReportUpdate(BaseModel):
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = None

class ReportResponse(BaseModel):
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
    name: str = Field(..., min_length=1, max_length=100)
    price_per_kg: float = Field(0.0, ge=0)
    elements: Optional[Dict[str, float]] = Field(default_factory=dict)
    is_acid: bool = False
    acid_type: Optional[str] = Field(None, max_length=10)

class FertilizerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_per_kg: Optional[float] = Field(None, ge=0)
    elements: Optional[Dict[str, float]] = None
    is_acid: Optional[bool] = None
    acid_type: Optional[str] = Field(None, max_length=10)

class FertilizerResponse(BaseModel):
    id: int
    user_id: int
    name: str
    price_per_kg: float
    elements: Optional[Dict[str, float]] = None
    is_acid: bool = False
    acid_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============================================================
# طرح‌های مربوط به WaterAnalysis (آنالیز آب)
# ============================================================
class WaterAnalysisCreate(BaseModel):
    water_percentage: float = Field(80.0, ge=0, le=100)
    wastewater_percentage: float = Field(20.0, ge=0, le=100)
    water_salinity: float = Field(0.0, ge=0)
    wastewater_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict)

class WaterAnalysisUpdate(BaseModel):
    water_percentage: Optional[float] = Field(None, ge=0, le=100)
    wastewater_percentage: Optional[float] = Field(None, ge=0, le=100)
    water_salinity: Optional[float] = Field(None, ge=0)
    wastewater_values: Optional[Dict[str, float]] = None
    water_values: Optional[Dict[str, float]] = None

class WaterAnalysisResponse(BaseModel):
    id: int
    report_id: int
    water_percentage: float
    wastewater_percentage: float
    water_salinity: float
    wastewater_values: Optional[Dict[str, float]] = None
    water_values: Optional[Dict[str, float]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# طرح‌های مربوط به Calculation (محاسبات)
# ============================================================
class CalculationCreate(BaseModel):
    target_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    final_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    reservoir_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    calc_rows: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    interpretation: Optional[str] = None

class CalculationUpdate(BaseModel):
    target_values: Optional[Dict[str, float]] = None
    final_values: Optional[Dict[str, float]] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    calc_rows: Optional[List[Dict[str, Any]]] = None
    interpretation: Optional[str] = None

class CalculationResponse(BaseModel):
    id: int
    report_id: int
    target_values: Optional[Dict[str, float]] = None
    final_values: Optional[Dict[str, float]] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    calc_rows: Optional[List[Dict[str, Any]]] = None
    interpretation: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# 🆕 طرح‌های جدید برای APIهای محاسباتی
# ============================================================

class IonBalanceRequest(BaseModel):
    """🆕 درخواست محاسبه تعادل یونی"""
    elements: Dict[str, float] = Field(..., description="مقادیر عناصر")
    unit: str = Field("ppm", description="واحد (ppm, meq, mmol)")

class IonBalanceResponse(BaseModel):
    """🆕 پاسخ محاسبه تعادل یونی"""
    cation: float
    anion: float
    is_balanced: bool
    message: str

class FinalSolutionRequest(BaseModel):
    """🆕 درخواست محاسبه محلول نهایی"""
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف")
    water_values: Dict[str, float] = Field(..., description="مقادیر موجود در آب")
    fertilizer_contributions: Dict[str, float] = Field(..., description="سهم کودها")

class FinalSolutionResponse(BaseModel):
    """🆕 پاسخ محاسبه محلول نهایی"""
    final_values: Dict[str, float]
    ion_balance: IonBalanceResponse

class ReservoirRequest(BaseModel):
    """🆕 درخواست محاسبه مخازن"""
    fertilizers: List[Dict[str, Any]] = Field(..., description="لیست کودها با وزن و خلوص")

class ReservoirResponse(BaseModel):
    """🆕 پاسخ محاسبه مخازن"""
    reservoir_data: Dict[str, List[Dict[str, Any]]]
    totals: Dict[str, float]

class UnitConversionRequest(BaseModel):
    """🆕 درخواست تبدیل واحد"""
    value: float = Field(..., description="مقدار")
    from_unit: str = Field(..., description="واحد مبدا (ppm, meq, mmol)")
    to_unit: str = Field(..., description="واحد مقصد (ppm, meq, mmol)")
    element: str = Field(..., description="نام عنصر")

class UnitConversionResponse(BaseModel):
    """🆕 پاسخ تبدیل واحد"""
    original_value: float
    converted_value: float
    from_unit: str
    to_unit: str
    element: str

# ============================================================
# 🆕 طرح‌های جدید برای Home Summary
# ============================================================

class HomeSummaryElementData(BaseModel):
    """داده هر عنصر برای داشبورد"""
    element: str
    target: float
    actual: float
    difference: float
    progress_percent: float

class HomeSummaryRecommendation(BaseModel):
    """توصیه برای داشبورد"""
    type: str
    title: str
    description: str

class HomeSummaryResponse(BaseModel):
    """پاسخ خلاصه داشبورد"""
    has_data: bool
    message: Optional[str] = None
    ion_balance: Optional[Dict[str, Any]] = None
    active_elements_count: Optional[int] = None
    total_elements: Optional[int] = None
    active_reservoirs_count: Optional[int] = None
    total_cost: Optional[float] = None
    total_reservoir_weight: Optional[float] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    elements_data: Optional[List[HomeSummaryElementData]] = None
    recommendations: Optional[List[HomeSummaryRecommendation]] = None
    water_salinity: Optional[float] = None

# ============================================================
# طرح‌های مربوط به تفسیر داده‌ها (Interpretation)
# ============================================================
class ElementStatusResponse(BaseModel):
    element: str
    target: float
    actual: float
    difference: float
    status: str
    message: str

class WaterQualityResponse(BaseModel):
    salinity: float
    impact: str
    recommendation: str

class RecommendationResponse(BaseModel):
    issue: str
    suggestion: str
    priority: str

class InterpretationResponse(BaseModel):
    ion_balance: IonBalanceResponse
    element_status: List[ElementStatusResponse]
    water_quality: WaterQualityResponse
    fertilizer_recommendation: List[RecommendationResponse]
    summary: str

# ============================================================
# طرح‌های عمومی
# ============================================================
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int