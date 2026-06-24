#!/usr/bin/env python3
"""
FarmTech-ProFertilizer - Full API Test Suite
این فایل تمام APIهای برنامه را به صورت کامل تست می‌کند

نحوه اجرا:
    cd backend
    python tests/test_full_api.py

پیش‌نیازها:
    - بک‌اند در حال اجرا باشد (http://localhost:8000)
    - دیتابیس ساخته شده باشد
"""

import requests
import json
import random
import sys
import time
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# ===== تنظیمات =====
load_dotenv()

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"
HEALTH_URL = f"{BASE_URL}/health"

# ===== رنگ‌ها برای خروجی زیبا =====
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    WHITE = '\033[97m'

def print_success(msg): 
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg): 
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_info(msg): 
    print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")

def print_warning(msg): 
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")

def print_subheader(msg):
    print(f"\n{Colors.BOLD}{Colors.PURPLE}--- {msg} ---{Colors.RESET}")

def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

# ============================================================
# کلاس تستر اصلی
# ============================================================

class FarmTechTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_url = API_URL
        self.token = None
        self.user_id = None
        self.report_id = None
        self.fertilizer_ids = []
        self.water_analysis_id = None
        self.calculation_id = None
        self.test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        # داده‌های تست
        self.test_phone = f"0912{random.randint(1000000, 9999999)}"
        self.test_password = "Test@123456"
        self.test_first_name = "تست"
        self.test_last_name = "سیستم"
        
        print_info(f"📱 شماره تلفن تست: {self.test_phone}")
        print_info(f"🔑 رمز عبور: {self.test_password}")

    # ============================================================
    # توابع کمکی
    # ============================================================

    def _request(self, method: str, endpoint: str, data: Any = None, headers: Dict = None) -> Dict:
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
            
            # تلاش برای تبدیل به JSON
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
        self.test_results["total"] += 1
        
        if result.get("success", False):
            self.test_results["passed"] += 1
            print_success(f"{test_name}: موفق (Status: {result.get('status_code')})")
            return True
        else:
            self.test_results["failed"] += 1
            error_msg = result.get("data", {}).get("error", "Unknown error")
            if isinstance(error_msg, dict):
                error_msg = json.dumps(error_msg, ensure_ascii=False)
            print_error(f"{test_name}: ناموفق (Status: {result.get('status_code')})")
            print_error(f"  خطا: {error_msg}")
            self.test_results["errors"].append({
                "test": test_name,
                "status": result.get("status_code"),
                "error": error_msg
            })
            return False

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
    # تست 2: ثبت‌نام کاربر جدید
    # ============================================================

    def test_register(self) -> bool:
        """تست ثبت‌نام کاربر جدید"""
        print_subheader("2. تست ثبت‌نام کاربر جدید")
        
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
        
        # اگر کاربر قبلاً ثبت شده بود، خطا را نادیده بگیر
        if result.get("status_code") == 400:
            error_detail = result.get("data", {}).get("detail", "")
            if "قبلاً ثبت شده" in error_detail or "already registered" in error_detail:
                print_warning("کاربر قبلاً ثبت شده است - ادامه تست")
                # تلاش برای ورود
                return self.test_login()
        
        return False

    # ============================================================
    # تست 3: ورود به سیستم
    # ============================================================

    def test_login(self) -> bool:
        """تست ورود به سیستم"""
        print_subheader("3. تست ورود به سیستم")
        
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
            print_info(f"⏱️  زمان انقضا: {token_data.get('expires_in')} ثانیه")
            return True
        
        return False

    # ============================================================
    # تست 4: دریافت اطلاعات کاربر فعلی
    # ============================================================

    def test_get_me(self) -> bool:
        """تست دریافت اطلاعات کاربر فعلی"""
        print_subheader("4. تست دریافت اطلاعات کاربر فعلی")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/auth/me")
        
        if self._assert_success(result, "دریافت اطلاعات کاربر"):
            user_data = result.get("data", {})
            print_info(f"👤 کاربر: {user_data.get('full_name')}")
            print_info(f"📱 تلفن: {user_data.get('phone_number')}")
            return True
        
        return False

    # ============================================================
    # تست 5: ایجاد کود
    # ============================================================

    def test_create_fertilizer(self, name: str, price: float, elements: Dict) -> Optional[str]:
        """تست ایجاد کود جدید"""
        print_subheader(f"5. ایجاد کود: {name}")
        
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
        print_subheader("5. ایجاد چندین کود مختلف")
        
        fertilizers = [
            {
                "name": "نیترات کلسیم",
                "price": 25000,
                "elements": {"N-NO3": 15.5, "Ca": 19}
            },
            {
                "name": "پتاسیم نیترات",
                "price": 32000,
                "elements": {"N-NO3": 13, "K": 38}
            },
            {
                "name": "فسفات پتاسیم",
                "price": 28000,
                "elements": {"P": 22, "K": 28}
            },
            {
                "name": "سولفات منیزیم",
                "price": 15000,
                "elements": {"S": 13, "Mg": 10}
            },
            {
                "name": "سولفات پتاسیم",
                "price": 18000,
                "elements": {"S": 17, "K": 41}
            },
            {
                "name": "نیترات آمونیوم",
                "price": 22000,
                "elements": {"N-NO3": 17, "N-NH4": 17}
            },
            {
                "name": "اسید فسفریک (H3PO4)",
                "price": 45000,
                "elements": {"P": 32},
                "is_acid": True,
                "acid_type": "H3PO4"
            },
            {
                "name": "اسید نیتریک (HNO3)",
                "price": 38000,
                "elements": {"N-NO3": 38},
                "is_acid": True,
                "acid_type": "HNO3"
            }
        ]
        
        success_count = 0
        for fert in fertilizers:
            # آماده‌سازی داده
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
    # تست 6: دریافت لیست کودها
    # ============================================================

    def test_get_fertilizers(self) -> bool:
        """تست دریافت لیست کودها"""
        print_subheader("6. تست دریافت لیست کودها")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        result = self._request("GET", "/fertilizers")
        
        if self._assert_success(result, "دریافت لیست کودها"):
            ferts = result.get("data", [])
            print_info(f"📊 تعداد کل کودها: {len(ferts)}")
            for f in ferts[:5]:  # نمایش 5 کود اول
                print_info(f"   - {f.get('name')} (ID: {f.get('id')})")
            if len(ferts) > 5:
                print_info(f"   ... و {len(ferts) - 5} کود دیگر")
            return True
        
        return False

    # ============================================================
    # تست 7: به‌روزرسانی کود
    # ============================================================

    def test_update_fertilizer(self, fert_id: str) -> bool:
        """تست به‌روزرسانی کود"""
        print_subheader(f"7. تست به‌روزرسانی کود (ID: {fert_id})")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not fert_id:
            print_error("شناسه کود معتبر نیست")
            return False
        
        data = {
            "name": f"{self.test_first_name} کود به‌روزرسانی شده",
            "price_per_kg": 99999
        }
        
        print_info(f"📝 به‌روزرسانی کود با ID: {fert_id}")
        print_info(f"   نام جدید: {data['name']}")
        print_info(f"   قیمت جدید: {data['price_per_kg']:,} تومان")
        
        result = self._request("PUT", f"/fertilizers/{fert_id}", data)
        
        if self._assert_success(result, f"به‌روزرسانی کود {fert_id}"):
            fert_data = result.get("data", {})
            print_info(f"✅ کود به‌روزرسانی شد: {fert_data.get('name')}")
            return True
        
        return False

    # ============================================================
    # تست 8: حذف کود
    # ============================================================

    def test_delete_fertilizer(self, fert_id: str) -> bool:
        """تست حذف کود"""
        print_subheader(f"8. تست حذف کود (ID: {fert_id})")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not fert_id:
            print_error("شناسه کود معتبر نیست")
            return False
        
        result = self._request("DELETE", f"/fertilizers/{fert_id}")
        
        if self._assert_success(result, f"حذف کود {fert_id}"):
            print_info(f"🗑️ کود با ID {fert_id} حذف شد")
            # حذف از لیست
            if fert_id in self.fertilizer_ids:
                self.fertilizer_ids.remove(fert_id)
            return True
        
        return False

    # ============================================================
    # تست 9: ایجاد گزارش
    # ============================================================

    def test_create_report(self) -> Optional[str]:
        """تست ایجاد گزارش جدید"""
        print_subheader("9. تست ایجاد گزارش جدید")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return None
        
        data = {
            "report_name": f"گزارش تست {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "plant_name": "گوجه فرنگی",
            "season": "بهار",
            "growth_stage": "گلدهی",
            "report_date": datetime.now().strftime("%Y/%m/%d")
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
        print_info(f"   آب: {data['water_percentage']}% - پساب: {data['wastewater_percentage']}%")
        
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
            return True
        
        return False

    # ============================================================
    # تست 13: ایجاد محاسبات
    # ============================================================

    def test_create_calculation(self) -> bool:
        """تست ایجاد محاسبات"""
        print_subheader("13. تست ایجاد محاسبات")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        data = {
            "target_values": {
                "N-NO3": 150,
                "P": 40,
                "S": 60,
                "N-NH4": 10,
                "K": 200,
                "Ca": 180,
                "Mg": 50,
                "Fe": 2.5,
                "Mn": 0.5,
                "Zn": 0.3,
                "B": 0.2,
                "Cu": 0.05,
                "Mo": 0.02
            },
            "final_values": {
                "N-NO3": 145,
                "P": 38,
                "S": 58,
                "N-NH4": 9,
                "K": 195,
                "Ca": 175,
                "Mg": 48,
                "Fe": 2.3,
                "Mn": 0.45,
                "Zn": 0.28,
                "B": 0.18,
                "Cu": 0.045,
                "Mo": 0.018
            },
            "reservoir_data": {
                "A": [
                    {"name": "Ca(NO3)2", "amount": 25.5},
                    {"name": "KNO3", "amount": 15.2}
                ],
                "B": [
                    {"name": "KH2PO4", "amount": 8.3},
                    {"name": "MgSO4", "amount": 12.5}
                ],
                "C": [
                    {"name": "H3PO4", "amount": 2.0},
                    {"name": "HNO3", "amount": 1.5}
                ]
            },
            "calc_rows": [
                {
                    "material_name": "Ca(NO3)2",
                    "weight": 25.5,
                    "purity": 99,
                    "cost": 25000,
                    "elements": {"N-NO3": 15.5, "Ca": 19}
                },
                {
                    "material_name": "KNO3",
                    "weight": 15.2,
                    "purity": 99,
                    "cost": 32000,
                    "elements": {"N-NO3": 13, "K": 38}
                }
            ]
        }
        
        print_info(f"🧮 ایجاد محاسبات برای گزارش {self.report_id}")
        
        result = self._request("POST", f"/calculations/{self.report_id}", data)
        
        if self._assert_success(result, "ایجاد محاسبات"):
            calc_data = result.get("data", {})
            self.calculation_id = calc_data.get("id")
            print_info(f"✅ محاسبات با ID {self.calculation_id} ایجاد شد")
            return True
        
        return False

    # ============================================================
    # تست 14: دریافت محاسبات
    # ============================================================

    def test_get_calculation(self) -> bool:
        """تست دریافت محاسبات"""
        print_subheader("14. تست دریافت محاسبات")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        result = self._request("GET", f"/calculations/{self.report_id}")
        
        if self._assert_success(result, "دریافت محاسبات"):
            calc_data = result.get("data", {})
            print_info(f"🧮 محاسبات:")
            print_info(f"   هدف‌ها: {len(calc_data.get('target_values', {}))} عنصر")
            print_info(f"   نهایی: {len(calc_data.get('final_values', {}))} عنصر")
            print_info(f"   مخازن: {len(calc_data.get('reservoir_data', {}))} مخزن")
            return True
        
        return False

    # ============================================================
    # تست 15: تولید تفسیر
    # ============================================================

    def test_interpretation(self) -> bool:
        """تست تولید تفسیر"""
        print_subheader("15. تست تولید تفسیر")
        
        if not self.token:
            print_error("توکن وجود ندارد")
            return False
        
        if not self.report_id:
            print_error("شناسه گزارش وجود ندارد")
            return False
        
        print_info(f"📊 تولید تفسیر برای گزارش {self.report_id}")
        
        result = self._request("POST", f"/calculations/{self.report_id}/calculate")
        
        if self._assert_success(result, "تولید تفسیر"):
            interp_data = result.get("data", {})
            print_info(f"📊 تفسیر:")
            print_info(f"   تعادل یونی: {interp_data.get('ion_balance', {}).get('message', 'N/A')}")
            print_info(f"   تعداد عناصر: {len(interp_data.get('element_status', []))}")
            print_info(f"   توصیه‌ها: {len(interp_data.get('fertilizer_recommendation', []))}")
            
            # نمایش خلاصه
            summary = interp_data.get('summary', '')
            if summary:
                print_info(f"   خلاصه:\n{summary}")
            return True
        
        return False

    # ============================================================
    # تست 16: حذف گزارش (پاک‌سازی)
    # ============================================================

    def test_delete_report(self) -> bool:
        """تست حذف گزارش (پاک‌سازی)"""
        print_subheader("16. تست حذف گزارش (پاک‌سازی)")
        
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
    # تست 17: خروج از سیستم
    # ============================================================

    def test_logout(self) -> bool:
        """تست خروج از سیستم"""
        print_subheader("17. تست خروج از سیستم")
        
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
    # اجرای همه تست‌ها
    # ============================================================

    def run_all_tests(self) -> bool:
        """اجرای همه تست‌ها به ترتیب"""
        print_header("🚀 شروع تست کامل FarmTech-ProFertilizer")
        print_info(f"📱 شماره تلفن تست: {self.test_phone}")
        print_info(f"🔑 رمز عبور: {self.test_password}")
        print_info(f"📍 آدرس API: {self.api_url}")
        print("")

        # لیست تست‌ها با توضیحات
        tests = [
            ("سلامت سرور", self.test_health),
            ("ثبت‌نام کاربر", self.test_register),
            ("ورود به سیستم", self.test_login),
            ("اطلاعات کاربر", self.test_get_me),
            ("ایجاد کودها", self.test_create_multiple_fertilizers),
            ("دریافت لیست کودها", self.test_get_fertilizers),
            ("به‌روزرسانی کود", lambda: self.test_update_fertilizer(self.fertilizer_ids[0] if self.fertilizer_ids else None)),
            ("ایجاد گزارش", self.test_create_report),
            ("دریافت گزارش‌ها", self.test_get_reports),
            ("ایجاد آنالیز آب", self.test_create_water_analysis),
            ("دریافت آنالیز آب", self.test_get_water_analysis),
            ("ایجاد محاسبات", self.test_create_calculation),
            ("دریافت محاسبات", self.test_get_calculation),
            ("تولید تفسیر", self.test_interpretation),
        ]

        # اجرای تست‌ها
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print_error(f"خطا در تست {test_name}: {e}")
                self.test_results["failed"] += 1
                self.test_results["total"] += 1
                self.test_results["errors"].append({
                    "test": test_name,
                    "error": str(e)
                })

        # پاک‌سازی: حذف گزارش
        self.test_delete_report()

        # خروج از سیستم
        self.test_logout()

        # ===== گزارش نهایی =====
        self.print_final_report()

        return self.test_results["failed"] == 0

    def print_final_report(self):
        """چاپ گزارش نهایی"""
        print_header("📊 گزارش نهایی تست")
        
        results = self.test_results
        
        print(f"\n{Colors.BOLD}آمار کلی:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅ موفق: {results['passed']}{Colors.RESET}")
        print(f"  {Colors.RED}❌ ناموفق: {results['failed']}{Colors.RESET}")
        print(f"  📊 مجموع: {results['total']}")
        
        if results['total'] > 0:
            success_rate = (results['passed'] / results['total']) * 100
            print(f"  📈 نرخ موفقیت: {success_rate:.1f}%")
        
        if results['errors']:
            print(f"\n{Colors.RED}خطاهای رخ داده:{Colors.RESET}")
            for i, error in enumerate(results['errors'], 1):
                print(f"  {i}. {error.get('test', 'Unknown')}:")
                print(f"     {error.get('error', 'Unknown error')}")
                if error.get('status'):
                    print(f"     Status: {error.get('status')}")
        
        print("\n" + "="*80)
        
        if results['failed'] == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 همه تست‌ها با موفقیت انجام شدند!{Colors.RESET}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️ برخی تست‌ها ناموفق بودند. لطفاً خطاها را بررسی کنید.{Colors.RESET}")
        
        print("="*80)

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


# ============================================================
# اجرای اصلی
# ============================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🌱 FarmTech-ProFertilizer - تست کامل API                  ║
    ║  📋 این تست تمام APIهای برنامه را بررسی می‌کند             ║
    ║  ⚠️  قبل از اجرا، مطمئن شوید بک‌اند در حال اجراست         ║
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
        print(f"\n\n{Colors.YELLOW}⏹️  تست توسط کاربر متوقف شد.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطای غیرمنتظره: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)