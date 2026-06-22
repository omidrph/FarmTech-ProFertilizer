# backend/app/database.py
"""اتصال و مدیریت دیتابیس SQLite"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

# ===== ایجاد اتصال به SQLite =====
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # مخصوص SQLite
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
    """ایجاد تمام جدول‌ها در دیتابیس"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """حذف تمام جدول‌ها از دیتابیس (فقط برای توسعه)"""
    Base.metadata.drop_all(bind=engine)