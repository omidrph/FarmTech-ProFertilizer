# backend/app/seeds/fertilizer_seeds.py
"""
Seed داده‌های اولیه کودهای سیستمی
این فایل شامل کودهای استاندارد و پرکاربرد در کشاورزی و گلخانه‌داری است.

منبع: جداول استاندارد کودهای شیمیایی
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Fertilizer

logger = logging.getLogger(__name__)


# ============================================================
# لیست کامل کودهای سیستمی (استاندارد)
# ============================================================
SYSTEM_FERTILIZERS: List[Dict[str, Any]] = [
    # ============================================================
    # 🟢 کودهای نیتروژنه
    # ============================================================
    {
        "name": "کلرید آمونیوم (NH4Cl)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "price_per_kg": 30000,
        "elements": {"N-NH4": 26.185, "Cl": 66.275},
        "is_acid": False,
        "description": "تامین نیتروژن آمونیومی و کلر - مناسب برنج و محصولات خاص",
        "npk_ratio": "26-0-0"
    },
    {
        "name": "دی آمونیوم فسفات ((NH4)2HPO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "price_per_kg": 50000,
        "elements": {"N-NH4": 21.216, "P": 23.478},
        "is_acid": False,
        "description": "تامین فسفر و نیتروژن - افزایش عملکرد و کیفیت محصول",
        "npk_ratio": "21-53-0"
    },
    {
        "name": "مونو آمونیوم فسفات (NH4H2PO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "price_per_kg": 48000,
        "elements": {"N-NH4": 12.178, "P": 26.930},
        "is_acid": False,
        "description": "تامین فسفر و نیتروژن - مناسب شروع رشد و ریشه‌زایی",
        "npk_ratio": "12-61-0"
    },
    {
        "name": "سولفات آمونیوم ((NH4)2SO4)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "price_per_kg": 32000,
        "elements": {"N-NH4": 21.200, "S": 24.266},
        "is_acid": False,
        "description": "تامین نیتروژن آمونیومی و گوگرد - کاهش pH خاک",
        "npk_ratio": "21-0-0"
    },
    {
        "name": "نیترات آمونیوم (NH4NO3)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "price_per_kg": 35000,
        "elements": {"N-NO3": 17.499, "N-NH4": 17.499},
        "is_acid": False,
        "description": "کود نیتروژنی با دو فرم نیترات و آمونیوم - جذب سریع و پایدار",
        "npk_ratio": "34-0-0"
    },

    # ============================================================
    # 🟡 کودهای بور
    # ============================================================
    {
        "name": "اسید بوریک (H3BO3)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 120000,
        "elements": {"B": 17.480},
        "is_acid": False,
        "description": "تامین بور - بهبود گرده‌افشانی و تشکیل میوه",
        "npk_ratio": "0-0-0"
    },
    {
        "name": "بوراکس (Na2B4O7.10H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 110000,
        "elements": {"B": 11.352, "Na": 12.080},
        "is_acid": False,
        "description": "تامین بور و سدیم - مناسب خاک‌های اسیدی",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🟣 کودهای کلسیمی
    # ============================================================
    {
        "name": "کربنات کلسیم (CaCO3)",
        "brand": "استاندارد",
        "category": "کلسیمی",
        "form": "powder",
        "price_per_kg": 25000,
        "elements": {"Ca": 40.043},
        "is_acid": False,
        "description": "تامین کلسیم - افزایش pH خاک - اصلاح خاک‌های اسیدی",
        "npk_ratio": "0-0-0"
    },
    {
        "name": "فسفات کلسیم مونوبازیک (Ca(H2PO4)2.H2O)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "price_per_kg": 42000,
        "elements": {"Ca": 17.072, "P": 26.387},
        "is_acid": False,
        "description": "تامین فسفر و کلسیم - مناسب خاک‌های اسیدی",
        "npk_ratio": "0-60-0"
    },
    {
        "name": "نیترات کلسیم (Ca(NO3)2.4H2O)",
        "brand": "استاندارد",
        "category": "کلسیمی",
        "form": "crystal",
        "price_per_kg": 45000,
        "elements": {"N-NO3": 11.861, "Ca": 16.963},
        "is_acid": False,
        "description": "تامین کلسیم و نیتروژن نیتراتی - افزایش استحکام گیاه",
        "npk_ratio": "15-0-0"
    },
    {
        "name": "سولفات کلسیم دی‌هیدرات (CaSO4.2H2O)",
        "brand": "استاندارد",
        "category": "کلسیمی",
        "form": "powder",
        "price_per_kg": 28000,
        "elements": {"Ca": 23.281, "S": 18.621},
        "is_acid": False,
        "description": "تامین کلسیم و گوگرد - بهبود ساختار خاک",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🔴 کودهای مس
    # ============================================================
    {
        "name": "کلات مس EDTA (Cu-EDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 185000,
        "elements": {"Cu": 14.087},
        "is_acid": False,
        "description": "کلات مس با پایه EDTA - افزایش مقاومت به بیماری‌ها",
        "chelating_agent": "EDTA"
    },
    {
        "name": "نیترات مس (Cu(NO3)2.3H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "price_per_kg": 70000,
        "elements": {"Cu": 26.228, "N-NO3": 11.565},
        "is_acid": False,
        "description": "تامین مس و نیتروژن - مناسب محلول‌های غذایی",
        "npk_ratio": "12-0-0"
    },
    {
        "name": "سولفات مس (CuSO4.5H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "price_per_kg": 60000,
        "elements": {"Cu": 25.455, "S": 12.846},
        "is_acid": False,
        "description": "تامین مس و گوگرد - خاصیت ضدقارچی و باکتری‌کشی",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🟠 کودهای آهن
    # ============================================================
    {
        "name": "کلات آهن DTPA (Fe-DTPA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 230000,
        "elements": {"Fe": 10.955},
        "is_acid": False,
        "description": "کلات آهن با پایه DTPA - پایداری تا pH 8.5",
        "chelating_agent": "DTPA"
    },
    {
        "name": "کلات آهن EDDHA (Fe-EDDHA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 280000,
        "elements": {"Fe": 13.706},
        "is_acid": False,
        "description": "کلات آهن با پایه EDDHA - پایداری تا pH 9 - مناسب خاک‌های آهکی",
        "chelating_agent": "EDDHA"
    },
    {
        "name": "کلات آهن EDTA (Fe-EDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 180000,
        "elements": {"Fe": 13.691},
        "is_acid": False,
        "description": "کلات آهن با پایه EDTA - پایداری تا pH 8 - رفع کلروز",
        "chelating_agent": "EDTA"
    },
    {
        "name": "سولفات آهن (FeSO4.7H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "price_per_kg": 48000,
        "elements": {"Fe": 20.086, "S": 11.528},
        "is_acid": False,
        "description": "تامین آهن و گوگرد - کاهش pH خاک - مناسب کشت ارگانیک",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🟤 کودهای منیزیم
    # ============================================================
    {
        "name": "کربنات منیزیم (MgCO3)",
        "brand": "استاندارد",
        "category": "منیزیمی",
        "form": "powder",
        "price_per_kg": 32000,
        "elements": {"Mg": 28.834},
        "is_acid": False,
        "description": "تامین منیزیم - افزایش pH خاک",
        "npk_ratio": "0-0-0"
    },
    {
        "name": "نیترات منیزیم (Mg(NO3)2.6H2O)",
        "brand": "استاندارد",
        "category": "منیزیمی",
        "form": "crystal",
        "price_per_kg": 42000,
        "elements": {"N-NO3": 10.922, "Mg": 9.464},
        "is_acid": False,
        "description": "تامین منیزیم و نیتروژن - افزایش فتوسنتز",
        "npk_ratio": "11-0-0"
    },
    {
        "name": "سولفات منیزیم (MgSO4.7H2O)",
        "brand": "استاندارد",
        "category": "منیزیمی",
        "form": "crystal",
        "price_per_kg": 38000,
        "elements": {"Mg": 9.861, "S": 13.010},
        "is_acid": False,
        "description": "تامین منیزیم و گوگرد - افزایش کلروفیل و فتوسنتز",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🟢 کودهای منگنز
    # ============================================================
    {
        "name": "کلات منگنز EDTA (Mn-EDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 175000,
        "elements": {"Mn": 13.694},
        "is_acid": False,
        "description": "کلات منگنز با پایه EDTA - رفع زردی بین رگبرگ",
        "chelating_agent": "EDTA"
    },

    # ============================================================
    # 🟡 کودهای مولیبدن
    # ============================================================
    {
        "name": "مولیبدات سدیم (Na2MoO4.2H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 250000,
        "elements": {"Mo": 39.650, "Na": 19.001},
        "is_acid": False,
        "description": "تامین مولیبدن و سدیم - افزایش تثبیت نیتروژن",
        "npk_ratio": "0-0-0"
    },

    # ============================================================
    # 🟣 کودهای NPK کامل
    # ============================================================
    {
        "name": "کود 20-20-20",
        "brand": "استاندارد",
        "category": "NPK کامل",
        "form": "powder",
        "price_per_kg": 85000,
        "elements": {
            "N-NO3": 10.000,
            "N-NH4": 10.000,
            "P": 8.733,
            "K": 16.600
        },
        "is_acid": False,
        "description": "کود کامل NPK با نسبت مساوی - مناسب رشد عمومی گیاه",
        "npk_ratio": "20-20-20"
    },

    # ============================================================
    # 🔴 کودهای پتاسیمی
    # ============================================================
    {
        "name": "کربنات پتاسیم (K2CO3)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "powder",
        "price_per_kg": 52000,
        "elements": {"K": 56.579},
        "is_acid": False,
        "description": "تامین پتاسیم - افزایش pH محلول - مناسب تنظیم pH",
        "npk_ratio": "0-0-68"
    },
    {
        "name": "کلرید پتاسیم (KCl)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "crystal",
        "price_per_kg": 35000,
        "elements": {"K": 52.446, "Cl": 47.554},
        "is_acid": False,
        "description": "تامین پتاسیم و کلر - اقتصادی‌ترین منبع پتاسیم",
        "npk_ratio": "0-0-60"
    },
    {
        "name": "سیترات پتاسیم (C6H5K3O7.H2O)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "powder",
        "price_per_kg": 65000,
        "elements": {"K": 38.322},
        "is_acid": False,
        "description": "تامین پتاسیم آلی - بهبود جذب عناصر و کیفیت محصول",
        "npk_ratio": "0-0-46"
    },
    {
        "name": "دی پتاسیم فسفات (K2HPO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "price_per_kg": 58000,
        "elements": {"P": 17.768, "K": 44.830},
        "is_acid": False,
        "description": "تامین فسفر و پتاسیم - مناسب محلول‌های غذایی با pH متعادل",
        "npk_ratio": "0-40-53"
    },
    {
        "name": "مونو پتاسیم فسفات (KH2PO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "price_per_kg": 55000,
        "elements": {"P": 22.765, "K": 28.728},
        "is_acid": False,
        "description": "تامین فسفر و پتاسیم - تحریک گلدهی و میوه‌دهی",
        "npk_ratio": "0-52-34"
    },
    {
        "name": "نیترات پتاسیم (KNO3)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "crystal",
        "price_per_kg": 62000,
        "elements": {"N-NO3": 13.854, "K": 38.667},
        "is_acid": False,
        "description": "تامین پتاسیم و نیتروژن - مناسب گلدهی و میوه‌دهی",
        "npk_ratio": "13-0-46"
    },
    {
        "name": "سولفات پتاسیم (K2SO4)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "powder",
        "price_per_kg": 48000,
        "elements": {"K": 44.874, "S": 18.399},
        "is_acid": False,
        "description": "تامین پتاسیم و گوگرد - فاقد کلر - مناسب خاک‌های شور",
        "npk_ratio": "0-0-50"
    },

    # ============================================================
    # 🔵 کودهای سدیم
    # ============================================================
    {
        "name": "نیترات سدیم (NaNO3)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "price_per_kg": 28000,
        "elements": {"N-NO3": 16.480, "Na": 27.048},
        "is_acid": False,
        "description": "تامین نیتروژن و سدیم - مناسب خاک‌های اسیدی",
        "npk_ratio": "16-0-0"
    },

    # ============================================================
    # 🟠 کودهای اسید فسفریک
    # ============================================================
    {
        "name": "اسید فسفریک 75% (H3PO4)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "price_per_kg": 35000,
        "elements": {"P": 23.684},
        "is_acid": True,
        "acid_type": "H3PO4",
        "description": "اسید فسفریک 75% - برای تنظیم pH و تامین فسفر",
        "npk_ratio": "0-75-0"
    },

    # ============================================================
    # 🟡 کودهای روی
    # ============================================================
    {
        "name": "کلات روی EDTA (Zn-EDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 175000,
        "elements": {"Zn": 14.422},
        "is_acid": False,
        "description": "کلات روی با پایه EDTA - جذب بالا - رفع کمبود روی",
        "chelating_agent": "EDTA"
    },
    {
        "name": "نیترات روی (Zn(NO3)2.6H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "price_per_kg": 65000,
        "elements": {"Zn": 21.980, "N-NO3": 9.418},
        "is_acid": False,
        "description": "تامین روی و نیتروژن - مناسب محلول‌های غذایی",
        "npk_ratio": "10-0-0"
    },
    {
        "name": "سولفات روی مونوهیدرات (ZnSO4.H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "price_per_kg": 55000,
        "elements": {"Zn": 36.436, "S": 17.878},
        "is_acid": False,
        "description": "تامین روی و گوگرد - رفع علائم کمبود روی و کوچکی برگ",
        "npk_ratio": "0-0-0"
    },
]


# ============================================================
# تابع اجرای Seed
# ============================================================
def seed_system_fertilizers(db: Session) -> Dict[str, int]:
    """
    افزودن کودهای سیستمی به دیتابیس
    
    Args:
        db: Session دیتابیس
    
    Returns:
        Dict با آمار عملیات:
        - added: تعداد کودهای اضافه شده
        - skipped: تعداد کودهای رد شده (قبلاً وجود داشته)
        - total: تعداد کل کودهای سیستمی
    """
    stats = {
        "added": 0,
        "skipped": 0,
        "total": len(SYSTEM_FERTILIZERS),
        "errors": []
    }
    
    logger.info(f"🌱 شروع Seed کودهای سیستمی - تعداد: {stats['total']}")
    
    for fert_data in SYSTEM_FERTILIZERS:
        try:
            # بررسی وجود کود با همین نام
            existing = db.query(Fertilizer).filter(
                Fertilizer.name == fert_data["name"],
                Fertilizer.is_system_default == True
            ).first()
            
            if existing:
                stats["skipped"] += 1
                logger.debug(f"⏭️  رد شد (موجود): {fert_data['name']}")
                continue
            
            # ایجاد کود سیستمی جدید
            new_fertilizer = Fertilizer(
                user_id=None,  # کودهای سیستمی متعلق به کاربر خاصی نیستند
                name=fert_data["name"],
                brand=fert_data.get("brand"),
                category=fert_data.get("category"),
                form=fert_data.get("form"),
                price_per_kg=fert_data.get("price_per_kg", 0.0),
                elements=fert_data.get("elements", {}),
                is_acid=fert_data.get("is_acid", False),
                acid_type=fert_data.get("acid_type"),
                description=fert_data.get("description"),
                is_system_default=True,
                solubility=None,
                ph_level=None,
                application_method=None,
                packaging=None,
                registration_code=None,
                npk_ratio=fert_data.get("npk_ratio"),
                organic_matter=None,
                chelating_agent=fert_data.get("chelating_agent")
            )
            
            db.add(new_fertilizer)
            stats["added"] += 1
            logger.info(f"✅ اضافه شد: {fert_data['name']}")
            
        except Exception as e:
            stats["errors"].append({
                "name": fert_data["name"],
                "error": str(e)
            })
            logger.error(f"❌ خطا در افزودن {fert_data['name']}: {e}")
    
    # Commit کردن تغییرات
    try:
        db.commit()
        logger.info(
            f"🎉 Seed کامل شد - "
            f"اضافه شده: {stats['added']} | "
            f"رد شده: {stats['skipped']} | "
            f"خطا: {len(stats['errors'])}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"❌ خطا در commit: {e}")
        stats["errors"].append({"name": "COMMIT", "error": str(e)})
    
    return stats


def get_system_fertilizers_count(db: Session) -> int:
    """دریافت تعداد کودهای سیستمی موجود در دیتابیس"""
    return db.query(Fertilizer).filter(
        Fertilizer.is_system_default == True
    ).count()


def clear_system_fertilizers(db: Session) -> int:
    """
    حذف تمام کودهای سیستمی از دیتابیس
    (برای اجرای مجدد seed)
    
    Returns:
        تعداد کودهای حذف شده
    """
    count = db.query(Fertilizer).filter(
        Fertilizer.is_system_default == True
    ).delete()
    db.commit()
    logger.info(f"🗑️  {count} کود سیستمی حذف شد")
    return count