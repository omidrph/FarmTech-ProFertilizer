# backend/app/schemas/report.py
"""
طرح‌های مربوط به Report (گزارش)
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    """طرح ایجاد گزارش جدید"""
    report_name: str = Field(..., min_length=1, max_length=100)
    plant_name: str = Field(..., min_length=1, max_length=50)
    season: str = Field(..., min_length=1, max_length=20)
    growth_stage: str = Field(..., min_length=1, max_length=50)
    report_date: str = Field(..., min_length=1, description="تاریخ شمسی")


class ReportUpdate(BaseModel):
    """طرح به‌روزرسانی گزارش"""
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = None
    is_recirculating_system: Optional[bool] = Field(
        None, description="آیا سیستم بازچرخشی (هیدروپونیک بسته) است؟ (برای تب PH)"
    )


class ReportResponse(BaseModel):
    """طرح پاسخ گزارش"""
    id: int
    user_id: int
    report_name: Optional[str]
    plant_name: Optional[str]
    season: Optional[str]
    growth_stage: Optional[str]
    report_date: Optional[str]
    is_recirculating_system: Optional[bool] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True




