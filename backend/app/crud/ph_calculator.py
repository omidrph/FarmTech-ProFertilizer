# backend/app/crud/ph_calculator.py
"""
عملیات CRUD برای مدل PhCalculation (تاریخچه‌ی ماشین‌حساب pH)
"""
from typing import Any, Dict, List, Optional

import logging

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Fertilizer, PhCalculation

logger = logging.getLogger(__name__)


def save_ph_calculation(
    db: Session,
    user_id: int,
    report_id: Optional[int],
    method: Optional[str],
    direction: Optional[str],
    inputs: Dict[str, Any],
    outputs: Dict[str, Any],
    chemical_name: Optional[str] = None,
    fertilizer_id: Optional[int] = None,
    note: Optional[str] = None,
    record_type: str = "correction",
    ec_ms_cm: Optional[float] = None,
) -> PhCalculation:
    """ذخیره‌ی یک رکورد pH: یا یک محاسبه‌ی کامل اصلاحی ('correction') یا فقط یک اندازه‌گیری پایشی ('monitoring')"""
    try:
        record = PhCalculation(
            user_id=user_id,
            report_id=report_id,
            method=method,
            direction=direction,
            record_type=record_type,
            ec_ms_cm=ec_ms_cm,
            inputs=inputs,
            outputs=outputs,
            chemical_name=chemical_name,
            fertilizer_id=fertilizer_id,
            note=note,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info(f"PhCalculation saved: {record.id} ({record_type})")
        return record
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving ph calculation: {e}")
        raise e


def get_ph_calculations(
    db: Session,
    user_id: int,
    report_id: Optional[int] = None,
    record_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[PhCalculation]:
    """دریافت تاریخچه‌ی محاسبات/پایش‌های pH کاربر (اختیاری: فیلتر بر اساس گزارش و نوع رکورد)"""
    try:
        query = db.query(PhCalculation).filter(PhCalculation.user_id == user_id)
        if report_id is not None:
            query = query.filter(PhCalculation.report_id == report_id)
        if record_type is not None:
            query = query.filter(PhCalculation.record_type == record_type)
        return query.order_by(desc(PhCalculation.created_at)).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting ph calculations: {e}")
        return []


def get_latest_correction(db: Session, user_id: int, report_id: int) -> Optional[PhCalculation]:
    """آخرین رکورد نوع 'correction' برای یک گزارش - برای نمایش در مخزن C صفحه‌ی محاسبه کود"""
    try:
        return (
            db.query(PhCalculation)
            .filter(
                PhCalculation.user_id == user_id,
                PhCalculation.report_id == report_id,
                PhCalculation.record_type == "correction",
            )
            .order_by(desc(PhCalculation.created_at))
            .first()
        )
    except Exception as e:
        logger.error(f"Error getting latest ph correction: {e}")
        return None


def get_ph_calculation_by_id(db: Session, calc_id: int) -> Optional[PhCalculation]:
    try:
        return db.query(PhCalculation).filter(PhCalculation.id == calc_id).first()
    except Exception as e:
        logger.error(f"Error getting ph calculation: {e}")
        return None


def delete_ph_calculation(db: Session, calc_id: int, user_id: int) -> bool:
    """حذف یک رکورد تاریخچه (فقط اگر متعلق به همان کاربر باشد)"""
    try:
        record = (
            db.query(PhCalculation)
            .filter(PhCalculation.id == calc_id, PhCalculation.user_id == user_id)
            .first()
        )
        if not record:
            return False
        db.delete(record)
        db.commit()
        logger.info(f"PhCalculation deleted: {calc_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting ph calculation: {e}")
        raise e


def get_acid_fertilizers_for_user(db: Session, user_id: int) -> List[Fertilizer]:
    """
    اسیدهای واقعی موجود در پایگاه‌داده‌ی کود (سیستمی + شخصی کاربر) -
    همان منبع درستِ «مخزن C» که به‌جای لیست ثابت و هاردکد قبلی استفاده
    می‌شود.
    """
    try:
        return (
            db.query(Fertilizer)
            .filter(
                Fertilizer.is_acid.is_(True),
                (Fertilizer.user_id == user_id) | (Fertilizer.is_system_default.is_(True)),
            )
            .order_by(Fertilizer.name)
            .all()
        )
    except Exception as e:
        logger.error(f"Error getting acid fertilizers: {e}")
        return []


def get_fertilizer_owned_or_system(db: Session, fertilizer_id: int, user_id: int) -> Optional[Fertilizer]:
    """یک کود را فقط اگر متعلق به کاربر یا سیستمی باشد برمی‌گرداند (جلوگیری از دسترسی به کود کاربر دیگر)"""
    try:
        return (
            db.query(Fertilizer)
            .filter(
                Fertilizer.id == fertilizer_id,
                (Fertilizer.user_id == user_id) | (Fertilizer.is_system_default.is_(True)),
            )
            .first()
        )
    except Exception as e:
        logger.error(f"Error getting fertilizer: {e}")
        return None
