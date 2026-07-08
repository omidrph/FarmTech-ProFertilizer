# backend/app/database.py
"""اتصال و مدیریت دیتابیس PostgreSQL با SSL"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
import time
import os

from app.config import settings

logger = logging.getLogger(__name__)

# ============================================================
# 🔐 ایجاد اتصال به PostgreSQL با SSL
# ============================================================

def get_database_url_with_ssl():
    """دریافت URL دیتابیس با تنظیمات SSL"""
    url = settings.DATABASE_URL
    
    # اگر SSL فعال است و URL هنوز پارامتر SSL ندارد
    if settings.DB_SSL_MODE and "sslmode" not in url:
        # اضافه کردن پارامترهای SSL
        ssl_params = f"sslmode={settings.DB_SSL_MODE}"
        
        if settings.DB_SSL_CA_CERT:
            ssl_params += f"&sslrootcert={settings.DB_SSL_CA_CERT}"
        
        if settings.DB_SSL_CLIENT_CERT:
            ssl_params += f"&sslcert={settings.DB_SSL_CLIENT_CERT}"
        
        if settings.DB_SSL_CLIENT_KEY:
            ssl_params += f"&sslkey={settings.DB_SSL_CLIENT_KEY}"
        
        # اضافه کردن به URL
        if "?" in url:
            url += f"&{ssl_params}"
        else:
            url += f"?{ssl_params}"
    
    return url


# ایجاد engine با تنظیمات SSL
DATABASE_URL = get_database_url_with_ssl()

# تنظیمات اتصال
connect_args = {}

# اگر SSL فعال است، تنظیمات اضافی
if settings.DB_SSL_MODE and settings.DB_SSL_MODE != "disable":
    connect_args = {
        "sslmode": settings.DB_SSL_MODE,
    }
    if settings.DB_SSL_CA_CERT:
        connect_args["sslrootcert"] = settings.DB_SSL_CA_CERT
    if settings.DB_SSL_CLIENT_CERT:
        connect_args["sslcert"] = settings.DB_SSL_CLIENT_CERT
    if settings.DB_SSL_CLIENT_KEY:
        connect_args["sslkey"] = settings.DB_SSL_CLIENT_KEY

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args if connect_args else {}
)

logger.info(f"🗄️ Database connected with SSL mode: {settings.DB_SSL_MODE}")

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
    با قابلیت Retry
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