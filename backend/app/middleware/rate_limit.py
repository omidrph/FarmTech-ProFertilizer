# backend/app/middleware/rate_limit.py
"""Rate Limiting Middleware برای جلوگیری از حملات Brute-Force"""

import time
from typing import Dict, List, Tuple
from collections import defaultdict
from datetime import datetime

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.security_logger import log_security_event

import logging

logger = logging.getLogger(__name__)


class RateLimiter(BaseHTTPMiddleware):
    """
    Middleware محدودیت تعداد درخواست‌ها
    
    ویژگی‌ها:
    - محدودیت بر اساس IP
    - محدودیت بر اساس مسیر (endpoint)
    - ثبت رویدادهای امنیتی برای تلاش‌های بیش از حد
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.max_requests = settings.RATE_LIMIT_MAX_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW_SECONDS
        
        # مسیرهایی که نیاز به Rate Limiting دارند
        self.limited_paths = [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/forgot-password",
            "/api/v1/auth/reset-password",
            "/api/v1/auth/verify-2fa",
            "/api/v1/auth/enable-2fa",
        ]
        
        logger.info(f"🔒 Rate Limiter initialized: {self.max_requests} requests per {self.window_seconds}s")
    
    async def dispatch(self, request: Request, call_next):
        """
        پردازش درخواست و اعمال محدودیت
        """
        # دریافت مسیر درخواست
        path = request.url.path
        
        # اگر مسیر در لیست محدودیت‌ها نیست، عبور کن
        if not any(path.startswith(limited_path) for limited_path in self.limited_paths):
            return await call_next(request)
        
        # دریافت IP واقعی (با توجه به Proxy)
        client_ip = self._get_client_ip(request)
        
        # کلید منحصر به فرد برای هر IP و مسیر
        key = f"{client_ip}:{path}"
        
        # پاک کردن درخواست‌های قدیمی‌تر از پنجره زمانی
        now = time.time()
        self.requests[key] = [t for t in self.requests[key] if now - t < self.window_seconds]
        
        # بررسی تعداد درخواست‌ها
        if len(self.requests[key]) >= self.max_requests:
            # ثبت رویداد امنیتی
            try:
                from app.database import get_db
                db = next(get_db())
                log_security_event(
                    db=db,
                    event_type="RATE_LIMIT_EXCEEDED",
                    ip_address=client_ip,
                    endpoint=path,
                    method=request.method,
                    details={
                        "attempts": len(self.requests[key]),
                        "max_allowed": self.max_requests,
                        "window_seconds": self.window_seconds
                    },
                    severity="WARNING"
                )
                db.close()
            except Exception as e:
                logger.error(f"Error logging rate limit event: {e}")
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً {self.window_seconds // 60} دقیقه دیگر تلاش کنید."
            )
        
        # اضافه کردن درخواست فعلی
        self.requests[key].append(now)
        
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """
        دریافت IP واقعی کاربر با توجه به Proxy
        
        Args:
            request: درخواست FastAPI
        
        Returns:
            str: آدرس IP
        """
        # اول از X-Forwarded-For (برای Proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # اولین IP در لیست، IP اصلی است
            return forwarded.split(",")[0].strip()
        
        # دوم از X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # در نهایت از client.host
        if request.client:
            return request.client.host
        
        return "unknown"


# ایجاد نمونه برای استفاده در main.py
rate_limiter = RateLimiter