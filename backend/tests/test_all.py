# backend/test_complete_fix.py
"""تست کامل و خودکار - همه مراحل را انجام می‌دهد"""

import requests
import json
import random
import sys
import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/health"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@localhost:5432/farmtech_db")

# ===== رنگ‌ها =====
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.RESET}")
def print_info(msg): print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")
def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")

def generate_phone():
    return f"0912{random.randint(1000000, 9999999)}"

# ============================================================
# بخش 1: تست دیتابیس
# ============================================================

def test_database():
    """بررسی اتصال به دیتابیس و وجود جدول‌ها"""
    print_header("۱. تست دیتابیس")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # بررسی جدول users
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_exists = cursor.fetchone()[0]
        print_info(f"جدول users: {'✅ وجود دارد' if users_exists else '❌ وجود ندارد'}")
        
        # بررسی جدول user_sessions
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'user_sessions'
            );
        """)
        sessions_exists = cursor.fetchone()[0]
        print_info(f"جدول user_sessions: {'✅ وجود دارد' if sessions_exists else '❌ وجود ندارد'}")
        
        # اگر جدول user_sessions وجود نداشت، ایجاد کن
        if not sessions_exists:
            print_warning("جدول user_sessions وجود ندارد، در حال ایجاد...")
            cursor.execute("""
                CREATE TABLE user_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    token VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)
            cursor.execute("CREATE INDEX idx_user_sessions_token ON user_sessions(token);")
            cursor.execute("CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);")
            conn.commit()
            print_success("جدول user_sessions با موفقیت ایجاد شد!")
        
        # تعداد کاربران
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print_info(f"تعداد کاربران: {user_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"خطا در تست دیتابیس: {e}")
        return False

# ============================================================
# بخش 2: تست سلامت سرور
# ============================================================

def test_health():
    print_header("۲. تست سلامت سرور")
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"سرور سالم است (Status: {response.status_code})")
            return True
        print_error(f"سرور پاسخ داد اما با خطا: {response.status_code}")
        return False
    except:
        print_error("سرور در دسترس نیست! لطفاً بک‌اند را اجرا کنید.")
        print_info("دستور: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return False

# ============================================================
# بخش 3: تست ثبت‌نام
# ============================================================

def test_register(phone, password):
    print_header(f"۳. تست ثبت‌نام ({phone})")
    
    data = {
        "first_name": "تست",
        "last_name": "کاربر",
        "phone_number": phone,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=data, timeout=10)
        print_info(f"وضعیت: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print_success("ثبت‌نام موفق!")
            print_info(f"پاسخ: {response.json()}")
            return True, response.json()
        elif response.status_code == 400:
            error_detail = response.json().get('detail', '')
            if "قبلاً ثبت شده" in error_detail:
                print_warning("کاربر قبلاً ثبت شده است")
                return True, None
            else:
                print_error(f"خطا: {error_detail}")
                return False, None
        else:
            print_error(f"ثبت‌نام ناموفق: {response.text}")
            return False, None
    except Exception as e:
        print_error(f"خطا: {e}")
        return False, None

# ============================================================
# بخش 4: تست ورود
# ============================================================

def test_login(phone, password):
    print_header(f"۴. تست ورود ({phone})")
    
    data = {
        "phone_number": phone,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data, timeout=10)
        print_info(f"وضعیت: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print_success("ورود موفق! توکن دریافت شد.")
            print_info(f"توکن: {token[:30]}...")
            print_info(f"زمان انقضا: {result.get('expires_in')} ثانیه")
            return True, token
        elif response.status_code == 401:
            print_error("ورود ناموفق: شماره تلفن یا رمز عبور اشتباه است")
            print_info(f"پاسخ: {response.text}")
            return False, None
        else:
            print_error(f"ورود ناموفق: {response.text}")
            return False, None
    except Exception as e:
        print_error(f"خطا: {e}")
        return False, None

# ============================================================
# بخش 5: تست /me
# ============================================================

def test_me(token):
    print_header("۵. تست /me")
    
    if not token:
        print_error("توکن وجود ندارد")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=10)
        print_info(f"وضعیت: {response.status_code}")
        
        if response.status_code == 200:
            print_success("دریافت اطلاعات کاربر موفق!")
            print_info(f"کاربر: {response.json()}")
            return True
        elif response.status_code == 401:
            print_error("خطای 401: توکن نامعتبر است")
            print_info(f"پاسخ: {response.text}")
            return False
        else:
            print_error(f"خطا: {response.text}")
            return False
    except Exception as e:
        print_error(f"خطا: {e}")
        return False

# ============================================================
# بخش 6: تست /fertilizers
# ============================================================

def test_fertilizers(token):
    print_header("۶. تست /fertilizers")
    
    if not token:
        print_error("توکن وجود ندارد")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/fertilizers", headers=headers, timeout=10)
        print_info(f"وضعیت: {response.status_code}")
        
        if response.status_code == 200:
            print_success("دریافت کودها موفق!")
            print_info(f"تعداد کودها: {len(response.json())}")
            return True
        elif response.status_code == 401:
            print_error("خطای 401: توکن نامعتبر است")
            return False
        else:
            print_error(f"خطا: {response.text}")
            return False
    except Exception as e:
        print_error(f"خطا: {e}")
        return False

# ============================================================
# بخش 7: تست ایجاد کود
# ============================================================

def test_create_fertilizer(token):
    print_header("۷. تست ایجاد کود")
    
    if not token:
        print_error("توکن وجود ندارد")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "کود تست NPK",
        "price_per_kg": 25000,
        "elements": {
            "N-NO3": 14.5,
            "P": 22,
            "K": 28
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/fertilizers", json=data, headers=headers, timeout=10)
        print_info(f"وضعیت: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print_success("ایجاد کود موفق!")
            print_info(f"پاسخ: {response.json()}")
            return True
        elif response.status_code == 401:
            print_error("خطای 401: توکن نامعتبر است")
            return False
        else:
            print_error(f"خطا: {response.text}")
            return False
    except Exception as e:
        print_error(f"خطا: {e}")
        return False

# ============================================================
# بخش 8: تست مستقیم دیتابیس (بررسی توکن ذخیره شده)
# ============================================================

def test_database_token(token):
    print_header("۸. بررسی توکن در دیتابیس")
    
    if not token:
        print_error("توکن وجود ندارد")
        return False
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, token, created_at, expires_at, is_active 
            FROM user_sessions 
            WHERE token = %s
        """, (token,))
        
        result = cursor.fetchone()
        
        if result:
            print_success("توکن در دیتابیس پیدا شد!")
            print_info(f"ID: {result[0]}")
            print_info(f"user_id: {result[1]}")
            print_info(f"token: {result[2][:20]}...")
            print_info(f"ایجاد: {result[3]}")
            print_info(f"انقضا: {result[4]}")
            print_info(f"فعال: {result[5]}")
            return True
        else:
            print_error("توکن در دیتابیس پیدا نشد!")
            return False
            
    except Exception as e:
        print_error(f"خطا: {e}")
        return False

# ============================================================
# بخش 9: جمع‌بندی و نتیجه‌گیری
# ============================================================

def run_all_tests():
    print_header("🚀 تست کامل و خودکار")
    
    # 1. تست دیتابیس
    db_ok = test_database()
    if not db_ok:
        print_error("❌ تست دیتابیس ناموفق")
        return
    
    # 2. تست سلامت
    if not test_health():
        print_error("❌ سرور در دسترس نیست")
        return
    
    # 3. ثبت‌نام
    phone = generate_phone()
    password = "123456"
    print_info(f"شماره تلفن تست: {phone}")
    print_info(f"رمز عبور: {password}")
    
    register_success, user_data = test_register(phone, password)
    if not register_success:
        print_error("❌ ثبت‌نام ناموفق")
        return
    
    # 4. ورود
    login_success, token = test_login(phone, password)
    if not login_success or not token:
        print_error("❌ ورود ناموفق")
        return
    
    # 5. تست /me
    me_ok = test_me(token)
    
    # 6. تست /fertilizers
    fert_ok = test_fertilizers(token)
    
    # 7. تست ایجاد کود
    create_ok = test_create_fertilizer(token)
    
    # 8. بررسی توکن در دیتابیس
    db_token_ok = test_database_token(token)
    
    # ===== گزارش نهایی =====
    print_header("📊 گزارش نهایی")
    
    results = [
        ("دیتابیس", db_ok),
        ("ثبت‌نام", register_success),
        ("ورود", login_success),
        ("/me", me_ok),
        ("/fertilizers", fert_ok),
        ("ایجاد کود", create_ok),
        ("توکن در دیتابیس", db_token_ok)
    ]
    
    passed = 0
    failed = 0
    
    for name, status in results:
        if status:
            print_success(f"{name}: موفق")
            passed += 1
        else:
            print_error(f"{name}: ناموفق")
            failed += 1
    
    print("="*70)
    print(f"✅ موفق: {passed}")
    print(f"❌ ناموفق: {failed}")
    
    if failed == 0:
        print_success("🎉 همه تست‌ها با موفقیت انجام شدند!")
        print_info(f"📱 شماره تلفن تست: {phone}")
        print_info(f"🔑 رمز عبور: {password}")
    else:
        print_error("⚠️ برخی تست‌ها ناموفق بودند")
        print_warning("پیشنهاد: لاگ‌های سرور را بررسی کنید")
    
    print("="*70)

if __name__ == "__main__":
    run_all_tests()