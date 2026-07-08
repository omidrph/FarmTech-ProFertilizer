# backend/app/schemas.py
"""همه طرح‌های Pydantic برای اعتبارسنجی داده‌ها - نسخه امنیتی کامل"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


# ============================================================
# 🔐 طرح‌های امنیتی - تغییر رمز عبور
# ============================================================

class ChangePasswordRequest(BaseModel):
    """درخواست تغییر رمز عبور"""
    current_password: str = Field(..., min_length=8, description="رمز عبور فعلی")
    new_password: str = Field(..., min_length=8, description="رمز عبور جدید")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """اعتبارسنجی قدرت رمز عبور جدید"""
        if len(v) < 8:
            raise ValueError('رمز عبور جدید باید حداقل ۸ کاراکتر باشد')
        
        if not any(c.isupper() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک حرف بزرگ داشته باشد')
        
        if not any(c.islower() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک حرف کوچک داشته باشد')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک عدد داشته باشد')
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک کاراکتر خاص داشته باشد')
        
        return v


class ChangePasswordResponse(BaseModel):
    """پاسخ تغییر رمز عبور"""
    message: str
    success: bool


# ============================================================
# 🔐 طرح‌های فراموشی رمز عبور (با پیامک)
# ============================================================

class ForgotPasswordRequest(BaseModel):
    """درخواست فراموشی رمز عبور"""
    phone_number: str = Field(..., description="شماره تلفن")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v


class ForgotPasswordResponse(BaseModel):
    """پاسخ فراموشی رمز عبور"""
    message: str
    success: bool
    reset_id: Optional[str] = None  # برای ردیابی


class ResetPasswordRequest(BaseModel):
    """درخواست بازنشانی رمز عبور"""
    phone_number: str = Field(..., description="شماره تلفن")
    code: str = Field(..., min_length=6, max_length=6, description="کد تأیید ۶ رقمی")
    new_password: str = Field(..., min_length=8, description="رمز عبور جدید")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('کد تأیید باید عددی باشد')
        return v
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('رمز عبور جدید باید حداقل ۸ کاراکتر باشد')
        
        if not any(c.isupper() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک حرف بزرگ داشته باشد')
        
        if not any(c.islower() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک حرف کوچک داشته باشد')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک عدد داشته باشد')
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in v):
            raise ValueError('رمز عبور جدید باید حداقل یک کاراکتر خاص داشته باشد')
        
        return v


class ResetPasswordResponse(BaseModel):
    """پاسخ بازنشانی رمز عبور"""
    message: str
    success: bool


# ============================================================
# 🔐 طرح‌های 2FA (تأیید دو مرحله‌ای)
# ============================================================

class Enable2FARequest(BaseModel):
    """درخواست فعال‌سازی 2FA"""
    phone_number: str = Field(..., description="شماره تلفن")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v


class Enable2FAResponse(BaseModel):
    """پاسخ فعال‌سازی 2FA"""
    secret: str
    backup_codes: List[str]
    qr_code_url: Optional[str] = None
    message: str
    success: bool


class Verify2FARequest(BaseModel):
    """درخواست تأیید 2FA"""
    code: str = Field(..., min_length=6, max_length=6, description="کد ۶ رقمی")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('کد باید عددی باشد')
        return v


class Verify2FAResponse(BaseModel):
    """پاسخ تأیید 2FA"""
    message: str
    success: bool


class Disable2FARequest(BaseModel):
    """درخواست غیرفعال‌سازی 2FA"""
    code: str = Field(..., min_length=6, max_length=6, description="کد ۶ رقمی")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('کد باید عددی باشد')
        return v


class Disable2FAResponse(BaseModel):
    """پاسخ غیرفعال‌سازی 2FA"""
    message: str
    success: bool


# ============================================================
# 🔐 طرح‌های با اعتبارسنجی امنیتی - جلوگیری از XSS و SQL Injection
# ============================================================

class SecureString(str):
    """کلاس کمکی برای اعتبارسنجی رشته‌های امن"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            return v
        
        # حذف کاراکترهای خطرناک
        dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/', '\\x00']
        for char in dangerous_chars:
            if char in v:
                raise ValueError(f'رشته حاوی کاراکترهای غیرمجاز است: {char}')
        
        return v.strip()


# ============================================================
# طرح‌های مربوط به User (کاربر) - امنیتی
# ============================================================
class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="نام")
    last_name: str = Field(..., min_length=1, max_length=50, description="نام خانوادگی")
    phone_number: str = Field(..., min_length=11, max_length=15, description="شماره تلفن")
    password: str = Field(..., min_length=8, max_length=100, description="رمز عبور")

    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        
        if not any(c.isupper() for c in v):
            raise ValueError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد')
        
        if not any(c.islower() for c in v):
            raise ValueError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('رمز عبور باید حداقل یک عدد داشته باشد')
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in v):
            raise ValueError('رمز عبور باید حداقل یک کاراکتر خاص داشته باشد')
        
        return v
    
    @validator('first_name', 'last_name')
    def validate_name(cls, v):
        # جلوگیری از XSS در نام
        if any(char in v for char in ['<', '>', '"', "'", ';', '--']):
            raise ValueError('نام حاوی کاراکترهای غیرمجاز است')
        return v.strip()


class UserLogin(BaseModel):
    phone_number: str = Field(..., description="شماره تلفن")
    password: str = Field(..., description="رمز عبور")

    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    full_name: str
    created_at: datetime
    is_2fa_enabled: bool = False

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=11, max_length=15)

    @validator('phone_number')
    def validate_phone(cls, v):
        if v and not re.match(r'^09[0-9]{9}$', v):
            raise ValueError('شماره تلفن باید با 09 شروع شده و 11 رقم باشد')
        return v
    
    @validator('first_name', 'last_name')
    def validate_name(cls, v):
        if v and any(char in v for char in ['<', '>', '"', "'", ';', '--']):
            raise ValueError('نام حاوی کاراکترهای غیرمجاز است')
        return v.strip() if v else v


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
# طرح‌های مربوط به Fertilizer (کود) - با اعتبارسنجی امنیتی
# ============================================================
class FertilizerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="نام کود (اجباری)")
    brand: Optional[str] = Field(None, max_length=100, description="برند/شرکت")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    form: Optional[str] = Field(None, max_length=20, description="فرم فیزیکی")
    concentration: Optional[float] = Field(100.0, ge=0, le=100, description="درصد خلوص/غلظت")
    elements: Optional[Dict[str, float]] = Field(default_factory=dict, description="درصد عناصر")
    price_per_kg: Optional[float] = Field(0.0, ge=0, description="قیمت هر کیلوگرم")
    is_acid: bool = Field(False, description="آیا اسید است؟")
    acid_type: Optional[str] = Field(None, max_length=10, description="نوع اسید")
    ph_level: Optional[float] = Field(None, ge=0, le=14, description="pH محلول")
    description: Optional[str] = Field(None, description="توضیحات")
    is_system_default: bool = Field(False, description="آیا کود سیستمی است؟")
    source_system_id: Optional[int] = Field(None, description="ID کود سیستمی مبدا")
    
    @validator('name')
    def validate_name(cls, v):
        # جلوگیری از XSS و SQL Injection
        if any(char in v for char in ['<', '>', '"', "'", ';', '--', '/*', '*/']):
            raise ValueError('نام کود حاوی کاراکترهای غیرمجاز است')
        return v.strip()
    
    @validator('elements')
    def validate_elements(cls, v):
        if v:
            for key, value in v.items():
                if not re.match(r'^[A-Za-z0-9\-]+$', key):
                    raise ValueError(f'نام عنصر {key} نامعتبر است')
                if not (0 <= value <= 100):
                    raise ValueError(f'مقدار عنصر {key} باید بین 0 تا 100 باشد')
        return v


class FertilizerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    form: Optional[str] = Field(None, max_length=20)
    concentration: Optional[float] = Field(None, ge=0, le=100)
    elements: Optional[Dict[str, float]] = None
    price_per_kg: Optional[float] = Field(None, ge=0)
    is_acid: Optional[bool] = None
    acid_type: Optional[str] = Field(None, max_length=10)
    ph_level: Optional[float] = Field(None, ge=0, le=14)
    description: Optional[str] = None
    is_system_default: Optional[bool] = None
    source_system_id: Optional[int] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v and any(char in v for char in ['<', '>', '"', "'", ';', '--', '/*', '*/']):
            raise ValueError('نام کود حاوی کاراکترهای غیرمجاز است')
        return v.strip() if v else v


class FertilizerResponse(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    form: Optional[str] = None
    concentration: Optional[float] = 100.0
    elements: Optional[Dict[str, float]] = None
    price_per_kg: Optional[float] = 0.0
    is_acid: bool = False
    acid_type: Optional[str] = None
    ph_level: Optional[float] = None
    description: Optional[str] = None
    is_system_default: bool = False
    source_system_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


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
# طرح‌های مربوط به Recipe (رسپی)
# ============================================================
class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="نام رسپی")
    description: Optional[str] = Field(None, description="توضیحات")
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف عناصر")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    stage: Optional[str] = Field(None, max_length=50, description="مرحله رشد")
    is_system: bool = Field(False, description="آیا رسپی سیستمی است؟")


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    target_values: Optional[Dict[str, float]] = None
    category: Optional[str] = Field(None, max_length=50)
    stage: Optional[str] = Field(None, max_length=50)


class RecipeResponse(BaseModel):
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
    system_recipes: List[RecipeResponse]
    user_recipes: List[RecipeResponse]


# ============================================================
# طرح‌های مربوط به WaterAnalysisTemplate
# ============================================================
class WaterAnalysisTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="نام قالب")
    description: Optional[str] = Field(None, description="توضیحات")
    water_percentage: float = Field(100.0, ge=0, le=100)
    wastewater_percentage: float = Field(0.0, ge=0, le=100)
    water_salinity: float = Field(0.8, ge=0)
    water_salinity_unit: str = Field('dS/m', description="واحد EC")
    water_ph: Optional[float] = Field(None, ge=0, le=14)
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    wastewater_values: Optional[Dict[str, float]] = Field(default_factory=dict)


class WaterAnalysisTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    water_percentage: Optional[float] = Field(None, ge=0, le=100)
    wastewater_percentage: Optional[float] = Field(None, ge=0, le=100)
    water_salinity: Optional[float] = Field(None, ge=0)
    water_salinity_unit: Optional[str] = None
    water_ph: Optional[float] = Field(None, ge=0, le=14)
    water_values: Optional[Dict[str, float]] = None
    wastewater_values: Optional[Dict[str, float]] = None


class WaterAnalysisTemplateResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    water_percentage: float
    wastewater_percentage: float
    water_salinity: float
    water_salinity_unit: str
    water_ph: Optional[float]
    water_values: Optional[Dict[str, float]]
    wastewater_values: Optional[Dict[str, float]]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============================================================
# طرح‌های مربوط به APIهای محاسباتی
# ============================================================
class IonBalanceRequest(BaseModel):
    elements: Dict[str, float] = Field(..., description="مقادیر عناصر")
    unit: str = Field("ppm", description="واحد (ppm, meq, mmol)")


class IonBalanceResponse(BaseModel):
    cation: float
    anion: float
    is_balanced: bool
    message: str


class FinalSolutionRequest(BaseModel):
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف")
    water_values: Dict[str, float] = Field(..., description="مقادیر موجود در آب")
    fertilizer_contributions: Dict[str, float] = Field(..., description="سهم کودها")


class FinalSolutionResponse(BaseModel):
    final_values: Dict[str, float]
    ion_balance: IonBalanceResponse


class ReservoirRequest(BaseModel):
    fertilizers: List[Dict[str, Any]] = Field(..., description="لیست کودها با وزن و خلوص")


class ReservoirResponse(BaseModel):
    reservoir_data: Dict[str, List[Dict[str, Any]]]
    totals: Dict[str, float]


class UnitConversionRequest(BaseModel):
    value: float = Field(..., description="مقدار")
    from_unit: str = Field(..., description="واحد مبدا (ppm, meq, mmol)")
    to_unit: str = Field(..., description="واحد مقصد (ppm, meq, mmol)")
    element: str = Field(..., description="نام عنصر")


class UnitConversionResponse(BaseModel):
    original_value: float
    converted_value: float
    from_unit: str
    to_unit: str
    element: str


# ============================================================
# طرح‌های مربوط به Home Summary
# ============================================================
class HomeSummaryElementData(BaseModel):
    element: str
    target: float
    actual: float
    difference: float
    progress_percent: float


class HomeSummaryRecommendation(BaseModel):
    type: str
    title: str
    description: str


class HomeSummaryResponse(BaseModel):
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
# طرح‌های مربوط به Interpretation
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
# طرح‌های Optimization با EC و pH و auto_balance
# ============================================================
class OptimizationOptions(BaseModel):
    method: str = Field("nnls", description="روش بهینه‌سازی")
    element_weights: Optional[Dict[str, float]] = Field(None, description="وزن اهمیت هر عنصر")
    max_cost: Optional[float] = Field(None, ge=0, description="حداکثر هزینه مجاز")
    allow_zero_weights: bool = Field(True, description="آیا وزن صفر مجاز است؟")
    max_iterations: int = Field(1000, ge=1, description="حداکثر تعداد تکرار")
    tolerance: float = Field(1e-6, ge=0, description="تلورانس همگرایی")
    cost_weight: float = Field(0.01, ge=0, le=1, description="ضریب اهمیت هزینه")
    use_precipitation_check: bool = Field(True, description="بررسی رسوب")
    use_ion_balance_check: bool = Field(True, description="بررسی تعادل یونی")
    auto_balance: bool = Field(True, description="تعادل یونی خودکار")
    reservoir_mode: str = Field("auto", description="حالت مخازن")


class OptimizationFertilizerInput(BaseModel):
    id: str = Field(..., description="شناسه کود")
    name: str = Field(..., description="نام کود")
    elements: Dict[str, float] = Field(..., description="درصد عناصر تشکیل‌دهنده")
    price_per_kg: float = Field(..., ge=0, description="قیمت هر کیلوگرم")
    purity: float = Field(100.0, ge=0, le=100, description="درصد خلوص")
    is_acid: bool = Field(False, description="آیا اسید است؟")
    is_system_default: bool = Field(False, description="آیا کود سیستمی است؟")
    fixed_weight: Optional[float] = Field(None, ge=0, description="وزن ثابت")


class OptimizationRequest(BaseModel):
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف عناصر (ppm)")
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict, description="عناصر موجود در آب")
    fertilizers: List[OptimizationFertilizerInput] = Field(..., description="لیست کودهای موجود")
    options: Optional[OptimizationOptions] = Field(default_factory=lambda: OptimizationOptions(), description="تنظیمات بهینه‌سازی")
    tank_volume: float = Field(1000.0, ge=1, description="حجم مخزن (لیتر)")
    stock_volume: float = Field(100.0, ge=1, description="حجم استوک (لیتر)")
    injection_ratio: float = Field(100.0, ge=1, description="نسبت تزریق (1:X)")


class EcPhStatusResponse(BaseModel):
    status: str = Field(..., description="وضعیت کلی: optimal, warning, critical")
    status_label: str = Field(..., description="برچسب وضعیت")
    color: str = Field(..., description="رنگ: success, warning, danger")
    message: str = Field(..., description="پیام وضعیت")
    issues: List[str] = Field(default_factory=list, description="لیست مشکلات")
    recommendations: List[str] = Field(default_factory=list, description="لیست توصیه‌ها")
    ec: float = Field(..., description="مقدار EC")
    ph: float = Field(..., description="مقدار pH")
    water_ec: Optional[float] = Field(None, description="EC آب")
    water_ph: Optional[float] = Field(None, description="pH آب")
    ec_status: str = Field("", description="وضعیت EC")
    ec_label: str = Field("", description="برچسب EC")
    ph_status: str = Field("", description="وضعیت pH")
    ph_label: str = Field("", description="برچسب pH")


class OptimizationResponse(BaseModel):
    weights: Dict[str, float] = Field(..., description="وزن بهینه هر کود (گرم)")
    concentrations: Dict[str, float] = Field(..., description="غلظت نهایی عناصر (ppm)")
    residual_error: float = Field(..., description="خطای باقی‌مانده")
    cost_total: float = Field(..., description="هزینه کل (تومان)")
    ion_balance: IonBalanceResponse = Field(..., description="تعادل یونی")
    target_achievement: Dict[str, float] = Field(..., description="درصد تحقق هر عنصر")
    warnings: List[str] = Field(default_factory=list, description="هشدارها")
    suggestions: List[str] = Field(default_factory=list, description="پیشنهادات")
    reservoir_data: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="توزیع مواد در مخازن")
    iterations: int = Field(..., description="تعداد تکرارها")
    convergence_time_ms: float = Field(..., description="زمان محاسبه (میلی‌ثانیه)")
    is_converged: bool = Field(True, description="آیا الگوریتم به جواب رسید؟")
    summary: str = Field(..., description="خلاصه نتیجه به‌صورت متنی")
    ec: float = Field(0.0, description="EC نهایی (dS/m)")
    ph: float = Field(7.0, description="pH نهایی")
    ec_status: str = Field("", description="وضعیت EC")
    ph_status: str = Field("", description="وضعیت pH")
    ec_ph_status: EcPhStatusResponse = Field(..., description="وضعیت ترکیبی EC و pH")


class OptimizationLogResponse(BaseModel):
    id: int
    user_id: int
    report_id: Optional[int]
    target_values: Dict[str, float]
    water_values: Optional[Dict[str, float]]
    fertilizers_selected: Optional[Dict[str, Any]]
    optimized_weights: Optional[Dict[str, float]]
    final_concentrations: Optional[Dict[str, float]]
    residual_error: Optional[float]
    cost_total: Optional[float]
    iterations: Optional[int]
    convergence_time_ms: Optional[float]
    ion_balance: Optional[Dict[str, Any]]
    warnings: Optional[List[str]]
    suggestions: Optional[List[str]]
    is_successful: bool
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PrecipitationCheckRequest(BaseModel):
    concentrations: Dict[str, float] = Field(..., description="غلظت عناصر (ppm)")
    temperature: float = Field(25.0, ge=0, le=100, description="دما (درجه سانتی‌گراد)")


class PrecipitationRiskItem(BaseModel):
    compound: str = Field(..., description="نام ترکیب رسوب‌کننده")
    ion_product: float = Field(..., description="حاصل‌ضرب یونی فعلی")
    ksp: float = Field(..., description="ثابت حلالیت")
    is_risky: bool = Field(..., description="آیا خطرناک است؟")
    suggestion: str = Field(..., description="پیشنهاد اصلاحی")


class PrecipitationCheckResponse(BaseModel):
    is_safe: bool = Field(..., description="آیا ترکیب ایمن است؟")
    risks: List[PrecipitationRiskItem] = Field(default_factory=list, description="خطرات احتمالی")
    suggestions: List[str] = Field(default_factory=list, description="پیشنهادات اصلاحی")