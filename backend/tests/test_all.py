#!/usr/bin/env python3
# backend/tests/test_all.py
"""
🧪 تست کامل سیستم FarmTech - ProFertilizer
===========================================

این فایل تمام بخش‌های برنامه را به صورت End-to-End تست می‌کند.

نحوه اجرا:
    cd backend
    python tests/test_all.py
"""

import os
import sys
import json
import time
import random
import logging
import requests
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# ============================================================
# تنظیمات
# ============================================================

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"
HEALTH_URL = f"{BASE_URL}/health"
DB_PATH = Path(__file__).parent.parent / "farmtech.db"

# ============================================================
# کلاس رنگ‌ها (سازگار با همه سیستم‌عامل‌ها)
# ============================================================

class Colors:
    """کلاس رنگ‌ها برای خروجی زیبا - سازگار با Windows/Linux/Mac"""
    
    # تلاش برای استفاده از colorama
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        GREEN = Fore.GREEN
        RED = Fore.RED
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        PURPLE = Fore.MAGENTA
        CYAN = Fore.CYAN
        BOLD = Style.BRIGHT
        RESET = Style.RESET_ALL
        WHITE = Fore.WHITE
        HAS_COLOR = True
    except ImportError:
        # اگر colorama نصب نیست، از کدهای ANSI استفاده کن
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        WHITE = '\033[97m'
        HAS_COLOR = True
        
        # اگر در Windows هستیم و ANSI پشتیبانی نمی‌شود
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                # اگر نمی‌توانیم ANSI را فعال کنیم، رنگ‌ها را غیرفعال کن
                GREEN = RED = YELLOW = BLUE = PURPLE = CYAN = ''
                BOLD = RESET = WHITE = ''
                HAS_COLOR = False


def print_success(msg): 
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg): 
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_info(msg): 
    print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")

def print_warning(msg): 
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")

def print_subheader(msg):
    print(f"\n{Colors.BOLD}{Colors.PURPLE}--- {msg} ---{Colors.RESET}")

def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================
# Data Classes
# ============================================================

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    duration_ms: float = 0

@dataclass
class TestSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    results: List[TestResult] = None
    
    def __post_init__(self):
        if self.results is None:
            self.results = []


# ============================================================
# کلاس اصلی تستر
# ============================================================

class FarmTechTester:
    """تستر کامل سیستم FarmTech"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.api_url = API_URL
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.report_id: Optional[int] = None
        self.fertilizer_ids: List[int] = []
        self.water_analysis_id: Optional[int] = None
        self.calculation_id: Optional[int] = None
        self.optimization_result: Optional[Dict] = None
        
        # داده‌های تست
        self.test_phone = f"0912{random.randint(1000000, 9999999)}"
        self.test_password = "Test@123456"
        self.test_first_name = "تست"
        self.test_last_name = "سیستم"
        
        self.summary = TestSummary()
        
        print_info(f"📱 شماره تلفن تست: {self.test_phone}")
        print_info(f"🔑 رمز عبور: {self.test_password}")
        print_info(f"🗄️ دیتابیس: {DB_PATH}")
    
    # ============================================================
    # توابع کمکی
    # ============================================================
    
    def _request(self, method: str, endpoint: str, data: Any = None, 
                 headers: Optional[Dict] = None) -> Dict[str, Any]:
        """ارسال درخواست به API"""
        url = f"{self.api_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token and 'Authorization' not in headers:
            headers['Authorization'] = f'Bearer {self.token}'
        
        headers['Content-Type'] = 'application/json'
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Method {method} not supported")
            
            try:
                result = response.json()
            except:
                result = {"raw": response.text}
            
            return {
                "status_code": response.status_code,
                "data": result,
                "success": 200 <= response.status_code < 300
            }
        except requests.exceptions.ConnectionError:
            return {
                "status_code": 0,
                "data": {"error": "ConnectionError - بک‌اند در دسترس نیست"},
                "success": False
            }
        except requests.exceptions.Timeout:
            return {
                "status_code": 0,
                "data": {"error": "Timeout - زمان درخواست به پایان رسید"},
                "success": False
            }
        except Exception as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "success": False
            }
    
    def _assert_success(self, result: Dict, test_name: str) -> bool:
        """بررسی موفقیت یک درخواست"""
        self.summary.total += 1
        
        if result.get("success", False):
            self.summary.passed += 1
            print_success(f"{test_name}: موفق (Status: {result.get('status_code')})")
            return True
        else:
            self.summary.failed += 1
            error_msg = result.get("data", {}).get("error", "Unknown error")
            if isinstance(error_msg, dict):
                error_msg = json.dumps(error_msg, ensure_ascii=False)
            print_error(f"{test_name}: ناموفق (Status: {result.get('status_code')})")
            print_error(f"  خطا: {error_msg}")
            self.summary.results.append(TestResult(
                name=test_name,
                passed=False,
                message=str(error_msg),
                data=result.get("data")
            ))
            return False
    
    def _check_db_connection(self) -> bool:
        """بررسی اتصال به دیتابیس"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            print_info(f"🗄️ دیتابیس متصل است. جداول: {len(tables)}")
            return True
        except Exception as e:
            print_error(f"خطا در اتصال به دیتابیس: {e}")
            return False
    
    def _get_db_data(self, table: str, column: str = "*", 
                     condition: Optional[str] = None) -> List[Dict]:
        """دریافت داده از دیتابیس"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = f"SELECT {column} FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print_error(f"خطا در دریافت داده از دیتابیس: {e}")
            return []
    
    # ============================================================
    # تست 1: بررسی سلامت سرور
    # ============================================================
    
    def test_health(self) -> bool:
        """تست سلامت سرور"""
        print_subheader("1. تست سلامت سرور")
        
        try:
            response = requests.get(HEALTH_URL, timeout=5)
            if response.status_code == 200:
                print_success(f"سرور سالم است (Status: {response.status_code})")
                print_info(f"پاسخ: {response.json()}")
                return True
            else:
                print_error(f"سرور پاسخ داد اما با خطا: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print_error("❌ سرور در دسترس نیست! لطفاً بک‌اند را اجرا کنید.")
            print_info("دستور: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            return False
        except Exception as e:
            print_error(f"خطا: {e}")
            return False
    
    # ============================================================
    # تست 2: دیتابیس
    # ============================================================
    
    def test_database(self) -> bool:
        """تست اتصال به دیتابیس"""
        print_subheader("2. تست اتصال به دیتابیس")
        
        if not self._check_db_connection():
            return False
        
        # بررسی جدول‌ها
        tables = self._get_db_data("sqlite_master", "name", "type='table'")
        table_names = [t['name'] for t in tables]
        
        expected_tables = ['users', 'reports', 'fertilizers', 'water_analyses', 
                          'calculations', 'recipes', 'optimization_logs']
        
        for table in expected_tables:
            if table in table_names:
                print_success(f"جدول {table} وجود دارد")
            else:
                print_warning(f"جدول {table} وجود ندارد")
        
        print_info(f"📊 تعداد کل جداول: {len(table_names)}")
        return True
    
    # ============================================================
    # تست 3: ثبت‌نام کاربر
    # ============================================================
    
    def test_register(self) -> bool:
        """تست ثبت‌نام کاربر جدید"""
        print_subheader("3. تست ثبت‌نام کاربر جدید")
        
        data = {
            "first_name": self.test_first_name,
            "last_name": self.test_last_name,
            "phone_number": self.test_phone,
            "password": self.test_password
        }
        
        print_info(f"📝 ثبت‌نام با شماره: {self.test_phone}")
        
        result = self._request("POST", "/auth/register", data)
        
        if self._assert_success(result, "ثبت‌نام کاربر"):
            user_data = result.get("data", {})
            self.user_id = user_data.get("id")
            print_info(f"👤 کاربر با ID {self.user_id} ثبت شد")
            print_info(f"   نام: {user_data.get('first_name')} {user_data.get('last_name')}")
            print_info(f"   تلفن: {user_data.get('phone_number')}")
            return True
        
        # اگر کاربر قبلاً ثبت شده بود
        if result.get("status_code") == 400:
            error_detail = result.get("data", {}).get("detail", "")
            if "قبلاً ثبت شده" in error_detail or "already registered" in error_detail:
                print_warning("کاربر قبلاً ثبت شده است - تلاش برای ورود")
                return self.test_login()
        
        return False
    
    # ============================================================
    # تست 4: ورود به سیستم
    # ============================================================
    
    def test_login(self) -> bool:
        """تست ورود به سیستم"""
        print_subheader("4. تست ورود به سیستم")
        
        data = {
            "phone_number": self.test_phone,
            "password": self.test_password
        }
        
        print_info(f"🔐 ورود با شماره: {self.test_phone}")
        
        result = self._request("POST", "/auth/login", data)
        
        if self._assert_success(result, "ورود به سیستم"):
            token_data = result.get("data", {})
            self.token = token_data.get("access_token")
            print_info(f"🔑 توکن دریافت شد: {self.token[:30]}...")
            print_info(f"⏱️ زمان انقضا: {token_data.get('expires_in')} ثانیه")
            
            # دریافت اطلاعات کاربر
            return self.test_get_me()
        
        return False
    
    # ============================================================
    # تست 5: دریافت اطلاعات کاربر
    # ============================================================
    
    def test_get_me(self) -> bool:
        """تست دریافت اطلاعات کاربر فعلی"""
        print_subheader("5. تست دریافت اطلاعات کاربر فعلی")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/auth/me")
        
        if self._assert_success(result, "دریافت اطلاعات کاربر"):
            user_data = result.get("data", {})
            self.user_id = user_data.get("id")
            print_info(f"👤 کاربر: {user_data.get('full_name')}")
            print_info(f"📱 تلفن: {user_data.get('phone_number')}")
            return True
        
        return False
    
    # ============================================================
    # تست 6: دریافت کودهای سیستمی
    # ============================================================
    
    def test_get_system_fertilizers(self) -> bool:
        """تست دریافت کودهای سیستمی"""
        print_subheader("6. تست دریافت کودهای سیستمی")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/fertilizers/system")
        
        if self._assert_success(result, "دریافت کودهای سیستمی"):
            ferts = result.get("data", [])
            print_info(f"📊 تعداد کودهای سیستمی: {len(ferts)}")
            if ferts:
                print_info(f"   نمونه: {ferts[0].get('name')} (ID: {ferts[0].get('id')})")
            return True
        
        return False
    
    # ============================================================
    # تست 7: ایجاد کود شخصی
    # ============================================================
    
    def test_create_fertilizer(self, name: str, price: float, 
                                elements: Dict) -> Optional[int]:
        """تست ایجاد کود جدید"""
        print_subheader(f"7. ایجاد کود: {name}")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return None
        
        data = {
            "name": name,
            "price_per_kg": price,
            "elements": elements
        }
        
        print_info(f"📦 ایجاد کود: {name} - {price:,} تومان")
        print_info(f"   عناصر: {json.dumps(elements, ensure_ascii=False)}")
        
        result = self._request("POST", "/fertilizers", data)
        
        if self._assert_success(result, f"ایجاد کود {name}"):
            fert_data = result.get("data", {})
            fert_id = fert_data.get("id")
            self.fertilizer_ids.append(fert_id)
            print_info(f"✅ کود با ID {fert_id} ایجاد شد")
            return fert_id
        
        return None
    
    def test_create_multiple_fertilizers(self) -> bool:
        """تست ایجاد چندین کود مختلف"""
        print_subheader("7. ایجاد چندین کود مختلف")
        
        fertilizers = [
            {
                "name": "نیترات کلسیم (Ca(NO3)2.4H2O)",
                "price": 550000,
                "elements": {"N-NO3": 11.861, "Ca": 16.963}
            },
            {
                "name": "نیترات آمونیوم (NH4NO3)",
                "price": 500000,
                "elements": {"N-NO3": 17.499, "N-NH4": 17.499}
            },
            {
                "name": "کلرید آمونیوم (NH4Cl)",
                "price": 350000,
                "elements": {"N-NH4": 26.185, "Cl": 66.275}
            },
            {
                "name": "مونو آمونیوم فسفات (NH4H2PO4)",
                "price": 750000,
                "elements": {"N-NH4": 12.178, "P": 26.930}
            },
            {
                "name": "کربنات پتاسیم (K2CO3)",
                "price": 800000,
                "elements": {"K": 56.579}
            },
            {
                "name": "نیترات منیزیم (Mg(NO3)2.6H2O)",
                "price": 480000,
                "elements": {"N-NO3": 10.922, "Mg": 9.464}
            },
            {
                "name": "سولفات آهن (FeSO4.7H2O)",
                "price": 500000,
                "elements": {"Fe": 20.086, "S": 11.528}
            },
            {
                "name": "سولفات روی مونوهیدرات (ZnSO4.H2O)",
                "price": 600000,
                "elements": {"Zn": 36.436, "S": 17.878}
            },
            {
                "name": "کلات منگنز EDTA (Mn-EDTA 13%)",
                "price": 1850000,
                "elements": {"Mn": 13.694}
            },
            {
                "name": "نیترات مس (Cu(NO3)2.3H2O)",
                "price": 750000,
                "elements": {"Cu": 26.228, "N-NO3": 11.565}
            },
            {
                "name": "اسید بوریک (H3BO3)",
                "price": 1200000,
                "elements": {"B": 17.480}
            },
            {
                "name": "مولیبدات سدیم (Na2MoO4.2H2O)",
                "price": 2800000,
                "elements": {"Mo": 39.650, "Na": 19.001}
            },
            {
                "name": "اسید سولفوریک 98% (H2SO4)",
                "price": 1500000,
                "elements": {"S": 31.997},
                "is_acid": True,
                "acid_type": "H2SO4"
            }
        ]
        
        success_count = 0
        for fert in fertilizers:
            data = {
                "name": fert["name"],
                "price_per_kg": fert["price"],
                "elements": fert["elements"]
            }
            
            if fert.get("is_acid"):
                data["is_acid"] = True
                data["acid_type"] = fert.get("acid_type")
            
            result = self._request("POST", "/fertilizers", data)
            
            if result.get("success", False):
                fert_data = result.get("data", {})
                self.fertilizer_ids.append(fert_data.get("id"))
                success_count += 1
                print_success(f"  ✅ {fert['name']} ایجاد شد (ID: {fert_data.get('id')})")
            else:
                print_error(f"  ❌ {fert['name']} ایجاد نشد")
                print_error(f"     خطا: {result.get('data', {}).get('detail', 'Unknown error')}")
        
        print_info(f"✅ {success_count}/{len(fertilizers)} کود با موفقیت ایجاد شد")
        return success_count > 0
    
    # ============================================================
    # تست 8: دریافت لیست کودها
    # ============================================================
    
    def test_get_fertilizers(self) -> bool:
        """تست دریافت لیست کودها"""
        print_subheader("8. تست دریافت لیست کودها")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/fertilizers")
        
        if self._assert_success(result, "دریافت لیست کودها"):
            ferts = result.get("data", [])
            print_info(f"📊 تعداد کل کودها: {len(ferts)}")
            for f in ferts[:5]:
                print_info(f"   - {f.get('name')} (ID: {f.get('id')})")
            if len(ferts) > 5:
                print_info(f"   ... و {len(ferts) - 5} کود دیگر")
            return True
        
        return False
    
    # ============================================================
    # تست 9: ایجاد گزارش
    # ============================================================
    
    def test_create_report(self) -> Optional[int]:
        """تست ایجاد گزارش جدید"""
        print_subheader("9. تست ایجاد گزارش جدید")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return None
        
        data = {
            "report_name": f"گزارش تست {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "plant_name": "توت فرنگی",
            "season": "بهار",
            "growth_stage": "رشد رویشی",
            "report_date": "۱۴۰۵/۰۴/۰۵"
        }
        
        print_info(f"📋 ایجاد گزارش: {data['report_name']}")
        
        result = self._request("POST", "/reports", data)
        
        if self._assert_success(result, "ایجاد گزارش"):
            report_data = result.get("data", {})
            self.report_id = report_data.get("id")
            print_info(f"✅ گزارش با ID {self.report_id} ایجاد شد")
            return self.report_id
        
        return None
    
    # ============================================================
    # تست 10: دریافت گزارش‌ها
    # ============================================================
    
    def test_get_reports(self) -> bool:
        """تست دریافت لیست گزارش‌ها"""
        print_subheader("10. تست دریافت لیست گزارش‌ها")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/reports")
        
        if self._assert_success(result, "دریافت لیست گزارش‌ها"):
            reports = result.get("data", [])
            print_info(f"📊 تعداد کل گزارش‌ها: {len(reports)}")
            for r in reports:
                print_info(f"   - {r.get('report_name')} (ID: {r.get('id')})")
            return True
        
        return False
    
    # ============================================================
    # تست 11: ایجاد آنالیز آب
    # ============================================================
    
    def test_create_water_analysis(self) -> bool:
        """تست ایجاد آنالیز آب"""
        print_subheader("11. تست ایجاد آنالیز آب")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        data = {
            "water_percentage": 80,
            "wastewater_percentage": 20,
            "water_salinity": 1.2,
            "wastewater_values": {
                "N-NO3": 25,
                "P": 8,
                "S": 12,
                "N-NH4": 3,
                "K": 18,
                "Ca": 35,
                "Fe": 0.8,
                "Mn": 0.2,
                "Zn": 0.1,
                "B": 0.05,
                "Cu": 0.02,
                "Mo": 0.01
            },
            "water_values": {
                "N-NO3": 5,
                "P": 1,
                "S": 3,
                "N-NH4": 0.5,
                "K": 4,
                "Ca": 10,
                "Fe": 0.1,
                "Mn": 0.02,
                "Zn": 0.01,
                "B": 0.005,
                "Cu": 0.002,
                "Mo": 0.001
            }
        }
        
        print_info(f"💧 ایجاد آنالیز آب برای گزارش {self.report_id}")
        
        result = self._request("POST", f"/water-analysis/{self.report_id}", data)
        
        if self._assert_success(result, "ایجاد آنالیز آب"):
            analysis_data = result.get("data", {})
            self.water_analysis_id = analysis_data.get("id")
            print_info(f"✅ آنالیز آب با ID {self.water_analysis_id} ایجاد شد")
            return True
        
        return False
    
    # ============================================================
    # تست 12: دریافت آنالیز آب
    # ============================================================
    
    def test_get_water_analysis(self) -> bool:
        """تست دریافت آنالیز آب"""
        print_subheader("12. تست دریافت آنالیز آب")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        result = self._request("GET", f"/water-analysis/{self.report_id}")
        
        if self._assert_success(result, "دریافت آنالیز آب"):
            analysis_data = result.get("data", {})
            print_info(f"💧 آنالیز آب:")
            print_info(f"   آب: {analysis_data.get('water_percentage')}%")
            print_info(f"   پساب: {analysis_data.get('wastewater_percentage')}%")
            print_info(f"   شوری: {analysis_data.get('water_salinity')}")
            
            # بررسی مقادیر عناصر
            water_values = analysis_data.get('water_values', {})
            if water_values:
                print_info(f"   عناصر آب: {len(water_values)} مورد")
            return True
        
        return False
    
    # ============================================================
    # تست 13: ایجاد عناصر هدف
    # ============================================================
    
    def test_create_targets(self) -> bool:
        """تست ایجاد عناصر هدف"""
        print_subheader("13. تست ایجاد عناصر هدف")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        data = {
            "target_values": {
                "N-NO3": 210,
                "P": 31,
                "S": 64,
                "N-NH4": 0,
                "K": 235,
                "Ca": 200,
                "Mg": 49,
                "Na": 0,
                "Cl": 10,
                "Fe": 2.9,
                "Mn": 0.5,
                "Zn": 0.05,
                "B": 0.5,
                "Cu": 0.02,
                "Mo": 0.05
            },
            "final_values": {},
            "reservoir_data": {},
            "calc_rows": []
        }
        
        print_info(f"🎯 ایجاد عناصر هدف برای گزارش {self.report_id}")
        
        result = self._request("POST", f"/calculations/{self.report_id}", data)
        
        if self._assert_success(result, "ایجاد عناصر هدف"):
            calc_data = result.get("data", {})
            self.calculation_id = calc_data.get("id")
            print_info(f"✅ عناصر هدف با ID {self.calculation_id} ایجاد شد")
            return True
        
        return False
    
    # ============================================================
    # 🆕 تست 14: بهینه‌سازی خودکار (هسته اصلی)
    # ============================================================
    
    def test_auto_optimization(self) -> bool:
        """تست بهینه‌سازی خودکار - قلب تپنده جدید FarmTech"""
        print_subheader("14. 🚀 تست بهینه‌سازی خودکار")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        # دریافت کودهای موجود
        ferts_result = self._request("GET", "/fertilizers")
        if not ferts_result.get("success", False):
            print_error("خطا در دریافت کودها")
            return False
        
        fertilizers = ferts_result.get("data", [])
        if not fertilizers:
            print_warning("هیچ کودی در سیستم وجود ندارد")
            return False
        
        # انتخاب چند کود برای بهینه‌سازی
        selected_fertilizers = fertilizers[:10]
        
        # آماده‌سازی داده‌ها
        target_values = {
            "N-NO3": 210,
            "P": 31,
            "K": 235,
            "Ca": 200,
            "Mg": 49,
            "S": 64,
            "Fe": 2.9,
            "Mn": 0.5,
            "Zn": 0.05,
            "B": 0.5,
            "Cu": 0.02,
            "Mo": 0.05,
            "Cl": 10
        }
        
        water_values = {
            "N-NO3": 5,
            "P": 1,
            "K": 4,
            "Ca": 10,
            "Mg": 2,
            "Fe": 0.1,
            "Mn": 0.02,
            "Zn": 0.01,
            "B": 0.005,
            "Cu": 0.002,
            "Mo": 0.001
        }
        
        # آماده‌سازی کودها برای ارسال
        ferts_for_optimization = []
        for f in selected_fertilizers:
            ferts_for_optimization.append({
                "id": str(f.get("id")),
                "name": f.get("name"),
                "elements": f.get("elements", {}),
                "price_per_kg": f.get("price_per_kg", 0),
                "purity": f.get("concentration", 100),
                "is_acid": f.get("is_acid", False),
                "is_system_default": f.get("is_system_default", False)
            })
        
        data = {
            "target_values": target_values,
            "water_values": water_values,
            "fertilizers": ferts_for_optimization,
            "options": {
                "method": "nnls",
                "use_precipitation_check": True,
                "use_ion_balance_check": True,
                "reservoir_mode": "auto",
                "max_iterations": 1000,
                "tolerance": 1e-6,
                "cost_weight": 0.01
            },
            "tank_volume": 5000,
            "stock_volume": 100,
            "injection_ratio": 100
        }
        
        print_info(f"🧮 ارسال درخواست بهینه‌سازی با {len(ferts_for_optimization)} کود")
        print_info(f"   عناصر هدف: {len(target_values)} مورد")
        
        start_time = time.time()
        result = self._request("POST", "/calculations/optimize", data)
        duration_ms = (time.time() - start_time) * 1000
        
        if self._assert_success(result, "بهینه‌سازی خودکار"):
            opt_data = result.get("data", {})
            self.optimization_result = opt_data
            
            print_info(f"⏱️ زمان محاسبه: {duration_ms:.0f}ms")
            print_info(f"💰 هزینه کل: {opt_data.get('cost_total', 0):,.0f} تومان")
            print_info(f"📊 خطای باقی‌مانده: {opt_data.get('residual_error', 0):.4f}")
            print_info(f"🔄 تعداد تکرار: {opt_data.get('iterations', 0)}")
            print_info(f"✅ همگرایی: {'موفق' if opt_data.get('is_converged', False) else 'ناموفق'}")
            
            # نمایش وزن‌ها
            weights = opt_data.get('weights', {})
            print_info(f"📦 وزن‌های بهینه ({len(weights)} کود):")
            for fert_id, weight in list(weights.items())[:5]:
                fert_name = next((f.get('name') for f in selected_fertilizers if str(f.get('id')) == fert_id), fert_id)
                print_info(f"   - {fert_name}: {weight:.3f} گرم")
            if len(weights) > 5:
                print_info(f"   ... و {len(weights) - 5} کود دیگر")
            
            # نمایش تعادل یونی
            ion_balance = opt_data.get('ion_balance', {})
            print_info(f"⚖️ تعادل یونی:")
            print_info(f"   کاتیون: {ion_balance.get('cation', 0):.2f} meq/L")
            print_info(f"   آنیون: {ion_balance.get('anion', 0):.2f} meq/L")
            print_info(f"   وضعیت: {'✅ متعادل' if ion_balance.get('is_balanced', False) else '⚠️ نامتعادل'}")
            
            # نمایش مخازن
            reservoir = opt_data.get('reservoir_data', {})
            print_info(f"🗄️ توزیع مخازن:")
            print_info(f"   مخزن A: {len(reservoir.get('A', []))} ماده")
            print_info(f"   مخزن B: {len(reservoir.get('B', []))} ماده")
            print_info(f"   مخزن C: {len(reservoir.get('C', []))} ماده")
            
            # نمایش هشدارها
            warnings = opt_data.get('warnings', [])
            if warnings:
                print_warning(f"⚠️ هشدارها ({len(warnings)}):")
                for w in warnings[:3]:
                    print_warning(f"   - {w}")
                if len(warnings) > 3:
                    print_warning(f"   ... و {len(warnings) - 3} هشدار دیگر")
            
            # نمایش پیشنهادات
            suggestions = opt_data.get('suggestions', [])
            if suggestions:
                print_info(f"💡 پیشنهادات ({len(suggestions)}):")
                for s in suggestions[:3]:
                    print_info(f"   - {s}")
                if len(suggestions) > 3:
                    print_info(f"   ... و {len(suggestions) - 3} پیشنهاد دیگر")
            
            return True
        
        return False
    
    # ============================================================
    # تست 15: دریافت خلاصه خانه
    # ============================================================
    
    def test_home_summary(self) -> bool:
        """تست دریافت خلاصه خانه"""
        print_subheader("15. تست دریافت خلاصه خانه")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/calculations/home-summary")
        
        if self._assert_success(result, "دریافت خلاصه خانه"):
            summary = result.get("data", {})
            print_info(f"📊 خلاصه خانه:")
            print_info(f"   داده وجود دارد: {summary.get('has_data', False)}")
            
            if summary.get('has_data'):
                ion_balance = summary.get('ion_balance', {})
                print_info(f"   تعادل یونی: {ion_balance.get('message', 'N/A')}")
                print_info(f"   عناصر فعال: {summary.get('active_elements_count', 0)}/{summary.get('total_elements', 0)}")
                print_info(f"   مخازن فعال: {summary.get('active_reservoirs_count', 0)}/3")
                print_info(f"   هزینه کل: {summary.get('total_cost', 0):,.0f} تومان")
                print_info(f"   توصیه‌ها: {len(summary.get('recommendations', []))} مورد")
            
            return True
        
        return False
    
    # ============================================================
    # تست 16: تولید تفسیر
    # ============================================================
    
    def test_interpretation(self) -> bool:
        """تست تولید تفسیر"""
        print_subheader("16. تست تولید تفسیر")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        result = self._request("POST", f"/calculations/{self.report_id}/calculate")
        
        if self._assert_success(result, "تولید تفسیر"):
            interp_data = result.get("data", {})
            print_info(f"📊 تفسیر:")
            print_info(f"   تعادل یونی: {interp_data.get('ion_balance', {}).get('message', 'N/A')}")
            print_info(f"   تعداد عناصر: {len(interp_data.get('element_status', []))}")
            print_info(f"   توصیه‌ها: {len(interp_data.get('fertilizer_recommendation', []))}")
            
            summary = interp_data.get('summary', '')
            if summary:
                print_info(f"   خلاصه:\n{summary[:200]}...")
            return True
        
        return False
    
    # ============================================================
    # تست 17: حذف گزارش (پاک‌سازی)
    # ============================================================
    
    def test_delete_report(self) -> bool:
        """تست حذف گزارش (پاک‌سازی)"""
        print_subheader("17. تست حذف گزارش (پاک‌سازی)")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_warning("شناسه گزارش وجود ندارد - پاک‌سازی انجام نشد")
            return True
        
        result = self._request("DELETE", f"/reports/{self.report_id}")
        
        if self._assert_success(result, f"حذف گزارش {self.report_id}"):
            print_info(f"🗑️ گزارش با ID {self.report_id} حذف شد")
            self.report_id = None
            return True
        
        return False
    
    # ============================================================
    # تست 18: خروج از سیستم
    # ============================================================
    
    def test_logout(self) -> bool:
        """تست خروج از سیستم"""
        print_subheader("18. تست خروج از سیستم")
        
        if not self.token:
            print_warning("توکن وجود ندارد - خروج انجام نشد")
            return True
        
        result = self._request("POST", "/auth/logout")
        
        if self._assert_success(result, "خروج از سیستم"):
            print_info("👋 خروج با موفقیت انجام شد")
            self.token = None
            return True
        
        return False
    
    # ============================================================
    # تست 19: بررسی داده‌های دیتابیس
    # ============================================================
    
    def test_database_data_integrity(self) -> bool:
        """تست یکپارچگی داده‌های دیتابیس"""
        print_subheader("19. تست یکپارچگی داده‌های دیتابیس")
        
        try:
            # بررسی کاربران
            users = self._get_db_data("users")
            print_info(f"👤 تعداد کاربران: {len(users)}")
            
            # بررسی کودها
            fertilizers = self._get_db_data("fertilizers")
            print_info(f"🧪 تعداد کودها: {len(fertilizers)}")
            
            # بررسی گزارش‌ها
            reports = self._get_db_data("reports")
            print_info(f"📋 تعداد گزارش‌ها: {len(reports)}")
            
            # بررسی آنالیز آب
            water_analyses = self._get_db_data("water_analyses")
            print_info(f"💧 تعداد آنالیز آب: {len(water_analyses)}")
            
            # بررسی محاسبات
            calculations = self._get_db_data("calculations")
            print_info(f"🧮 تعداد محاسبات: {len(calculations)}")
            
            # بررسی رسپی‌ها
            recipes = self._get_db_data("recipes")
            print_info(f"📝 تعداد رسپی‌ها: {len(recipes)}")
            
            # بررسی تاریخچه بهینه‌سازی
            optimization_logs = self._get_db_data("optimization_logs")
            print_info(f"🚀 تعداد تاریخچه بهینه‌سازی: {len(optimization_logs)}")
            
            print_success("✅ یکپارچگی داده‌ها تأیید شد")
            return True
            
        except Exception as e:
            print_error(f"خطا در بررسی داده‌ها: {e}")
            return False
    
    # ============================================================
    # اجرای همه تست‌ها
    # ============================================================
    
    def run_all_tests(self) -> bool:
        """اجرای همه تست‌ها به ترتیب"""
        print_header("🚀 شروع تست کامل FarmTech-ProFertilizer")
        print_info(f"📱 شماره تلفن تست: {self.test_phone}")
        print_info(f"🔑 رمز عبور: {self.test_password}")
        print_info(f"📍 آدرس API: {self.api_url}")
        print_info(f"🗄️ دیتابیس: {DB_PATH}")
        print("")

        # لیست تست‌ها با توضیحات
        tests = [
            ("سلامت سرور", self.test_health),
            ("اتصال دیتابیس", self.test_database),
            ("ثبت‌نام کاربر", self.test_register),
            ("ورود به سیستم", self.test_login),
            ("اطلاعات کاربر", self.test_get_me),
            ("کودهای سیستمی", self.test_get_system_fertilizers),
            ("ایجاد کودهای متعدد", self.test_create_multiple_fertilizers),
            ("دریافت لیست کودها", self.test_get_fertilizers),
            ("ایجاد گزارش", self.test_create_report),
            ("دریافت گزارش‌ها", self.test_get_reports),
            ("ایجاد آنالیز آب", self.test_create_water_analysis),
            ("دریافت آنالیز آب", self.test_get_water_analysis),
            ("ایجاد عناصر هدف", self.test_create_targets),
            ("🚀 بهینه‌سازی خودکار", self.test_auto_optimization),
            ("خلاصه خانه", self.test_home_summary),
            ("تولید تفسیر", self.test_interpretation),
            ("یکپارچگی داده‌ها", self.test_database_data_integrity),
        ]

        # اجرای تست‌ها
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print_error(f"خطا در تست {test_name}: {e}")
                self.summary.failed += 1
                self.summary.total += 1
                self.summary.results.append(TestResult(
                    name=test_name,
                    passed=False,
                    message=str(e)
                ))

        # پاک‌سازی: حذف گزارش
        self.test_delete_report()

        # خروج از سیستم
        self.test_logout()

        # ===== گزارش نهایی =====
        self.print_final_report()

        return self.summary.failed == 0
    
    # ============================================================
    # گزارش نهایی
    # ============================================================
    
    def print_final_report(self):
        """چاپ گزارش نهایی"""
        print_header("📊 گزارش نهایی تست")
        
        results = self.summary
        
        print(f"\n{Colors.BOLD}آمار کلی:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅ موفق: {results.passed}{Colors.RESET}")
        print(f"  {Colors.RED}❌ ناموفق: {results.failed}{Colors.RESET}")
        print(f"  📊 مجموع: {results.total}")
        
        if results.total > 0:
            success_rate = (results.passed / results.total) * 100
            print(f"  📈 نرخ موفقیت: {success_rate:.1f}%")
        
        if results.results:
            failed_tests = [r for r in results.results if not r.passed]
            if failed_tests:
                print(f"\n{Colors.RED}تست‌های ناموفق:{Colors.RESET}")
                for i, test in enumerate(failed_tests, 1):
                    print(f"  {i}. {test.name}:")
                    print(f"     {test.message}")
        
        print("\n" + "="*70)
        
        if results.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 همه تست‌ها با موفقیت انجام شدند!{Colors.RESET}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️ برخی تست‌ها ناموفق بودند. لطفاً خطاها را بررسی کنید.{Colors.RESET}")
        
        print("="*70)
    
    def print_summary(self):
        """چاپ خلاصه تست"""
        print_header("📋 خلاصه تست")
        
        print(f"\n{Colors.BOLD}اطلاعات کاربر تست:{Colors.RESET}")
        print(f"  📱 شماره تلفن: {self.test_phone}")
        print(f"  🔑 رمز عبور: {self.test_password}")
        print(f"  👤 نام: {self.test_first_name} {self.test_last_name}")
        
        print(f"\n{Colors.BOLD}داده‌های ایجاد شده:{Colors.RESET}")
        print(f"  📦 تعداد کودها: {len(self.fertilizer_ids)}")
        print(f"  📋 شناسه گزارش: {self.report_id}")
        print(f"  💧 شناسه آنالیز آب: {self.water_analysis_id}")
        print(f"  🧮 شناسه محاسبات: {self.calculation_id}")
        
        if self.optimization_result:
            print(f"\n{Colors.BOLD}نتیجه بهینه‌سازی:{Colors.RESET}")
            print(f"  💰 هزینه کل: {self.optimization_result.get('cost_total', 0):,.0f} تومان")
            print(f"  📊 خطای باقی‌مانده: {self.optimization_result.get('residual_error', 0):.4f}")
            print(f"  ✅ همگرایی: {'موفق' if self.optimization_result.get('is_converged', False) else 'ناموفق'}")


# ============================================================
# اجرای اصلی
# ============================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🧪 FarmTech-ProFertilizer - تست کامل سیستم               ║
    ║  📋 این تست تمام بخش‌های برنامه را بررسی می‌کند          ║
    ║  ⚠️  قبل از اجرا، مطمئن شوید بک‌اند در حال اجراست        ║
    ║  📍 دستور: cd backend && uvicorn app.main:app --reload   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    tester = FarmTechTester()
    
    try:
        success = tester.run_all_tests()
        tester.print_summary()
        
        if success:
            print(f"\n{Colors.GREEN}✅ همه تست‌ها با موفقیت انجام شد!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}❌ برخی تست‌ها ناموفق بودند.{Colors.RESET}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️ تست توسط کاربر متوقف شد.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطای غیرمنتظره: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)