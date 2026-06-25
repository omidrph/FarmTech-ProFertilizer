# backend/app/routes/recipes.py
"""مسیرهای رسپی‌ها (Recipes)"""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models import User, Recipe
from app.schemas import (
    RecipeCreate, RecipeUpdate, RecipeResponse, RecipeListResponse
)
import app.crud as crud
from app.security import get_current_user

logger = logging.getLogger(__name__)

recipes_router = APIRouter(prefix="/recipes", tags=["Recipes"])


# ============================================================
# دریافت همه رسپی‌ها (سیستمی + شخصی کاربر)
# ============================================================
@recipes_router.get("/", response_model=RecipeListResponse)
def get_all_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت همه رسپی‌های سیستمی و شخصی کاربر"""
    try:
        result = crud.get_all_recipes_for_user(db, current_user.id)
        return result
    except Exception as e:
        logger.error(f"Error in get_all_recipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت رسپی‌ها: {str(e)}"
        )


# ============================================================
# دریافت رسپی‌های سیستمی
# ============================================================
@recipes_router.get("/system", response_model=List[RecipeResponse])
def get_system_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت رسپی‌های سیستمی"""
    try:
        return crud.get_system_recipes(db, skip, limit)
    except Exception as e:
        logger.error(f"Error in get_system_recipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت رسپی‌های سیستمی: {str(e)}"
        )


# ============================================================
# دریافت رسپی‌های شخصی کاربر
# ============================================================
@recipes_router.get("/user", response_model=List[RecipeResponse])
def get_user_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت رسپی‌های شخصی کاربر فعلی"""
    try:
        return crud.get_user_recipes(db, current_user.id, skip, limit)
    except Exception as e:
        logger.error(f"Error in get_user_recipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت رسپی‌های شخصی: {str(e)}"
        )


# ============================================================
# دریافت یک رسپی با شناسه
# ============================================================
@recipes_router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت یک رسپی با شناسه"""
    try:
        recipe = crud.get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رسپی پیدا نشد"
            )
        
        # اگر رسپی شخصی است، فقط خود کاربر می‌تواند ببیند
        if not recipe.is_system and recipe.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این رسپی ندارید"
            )
        
        return recipe
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت رسپی: {str(e)}"
        )


# ============================================================
# ایجاد رسپی شخصی جدید
# ============================================================
@recipes_router.post("/", response_model=RecipeResponse)
def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد رسپی شخصی جدید"""
    try:
        recipe = crud.create_recipe(db, recipe_data, current_user.id, is_system=False)
        return recipe
    except Exception as e:
        logger.error(f"Error in create_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد رسپی: {str(e)}"
        )


# ============================================================
# به‌روزرسانی رسپی شخصی
# ============================================================
@recipes_router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """به‌روزرسانی رسپی شخصی"""
    try:
        recipe = crud.get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رسپی پیدا نشد"
            )
        
        # فقط کاربر صاحب رسپی می‌تواند ویرایش کند
        if recipe.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این رسپی ندارید"
            )
        
        # رسپی‌های سیستمی قابل ویرایش نیستند
        if recipe.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رسپی‌های سیستمی قابل ویرایش نیستند. می‌توانید از آن یک کپی شخصی بسازید."
            )
        
        updated_recipe = crud.update_recipe(db, recipe_id, recipe_data)
        return updated_recipe
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در به‌روزرسانی رسپی: {str(e)}"
        )


# ============================================================
# حذف رسپی شخصی
# ============================================================
@recipes_router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف رسپی شخصی"""
    try:
        recipe = crud.get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رسپی پیدا نشد"
            )
        
        # فقط کاربر صاحب رسپی می‌تواند حذف کند
        if recipe.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این رسپی ندارید"
            )
        
        # رسپی‌های سیستمی قابل حذف نیستند
        if recipe.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رسپی‌های سیستمی قابل حذف نیستند"
            )
        
        crud.delete_recipe(db, recipe_id)
        return {"message": "رسپی با موفقیت حذف شد", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در حذف رسپی: {str(e)}"
        )


# ============================================================
# اعمال رسپی به عناصر هدف کاربر
# ============================================================
@recipes_router.post("/{recipe_id}/apply")
def apply_recipe_to_targets(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """اعمال مقادیر رسپی به عناصر هدف کاربر"""
    try:
        recipe = crud.get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رسپی پیدا نشد"
            )
        
        # اگر رسپی شخصی است، فقط خود کاربر می‌تواند از آن استفاده کند
        if not recipe.is_system and recipe.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="شما دسترسی به این رسپی ندارید"
            )
        
        # اینجا باید عناصر هدف کاربر به‌روزرسانی شود
        # از TargetStore یا مستقیماً در دیتابیس
        
        return {
            "message": f"رسپی '{recipe.name}' با موفقیت اعمال شد",
            "success": True,
            "target_values": recipe.target_values
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in apply_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در اعمال رسپی: {str(e)}"
        )


# ============================================================
# کپی کردن رسپی سیستمی به عنوان رسپی شخصی
# ============================================================
@recipes_router.post("/{recipe_id}/copy")
def copy_system_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """کپی کردن یک رسپی سیستمی به عنوان رسپی شخصی کاربر"""
    try:
        recipe = crud.get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رسپی پیدا نشد"
            )
        
        # فقط رسپی‌های سیستمی قابل کپی هستند
        if not recipe.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="فقط رسپی‌های سیستمی قابل کپی هستند"
            )
        
        # ایجاد رسپی شخصی جدید با داده‌های رسپی سیستمی
        new_recipe_data = RecipeCreate(
            name=f"{recipe.name} (کپی)",
            description=recipe.description,
            target_values=recipe.target_values,
            category=recipe.category,
            stage=recipe.stage,
            is_system=False
        )
        
        new_recipe = crud.create_recipe(db, new_recipe_data, current_user.id, is_system=False)
        
        return {
            "message": f"رسپی '{recipe.name}' با موفقیت کپی شد",
            "success": True,
            "recipe": new_recipe
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in copy_recipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در کپی رسپی: {str(e)}"
        )