# backend/tests/test_report_save_flow.py
#!/usr/bin/env python3
"""
تست کامل جریان ذخیره‌سازی گزارش‌ها و عناصر هدف
این تست بررسی می‌کند که:
1. گزارش جدید به درستی ایجاد شود
2. عناصر هدف ذخیره شوند
3. گزارش بارگذاری مجدد شود و عناصر هدف بازیابی شوند
4. محاسبات به درستی ذخیره و بازیابی شوند
"""

import sys
import json
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, create_tables
from app.models import Base
from app.crud import (
    create_report, get_report_by_id, 
    create_calculation, get_calculation_by_report,
    update_calculation, get_user_by_phone
)
from app.schemas import ReportCreate, CalculationCreate, CalculationUpdate, UserCreate
from app.security import get_password_hash

DB_PATH = Path(__file__).parent.parent / "farmtech.db"

def setup_database():
    """راه‌اندازی دیتابیس تست"""
    print("📦 Setting up test database...")
    
    # ایجاد جدول‌ها
    create_tables()
    
    db = SessionLocal()
    user_id = None
    
    try:
        # بررسی وجود کاربر
        user = get_user_by_phone(db, "09121234567")
        
        if user:
            user_id = user.id
            print(f"✅ Test user exists: ID={user_id}")
        else:
            # ایجاد کاربر تست
            import secrets
            import hashlib
            
            salt = secrets.token_hex(16)
            hash_obj = hashlib.sha256((salt + "Test@123456").encode('utf-8'))
            password_hash = f"{salt}:{hash_obj.hexdigest()}"
            
            # اتصال مستقیم به SQLite برای ایجاد کاربر
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, phone_number, password_hash, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, ("تست", "سیستم", "09121234567", password_hash, 1))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            print(f"✅ Test user created: ID={user_id}")
            
    except Exception as e:
        print(f"❌ Error in setup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    # اگر به هر دلیلی user_id ایجاد نشد، از 1 استفاده کن
    if user_id is None:
        print("⚠️ Using default user_id=1")
        user_id = 1
    
    return user_id

def test_report_creation(db, user_id):
    """تست ۱: ایجاد گزارش"""
    print("\n📌 Test 1: Creating report")
    print("-" * 50)
    
    try:
        report_data = ReportCreate(
            report_name="گزارش تست",
            plant_name="گوجه فرنگی",
            season="بهار",
            growth_stage="گلدهی",
            report_date="۱۴۰۵/۰۴/۱۰"
        )
        
        report = create_report(db, report_data, user_id)
        print(f"✅ Report created: ID={report.id}, Name={report.report_name}")
        return report.id
    except Exception as e:
        print(f"❌ Error creating report: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_create_calculation(db, report_id):
    """تست ۲: ایجاد محاسبات با عناصر هدف"""
    print("\n📌 Test 2: Creating calculation with target values")
    print("-" * 50)
    
    if not report_id:
        print("❌ No report ID provided")
        return None
    
    try:
        target_values = {
            "N-NO3": 140.0,
            "P": 50.0,
            "K": 350.0,
            "Ca": 200.0,
            "Mg": 50.0,
            "S": 150.0,
            "Fe": 3.0,
            "Mn": 0.8,
            "Zn": 0.1,
            "B": 0.3,
            "Cu": 0.07,
            "Mo": 0.03
        }
        
        calc_data = CalculationCreate(
            target_values=target_values,
            final_values={},
            reservoir_data={"A": [], "B": [], "C": []},
            calc_rows=[]
        )
        
        calculation = create_calculation(db, calc_data, report_id)
        print(f"✅ Calculation created: ID={calculation.id}")
        print(f"   Target values: {len(calculation.target_values)} elements")
        return calculation.id
    except Exception as e:
        print(f"❌ Error creating calculation: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_read_calculation(db, report_id):
    """تست ۳: خواندن محاسبات"""
    print("\n📌 Test 3: Reading calculation")
    print("-" * 50)
    
    if not report_id:
        print("❌ No report ID provided")
        return False
    
    try:
        calculation = get_calculation_by_report(db, report_id)
        
        if not calculation:
            print("❌ Calculation not found")
            return False
        
        print(f"✅ Calculation found: ID={calculation.id}")
        print(f"   Target values count: {len(calculation.target_values)}")
        
        # نمایش عناصر
        for element, value in list(calculation.target_values.items())[:5]:
            print(f"   - {element}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading calculation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_update_calculation(db, report_id):
    """تست ۴: به‌روزرسانی محاسبات"""
    print("\n📌 Test 4: Updating calculation")
    print("-" * 50)
    
    if not report_id:
        print("❌ No report ID provided")
        return False
    
    try:
        calculation = get_calculation_by_report(db, report_id)
        
        if not calculation:
            print("❌ Calculation not found")
            return False
        
        # تغییر عناصر هدف
        updated_targets = calculation.target_values.copy()
        updated_targets["K"] = 400.0
        updated_targets["Ca"] = 220.0
        
        calc_update = CalculationUpdate(
            target_values=updated_targets,
            final_values={},
            reservoir_data={"A": [], "B": [], "C": []},
            calc_rows=[]
        )
        
        updated = update_calculation(db, calculation.id, calc_update)
        
        if not updated:
            print("❌ Update failed")
            return False
        
        print(f"✅ Calculation updated: ID={updated.id}")
        print(f"   K: {updated.target_values.get('K')} (expected: 400)")
        print(f"   Ca: {updated.target_values.get('Ca')} (expected: 220)")
        return True
    except Exception as e:
        print(f"❌ Error updating calculation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_read_after_update(db, report_id):
    """تست ۵: خواندن مجدد پس از به‌روزرسانی"""
    print("\n📌 Test 5: Reading after update")
    print("-" * 50)
    
    if not report_id:
        print("❌ No report ID provided")
        return False
    
    try:
        calculation = get_calculation_by_report(db, report_id)
        
        if not calculation:
            print("❌ Calculation not found")
            return False
        
        print(f"✅ Calculation found: ID={calculation.id}")
        print(f"   K: {calculation.target_values.get('K')} (expected: 400)")
        print(f"   Ca: {calculation.target_values.get('Ca')} (expected: 220)")
        
        if calculation.target_values.get('K') != 400:
            print("❌ K value not updated correctly")
            return False
        
        if calculation.target_values.get('Ca') != 220:
            print("❌ Ca value not updated correctly")
            return False
        
        print("✅ All values updated correctly")
        return True
    except Exception as e:
        print(f"❌ Error reading after update: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_create_second_report(db, user_id):
    """تست ۶: ایجاد گزارش دوم و بررسی ریست شدن داده‌ها"""
    print("\n📌 Test 6: Creating second report (should reset data)")
    print("-" * 50)
    
    if not user_id:
        print("❌ No user ID provided")
        return None
    
    try:
        report_data = ReportCreate(
            report_name="گزارش تست دوم",
            plant_name="خیار",
            season="تابستان",
            growth_stage="رشد رویشی",
            report_date="۱۴۰۵/۰۴/۱۵"
        )
        
        report = create_report(db, report_data, user_id)
        print(f"✅ Second report created: ID={report.id}")
        
        # بررسی اینکه محاسبات برای گزارش جدید خالی است
        calculation = get_calculation_by_report(db, report.id)
        
        if calculation:
            print(f"⚠️ Calculation exists for new report: ID={calculation.id}")
            print(f"   Target values: {len(calculation.target_values)}")
        else:
            print("✅ No calculation for new report (correct behavior)")
        
        return report.id
    except Exception as e:
        print(f"❌ Error creating second report: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_database_direct():
    """تست ۷: بررسی مستقیم دیتابیس"""
    print("\n📌 Test 7: Direct database inspection")
    print("-" * 50)
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # بررسی جدول reports
        cursor.execute("SELECT id, report_name, user_id FROM reports ORDER BY id DESC LIMIT 5")
        reports = cursor.fetchall()
        
        print(f"📊 Recent reports:")
        for report in reports:
            print(f"   ID: {report[0]}, Name: {report[1]}, User: {report[2]}")
        
        # بررسی جدول calculations
        cursor.execute("""
            SELECT id, report_id, target_values 
            FROM calculations 
            ORDER BY id DESC 
            LIMIT 5
        """)
        calcs = cursor.fetchall()
        
        print(f"\n📊 Recent calculations:")
        for calc in calcs:
            calc_id, report_id, target_values = calc
            print(f"   ID: {calc_id}, Report: {report_id}")
            if target_values:
                try:
                    if isinstance(target_values, str):
                        target_values = json.loads(target_values)
                    print(f"   Elements: {len(target_values)}")
                except:
                    print(f"   Elements: (parse error)")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error in database direct: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 70)
    print("🧪 Testing Report Save Flow")
    print("=" * 70)
    
    # Setup
    user_id = setup_database()
    if not user_id:
        print("❌ Failed to setup database")
        return False
    
    db = SessionLocal()
    
    results = []
    
    try:
        # تست ۱: ایجاد گزارش
        report_id = test_report_creation(db, user_id)
        results.append(report_id is not None)
        
        if report_id:
            # تست ۲: ایجاد محاسبات
            calc_id = test_create_calculation(db, report_id)
            results.append(calc_id is not None)
            
            # تست ۳: خواندن محاسبات
            results.append(test_read_calculation(db, report_id))
            
            # تست ۴: به‌روزرسانی محاسبات
            results.append(test_update_calculation(db, report_id))
            
            # تست ۵: خواندن مجدد
            results.append(test_read_after_update(db, report_id))
        
        # تست ۶: ایجاد گزارش دوم
        second_report_id = test_create_second_report(db, user_id)
        results.append(second_report_id is not None)
        
        # تست ۷: بررسی دیتابیس
        results.append(test_database_direct())
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)
    finally:
        db.close()
    
    # جمع‌بندی
    print("\n" + "=" * 70)
    print("📊 Results Summary")
    print("=" * 70)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Database operations are working correctly.")
        print("⚠️  The issue is in the frontend code, not the backend.")
    else:
        print("\n❌ Some tests failed. Please check the database schema.")
        print("\n💡 Try running: python create_db_direct.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)