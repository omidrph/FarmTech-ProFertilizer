# backend/app/seeds/fertilizer_seeds.py
"""
Seed داده‌های اولیه کودهای سیستمی
این فایل کودهای پرکاربرد و مفید را از کاتالوگ شرکت‌های معتبر ایرانی استخراج کرده است.

شرکت‌های منبع:
- اطلس (ATLAS) - www.atlas-chem.ir
- رازاک شیمی (Razak Shimi)
- ردسا (REDSA) - www.redsa.ir
- گل سم گرگان

تبدیل‌های استفاده شده:
- P2O5 → P: × 0.4364
- K2O → K: × 0.8302
- CaO → Ca: × 0.7147
- MgO → Mg: × 0.6031
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Fertilizer

logger = logging.getLogger(__name__)


# ============================================================
# لیست کامل کودهای سیستمی
# ============================================================
SYSTEM_FERTILIZERS: List[Dict[str, Any]] = [
    # ============================================================
    # 🔴 اسیدهای پایه (برای تنظیم pH)
    # ============================================================
    {
        "name": "اسید فسفریک (H3PO4) 85%",
        "brand": "عمومی",
        "category": "اسید",
        "form": "liquid",
        "price_per_kg": 45000,
        "elements": {"P": 44.0},
        "is_acid": True,
        "acid_type": "H3PO4",
        "description": "اسید فسفریک 85% - برای تنظیم pH و تامین فسفر"
    },
    {
        "name": "اسید نیتریک (HNO3) 65%",
        "brand": "عمومی",
        "category": "اسید",
        "form": "liquid",
        "price_per_kg": 38000,
        "elements": {"N-NO3": 68.0},
        "is_acid": True,
        "acid_type": "HNO3",
        "description": "اسید نیتریک 65% - برای تنظیم pH و تامین نیتروژن"
    },
    {
        "name": "اسید سولفوریک (H2SO4) 98%",
        "brand": "عمومی",
        "category": "اسید",
        "form": "liquid",
        "price_per_kg": 25000,
        "elements": {"S": 33.0},
        "is_acid": True,
        "acid_type": "H2SO4",
        "description": "اسید سولفوریک 98% - برای تنظیم pH و تامین گوگرد"
    },

    # ============================================================
    # 🟢 کودهای NPK کامل (پرکاربردترین)
    # ============================================================
    {
        "name": "NPK 20-20-20 گرین استار",
        "brand": "رازاک شیمی",
        "category": "NPK کامل",
        "form": "powder",
        "price_per_kg": 85000,
        "elements": {
            "N-NO3": 13.0,
            "N-NH4": 7.0,
            "P": 8.73,
            "K": 16.60
        },
        "is_acid": False,
        "description": "کود کامل NPK با نسبت مساوی - مناسب برای رشد عمومی گیاه"
    },
    {
        "name": "NPK 20-20-20 فرتی گل",
        "brand": "گل سم گرگان",
        "category": "NPK کامل",
        "form": "powder",
        "price_per_kg": 88000,
        "elements": {
            "N-NO3": 13.0,
            "N-NH4": 7.0,
            "P": 8.73,
            "K": 16.60
        },
        "is_acid": False,
        "description": "کود کامل میکروکریستال با حلالیت 100% - حاوی ریزمغذی کلاته EDTA"
    },
    {
        "name": "NPK 12-12-36 گرین استار",
        "brand": "رازاک شیمی",
        "category": "NPK پتاسیم بالا",
        "form": "powder",
        "price_per_kg": 92000,
        "elements": {
            "N-NO3": 8.0,
            "N-NH4": 4.0,
            "P": 5.24,
            "K": 29.89
        },
        "is_acid": False,
        "description": "کود پتاسیم بالا - مناسب برای مرحله گلدهی و رسیدن میوه"
    },
    {
        "name": "NPK 10-52-10 زاگرا استار",
        "brand": "رازاک شیمی",
        "category": "NPK فسفر بالا",
        "form": "powder",
        "price_per_kg": 95000,
        "elements": {
            "N-NO3": 7.0,
            "N-NH4": 3.0,
            "P": 22.69,
            "K": 8.30
        },
        "is_acid": False,
        "description": "کود فسفر بالا - مناسب برای ریشه‌زایی و استقرار نشاء"
    },
    {
        "name": "NPK 15-5-30 زاگرا استار",
        "brand": "رازاک شیمی",
        "category": "NPK پتاسیم بالا",
        "form": "powder",
        "price_per_kg": 90000,
        "elements": {
            "N-NO3": 10.0,
            "N-NH4": 5.0,
            "P": 2.18,
            "K": 24.91
        },
        "is_acid": False,
        "description": "کود پتاسیم بالا - مناسب برای افزایش کیفیت و رنگ‌آوری میوه"
    },
    {
        "name": "NPK 30-10-10 زاگرا استار",
        "brand": "رازاک شیمی",
        "category": "NPK نیتروژن بالا",
        "form": "powder",
        "price_per_kg": 87000,
        "elements": {
            "N-NO3": 20.0,
            "N-NH4": 10.0,
            "P": 4.36,
            "K": 8.30
        },
        "is_acid": False,
        "description": "کود نیتروژن بالا - مناسب برای رشد رویشی و افزایش سبزینه"
    },
    {
        "name": "NPK 36-12-12 فرتی گل",
        "brand": "گل سم گرگان",
        "category": "NPK پتاسیم بالا",
        "form": "powder",
        "price_per_kg": 93000,
        "elements": {
            "N-NO3": 8.0,
            "N-NH4": 4.0,
            "P": 5.24,
            "K": 29.89
        },
        "is_acid": False,
        "description": "کود پتاسیم بسیار بالا - مناسب برای مرحله نهایی رسیدن میوه"
    },

    # ============================================================
    # 🟡 کودهای تک عنصری ماکرو
    # ============================================================
    {
        "name": "نیترات کلسیم",
        "brand": "رازاک شیمی",
        "category": "نیترات",
        "form": "crystal",
        "price_per_kg": 45000,
        "elements": {
            "N-NO3": 15.5,
            "Ca": 18.94
        },
        "is_acid": False,
        "description": "تامین نیتروژن نیتراتی و کلسیم - افزایش استحکام گیاه"
    },
    {
        "name": "نیترات پتاسیم",
        "brand": "عمومی",
        "category": "نیترات",
        "form": "crystal",
        "price_per_kg": 65000,
        "elements": {
            "N-NO3": 13.0,
            "K": 38.0
        },
        "is_acid": False,
        "description": "تامین نیتروژن و پتاسیم - مناسب برای گلدهی و میوه‌دهی"
    },
    {
        "name": "نیترات منیزیم",
        "brand": "کوالی مکس",
        "category": "نیترات",
        "form": "crystal",
        "price_per_kg": 42000,
        "elements": {
            "N-NO3": 10.5,
            "Mg": 9.36
        },
        "is_acid": False,
        "description": "تامین نیتروژن و منیزیم - افزایش فتوسنتز و سبزینه"
    },
    {
        "name": "نیترات آمونیوم",
        "brand": "عمومی",
        "category": "نیترات",
        "form": "crystal",
        "price_per_kg": 35000,
        "elements": {
            "N-NO3": 17.0,
            "N-NH4": 17.0
        },
        "is_acid": False,
        "description": "کود نیتروژنی با دو فرم نیترات و آمونیوم"
    },
    {
        "name": "مونو پتاسیم فسفات (MKP 0-52-34)",
        "brand": "کوالی مکس",
        "category": "فسفات",
        "form": "powder",
        "price_per_kg": 98000,
        "elements": {
            "P": 22.69,
            "K": 28.23
        },
        "is_acid": False,
        "description": "بدون نیتروژن - تحریک گل‌انگیزی و توسعه ریشه - مناسب هیدروپونیک"
    },
    {
        "name": "سولفات پتاسیم (سولوپتاس)",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "powder",
        "price_per_kg": 75000,
        "elements": {
            "K": 42.34,
            "S": 17.5
        },
        "is_acid": False,
        "description": "تامین پتاسیم و گوگرد - فاقد کلراید - مناسب خاک‌های شور"
    },

    # ============================================================
    # 🔵 سولفات‌های تک عنصری (ریزمغذی و ثانویه)
    # ============================================================
    {
        "name": "سولفات روی",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "powder",
        "price_per_kg": 55000,
        "elements": {
            "Zn": 22.0,
            "S": 11.0
        },
        "is_acid": False,
        "description": "تامین روی و گوگرد - رفع علائم کمبود روی"
    },
    {
        "name": "سولفات منگنز",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "powder",
        "price_per_kg": 52000,
        "elements": {
            "Mn": 32.0,
            "S": 12.8
        },
        "is_acid": False,
        "description": "تامین منگنز و گوگرد - رفع زردی بین رگبرگ"
    },
    {
        "name": "سولفات مس",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "powder",
        "price_per_kg": 60000,
        "elements": {
            "Cu": 25.0,
            "S": 12.5
        },
        "is_acid": False,
        "description": "تامین مس و گوگرد - خاصیت ضدقارچی"
    },
    {
        "name": "سولفات منیزیم",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "powder",
        "price_per_kg": 38000,
        "elements": {
            "Mg": 16.0,
            "S": 13.0
        },
        "is_acid": False,
        "description": "تامین منیزیم و گوگرد - افزایش فتوسنتز و ساخت کلروفیل"
    },
    {
        "name": "سولفات آهن",
        "brand": "رازاک شیمی",
        "category": "سولفات",
        "form": "crystal",
        "price_per_kg": 48000,
        "elements": {
            "Fe": 20.0,
            "S": 11.5
        },
        "is_acid": False,
        "description": "تامین آهن و گوگرد - مناسب خاک‌های قلیایی - کاهش pH خاک"
    },

    # ============================================================
    # 🟣 کلات‌های EDTA (جذب بالا)
    # ============================================================
    {
        "name": "کلات آهن EDTA (Fe-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 180000,
        "elements": {"Fe": 6.0},
        "is_acid": False,
        "description": "کلات آهن با پایه EDTA - پایداری تا pH 8 - رفع کلروز"
    },
    {
        "name": "کلات روی EDTA (Zn-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 175000,
        "elements": {"Zn": 15.0},
        "is_acid": False,
        "description": "کلات روی با پایه EDTA - جذب بالا - پایداری تا pH 10"
    },
    {
        "name": "کلات منگنز EDTA (Mn-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 175000,
        "elements": {"Mn": 13.0},
        "is_acid": False,
        "description": "کلات منگنز با پایه EDTA - رفع زردی بین رگبرگ"
    },
    {
        "name": "کلات مس EDTA (Cu-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 185000,
        "elements": {"Cu": 15.0},
        "is_acid": False,
        "description": "کلات مس با پایه EDTA - افزایش مقاومت به بیماری‌ها"
    },
    {
        "name": "کلات کلسیم EDTA (Ca-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 170000,
        "elements": {"Ca": 10.0},
        "is_acid": False,
        "description": "کلات کلسیم با پایه EDTA - جلوگیری از پوسیدگی گلگاه گوجه"
    },
    {
        "name": "کلات منیزیم EDTA (Mg-EDTA)",
        "brand": "اطلس",
        "category": "کلات EDTA",
        "form": "powder",
        "price_per_kg": 165000,
        "elements": {"Mg": 6.0},
        "is_acid": False,
        "description": "کلات منیزیم با پایه EDTA - افزایش فتوسنتز"
    },

    # ============================================================
    # 🟤 کلات‌های آمینو اسیدی (گلایسینات - جذب سریع)
    # ============================================================
    {
        "name": "کلات آهن گلایسینات (Fe-Glycinate)",
        "brand": "اطلس",
        "category": "کلات آمینو اسیدی",
        "form": "powder",
        "price_per_kg": 220000,
        "elements": {"Fe": 13.0},
        "is_acid": False,
        "description": "کلات آهن آلی با گلایسین - جذب سریع از ریشه و برگ - پایداری در خاک‌های قلیایی"
    },
    {
        "name": "کلات روی گلایسینات (Zn-Glycinate)",
        "brand": "اطلس",
        "category": "کلات آمینو اسیدی",
        "form": "powder",
        "price_per_kg": 210000,
        "elements": {"Zn": 15.0},
        "is_acid": False,
        "description": "کلات روی آلی - رفع سریع کمبود روی - بهبود رشد رویشی"
    },
    {
        "name": "کلات منگنز گلایسینات (Mn-Glycinate)",
        "brand": "اطلس",
        "category": "کلات آمینو اسیدی",
        "form": "powder",
        "price_per_kg": 210000,
        "elements": {"Mn": 15.0},
        "is_acid": False,
        "description": "کلات منگنز آلی - رفع سریع زردی بین رگبرگ - فاقد سدیم"
    },

    # ============================================================
    # ⚫ کلات آهن EDDHA (مناسب خاک‌های بسیار قلیایی)
    # ============================================================
    {
        "name": "کلات آهن EDDHA (Fe-EDDHA)",
        "brand": "اطلس",
        "category": "کلات EDDHA",
        "form": "powder",
        "price_per_kg": 280000,
        "elements": {"Fe": 6.0},
        "is_acid": False,
        "description": "کلات آهن با پایه EDDHA - پایداری تا pH 9 - مناسب خاک‌های آهکی و بسیار قلیایی"
    },

    # ============================================================
    # 🟠 کودهای ریزمغذی کامل (کمپلکس)
    # ============================================================
    {
        "name": "یونی کمپلکس پودری",
        "brand": "گل سم گرگان",
        "category": "ریزمغذی کامل",
        "form": "powder",
        "price_per_kg": 195000,
        "elements": {
            "Fe": 5.0,
            "Zn": 5.0,
            "Mn": 4.0,
            "Cu": 4.0,
            "B": 1.5,
            "Mo": 0.07,
            "Mg": 1.2,
            "S": 25.0
        },
        "is_acid": False,
        "description": "کود کامل ریزمغذی چندعنصری - کاملاً محلول در آب"
    },
    {
        "name": "تراست کمبی (Trust Combi)",
        "brand": "ردسا",
        "category": "ریزمغذی کامل",
        "form": "powder",
        "price_per_kg": 205000,
        "elements": {
            "N": 3.0,
            "Mg": 1.0,
            "Fe": 4.0,
            "Zn": 3.0,
            "Mn": 2.0,
            "Cu": 0.5,
            "B": 0.5,
            "Mo": 0.05
        },
        "is_acid": False,
        "description": "کلات کامل ریزمغذی با پایه EDTA - حاوی اسید آمینه - مناسب هیدروپونیک"
    },
    {
        "name": "مولتی کلات 8 (Multi Chelate 8)",
        "brand": "اطلس",
        "category": "ریزمغذی کامل",
        "form": "powder",
        "price_per_kg": 190000,
        "elements": {
            "Fe": 4.0,
            "Zn": 2.5,
            "Mn": 2.5,
            "Cu": 0.6,
            "B": 0.4,
            "Mo": 0.2,
            "Ca": 1.2,
            "Mg": 0.6
        },
        "is_acid": False,
        "description": "کلات کامل 8 عنصر ریزمغذی با پایه EDTA - جذب بالا در خاک‌های قلیایی"
    },

    # ============================================================
    # 🔶 کودهای ویژه (کلسیم-بور، پتاسیم مایع، هیومیک اسید)
    # ============================================================
    {
        "name": "کلسیم بور (Trust Calbor)",
        "brand": "ردسا",
        "category": "کلسیم-بور",
        "form": "liquid",
        "price_per_kg": 185000,
        "elements": {
            "Ca": 11.44,
            "B": 1.0
        },
        "is_acid": False,
        "description": "کلات کلسیم و بور - افزایش ماندگاری محصول - جلوگیری از پوسیدگی گلگاه"
    },
    {
        "name": "تراست پتاسیم 52 (Trust K 52)",
        "brand": "ردسا",
        "category": "پتاسیم مایع",
        "form": "liquid",
        "price_per_kg": 125000,
        "elements": {
            "N": 3.0,
            "K": 40.0
        },
        "is_acid": False,
        "description": "کود پتاسیم مایع با ازت و اسید آمینه - افزایش مقاومت به تنش‌ها"
    },
    {
        "name": "هیومیک اسید 95% پودری",
        "brand": "رازاک شیمی",
        "category": "محرک رشد",
        "form": "powder",
        "price_per_kg": 145000,
        "elements": {},
        "is_acid": False,
        "description": "کلات کننده طبیعی - اصلاح خاک‌های قلیایی - افزایش جذب عناصر"
    },
    {
        "name": "فولویک اسید",
        "brand": "رازاک شیمی",
        "category": "محرک رشد",
        "form": "powder",
        "price_per_kg": 165000,
        "elements": {},
        "is_acid": False,
        "description": "اسید فولویک خالص - جذب سریع از طریق برگ و ریشه"
    },
    {
        "name": "تراست بور (Trust Boron)",
        "brand": "ردسا",
        "category": "ریزمغذی",
        "form": "liquid",
        "price_per_kg": 155000,
        "elements": {"B": 11.0},
        "is_acid": False,
        "description": "بور کمپلکس شده - بهبود گرده‌افشانی - افزایش قند میوه"
    },
    {
        "name": "تراست نیتروزینک (Trust Nitrozinc)",
        "brand": "ردسا",
        "category": "روی-نیتروژن",
        "form": "liquid",
        "price_per_kg": 140000,
        "elements": {
            "N": 2.0,
            "Zn": 8.0
        },
        "is_acid": False,
        "description": "کود روی و نیتروژن با اسید آمینه - جلوگیری از ریزش گل و میوه"
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
                npk_ratio=None,
                organic_matter=None,
                chelating_agent=None
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