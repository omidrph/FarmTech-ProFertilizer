# backend/app/main.py
"""
نقطه ورود اصلی برنامه FastAPI
FarmTech - ProFertilizer Management System
نسخه امنیتی کامل
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
import time
import json

from app.config import settings, CORS_ORIGINS
from app.database import create_tables, SessionLocal
from app.routes import router
from app.security import get_current_user
from app.models import User
from app.middleware.rate_limit import RateLimiter

# ===== Import برای بارگذاری کودهای سیستمی =====
from app.seeds.fertilizer_seeds import (
    seed_system_fertilizers,
    get_system_fertilizers_count
)

# ===== Import برای بارگذاری رسپی‌های سیستمی =====
from app.seeds.recipe_seeds import (
    seed_system_recipes,
    get_system_recipes_count
)

# ===== تنظیمات Logger =====
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== ایجاد اپلیکیشن FastAPI =====
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="سیستم هوشمند نسخه‌نویسی کود و تغذیه - FarmTech",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# ============================================================
# 🔐 اضافه کردن Rate Limiter Middleware
# ============================================================
app.add_middleware(RateLimiter)

# ============================================================
# 🔐 اضافه کردن Middleware محدودیت حجم درخواست
# ============================================================
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    """
    محدود کردن حجم درخواست‌ها برای جلوگیری از حملات DoS
    """
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    
    # فقط برای متدهای POST, PUT, PATCH
    if request.method in ["POST", "PUT", "PATCH"]:
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > MAX_SIZE:
                    return JSONResponse(
                        status_code=413,
                        content={"detail": "حجم داده‌های ارسالی بیش از حد مجاز است (حداکثر ۱۰ مگابایت)"}
                    )
            except ValueError:
                pass
    
    return await call_next(request)

# ============================================================
# 🔐 اضافه کردن Headers امنیتی
# ============================================================
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    اضافه کردن Headers امنیتی به تمام پاسخ‌ها
    """
    response = await call_next(request)
    
    # جلوگیری از MIME Type Sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # جلوگیری از Clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    
    # HSTS (فقط در محیط تولید)
    if not settings.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Content Security Policy (CSP)
    if settings.DEBUG:
        csp = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self' http://localhost:8000 http://localhost:3000;"
    else:
        csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self' data:; connect-src 'self' https://yourdomain.com;"
    
    response.headers["Content-Security-Policy"] = csp
    
    return response

# ============================================================
# 🔧 تنظیمات CORS (با CORS_ORIGINS از config.py)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=settings.CORS_EXPOSE_HEADERS,
    max_age=settings.CORS_MAX_AGE,
)

# ============================================================
# Exception Handlers (امنیتی) - ✅ اصلاح شده برای نمایش خطاهای دقیق
# ============================================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """مدیریت خطاهای HTTP - نمایش پیام‌های دقیق"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """مدیریت خطاهای اعتبارسنجی"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.error(f"Validation Error: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "خطا در اعتبارسنجی داده‌ها. لطفاً اطلاعات را بررسی کنید.",
            "errors": errors if settings.DEBUG else []
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    مدیریت خطاهای عمومی - نمایش پیام‌های دقیق برای خطاهای خاص
    """
    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    # ✅ اگر خطا از نوع ValueError باشد، پیام آن را برگردان
    if isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc), "status_code": 400}
        )
    
    # در حالت Debug، جزئیات کامل خطا نمایش داده شود
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "خطای داخلی سرور",
                "message": str(exc),
                "traceback": traceback.format_exc(),
                "status_code": 500
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "خطای داخلی سرور. لطفاً با پشتیبانی تماس بگیرید.", "status_code": 500}
    )

# ============================================================
# Middleware برای لاگ‌گیری امنیتی درخواست‌ها
# ============================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    لاگ‌گیری همه درخواست‌های HTTP با حذف اطلاعات حساس
    """
    start_time = time.time()
    
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "client": request.client.host if request.client else "unknown"
    }
    
    if request.query_params:
        sensitive_params = ["password", "token", "secret", "api_key", "code"]
        safe_params = {}
        for k, v in request.query_params.items():
            if k.lower() in sensitive_params:
                safe_params[k] = "***"
            else:
                safe_params[k] = v
        log_data["query_params"] = safe_params
    
    logger.info(f"📤 Request: {json.dumps(log_data, ensure_ascii=False)}")
    
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"📥 {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response

# ============================================================
# مسیرهای اصلی
# ============================================================
@app.get("/")
async def root():
    """مسیر ریشه - اطلاعات پایه برنامه"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """بررسی سلامت سرور"""
    return {"status": "healthy", "database": "connected"}

@app.get("/api/v1/auth/test")
async def auth_test(current_user: User = Depends(get_current_user)):
    """تست احراز هویت"""
    return {
        "message": "✅ احراز هویت موفق",
        "user": {
            "id": current_user.id,
            "phone": current_user.phone_number,
            "full_name": current_user.full_name
        }
    }

# ============================================================
# ثبت Routerها
# ============================================================
app.include_router(router, prefix=settings.API_PREFIX)

# ============================================================
# رویدادهای Startup/Shutdown
# ============================================================
@app.on_event("startup")
async def startup_event():
    """رویداد شروع برنامه"""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info(f"🗄️ Database URL: {settings.DATABASE_URL}")
    
    try:
        create_tables()
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return
    
    db = SessionLocal()
    
    try:
        try:
            fertilizer_count = get_system_fertilizers_count(db)
            logger.info(f"📊 تعداد کودهای سیستمی فعلی: {fertilizer_count}")
            
            if fertilizer_count == 0:
                logger.info("🌱 در حال بارگذاری کودهای سیستمی...")
                stats = seed_system_fertilizers(db)
                
                logger.info(
                    f"✅ کودهای سیستمی بارگذاری شدند - "
                    f"اضافه شده: {stats['added']} | "
                    f"رد شده: {stats['skipped']} | "
                    f"خطا: {len(stats['errors'])}"
                )
                
                if stats['errors']:
                    for err in stats['errors']:
                        logger.warning(f"⚠️  خطا در {err['name']}: {err['error']}")
            else:
                logger.info(f"✅ کودهای سیستمی از قبل موجود هستند ({fertilizer_count} مورد)")
                
        except Exception as e:
            logger.error(f"❌ خطا در بارگذاری کودهای سیستمی: {e}")
            db.rollback()
        
        try:
            recipe_count = get_system_recipes_count(db)
            logger.info(f"📊 تعداد رسپی‌های سیستمی فعلی: {recipe_count}")
            
            if recipe_count == 0:
                logger.info("📋 در حال بارگذاری رسپی‌های سیستمی...")
                stats = seed_system_recipes(db)
                
                logger.info(
                    f"✅ رسپی‌های سیستمی بارگذاری شدند - "
                    f"اضافه شده: {stats['added']} | "
                    f"رد شده: {stats['skipped']} | "
                    f"خطا: {len(stats['errors'])}"
                )
                
                if stats['errors']:
                    for err in stats['errors']:
                        logger.warning(f"⚠️  خطا در {err['name']}: {err['error']}")
            else:
                logger.info(f"✅ رسپی‌های سیستمی از قبل موجود هستند ({recipe_count} مورد)")
                
        except Exception as e:
            logger.error(f"❌ خطا در بارگذاری رسپی‌های سیستمی: {e}")
            db.rollback()
            
    except Exception as e:
        logger.error(f"❌ خطا در فرآیند startup: {e}")
    finally:
        db.close()
    
    logger.info(f"🎉 {settings.APP_NAME} آماده استفاده است!")

@app.on_event("shutdown")
async def shutdown_event():
    """رویداد توقف برنامه"""
    logger.info(f"👋 Shutting down {settings.APP_NAME}")