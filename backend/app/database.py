# backend/app/database.py
"""اتصال و مدیریت دیتابیس PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
import time

from app.config import settings

logger = logging.getLogger(__name__)

# ===== ایجاد اتصال به PostgreSQL =====
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# ===== ایجاد SessionLocal =====
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ===== ایجاد کلاس پایه برای مدل‌ها =====
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    وابستگی برای دریافت Session دیتابیس
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    ایجاد تمام جدول‌ها در دیتابیس
    ✅ اصلاح شده برای PostgreSQL با قابلیت Retry
    """
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Tables created successfully with SQLAlchemy")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error(f"❌ Failed to create tables after {max_retries} attempts")
                return False
    return False


def drop_tables():
    """حذف تمام جدول‌ها از دیتابیس (فقط برای توسعه)"""
    Base.metadata.drop_all(bind=engine)


def get_engine():
    """دریافت engine دیتابیس برای استفاده در جاهای دیگر"""
    return engine