# backend/app/schemas/ph_calculator.py
"""طرح‌های مربوط به ماشین‌حساب pH"""
from typing import Dict, List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================
# ماده‌ی شیمیایی (اسید/باز انتخابی)
# ============================================================
class ChemicalInput(BaseModel):
    """
    ماده‌ی شیمیایی مورد استفاده در محاسبه.
    اگر fertilizer_id داده شود، سرور مقادیر mw/z/purity_pct را از
    پایگاه‌داده‌ی کود واقعی کاربر می‌خواند (density_g_ml اگر داده نشود
    از جدول مرجع resolve می‌شود). اگر fertilizer_id داده نشود، همه‌ی
    فیلدها باید دستی وارد شوند (اسید/باز سفارشی).
    """
    fertilizer_id: Optional[int] = Field(None, description="شناسه‌ی کود اسیدی/بازی از پایگاه‌داده کود")
    name: Optional[str] = Field(None, max_length=100)
    kind: Optional[Literal["acid", "base"]] = None
    mw: Optional[float] = Field(None, gt=0, description="جرم مولی g/mol (برای ماده‌ی سفارشی الزامی)")
    z: Optional[float] = Field(None, gt=0, description="ظرفیت مؤثر (برای اسید فسفریک از fertilizer_id خودکار تشخیص داده می‌شود)")
    purity_pct: Optional[float] = Field(None, gt=0, le=100, description="خلوص وزنی ٪ (اگر ندهید و fertilizer_id بدهید از پایگاه‌داده خوانده می‌شود)")
    density_g_ml: Optional[float] = Field(None, gt=0, description="چگالی g/mL (اگر ندهید، از جدول مرجع یا پایگاه‌داده تخمین زده می‌شود)")


class ChemicalOutput(BaseModel):
    id: str
    name: str
    formula: str
    kind: str
    mw: float
    z: str  # عدد به صورت رشته یا 'phosphoric'
    purity_pct: float
    density_g_ml: float
    source: str
    fertilizer_id: Optional[int] = None
    density_is_reference: bool = Field(
        False, description="اگر True باشد، چگالی از جدول مرجع صنعتی تخمین زده شده (نه از SDS واقعی محصول)"
    )
    density_extrapolated: bool = Field(
        False, description="اگر True باشد، درصد خلوص خارج از بازه‌ی جدول مرجع چگالی بوده است"
    )


# ============================================================
# لیست اسیدهای/بازهای موجود در پایگاه‌داده کود (dropdown)
# ============================================================
class AcidOption(BaseModel):
    fertilizer_id: int
    name: str
    acid_type: Optional[str] = None
    concentration: float
    form: Optional[str] = None
    is_system_default: bool = False
    recognized: bool = Field(..., description="آیا acid_type در جدول ثابت‌های شیمیایی شناخته‌شده است")
    suggested_mw: Optional[float] = None
    suggested_z: Optional[str] = None
    suggested_density_g_ml: Optional[float] = None
    density_extrapolated: bool = False


# ============================================================
# درخواست‌های محاسبه
# ============================================================
class TheoreticalRequest(BaseModel):
    volume_l: float = Field(..., gt=0)
    current_ph: float = Field(..., ge=0, le=14)
    target_ph: float = Field(..., ge=0, le=14)
    temperature_c: float = Field(25.0, ge=0, le=60)
    alkalinity_value: float = Field(..., gt=0)
    alkalinity_unit: Literal["mg_l_caco3", "meq_l"] = "mg_l_caco3"
    sample_type: Literal["simple", "complex"] = "simple"
    chemical: ChemicalInput
    report_id: Optional[int] = None
    save: bool = False
    note: Optional[str] = Field(None, max_length=500)


class TitrationPointInput(BaseModel):
    volume_ml: float = Field(..., gt=0)
    ph: float = Field(..., ge=0, le=14)


class TitrationRequest(BaseModel):
    volume_l: float = Field(..., gt=0)
    current_ph: float = Field(..., ge=0, le=14)
    target_ph: float = Field(..., ge=0, le=14)
    temperature_c: float = Field(25.0, ge=0, le=60)
    normality: float = Field(..., gt=0)
    sample_volume_ml: float = Field(..., gt=0)
    points: List[TitrationPointInput] = Field(..., min_items=1, max_items=40)
    chemical: ChemicalInput
    report_id: Optional[int] = None
    save: bool = False
    note: Optional[str] = Field(None, max_length=500)


# ============================================================
# پاسخ محاسبه
# ============================================================
class TheoreticalDetail(BaseModel):
    ct_mmol_l: float
    initial_alk_mg_l: float
    target_alk_mg_l: float
    delta_meq_l: float
    pK1: float
    pK2: float


class TitrationDetail(BaseModel):
    from_volume_ml: float
    to_volume_ml: float
    dose_ml: float
    meq_per_l: float


class Sensitivity(BaseModel):
    min_l: float
    max_l: float


class DoseResponse(BaseModel):
    ok: bool = True
    method: Literal["theoretical", "titration", "no-adjustment"]
    direction: Literal["acid", "base", "none"]
    total_meq: float
    effective_z: float
    pure_mass_g: float
    commercial_mass_g: float
    commercial_volume_l: float
    warnings: List[str] = []
    sensitivity: Optional[Sensitivity] = None
    theoretical: Optional[TheoreticalDetail] = None
    titration: Optional[TitrationDetail] = None
    chemical: ChemicalOutput
    saved_id: Optional[int] = None


class DoseErrorResponse(BaseModel):
    ok: bool = False
    error: str
    need_titration: bool = False


# ============================================================
# تاریخچه
# ============================================================
class PhHistoryItem(BaseModel):
    id: int
    report_id: Optional[int] = None
    method: str
    direction: Optional[str] = None
    chemical_name: Optional[str] = None
    inputs: dict
    outputs: dict
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# داده‌ی زمینه (context) - برای پیش‌پرکردن/نمایش اطلاعاتی صفحه
# بدون دست‌کاری صفحات آنالیز آب و عناصر هدف
# ============================================================
class PhContextResponse(BaseModel):
    water_salinity: Optional[float] = None
    water_values: Optional[Dict[str, float]] = None
    target_elements: Optional[Dict[str, float]] = None
    target_unit: Optional[str] = None
    is_likely_complex_solution: bool = Field(
        False,
        description="اگر عناصر هدف شامل فسفات/آمونیوم/... باشند که ظرفیت اسیدی/بازی را تحت تأثیر قرار می‌دهند، True است و پیشنهاد می‌شود sample_type روی complex باشد"
    )
    complex_indicator_elements: List[str] = []
    latest_reservoir_c: Optional[List[dict]] = Field(
        None, description="اسیدهای مخزن C از آخرین محاسبه‌ی ذخیره‌شده‌ی این گزارش (فقط اطلاعاتی)"
    )
