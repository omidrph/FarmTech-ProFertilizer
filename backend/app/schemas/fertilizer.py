# backend/app/schemas/fertilizer.py
"""
طرح‌های مربوط به Fertilizer (کود)
"""

from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, validator
import re

from .base import validate_name


class FertilizerCreate(BaseModel):
    """طرح ایجاد کود جدید - فقط name اجباری است"""
    
    name: str = Field(..., min_length=1, max_length=100, description="نام کود (اجباری)")
    brand: Optional[str] = Field(None, max_length=100, description="برند/شرکت")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    form: Optional[str] = Field(None, max_length=20, description="فرم فیزیکی: liquid, powder, crystal, granular")
    concentration: Optional[float] = Field(100.0, ge=0, le=100, description="درصد خلوص/غلظت")
    elements: Optional[Dict[str, float]] = Field(default_factory=dict, description="درصد عناصر")
    price_per_kg: Optional[float] = Field(0.0, ge=0, description="قیمت هر کیلوگرم")
    is_acid: bool = Field(False, description="آیا اسید است؟")
    acid_type: Optional[str] = Field(None, max_length=10, description="نوع اسید: H3PO4, HNO3, H2SO4")
    ph_level: Optional[float] = Field(None, ge=0, le=14, description="pH محلول")
    description: Optional[str] = Field(None, description="توضیحات")
    is_system_default: bool = Field(False, description="آیا کود سیستمی است؟")
    source_system_id: Optional[int] = Field(None, description="ID کود سیستمی مبدا")
    
    @validator('name')
    def validate_name_field(cls, v):
        # جلوگیری از XSS و SQL Injection
        if any(char in v for char in ['<', '>', '"', "'", ';', '--', '/*', '*/']):
            raise ValueError('نام کود حاوی کاراکترهای غیرمجاز است')
        return v.strip()
    
    @validator('elements')
    def validate_elements(cls, v):
        if v:
            for key, value in v.items():
                if not re.match(r'^[A-Za-z0-9\-]+$', key):
                    raise ValueError(f'نام عنصر {key} نامعتبر است')
                if not (0 <= value <= 100):
                    raise ValueError(f'مقدار عنصر {key} باید بین 0 تا 100 باشد')
        return v


class FertilizerUpdate(BaseModel):
    """طرح به‌روزرسانی کود - همه فیلدها اختیاری"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    form: Optional[str] = Field(None, max_length=20)
    concentration: Optional[float] = Field(None, ge=0, le=100)
    elements: Optional[Dict[str, float]] = None
    price_per_kg: Optional[float] = Field(None, ge=0)
    is_acid: Optional[bool] = None
    acid_type: Optional[str] = Field(None, max_length=10)
    ph_level: Optional[float] = Field(None, ge=0, le=14)
    description: Optional[str] = None
    is_system_default: Optional[bool] = None
    source_system_id: Optional[int] = None
    
    @validator('name')
    def validate_name_field(cls, v):
        if v and any(char in v for char in ['<', '>', '"', "'", ';', '--', '/*', '*/']):
            raise ValueError('نام کود حاوی کاراکترهای غیرمجاز است')
        return v.strip() if v else v


class FertilizerResponse(BaseModel):
    """طرح پاسخ کود - شامل همه فیلدها"""
    
    id: int
    user_id: Optional[int]
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    form: Optional[str] = None
    concentration: Optional[float] = 100.0
    elements: Optional[Dict[str, float]] = None
    price_per_kg: Optional[float] = 0.0
    is_acid: bool = False
    acid_type: Optional[str] = None
    ph_level: Optional[float] = None
    description: Optional[str] = None
    is_system_default: bool = False
    source_system_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True