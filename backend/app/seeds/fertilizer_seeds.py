# backend/app/seeds/fertilizer_seeds.py
"""
Seed داده‌های اولیه کودهای سیستمی
این فایل شامل کودهای استاندارد و پرکاربرد در کشاورزی و گلخانه‌داری است.

منبع: جداول استاندارد کودهای شیمیایی و نرخنامه سال ۱۴۰۵ وزارت جهاد کشاورزی
آخرین به‌روزرسانی: تیرماه ۱۴۰۵

تعداد کودها: ۴۵ کود (۳۹ استاندارد + ۶ کود شرکتی GRANJA)
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Fertilizer

logger = logging.getLogger(__name__)


# ============================================================
# 🆕 لیست کامل کودهای سیستمی (مرتب‌سازی شده بر اساس حروف الفبای انگلیسی)
# ============================================================
SYSTEM_FERTILIZERS: List[Dict[str, Any]] = [
    
    # ============================================================
    # 🔵 کودهای با حرف A
    # ============================================================
    {
        "name": "Ammonium Chloride (NH₄Cl)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 350000,
        "elements": {"N-NH4": 26.187, "Cl": 66.282},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "کلرید آمونیوم (Ammonium Chloride) - تامین نیتروژن آمونیومی و کلر - مناسب برنج و محصولات خاص - دارای خاصیت اسیدی"
    },
    {
        "name": "Ammonium Dibasic Phosphate ((NH₄)₂HPO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 800000,
        "elements": {"N-NH4": 21.213, "P": 23.481},
        "is_acid": False,
        "ph_level": 8.0,
        "description": "دی‌فسفات آمونیوم (Ammonium Dibasic Phosphate) - تامین فسفر و نیتروژن - افزایش عملکرد و کیفیت محصول - دارای خاصیت قلیایی"
    },
    {
        "name": "Ammonium Monobasic Phosphate (NH₄H₂PO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"N-NH4": 12.177, "P": 26.928},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "مونوفسفات آمونیوم (Ammonium Monobasic Phosphate) - تامین فسفر و نیتروژن - مناسب شروع رشد و ریشه‌زایی - دارای خاصیت اسیدی"
    },
    {
        "name": "Ammonium Nitrate (NH₄NO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 500000,
        "elements": {"N-NO3": 17.499, "N-NH4": 17.499},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "نیترات آمونیوم (Ammonium Nitrate) - کود نیتروژنی با دو فرم نیترات و آمونیوم - جذب سریع و پایدار - مناسب برای مراحل رشد رویشی"
    },
    {
        "name": "Ammonium Sulfate ((NH₄)₂SO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 450000,
        "elements": {"N-NH4": 21.201, "S": 24.264},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "سولفات آمونیوم (Ammonium Sulfate) - تامین نیتروژن آمونیومی و گوگرد - کاهش pH خاک - مناسب برای خاک‌های آهکی"
    },

    # ============================================================
    # 🔵 کودهای با حرف B
    # ============================================================
    {
        "name": "Boric Acid (H₃BO₃)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.5,
        "price_per_kg": 1200000,
        "elements": {"B": 17.483},
        "is_acid": False,
        "ph_level": 5.0,
        "description": "اسید بوریک (Boric Acid) - تامین بور - بهبود گرده‌افشانی و تشکیل میوه - افزایش کیفیت محصول"
    },

    # ============================================================
    # 🔵 کودهای با حرف C
    # ============================================================
    {
        "name": "Calcium Carbonate (CaCO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 200000,
        "elements": {"Ca": 40.043},
        "is_acid": False,
        "ph_level": 9.0,
        "description": "کربنات کلسیم (Calcium Carbonate) - تامین کلسیم - افزایش pH خاک - مناسب خاک‌های اسیدی"
    },
    {
        "name": "Calcium Monobasic Phosphate (Ca(H₂PO₄)₂·H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 95.0,
        "price_per_kg": 650000,
        "elements": {"P": 24.579, "Ca": 17.088},
        "is_acid": False,
        "ph_level": 3.0,
        "description": "مونوفسفات کلسیم (Calcium Monobasic Phosphate) - تامین فسفر و کلسیم - مناسب خاک‌های اسیدی - دارای خاصیت اسیدی"
    },
    {
        "name": "Calcium Nitrate (Ca(NO₃)₂·4H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 550000,
        "elements": {"N-NO3": 11.861, "Ca": 16.963},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "نیترات کلسیم (Calcium Nitrate) - تامین کلسیم و نیتروژن نیتراتی - افزایش استحکام گیاه و دیواره سلولی"
    },
    {
        "name": "Calcium Sulfate (CaSO₄·2H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 95.0,
        "price_per_kg": 350000,
        "elements": {"Ca": 23.283, "S": 18.624},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "سولفات کلسیم (Calcium Sulfate) - تامین کلسیم و گوگرد - بهبود ساختار خاک - مناسب خاک‌های شور"
    },
    {
        "name": "Copper EDTA (CuEDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 14.5,
        "price_per_kg": 2000000,
        "elements": {"Cu": 14.500},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "مس EDTA (Copper EDTA) - کلات مس با پایه EDTA - افزایش مقاومت به بیماری‌ها - خاصیت ضدقارچی"
    },
    {
        "name": "Copper Nitrate (Cu(NO₃)₂·3H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"N-NO3": 11.381, "Cu": 26.030},
        "is_acid": False,
        "ph_level": 4.0,
        "description": "نیترات مس (Copper Nitrate) - تامین مس و نیتروژن - مناسب محلول‌های غذایی - جذب سریع"
    },
    {
        "name": "Copper Sulfate (CuSO₄·5H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 98.0,
        "price_per_kg": 650000,
        "elements": {"Cu": 25.450, "S": 12.841},
        "is_acid": False,
        "ph_level": 3.5,
        "description": "سولفات مس (Copper Sulfate) - تامین مس و گوگرد - خاصیت ضدقارچی و باکتری‌کشی - رفع کمبود مس"
    },

    # ============================================================
    # 🔵 کودهای با حرف F (Fertilizer 20-20-20)
    # ============================================================
    {
        "name": "Fertilizer 20-20-20 (NPK)",
        "brand": "استاندارد",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 950000,
        "elements": {"N-NO3": 20.000, "P": 8.728, "K": 16.602},
        "is_acid": False,
        "ph_level": 6.5,
        "description": "کود کامل ۲۰-۲۰-۲۰ (Fertilizer 20-20-20) - نسبت مساوی NPK - مناسب رشد عمومی گیاه - متعادل - حاوی ۲۰% نیتروژن نیتراتی"
    },

    # ============================================================
    # 🔵 کودهای با حرف I
    # ============================================================
    {
        "name": "Iron DTPA (FeDTPA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 10.0,
        "price_per_kg": 2500000,
        "elements": {"Fe": 10.000},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "آهن DTPA (Iron DTPA) - کلات آهن با پایه DTPA - پایداری تا pH 8.5 - مناسب خاک‌های نیمه آهکی"
    },
    {
        "name": "Iron EDDHA (FeEDDHA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 6.0,
        "price_per_kg": 3000000,
        "elements": {"Fe": 6.000},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "آهن EDDHA (Iron EDDHA) - کلات آهن با پایه EDDHA - پایداری تا pH 9 - مناسب خاک‌های آهکی - رفع کلروز شدید"
    },
    {
        "name": "Iron EDTA (FeEDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 9.0,
        "price_per_kg": 1900000,
        "elements": {"Fe": 9.000},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "آهن EDTA (Iron EDTA) - کلات آهن با پایه EDTA - پایداری تا pH 8 - رفع کلروز آهن - جذب بالا"
    },
    {
        "name": "Iron II Sulfate (FeSO₄·7H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 98.0,
        "price_per_kg": 500000,
        "elements": {"Fe": 20.088, "S": 11.532},
        "is_acid": False,
        "ph_level": 3.5,
        "description": "سولفات آهن (Iron II Sulfate) - تامین آهن و گوگرد - کاهش pH خاک - مناسب کشت ارگانیک - اقتصادی"
    },

    # ============================================================
    # 🔵 کودهای با حرف M
    # ============================================================
    {
        "name": "Magnesium Carbonate (MgCO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 350000,
        "elements": {"Mg": 28.827},
        "is_acid": False,
        "ph_level": 9.5,
        "description": "کربنات منیزیم (Magnesium Carbonate) - تامین منیزیم - افزایش pH خاک - مناسب خاک‌های اسیدی"
    },
    {
        "name": "Magnesium Nitrate (Mg(NO₃)₂·6H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 480000,
        "elements": {"N-NO3": 10.925, "Mg": 9.479},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "نیترات منیزیم (Magnesium Nitrate) - تامین منیزیم و نیتروژن - افزایش فتوسنتز و سبزینگی - جذب سریع"
    },
    {
        "name": "Magnesium Sulfate (MgSO₄·7H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 400000,
        "elements": {"Mg": 9.861, "S": 13.008},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "سولفات منیزیم (Magnesium Sulfate) - تامین منیزیم و گوگرد - افزایش کلروفیل و فتوسنتز - رفع زردی برگ‌ها"
    },
    {
        "name": "Mn EDTA (MnEDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 12.0,
        "price_per_kg": 1850000,
        "elements": {"Mn": 12.000},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "منگنز EDTA (Mn EDTA) - کلات منگنز با پایه EDTA - رفع زردی بین رگبرگ - افزایش فتوسنتز"
    },

    # ============================================================
    # 🔵 کودهای با حرف N (Nitric Acid)
    # ============================================================
    {
        "name": "Nitric Acid 63% (HNO₃)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 63.0,
        "price_per_kg": 4800000,
        "elements": {"N-NO3": 22.229},
        "is_acid": True,
        "acid_type": "HNO3",
        "density_g_ml": 1.383,
        "ph_level": 1.0,
        "description": "اسید نیتریک ۶۳٪ (Nitric Acid 63%) - منبع نیتروژن نیتراتی و تنظیم‌کننده pH - بسیار قوی"
    },

    # ============================================================
    # 🔵 کودهای با حرف P
    # ============================================================
    {
        "name": "Phosphoric Acid 75% (H₃PO₄)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 75.0,
        "price_per_kg": 3450000,
        "elements": {"P": 31.608},
        "is_acid": True,
        "acid_type": "H3PO4",
        "density_g_ml": 1.579,
        "ph_level": 1.5,
        "description": "اسید فسفریک ۷۵٪ (Phosphoric Acid 75%) - تنظیم pH و تامین فسفر - مناسب سیستم‌های آبیاری"
    },
    {
        "name": "Potassium Carbonate (K₂CO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 800000,
        "elements": {"K": 56.589},
        "is_acid": False,
        "is_base": True,
        "acid_type": "K2CO3",
        "ph_level": 11.5,
        "description": "کربنات پتاسیم (Potassium Carbonate) - تامین پتاسیم - افزایش pH محلول - مناسب تنظیم pH - خاصیت قلیایی قوی"
    },
    {
        "name": "Potassium Hydroxide 90% (KOH)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 90.0,
        "price_per_kg": 0.0,
        "elements": {"K": 69.682},
        "is_acid": False,
        "is_base": True,
        "acid_type": "KOH",
        "ph_level": 13.5,
        "description": "پتاسیم هیدروکسید ۹۰٪ (KOH) - باز تنظیم‌کنندهٔ pH و منبع پتاسیم - بسیار خورنده؛ با دستکش و عینک و همیشه در آب حل شود"
    },
    {
        "name": "Potassium Chloride (KCl)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.5,
        "price_per_kg": 933620,
        "elements": {"K": 52.445, "Cl": 47.555},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "کلرید پتاسیم (Potassium Chloride) - تامین پتاسیم و کلر - اقتصادی‌ترین منبع پتاسیم - دارای کلر"
    },
    {
        "name": "Potassium Citrate (K₃C₆H₅O₇·H₂O)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 900000,
        "elements": {"K": 36.155},
        "is_acid": False,
        "ph_level": 8.0,
        "description": "سیترات پتاسیم (Potassium Citrate) - تامین پتاسیم - منبع آلی پتاسیم - مناسب سیستم‌های آبیاری"
    },
    {
        "name": "Potassium Dibasic Phosphate (K₂HPO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 700000,
        "elements": {"P": 17.783, "K": 44.895},
        "is_acid": False,
        "ph_level": 9.0,
        "description": "دی‌فسفات پتاسیم (Potassium Dibasic Phosphate) - تامین فسفر و پتاسیم - مناسب محلول‌های غذایی با pH متعادل - خاصیت قلیایی"
    },
    {
        "name": "Potassium Monobasic Phosphate (KH₂PO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 680000,
        "elements": {"P": 22.762, "K": 28.731},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "مونوفسفات پتاسیم (Potassium Monobasic Phosphate) - تامین فسفر و پتاسیم - تحریک گلدهی و میوه‌دهی - دارای خاصیت اسیدی"
    },
    {
        "name": "Potassium Nitrate (KNO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 750000,
        "elements": {"N-NO3": 13.854, "K": 38.672},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "نیترات پتاسیم (Potassium Nitrate) - تامین پتاسیم و نیتروژن - مناسب گلدهی و میوه‌دهی - بدون کلر"
    },
    {
        "name": "Potassium Sulfate (K₂SO₄)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 1369999,
        "elements": {"K": 44.874, "S": 18.401},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "سولفات پتاسیم (Potassium Sulfate) - تامین پتاسیم و گوگرد - فاقد کلر - مناسب خاک‌های شور - کیفیت بالا"
    },

    # ============================================================
    # 🔵 کودهای با حرف S
    # ============================================================
    {
        "name": "Sodium Borate (Na₂B₄O₇·10H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 1100000,
        "elements": {"B": 11.338, "Na": 12.057},
        "is_acid": False,
        "ph_level": 9.0,
        "description": "بوراکس (Sodium Borate) - تامین بور و سدیم - مناسب خاک‌های اسیدی - خاصیت قلیایی"
    },
    {
        "name": "Sodium Molybdate (Na₂MoO₄·2H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 99.0,
        "price_per_kg": 2800000,
        "elements": {"Mo": 39.656, "Na": 19.003},
        "is_acid": False,
        "ph_level": 8.0,
        "description": "مولیبدات سدیم (Sodium Molybdate) - تامین مولیبدن و سدیم - افزایش تثبیت نیتروژن - برای حبوبات ضروری"
    },
    {
        "name": "Sodium Nitrate (NaNO₃)",
        "brand": "استاندارد",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 350000,
        "elements": {"N-NO3": 16.479, "Na": 27.052},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "نیترات سدیم (Sodium Nitrate) - تامین نیتروژن نیتراتی و سدیم - مناسب خاک‌های اسیدی - جذب سریع"
    },
    {
        "name": "Sulfuric Acid 98% (H₂SO₄)",
        "brand": "استاندارد",
        "category": "اسید",
        "form": "liquid",
        "concentration": 98.0,
        "price_per_kg": 1500000,
        "elements": {"S": 32.692},
        "is_acid": True,
        "acid_type": "H2SO4",
        "density_g_ml": 1.84,
        "ph_level": 1.0,
        "description": "اسید سولفوریک ۹۸٪ (Sulfuric Acid 98%) - تنظیم‌کننده pH و تامین گوگرد - بسیار قوی"
    },

    # ============================================================
    # 🔵 کودهای با حرف Z
    # ============================================================
    {
        "name": "Zinc EDTA (ZnEDTA)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 14.0,
        "price_per_kg": 1900000,
        "elements": {"Zn": 14.000},
        "is_acid": False,
        "ph_level": 7.0,
        "description": "روی EDTA (Zinc EDTA) - کلات روی با پایه EDTA - جذب بالا - رفع کمبود روی و کوچکی برگ"
    },
    {
        "name": "Zinc Nitrate (Zn(NO₃)₂·6H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "crystal",
        "concentration": 99.0,
        "price_per_kg": 700000,
        "elements": {"N-NO3": 9.150, "Zn": 21.978},
        "is_acid": False,
        "ph_level": 5.5,
        "description": "نیترات روی (Zinc Nitrate) - تامین روی و نیتروژن - مناسب محلول‌های غذایی - جذب سریع"
    },
    {
        "name": "Zinc Sulfate (ZnSO₄·7H₂O)",
        "brand": "استاندارد",
        "category": "ریزمغذی",
        "form": "powder",
        "concentration": 98.0,
        "price_per_kg": 600000,
        "elements": {"Zn": 22.744, "S": 11.153},
        "is_acid": False,
        "ph_level": 4.5,
        "description": "سولفات روی (Zinc Sulfate) - تامین روی و گوگرد - رفع علائم کمبود روی - اقتصادی"
    },

    # ============================================================
    # 🏭 کودهای شرکتی — GRANJA (گرانجا)
    # منبع: برگه‌های آزمایش شمارهٔ ۳۶۰ تا ۳۶۵ (مقادیر به‌صورت «محصول به‌همان‌صورت» اندازه‌گیری شده‌اند؛
    # بنابراین خلوص ۱۰۰٪ ثبت شده تا در درصد عناصر دوباره ضرب نشود).
    # P، K، Ca، Mg و S از اکسیدهای برگه به عنصر تبدیل شده‌اند.
    # ⚠️ تخمینی (باید با شرکت تأیید شود): تقسیم نیتروژن به نیترات/آمونیوم در NPKها، قیمت‌ها و نوع فیزیکی.
    # ============================================================
    {
        "name": "GRANJA NPK 10-52-10+TE",
        "brand": "GRANJA",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 100.0,
        "price_per_kg": 1150000,
        "elements": {"N-NO3": 1.4, "N-NH4": 8.8, "P": 22.607, "K": 8.218, "Fe": 0.05, "Mn": 0.03, "Zn": 0.01, "Cu": 0.02, "B": 0.02, "Mo": 0.001, "Na": 0.04, "Cl": 0.1},
        "is_acid": False,
        "description": "کود کامل 10-52-10 همراه با عناصر کم‌مصرف (TE) شرکت GRANJA - آزمایشگاه 360 - حلالیت 300 g/L در ۲۰°C - N کل 10.2٪ ، P₂O₅ 51.8٪ ، K₂O 9.9٪ (به عنصر تبدیل شده) - فرم نیتروژن (نیترات/آمونیوم) تخمینی از مواد اولیهٔ متداول و قیمت تخمینی؛ نیاز به تأیید شرکت - میکروها کلاته (نوع کلات نامشخص) - فلزات سنگین: Pb 15.0، Cd 0.8، Co 2.6، Ni 3.6 ppb، As 5.0 ppm"
    },
    {
        "name": "GRANJA NPK 12-12-36+TE",
        "brand": "GRANJA",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 100.0,
        "price_per_kg": 1100000,
        "elements": {"N-NO3": 10.1, "N-NH4": 1.7, "P": 5.412, "K": 30.051, "Fe": 0.05, "Mn": 0.03, "Zn": 0.01, "Cu": 0.02, "B": 0.02, "Mo": 0.001, "Na": 0.1, "Cl": 0.2},
        "is_acid": False,
        "description": "کود کامل 12-12-36 همراه با عناصر کم‌مصرف (TE) شرکت GRANJA - آزمایشگاه 361 - حلالیت 305 g/L در ۲۰°C - N کل 11.8٪ ، P₂O₅ 12.4٪ ، K₂O 36.2٪ (به عنصر تبدیل شده) - فرم نیتروژن (نیترات/آمونیوم) تخمینی از مواد اولیهٔ متداول و قیمت تخمینی؛ نیاز به تأیید شرکت - میکروها کلاته (نوع کلات نامشخص) - فلزات سنگین: Pb 14.9، Cd 0.7، Co 5.2، Ni 4.2 ppb، As <0.05 ppm"
    },
    {
        "name": "GRANJA NPK 15-5-30+TE",
        "brand": "GRANJA",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 100.0,
        "price_per_kg": 1050000,
        "elements": {"N-NO3": 12.6, "N-NH4": 4.2, "P": 2.837, "K": 27.229, "Fe": 0.06, "Mn": 0.03, "Zn": 0.01, "Cu": 0.03, "B": 0.02, "Mo": 0.001, "Na": 0.1, "Cl": 0.3},
        "is_acid": False,
        "description": "کود کامل 15-5-30 همراه با عناصر کم‌مصرف (TE) شرکت GRANJA - آزمایشگاه 362 - حلالیت 295 g/L در ۲۰°C - N کل 16.8٪ ، P₂O₅ 6.5٪ ، K₂O 32.8٪ (به عنصر تبدیل شده) - فرم نیتروژن (نیترات/آمونیوم) تخمینی از مواد اولیهٔ متداول و قیمت تخمینی؛ نیاز به تأیید شرکت - میکروها کلاته (نوع کلات نامشخص) - فلزات سنگین: Pb 14.6، Cd 0.6، Co 4.7، Ni 3.7 ppb، As <0.05 ppm"
    },
    {
        "name": "GRANJA NPK 20-20-20+TE",
        "brand": "GRANJA",
        "category": "NPK کامل",
        "form": "powder",
        "concentration": 100.0,
        "price_per_kg": 1000000,
        "elements": {"N-NO3": 10.7, "N-NH4": 8.6, "P": 8.772, "K": 17.018, "Fe": 0.05, "Mn": 0.03, "Zn": 0.01, "Cu": 0.02, "B": 0.02, "Mo": 0.001, "Na": 0.08, "Cl": 0.3},
        "is_acid": False,
        "description": "کود کامل 20-20-20 همراه با عناصر کم‌مصرف (TE) شرکت GRANJA - آزمایشگاه 363 - حلالیت 300 g/L در ۲۰°C - N کل 19.3٪ ، P₂O₅ 20.1٪ ، K₂O 20.5٪ (به عنصر تبدیل شده) - فرم نیتروژن (نیترات/آمونیوم) تخمینی از مواد اولیهٔ متداول و قیمت تخمینی؛ نیاز به تأیید شرکت - میکروها کلاته (نوع کلات نامشخص) - فلزات سنگین: Pb 12.7، Cd 0.6، Co 3.1، Ni 3.4 ppb، As <0.05 ppm"
    },
    {
        "name": "GRANJA Potassium Sulfate (K₂SO₄)",
        "brand": "GRANJA",
        "category": "ماکرو",
        "form": "powder",
        "concentration": 100.0,
        "price_per_kg": 1370000,
        "elements": {"K": 45.492, "S": 19.062, "Mg": 0.012, "Ca": 0.014, "Na": 0.2, "Cl": 0.4},
        "is_acid": False,
        "description": "سولفات پتاسیم شرکت GRANJA - آزمایشگاه ۳۶۴ - K₂O 54.8٪ و SO₃ 47.6٪ (به عنصر تبدیل شده) - حلالیت ۱۱۱ g/L در ۲۰°C - رطوبت ۱٫۴۵٪ - قیمت تخمینی - فلزات سنگین: Pb 14.3، Cd 0.9، Co 7.6، Ni 5.3 ppb، As <0.05 ppm"
    },
    {
        "name": "GRANJA Calcium Nitrate (Ca(NO₃)₂)",
        "brand": "GRANJA",
        "category": "ماکرو",
        "form": "crystal",
        "concentration": 100.0,
        "price_per_kg": 550000,
        "elements": {"N-NO3": 13.9, "N-NH4": 1.1, "Ca": 21.1, "Mg": 0.042, "Na": 0.02, "Cl": 0.07},
        "is_acid": False,
        "ph_level": 6.0,
        "description": "نیترات کلسیم شرکت GRANJA - آزمایشگاه ۳۶۵ - N کل ۱۵٫۰٪ (نیترات ۱۳٫۹٪ + آمونیوم ۱٫۱٪) - Ca محلول ۲۱٫۱٪ - pH (۱:۱۰) برابر ۶٫۰ - قیمت و نوع فیزیکی تخمینی - فلزات سنگین: Pb 14.5، Cd 1.2، Co 4.2، Ni 6.4 ppb، As <0.05 ppm"
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
                is_base=fert_data.get("is_base", False),
                density_g_ml=fert_data.get("density_g_ml"),
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
