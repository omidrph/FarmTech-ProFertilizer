# backend/app/schemas/water_analysis.py
"""
طرح‌های مربوط به WaterAnalysis (آنالیز آب)
"""

from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


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
    wastewater_values: Optional[Dict[str, float]] = None
    water_values: Optional[Dict[str, float]] = None
    created_at: datetime

    class Config:
        from_attributes = True