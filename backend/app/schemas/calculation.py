
# backend/app/schemas/calculation.py
"""
طرح‌های مربوط به Calculation (محاسبات)
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


class CalculationCreate(BaseModel):
    """طرح ایجاد محاسبات جدید"""
    target_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    final_values: Optional[Dict[str, float]] = Field(default_factory=dict)
    reservoir_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    calc_rows: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    interpretation: Optional[str] = None
    # 🆕 برای بازیابی کامل صفحه محاسبه کود بدون محاسبه مجدد
    selected_fertilizer_ids: Optional[List[str]] = Field(default_factory=list)
    optimization_options: Optional[Dict[str, Any]] = Field(default_factory=dict)
    optimization_result: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CalculationUpdate(BaseModel):
    """طرح به‌روزرسانی محاسبات"""
    target_values: Optional[Dict[str, float]] = None
    final_values: Optional[Dict[str, float]] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    calc_rows: Optional[List[Dict[str, Any]]] = None
    interpretation: Optional[str] = None
    # 🆕
    selected_fertilizer_ids: Optional[List[str]] = None
    optimization_options: Optional[Dict[str, Any]] = None
    optimization_result: Optional[Dict[str, Any]] = None


class CalculationResponse(BaseModel):
    """طرح پاسخ محاسبات"""
    id: int
    report_id: int
    target_values: Optional[Dict[str, float]] = None
    final_values: Optional[Dict[str, float]] = None
    reservoir_data: Optional[Dict[str, Any]] = None
    calc_rows: Optional[List[Dict[str, Any]]] = None
    interpretation: Optional[str] = None
    # 🆕
    selected_fertilizer_ids: Optional[List[str]] = None
    optimization_options: Optional[Dict[str, Any]] = None
    optimization_result: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
