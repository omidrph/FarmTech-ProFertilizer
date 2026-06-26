# backend/app/seeds/fertilizer_seeds.py
"""
Seed داده‌های اولیه کودهای سیستمی
این فایل شامل کودهای استاندارد و پرکاربرد در کشاورزی و گلخانه‌داری است.

منبع: جداول استاندارد کودهای شیمیایی و نرخنامه سال ۱۴۰۵ وزارت جهاد کشاورزی
آخرین به‌روزرسانی: تیرماه ۱۴۰۵

تعداد کودها: ۴۲+ کود پرکاربرد
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Fertilizer

logger = logging.getLogger(__name__)


# ============================================================
# 🆕 لیست کامل کودهای سیستمی (فقط برای کپی کردن)
# ============================================================
SYSTEM_FERTILIZERS: List[Dict[str, Any]] = [
    
    # ============================================================
    # 🟢 کودهای نیتروژنه (Nitrogen Fertilizers)
    # ============================================================
    {
        "name": "نیترات آمونیوم (NH4NO3)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 500000,
        "elements": {"N-NO3": 17.499, "N-NH4": 17.499},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "کود نیتروژنی با دو فرم نیترات و آمونیوم - جذب سریع و پایدار - مناسب برای مراحل رشد رویشی"
    },
    {
        "name": "سولفات آمونیوم ((NH4)2SO4)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 450000,
        "elements": {"N-NH4": 21.200, "S": 24.266},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "تامین نیتروژن آمونیومی و گوگرد - کاهش pH خاک - مناسب برای خاک‌های آهکی"
    },
    {
        "name": "کلرید آمونیوم (NH4Cl)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 350000,
        "elements": {"N-NH4": 26.185, "Cl": 66.275},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "تامین نیتروژن آمونیومی و کلر - مناسب برنج و محصولات خاص - دارای خاصیت اسیدی"
    },
    {
        "name": "نیترات سدیم (NaNO3)",
        "brand": "استاندارد",
        "category": "نیتروژنه",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 350000,
        "elements": {"N-NO3": 16.480, "Na": 27.048},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "تامین نیتروژن نیتراتی و سدیم - مناسب خاک‌های اسیدی - جذب سریع"
    },
    {
        "name": "نیترات کلسیم (Ca(NO3)2.4H2O)",
        "brand": "استاندارد",
        "category": "کلسیمی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 550000,
        "elements": {"N-NO3": 11.861, "Ca": 16.963},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "تامین کلسیم و نیتروژن نیتراتی - افزایش استحکام گیاه و دیواره سلولی"
    },

    # ============================================================
    # 🟣 کودهای فسفاته (Phosphate Fertilizers)
    # ============================================================
    {
        "name": "مونو آمونیوم فسفات (NH4H2PO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"N-NH4": 12.178, "P": 26.930},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "تامین فسفر و نیتروژن - مناسب شروع رشد و ریشه‌زایی - دارای خاصیت اسیدی"
    },
    {
        "name": "دی آمونیوم فسفات ((NH4)2HPO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 800000,
        "elements": {"N-NH4": 21.216, "P": 23.478},
        "is_acid": False,
        "ph_level": 8.0,
        "description": "تامین فسفر و نیتروژن - افزایش عملکرد و کیفیت محصول - دارای خاصیت قلیایی"
    },
    {
        "name": "سوپر فسفات تریپل (TSP)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 92.0,
        "price_per_kg": 1432169,
        "elements": {"P": 20.000, "Ca": 15.000},
        "is_acid": False,
        "ph_level": 3.0,
        "description": "کود فسفاته با درصد بالای فسفر - تقویت ریشه و گلدهی - دارای خاصیت اسیدی قوی"
    },
    {
        "name": "فسفات ساده (SSP)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 85.0,
        "price_per_kg": 673944,
        "elements": {"P": 8.000, "Ca": 19.000, "S": 11.000},
        "is_acid": False,
        "ph_level": 3.5,
        "description": "کود فسفاته ساده - تامین فسفر و گوگرد مورد نیاز گیاه - اقتصادی"
    },
    {
        "name": "فسفات کلسیم مونوبازیک (Ca(H2PO4)2.H2O)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 95.0,
        "price_per_kg": 650000,
        "elements": {"Ca": 17.072, "P": 26.387},
        "is_acid": False,
        "ph_level": 3.0,
        "description": "تامین فسفر و کلسیم - مناسب خاک‌های اسیدی - دارای خاصیت اسیدی"
    },

    # ============================================================
    # 🔴 کودهای پتاسیمی (Potassium Fertilizers)
    # ============================================================
    {
        "name": "نیترات پتاسیم (KNO3)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"N-NO3": 13.854, "K": 38.667},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "تامین پتاسیم و نیتروژن - مناسب گلدهی و میوه‌دهی - بدون کلر"
    },
    {
        "name": "سولفات پتاسیم (K2SO4)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 1369999,
        "elements": {"K": 44.874, "S": 18.399},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "تامین پتاسیم و گوگرد - فاقد کلر - مناسب خاک‌های شور - کیفیت بالا"
    },
    {
        "name": "کلرید پتاسیم (KCl)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 933620,
        "elements": {"K": 52.446, "Cl": 47.554},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "تامین پتاسیم و کلر - اقتصادی‌ترین منبع پتاسیم - دارای کلر"
    },
    {
        "name": "مونو پتاسیم فسفات (KH2PO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 680000,
        "elements": {"P": 22.765, "K": 28.728},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "تامین فسفر و پتاسیم - تحریک گلدهی و میوه‌دهی - دارای خاصیت اسیدی"
    },
    {
        "name": "دی پتاسیم فسفات (K2HPO4)",
        "brand": "استاندارد",
        "category": "فسفاته",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 700000,
        "elements": {"P": 17.768, "K": 44.830},
        "is_acid": False,
        "ph_level": 9.0,
        "description": "تامین فسفر و پتاسیم - مناسب محلول‌های غذایی با pH متعادل - خاصیت قلیایی"
    },
    {
        "name": "کربنات پتاسیم (K2CO3)",
        "brand": "استاندارد",
        "category": "پتاسیمی",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 800000,
        "elements": {"K": 56.579},
        "is_acid": False,
        "ph_level": 11.5,
        "description": "تامین پتاسیم - افزایش pH محلول - مناسب تنظیم pH - خاصیت قلیایی قوی"
    },

    # ============================================================
    # 🟤 کودهای منیزیم (Magnesium Fertilizers)
    # ============================================================
    {
        "name": "سولفات منیزیم (MgSO4.7H2O)",
        "brand": "استاندارد",
        "category": "منیزیمی",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 400000,
        "elements": {"Mg": 9.861, "S": 13.010},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "تامین منیزیم و گوگرد - افزایش کلروفیل و فتوسنتز - رفع زردی برگ‌ها"
    },
    {
        "name": "نیترات منیزیم (Mg(NO3)2.6H2O)",
        "brand": "استاندارد",
        "category": "منیزیمی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 480000,
        "elements": {"N-NO3": 10.922, "Mg": 9.464},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "تامین منیزیم و نیتروژن - افزایش فتوسنتز و سبزینگی - جذب سریع"
    },

    # ============================================================
    # 🟠 کودهای آهن (Iron Fertilizers - Chelated)
    # ============================================================
    {
        "name": "کلات آهن EDDHA (Fe-EDDHA 6%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 6.0,
        "price_per_kg": 3000000,
        "elements": {"Fe": 13.706},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات آهن با پایه EDDHA - پایداری تا pH 9 - مناسب خاک‌های آهکی - رفع کلروز شدید"
    },
    {
        "name": "کلات آهن DTPA (Fe-DTPA 7%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 7.0,
        "price_per_kg": 2500000,
        "elements": {"Fe": 10.955},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات آهن با پایه DTPA - پایداری تا pH 8.5 - مناسب خاک‌های نیمه آهکی"
    },
    {
        "name": "کلات آهن EDTA (Fe-EDTA 13%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 13.0,
        "price_per_kg": 1900000,
        "elements": {"Fe": 13.691},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات آهن با پایه EDTA - پایداری تا pH 8 - رفع کلروز آهن - جذب بالا"
    },
    {
        "name": "سولفات آهن (FeSO4.7H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 98.0,
        "price_per_kg": 500000,
        "elements": {"Fe": 20.086, "S": 11.528},
        "is_acid": False,
        "ph_level": 3.5,
        "description": "تامین آهن و گوگرد - کاهش pH خاک - مناسب کشت ارگانیک - اقتصادی"
    },

    # ============================================================
    # 🟡 کودهای روی (Zinc Fertilizers)
    # ============================================================
    {
        "name": "کلات روی EDTA (Zn-EDTA 15%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 15.0,
        "price_per_kg": 1900000,
        "elements": {"Zn": 14.422},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات روی با پایه EDTA - جذب بالا - رفع کمبود روی و کوچکی برگ"
    },
    {
        "name": "سولفات روی مونوهیدرات (ZnSO4.H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 600000,
        "elements": {"Zn": 36.436, "S": 17.878},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "تامین روی و گوگرد - رفع علائم کمبود روی - اقتصادی"
    },
    {
        "name": "نیترات روی (Zn(NO3)2.6H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 700000,
        "elements": {"Zn": 21.980, "N-NO3": 9.418},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "تامین روی و نیتروژن - مناسب محلول‌های غذایی - جذب سریع"
    },

    # ============================================================
    # 🟢 کودهای منگنز (Manganese Fertilizers)
    # ============================================================
    {
        "name": "کلات منگنز EDTA (Mn-EDTA 13%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 13.0,
        "price_per_kg": 1850000,
        "elements": {"Mn": 13.694},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات منگنز با پایه EDTA - رفع زردی بین رگبرگ - افزایش فتوسنتز"
    },

    # ============================================================
    # 🔴 کودهای مس (Copper Fertilizers)
    # ============================================================
    {
        "name": "کلات مس EDTA (Cu-EDTA 14%)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 14.0,
        "price_per_kg": 2000000,
        "elements": {"Cu": 14.087},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلات مس با پایه EDTA - افزایش مقاومت به بیماری‌ها - خاصیت ضدقارچی"
    },
    {
        "name": "سولفات مس (CuSO4.5H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 98.0,
        "price_per_kg": 650000,
        "elements": {"Cu": 25.455, "S": 12.846},
        "is_acid": False,
        "ph_level": 3.5,
        "description": "تامین مس و گوگرد - خاصیت ضدقارچی و باکتری‌کشی - رفع کمبود مس"
    },
    {
        "name": "نیترات مس (Cu(NO3)2.3H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"Cu": 26.228, "N-NO3": 11.565},
        "is_acid": False,
        "ph_level": 4.0,
        "description": "تامین مس و نیتروژن - مناسب محلول‌های غذایی - جذب سریع"
    },

    # ============================================================
    # 🟡 کودهای بور (Boron Fertilizers)
    # ============================================================
    {
        "name": "اسید بوریک (H3BO3)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.5,
        "price_per_kg": 1200000,
        "elements": {"B": 17.480},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "تامین بور - بهبود گرده‌افشانی و تشکیل میوه - افزایش کیفیت محصول"
    },
    {
        "name": "بوراکس (Na2B4O7.10H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 1100000,
        "elements": {"B": 11.352, "Na": 12.080},
        "is_acid": False,
        "ph_level": 9.0,
        "description": "تامین بور و سدیم - مناسب خاک‌های اسیدی - خاصیت قلیایی"
    },

    # ============================================================
    # 🟡 کودهای مولیبدن (Molybdenum Fertilizers)
    # ============================================================
    {
        "name": "مولیبدات سدیم (Na2MoO4.2H2O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 2800000,
        "elements": {"Mo": 39.650, "Na": 19.001},
        "is_acid": False,
        "ph_level": 8.0,
        "description": "تامین مولیبدن و سدیم - افزایش تثبیت نیتروژن - برای حبوبات ضروری"
    },

    # ============================================================
    # 🟣 کودهای NPK کامل
    # ============================================================
    {
        "name": "کود کامل 20-20-20",
        "brand": "استاندارد",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 950000,
        "elements": {"N-NO3": 10.000, "N-NH4": 10.000, "P": 8.733, "K": 16.600},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "کود کامل NPK با نسبت مساوی - مناسب رشد عمومی گیاه - متعادل"
    },
    {
        "name": "کود کامل 20-20-20 (مایع)",
        "brand": "استاندارد",
        "category": "NPK کامل",
        "form": "liquid",
        "concentration": 35.0,
        "price_per_kg": 1200000,
        "elements": {"N-NO3": 7.000, "N-NH4": 7.000, "P": 5.500, "K": 12.000},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "کود کامل NPK مایع با نسبت مساوی - جذب سریع - مناسب محلول‌پاشی"
    },
    {
        "name": "کود 12-12-36 (پتاسیم بالا)",
        "brand": "استاندارد",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 1100000,
        "elements": {"N-NO3": 6.000, "N-NH4": 6.000, "P": 5.240, "K": 29.880},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "کود NPK با پتاسیم بالا - مناسب گلدهی و میوه‌دهی - افزایش کیفیت میوه"
    },

    # ============================================================
    # 🟠 اسیدها (Acids)
    # ============================================================
    {
        "name": "اسید فسفریک 75% (H3PO4)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 75.0,
        "price_per_kg": 3450000,
        "elements": {"P": 23.684},
        "is_acid": True,
        "acid_type": "H3PO4",
        "ph_level": 1.5,
        "description": "اسید فسفریک 75% - برای تنظیم pH و تامین فسفر - مناسب سیستم‌های آبیاری"
    },
    {
        "name": "اسید نیتریک 63% (HNO3)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 63.0,
        "price_per_kg": 4800000,
        "elements": {"N-NO3": 13.997},
        "is_acid": True,
        "acid_type": "HNO3",
        "ph_level": 1.0,
        "description": "اسید نیتریک 63% - منبع نیتروژن نیتراتی و تنظیم‌کننده pH - قوی"
    },
    {
        "name": "اسید سولفوریک 98% (H2SO4)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 98.0,
        "price_per_kg": 1500000,
        "elements": {"S": 31.997},
        "is_acid": True,
        "acid_type": "H2SO4",
        "ph_level": 1.0,
        "description": "اسید سولفوریک 98% - تنظیم‌کننده pH و تامین گوگرد - بسیار قوی"
    }
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
        Dict با آمار عملیات
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
                Fertilizer.is_system_default == True,
                Fertilizer.user_id == None
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
                concentration=fert_data.get("concentration", 100.0),
                elements=fert_data.get("elements", {}),
                price_per_kg=fert_data.get("price_per_kg", 0.0),
                is_acid=fert_data.get("is_acid", False),
                acid_type=fert_data.get("acid_type"),
                ph_level=fert_data.get("ph_level"),
                description=fert_data.get("description"),
                is_system_default=True,
                source_system_id=None
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
        Fertilizer.is_system_default == True,
        Fertilizer.user_id == None
    ).count()


def clear_system_fertilizers(db: Session) -> int:
    """
    حذف تمام کودهای سیستمی از دیتابیس
    (برای اجرای مجدد seed)
    
    Returns:
        تعداد کودهای حذف شده
    """
    count = db.query(Fertilizer).filter(
        Fertilizer.is_system_default == True,
        Fertilizer.user_id == None
    ).delete()
    db.commit()
    logger.info(f"🗑️  {count} کود سیستمی حذف شد")
    return count