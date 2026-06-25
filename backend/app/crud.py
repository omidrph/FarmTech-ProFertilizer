# backend/app/crud.py
"""عملیات پایه دیتابیس (CRUD) برای همه مدل‌ها"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
import logging

# ============================================================
# 🆕 Import مدل‌ها (WaterAnalysisTemplate اضافه شد)
# ============================================================
from app.models import (
    User, Report, Fertilizer, WaterAnalysis, Calculation, 
    UserSession, Recipe, WaterAnalysisTemplate
)

# ============================================================
# 🆕 Import طرح‌ها (WaterAnalysisTemplate* اضافه شد)
# ============================================================
from app.schemas import (
    UserCreate, UserUpdate,
    ReportCreate, ReportUpdate,
    FertilizerCreate, FertilizerUpdate,
    WaterAnalysisCreate, WaterAnalysisUpdate,
    CalculationCreate, CalculationUpdate,
    RecipeCreate, RecipeUpdate,
    WaterAnalysisTemplateCreate, WaterAnalysisTemplateUpdate, WaterAnalysisTemplateResponse
)

from app.security import get_password_hash, delete_user_sessions

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)


# ============================================================
# CRUD برای User (کاربر)
# ============================================================

def create_user(db: Session, user_data: UserCreate) -> User:
    """ایجاد کاربر جدید"""
    try:
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            password_hash=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created: {db_user.id} - {db_user.phone_number}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise e


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """دریافت کاربر با شناسه"""
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error getting user by id: {e}")
        return None


def get_user_by_phone(db: Session, phone_number: str) -> Optional[User]:
    """دریافت کاربر با شماره تلفن"""
    try:
        return db.query(User).filter(User.phone_number == phone_number).first()
    except Exception as e:
        logger.error(f"Error getting user by phone: {e}")
        return None


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """دریافت لیست کاربران"""
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return []


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """به‌روزرسانی اطلاعات کاربر"""
    try:
        db_user = get_user_by_id(db, user_id)
        
        if db_user is None:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User updated: {db_user.id}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        raise e


def delete_user(db: Session, user_id: int) -> bool:
    """حذف کاربر (همراه با حذف نشست‌ها)"""
    try:
        db_user = get_user_by_id(db, user_id)
        
        if db_user is None:
            return False
        
        delete_user_sessions(user_id, db)
        
        db.delete(db_user)
        db.commit()
        
        logger.info(f"User deleted: {user_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {e}")
        raise e


# ============================================================
# CRUD برای Report (گزارش)
# ============================================================

def create_report(db: Session, report_data: ReportCreate, user_id: int) -> Report:
    """ایجاد گزارش جدید"""
    try:
        db_report = Report(
            user_id=user_id,
            report_name=report_data.report_name,
            plant_name=report_data.plant_name,
            season=report_data.season,
            growth_stage=report_data.growth_stage,
            report_date=report_data.report_date
        )
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        logger.info(f"Report created: {db_report.id} for user {user_id}")
        return db_report
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating report: {e}")
        raise e


def get_report_by_id(db: Session, report_id: int) -> Optional[Report]:
    """دریافت گزارش با شناسه"""
    try:
        return db.query(Report).filter(Report.id == report_id).first()
    except Exception as e:
        logger.error(f"Error getting report by id: {e}")
        return None


def get_reports_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Report]:
    """دریافت گزارش‌های یک کاربر"""
    try:
        return db.query(Report).filter(Report.user_id == user_id).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting reports by user: {e}")
        return []


def update_report(db: Session, report_id: int, report_data: ReportUpdate) -> Optional[Report]:
    """به‌روزرسانی گزارش"""
    try:
        db_report = get_report_by_id(db, report_id)
        
        if db_report is None:
            return None
        
        update_data = report_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_report, key, value)
        
        db.commit()
        db.refresh(db_report)
        
        logger.info(f"Report updated: {report_id}")
        return db_report
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating report: {e}")
        raise e


def delete_report(db: Session, report_id: int) -> bool:
    """حذف گزارش"""
    try:
        db_report = get_report_by_id(db, report_id)
        
        if db_report is None:
            return False
        
        db.delete(db_report)
        db.commit()
        
        logger.info(f"Report deleted: {report_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting report: {e}")
        raise e


# ============================================================
# CRUD برای Fertilizer (کود) - اصلاح شده نهایی
# ============================================================

def create_fertilizer(db: Session, fertilizer_data: FertilizerCreate, user_id: int):
    """
    ایجاد کود جدید
    
    توجه: این تابع حتماً باید یک شیء Fertilizer برگرداند، نه عدد
    """
    try:
        logger.info(f"Creating fertilizer: {fertilizer_data.name} for user {user_id}")
        
        # ایجاد شیء Fertilizer
        db_fertilizer = Fertilizer(
            user_id=user_id,
            name=fertilizer_data.name,
            price_per_kg=fertilizer_data.price_per_kg,
            elements=fertilizer_data.elements or {},
            is_acid=fertilizer_data.is_acid,
            acid_type=fertilizer_data.acid_type
        )
        
        # اضافه کردن به دیتابیس
        db.add(db_fertilizer)
        
        # Commit کردن
        db.commit()
        
        # Refresh کردن برای دریافت ID
        db.refresh(db_fertilizer)
        
        # لاگ کردن
        logger.info(f"Fertilizer created successfully: ID={db_fertilizer.id}, Name={db_fertilizer.name}")
        
        # برگرداندن شیء Fertilizer (نه عدد!)
        return db_fertilizer
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating fertilizer: {e}")
        raise e


def get_fertilizer_by_id(db: Session, fertilizer_id: int) -> Optional[Fertilizer]:
    """دریافت کود با شناسه"""
    try:
        return db.query(Fertilizer).filter(Fertilizer.id == fertilizer_id).first()
    except Exception as e:
        logger.error(f"Error getting fertilizer by id: {e}")
        return None


def get_fertilizers_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Fertilizer]:
    """دریافت کودهای یک کاربر"""
    try:
        return db.query(Fertilizer).filter(Fertilizer.user_id == user_id).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting fertilizers by user: {e}")
        return []


def update_fertilizer(db: Session, fertilizer_id: int, fertilizer_data: FertilizerUpdate) -> Optional[Fertilizer]:
    """به‌روزرسانی کود"""
    try:
        db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
        
        if db_fertilizer is None:
            return None
        
        update_data = fertilizer_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_fertilizer, key, value)
        
        db.commit()
        db.refresh(db_fertilizer)
        
        logger.info(f"Fertilizer updated: {fertilizer_id}")
        return db_fertilizer
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating fertilizer: {e}")
        raise e


def delete_fertilizer(db: Session, fertilizer_id: int) -> bool:
    """حذف کود"""
    try:
        db_fertilizer = get_fertilizer_by_id(db, fertilizer_id)
        
        if db_fertilizer is None:
            return False
        
        db.delete(db_fertilizer)
        db.commit()
        
        logger.info(f"Fertilizer deleted: {fertilizer_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting fertilizer: {e}")
        raise e


# ============================================================
# CRUD برای WaterAnalysis (آنالیز آب)
# ============================================================

def create_water_analysis(db: Session, analysis_data: WaterAnalysisCreate, report_id: int) -> WaterAnalysis:
    """ایجاد آنالیز آب"""
    try:
        db_analysis = WaterAnalysis(
            report_id=report_id,
            water_percentage=analysis_data.water_percentage,
            wastewater_percentage=analysis_data.wastewater_percentage,
            water_salinity=analysis_data.water_salinity,
            wastewater_values=analysis_data.wastewater_values or {},
            water_values=analysis_data.water_values or {}
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        logger.info(f"Water analysis created: {db_analysis.id} for report {report_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating water analysis: {e}")
        raise e


def get_water_analysis_by_report(db: Session, report_id: int) -> Optional[WaterAnalysis]:
    """دریافت آنالیز آب بر اساس گزارش"""
    try:
        return db.query(WaterAnalysis).filter(WaterAnalysis.report_id == report_id).first()
    except Exception as e:
        logger.error(f"Error getting water analysis by report: {e}")
        return None


def update_water_analysis(db: Session, analysis_id: int, analysis_data: WaterAnalysisUpdate) -> Optional[WaterAnalysis]:
    """به‌روزرسانی آنالیز آب"""
    try:
        db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
        
        if db_analysis is None:
            return None
        
        update_data = analysis_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_analysis, key, value)
        
        db.commit()
        db.refresh(db_analysis)
        
        logger.info(f"Water analysis updated: {analysis_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating water analysis: {e}")
        raise e


def delete_water_analysis(db: Session, analysis_id: int) -> bool:
    """حذف آنالیز آب"""
    try:
        db_analysis = db.query(WaterAnalysis).filter(WaterAnalysis.id == analysis_id).first()
        
        if db_analysis is None:
            return False
        
        db.delete(db_analysis)
        db.commit()
        
        logger.info(f"Water analysis deleted: {analysis_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting water analysis: {e}")
        raise e


# ============================================================
# CRUD برای Calculation (محاسبات)
# ============================================================

def create_calculation(db: Session, calc_data: CalculationCreate, report_id: int) -> Calculation:
    """ایجاد محاسبات جدید"""
    try:
        db_calculation = Calculation(
            report_id=report_id,
            target_values=calc_data.target_values or {},
            final_values=calc_data.final_values or {},
            reservoir_data=calc_data.reservoir_data or {},
            calc_rows=calc_data.calc_rows or [],
            interpretation=calc_data.interpretation
        )
        
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        
        logger.info(f"Calculation created: {db_calculation.id} for report {report_id}")
        return db_calculation
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating calculation: {e}")
        raise e


def get_calculation_by_report(db: Session, report_id: int) -> Optional[Calculation]:
    """دریافت محاسبات بر اساس گزارش"""
    try:
        return db.query(Calculation).filter(Calculation.report_id == report_id).first()
    except Exception as e:
        logger.error(f"Error getting calculation by report: {e}")
        return None


def update_calculation(db: Session, calc_id: int, calc_data: CalculationUpdate) -> Optional[Calculation]:
    """به‌روزرسانی محاسبات"""
    try:
        db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        
        if db_calculation is None:
            return None
        
        update_data = calc_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_calculation, key, value)
        
        db.commit()
        db.refresh(db_calculation)
        
        logger.info(f"Calculation updated: {calc_id}")
        return db_calculation
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating calculation: {e}")
        raise e


def delete_calculation(db: Session, calc_id: int) -> bool:
    """حذف محاسبات"""
    try:
        db_calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
        
        if db_calculation is None:
            return False
        
        db.delete(db_calculation)
        db.commit()
        
        logger.info(f"Calculation deleted: {calc_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting calculation: {e}")
        raise e


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


# ============================================================
# 🆕 CRUD برای WaterAnalysisTemplate (قالب آنالیز آب)
# ============================================================

def create_water_template(db: Session, template_data: WaterAnalysisTemplateCreate, user_id: int) -> WaterAnalysisTemplate:
    """ایجاد قالب آنالیز آب جدید"""
    try:
        db_template = WaterAnalysisTemplate(
            user_id=user_id,
            name=template_data.name,
            description=template_data.description,
            water_percentage=template_data.water_percentage,
            wastewater_percentage=template_data.wastewater_percentage,
            water_salinity=template_data.water_salinity,
            water_salinity_unit=template_data.water_salinity_unit,
            water_ph=template_data.water_ph,
            water_values=template_data.water_values or {},
            wastewater_values=template_data.wastewater_values or {}
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        logger.info(f"Water template created: {db_template.id} - {db_template.name}")
        return db_template
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating water template: {e}")
        raise e


def get_water_templates_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[WaterAnalysisTemplate]:
    """دریافت قالب‌های آنالیز آب کاربر"""
    try:
        return db.query(WaterAnalysisTemplate).filter(
            WaterAnalysisTemplate.user_id == user_id
        ).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting water templates: {e}")
        return []


def get_water_template_by_id(db: Session, template_id: int) -> Optional[WaterAnalysisTemplate]:
    """دریافت قالب آنالیز آب با شناسه"""
    try:
        return db.query(WaterAnalysisTemplate).filter(
            WaterAnalysisTemplate.id == template_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting water template by id: {e}")
        return None


def update_water_template(db: Session, template_id: int, template_data: WaterAnalysisTemplateUpdate) -> Optional[WaterAnalysisTemplate]:
    """به‌روزرسانی قالب آنالیز آب"""
    try:
        db_template = get_water_template_by_id(db, template_id)
        if db_template is None:
            return None
        
        update_data = template_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_template, key, value)
        
        db.commit()
        db.refresh(db_template)
        logger.info(f"Water template updated: {template_id}")
        return db_template
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating water template: {e}")
        raise e


def delete_water_template(db: Session, template_id: int) -> bool:
    """حذف قالب آنالیز آب"""
    try:
        db_template = get_water_template_by_id(db, template_id)
        if db_template is None:
            return False
        
        db.delete(db_template)
        db.commit()
        logger.info(f"Water template deleted: {template_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting water template: {e}")
        raise e