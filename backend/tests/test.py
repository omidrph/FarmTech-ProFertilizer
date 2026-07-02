#!/usr/bin/env python3
"""
تست محاسبه EC و pH - تشخیص دقیق مشکل
======================================

این اسکریپت محاسبات EC و pH را با داده‌های واقعی تست می‌کند.

نحوه اجرا:
    cd backend
    python tests/test_ec_ph_debug.py
"""

import sys
import os
import json
from pathlib import Path

# اضافه کردن مسیر backend به sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.ion_balance import (
    calculate_ec,
    calculate_ph,
    get_ec_ph_status,
    calculate_ion_balance,
    auto_balance_ion,
    ppm_to_meq,
    ALL_ELEMENTS,
    CATION_ELEMENTS,
    ANION_ELEMENTS,
    VALENCES,
    MOLECULAR_WEIGHTS,
    ION_TO_EC_COEFFICIENTS,
    ACIDITY_COEFFICIENTS
)

print("=" * 80)
print("🧪 تست محاسبه EC و pH - تشخیص دقیق مشکل")
print("=" * 80 + "\n")

# ============================================================
# داده‌های تست - از خروجی واقعی برنامه
# ============================================================

# غلظت نهایی عناصر (از خروجی)
CONCENTRATIONS = {
    "N-NO3": 320.0,
    "P": 103.0,
    "S": 174.0,
    "K": 364.0,
    "Ca": 330.0,
    "Mg": 96.0,
    "Fe": 4.9,
    "Mn": 2.0,
    "Zn": 0.2,
    "B": 0.7,
    "Cu": 0.1,
    "Mo": 0.1,
    "Cl": 515.6,
    "N-NH4": 0.0,
    "Na": 0.0
}

# آب کاربر (از آنالیز آب)
WATER_VALUES = {
    "EC": 0.8,  # dS/m
    "pH": 7.0,  # pH آب
    "Ca": 30.0
}

print("📊 داده‌های تست:")
print(f"  غلظت عناصر: {len(CONCENTRATIONS)} عنصر")
print(f"  pH آب: {WATER_VALUES.get('pH', 7.0)}")
print(f"  EC آب: {WATER_VALUES.get('EC', 0.8)} dS/m")
print()

# ============================================================
# تست 1: نمایش ضرایب EC
# ============================================================
print("📌 تست 1: بررسی ضرایب EC")
print("-" * 50)

print("ضرایب EC برای عناصر موجود:")
for element in CONCENTRATIONS:
    if element in ION_TO_EC_COEFFICIENTS:
        coeff = ION_TO_EC_COEFFICIENTS[element]
        meq = ppm_to_meq(CONCENTRATIONS[element], element)
        contribution = meq * coeff
        print(f"  {element}: PPM={CONCENTRATIONS[element]:>8.2f} | MEQ={meq:>8.4f} | ضریب={coeff:>6.3f} | سهم={contribution:>10.4f}")
    else:
        print(f"  {element}: ⚠️ ضریب EC تعریف نشده است!")

print()

# ============================================================
# تست 2: محاسبه EC
# ============================================================
print("📌 تست 2: محاسبه EC")
print("-" * 50)

try:
    ec_result = calculate_ec(CONCENTRATIONS, unit="ppm")
    
    print(f"  EC محاسبه شده: {ec_result['ec']:.4f} dS/m")
    print(f"  وضعیت EC: {ec_result['status_label']}")
    print(f"  تعداد عناصر فعال: {len(ec_result.get('active_elements', []))}")
    
    # نمایش مجموع MEQ
    total_meq = sum(c['meq'] for c in ec_result.get('contributions', {}).values())
    print(f"  مجموع MEQ: {total_meq:.4f} meq/L")
    
    # نمایش سهم هر عنصر در EC
    print("\n  سهم هر عنصر در EC:")
    for element, data in ec_result.get('contributions', {}).items():
        print(f"    {element}: {data['contribution']:.6f} (از {data['meq']:.4f} meq)")
    
    if ec_result['ec'] < 0.5:
        print("\n  ❌ EC بسیار پایین است! (مشکل در ضرایب یا محاسبه)")
    else:
        print("\n  ✅ EC در محدوده قابل قبول است")
        
except Exception as e:
    print(f"  ❌ خطا در محاسبه EC: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================
# تست 3: محاسبه pH
# ============================================================
print("📌 تست 3: محاسبه pH")
print("-" * 50)

try:
    water_ph = WATER_VALUES.get('pH', 7.0)
    ph_result = calculate_ph(CONCENTRATIONS, unit="ppm", water_ph=water_ph)
    
    print(f"  pH آب: {water_ph}")
    print(f"  pH محاسبه شده: {ph_result['ph']:.4f}")
    print(f"  تغییر pH (ph_shift): {ph_result.get('ph_shift', 0):.4f}")
    print(f"  وضعیت pH: {ph_result['status_label']}")
    
    # نمایش ضرایب اسیدی/بازی
    print("\n  ضرایب اسیدی/بازی برای عناصر:")
    for element, data in ph_result.get('contributions', {}).items():
        coeff = data['coefficient']
        meq = data['meq']
        contribution = data['contribution']
        acid_type = "اسیدی" if coeff > 0 else "بازی" if coeff < 0 else "خنثی"
        print(f"    {element}: ضریب={coeff:>6.2f} | MEQ={meq:>8.4f} | سهم={contribution:>8.4f} | {acid_type}")
    
    if ph_result['ph'] < 4.0:
        print("\n  ❌ pH بسیار پایین است! (مشکل در ضرایب اسیدی/بازی)")
    else:
        print("\n  ✅ pH در محدوده قابل قبول است")
        
except Exception as e:
    print(f"  ❌ خطا در محاسبه pH: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================
# تست 4: بررسی ضرایب اسیدی/بازی
# ============================================================
print("📌 تست 4: بررسی ضرایب اسیدی/بازی")
print("-" * 50)

print("ضرایب اسیدی/بازی برای عناصر موجود:")
for element, value in CONCENTRATIONS.items():
    if value == 0:
        continue
    if element in ACIDITY_COEFFICIENTS:
        coeff = ACIDITY_COEFFICIENTS[element]
        type_label = "اسیدی" if coeff > 0 else "بازی" if coeff < 0 else "خنثی"
        print(f"  {element}: ضریب={coeff:>6.2f} | {type_label}")
    else:
        print(f"  {element}: ⚠️ ضریب اسیدی/بازی تعریف نشده است!")

print()

# ============================================================
# تست 5: بررسی کامل تعادل یونی و auto_balance
# ============================================================
print("📌 تست 5: تعادل یونی و auto_balance")
print("-" * 50)

try:
    cation, anion, is_balanced, details = calculate_ion_balance(CONCENTRATIONS, unit="ppm")
    
    print(f"  کاتیون: {cation:.4f} meq/L")
    print(f"  آنیون: {anion:.4f} meq/L")
    print(f"  اختلاف: {abs(cation - anion):.4f} meq/L")
    print(f"  متعادل: {'✅ بله' if is_balanced else '❌ خیر'}")
    
    # عناصر کاتیون
    print("\n  عناصر کاتیون:")
    for el, val in details.get('cation_elements', {}).items():
        print(f"    {el}: {val:.4f} meq/L")
    
    # عناصر آنیون
    print("\n  عناصر آنیون:")
    for el, val in details.get('anion_elements', {}).items():
        print(f"    {el}: {val:.4f} meq/L")
    
    # عناصر خنثی
    if details.get('neutral_elements'):
        print("\n  عناصر خنثی:")
        for el, val in details.get('neutral_elements', {}).items():
            print(f"    {el}: {val:.4f} meq/L")
    
    # تست auto_balance
    if not is_balanced:
        print("\n  🔄 اعمال auto_balance:")
        balance_result = auto_balance_ion(CONCENTRATIONS, unit="ppm")
        print(f"    متعادل شد: {'✅ بله' if balance_result['is_balanced'] else '❌ خیر'}")
        if balance_result.get('added_element'):
            print(f"    عنصر اضافه شده: {balance_result['added_element']}")
            print(f"    مقدار اضافه شده: {balance_result['added_amount']:.2f} ppm")
        print(f"    پیام: {balance_result['message']}")
        
        # نمایش تعادل جدید
        new_cation, new_anion, new_balanced, _ = calculate_ion_balance(
            balance_result['concentrations'], unit="ppm"
        )
        print(f"    کاتیون جدید: {new_cation:.4f} meq/L")
        print(f"    آنیون جدید: {new_anion:.4f} meq/L")
        print(f"    اختلاف جدید: {abs(new_cation - new_anion):.4f} meq/L")
    
except Exception as e:
    print(f"  ❌ خطا: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================
# تست 6: بررسی علت EC = 0.01
# ============================================================
print("📌 تست 6: بررسی علت EC پایین")
print("-" * 50)

# محاسبه دستی EC
total_ec_manual = 0.0
print("محاسبه دستی EC:")
for element, value in CONCENTRATIONS.items():
    if value == 0:
        continue
    if element not in ION_TO_EC_COEFFICIENTS:
        print(f"  ⚠️ {element}: ضریب EC تعریف نشده!")
        continue
    meq = ppm_to_meq(value, element)
    coeff = ION_TO_EC_COEFFICIENTS[element]
    contribution = meq * coeff
    total_ec_manual += contribution
    print(f"  {element}: {value:.2f} ppm → {meq:.4f} meq × {coeff:.3f} = {contribution:.6f}")

ec_manual = total_ec_manual / 1000
print(f"\n  EC دستی: {ec_manual:.6f} dS/m")

if ec_manual < 0.5:
    print("  ❌ مشکل: ضرایب EC بسیار کوچک هستند!")
    print("  💡 پیشنهاد: ضرایب EC را 10 برابر کنید (0.7 به جای 0.07)")
else:
    print("  ✅ EC دستی در محدوده قابل قبول است")

print()

# ============================================================
# تست 7: بررسی علت pH = 0.00
# ============================================================
print("📌 تست 7: بررسی علت pH پایین")
print("-" * 50)

# محاسبه دستی pH
water_ph = WATER_VALUES.get('pH', 7.0)
ph_shift_manual = 0.0

print(f"pH آب: {water_ph}")
print("محاسبه دستی تغییر pH:")
for element, value in CONCENTRATIONS.items():
    if value == 0:
        continue
    if element not in ACIDITY_COEFFICIENTS:
        print(f"  ⚠️ {element}: ضریب اسیدی/بازی تعریف نشده!")
        continue
    meq = ppm_to_meq(value, element)
    coeff = ACIDITY_COEFFICIENTS[element]
    contribution = meq * coeff
    ph_shift_manual += contribution
    acid_type = "اسیدی" if coeff > 0 else "بازی" if coeff < 0 else "خنثی"
    print(f"  {element}: {value:.2f} ppm → {meq:.4f} meq × {coeff:.2f} = {contribution:.4f} ({acid_type})")

ph_manual = water_ph + ph_shift_manual
print(f"\n  تغییر pH: {ph_shift_manual:.4f}")
print(f"  pH دستی: {ph_manual:.4f}")

if ph_manual < 4.0:
    print("  ❌ مشکل: ضرایب اسیدی/بازی بسیار بزرگ هستند!")
    print("  💡 پیشنهاد: ضرایب را 10 برابر کوچکتر کنید (0.05 به جای 0.5)")
else:
    print("  ✅ pH دستی در محدوده قابل قبول است")

print()

# ============================================================
# خلاصه نهایی
# ============================================================
print("=" * 80)
print("📋 خلاصه نهایی")
print("=" * 80)

print("""
🔍 تشخیص مشکلات:

1. EC = 0.01 dS/m → مشکل در ضرایب EC
   - ضرایب فعلی (0.07) بسیار کوچک هستند
   - باید حدود 10 برابر بزرگتر باشند (0.7)
   - یا اینکه EC باید به جای تقسیم بر 1000، بر 100 تقسیم شود

2. pH = 0.00 → مشکل در ضرایب اسیدی/بازی
   - ضرایب فعلی (0.5) بسیار بزرگ هستند
   - باید حدود 10 برابر کوچکتر باشند (0.05)
   - یا اینکه ضریب N-NH4 باید اصلاح شود

3. Cl = 515.6 با هدف 465 → مشکل در auto_balance
   - auto_balance مقدار Cl را بیش از حد اضافه کرده است
   - باید مقدار دقیق‌تری محاسبه شود

💡 راه‌حل‌های پیشنهادی:
   1. ضرایب EC را از 0.07 به 0.7 تغییر دهید
   2. ضرایب اسیدی/بازی را از 0.5 به 0.05 تغییر دهید
   3. در auto_balance، مقدار دقیق‌تری برای Cl محاسبه کنید
""")

print("=" * 80)
print("✅ تست کامل شد!")
print("=" * 80)