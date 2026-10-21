# backend/app/seeds/fertilizer_seeds.py
"""
فهرست کودهای شرکتی (عمومی و فقط‌خواندنی برای همهٔ کاربران)

مفهوم «کود سیستمی» از برنامه حذف شده است؛ فقط «کود شرکتی» داریم.
فعلاً فهرست خالی است و داده‌های درست بعداً اینجا اضافه می‌شود.

قالب هر کود (elements = درصد وزنی «عنصر» در محصول؛ label_values = همان مقدار به‌شکل روی برچسب، فقط برای نمایش):

    {
        "name": "نام تجاری کود",
        "formula": "KNO₃",
        "brand": "نام شرکت",
        "category": "ماکرو",
        "form": "crystal",             # powder | crystal | liquid | granular
        "concentration": 99.0,         # خلوص روی برچسب (توضیحی)
        "elements": {"N-NO3": 13.0, "K": 38.7},
        "label_values": {"N-NO3": 13.0, "K2O": 46.6},
        "price_per_kg": 0,
        "is_acid": False, "is_base": False,
        "density_g_ml": None,
        "description": "",
    }
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Fertilizer

logger = logging.getLogger(__name__)

# نام قبلی حفظ شده تا import ها در main.py و seeds/__init__.py نشکنند
SYSTEM_FERTILIZERS: List[Dict[str, Any]] = []


def seed_system_fertilizers(db: Session) -> Dict[str, int]:
    """افزودن کودهای شرکتی به دیتابیس (idempotent بر اساس نام)"""
    stats = {"added": 0, "skipped": 0, "total": len(SYSTEM_FERTILIZERS), "errors": []}
    if not SYSTEM_FERTILIZERS:
        return stats

    try:
        from sqlalchemy import text as _text
        db.execute(_text("SELECT pg_advisory_xact_lock(727001)"))
    except Exception:
        db.rollback()

    for d in SYSTEM_FERTILIZERS:
        try:
            exists = db.query(Fertilizer).filter(
                Fertilizer.name == d["name"],
                Fertilizer.is_system_default == True,  # noqa: E712  (فلگ داخلی = فهرست شرکتی عمومی)
                Fertilizer.user_id == None,            # noqa: E711
            ).first()
            if exists:
                stats["skipped"] += 1
                continue
            db.add(Fertilizer(
                user_id=None,
                name=d["name"],
                formula=d.get("formula"),
                brand=d.get("brand"),
                category=d.get("category"),
                form=d.get("form"),
                concentration=d.get("concentration", 100.0),
                elements=d.get("elements", {}),
                label_values=d.get("label_values"),
                price_per_kg=d.get("price_per_kg", 0.0),
                is_acid=d.get("is_acid", False),
                is_base=d.get("is_base", False),
                density_g_ml=d.get("density_g_ml"),
                description=d.get("description"),
                is_system_default=True,
                source_system_id=None,
            ))
            stats["added"] += 1
        except Exception as e:
            stats["errors"].append({"name": d.get("name"), "error": str(e)})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        stats["errors"].append({"name": "COMMIT", "error": str(e)})
    return stats


def get_system_fertilizers_count(db: Session) -> int:
    return db.query(Fertilizer).filter(
        Fertilizer.is_system_default == True,  # noqa: E712
        Fertilizer.user_id == None,            # noqa: E711
    ).count()


def clear_system_fertilizers(db: Session) -> int:
    count = db.query(Fertilizer).filter(
        Fertilizer.is_system_default == True,  # noqa: E712
        Fertilizer.user_id == None,            # noqa: E711
    ).delete()
    db.commit()
    return count
