# backend/app/crud/ph_calculator.py
"""عملیات CRUD «اصلاح pH» (PhAdjustment) و واکشی اسید/بازهای پایگاه‌داده کود کاربر"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from app.models import Fertilizer, PhAdjustment

logger = logging.getLogger(__name__)


# ============================================================
# اسید/بازها از پایگاه‌داده‌ی کود «خود کاربر»
# ============================================================
def list_adjuster_fertilizers(db: Session, user_id: int) -> List[Fertilizer]:
    """کودهای کاربر که اسید یا باز تنظیم‌کنندهٔ pH هستند (is_acid یا is_base)."""
    return (
        db.query(Fertilizer)
        .filter(
            Fertilizer.user_id == user_id,
            or_(Fertilizer.is_acid.is_(True), Fertilizer.is_base.is_(True)),
        )
        .order_by(Fertilizer.name)
        .all()
    )


def get_user_fertilizer(db: Session, fertilizer_id: int, user_id: int) -> Optional[Fertilizer]:
    return (
        db.query(Fertilizer)
        .filter(Fertilizer.id == fertilizer_id, Fertilizer.user_id == user_id)
        .first()
    )


# ============================================================
# اصلاح‌ها (تاریخچه)
# ============================================================
def create_adjustment(db: Session, user_id: int, report_id: int, data: Dict[str, Any], activate: bool = False) -> PhAdjustment:
    try:
        record = PhAdjustment(user_id=user_id, report_id=report_id, is_active=False, **data)
        db.add(record)
        db.flush()
        if activate:
            _activate(db, record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def list_adjustments(db: Session, user_id: int, report_id: int, limit: int = 100) -> List[PhAdjustment]:
    return (
        db.query(PhAdjustment)
        .filter(PhAdjustment.user_id == user_id, PhAdjustment.report_id == report_id)
        .order_by(desc(PhAdjustment.created_at), desc(PhAdjustment.id))
        .limit(limit)
        .all()
    )


def get_adjustment(db: Session, adj_id: int, user_id: int) -> Optional[PhAdjustment]:
    return (
        db.query(PhAdjustment)
        .filter(PhAdjustment.id == adj_id, PhAdjustment.user_id == user_id)
        .first()
    )


def get_active_adjustment(db: Session, user_id: int, report_id: int) -> Optional[PhAdjustment]:
    return (
        db.query(PhAdjustment)
        .filter(
            PhAdjustment.user_id == user_id,
            PhAdjustment.report_id == report_id,
            PhAdjustment.is_active.is_(True),
        )
        .first()
    )


def _activate(db: Session, record: PhAdjustment) -> None:
    """هر گزارش فقط یک اصلاح فعال دارد؛ ابتدا فعال قبلی خاموش می‌شود."""
    db.query(PhAdjustment).filter(
        PhAdjustment.report_id == record.report_id,
        PhAdjustment.is_active.is_(True),
        PhAdjustment.id != record.id,
    ).update({PhAdjustment.is_active: False}, synchronize_session=False)
    db.flush()
    record.is_active = True


def set_adjustment_active(db: Session, record: PhAdjustment, active: bool) -> PhAdjustment:
    try:
        if active:
            _activate(db, record)
        else:
            record.is_active = False
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def delete_adjustment(db: Session, record: PhAdjustment) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise
