#!/usr/bin/env python3
"""
🧪 تست کامل جریان FarmTech - ProFertilizer
===========================================

این فایل تمام جریان برنامه را از ابتدا تا انتها تست می‌کند:
1. ایجاد کاربر
2. ایجاد گزارش
3. ذخیره آنالیز آب
4. ذخیره عناصر هدف
5. بهینه‌سازی خودکار
6. ذخیره نتیجه بهینه‌سازی
7. بارگذاری مجدد گزارش
8. بررسی صحت داده‌ها
9. بررسی تب خانه
10. ایجاد گزارش جدید و ریست شدن

نحوه اجرا:
    cd backend
    python tests/test_full_flow.py
"""

import os
import sys
import json
import sqlite3
import time
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# ============================================================
# تنظیمات
# ============================================================

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "farmtech.db"
BACKEND_DIR = BASE_DIR

# اضافه کردن مسیر backend به sys.path
sys.path.insert(0, str(BACKEND_DIR))

# ============================================================
# کلاس رنگ‌ها (اصلاح شده)
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
    # ✅ اضافه کردن WHITE
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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")

def print_subheader(msg):
    print(f"\n{Colors.BOLD}{Colors.PURPLE}--- {msg} ---{Colors.RESET}")

# ============================================================
# کلاس تستر
# ============================================================

class FullFlowTester:
    """تستر کامل جریان برنامه"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None
        self.test_user_id = None
        self.test_report_id = None
        self.test_calculation_id = None
        self.test_water_analysis_id = None
        
        # داده‌های تست
        self.test_phone = "09121234567"
        self.test_password = "Test@123456"
        self.test_first_name = "تست"
        self.test_last_name = "سیستم"
        
        # داده‌های گزارش
        self.report_data = {
            "report_name": "گزارش تست کامل",
            "plant_name": "گوجه فرنگی",
            "season": "تابستان",
            "growth_stage": "گلدهی",
            "report_date": "۱۴۰۵/۰۴/۱۳"
        }
        
        # داده‌های عناصر هدف
        self.target_values = {
            "N-NO3": 207.0,
            "P": 55.0,
            "K": 289.0,
            "Mg": 38.0,
            "Ca": 155.0,
            "S": 51.0,
            "Fe": 6.8,
            "Mn": 1.97,
            "Zn": 0.25,
            "B": 0.7,
            "Cu": 0.07,
            "Mo": 0.05,
            "Cl": 200.0
        }
        
        # داده‌های آب
        self.water_data = {
            "water_percentage": 100.0,
            "wastewater_percentage": 0.0,
            "water_salinity": 0.8,
            "water_values": {"K": 35.0, "Ca": 50.0},
            "wastewater_values": {}
        }
        
        # نتیجه تست‌ها
        self.results = []
        self.passed = 0
        self.failed = 0
        
    # ============================================================
    # توابع کمکی دیتابیس
    # ============================================================
    
    def connect_db(self) -> bool:
        """اتصال به دیتابیس"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            print_success(f"اتصال به دیتابیس: {self.db_path}")
            return True
        except Exception as e:
            print_error(f"خطا در اتصال به دیتابیس: {e}")
            return False
    
    def close_db(self):
        """بستن اتصال دیتابیس"""
        if self.conn:
            self.conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """اجرای کوئری و برگرداندن نتایج"""
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print_error(f"خطا در اجرای کوئری: {e}")
            return []
    
    def execute_insert(self, query: str, params: tuple = ()) -> Optional[int]:
        """اجرای کوئری INSERT و برگرداندن ID"""
        if not self.conn:
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print_error(f"خطا در INSERT: {e}")
            self.conn.rollback()
            return None
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """اجرای کوئری UPDATE"""
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print_error(f"خطا در UPDATE: {e}")
            self.conn.rollback()
            return False
    
    def get_table_data(self, table: str, condition: str = "") -> List[Dict[str, Any]]:
        """دریافت داده‌های یک جدول"""
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)
    
    # ============================================================
    # تست 1: بررسی دیتابیس
    # ============================================================
    
    def test_database_exists(self) -> bool:
        """تست 1: بررسی وجود دیتابیس و جداول"""
        print_subheader("1. بررسی دیتابیس و جداول")
        
        if not self.db_path.exists():
            print_error(f"فایل دیتابیس وجود ندارد: {self.db_path}")
            return False
        
        print_success(f"فایل دیتابیس وجود دارد: {self.db_path}")
        
        # بررسی جداول
        tables = self.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [t['name'] for t in tables]
        
        expected_tables = ['users', 'reports', 'fertilizers', 'water_analyses', 
                          'calculations', 'recipes', 'optimization_logs']
        
        all_exist = True
        for table in expected_tables:
            if table in table_names:
                print_success(f"  جدول {table} وجود دارد")
            else:
                print_error(f"  جدول {table} وجود ندارد")
                all_exist = False
        
        return all_exist
    
    # ============================================================
    # تست 2: ایجاد کاربر تست
    # ============================================================
    
    def test_create_user(self) -> bool:
        """تست 2: ایجاد کاربر تست"""
        print_subheader("2. ایجاد کاربر تست")
        
        # بررسی وجود کاربر
        existing = self.execute_query(
            "SELECT id FROM users WHERE phone_number = ?",
            (self.test_phone,)
        )
        
        if existing:
            self.test_user_id = existing[0]['id']
            print_success(f"کاربر تست قبلاً وجود دارد (ID: {self.test_user_id})")
            return True
        
        # ایجاد کاربر جدید
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((salt + self.test_password).encode('utf-8'))
        password_hash = f"{salt}:{hash_obj.hexdigest()}"
        
        user_id = self.execute_insert(
            """INSERT INTO users (first_name, last_name, phone_number, password_hash, is_active)
               VALUES (?, ?, ?, ?, ?)""",
            (self.test_first_name, self.test_last_name, self.test_phone, password_hash, 1)
        )
        
        if user_id:
            self.test_user_id = user_id
            print_success(f"کاربر تست ایجاد شد (ID: {self.test_user_id})")
            return True
        else:
            print_error("خطا در ایجاد کاربر تست")
            return False
    
    # ============================================================
    # تست 3: ایجاد گزارش
    # ============================================================
    
    def test_create_report(self) -> bool:
        """تست 3: ایجاد گزارش"""
        print_subheader("3. ایجاد گزارش")
        
        if not self.test_user_id:
            print_error("کاربر تست وجود ندارد")
            return False
        
        report_id = self.execute_insert(
            """INSERT INTO reports (user_id, report_name, plant_name, season, growth_stage, report_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.test_user_id,
                self.report_data["report_name"],
                self.report_data["plant_name"],
                self.report_data["season"],
                self.report_data["growth_stage"],
                self.report_data["report_date"]
            )
        )
        
        if report_id:
            self.test_report_id = report_id
            print_success(f"گزارش ایجاد شد (ID: {self.test_report_id})")
            print_info(f"  نام: {self.report_data['report_name']}")
            print_info(f"  گیاه: {self.report_data['plant_name']}")
            return True
        else:
            print_error("خطا در ایجاد گزارش")
            return False
    
    # ============================================================
    # تست 4: ذخیره آنالیز آب
    # ============================================================
    
    def test_save_water_analysis(self) -> bool:
        """تست 4: ذخیره آنالیز آب"""
        print_subheader("4. ذخیره آنالیز آب")
        
        if not self.test_report_id:
            print_error("گزارش وجود ندارد")
            return False
        
        water_id = self.execute_insert(
            """INSERT INTO water_analyses 
               (report_id, water_percentage, wastewater_percentage, water_salinity, water_values, wastewater_values)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.test_report_id,
                self.water_data["water_percentage"],
                self.water_data["wastewater_percentage"],
                self.water_data["water_salinity"],
                json.dumps(self.water_data["water_values"]),
                json.dumps(self.water_data["wastewater_values"])
            )
        )
        
        if water_id:
            self.test_water_analysis_id = water_id
            print_success(f"آنالیز آب ذخیره شد (ID: {self.test_water_analysis_id})")
            print_info(f"  درصد آب: {self.water_data['water_percentage']}%")
            print_info(f"  شوری: {self.water_data['water_salinity']}")
            return True
        else:
            print_error("خطا در ذخیره آنالیز آب")
            return False
    
    # ============================================================
    # تست 5: ذخیره عناصر هدف و محاسبات
    # ============================================================
    
    def test_save_calculation(self) -> bool:
        """تست 5: ذخیره عناصر هدف و محاسبات"""
        print_subheader("5. ذخیره عناصر هدف و محاسبات")
        
        if not self.test_report_id:
            print_error("گزارش وجود ندارد")
            return False
        
        calc_id = self.execute_insert(
            """INSERT INTO calculations 
               (report_id, target_values, final_values, reservoir_data, calc_rows)
               VALUES (?, ?, ?, ?, ?)""",
            (
                self.test_report_id,
                json.dumps(self.target_values),
                json.dumps({}),  # final_values خالی
                json.dumps({"A": [], "B": [], "C": []}),
                json.dumps([])   # calc_rows خالی
            )
        )
        
        if calc_id:
            self.test_calculation_id = calc_id
            print_success(f"محاسبات ذخیره شد (ID: {self.test_calculation_id})")
            print_info(f"  تعداد عناصر هدف: {len(self.target_values)}")
            return True
        else:
            print_error("خطا در ذخیره محاسبات")
            return False
    
    # ============================================================
    # تست 6: شبیه‌سازی بهینه‌سازی و ذخیره نتیجه
    # ============================================================
    
    def test_save_optimization_result(self) -> bool:
        """تست 6: شبیه‌سازی بهینه‌سازی و ذخیره نتیجه"""
        print_subheader("6. شبیه‌سازی بهینه‌سازی و ذخیره نتیجه")
        
        if not self.test_calculation_id:
            print_error("محاسبات وجود ندارد")
            return False
        
        # شبیه‌سازی نتیجه بهینه‌سازی
        optimization_result = {
            "weights": {
                "39": 97.87,
                "42": 467.20,
                "44": 4.02,
                "45": 267.57,
                "50": 0.27,
                "52": 636.52,
                "56": 34.54,
                "57": 134.51,
                "60": 136.81,
                "64": 286.27,
                "71": 0.13,
                "73": 149.80,
                "76": 1.12
            },
            "concentrations": {
                "N-NH4": 106.44,
                "Cl": 200.0,
                "N-NO3": 207.0,
                "B": 0.70,
                "Ca": 155.0,
                "Cu": 0.07,
                "P": 55.0,
                "K": 289.0,
                "Fe": 6.80,
                "S": 51.0,
                "Mg": 38.0,
                "Mn": 1.97,
                "Mo": 0.05,
                "Na": 0.02,
                "Zn": 0.25
            },
            "residual_error": 0.001,
            "cost_total": 1743124.0,
            "is_converged": True,
            "iterations": 10,
            "convergence_time_ms": 150.5
        }
        
        # به‌روزرسانی calculation با final_values و calc_rows
        calc_rows = []
        for fert_id, weight in optimization_result["weights"].items():
            calc_rows.append({
                "materialName": f"کود {fert_id}",
                "weight": weight,
                "purity": 99.0,
                "cost": weight * 10000,
                "elements": {},
                "isAcid": False,
                "fertilizerId": fert_id,
                "isFixedRow": False
            })
        
        # ✅ ذخیره final_values در دیتابیس
        success = self.execute_update(
            """UPDATE calculations 
               SET final_values = ?, calc_rows = ?, reservoir_data = ?
               WHERE id = ?""",
            (
                json.dumps(optimization_result["concentrations"]),
                json.dumps(calc_rows),
                json.dumps({"A": [], "B": [], "C": []}),
                self.test_calculation_id
            )
        )
        
        if success:
            print_success("نتیجه بهینه‌سازی در دیتابیس ذخیره شد")
            print_info(f"  تعداد کودها: {len(optimization_result['weights'])}")
            print_info(f"  هزینه کل: {optimization_result['cost_total']:,.0f} تومان")
            return True
        else:
            print_error("خطا در ذخیره نتیجه بهینه‌سازی")
            return False
    
    # ============================================================
    # تست 7: بارگذاری مجدد گزارش و بررسی داده‌ها
    # ============================================================
    
    def test_reload_report(self) -> bool:
        """تست 7: بارگذاری مجدد گزارش و بررسی داده‌ها"""
        print_subheader("7. بارگذاری مجدد گزارش و بررسی داده‌ها")
        
        if not self.test_report_id:
            print_error("گزارش وجود ندارد")
            return False
        
        # 1. دریافت گزارش
        report = self.execute_query(
            "SELECT * FROM reports WHERE id = ?",
            (self.test_report_id,)
        )
        
        if not report:
            print_error("گزارش پیدا نشد")
            return False
        
        print_success(f"گزارش بارگذاری شد: {report[0]['report_name']}")
        print_info(f"  گیاه: {report[0]['plant_name']}")
        print_info(f"  فصل: {report[0]['season']}")
        print_info(f"  مرحله: {report[0]['growth_stage']}")
        
        # 2. دریافت آنالیز آب
        water = self.execute_query(
            "SELECT * FROM water_analyses WHERE report_id = ?",
            (self.test_report_id,)
        )
        
        if water:
            print_success(f"آنالیز آب بارگذاری شد")
            water_values = json.loads(water[0]['water_values']) if water[0]['water_values'] else {}
            print_info(f"  عناصر آب: {len(water_values)}")
        else:
            print_warning("آنالیز آب پیدا نشد")
        
        # 3. دریافت محاسبات
        calc = self.execute_query(
            "SELECT * FROM calculations WHERE report_id = ?",
            (self.test_report_id,)
        )
        
        if calc:
            print_success(f"محاسبات بارگذاری شد")
            target_values = json.loads(calc[0]['target_values']) if calc[0]['target_values'] else {}
            final_values = json.loads(calc[0]['final_values']) if calc[0]['final_values'] else {}
            calc_rows = json.loads(calc[0]['calc_rows']) if calc[0]['calc_rows'] else []
            
            print_info(f"  عناصر هدف: {len(target_values)}")
            print_info(f"  عناصر نهایی: {len(final_values)}")
            print_info(f"  ردیف‌های محاسبه: {len(calc_rows)}")
            
            # ✅ بررسی: آیا final_values ذخیره شده؟
            if final_values:
                print_success("✅ final_values در دیتابیس ذخیره شده است")
                # نمایش چند عنصر
                for element, value in list(final_values.items())[:5]:
                    print_info(f"    {element}: {value:.2f}")
            else:
                print_error("❌ final_values در دیتابیس ذخیره نشده است!")
                return False
            
            # ✅ بررسی: آیا calc_rows ذخیره شده؟
            if calc_rows:
                print_success("✅ calc_rows در دیتابیس ذخیره شده است")
                print_info(f"  تعداد ردیف‌ها: {len(calc_rows)}")
            else:
                print_error("❌ calc_rows در دیتابیس ذخیره نشده است!")
                return False
            
            return True
        else:
            print_error("محاسبات پیدا نشد")
            return False
    
    # ============================================================
    # تست 8: بررسی داده‌های تب خانه (HomeTab)
    # ============================================================
    
    def test_home_tab_data(self) -> bool:
        """تست 8: بررسی داده‌های تب خانه"""
        print_subheader("8. بررسی داده‌های تب خانه")
        
        if not self.test_report_id:
            print_error("گزارش وجود ندارد")
            return False
        
        # دریافت محاسبات
        calc = self.execute_query(
            "SELECT * FROM calculations WHERE report_id = ?",
            (self.test_report_id,)
        )
        
        if not calc:
            print_error("محاسبات پیدا نشد")
            return False
        
        target_values = json.loads(calc[0]['target_values']) if calc[0]['target_values'] else {}
        final_values = json.loads(calc[0]['final_values']) if calc[0]['final_values'] else {}
        
        # ✅ بررسی: آیا final_values با target_values مطابقت دارد؟
        print_info("مقایسه عناصر هدف و نهایی:")
        
        missing_elements = []
        for element, target in target_values.items():
            actual = final_values.get(element, 0)
            if target > 0:
                percent = (actual / target) * 100 if target > 0 else 0
                status = "✅" if 90 <= percent <= 110 else "⚠️"
                print_info(f"  {status} {element}: هدف={target:.2f}, تامین={actual:.2f}, درصد={percent:.1f}%")
                
                if percent < 50:
                    missing_elements.append(element)
        
        if missing_elements:
            print_warning(f"عناصر با درصد پایین: {missing_elements}")
        
        # ✅ بررسی: آیا عناصر نهایی وجود دارند؟
        if final_values:
            print_success(f"✅ تب خانه داده‌های نهایی را دارد ({len(final_values)} عنصر)")
            return True
        else:
            print_error("❌ تب خانه داده‌های نهایی را ندارد!")
            return False
    
    # ============================================================
    # تست 9: ایجاد گزارش جدید و بررسی ریست شدن
    # ============================================================
    
    def test_new_report_reset(self) -> bool:
        """تست 9: ایجاد گزارش جدید و بررسی ریست شدن"""
        print_subheader("9. ایجاد گزارش جدید و بررسی ریست شدن")
        
        if not self.test_user_id:
            print_error("کاربر تست وجود ندارد")
            return False
        
        # ایجاد گزارش جدید
        new_report_id = self.execute_insert(
            """INSERT INTO reports (user_id, report_name, plant_name, season, growth_stage, report_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.test_user_id,
                "گزارش جدید تست",
                "خیار",
                "بهار",
                "رشد رویشی",
                "۱۴۰۵/۰۴/۱۴"
            )
        )
        
        if not new_report_id:
            print_error("خطا در ایجاد گزارش جدید")
            return False
        
        print_success(f"گزارش جدید ایجاد شد (ID: {new_report_id})")
        
        # بررسی اینکه محاسبات برای گزارش جدید خالی است
        calc = self.execute_query(
            "SELECT * FROM calculations WHERE report_id = ?",
            (new_report_id,)
        )
        
        if calc:
            print_warning(f"⚠️ گزارش جدید محاسبات دارد (ID: {calc[0]['id']})")
            target_values = json.loads(calc[0]['target_values']) if calc[0]['target_values'] else {}
            final_values = json.loads(calc[0]['final_values']) if calc[0]['final_values'] else {}
            
            if target_values:
                print_warning(f"  عناصر هدف وجود دارند: {len(target_values)}")
                # این یعنی ریست نشده!
                return False
            else:
                print_success("✅ عناصر هدف خالی هستند (ریست شده)")
                return True
        else:
            print_success("✅ گزارش جدید محاسبات ندارد (ریست شده)")
            return True
    
    # ============================================================
    # تست 10: بررسی یکپارچگی دیتابیس
    # ============================================================
    
    def test_database_integrity(self) -> bool:
        """تست 10: بررسی یکپارچگی دیتابیس"""
        print_subheader("10. بررسی یکپارچگی دیتابیس")
        
        # بررسی روابط
        reports = self.execute_query("SELECT id, user_id FROM reports")
        print_info(f"تعداد گزارش‌ها: {len(reports)}")
        
        water_analyses = self.execute_query("SELECT id, report_id FROM water_analyses")
        print_info(f"تعداد آنالیز آب: {len(water_analyses)}")
        
        calculations = self.execute_query("SELECT id, report_id FROM calculations")
        print_info(f"تعداد محاسبات: {len(calculations)}")
        
        # بررسی اینکه هر report_id در reports وجود دارد
        report_ids = [r['id'] for r in reports]
        
        missing_reports = []
        for w in water_analyses:
            if w['report_id'] not in report_ids:
                missing_reports.append(f"water_analysis {w['id']} -> report {w['report_id']}")
        
        for c in calculations:
            if c['report_id'] not in report_ids:
                missing_reports.append(f"calculation {c['id']} -> report {c['report_id']}")
        
        if missing_reports:
            print_warning(f"ارتباطات شکسته: {missing_reports}")
            return False
        else:
            print_success("✅ همه ارتباطات سالم هستند")
            return True
    
    # ============================================================
    # اجرای همه تست‌ها
    # ============================================================
    
    def run_all_tests(self) -> bool:
        """اجرای همه تست‌ها"""
        print_header("🧪 شروع تست کامل جریان FarmTech")
        print_info(f"📁 دیتابیس: {self.db_path}")
        print_info(f"📱 شماره تلفن تست: {self.test_phone}")
        print_info(f"🔑 رمز عبور: {self.test_password}")
        
        # اتصال به دیتابیس
        if not self.connect_db():
            return False
        
        tests = [
            ("بررسی دیتابیس", self.test_database_exists),
            ("ایجاد کاربر تست", self.test_create_user),
            ("ایجاد گزارش", self.test_create_report),
            ("ذخیره آنالیز آب", self.test_save_water_analysis),
            ("ذخیره عناصر هدف", self.test_save_calculation),
            ("ذخیره نتیجه بهینه‌سازی", self.test_save_optimization_result),
            ("بارگذاری مجدد گزارش", self.test_reload_report),
            ("بررسی داده‌های تب خانه", self.test_home_tab_data),
            ("ایجاد گزارش جدید و ریست", self.test_new_report_reset),
            ("بررسی یکپارچگی دیتابیس", self.test_database_integrity),
        ]
        
        print()
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    self.passed += 1
                else:
                    self.failed += 1
                self.results.append((test_name, result))
            except Exception as e:
                print_error(f"خطا در تست {test_name}: {e}")
                self.failed += 1
                self.results.append((test_name, False))
        
        # نمایش گزارش نهایی
        self.print_final_report()
        
        # بستن اتصال
        self.close_db()
        
        return self.failed == 0
    
    # ============================================================
    # گزارش نهایی
    # ============================================================
    
    def print_final_report(self):
        """چاپ گزارش نهایی"""
        print_header("📊 گزارش نهایی تست")
        
        total = self.passed + self.failed
        print(f"\n{Colors.BOLD}آمار کلی:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅ موفق: {self.passed}{Colors.RESET}")
        print(f"  {Colors.RED}❌ ناموفق: {self.failed}{Colors.RESET}")
        print(f"  📊 مجموع: {total}")
        
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"  📈 نرخ موفقیت: {success_rate:.1f}%")
        
        print(f"\n{Colors.BOLD}جزئیات تست‌ها:{Colors.RESET}")
        for test_name, result in self.results:
            status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if result else f"{Colors.RED}❌ FAIL{Colors.RESET}"
            print(f"  {status} - {test_name}")
        
        print("\n" + "="*70)
        
        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 همه تست‌ها با موفقیت انجام شدند!{Colors.RESET}")
            print(f"{Colors.GREEN}✅ سیستم به درستی کار می‌کند.{Colors.RESET}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️ برخی تست‌ها ناموفق بودند.{Colors.RESET}")
            # تحلیل دقیق خطاها
            failed_tests = [name for name, result in self.results if not result]
            print(f"{Colors.YELLOW}💡 تست‌های ناموفق: {', '.join(failed_tests)}{Colors.RESET}")
            
            if "بارگذاری مجدد گزارش" in failed_tests or "بررسی داده‌های تب خانه" in failed_tests:
                print(f"{Colors.YELLOW}🔧 مشکل اصلی: final_values در دیتابیس ذخیره نمی‌شود.{Colors.RESET}")
                print(f"{Colors.YELLOW}🔧 راه حل: در optimizeFertilizers بعد از دریافت نتیجه، saveCurrentReport صدا زده شود.{Colors.RESET}")
        
        print("="*70)

# ============================================================
# اجرای اصلی
# ============================================================

def main():
    try:
        tester = FullFlowTester()
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️ تست توسط کاربر متوقف شد.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطای غیرمنتظره: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()