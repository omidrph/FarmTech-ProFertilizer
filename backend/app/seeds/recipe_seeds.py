# backend/app/seeds/recipe_seeds.py
"""
رسپی‌های استاندارد سیستمی (جایگزین کامل رسپی‌های قبلی)

همهٔ مقادیر از منابع علمی منتشرشده گرفته شده و بر حسب mg/L «عنصر» هستند
(N-NO3 و N-NH4 بر مبنای N، P بر مبنای P، S بر مبنای S):

• Hoagland & Arnon (1938)، Steiner (1984)، Cooper (1979) — جدول مرجع Anaç و همکاران
• Sonneveld & Straver (1994) — «Nutrient solutions for vegetables and flowers grown in
  water or substrates»: محلول استاندارد ۱۰ محصول (mmol/L → mg/L)
• De Kreij و همکاران (1997) — محلول شروع و تغذیهٔ مجدد گوجه‌فرنگی

تعادل یونی همهٔ رسپی‌ها بررسی شده است (اختلاف کاتیون و آنیون ≤ ۰٫۵ meq/L).

مهم: seed_system_recipes هر بار هنگام راه‌اندازی «همگام‌سازی» می‌کند؛
رسپی‌های سیستمی که در این فهرست نیستند حذف می‌شوند. رسپی‌های شخصی کاربران دست‌نخورده می‌مانند.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Recipe

logger = logging.getLogger(__name__)

SYSTEM_RECIPES: List[Dict[str, Any]] = [
    {
        'name': 'هوگلند و آرنون (۱۹۳۸)',
        'category': 'کلاسیک',
        'stage': 'عمومی',
        'description': 'محلول مرجع عمومی هوگلند و آرنون (۱۹۳۸) — مناسب شروع و آزمایش. منبع: Hoagland & Arnon؛ جدول مرجع Anaç و همکاران.',
        'target_values': {'N-NO3': 196.0, 'N-NH4': 14.0, 'P': 31.0, 'S': 64.0, 'K': 234.0, 'Ca': 160.0, 'Mg': 48.0, 'Fe': 2.5, 'Mn': 0.5, 'Zn': 0.05, 'B': 0.5, 'Cu': 0.02, 'Mo': 0.01},
    },
    {
        'name': 'اشتاینر – محلول جهانی (۱۹۸۴)',
        'category': 'کلاسیک',
        'stage': 'عمومی',
        'description': 'محلول جهانی اشتاینر با نسبت ثابت کاتیون\u200cها (K:Ca:Mg ≈ ۳۵:۴۵:۲۰) و آنیون\u200cها (NO₃:H₂PO₄:SO₄ ≈ ۶۰:۵:۳۵). منبع: Steiner (1984)؛ EC حدود ۲ dS/m.',
        'target_values': {'N-NO3': 167.0, 'P': 31.0, 'S': 111.0, 'K': 277.0, 'Ca': 183.0, 'Mg': 49.0, 'Fe': 1.33, 'Mn': 0.62, 'Zn': 0.11, 'B': 0.44, 'Cu': 0.02, 'Mo': 0.048},
    },
    {
        'name': 'کوپر – NFT (۱۹۷۹)',
        'category': 'کلاسیک',
        'stage': 'عمومی',
        'description': 'محلول استاندارد کوپر برای کشت NFT (کاهو و سبزیجات). منبع: Cooper (1979)؛ EC حدود ۲ dS/m.',
        'target_values': {'N-NO3': 200.0, 'P': 60.0, 'S': 68.0, 'K': 300.0, 'Ca': 170.0, 'Mg': 50.0, 'Fe': 12.0, 'Mn': 2.0, 'Zn': 0.1, 'B': 0.3, 'Cu': 0.1, 'Mo': 0.2},
    },
    {
        'name': 'بادمجان – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای بادمجان (EC حدود 2.1 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 217.1, 'N-NH4': 21.0, 'P': 38.7, 'S': 48.1, 'K': 263.9, 'Ca': 130.3, 'Mg': 60.8, 'Fe': 0.838, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'خیار – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای خیار (EC حدود 2.2 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی. سیلیسیم در این رسپی هست.',
        'target_values': {'N-NO3': 224.1, 'N-NH4': 17.5, 'P': 38.7, 'S': 44.1, 'K': 312.8, 'Ca': 160.3, 'Mg': 33.4, 'Fe': 0.838, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048, 'Si': 21.1},
    },
    {
        'name': 'کلم\u200cرابی – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای کلم\u200cرابی (EC حدود 1.5 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 147.1, 'N-NH4': 10.5, 'P': 31.0, 'S': 28.1, 'K': 215.0, 'Ca': 100.2, 'Mg': 24.3, 'Fe': 1.955, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'خربزه / طالبی – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای خربزه / طالبی (EC حدود 2.2 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی. سیلیسیم در این رسپی هست.',
        'target_values': {'N-NO3': 227.6, 'N-NH4': 14.0, 'P': 38.7, 'S': 48.1, 'K': 293.2, 'Ca': 190.4, 'Mg': 30.4, 'Fe': 0.558, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048, 'Si': 21.1},
    },
    {
        'name': 'فلفل دلمه\u200cای – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای فلفل دلمه\u200cای (EC حدود 2.1 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 213.6, 'N-NH4': 14.0, 'P': 38.7, 'S': 56.1, 'K': 293.2, 'Ca': 170.3, 'Mg': 36.5, 'Fe': 0.838, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'کاهو – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای کاهو (EC حدود 2.6 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی. سیلیسیم در این رسپی هست.',
        'target_values': {'N-NO3': 266.1, 'N-NH4': 17.5, 'P': 61.9, 'S': 36.1, 'K': 430.1, 'Ca': 180.4, 'Mg': 24.3, 'Fe': 2.234, 'Mn': 0.275, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048, 'Si': 14.0},
    },
    {
        'name': 'گوجه\u200cفرنگی – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای گوجه\u200cفرنگی (EC حدود 2.3 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 192.6, 'N-NH4': 17.5, 'P': 38.7, 'S': 120.2, 'K': 342.1, 'Ca': 170.3, 'Mg': 48.6, 'Fe': 0.838, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'توت\u200cفرنگی – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای توت\u200cفرنگی (EC حدود 1.5 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 140.1, 'N-NH4': 7.0, 'P': 38.7, 'S': 36.1, 'K': 205.3, 'Ca': 110.2, 'Mg': 27.3, 'Fe': 1.117, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'داوودی – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای داوودی (EC حدود 1.8 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 178.6, 'N-NH4': 17.5, 'P': 31.0, 'S': 32.1, 'K': 293.2, 'Ca': 100.2, 'Mg': 24.3, 'Fe': 3.351, 'Mn': 1.099, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'فریزیا – استاندارد هلندی',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول استاندارد کشت بدون خاک برای فریزیا (EC حدود 2.1 dS/m). منبع: Sonneveld & Straver (1994)؛ Zn و B و Cu و Mo مطابق مقادیر استاندارد هلندی.',
        'target_values': {'N-NO3': 203.1, 'N-NH4': 17.5, 'P': 38.7, 'S': 48.1, 'K': 303.0, 'Ca': 135.3, 'Mg': 36.5, 'Fe': 1.396, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'گوجه\u200cفرنگی – محلول شروع',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول شروع',
        'description': 'محلول شروع (استارتر) گوجه\u200cفرنگی برای پر کردن بستر پیش از کاشت (EC حدود ۳٫۷ dS/m). منبع: De Kreij و همکاران (1997).',
        'target_values': {'N-NO3': 322.2, 'N-NH4': 1.4, 'P': 31.0, 'S': 218.0, 'K': 312.8, 'Ca': 400.8, 'Mg': 109.4, 'Fe': 1.396, 'Mn': 0.275, 'Zn': 0.458, 'B': 0.541, 'Cu': 0.048, 'Mo': 0.048},
    },
    {
        'name': 'گوجه\u200cفرنگی – محلول تغذیه مجدد',
        'category': 'هلندی (سونولد)',
        'stage': 'محلول تغذیه',
        'description': 'محلول تغذیه مجدد (Refilling) گوجه\u200cفرنگی در طول فصل (EC حدود ۱٫۵ dS/m). منبع: De Kreij و همکاران (1997).',
        'target_values': {'N-NO3': 150.6, 'N-NH4': 14.0, 'P': 38.7, 'S': 48.1, 'K': 254.1, 'Ca': 110.2, 'Mg': 24.3, 'Fe': 0.838, 'Mn': 0.549, 'Zn': 0.262, 'B': 0.216, 'Cu': 0.048, 'Mo': 0.048},
    },
]


def seed_system_recipes(db: Session, verify: bool = False) -> Dict[str, int]:
    """همگام‌سازی رسپی‌های سیستمی: حذف قدیمی‌ها + افزودن رسپی‌های استاندارد جدید"""
    stats = {"added": 0, "skipped": 0, "removed": 0, "total": len(SYSTEM_RECIPES), "errors": []}
    names = {r["name"] for r in SYSTEM_RECIPES}

    # چند worker همزمان استارت می‌شوند؛ قفل می‌گیریم تا رسپی‌ها دوبار ساخته نشوند
    try:
        from sqlalchemy import text as _text
        db.execute(_text("SELECT pg_advisory_xact_lock(727002)"))
    except Exception:
        db.rollback()

    try:
        stale = db.query(Recipe).filter(Recipe.is_system == True, ~Recipe.name.in_(names)).all()  # noqa: E712
        for r in stale:
            db.delete(r)
        stats["removed"] = len(stale)
    except Exception as e:
        stats["errors"].append({"name": "CLEANUP", "error": str(e)})

    # حذف تکراری‌ها (اگر قبلاً چند بار seed شده باشد): از هر نام فقط قدیمی‌ترین نگه داشته می‌شود
    try:
        seen = set()
        for r in db.query(Recipe).filter(Recipe.is_system == True).order_by(Recipe.id).all():  # noqa: E712
            if r.name in seen:
                db.delete(r)
                stats["removed"] += 1
            else:
                seen.add(r.name)
        db.flush()
    except Exception as e:
        stats["errors"].append({"name": "DEDUPE", "error": str(e)})

    for data in SYSTEM_RECIPES:
        try:
            existing = db.query(Recipe).filter(Recipe.name == data["name"], Recipe.is_system == True).first()  # noqa: E712
            if existing:
                # به‌روزرسانی مقادیر در صورت تغییر فهرست
                existing.description = data.get("description")
                existing.category = data.get("category")
                existing.stage = data.get("stage")
                existing.target_values = data["target_values"]
                stats["skipped"] += 1
                continue
            db.add(Recipe(
                name=data["name"],
                description=data.get("description"),
                category=data.get("category"),
                stage=data.get("stage"),
                target_values=data["target_values"],
                is_system=True,
                user_id=None,
            ))
            stats["added"] += 1
        except Exception as e:
            stats["errors"].append({"name": data["name"], "error": str(e)})

    try:
        db.commit()
        logger.info(f"رسپی‌های سیستمی: اضافه {stats['added']} | به‌روز {stats['skipped']} | حذف {stats['removed']}")
    except Exception as e:
        db.rollback()
        stats["errors"].append({"name": "COMMIT", "error": str(e)})
    return stats


def get_system_recipes_count(db: Session) -> int:
    return db.query(Recipe).filter(Recipe.is_system == True).count()  # noqa: E712