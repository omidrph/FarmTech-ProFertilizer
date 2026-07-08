# backend/app/schemas/water_template.py
"""
طرح‌های مربوط به WaterAnalysisTemplate (قالب آنالیز آب)
"""

from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class WaterAnalysisTemplateCreate(BaseModel):
    """طرح ایجاد قالب آنالیز آب جدید"""
    name: str = Field(..., min_length=1, max_length=100, description="نام قالب")
    description: Optional[str] = Field(None, description="توضیحات")
    water_percentage: float = Field(100.0, ge=0, le=100)
    wastewater_percentage: float = Field(0.0, ge=0, le=100)
    water_salinity: float = Field(0.8, ge=0)
    water_salinity_unit: str = Field('dS/m', description="واحد EC: dS/m, mS/cm, μS/cm")
    water_ph: Optional[float] = Field(None, ge=0, le=14)
    water_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    wastewater_values: Optional[Dict[str, float]] = Field(default_factory=dict)


class WaterAnalysisTemplateUpdate(BaseModel):
    """طرح به‌روزرسانی قالب آنالیز آب"""
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
    """طرح پاسخ قالب آنالیز آب"""
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