# backend/app/schemas.py
"""همه طرح‌های Pydantic برای اعتبارسنجی داده‌ها - نسخه اصلاح شده"""
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
# طرح‌های مربوط به Fertilizer (کود) - اصلاح شده
# ============================================================
class FertilizerCreate(BaseModel):
    """طرح ایجاد کود جدید - فقط name اجباری است"""
    # ===== فیلد اجباری =====
    name: str = Field(..., min_length=1, max_length=100, description="نام کود (اجباری)")
    
    # ===== فیلدهای اصلی - اختیاری =====
    price_per_kg: Optional[float] = Field(None, ge=0, description="قیمت هر کیلوگرم")
    elements: Optional[Dict[str, float]] = Field(default_factory=dict, description="درصد عناصر")
    is_acid: bool = Field(False, description="آیا اسید است؟")
    acid_type: Optional[str] = Field(None, max_length=10, description="نوع اسید")
    
    # ===== 🆕 فیلدهای جدید - همه اختیاری =====
    is_system_default: bool = Field(False, description="آیا کود سیستمی است؟")
    brand: Optional[str] = Field(None, max_length=100, description="برند/شرکت")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    form: Optional[str] = Field(None, max_length=20, description="حالت فیزیکی")
    solubility: Optional[str] = Field(None, max_length=50, description="حلالیت")
    ph_level: Optional[str] = Field(None, max_length=20, description="pH محلول")
    description: Optional[str] = Field(None, description="توضیحات")
    application_method: Optional[str] = Field(None, max_length=100, description="روش مصرف")
    packaging: Optional[str] = Field(None, max_length=50, description="بسته‌بندی")
    registration_code: Optional[str] = Field(None, max_length=20, description="کد ثبت")
    npk_ratio: Optional[str] = Field(None, max_length=20, description="نسبت NPK")
    organic_matter: Optional[float] = Field(None, ge=0, le=100, description="درصد مواد آلی")
    chelating_agent: Optional[str] = Field(None, max_length=20, description="عامل کلات‌کننده")

class FertilizerUpdate(BaseModel):
    """طرح به‌روزرسانی کود - همه فیلدها اختیاری"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_per_kg: Optional[float] = Field(None, ge=0)
    elements: Optional[Dict[str, float]] = None
    is_acid: Optional[bool] = None
    acid_type: Optional[str] = Field(None, max_length=10)
    
    # 🆕 فیلدهای جدید
    is_system_default: Optional[bool] = None
    brand: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    form: Optional[str] = Field(None, max_length=20)
    solubility: Optional[str] = Field(None, max_length=50)
    ph_level: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    application_method: Optional[str] = Field(None, max_length=100)
    packaging: Optional[str] = Field(None, max_length=50)
    registration_code: Optional[str] = Field(None, max_length=20)
    npk_ratio: Optional[str] = Field(None, max_length=20)
    organic_matter: Optional[float] = Field(None, ge=0, le=100)
    chelating_agent: Optional[str] = Field(None, max_length=20)

class FertilizerResponse(BaseModel):
    """طرح پاسخ کود - شامل همه فیلدها"""
    id: int
    user_id: Optional[int] = None  # ✅ nullable شد
    name: str
    
    # فیلدهای اصلی
    price_per_kg: Optional[float] = None
    elements: Optional[Dict[str, float]] = None
    is_acid: bool = False
    acid_type: Optional[str] = None
    
    # 🆕 فیلدهای جدید
    is_system_default: bool = False
    brand: Optional[str] = None
    category: Optional[str] = None
    form: Optional[str] = None
    solubility: Optional[str] = None
    ph_level: Optional[str] = None
    description: Optional[str] = None
    application_method: Optional[str] = None
    packaging: Optional[str] = None
    registration_code: Optional[str] = None
    npk_ratio: Optional[str] = None
    organic_matter: Optional[float] = None
    chelating_agent: Optional[str] = None
    
    # تاریخ‌ها
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
# طرح‌های مربوط به APIهای محاسباتی
# ============================================================

class IonBalanceRequest(BaseModel):
    """درخواست محاسبه تعادل یونی"""
    elements: Dict[str, float] = Field(..., description="مقادیر عناصر")
    unit: str = Field("ppm", description="واحد (ppm, meq, mmol)")

class IonBalanceResponse(BaseModel):
    """پاسخ محاسبه تعادل یونی"""
    cation: float
    anion: float
    is_balanced: bool
    message: str

class FinalSolutionRequest(BaseModel):
    """درخواست محاسبه محلول نهایی"""
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف")
    water_values: Dict[str, float] = Field(..., description="مقادیر موجود در آب")
    fertilizer_contributions: Dict[str, float] = Field(..., description="سهم کودها")

class FinalSolutionResponse(BaseModel):
    """پاسخ محاسبه محلول نهایی"""
    final_values: Dict[str, float]
    ion_balance: IonBalanceResponse

class ReservoirRequest(BaseModel):
    """درخواست محاسبه مخازن"""
    fertilizers: List[Dict[str, Any]] = Field(..., description="لیست کودها با وزن و خلوص")

class ReservoirResponse(BaseModel):
    """پاسخ محاسبه مخازن"""
    reservoir_data: Dict[str, List[Dict[str, Any]]]
    totals: Dict[str, float]

class UnitConversionRequest(BaseModel):
    """درخواست تبدیل واحد"""
    value: float = Field(..., description="مقدار")
    from_unit: str = Field(..., description="واحد مبدا (ppm, meq, mmol)")
    to_unit: str = Field(..., description="واحد مقصد (ppm, meq, mmol)")
    element: str = Field(..., description="نام عنصر")

class UnitConversionResponse(BaseModel):
    """پاسخ تبدیل واحد"""
    original_value: float
    converted_value: float
    from_unit: str
    to_unit: str
    element: str

# ============================================================
# طرح‌های مربوط به Home Summary
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

    # ============================================================
# طرح‌های مربوط به Recipe (رسپی)
# ============================================================

class RecipeBase(BaseModel):
    """طرح پایه رسپی"""
    name: str = Field(..., min_length=1, max_length=100, description="نام رسپی")
    description: Optional[str] = Field(None, description="توضیحات")
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف عناصر")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    stage: Optional[str] = Field(None, max_length=50, description="مرحله رشد")
    is_system: bool = Field(False, description="آیا رسپی سیستمی است؟")

class RecipeCreate(RecipeBase):
    """طرح ایجاد رسپی جدید"""
    pass

class RecipeUpdate(BaseModel):
    """طرح به‌روزرسانی رسپی"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    target_values: Optional[Dict[str, float]] = None
    category: Optional[str] = Field(None, max_length=50)
    stage: Optional[str] = Field(None, max_length=50)

class RecipeResponse(BaseModel):
    """طرح پاسخ رسپی"""
    id: int
    name: str
    description: Optional[str]
    target_values: Dict[str, float]
    category: Optional[str]
    stage: Optional[str]
    is_system: bool
    user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class RecipeListResponse(BaseModel):
    """پاسخ لیست رسپی‌ها (با تفکیک سیستمی و شخصی)"""
    system_recipes: List[RecipeResponse]
    user_recipes: List[RecipeResponse]