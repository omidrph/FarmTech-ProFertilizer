# backend/app/security_logger.py
"""سیستم لاگ‌گیری امنیتی FarmTech"""

import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models import SecurityLog

logger = logging.getLogger(__name__)


def log_security_event(
    db: Session,
    event_type: str,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None,
    severity: str = "INFO"
) -> SecurityLog:
    """
    ثبت رویداد امنیتی در دیتابیس
    
    Args:
        db: Session دیتابیس
        event_type: نوع رویداد (LOGIN_SUCCESS, LOGIN_FAILED, etc.)
        user_id: شناسه کاربر (اختیاری)
        ip_address: آدرس IP
        user_agent: User-Agent مرورگر
        endpoint: آدرس endpoint
        method: متد HTTP
        details: جزئیات اضافی
        error_message: پیام خطا (در صورت وجود)
        severity: سطح اهمیت (INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        SecurityLog: شیء ثبت شده
    """
    try:
        log_entry = SecurityLog(
            user_id=user_id,
            event_type=event_type,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            method=method,
            details=details,
            error_message=error_message
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        # همچنین در لاگ فایل نیز ثبت شود
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "ip": ip_address,
            "details": details
        }
        
        if severity == "CRITICAL":
            logger.critical(json.dumps(log_data, ensure_ascii=False))
        elif severity == "ERROR":
            logger.error(json.dumps(log_data, ensure_ascii=False))
        elif severity == "WARNING":
            logger.warning(json.dumps(log_data, ensure_ascii=False))
        else:
            logger.info(json.dumps(log_data, ensure_ascii=False))
        
        return log_entry
        
    except Exception as e:
        logger.error(f"Error logging security event: {e}")
        # اگر خطا در ذخیره لاگ بود، حداقل در لاگ فایل ثبت کن
        try:
            logger.warning(f"SECURITY EVENT: {event_type} - User: {user_id} - IP: {ip_address}")
        except:
            pass
        return None


def get_security_logs(
    db: Session,
    user_id: Optional[int] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
    skip: int = 0
) -> list:
    """
    دریافت لاگ‌های امنیتی
    
    Args:
        db: Session دیتابیس
        user_id: فیلتر بر اساس کاربر
        event_type: فیلتر بر اساس نوع رویداد
        severity: فیلتر بر اساس سطح اهمیت
        limit: تعداد نتایج
        skip: تعداد رد شدن
    
    Returns:
        list: لیست لاگ‌ها
    """
    query = db.query(SecurityLog)
    
    if user_id:
        query = query.filter(SecurityLog.user_id == user_id)
    
    if event_type:
        query = query.filter(SecurityLog.event_type == event_type)
    
    if severity:
        query = query.filter(SecurityLog.severity == severity)
    
    return query.order_by(SecurityLog.created_at.desc()).offset(skip).limit(limit).all()


def cleanup_old_security_logs(db: Session, days: int = 90) -> int:
    """
    پاک‌سازی لاگ‌های قدیمی
    
    Args:
        db: Session دیتابیس
        days: تعداد روزهای نگهداری
    
    Returns:
        int: تعداد لاگ‌های حذف شده
    """
    from datetime import datetime, timedelta
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    count = db.query(SecurityLog).filter(
        SecurityLog.created_at < cutoff
    ).delete()
    db.commit()
    
    logger.info(f"🧹 {count} security logs older than {days} days deleted")
    return count