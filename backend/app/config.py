# backend/app/config.py
"""تنظیمات کل برنامه و متغیرهای محیطی"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # ===== تنظیمات دیتابیس =====
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/farmtech_db"
    )
    
    DB_SSL_MODE: str = os.getenv("DB_SSL_MODE", "disable")
    DB_SSL_CA_CERT: Optional[str] = os.getenv("DB_SSL_CA_CERT")
    DB_SSL_CLIENT_CERT: Optional[str] = os.getenv("DB_SSL_CLIENT_CERT")
    DB_SSL_CLIENT_KEY: Optional[str] = os.getenv("DB_SSL_CLIENT_KEY")
    
    # ===== تنظیمات امنیت =====
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("SESSION_EXPIRY_HOURS", 24)) * 60
    
    # ===== تنظیمات برنامه =====
    APP_NAME: str = "FarmTech - ProFertilizer"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ===== 🔧 تنظیمات CORS =====
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["Content-Type", "Authorization", "Accept", "X-Requested-With"]
    CORS_EXPOSE_HEADERS: List[str] = ["Content-Disposition"]
    CORS_MAX_AGE: int = 86400
    
    API_PREFIX: str = "/api/v1"
    
    # ===== Rate Limiting =====
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 5))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 300))
    
    # ===== قفل حساب =====
    MAX_FAILED_ATTEMPTS: int = int(os.getenv("MAX_FAILED_ATTEMPTS", 5))
    ACCOUNT_LOCK_MINUTES: int = int(os.getenv("ACCOUNT_LOCK_MINUTES", 15))
    
    # ===== Session =====
    SESSION_EXPIRY_HOURS: int = int(os.getenv("SESSION_EXPIRY_HOURS", 24))
    SESSION_INACTIVITY_DAYS: int = int(os.getenv("SESSION_INACTIVITY_DAYS", 30))
    
    # ===== SMS =====
    SMS_PROVIDER: str = os.getenv("SMS_PROVIDER", "kavenegar")
    SMS_API_KEY: Optional[str] = os.getenv("SMS_API_KEY")
    SMS_SENDER_NUMBER: Optional[str] = os.getenv("SMS_SENDER_NUMBER")
    SMS_VERIFICATION_TEMPLATE: Optional[str] = os.getenv("SMS_VERIFICATION_TEMPLATE")
    SMS_RESET_PASSWORD_TEMPLATE: Optional[str] = os.getenv("SMS_RESET_PASSWORD_TEMPLATE")
    SMS_2FA_TEMPLATE: Optional[str] = os.getenv("SMS_2FA_TEMPLATE")
    
    # ===== 2FA =====
    TOTP_ISSUER: str = os.getenv("TOTP_ISSUER", "FarmTech")
    TOTP_PERIOD: int = int(os.getenv("TOTP_PERIOD", 30))
    TOTP_DIGITS: int = int(os.getenv("TOTP_DIGITS", 6))
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()


# ============================================================
# 🔧 CORS_ORIGINS به عنوان متغیر جداگانه
# ============================================================
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]