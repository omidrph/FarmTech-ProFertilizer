#!/usr/bin/env python3
"""
تست مخازن FarmTech - بررسی ساختار reservoir_data از بک‌اند

نحوه اجرا:
    cd backend
    python tests/test_reservoir.py

پیش‌نیاز:
    - بک‌اند در حال اجرا باشد (http://localhost:8000)
"""

import requests
import json
import sys
import sqlite3
import hashlib
import secrets
from pathlib import Path
from typing import Dict, List, Any, Optional

# ============================================================
# تنظیمات
# ============================================================
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"
DB_PATH = Path(__file__).parent.parent / "farmtech.db"

# اطلاعات کاربر تست
TEST_USER = {
    "phone_number": "09121234567",
    "password": "Test@123456",
    "first_name": "تست",
    "last_name": "سیستم"
}

# ============================================================
# رنگ‌ها برای خروجی زیبا
# ============================================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.RESET}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")
def print_info(msg): print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")
def print_header(msg): print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n{Colors.BOLD}{msg}{Colors.RESET}\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")


# ============================================================
# توابع دیتابیس
# ============================================================
def create_test_user():
    """ایجاد کاربر تست در دیتابیس اگر وجود نداشته باشد"""
    if not DB_PATH.exists():
        print_warning(f"دیتابیس در مسیر {DB_PATH} وجود ندارد")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # بررسی وجود کاربر
        cursor.execute(
            "SELECT id FROM users WHERE phone_number = ?",
            (TEST_USER["phone_number"],)
        )
        existing = cursor.fetchone()

        if existing:
            print_success(f"کاربر تست قبلاً وجود دارد (ID: {existing[0]})")
            conn.close()
            return True

        # ایجاد کاربر جدید
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((salt + TEST_USER["password"]).encode('utf-8'))
        password_hash = f"{salt}:{hash_obj.hexdigest()}"

        cursor.execute("""
            INSERT INTO users (first_name, last_name, phone_number, password_hash, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, (
            TEST_USER["first_name"],
            TEST_USER["last_name"],
            TEST_USER["phone_number"],
            password_hash,
            1
        ))

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        print_success(f"کاربر تست ایجاد شد (ID: {user_id})")
        return True

    except Exception as e:
        print_error(f"خطا در ایجاد کاربر: {e}")
        return False


# ============================================================
# کلاس تست
# ============================================================
class ReservoirTester:
    def __init__(self):
        self.token: Optional[str] = None
        self.session = requests.Session()

    def login(self) -> bool:
        """ورود به سیستم"""
        print_info("🔐 ورود به سیستم...")

        # ابتدا کاربر را ایجاد کن
        if not create_test_user():
            print_warning("نمی‌توان کاربر تست را ایجاد کرد، ادامه می‌دهیم...")

        try:
            response = self.session.post(
                f"{API_URL}/auth/login",
                json={
                    "phone_number": TEST_USER["phone_number"],
                    "password": TEST_USER["password"]
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })
                print_success("ورود با موفقیت انجام شد")
                return True
            else:
                print_error(f"خطا در ورود: {response.status_code} - {response.text}")
                return False

        except requests.exceptions.ConnectionError:
            print_error("❌ اتصال به سرور برقرار نیست! لطفاً بک‌اند را اجرا کنید.")
            print_info("دستور: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            return False
        except Exception as e:
            print_error(f"خطا در ورود: {e}")
            return False

    def get_fertilizers(self) -> List[Dict]:
        """دریافت لیست کودها"""
        print_info("📥 دریافت لیست کودها...")
        try:
            response = self.session.get(f"{API_URL}/fertilizers?include_system=true", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print_success(f"{len(data)} کود دریافت شد")
                return data
            else:
                print_error(f"خطا در دریافت کودها: {response.status_code}")
                return []
        except Exception as e:
            print_error(f"خطا: {e}")
            return []

    def run_optimization(self, fertilizers: List[Dict]) -> Optional[Dict]:
        """اجرای بهینه‌سازی"""
        print_info("🚀 اجرای بهینه‌سازی...")

        if not fertilizers:
            print_error("هیچ کودی برای بهینه‌سازی وجود ندارد")
            return None

        # انتخاب حداکثر 15 کود
        selected = []
        for f in fertilizers[:15]:
            selected.append({
                'id': str(f.get('id')),
                'name': f.get('name', 'نامشخص'),
                'elements': f.get('elements', {}),
                'price_per_kg': f.get('pricePerKg', f.get('price_per_kg', 0)),
                'purity': f.get('concentration', 100),
                'is_acid': f.get('isAcid', f.get('is_acid', False)),
                'is_system_default': f.get('isSystemDefault', f.get('is_system_default', False))
            })

        print_info(f"📦 {len(selected)} کود انتخاب شد")

        # عناصر هدف
        target_values = {
            'N-NO3': 210,
            'P': 31,
            'K': 235,
            'Ca': 200,
            'Mg': 49,
            'S': 64,
            'Fe': 2.9,
            'Mn': 0.5,
            'Zn': 0.05,
            'B': 0.5,
            'Cu': 0.02,
            'Mo': 0.05
        }

        request_body = {
            'target_values': target_values,
            'water_values': {},
            'fertilizers': selected,
            'options': {
                'method': 'nnls',
                'use_precipitation_check': True,
                'use_ion_balance_check': True,
                'auto_balance': True,
                'reservoir_mode': 'auto'
            },
            'tank_volume': 5000,
            'stock_volume': 100,
            'injection_ratio': 100
        }

        try:
            response = self.session.post(
                f"{API_URL}/calculations/optimize",
                json=request_body,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                print_success("بهینه‌سازی با موفقیت انجام شد")
                return result
            else:
                print_error(f"خطا در بهینه‌سازی: {response.status_code}")
                try:
                    error_data = response.json()
                    print_error(f"پیام: {error_data.get('detail', response.text)}")
                except:
                    print_error(f"پیام: {response.text}")
                return None
        except Exception as e:
            print_error(f"خطا: {e}")
            return None

    def analyze_reservoir_data(self, result: Dict, fertilizers: List[Dict]):
        """تحلیل و نمایش reservoir_data"""
        print_header("📊 تحلیل reservoir_data")

        reservoir_data = result.get('reservoir_data', {'A': [], 'B': [], 'C': []})

        # 1. نمایش خام
        print_info("📄 داده‌های خام reservoir_data:")
        print(json.dumps(reservoir_data, indent=2, ensure_ascii=False))
        print()

        # 2. بررسی هر مخزن
        print_header("🗄️ بررسی مخازن")

        tank_names = {
            'A': 'مخزن کلسیم',
            'B': 'مخزن اصلی',
            'C': 'مخزن اسید'
        }

        all_have_id = True
        total_items = 0
        items_with_id = 0

        for key in ['A', 'B', 'C']:
            items = reservoir_data.get(key, [])
            total_items += len(items)
            print(f"\n{Colors.BOLD}مخزن {key} - {tank_names.get(key, '')}{Colors.RESET}")
            print(f"تعداد: {len(items)} مورد")

            if items:
                for item in items:
                    has_id = item.get('fertilizer_id')
                    items_with_id += 1 if has_id else 0
                    status = "✅" if has_id else "❌"
                    color = Colors.GREEN if has_id else Colors.RED
                    print(f"  {status} name: {color}\"{item.get('name', 'نامشخص')}\"{Colors.RESET}, "
                          f"amount: {item.get('amount', 0)}, "
                          f"fertilizer_id: {color}\"{has_id or 'وجود ندارد'}\"{Colors.RESET}")
                    if not has_id:
                        all_have_id = False
            else:
                print(f"  {Colors.YELLOW}(خالی){Colors.RESET}")

        # 3. بررسی تطابق
        print_header("🔗 تطابق کودها با مخزن")

        # ساخت Map مخزن
        tank_map = {}
        for tank_key, items in reservoir_data.items():
            if items:
                for item in items:
                    fert_id = item.get('fertilizer_id')
                    if fert_id:
                        tank_map[str(fert_id)] = tank_key

        weights = result.get('weights', {})
        print(f"\nتعداد وزن‌های بهینه: {len(weights)}")

        matched = 0
        unmatched = 0
        zero_weights = 0

        for fert_id, weight in weights.items():
            if weight > 0:
                tank = tank_map.get(str(fert_id))
                fert = next((f for f in fertilizers if str(f.get('id')) == str(fert_id)), None)
                name = fert.get('name', fert_id) if fert else fert_id

                if tank:
                    color = Colors.GREEN
                    status = "✅"
                    matched += 1
                else:
                    color = Colors.RED
                    status = "❌"
                    unmatched += 1

                print(f"  {status} {color}{name}{Colors.RESET}: {weight:.3f}g → مخزن {tank or '❌ پیدا نشد'}")
            else:
                zero_weights += 1

        print(f"\n{Colors.BOLD}آمار تطابق:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅ تطابق یافت شد: {matched}{Colors.RESET}")
        print(f"  {Colors.RED}❌ تطابق یافت نشد: {unmatched}{Colors.RESET}")
        print(f"  {Colors.YELLOW}⚠️ وزن صفر: {zero_weights}{Colors.RESET}")

        # 4. نتیجه نهایی
        print_header("📋 نتیجه نهایی")

        print(f"\nآمار مخازن:")
        print(f"  کل آیتم‌ها در مخازن: {total_items}")
        print(f"  آیتم‌های دارای fertilizer_id: {items_with_id}/{total_items}")

        if total_items == 0:
            print_warning("⚠️ هیچ آیتمی در مخازن وجود ندارد!")
            print_warning("   - ممکن است وزن همه کودها صفر باشد")
            print_warning("   - یا بهینه‌سازی به درستی انجام نشده باشد")
            return False

        if all_have_id and matched > 0:
            print_success("✅ همه موارد دارای fertilizer_id هستند و تطابق برقرار است!")
            print_success("✅ مخزن‌ها به درستی نمایش داده می‌شوند.")
            return True
        elif not all_have_id:
            print_error("❌ برخی موارد fertilizer_id ندارند!")
            print_warning("⚠️ لطفاً فایل distributor.py را بررسی کنید:")
            print_warning("   - مطمئن شوید fertilizer_id به آیتم‌های مخزن اضافه شده است")
            print_warning("   - سرور بک‌اند را ری‌استارت کنید")
            return False
        else:
            print_warning("⚠️ برخی از کودها در مخزن پیدا نشدند!")
            print_warning("   - ممکن است نام کودها با هم مطابقت نداشته باشد")
            print_warning("   - بررسی کنید که fertilizer_id به درستی ست شده باشد")
            return False

    def run(self):
        """اجرای کامل تست"""
        print_header("🧪 تست مخازن FarmTech")

        # 1. ورود
        if not self.login():
            print_error("ورود ناموفق، تست متوقف شد")
            return False

        # 2. دریافت کودها
        fertilizers = self.get_fertilizers()
        if not fertilizers:
            print_error("کودی دریافت نشد، تست متوقف شد")
            return False

        # 3. اجرای بهینه‌سازی
        result = self.run_optimization(fertilizers)
        if not result:
            print_error("بهینه‌سازی ناموفق، تست متوقف شد")
            return False

        # 4. تحلیل نتایج
        return self.analyze_reservoir_data(result, fertilizers)


# ============================================================
# اجرای اصلی
# ============================================================
def main():
    tester = ReservoirTester()
    success = tester.run()

    print()
    if success:
        print_success("🎉 همه تست‌ها با موفقیت انجام شد!")
        print_info("💡 مخزن‌ها به درستی نمایش داده می‌شوند.")
    else:
        print_error("❌ برخی تست‌ها ناموفق بودند.")
        print_info("🔧 برای رفع مشکل:")
        print_info("   1. فایل backend/app/core/reservoir/distributor.py را بررسی کنید")
        print_info("   2. مطمئن شوید fertilizer_id به آیتم‌های مخزن اضافه شده است")
        print_info("   3. سرور بک‌اند را ری‌استارت کنید")
        print_info("   4. دوباره تست را اجرا کنید")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())