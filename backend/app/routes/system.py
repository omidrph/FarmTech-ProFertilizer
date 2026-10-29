# backend/app/routes/system.py
"""
مسیرهای عمومی وضعیت سیستم (بدون نیاز به ورود)
- وضعیت حالت تعمیر و باز/بسته بودن ثبت‌نام
- اعلان‌های فعال (با فیلتر مخاطب؛ اگر کاربر وارد شده باشد نقشش لحاظ می‌شود)
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Announcement, User
from app.security import get_app_settings, get_current_user

system_router = APIRouter(prefix="/system", tags=["System"])


async def _optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None


@system_router.get("/status")
async def system_status(db: Session = Depends(get_db), user: Optional[User] = Depends(_optional_user)):
    now = datetime.now(timezone.utc)
    cfg = get_app_settings(db)
    maint = cfg.get("maintenance") or {}
    reg = cfg.get("registration") or {}

    role = user.role if user else None
    audiences = ["all"] + (["plus"] if role in ("plus", "admin") else []) + (["user"] if role in (None, "user") else [])
    anns = (
        db.query(Announcement)
        .filter(Announcement.is_active == True,  # noqa: E712
                Announcement.audience.in_(audiences),
                or_(Announcement.starts_at == None, Announcement.starts_at <= now),  # noqa: E711
                or_(Announcement.ends_at == None, Announcement.ends_at >= now))      # noqa: E711
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )
    return {
        "maintenance": {"enabled": bool(maint.get("enabled")), "message": maint.get("message") or ""},
        "registration": {"enabled": reg.get("enabled") is not False, "message": reg.get("message") or ""},
        "announcements": [
            {"id": a.id, "title": a.title, "body": a.body, "level": a.level} for a in anns
        ],
    }
