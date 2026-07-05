#!/usr/bin/env python3
# scripts/init_db.py
"""اسکریپت مقداردهی اولیه دیتابیس PostgreSQL"""

import sys
import os
import time
import logging
from pathlib import Path

# ============================================================
# 🔧 اضافه کردن مسیر backend به PYTHONPATH
# ============================================================
BASE_DIR = Path(__file__).parent.parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))
os.environ["PYTHONPATH"] = str(BACKEND_DIR) + os.pathsep + os.environ.get("PYTHONPATH", "")

# ============================================================
# تنظیم logging
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# تنظیم متغیرهای محیطی برای دیتابیس
# ============================================================
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@db:5432/farmtech_db")

# ============================================================
# Import ماژول‌های app
# ============================================================
try:
    from app.config import settings
    from app.database import create_tables, SessionLocal
    from app.seeds.fertilizer_seeds import seed_system_fertilizers
    from app.seeds.recipe_seeds import seed_system_recipes
    from app.crud import create_user, get_user_by_phone
    from app.schemas import UserCreate
except ImportError as e:
    logger.error(f"❌ Failed to import app modules: {e}")
    logger.error(f"   Make sure backend directory is at: {BACKEND_DIR}")
    logger.error(f"   Current sys.path: {sys.path}")
    sys.exit(1)


def wait_for_db(max_retries=10, delay=3):
    """منتظر ماندن تا آماده شدن دیتابیس"""
    logger.info("⏳ Waiting for database to be ready...")
    
    for attempt in range(max_retries):
        try:
            from sqlalchemy import text, create_engine
            
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            engine.dispose()
            logger.info("✅ Database is ready")
            return True
        except Exception as e:
            logger.warning(f"⏳ Waiting for database... ({attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    logger.error("❌ Database not ready after waiting")
    return False


def main():
    """اجرای مقداردهی اولیه"""
    logger.info("=" * 60)
    logger.info("🚀 Starting database initialization...")
    logger.info("=" * 60)
    logger.info(f"📁 Backend path: {BACKEND_DIR}")
    logger.info(f"🗄️  Database URL: {settings.DATABASE_URL}")
    logger.info("=" * 60)
    
    # 1. انتظار برای دیتابیس
    if not wait_for_db():
        logger.error("❌ Database not ready. Exiting...")
        sys.exit(1)
    
    # 2. ایجاد جدول‌ها
    logger.info("📦 Creating tables...")
    try:
        if create_tables():
            logger.info("✅ Tables created successfully")
        else:
            logger.error("❌ Failed to create tables")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        sys.exit(1)
    
    # 3. بارگذاری کودهای سیستمی
    logger.info("🌱 Seeding system fertilizers...")
    try:
        db = SessionLocal()
        fert_stats = seed_system_fertilizers(db)
        db.commit()
        db.close()
        
        logger.info(f"   ✅ Fertilizers: {fert_stats['added']} added, {fert_stats['skipped']} skipped")
        if fert_stats.get('errors'):
            for err in fert_stats['errors']:
                logger.warning(f"      ⚠️ Error: {err}")
    except Exception as e:
        logger.error(f"❌ Error seeding fertilizers: {e}")
    
    # 4. بارگذاری رسپی‌های سیستمی
    logger.info("📋 Seeding system recipes...")
    try:
        db = SessionLocal()
        recipe_stats = seed_system_recipes(db, verify=False)
        db.commit()
        db.close()
        
        logger.info(f"   ✅ Recipes: {recipe_stats['added']} added, {recipe_stats['skipped']} skipped")
        if recipe_stats.get('errors'):
            for err in recipe_stats['errors']:
                logger.warning(f"      ⚠️ Error: {err}")
    except Exception as e:
        logger.error(f"❌ Error seeding recipes: {e}")
    
    # 5. ایجاد کاربر تست
    logger.info("👤 Creating test user...")
    try:
        db = SessionLocal()
        existing = get_user_by_phone(db, "09121234567")
        
        if not existing:
            user_data = UserCreate(
                first_name="تست",
                last_name="سیستم",
                phone_number="09121234567",
                password="Test@123456"
            )
            user = create_user(db, user_data)
            db.commit()
            logger.info(f"   ✅ Test user created: ID={user.id}")
        else:
            logger.info(f"   ✅ Test user already exists: ID={existing.id}")
        
        db.close()
    except Exception as e:
        logger.warning(f"   ⚠️ Could not create test user: {e}")
    
    logger.info("=" * 60)
    logger.info("🎉 Database initialization completed successfully!")
    logger.info("=" * 60)
    logger.info("👤 Test user credentials:")
    logger.info("   📱 Phone: 09121234567")
    logger.info("   🔑 Password: Test@123456")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()