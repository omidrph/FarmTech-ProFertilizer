# backend/app/main.py
"""نقطه ورود اصلی برنامه FastAPI"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from app.config import settings
from app.database import create_tables
from app.routes import router
from app.security import get_current_user
from app.models import User

# ===== تنظیمات Logger =====
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== ایجاد اپلیکیشن FastAPI =====
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="سیستم هوشمند نسخه‌نویسی کود و تغذیه - FarmTech",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ===== تنظیمات CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Exception Handlers =====
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
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
        content={"detail": "خطا در اعتبارسنجی داده‌ها", "errors": errors}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "خطای داخلی سرور",
            "message": str(exc) if settings.DEBUG else "لطفاً با پشتیبانی تماس بگیرید"
        }
    )

# ===== Middleware برای لاگ‌گیری =====
@app.middleware("http")
async def log_requests(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    return response

# ===== مسیرهای اصلی =====
@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# ===== مسیر تست احراز هویت =====
@app.get("/api/v1/auth/test")
async def auth_test(current_user: User = Depends(get_current_user)):
    """تست get_current_user - اگر این کار کند یعنی همه چیز درست است"""
    return {
        "message": "✅ احراز هویت موفق",
        "user": {
            "id": current_user.id,
            "phone": current_user.phone_number,
            "full_name": current_user.full_name
        }
    }

# ===== ثبت Routerها =====
app.include_router(router, prefix=settings.API_PREFIX)

# ===== رویدادهای Startup/Shutdown =====
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"SECRET_KEY: {settings.SECRET_KEY[:10]}...")
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")