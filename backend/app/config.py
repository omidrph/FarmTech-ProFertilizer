# backend/app/config.py
"""تنظیمات کل برنامه و متغیرهای محیطی"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # ===== تنظیمات دیتابیس (PostgreSQL) =====
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/farmtech_db"
    )
    
    # ===== تنظیمات امنیت =====
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-super-secret-key-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # ===== تنظیمات برنامه =====
    APP_NAME: str = "FarmTech - ProFertilizer"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # ===== ✅ تنظیمات CORS (با مقدار پیش‌فرض) =====
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ],
        description="لیست آدرس‌های مجاز CORS"
    )
    
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()