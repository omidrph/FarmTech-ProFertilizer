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
    # 🔧 دیگر مقدار پیش‌فرض ناامن ندارد؛ اگر در .env تنظیم نشود، برنامه با خطا متوقف می‌شود
    # تا از اجرای تصادفی با کلید عمومی/شناخته‌شده در پروڈاکشن جلوگیری شود.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("SESSION_EXPIRY_HOURS", 24)) * 60
    
    # ===== تنظیمات برنامه =====
    APP_NAME: str = "FarmTech - ProFertilizer"
    APP_VERSION: str = "0.1.0"
    # 🔧 پیش‌فرض DEBUG اکنون False است (قبلاً "True" بود که برای پروڈاکشن خطرناک است:
    # نمایش traceback کامل به کاربر، باز بودن /docs و /redoc، و CSP ضعیف‌تر)
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
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
    
    # ===== 🔧 محیط اجرا (برای تصمیم‌گیری‌های سخت‌گیرانه‌تر در پروڈاکشن) =====
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()


# ============================================================
# 🔧 اعتبارسنجی تنظیمات حیاتی امنیتی هنگام بالا آمدن برنامه
# ============================================================
# اگر DEBUG خاموش باشد (یعنی این پروڈاکشن است) ولی SECRET_KEY خالی یا
# همان مقدار پیش‌فرض قدیمی/ناامن باشد، برنامه عمداً بالا نمی‌آید تا
# با یک کلید شناخته‌شده/خالی در معرض دید عموم قرار نگیرد.
_INSECURE_SECRET_KEYS = {
    "",
    "your-super-secret-key-change-this-in-production",
    "changeme",
    "secret",
}

if not settings.DEBUG and settings.SECRET_KEY in _INSECURE_SECRET_KEYS:
    raise RuntimeError(
        "❌ SECRET_KEY تنظیم نشده یا مقدار پیش‌فرض ناامن دارد. "
        "قبل از اجرای پروڈاکشن (DEBUG=False)، یک مقدار تصادفی و امن در "
        "متغیر محیطی SECRET_KEY قرار دهید. می‌توانید با دستور زیر یک مقدار "
        "امن تولید کنید: python -c \"import secrets; print(secrets.token_urlsafe(64))\""
    )

if settings.DEBUG and settings.SECRET_KEY in _INSECURE_SECRET_KEYS:
    # فقط هشدار در حالت توسعه؛ اجرا را متوقف نمی‌کند
    import logging
    logging.getLogger(__name__).warning(
        "⚠️ SECRET_KEY تنظیم نشده - از یک مقدار موقت تصادفی برای این اجرا استفاده می‌شود. "
        "این برای پروڈاکشن مناسب نیست."
    )
    import secrets as _secrets
    settings.SECRET_KEY = _secrets.token_urlsafe(64)


# ============================================================
# 🔧 CORS_ORIGINS اکنون واقعاً از متغیر محیطی خوانده می‌شود
# ============================================================
# قبلاً این مقدار هاردکد بود و متغیر محیطی CORS_ORIGINS (که در
# docker-compose.yml ست می‌شد) کاملاً نادیده گرفته می‌شد. یعنی حتی با
# تنظیم دامنه‌ی واقعی در .env، بک‌اند درخواست‌های CORS از آن دامنه را رد
# می‌کرد. اکنون:
#   - اگر CORS_ORIGINS در .env/env تنظیم شده باشد، همان استفاده می‌شود
#     (لیستی جدا شده با کاما، مثل: https://example.com,https://www.example.com)
#   - در غیر این صورت، فقط در حالت DEBUG=True آدرس‌های localhost پیش‌فرض
#     قرار می‌گیرند تا در پروڈاکشن به‌صورت ناخواسته باز نماند.
_cors_env = os.getenv("CORS_ORIGINS", "").strip()

if _cors_env:
    CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_env.split(",") if origin.strip()]
elif settings.DEBUG:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
else:
    # پروڈاکشن بدون تنظیم صریح CORS_ORIGINS: به‌جای باز گذاشتن یا
    # سکوت، صراحتاً خالی می‌ماند (یعنی هیچ دامنه‌ای مجاز نیست) تا مشکل
    # زود در لاگ/تست دیده شود، نه بعد از دیپلوی.
    CORS_ORIGINS = []
    import logging
    logging.getLogger(__name__).warning(
        "⚠️ CORS_ORIGINS در متغیرهای محیطی تنظیم نشده است. در حالت پروڈاکشن "
        "هیچ دامنه‌ای برای CORS مجاز نخواهد بود تا زمانی که آن را در .env "
        "تنظیم کنید، مثال: CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com"
    )