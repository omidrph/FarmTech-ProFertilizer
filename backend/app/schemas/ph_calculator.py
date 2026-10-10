# backend/app/schemas/ph_calculator.py
"""طرح‌های «اصلاح pH» (روش نسبتی: رسپی مشخص یا آزمون روی نمونه)"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


# ============================================================
# لیست اسید/بازهای پایگاه‌داده‌ی کود کاربر
# ============================================================
class AdjusterOption(BaseModel):
    fertilizer_id: int
    name: str
    kind: Literal["acid", "base"]
    acid_type: Optional[str] = None
    form: Optional[str] = None
    concentration: float = Field(..., description="درصد خلوص ثبت‌شده در پایگاه‌داده کود")
    dose_unit: Literal["ml", "g"] = Field(..., description="واحد مقدار مصرفی: مایع=mL، جامد=g")
    elements_pct: Dict[str, float] = Field(default_factory=dict, description="درصد وزنی عناصر در محصول تجاری")
    elements_source: Literal["database", "derived", "missing"] = "database"
    density_g_ml: Optional[float] = Field(None, description="چگالی مرجع (فقط برای مایعات)")
    density_is_reference: bool = False
    density_extrapolated: bool = False
    recognized: bool = Field(False, description="نوع در جدول مشخصات شناخته‌شده است")
    warnings: List[str] = Field(default_factory=list)


# ============================================================
# درخواست محاسبه / ثبت
# ============================================================
class TrialStepInput(BaseModel):
    amount: float = Field(..., gt=0, description="مقدار اضافه‌شده در همین مرحله (mL یا g)")
    ph: float = Field(..., ge=0, le=14, description="pH پس از همین مرحله")


class AdjustmentRequest(BaseModel):
    mode: Literal["known", "trial"]
    fertilizer_id: int
    tank_volume_l: float = Field(..., gt=0, le=10_000_000)
    initial_ph: Optional[float] = Field(None, ge=0, le=14)
    target_ph: Optional[float] = Field(None, ge=0, le=14)
    density_g_ml: Optional[float] = Field(None, gt=0, le=5, description="چگالی دقیق برگهٔ SDS (فقط مایعات)")

    # --- حالت رسپی ---
    dose_amount: Optional[float] = Field(None, gt=0, description="مقدار ماده در رسپی (mL یا g)")
    dose_basis_volume_l: Optional[float] = Field(
        None, gt=0, description="رسپی برای چند لیتر محلول است (پیش‌فرض: همان حجم مخزن)"
    )

    # --- حالت آزمون و خطا ---
    sample_volume_l: Optional[float] = Field(None, gt=0, le=1000)
    steps: List[TrialStepInput] = Field(default_factory=list, max_length=60)

    report_id: Optional[int] = Field(None, description="برای مقایسه با آلکالینیتی آب و EC پایهٔ گزارش")

    @model_validator(mode="after")
    def _check_mode_fields(self):
        if self.mode == "known":
            if self.dose_amount is None:
                raise ValueError("در حالت رسپی، مقدار ماده الزامی است.")
        else:
            if self.initial_ph is None or self.target_ph is None:
                raise ValueError("در حالت آزمون و خطا، pH اولیه و pH هدف الزامی‌اند.")
            if self.sample_volume_l is None:
                raise ValueError("حجم نمونه الزامی است.")
            if not self.steps:
                raise ValueError("حداقل یک مرحله (مقدار و pH) وارد کنید.")
        return self


class AdjustmentSaveRequest(AdjustmentRequest):
    report_id: int = Field(..., description="گزارشی که این اصلاح روی آن ثبت می‌شود")
    note: Optional[str] = Field(None, max_length=500)
    ec_before: Optional[float] = Field(None, ge=0, le=30, description="EC اندازه‌گیری‌شده قبل از اصلاح (dS/m)")
    ec_after: Optional[float] = Field(None, ge=0, le=30, description="EC اندازه‌گیری‌شده بعد از اصلاح (dS/m)")
    apply: bool = Field(False, description="هم‌زمان در چرخهٔ محاسبهٔ گزارش اعمال شود")


class AdjustmentUpdate(BaseModel):
    """ویرایش فیلدهای توصیفی یک رکورد تاریخچه (خود دوز/نتیجه تغییر نمی‌کند؛ برای آن «استفاده مجدد» کنید)"""
    note: Optional[str] = Field(None, max_length=500)
    ec_before: Optional[float] = Field(None, ge=0, le=30)
    ec_after: Optional[float] = Field(None, ge=0, le=30)


# ============================================================
# پاسخ محاسبه
# ============================================================
class ChemicalSnapshot(BaseModel):
    fertilizer_id: Optional[int] = None
    name: str
    kind: Literal["acid", "base"]
    acid_type: Optional[str] = None
    form: Optional[str] = None
    purity_pct: float
    density_g_ml: Optional[float] = None
    density_is_reference: bool = False
    elements_pct: Dict[str, float] = Field(default_factory=dict)
    elements_source: str = "database"


class CurvePoint(BaseModel):
    amount: float
    ph: float


class AdjustmentResult(BaseModel):
    ok: bool = True
    mode: Literal["known", "trial"]
    kind: Literal["acid", "base"]
    chemical: ChemicalSnapshot
    dose_unit: Literal["ml", "g"]
    tank_volume_l: float
    initial_ph: Optional[float] = None
    target_ph: Optional[float] = None
    final_ph: Optional[float] = None

    dose_tank: float = Field(..., description="مقدار برای کل مخزن (mL یا g)")
    dose_per_1000l: float
    commercial_mass_g: float = Field(..., description="جرم محصول تجاری (g)")
    pure_mass_g: float = Field(..., description="جرم ماده‌ی خالص (g)")
    stage_first: float = Field(..., description="مقدار مرحلهٔ اول (۷۰٪ دوز)")
    stage_rest: float

    # trial
    sample_volume_l: Optional[float] = None
    scale_factor: Optional[float] = None
    sample_dose: Optional[float] = None
    trial_method: Optional[Literal["interpolated", "measured"]] = None
    curve: List[CurvePoint] = Field(default_factory=list)
    # known
    dose_basis_volume_l: Optional[float] = None

    element_contributions: Dict[str, float] = Field(default_factory=dict, description="mg/L در محلول نهایی")
    strength_meq_l: float = 0.0
    water_alkalinity_meq_l: Optional[float] = None
    ec_delta: float = 0.0
    base_ec: Optional[float] = Field(None, description="EC آخرین محاسبهٔ گزارش (بدون این اصلاح)")
    predicted_ec: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)


# ============================================================
# رکورد ذخیره‌شده (تاریخچه)
# ============================================================
class AdjustmentItem(BaseModel):
    id: int
    report_id: int
    mode: Literal["known", "trial"]
    kind: Literal["acid", "base"]
    fertilizer_id: Optional[int] = None
    chemical_name: str
    chemical: dict
    tank_volume_l: float
    initial_ph: Optional[float] = None
    target_ph: Optional[float] = None
    final_ph: Optional[float] = None
    sample_volume_l: Optional[float] = None
    trial_steps: Optional[List[dict]] = None
    dose_unit: Literal["ml", "g"]
    dose_tank: float
    dose_per_1000l: float
    element_contributions: Dict[str, float]
    ec_delta: Optional[float] = None
    ec_before: Optional[float] = None
    ec_after: Optional[float] = None
    note: Optional[str] = None
    is_active: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActiveAdjustmentSummary(BaseModel):
    """خلاصهٔ اصلاح فعال - برای نمایش در صفحهٔ محاسبهٔ کود و پاسخ بهینه‌ساز"""
    id: int
    chemical_name: str
    kind: Literal["acid", "base"]
    mode: Literal["known", "trial"]
    dose_unit: Literal["ml", "g"]
    dose_tank: float
    dose_per_1000l: float
    tank_volume_l: float
    initial_ph: Optional[float] = None
    target_ph: Optional[float] = None
    final_ph: Optional[float] = None
    element_contributions: Dict[str, float]
    ec_delta: Optional[float] = None
    updated_at: Optional[datetime] = None


# ============================================================
# زمینهٔ صفحهٔ PH
# ============================================================
class PhContextResponse(BaseModel):
    plant_name: Optional[str] = None
    tank_volume_l: Optional[float] = Field(None, description="حجم مخزن اصلی از آخرین محاسبهٔ گزارش")
    water_ph: Optional[float] = None
    water_alkalinity_ppm: Optional[float] = None
    base_ec: Optional[float] = Field(None, description="EC آخرین محاسبه (dS/m)، بدون اصلاح فعال")
    suggested_target_ph: float = 6.0
    target_ph_range: List[float] = [5.5, 6.5]
    active: Optional[ActiveAdjustmentSummary] = None
