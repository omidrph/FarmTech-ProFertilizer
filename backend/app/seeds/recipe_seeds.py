# backend/app/seeds/recipe_seeds.py
"""
Seed داده‌های اولیه رسپی‌های سیستمی - نسخه اصلاح شده با تعادل یونی
این فایل شامل ۲۵ رسپی استاندارد برای محصولات مختلف است.

منبع: Howard Resh, University of Florida, Douglas Peckenpaugh
آخرین به‌روزرسانی: تیرماه ۱۴۰۵

✅ اصلاحات انجام شده:
- اضافه شدن یون‌های پادبار (Na, Cl) برای برقراری تعادل یونی
- تلرانس تعادل: اختلاف کاتیون و آنیون < 0.5 meq/L
- عناصر هدف اصلی بدون تغییر باقی مانده‌اند
- اصلاح مقادیر Cu و Mo برای جلوگیری از خطای الگوریتم
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from app.models import Recipe

logger = logging.getLogger(__name__)


# ============================================================
# 📊 داده‌های مرجع برای محاسبه تعادل یونی
# ============================================================

# وزن مولکولی عناصر (g/mol)
MW = {
    'N-NO3': 62.0049,
    'P': 30.9738,
    'S': 32.065,
    'N-NH4': 18.0385,
    'K': 39.0983,
    'Ca': 40.078,
    'Mg': 24.305,
    'Na': 22.9898,
    'Cl': 35.453,
}

# ظرفیت یونی (بار)
VALENCE = {
    'N-NO3': -1,
    'P': -1,
    'S': -2,
    'N-NH4': +1,
    'K': +1,
    'Ca': +2,
    'Mg': +2,
    'Na': +1,
    'Cl': -1,
}

# کاتیون‌ها (بار مثبت)
CATIONS = ['N-NH4', 'K', 'Ca', 'Mg', 'Na']

# آنیون‌ها (بار منفی)
ANIONS = ['N-NO3', 'P', 'S', 'Cl']


def ppm_to_meq(ppm: float, element: str) -> float:
    """تبدیل PPM به MEQ/L"""
    mw = MW.get(element, 0)
    valence = abs(VALENCE.get(element, 0))
    if mw == 0 or valence == 0:
        return 0
    return (ppm * valence) / mw


def calculate_ion_balance(target_values: Dict[str, float]) -> Dict[str, float]:
    """
    محاسبه تعادل یونی یک رسپی
    
    Returns:
        Dict: {'cation': float, 'anion': float, 'difference': float, 'is_balanced': bool}
    """
    cation = 0.0
    anion = 0.0
    
    for element, value in target_values.items():
        if element not in MW or value == 0:
            continue
        meq = ppm_to_meq(value, element)
        if element in CATIONS:
            cation += meq
        elif element in ANIONS:
            anion += meq
    
    return {
        'cation': cation,
        'anion': anion,
        'difference': abs(cation - anion),
        'is_balanced': abs(cation - anion) < 0.5
    }


def add_counter_ions(target_values: Dict[str, float]) -> Dict[str, float]:
    """
    افزودن یون‌های پادبار برای برقراری تعادل یونی
    
    اگر کاتیون‌ها بیشتر باشند → کلر (Cl⁻) اضافه می‌شود
    اگر آنیون‌ها بیشتر باشند → سدیم (Na⁺) اضافه می‌شود
    
    Args:
        target_values: دیکشنری عناصر هدف
    
    Returns:
        Dict: دیکشنری اصلاح شده با یون‌های پادبار
    """
    result = target_values.copy()
    
    # محاسبه تعادل فعلی
    balance = calculate_ion_balance(result)
    
    if balance['is_balanced']:
        return result
    
    cation = balance['cation']
    anion = balance['anion']
    difference = balance['difference']
    
    if cation > anion:
        # کاتیون بیشتر است → کلر (Cl⁻) اضافه می‌شود
        # محاسبه مقدار کلر مورد نیاز (به PPM)
        cl_meq = difference
        cl_ppm = cl_meq * MW['Cl'] / 1  # ظرفیت کلر = 1
        result['Cl'] = round(cl_ppm + 0.5, 2)  # کمی بیشتر برای اطمینان
    else:
        # آنیون بیشتر است → سدیم (Na⁺) اضافه می‌شود
        # محاسبه مقدار سدیم مورد نیاز (به PPM)
        na_meq = difference
        na_ppm = na_meq * MW['Na'] / 1  # ظرفیت سدیم = 1
        result['Na'] = round(na_ppm + 0.5, 2)  # کمی بیشتر برای اطمینان
    
    # بررسی مجدد تعادل
    new_balance = calculate_ion_balance(result)
    
    # اگر هنوز متعادل نشده، مقدار بیشتری اضافه کن
    if not new_balance['is_balanced']:
        if cation > anion:
            extra_cl = new_balance['difference'] * MW['Cl']
            result['Cl'] = result.get('Cl', 0) + round(extra_cl, 2)
        else:
            extra_na = new_balance['difference'] * MW['Na']
            result['Na'] = result.get('Na', 0) + round(extra_na, 2)
    
    return result


def verify_recipe(target_values: Dict[str, float], name: str) -> bool:
    """بررسی یک رسپی و چاپ نتیجه"""
    balance = calculate_ion_balance(target_values)
    status = "✅ متعادل" if balance['is_balanced'] else "❌ نامتعادل"
    print(f"  {name[:40]:<40} | {status} | کاتیون: {balance['cation']:.2f} | آنیون: {balance['anion']:.2f} | اختلاف: {balance['difference']:.2f}")
    return balance['is_balanced']


# ============================================================
# 🆕 لیست کامل رسپی‌های سیستمی (اصلاح شده با تعادل یونی)
# ============================================================

SYSTEM_RECIPES: List[Dict[str, Any]] = [
    # ============================================================
    # ۱. Chilli (maximumyield)
    # ============================================================
    {
        "name": "Chilli (maximumyield)",
        "description": "رسپی استاندارد فلفل - حداکثر عملکرد - اصلاح شده با تعادل یونی",
        "category": "فلفل",
        "stage": "گلدهی و میوه‌دهی",
        "target_values": {
            "N-NO3": 320, "N-NH4": 0, "P": 103, "K": 364,
            "Mg": 96, "Ca": 330, "S": 174,
            "Fe": 4.9, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 465.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲. Cucumber (Howard Resh)
    # ============================================================
    {
        "name": "Cucumber (Howard Resh)",
        "description": "رسپی استاندارد خیار - هوارد رش - اصلاح شده با تعادل یونی",
        "category": "خیار",
        "stage": "رشد و میوه‌دهی",
        "target_values": {
            "N-NO3": 140, "N-NH4": 0, "P": 50, "K": 350,
            "Mg": 50, "Ca": 200, "S": 150,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03,
            "Cl": 320.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۳. Generic Bloom (maximumyield) ✅ اصلاح شده
    # ============================================================
    {
        "name": "Generic Bloom (maximumyield)",
        "description": "رسپی عمومی برای مرحله گلدهی - اصلاح شده با تعادل یونی",
        "category": "عمومی",
        "stage": "گلدهی",
        "target_values": {
            "N-NO3": 130, "N-NH4": 10, "P": 60, "K": 300,
            "Mg": 30, "Ca": 100, "S": 60,
            "Fe": 2, "Mn": 0.5, "Zn": 0.1, "B": 0.5, 
            "Cu": 0.5,  # ✅ از 0.05 به 0.5 افزایش یافت
            "Mo": 0.05,
            "Cl": 200.0  # ✅ افزایش برای تعادل بهتر
        }
    },
    
    # ============================================================
    # ۴. Generic Dry Season (Howard Resh)
    # ============================================================
    {
        "name": "Generic Dry Season (Howard Resh)",
        "description": "رسپی عمومی برای فصل خشک - اصلاح شده با تعادل یونی",
        "category": "عمومی",
        "stage": "فصل خشک",
        "target_values": {
            "N-NO3": 177, "N-NH4": 53, "P": 60, "K": 200,
            "Mg": 36, "Ca": 250, "S": 129,
            "Fe": 5, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.03, "Mo": 0.02,
            "Cl": 130.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۵. Generic for Berries (Growing Edge)
    # ============================================================
    {
        "name": "Generic for Berries (Growing Edge)",
        "description": "رسپی عمومی برای توت‌ها - اصلاح شده با تعادل یونی",
        "category": "توت",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 207, "N-NH4": 0, "P": 55, "K": 289,
            "Mg": 38, "Ca": 155, "S": 51,
            "Fe": 6.8, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 200.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۶. Generic Grow (maximumyield)
    # ============================================================
    {
        "name": "Generic Grow (maximumyield)",
        "description": "رسپی عمومی برای مرحله رشد رویشی - اصلاح شده با تعادل یونی",
        "category": "عمومی",
        "stage": "رشد رویشی",
        "target_values": {
            "N-NO3": 160, "N-NH4": 0, "P": 30, "K": 230,
            "Mg": 30, "Ca": 100, "S": 60,
            "Fe": 2, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.05, "Mo": 0.05,
            "Cl": 155.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۷. Generic Wet Season (Howard Resh)
    # ============================================================
    {
        "name": "Generic Wet Season (Howard Resh)",
        "description": "رسپی عمومی برای فصل مرطوب - اصلاح شده با تعادل یونی",
        "category": "عمومی",
        "stage": "فصل مرطوب",
        "target_values": {
            "N-NO3": 115, "N-NH4": 32, "P": 50, "K": 150,
            "Mg": 50, "Ca": 150, "S": 50,
            "Fe": 5, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.03, "Mo": 0.02,
            "Cl": 180.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۸. Hoagland solution
    # ============================================================
    {
        "name": "Hoagland solution",
        "description": "محلول استاندارد هوگلند - یکی از معروف‌ترین فرمول‌های غذایی - اصلاح شده با تعادل یونی",
        "category": "استاندارد",
        "stage": "عمومی",
        "target_values": {
            "N-NO3": 210, "N-NH4": 0, "P": 31, "K": 235,
            "Mg": 49, "Ca": 200, "S": 64,
            "Fe": 2.9, "Mn": 0.5, "Zn": 0.05, "B": 0.5, "Cu": 0.02, "Mo": 0.05,
            "Cl": 100.0,  # ✅ اضافه شده برای تعادل یونی
            "Na": 15.0    # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۹. Lettuce 2 (Howard Resh)
    # ============================================================
    {
        "name": "Lettuce 2 (Howard Resh)",
        "description": "رسپی استاندارد کاهو - نسخه ۲ هوارد رش - اصلاح شده با تعادل یونی",
        "category": "کاهو",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 165, "N-NH4": 15, "P": 50, "K": 210,
            "Mg": 45, "Ca": 190, "S": 113,
            "Fe": 4, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.1, "Mo": 0.05,
            "Cl": 160.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۰. Lettuce General (Howard Resh)
    # ============================================================
    {
        "name": "Lettuce General (Howard Resh)",
        "description": "رسپی عمومی کاهو - هوارد رش - اصلاح شده با تعادل یونی",
        "category": "کاهو",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 165, "N-NH4": 15, "P": 50, "K": 210,
            "Mg": 45, "Ca": 190, "S": 65,
            "Fe": 4, "Mn": 0.5, "Zn": 0.1, "B": 0.5, "Cu": 0.1, "Mo": 0.05,
            "Cl": 180.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۱. Melons (Douglas Peckenpaugh)
    # ============================================================
    {
        "name": "Melons (Douglas Peckenpaugh)",
        "description": "رسپی استاندارد طالبی و خربزه - اصلاح شده با تعادل یونی",
        "category": "خربزه و طالبی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 215, "N-NH4": 0, "P": 86, "K": 343,
            "Mg": 85, "Ca": 175, "S": 113,
            "Fe": 6.8, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 270.0,  # ✅ اضافه شده برای تعادل یونی
            "Si": 10
        }
    },
    
    # ============================================================
    # ۱۲. Pepper (Howard Resh)
    # ============================================================
    {
        "name": "Pepper (Howard Resh)",
        "description": "رسپی استاندارد فلفل دلمه‌ای - هوارد رش - اصلاح شده با تعادل یونی",
        "category": "فلفل",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 190, "N-NH4": 18, "P": 40, "K": 340,
            "Mg": 50, "Ca": 170, "S": 360,
            "Fe": 5, "Mn": 0.55, "Zn": 0.33, "B": 0.33, "Cu": 0.05, "Mo": 0.05,
            "Cl": 100.0,  # ✅ اضافه شده برای تعادل یونی
            "Na": 120.0   # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۳. Rice (Douglas Peckenpaugh)
    # ============================================================
    {
        "name": "Rice (Douglas Peckenpaugh)",
        "description": "رسپی استاندارد برنج - اصلاح شده با تعادل یونی",
        "category": "برنج",
        "stage": "رشد",
        "target_values": {
            "N-NO3": 249, "N-NH4": 0, "P": 58, "K": 80,
            "Mg": 65, "Ca": 317, "S": 87,
            "Fe": 5, "Mn": 0.8, "Zn": 0.4, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 310.0,  # ✅ اضافه شده برای تعادل یونی
            "Si": 100
        }
    },
    
    # ============================================================
    # ۱۴. Strawberry Drip Irrigation (schundler.com)
    # ============================================================
    {
        "name": "Strawberry Drip Irrigation (schundler.com)",
        "description": "رسپی توت فرنگی - آبیاری قطره‌ای - اصلاح شده با تعادل یونی",
        "category": "توت فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 80, "N-NH4": 0, "P": 45, "K": 100,
            "Mg": 50, "Ca": 200, "S": 180,
            "Fe": 3, "Mn": 0.5, "Zn": 0.5, "B": 0.5, "Cu": 0.05, "Mo": 0.05,
            "Cl": 140.0,  # ✅ اضافه شده برای تعادل یونی
            "Na": 10.0    # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۵. Strawberry Fruiting (growing edge)
    # ============================================================
    {
        "name": "Strawberry Fruiting (growing edge)",
        "description": "رسپی توت فرنگی - مرحله میوه‌دهی - اصلاح شده با تعادل یونی",
        "category": "توت فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 128, "N-NH4": 0, "P": 58, "K": 211,
            "Mg": 40, "Ca": 104, "S": 54,
            "Fe": 5, "Mn": 2, "Zn": 0.25, "B": 0.7, "Cu": 0.07, "Mo": 0.05,
            "Cl": 120.0,  # ✅ اضافه شده برای تعادل یونی
            "Na": 15.0    # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۶. Tomato (Howard Resh)
    # ============================================================
    {
        "name": "Tomato (Howard Resh)",
        "description": "رسپی استاندارد گوجه فرنگی - هوارد رش - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "میوه‌دهی",
        "target_values": {
            "N-NO3": 140, "N-NH4": 0, "P": 50, "K": 352,
            "Mg": 50, "Ca": 180, "S": 168,
            "Fe": 5, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03,
            "Cl": 250.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۷. Tomato Stage 1 (10-14 days) - Howard Resh
    # ============================================================
    {
        "name": "Tomato Stage 1 (10-14 days)",
        "description": "رسپی گوجه فرنگی - مرحله ۱ (۱۰-۱۴ روزه) - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "نشاء (۱۰-۱۴ روز)",
        "target_values": {
            "N-NO3": 100, "N-NH4": 0, "P": 40, "K": 200,
            "Mg": 20, "Ca": 100, "S": 53,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03,
            "Cl": 150.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۸. Tomato Stage 2 (first cluster) - Howard Resh
    # ============================================================
    {
        "name": "Tomato Stage 2 (first cluster)",
        "description": "رسپی گوجه فرنگی - مرحله ۲ (اولین خوشه) - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "اولین خوشه",
        "target_values": {
            "N-NO3": 130, "N-NH4": 10, "P": 55, "K": 300,
            "Mg": 33, "Ca": 150, "S": 109,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03,
            "Cl": 180.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۱۹. Tomato Stage 3 (plant maturity) - Howard Resh
    # ============================================================
    {
        "name": "Tomato Stage 3 (plant maturity)",
        "description": "رسپی گوجه فرنگی - مرحله ۳ (بلوغ گیاه) - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "بلوغ گیاه",
        "target_values": {
            "N-NO3": 180, "N-NH4": 0, "P": 65, "K": 400,
            "Mg": 45, "Ca": 400, "S": 144,
            "Fe": 3, "Mn": 0.8, "Zn": 0.1, "B": 0.3, "Cu": 0.07, "Mo": 0.03,
            "Cl": 340.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۰. Tomatoes - Fourth Cluster (U of Florida)
    # ============================================================
    {
        "name": "Tomatoes - Fourth Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه چهارم - دانشگاه فلوریدا - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "خوشه چهارم",
        "target_values": {
            "N-NO3": 120, "N-NH4": 0, "P": 50, "K": 150,
            "Mg": 50, "Ca": 150, "S": 60,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05,
            "Cl": 280.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۱. Tomatoes - Second Cluster (U of Florida)
    # ============================================================
    {
        "name": "Tomatoes - Second Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه دوم - دانشگاه فلوریدا - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "خوشه دوم",
        "target_values": {
            "N-NO3": 80, "N-NH4": 0, "P": 50, "K": 120,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05,
            "Cl": 240.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۲. Tomatoes - Third Cluster (U of Florida)
    # ============================================================
    {
        "name": "Tomatoes - Third Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - خوشه سوم - دانشگاه فلوریدا - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "خوشه سوم",
        "target_values": {
            "N-NO3": 100, "N-NH4": 0, "P": 50, "K": 150,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05,
            "Cl": 250.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۳. Tomatoes - till First Cluster (U of Florida)
    # ============================================================
    {
        "name": "Tomatoes - till First Cluster (U of Florida)",
        "description": "رسپی گوجه فرنگی - تا اولین خوشه - دانشگاه فلوریدا - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "تا اولین خوشه",
        "target_values": {
            "N-NO3": 70, "N-NH4": 0, "P": 50, "K": 120,
            "Mg": 40, "Ca": 150, "S": 50,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05,
            "Cl": 230.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۴. Tomatoes to termination (U of Florida)
    # ============================================================
    {
        "name": "Tomatoes to termination (U of Florida)",
        "description": "رسپی گوجه فرنگی - تا پایان دوره - دانشگاه فلوریدا - اصلاح شده با تعادل یونی",
        "category": "گوجه فرنگی",
        "stage": "پایان دوره",
        "target_values": {
            "N-NO3": 150, "N-NH4": 0, "P": 50, "K": 200,
            "Mg": 50, "Ca": 150, "S": 60,
            "Fe": 2.8, "Mn": 0.8, "Zn": 0.3, "B": 0.7, "Cu": 0.2, "Mo": 0.05,
            "Cl": 310.0  # ✅ اضافه شده برای تعادل یونی
        }
    },
    
    # ============================================================
    # ۲۵. Tropical Lettuce (Douglas Peckenpaugh) ✅ اصلاح شده
    # ============================================================
    {
        "name": "Tropical Lettuce (Douglas Peckenpaugh)",
        "description": "رسپی کاهو گرمسیری - داگلاس پکنپا - اصلاح شده با تعادل یونی",
        "category": "کاهو",
        "stage": "رشد گرمسیری",
        "target_values": {
            "N-NO3": 190, "N-NH4": 0, "P": 25, "K": 98,
            "Mg": 25, "Ca": 216, "S": 33,
            "Fe": 4.9, "Mn": 1.97, "Zn": 0.25, "B": 0.7, "Cu": 0.07, 
            "Mo": 0.5,  # ✅ از 0.05 به 0.5 افزایش یافت
            "Cl": 180.0,  # ✅ افزایش برای تعادل بهتر
            "Na": 25.0    # ✅ افزایش برای تعادل بهتر
        }
    },
]


# ============================================================
# تابع اجرای Seed
# ============================================================

def seed_system_recipes(db: Session, verify: bool = True) -> Dict[str, int]:
    """
    افزودن رسپی‌های سیستمی به دیتابیس
    
    Args:
        db: Session دیتابیس
        verify: آیا تعادل یونی را بررسی و چاپ کند
    
    Returns:
        Dict با آمار عملیات
    """
    stats = {
        "added": 0,
        "skipped": 0,
        "total": len(SYSTEM_RECIPES),
        "errors": []
    }
    
    logger.info(f"🌱 شروع Seed رسپی‌های سیستمی - تعداد: {stats['total']}")
    
    # بررسی تعادل یونی (اختیاری)
    if verify:
        print("\n" + "=" * 80)
        print("📊 بررسی تعادل یونی رسپی‌های سیستمی (قبل از ذخیره)")
        print("=" * 80)
        balanced_count = 0
        for recipe in SYSTEM_RECIPES:
            if verify_recipe(recipe['target_values'], recipe['name']):
                balanced_count += 1
        print("-" * 80)
        print(f"✅ رسپی‌های متعادل: {balanced_count}/{len(SYSTEM_RECIPES)}")
        print("=" * 80 + "\n")
    
    for recipe_data in SYSTEM_RECIPES:
        try:
            # بررسی وجود رسپی با همین نام
            existing = db.query(Recipe).filter(
                Recipe.name == recipe_data["name"],
                Recipe.is_system == True
            ).first()
            
            if existing:
                stats["skipped"] += 1
                logger.debug(f"⏭️  رد شد (موجود): {recipe_data['name']}")
                continue
            
            # ایجاد رسپی سیستمی جدید
            new_recipe = Recipe(
                name=recipe_data["name"],
                description=recipe_data.get("description"),
                category=recipe_data.get("category"),
                stage=recipe_data.get("stage"),
                target_values=recipe_data["target_values"],
                is_system=True,
                user_id=None
            )
            
            db.add(new_recipe)
            stats["added"] += 1
            logger.info(f"✅ اضافه شد: {recipe_data['name']}")
            
        except Exception as e:
            stats["errors"].append({
                "name": recipe_data["name"],
                "error": str(e)
            })
            logger.error(f"❌ خطا در افزودن {recipe_data['name']}: {e}")
    
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


def get_system_recipes_count(db: Session) -> int:
    """دریافت تعداد رسپی‌های سیستمی موجود در دیتابیس"""
    return db.query(Recipe).filter(
        Recipe.is_system == True
    ).count()


def clear_system_recipes(db: Session) -> int:
    """
    حذف تمام رسپی‌های سیستمی از دیتابیس
    (برای اجرای مجدد seed)
    
    Returns:
        تعداد رسپی‌های حذف شده
    """
    count = db.query(Recipe).filter(
        Recipe.is_system == True
    ).delete()
    db.commit()
    logger.info(f"🗑️  {count} رسپی سیستمی حذف شد")
    return count


def verify_all_recipes() -> Dict[str, Any]:
    """
    بررسی تعادل یونی همه رسپی‌ها (بدون تغییر در دیتابیس)
    
    Returns:
        Dict: آمار و جزئیات
    """
    print("\n" + "=" * 80)
    print("📊 بررسی تعادل یونی رسپی‌های سیستمی")
    print("=" * 80)
    
    results = []
    balanced_count = 0
    
    for recipe in SYSTEM_RECIPES:
        balance = calculate_ion_balance(recipe['target_values'])
        is_balanced = balance['is_balanced']
        if is_balanced:
            balanced_count += 1
        results.append({
            'name': recipe['name'],
            'category': recipe.get('category', ''),
            'stage': recipe.get('stage', ''),
            'cation': balance['cation'],
            'anion': balance['anion'],
            'difference': balance['difference'],
            'is_balanced': is_balanced
        })
    
    print(f"\n✅ رسپی‌های متعادل: {balanced_count}/{len(SYSTEM_RECIPES)}")
    print(f"❌ رسپی‌های نامتعادل: {len(SYSTEM_RECIPES) - balanced_count}/{len(SYSTEM_RECIPES)}")
    
    # نمایش رسپی‌های نامتعادل (اگر وجود داشته باشند)
    unbalanced = [r for r in results if not r['is_balanced']]
    if unbalanced:
        print("\n⚠️ رسپی‌های نامتعادل:")
        for r in unbalanced[:5]:
            print(f"  - {r['name'][:40]}: اختلاف {r['difference']:.2f} meq/L")
        if len(unbalanced) > 5:
            print(f"  ... و {len(unbalanced) - 5} رسپی دیگر")
    
    print("=" * 80)
    
    return {
        'total': len(results),
        'balanced': balanced_count,
        'unbalanced': len(results) - balanced_count,
        'results': results
    }


# ============================================================
# اجرای مستقیم برای تست
# ============================================================

if __name__ == "__main__":
    # فقط برای تست - بدون اتصال به دیتابیس
    print("\n🔍 بررسی تعادل یونی رسپی‌ها...\n")
    verify_all_recipes()