# backend/app/schemas/interpretation.py
"""
طرح‌های مربوط به Interpretation (تفسیر داده‌ها)
"""

from typing import List
from pydantic import BaseModel

from .common import IonBalanceResponse


class ElementStatusResponse(BaseModel):
    """وضعیت یک عنصر"""
    element: str
    target: float
    actual: float
    difference: float
    status: str  # deficient, sufficient, excessive, toxic
    message: str


class WaterQualityResponse(BaseModel):
    """وضعیت کیفیت آب"""
    salinity: float
    impact: str  # مناسب, متوسط, بالا
    recommendation: str


class RecommendationResponse(BaseModel):
    """یک توصیه کودی"""
    issue: str
    suggestion: str
    priority: str  # high, medium, low


class InterpretationResponse(BaseModel):
    """پاسخ تفسیر کامل"""
    ion_balance: IonBalanceResponse
    element_status: List[ElementStatusResponse]
    water_quality: WaterQualityResponse
    fertilizer_recommendation: List[RecommendationResponse]
    summary: str