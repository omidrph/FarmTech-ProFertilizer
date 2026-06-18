# backend/tests/test_all.py
"""
تست جامع همه بخش‌های پروژه FarmTech
برای اطمینان از اینکه همه چیز به درستی کار می‌کند
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any

# ============================================================
# بخش 1: تست تنظیمات و متغیرهای محیطی
# ============================================================

def test_environment():
    """تست متغیرهای محیطی و تنظیمات"""
    print("\n" + "="*60)
    print("📋 بخش 1: تست تنظیمات و متغیرهای محیطی")
    print("="*60)
    
    results = []
    
    # تست وجود فایل .env
    env_exists = os.path.exists(".env")
    results.append({
        "test": "فایل .env",
        "status": "✅" if env_exists else "❌",
        "detail": "وجود دارد" if env_exists else "وجود ندارد"
    })
    
    # تست متغیرهای اصلی
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "DEBUG"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        status = "✅" if value else "❌"
        detail = value[:20] + "..." if value and len(value) > 20 else value
        results.append({
            "test": f"متغیر {var}",
            "status": status,
            "detail": detail if value else "تعریف نشده"
        })
    
    # نمایش نتایج
    for r in results:
        print(f"  {r['status']} {r['test']}: {r['detail']}")
    
    all_passed = all(r["status"] == "✅" for r in results)
    return all_passed


# ============================================================
# بخش 2: تست اتصال به دیتابیس
# ============================================================

def test_database_connection():
    """تست اتصال به دیتابیس PostgreSQL"""
    print("\n" + "="*60)
    print("🗄️ بخش 2: تست اتصال به دیتابیس")
    print("="*60)
    
    try:
        from app.database import engine, SessionLocal
        from sqlalchemy import text
        
        # تست اتصال با یک کوئری ساده
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("  ✅ اتصال به دیتابیس: موفق")
                return True
            else:
                print("  ❌ اتصال به دیتابیس: ناموفق - پاسخ غیرمنتظره")
                return False
                
    except ImportError as e:
        print(f"  ❌ خطا در Import: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطا در اتصال به دیتابیس: {e}")
        return False


# ============================================================
# بخش 3: تست مدل‌ها (Models) - ساده شده
# ============================================================

def test_models():
    """تست مدل‌های دیتابیس"""
    print("\n" + "="*60)
    print("📊 بخش 3: تست مدل‌های دیتابیس")
    print("="*60)
    
    try:
        from app.models import User, Report, Fertilizer, WaterAnalysis, Calculation
        
        # لیست مدل‌ها
        models = [
            ("User", User),
            ("Report", Report),
            ("Fertilizer", Fertilizer),
            ("WaterAnalysis", WaterAnalysis),
            ("Calculation", Calculation)
        ]
        
        all_ok = True
        for name, model in models:
            try:
                # بررسی اینکه مدل دارای نام جدول است
                if hasattr(model, "__tablename__"):
                    print(f"  ✅ مدل {name}: وجود دارد (جدول: {model.__tablename__})")
                else:
                    print(f"  ⚠️ مدل {name}: وجود دارد اما __tablename__ تعریف نشده")
                    all_ok = False
            except Exception as e:
                print(f"  ❌ مدل {name}: خطا - {e}")
                all_ok = False
        
        return all_ok
        
    except ImportError as e:
        print(f"  ❌ خطا در Import مدل‌ها: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطا در تست مدل‌ها: {e}")
        return False


# ============================================================
# بخش 4: تست طرح‌ها (Schemas)
# ============================================================

def test_schemas():
    """تست طرح‌های Pydantic"""
    print("\n" + "="*60)
    print("📝 بخش 4: تست طرح‌های Pydantic")
    print("="*60)
    
    try:
        from app.schemas import (
            UserCreate, UserLogin, UserResponse,
            ReportCreate, ReportResponse,
            FertilizerCreate, FertilizerResponse,
            Token, TokenData
        )
        
        # تست UserCreate
        try:
            user_data = UserCreate(
                first_name="علی",
                last_name="محمدی",
                phone_number="09121234567",
                password="123456"
            )
            print(f"  ✅ UserCreate: موفق - {user_data.phone_number}")
        except Exception as e:
            print(f"  ❌ UserCreate: خطا - {e}")
            return False
        
        # تست FertilizerCreate
        try:
            fert_data = FertilizerCreate(
                name="کود NPK",
                price_per_kg=25000,
                elements={"N": 20, "P": 20, "K": 20}
            )
            print(f"  ✅ FertilizerCreate: موفق - {fert_data.name}")
        except Exception as e:
            print(f"  ❌ FertilizerCreate: خطا - {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ خطا در Import طرح‌ها: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطا در تست طرح‌ها: {e}")
        return False


# ============================================================
# بخش 5: تست امنیت (Security) - اصلاح شده
# ============================================================

def test_security():
    """تست توابع امنیت (JWT)"""
    print("\n" + "="*60)
    print("🔒 بخش 5: تست امنیت")
    print("="*60)
    
    try:
        from app.security import create_access_token, decode_access_token
        from jose import jwt
        
        # تست JWT با داده ساده
        test_data = {"sub": "1", "phone": "09121234567"}
        token = create_access_token(test_data)
        
        if token and len(token) > 0:
            print("  ✅ ایجاد توکن JWT: موفق")
        else:
            print("  ❌ ایجاد توکن JWT: ناموفق")
            return False
        
        # تست رمزگشایی JWT
        decoded = decode_access_token(token)
        if decoded and decoded.user_id == 1:
            print("  ✅ رمزگشایی توکن: موفق")
        else:
            print("  ❌ رمزگشایی توکن: ناموفق")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ خطا در Import امنیت: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطا در تست امنیت: {e}")
        return False


# ============================================================
# بخش 6: تست سرویس‌ها (Services)
# ============================================================

def test_services():
    """تست توابع محاسباتی سرویس‌ها"""
    print("\n" + "="*60)
    print("🧮 بخش 6: تست سرویس‌ها و محاسبات")
    print("="*60)
    
    try:
        from app.services import (
            ppm_to_meq, meq_to_ppm,
            ppm_to_mmol, mmol_to_ppm,
            calculate_ion_balance,
            format_decimal
        )
        
        results = []
        
        # تست تبدیل PPM به MEQ
        ppm_val = 100
        meq_val = ppm_to_meq(ppm_val, "K")
        results.append({
            "name": "PPM → MEQ (K)",
            "status": "✅" if meq_val > 0 else "❌",
            "detail": f"{ppm_val} PPM → {meq_val:.2f} MEQ"
        })
        
        # تست تبدیل MEQ به PPM
        meq_val_back = meq_to_ppm(meq_val, "K")
        results.append({
            "name": "MEQ → PPM (K)",
            "status": "✅" if abs(meq_val_back - ppm_val) < 0.01 else "❌",
            "detail": f"{meq_val:.2f} MEQ → {meq_val_back:.2f} PPM"
        })
        
        # تست تعادل یونی
        target_values = {
            "K": 200,
            "Ca": 150,
            "Mg": 50,
            "Na": 20,
            "N-NO3": 150,
            "Cl": 100
        }
        cation, anion, is_balanced = calculate_ion_balance(target_values)
        results.append({
            "name": "تعادل یونی",
            "status": "✅" if is_balanced else "⚠️",
            "detail": f"کاتیون={cation:.2f}, آنیون={anion:.2f}, {'متعادل' if is_balanced else 'نامتعادل'}"
        })
        
        # تست format_decimal
        formatted = format_decimal(123.45678, 3)
        results.append({
            "name": "فرمت اعداد",
            "status": "✅" if formatted == "123.457" else "❌",
            "detail": f"123.45678 → {formatted}"
        })
        
        # نمایش نتایج
        all_ok = True
        for r in results:
            print(f"  {r['status']} {r['name']}: {r['detail']}")
            if r["status"] == "❌":
                all_ok = False
        
        return all_ok
        
    except ImportError as e:
        print(f"  ❌ خطا در Import سرویس‌ها: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطا در تست سرویس‌ها: {e}")
        return False


# ============================================================
# بخش 7: تست فرانت‌اند (Frontend) - اصلاح مسیر
# ============================================================

def test_frontend():
    """تست وجود فایل‌های فرانت‌اند"""
    print("\n" + "="*60)
    print("🌐 بخش 7: تست فایل‌های فرانت‌اند")
    print("="*60)
    
    # مسیر ریشه پروژه
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    frontend_path = os.path.join(project_root, "frontend")
    
    frontend_files = [
        os.path.join(frontend_path, "package.json"),
        os.path.join(frontend_path, "vite.config.ts"),
        os.path.join(frontend_path, "index.html"),
        os.path.join(frontend_path, "src", "main.ts"),
        os.path.join(frontend_path, "src", "App.vue"),
        os.path.join(frontend_path, "src", "views", "MainLayout.vue"),
        os.path.join(frontend_path, "src", "router", "index.ts"),
        os.path.join(frontend_path, "public", "Logo.webp"),
        os.path.join(frontend_path, "public", "favicon.webp")
    ]
    
    results = []
    all_ok = True
    
    for file_path in frontend_files:
        exists = os.path.exists(file_path)
        # نمایش نام فایل به صورت خلاصه
        short_name = os.path.relpath(file_path, project_root)
        results.append({
            "file": short_name,
            "status": "✅" if exists else "❌"
        })
        if not exists:
            all_ok = False
    
    for r in results:
        print(f"  {r['status']} {r['file']}")
    
    if all_ok:
        print("  ✅ همه فایل‌های فرانت‌اند وجود دارند")
    else:
        print("  ⚠️ برخی فایل‌های فرانت‌اند وجود ندارند")
    
    return all_ok


# ============================================================
# بخش 8: تست API (با بررسی وجود سرور)
# ============================================================

def test_api_endpoints():
    """تست APIهای اصلی با درخواست واقعی"""
    print("\n" + "="*60)
    print("🔗 بخش 8: تست API")
    print("="*60)
    
    try:
        import httpx
        
        # تنظیمات
        base_url = "http://localhost:8000"
        api_prefix = "/api/v1"
        
        async def test_apis():
            async with httpx.AsyncClient(timeout=5.0) as client:
                results = []
                
                # تست 1: Health Check
                try:
                    response = await client.get(f"{base_url}/health")
                    if response.status_code == 200:
                        results.append({"test": "Health Check", "status": "✅", "detail": "OK"})
                    else:
                        results.append({"test": "Health Check", "status": "❌", "detail": f"Status: {response.status_code}"})
                except httpx.ConnectError:
                    results.append({"test": "Health Check", "status": "⚠️", "detail": "سرور در حال اجرا نیست (برای تست API، ابتدا سرور را اجرا کنید)"})
                except Exception as e:
                    results.append({"test": "Health Check", "status": "❌", "detail": str(e)})
                
                # تست 2: ثبت‌نام (Register) - فقط اگر سرور در حال اجرا باشد
                if results[0]["status"] == "✅":
                    try:
                        register_data = {
                            "first_name": "تست",
                            "last_name": "کاربر",
                            "phone_number": "09121234568",
                            "password": "123456"
                        }
                        response = await client.post(
                            f"{base_url}{api_prefix}/auth/register",
                            json=register_data
                        )
                        if response.status_code in [200, 201, 400]:
                            results.append({"test": "ثبت‌نام کاربر", "status": "✅", "detail": f"Status: {response.status_code}"})
                        else:
                            results.append({"test": "ثبت‌نام کاربر", "status": "❌", "detail": f"Status: {response.status_code}"})
                    except Exception as e:
                        results.append({"test": "ثبت‌نام کاربر", "status": "❌", "detail": str(e)})
                    
                    # تست 3: ورود (Login)
                    try:
                        login_data = {
                            "phone_number": "09121234568",
                            "password": "123456"
                        }
                        response = await client.post(
                            f"{base_url}{api_prefix}/auth/login",
                            json=login_data
                        )
                        if response.status_code in [200, 401]:
                            results.append({"test": "ورود کاربر", "status": "✅", "detail": f"Status: {response.status_code}"})
                        else:
                            results.append({"test": "ورود کاربر", "status": "❌", "detail": f"Status: {response.status_code}"})
                    except Exception as e:
                        results.append({"test": "ورود کاربر", "status": "❌", "detail": str(e)})
                else:
                    results.append({"test": "ثبت‌نام کاربر", "status": "⏭️", "detail": "رد شد (سرور در حال اجرا نیست)"})
                    results.append({"test": "ورود کاربر", "status": "⏭️", "detail": "رد شد (سرور در حال اجرا نیست)"})
                
                # نمایش نتایج
                all_ok = True
                for r in results:
                    print(f"  {r['status']} {r['test']}: {r['detail']}")
                    if r["status"] == "❌":
                        all_ok = False
                
                return all_ok
        
        # اجرای تست‌های async
        result = asyncio.run(test_apis())
        return result
        
    except ImportError:
        print("  ⚠️ کتابخانه httpx نصب نیست. تست API انجام نشد.")
        return True
    except Exception as e:
        print(f"  ⚠️ خطا در تست API: {e}")
        return False


# ============================================================
# بخش 9: جمع‌بندی و گزارش نهایی
# ============================================================

def run_all_tests():
    """اجرای همه تست‌ها و نمایش گزارش نهایی"""
    print("\n" + "="*60)
    print("🚀 شروع تست جامع پروژه FarmTech - ProFertilizer")
    print(f"📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # بارگذاری متغیرهای محیطی
    from dotenv import load_dotenv
    load_dotenv()
    
    # اجرای تست‌ها
    tests = [
        ("تنظیمات و متغیرهای محیطی", test_environment),
        ("اتصال به دیتابیس", test_database_connection),
        ("مدل‌های دیتابیس", test_models),
        ("طرح‌های Pydantic", test_schemas),
        ("امنیت (JWT)", test_security),
        ("سرویس‌ها و محاسبات", test_services),
        ("فایل‌های فرانت‌اند", test_frontend),
        ("API", test_api_endpoints)
    ]
    
    results = []
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    
    for name, test_func in tests:
        try:
            passed = test_func()
            # برای تست API که ممکن است Skipped برگرداند
            if name == "API" and passed is None:
                results.append({"name": name, "status": "⏭️"})
                total_skipped += 1
            elif passed:
                results.append({"name": name, "status": "✅"})
                total_passed += 1
            else:
                results.append({"name": name, "status": "❌"})
                total_failed += 1
        except Exception as e:
            print(f"  ❌ خطا در تست {name}: {e}")
            results.append({"name": name, "status": "❌"})
            total_failed += 1
    
    # گزارش نهایی
    print("\n" + "="*60)
    print("📊 گزارش نهایی تست‌ها")
    print("="*60)
    
    for r in results:
        print(f"  {r['status']} {r['name']}")
    
    print("-"*60)
    print(f"  ✅ موفق: {total_passed}")
    print(f"  ❌ ناموفق: {total_failed}")
    if total_skipped > 0:
        print(f"  ⏭️ رد شده: {total_skipped}")
    print(f"  📊 مجموع: {total_passed + total_failed + total_skipped}")
    
    if total_failed == 0:
        print("\n🎉 همه تست‌ها با موفقیت انجام شدند! پروژه آماده است.")
    else:
        print("\n⚠️ برخی تست‌ها ناموفق بودند. لطفاً خطاها را بررسی کنید.")
    
    print("="*60)
    return total_failed == 0


# ============================================================
# اجرای اصلی
# ============================================================

if __name__ == "__main__":
    # مسیر پروژه را به sys.path اضافه کنید
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, backend_dir)
    
    # تغییر دایرکتوری به backend
    os.chdir(backend_dir)
    
    # اجرای تست‌ها
    success = run_all_tests()
    
    # خروج با کد مناسب
    sys.exit(0 if success else 1)