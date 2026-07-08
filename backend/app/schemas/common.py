# backend/app/schemas/common.py
"""
طرح‌های عمومی و مشترک
شامل: IonBalance, FinalSolution, Reservoir, UnitConversion, HomeSummary, Message, Paginated
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============================================================
# طرح‌های مربوط به APIهای محاسباتی
# ============================================================

class IonBalanceRequest(BaseModel):
    """درخواست محاسبه تعادل یونی"""
    elements: Dict[str, float] = Field(..., description="مقادیر عناصر")
    unit: str = Field("ppm", description="واحد (ppm, meq, mmol)")


class IonBalanceResponse(BaseModel):
    """پاسخ تعادل یونی"""
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
    """پاسخ محلول نهایی"""
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
    """داده یک عنصر در خلاصه خانه"""
    element: str
    target: float
    actual: float
    difference: float
    progress_percent: float


class HomeSummaryRecommendation(BaseModel):
    """یک توصیه در خلاصه خانه"""
    type: str  # success, warning, danger
    title: str
    description: str


class HomeSummaryResponse(BaseModel):
    """پاسخ خلاصه خانه"""
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
# طرح‌های عمومی
# ============================================================

class MessageResponse(BaseModel):
    """پاسخ پیام عمومی"""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    """پاسخ لیست صفحه‌بندی شده"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int