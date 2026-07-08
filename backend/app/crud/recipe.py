# backend/app/crud/recipe.py
"""
عملیات CRUD برای مدل Recipe (رسپی)
"""

from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import logging

from app.models import Recipe
from app.schemas import RecipeCreate, RecipeUpdate

logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای Recipe (رسپی)
# ============================================================

def create_recipe(db: Session, recipe_data: RecipeCreate, user_id: Optional[int] = None, is_system: bool = False) -> Recipe:
    """ایجاد رسپی جدید"""
    try:
        db_recipe = Recipe(
            name=recipe_data.name,
            description=recipe_data.description,
            target_values=recipe_data.target_values,
            category=recipe_data.category,
            stage=recipe_data.stage,
            is_system=is_system,
            user_id=user_id if not is_system else None
        )
        
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        
        logger.info(f"Recipe created: {db_recipe.id} - {db_recipe.name} (system={is_system})")
        return db_recipe
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating recipe: {e}")
        raise e


def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
    """دریافت رسپی با شناسه"""
    try:
        return db.query(Recipe).filter(Recipe.id == recipe_id).first()
    except Exception as e:
        logger.error(f"Error getting recipe by id: {e}")
        return None


def get_system_recipes(db: Session, skip: int = 0, limit: int = 100) -> List[Recipe]:
    """دریافت رسپی‌های سیستمی"""
    try:
        return db.query(Recipe).filter(
            Recipe.is_system == True
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting system recipes: {e}")
        return []


def get_user_recipes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Recipe]:
    """دریافت رسپی‌های شخصی کاربر"""
    try:
        return db.query(Recipe).filter(
            Recipe.user_id == user_id,
            Recipe.is_system == False
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting user recipes: {e}")
        return []


def get_all_recipes_for_user(db: Session, user_id: int) -> Dict[str, List[Recipe]]:
    """دریافت همه رسپی‌ها (سیستمی + شخصی) برای یک کاربر"""
    try:
        system = get_system_recipes(db)
        user = get_user_recipes(db, user_id)
        return {
            "system_recipes": system,
            "user_recipes": user
        }
    except Exception as e:
        logger.error(f"Error getting all recipes for user: {e}")
        return {"system_recipes": [], "user_recipes": []}


def update_recipe(db: Session, recipe_id: int, recipe_data: RecipeUpdate) -> Optional[Recipe]:
    """به‌روزرسانی رسپی"""
    try:
        db_recipe = get_recipe_by_id(db, recipe_id)
        
        if db_recipe is None:
            return None
        
        update_data = recipe_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_recipe, key, value)
        
        db.commit()
        db.refresh(db_recipe)
        
        logger.info(f"Recipe updated: {recipe_id}")
        return db_recipe
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating recipe: {e}")
        raise e


def delete_recipe(db: Session, recipe_id: int) -> bool:
    """حذف رسپی"""
    try:
        db_recipe = get_recipe_by_id(db, recipe_id)
        
        if db_recipe is None:
            return False
        
        # رسپی‌های سیستمی قابل حذف نیستند
        if db_recipe.is_system:
            logger.warning(f"Cannot delete system recipe: {recipe_id}")
            return False
        
        db.delete(db_recipe)
        db.commit()
        
        logger.info(f"Recipe deleted: {recipe_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting recipe: {e}")
        raise e


def apply_recipe_to_targets(db: Session, recipe_id: int, user_id: int) -> Optional[Dict[str, float]]:
    """اعمال مقادیر یک رسپی به عناصر هدف کاربر و برگرداندن مقادیر"""
    try:
        recipe = get_recipe_by_id(db, recipe_id)
        if not recipe:
            return None
        
        # اگر رسپی شخصی است، فقط خود کاربر می‌تواند از آن استفاده کند
        if not recipe.is_system and recipe.user_id != user_id:
            return None
        
        # برگرداندن مقادیر هدف رسپی
        return recipe.target_values
    except Exception as e:
        logger.error(f"Error applying recipe: {e}")
        return None