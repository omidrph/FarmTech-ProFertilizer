# backend/app/config.py
"""تنظیمات کل برنامه و متغیرهای محیطی"""

import os
import json
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()


class Settings(BaseSettings):
    """تنظیمات اصلی برنامه"""
    
    # ===== تنظیمات دیتابیس =====
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:mysecretpassword@localhost:5432/farmtech_db"
    )
    
    # ===== تنظیمات امنیت =====
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-here-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 روز
    
    # ===== تنظیمات برنامه =====
    APP_NAME: str = "FarmTech - ProFertilizer"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # ===== تنظیمات CORS =====
    # اصلاح: استفاده از Field با مقدار پیش‌فرض
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]
    )
    
    # ===== تنظیمات API =====
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# ایجاد یک نمونه از تنظیمات برای استفاده در سراسر برنامه
settings = Settings()