# backend/app/schemas/optimization.py
"""
طرح‌های مربوط به بهینه‌سازی (Optimization)
شامل: OptimizationRequest, OptimizationResponse, OptimizationOptions, EcPhStatusResponse, etc.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .common import IonBalanceResponse


class OptimizationOptions(BaseModel):
    """تنظیمات بهینه‌سازی"""
    
    method: str = Field("nnls", description="روش بهینه‌سازی: nnls, lsq_linear, lsq_linear_with_cost")
    element_weights: Optional[Dict[str, float]] = Field(None, description="وزن اهمیت هر عنصر")
    max_cost: Optional[float] = Field(None, ge=0, description="حداکثر هزینه مجاز (تومان)")
    allow_zero_weights: bool = Field(True, description="آیا وزن صفر مجاز است؟")
    max_iterations: int = Field(1000, ge=1, description="حداکثر تعداد تکرار")
    tolerance: float = Field(1e-6, ge=0, description="تلورانس همگرایی")
    cost_weight: float = Field(0.01, ge=0, le=1, description="ضریب اهمیت هزینه در بهینه‌سازی")
    use_precipitation_check: bool = Field(True, description="بررسی رسوب")
    use_ion_balance_check: bool = Field(True, description="بررسی تعادل یونی")
    auto_balance: bool = Field(True, description="تعادل یونی خودکار (اضافه کردن Na یا Cl)")
    reservoir_mode: str = Field("auto", description="حالت مخازن: auto (خودکار), manual (دستی)")


class OptimizationFertilizerInput(BaseModel):
    """ورودی کود برای بهینه‌سازی"""
    
    id: str = Field(..., description="شناسه کود")
    name: str = Field(..., description="نام کود")
    elements: Dict[str, float] = Field(..., description="درصد عناصر تشکیل‌دهنده")
    price_per_kg: float = Field(..., ge=0, description="قیمت هر کیلوگرم")
    purity: float = Field(100.0, ge=0, le=100, description="درصد خلوص")
    is_acid: bool = Field(False, description="آیا اسید است؟")
    is_system_default: bool = Field(False, description="آیا کود سیستمی است؟")
    fixed_weight: Optional[float] = Field(None, ge=0, description="وزن ثابت (اگر کاربر تعیین کرده باشد)")


class OptimizationRequest(BaseModel):
    """درخواست بهینه‌سازی فرمول کود"""
    
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف عناصر (ppm)")
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict, description="عناصر موجود در آب (ppm) - شامل EC و pH")
    fertilizers: List[OptimizationFertilizerInput] = Field(..., description="لیست کودهای موجود با عناصر و قیمت")
    options: Optional[OptimizationOptions] = Field(default_factory=lambda: OptimizationOptions(), description="تنظیمات بهینه‌سازی")
    tank_volume: float = Field(1000.0, ge=1, description="حجم مخزن (لیتر)")
    stock_volume: float = Field(100.0, ge=1, description="حجم استوک (لیتر)")
    injection_ratio: float = Field(100.0, ge=1, description="نسبت تزریق (1:X)")


class EcPhStatusResponse(BaseModel):
    """وضعیت ترکیبی EC و pH"""
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
    """پاسخ بهینه‌سازی"""
    
    weights: Dict[str, float] = Field(..., description="وزن بهینه هر کود (گرم)")
    concentrations: Dict[str, float] = Field(..., description="غلظت نهایی عناصر (ppm)")
    residual_error: float = Field(..., description="خطای باقی‌مانده")
    cost_total: float = Field(..., description="هزینه کل (تومان)")
    ion_balance: IonBalanceResponse = Field(..., description="تعادل یونی")
    target_achievement: Dict[str, float] = Field(..., description="درصد تحقق هر عنصر (۰ تا ۱۰۰)")
    warnings: List[str] = Field(default_factory=list, description="هشدارها")
    suggestions: List[str] = Field(default_factory=list, description="پیشنهادات")
    reservoir_data: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="توزیع مواد در مخازن A, B, C")
    iterations: int = Field(..., description="تعداد تکرارها")
    convergence_time_ms: float = Field(..., description="زمان محاسبه (میلی‌ثانیه)")
    is_converged: bool = Field(True, description="آیا الگوریتم به جواب رسید؟")
    summary: str = Field(..., description="خلاصه نتیجه به‌صورت متنی")
    ec: float = Field(0.0, description="EC نهایی (dS/m)")
    ph: float = Field(7.0, description="pH نهایی")
    ec_status: str = Field("", description="وضعیت EC (مطلوب, کم, بالا, بحرانی)")
    ph_status: str = Field("", description="وضعیت pH (مطلوب, اسیدی, قلیایی, بحرانی)")
    ec_ph_status: EcPhStatusResponse = Field(..., description="وضعیت ترکیبی EC و pH")


class OptimizationLogResponse(BaseModel):
    """پاسخ تاریخچه بهینه‌سازی"""
    
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
    """درخواست بررسی رسوب"""
    
    concentrations: Dict[str, float] = Field(..., description="غلظت عناصر (ppm)")
    temperature: float = Field(25.0, ge=0, le=100, description="دما (درجه سانتی‌گراد)")


class PrecipitationRiskItem(BaseModel):
    """یک خطر رسوب"""
    
    compound: str = Field(..., description="نام ترکیب رسوب‌کننده")
    ion_product: float = Field(..., description="حاصل‌ضرب یونی فعلی")
    ksp: float = Field(..., description="ثابت حلالیت")
    is_risky: bool = Field(..., description="آیا خطرناک است؟")
    suggestion: str = Field(..., description="پیشنهاد اصلاحی")


class PrecipitationCheckResponse(BaseModel):
    """پاسخ بررسی رسوب"""
    
    is_safe: bool = Field(..., description="آیا ترکیب ایمن است؟")
    risks: List[PrecipitationRiskItem] = Field(default_factory=list, description="خطرات احتمالی")
    suggestions: List[str] = Field(default_factory=list, description="پیشنهادات اصلاحی")