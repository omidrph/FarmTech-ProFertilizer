# backend/app/schemas/recipe.py
"""
طرح‌های مربوط به Recipe (رسپی)
"""

from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    """طرح پایه رسپی"""
    name: str = Field(..., min_length=1, max_length=100, description="نام رسپی")
    description: Optional[str] = Field(None, description="توضیحات")
    target_values: Dict[str, float] = Field(..., description="مقادیر هدف عناصر")
    category: Optional[str] = Field(None, max_length=50, description="دسته‌بندی")
    stage: Optional[str] = Field(None, max_length=50, description="مرحله رشد")
    is_system: bool = Field(False, description="آیا رسپی سیستمی است؟")


class RecipeCreate(RecipeBase):
    """طرح ایجاد رسپی جدید"""
    pass


class RecipeUpdate(BaseModel):
    """طرح به‌روزرسانی رسپی"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    target_values: Optional[Dict[str, float]] = None
    category: Optional[str] = Field(None, max_length=50)
    stage: Optional[str] = Field(None, max_length=50)


class RecipeResponse(BaseModel):
    """طرح پاسخ رسپی"""
    id: int
    name: str
    description: Optional[str]
    target_values: Dict[str, float]
    category: Optional[str]
    stage: Optional[str]
    is_system: bool
    user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    """طرح پاسخ لیست رسپی‌ها"""
    system_recipes: List[RecipeResponse]
    user_recipes: List[RecipeResponse]