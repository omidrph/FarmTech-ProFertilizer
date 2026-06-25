# backend/app/seeds/recipe_seeds.py
"""
Seed داده‌های اولیه رسپی‌های سیستمی
این فایل شامل ۲۵ رسپی استاندارد برای محصولات مختلف است.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Recipe

logger = logging.getLogger(__name__)


# ============================================================
# لیست کامل رسپی‌های سیستمی
# ============================================================
SYSTEM_RECIPES: List[Dict[str, Any]] = [
    # ۱. Chilli (maximumyield)
    {
        "name": "Chilli (maximumyield)",
        "description": "رسپی استاندارد فلفل - حداکثر عملکرد",
        "category": "فلفل",
        "stage": "گلدهی و میوه‌دهی",
        "target_values": {
            "N-NO3": 320, "N-NH4": 0, "P": 103, "K": 364,
            "Mg": 96, "Ca": 330, "S": 174,
            "Fe": 4.9, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05
        }
    },
    # ۲. Cucumber (Howard Resh)
    {
        "name": "Cucumber (Howard Resh)",
        "description": "رسپی استاندارد خیار - هوارد رش",
        "category": "خیار",
        "stage": "رشد و میوه‌دهی",
        "target_values": {
            "N-NO3": 140, "N-NH4": 0, "P": 50, "K": 350,
            "Mg": 50, "Ca": 200, "S": 150,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03
        }
    },
    # ۳. Generic Bloom (maximumyield)
    {
        "name": "Generic Bloom (maximumyield)",
        "description": "رسپی عمومی برای مرحله گلدهی",
        "category": "عمومی",
        "stage": "گلدهی",
        "target_values": {
            "N-NO3": 130, "N-NH4": 10, "P": 60, "K": 300,
            "Mg": 30, "Ca": 100, "S": 60,
            "Fe": 2, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.05, "Mo": 0.05
        }
    },
    # ۴. Generic Dry Season (Howard Resh)
    {
        "name": "Generic Dry Season (Howard Resh)",
        "description": "رسپی عمومی برای فصل خشک",
        "category": "عمومی",
        "stage": "فصل خشک",
        "target_values": {
            "N-NO3": 177, "N-NH4": 53, "P": 60, "K": 200,
            "Mg": 36, "Ca": 250, "S": 129,
            "Fe": 5, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.03, "Mo": 0.02
        }
    },
    # ۵. Generic for Berries (Growing Edge)
    {
        "name": "Generic for Berries (Growing Edge)",
        "description": "رسپی عمومی برای توت‌ها",
        "category": "توت",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 207, "N-NH4": 0, "P": 55, "K": 289,
            "Mg": 38, "Ca": 155, "S": 51,
            "Fe": 6.8, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05
        }
    },
    # ۶. Generic Grow (maximumyield)
    {
        "name": "Generic Grow (maximumyield)",
        "description": "رسپی عمومی برای مرحله رشد رویشی",
        "category": "عمومی",
        "stage": "رشد رویشی",
        "target_values": {
            "N-NO3": 160, "N-NH4": 0, "P": 30, "K": 230,
            "Mg": 30, "Ca": 100, "S": 60,
            "Fe": 2, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.05, "Mo": 0.05
        }
    },
    # ۷. Generic Wet Season (Howard Resh)
    {
        "name": "Generic Wet Season (Howard Resh)",
        "description": "رسپی عمومی برای فصل مرطوب",
        "category": "عمومی",
        "stage": "فصل مرطوب",
        "target_values": {
            "N-NO3": 115, "N-NH4": 32, "P": 50, "K": 150,
            "Mg": 50, "Ca": 150, "S": 50,
            "Fe": 5, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.03, "Mo": 0.02
        }
    },
    # ۸. Hoagland solution
    {
        "name": "Hoagland solution",
        "description": "محلول استاندارد هوگلند - یکی از معروف‌ترین فرمول‌های غذایی",
        "category": "استاندارد",
        "stage": "عمومی",
        "target_values": {
            "N-NO3": 210, "N-NH4": 0, "P": 31, "K": 235,
            "Mg": 49, "Ca": 200, "S": 64,
            "Fe": 2.9, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.02, "Mo": 0.05,
            "Cl": 10
        }
    },
    # ۹. Lettuce 2 (Howard Resh)
    {
        "name": "Lettuce 2 (Howard Resh)",
        "description": "رسپی استاندارد کاهو - نسخه ۲ هوارد رش",
        "category": "کاهو",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 165, "N-NH4": 15, "P": 50, "K": 210,
            "Mg": 45, "Ca": 190, "S": 113,
            "Fe": 4, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.1, "Mo": 0.05
        }
    },
    # ۱۰. Lettuce General (Howard Resh)
    {
        "name": "Lettuce General (Howard Resh)",
        "description": "رسپی عمومی کاهو - هوارد رش",
        "category": "کاهو",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 165, "N-NH4": 15, "P": 50, "K": 210,
            "Mg": 45, "Ca": 190, "S": 65,
            "Fe": 4, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.1, "Mo": 0.05
        }
    },
    # ۱۱. Melons (Douglas Peckenpaugh)
    {
        "name": "Melons (Douglas Peckenpaugh)",
        "description": "رسپی استاندارد طالبی و خربزه",
        "category": "خربزه و طالبی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 215, "N-NH4": 0, "P": 86, "K": 343,
            "Mg": 85, "Ca": 175, "S": 113,
            "Fe": 6.8, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Si": 10
        }
    },
    # ۱۲. Pepper (Howard Resh)
    {
        "name": "Pepper (Howard Resh)",
        "description": "رسپی استاندارد فلفل دلمه‌ای - هوارد رش",
        "category": "فلفل",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 190, "N-NH4": 18, "P": 40, "K": 340,
            "Mg": 50, "Ca": 170, "S": 360,
            "Fe": 5, "Mn": 0.55, "Zn": 0.33, "B": 0.33, "Cu": 0.05, "Mo": 0.05
        }
    },
    # ۱۳. Rice (Douglas Peckenpaugh)
    {
        "name": "Rice (Douglas Peckenpaugh)",
        "description": "رسپی استاندارد برنج",
        "category": "برنج",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 249, "N-NH4": 0, "P": 58, "K": 80,
            "Mg": 65, "Ca": 317, "S": 87,
            "Fe": 5, "Mn": 0.8, "Zn": 0.4, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Si": 100
        }
    },
    # ۱۴. Strawberry Drip Irrigation (schundler.com)
    {
        "name": "Strawberry Drip Irrigation (schundler.com)",
        "description": "رسپی توت فرنگی - آبیاری قطره‌ای",
        "category": "توت فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 80, "N-NH4": 0, "P": 45, "K": 100,
            "Mg": 50, "Ca": 200, "S": 180,
            "Fe": 3, "Mn": 0.5, "Zn": 0.5, "B": 0.5, "Cu": 0.05, "Mo": 0.05,
            "Cl": 10
        }
    },
    # ۱۵. Strawberry Fruiting (growing edge)
    {
        "name": "Strawberry Fruiting (growing edge)",
        "description": "رسپی توت فرنگی - مرحله میوه‌دهی",
        "category": "توت فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 128, "N-NH4": 0, "P": 58, "K": 211,
            "Mg": 40, "Ca": 104, "S": 54,
            "Fe": 5, "Mn": 2, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 10
        }
    },
    # ۱۶. Tomato (Howard Resh)
    {
        "name": "Tomato (Howard Resh)",
        "description": "رسپی استاندارد گوجه فرنگی - هوارد رش",
        "category": "گوجه فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 140, "N-NH4": 0, "P": 50, "K": 352,
            "Mg": 50, "Ca": 180, "S": 168,
            "Fe": 5, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03
        }
    },
    # ۱۷. Tomato Stage 1 (10-14 days) - Howard Resh
    {
        "name": "Tomato Stage 1 (10-14 days)",
        "description": "رسپی گوجه فرنگی - مرحله ۱ (۱۰-۱۴ روزه)",
        "category": "گوجه فرنگی",
        "stage": "نشاء (۱۰-۱۴ روز)",
        "target_values": {
            "N-NO3": 100, "N-NH4": 0, "P": 40, "K": 200,
            "Mg": 20, "Ca": 100, "S": 53,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03
        }
    },
    # ۱۸. Tomato Stage 2 (first cluster) - Howard Resh
    {
        "name": "Tomato Stage 2 (first cluster)",
        "description": "رسپی گوجه فرنگی - مرحله ۲ (اولین خوشه)",
        "category": "گوجه فرنگی",
        "stage": "اولین خوشه",
        "target_values": {
            "N-NO3": 130, "N-NH4": 10, "P": 55, "K": 300,
            "Mg": 33, "Ca": 150, "S": 109,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03
        }
    },
    # ۱۹. Tomato Stage 3 (plant maturity) - Howard Resh
    {
        "name": "Tomato Stage 3 (plant maturity)",
        "description": "رسپی گوجه فرنگی - مرحله ۳ (بلوغ گیاه)",
        "category": "گوجه فرنگی",
        "stage": "بلوغ گیاه",
        "target_values": {
            "N-NO3": 180, "N-NH4": 0, "P": 65, "K": 400,
            "Mg": 45, "Ca": 400, "S": 144,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03
        }
    },
    # ۲۰. Tomatoes - Fourth Cluster (U of Florida)
    {
        "name": "Tomatoes - Fourth Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه چهارم - دانشگاه فلوریدا",
        "category": "گوجه فرنگی",
        "stage": "خوشه چهارم",
        "target_values": {
            "N-NO3": 120, "N-NH4": 0, "P": 50, "K": 150,
            "Mg": 50, "Ca": 150, "S": 60,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05
        }
    },
    # ۲۱. Tomatoes - Second Cluster (U of Florida)
    {
        "name": "Tomatoes - Second Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه دوم - دانشگاه فلوریدا",
        "category": "گوجه فرنگی",
        "stage": "خوشه دوم",
        "target_values": {
            "N-NO3": 80, "N-NH4": 0, "P": 50, "K": 120,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05
        }
    },
    # ۲۲. Tomatoes - Third Cluster (U of Florida)
    {
        "name": "Tomatoes - Third Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه سوم - دانشگاه فلوریدا",
        "category": "گوجه فرنگی",
        "stage": "خوشه سوم",
        "target_values": {
            "N-NO3": 100, "N-NH4": 0, "P": 50, "K": 150,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05
        }
    },
    # ۲۳. Tomatoes - till First Cluster (U of Florida)
    {
        "name": "Tomatoes - till First Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - تا اولین خوشه - دانشگاه فلوریدا",
        "category": "گوجه فرنگی",
        "stage": "تا اولین خوشه",
        "target_values": {
            "N-NO3": 70, "N-NH4": 0, "P": 50, "K": 120,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05
        }
    },
    # ۲۴. Tomatoes to termination (U of Florida)
    {
        "name": "Tomatoes to termination (U of Florida)",
        "description": "رسپی گوجه فرنگی - تا پایان دوره - دانشگاه فلوریدا",
        "category": "گوجه فرنگی",
        "stage": "پایان دوره",
        "target_values": {
            "N-NO3": 150, "N-NH4": 0, "P": 50, "K": 200,
            "Mg": 50, "Ca": 150, "S": 60,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05
        }
    },
    # ۲۵. Tropical Lettuce (Douglas Peckenpaugh)
    {
        "name": "Tropical Lettuce (Douglas Peckenpaugh)",
        "description": "رسپی کاهو گرمسیری - داگلاس پکنپا",
        "category": "کاهو",
        "stage": "رشد گرمسیری",
        "target_values": {
            "N-NO3": 190, "N-NH4": 0, "P": 25, "K": 98,
            "Mg": 25, "Ca": 216, "S": 33,
            "Fe": 4.9, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Na": 10
        }
    },
]


# ============================================================
# تابع اجرای Seed
# ============================================================
def seed_system_recipes(db: Session) -> Dict[str, int]:
    """
    افزودن رسپی‌های سیستمی به دیتابیس
    
    Args:
        db: Session دیتابیس
    
    Returns:
        Dict با آمار عملیات
    """
    stats = {
        "added": 0,
        "skipped": 0,
        "total": len(SYSTEM_RECIPES),
        "errors": []
    }
    
    logger.info(f"🌱 شروع Seed رسپی‌های سیستمی - تعداد: {stats['total']}")
    
    for recipe_data in SYSTEM_RECIPES:
        try:
            # بررسی وجود رسپی با همین نام
            existing = db.query(Recipe).filter(
                Recipe.name == recipe_data["name"],
                Recipe.is_system == True
            ).first()
            
            if existing:
                stats["skipped"] += 1
                logger.debug(f"⏭️  رد شد (موجود): {recipe_data['name']}")
                continue
            
            # ایجاد رسپی سیستمی جدید
            new_recipe = Recipe(
                name=recipe_data["name"],
                description=recipe_data.get("description"),
                category=recipe_data.get("category"),
                stage=recipe_data.get("stage"),
                target_values=recipe_data["target_values"],
                is_system=True,
                user_id=None
            )
            
            db.add(new_recipe)
            stats["added"] += 1
            logger.info(f"✅ اضافه شد: {recipe_data['name']}")
            
        except Exception as e:
            stats["errors"].append({
                "name": recipe_data["name"],
                "error": str(e)
            })
            logger.error(f"❌ خطا در افزودن {recipe_data['name']}: {e}")
    
    # Commit کردن تغییرات
    try:
        db.commit()
        logger.info(
            f"🎉 Seed کامل شد - "
            f"اضافه شده: {stats['added']} | "
            f"رد شده: {stats['skipped']} | "
            f"خطا: {len(stats['errors'])}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"❌ خطا در commit: {e}")
        stats["errors"].append({"name": "COMMIT", "error": str(e)})
    
    return stats


def get_system_recipes_count(db: Session) -> int:
    """دریافت تعداد رسپی‌های سیستمی موجود در دیتابیس"""
    return db.query(Recipe).filter(
        Recipe.is_system == True
    ).count()


def clear_system_recipes(db: Session) -> int:
    """
    حذف تمام رسپی‌های سیستمی از دیتابیس
    (برای اجرای مجدد seed)
    
    Returns:
        تعداد رسپی‌های حذف شده
    """
    count = db.query(Recipe).filter(
        Recipe.is_system == True
    ).delete()
    db.commit()
    logger.info(f"🗑️  {count} رسپی سیستمی حذف شد")
    return count