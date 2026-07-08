# backend/app/schemas/report.py
"""
طرح‌های مربوط به Report (گزارش)
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    """طرح ایجاد گزارش جدید"""
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = Field(None, description="تاریخ شمسی")


class ReportUpdate(BaseModel):
    """طرح به‌روزرسانی گزارش"""
    report_name: Optional[str] = Field(None, max_length=100)
    plant_name: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    growth_stage: Optional[str] = Field(None, max_length=50)
    report_date: Optional[str] = None


class ReportResponse(BaseModel):
    """طرح پاسخ گزارش"""
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