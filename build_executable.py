#!/usr/bin/env python3
"""
FarmTech - ProFertilizer
ساخت نسخه اجرایی (Executable) برای دسکتاپ
"""

import os
import sys
import shutil
import subprocess
import platform
import json
import zipfile
from pathlib import Path
from datetime import datetime

# ============================================================
# تنظیمات
# ============================================================
PROJECT_DIR = Path(__file__).parent.absolute()
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build_temp"
OUTPUT_DIR = PROJECT_DIR / "FarmTech_Desktop"

# ============================================================
# رنگ‌ها
# ============================================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.RESET}")
def print_info(msg): print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")
def print_header(msg): print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}\n{Colors.BOLD}{msg}{Colors.RESET}\n{Colors.CYAN}{'='*70}{Colors.RESET}")

# ============================================================
# توابع کمکی
# ============================================================
def run_command(cmd, cwd=None, env=None):
    """اجرای دستور و نمایش خروجی"""
    print_info(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        shell=isinstance(cmd, str),
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print_warning(result.stderr)
    return result.returncode == 0

def get_python_exe():
    """دریافت مسیر Python"""
    if platform.system() == 'Windows':
        return sys.executable
    return sys.executable

def get_npm_cmd():
    """دریافت دستور npm مناسب سیستم"""
    return 'npm.cmd' if platform.system() == 'Windows' else 'npm'

# ============================================================
# مرحله 1: Build فرانت‌اند
# ============================================================
def build_frontend():
    print_header("🏗️  مرحله 1: ساخت فرانت‌اند (Vue)")
    
    frontend_dir = PROJECT_DIR / "frontend"
    if not frontend_dir.exists():
        print_error("پوشه frontend یافت نشد!")
        return False
    
    # نصب وابستگی‌ها
    print_info("نصب وابستگی‌های فرانت‌اند...")
    npm = get_npm_cmd()
    if not run_command([npm, 'install'], cwd=str(frontend_dir)):
        print_error("خطا در نصب وابستگی‌های فرانت‌اند")
        return False
    
    # Build
    print_info("ساخت فرانت‌اند...")
    if not run_command([npm, 'run', 'build'], cwd=str(frontend_dir)):
        print_error("خطا در ساخت فرانت‌اند")
        return False
    
    # بررسی خروجی
    dist_dir = frontend_dir / "dist"
    if not dist_dir.exists():
        print_error("پوشه dist ساخته نشد!")
        return False
    
    print_success(f"فرانت‌اند ساخته شد: {dist_dir}")
    return True

# ============================================================
# مرحله 2: ساخت بک‌اند با PyInstaller
# ============================================================
def build_backend():
    print_header("🏗️  مرحله 2: ساخت بک‌اند (FastAPI)")
    
    backend_dir = PROJECT_DIR / "backend"
    if not backend_dir.exists():
        print_error("پوشه backend یافت نشد!")
        return False
    
    # نصب PyInstaller
    print_info("نصب PyInstaller...")
    python = get_python_exe()
    if not run_command([python, '-m', 'pip', 'install', 'pyinstaller', '--upgrade'], cwd=str(backend_dir)):
        print_error("خطا در نصب PyInstaller")
        return False
    
    # نصب وابستگی‌های بک‌اند
    print_info("نصب وابستگی‌های بک‌اند...")
    if not run_command([python, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'], cwd=str(backend_dir)):
        print_error("خطا در نصب وابستگی‌های بک‌اند")
        return False
    
    # ساخت فایل اصلی
    print_info("ساخت فایل اجرایی بک‌اند...")
    
    # ایجاد فایل spec برای PyInstaller
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=[r'{backend_dir}'],
    binaries=[],
    datas=[
        (r'{backend_dir}/farmtech.db', '.'),
    ],
    hiddenimports=[
        'sqlalchemy',
        'sqlalchemy.ext.declarative',
        'sqlalchemy.orm',
        'numpy',
        'scipy',
        'scipy.optimize',
        'scipy.linalg',
        'scipy.sparse',
        'scipy.special',
        'scipy.stats',
        'scipy.integrate',
        'scipy.interpolate',
        'scipy.signal',
        'scipy.ndimage',
        'scipy.cluster',
        'scipy.fft',
        'scipy.io',
        'scipy.misc',
        'scipy.spatial',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FarmTech_Backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    spec_path = backend_dir / "farmtech.spec"
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # اجرای PyInstaller
    if not run_command([python, '-m', 'PyInstaller', '--clean', str(spec_path)], cwd=str(backend_dir)):
        print_error("خطا در ساخت بک‌اند با PyInstaller")
        return False
    
    # پیدا کردن فایل خروجی
    exe_dir = backend_dir / "dist"
    if platform.system() == 'Windows':
        exe_file = exe_dir / "FarmTech_Backend.exe"
    else:
        exe_file = exe_dir / "FarmTech_Backend"
    
    if not exe_file.exists():
        print_error("فایل اجرایی بک‌اند ساخته نشد!")
        return False
    
    print_success(f"بک‌اند ساخته شد: {exe_file}")
    return True

# ============================================================
# مرحله 3: ساخت Launcher
# ============================================================
def create_launcher():
    print_header("🚀 مرحله 3: ساخت Launcher")
    
    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # کپی فرانت‌اند
    frontend_dist = PROJECT_DIR / "frontend" / "dist"
    if frontend_dist.exists():
        target_frontend = output_dir / "frontend"
        if target_frontend.exists():
            shutil.rmtree(target_frontend)
        shutil.copytree(frontend_dist, target_frontend)
        print_success("فرانت‌اند کپی شد")
    
    # کپی بک‌اند
    backend_exe = PROJECT_DIR / "backend" / "dist" / "FarmTech_Backend.exe"
    if backend_exe.exists():
        target_backend = output_dir / "FarmTech_Backend.exe"
        shutil.copy2(backend_exe, target_backend)
        print_success("بک‌اند کپی شد")
    
    # کپی دیتابیس (در صورت وجود)
    db_path = PROJECT_DIR / "backend" / "farmtech.db"
    if db_path.exists():
        shutil.copy2(db_path, output_dir / "farmtech.db")
        print_success("دیتابیس کپی شد")
    
    # ============================================================
    # ساخت فایل launch.bat (ویندوز)
    # ============================================================
    bat_content = '''@echo off
chcp 65001 >nul
title FarmTech - ProFertilizer

echo ============================================================
echo    🌱 FarmTech - ProFertilizer
echo    سیستم هوشمند نسخه‌نویسی کود
echo ============================================================
echo.

echo 🔍 Checking ports...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo 🚀 Starting Backend Server...
start "FarmTech Backend" /MIN FarmTech_Backend.exe

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo 🌐 Starting Frontend...
echo.
echo ============================================================
echo    ✅ FarmTech is ready!
echo    🌐 Open in browser: http://localhost:3000
echo    ⚠️  Keep this window open!
echo    🛑 Press Ctrl+C to stop all services
echo ============================================================
echo.

cd frontend
start /B npm run dev -- --host 0.0.0.0 --port 3000

echo.
echo 🟢 Running...
pause >nul

echo 🛑 Stopping services...
taskkill /F /IM FarmTech_Backend.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo ✅ Done!
'''
    
    bat_path = output_dir / "launch.bat"
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print_success("launch.bat ایجاد شد")

    # ============================================================
    # ساخت فایل launch.sh (لینوکس/مک)
    # ============================================================
    sh_content = '''#!/bin/bash
echo "============================================================"
echo "   🌱 FarmTech - ProFertilizer"
echo "   سیستم هوشمند نسخه‌نویسی کود"
echo "============================================================"
echo ""

echo "🔍 Checking ports..."
for pid in $(lsof -ti :8000); do
    kill -9 $pid 2>/dev/null
done

echo "🚀 Starting Backend Server..."
chmod +x FarmTech_Backend
./FarmTech_Backend &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 5

echo "🌐 Starting Frontend..."
echo ""
echo "============================================================"
echo "   ✅ FarmTech is ready!"
echo "   🌐 Open in browser: http://localhost:3000"
echo "   ⚠️  Keep this terminal open!"
echo "   🛑 Press Ctrl+C to stop all services"
echo "============================================================"
echo ""

cd frontend
npm run dev -- --host 0.0.0.0 --port 3000

echo ""
echo "🛑 Stopping services..."
kill $BACKEND_PID 2>/dev/null
echo "✅ Done!"
'''
    
    sh_path = output_dir / "launch.sh"
    with open(sh_path, "w", encoding="utf-8") as f:
        f.write(sh_content)
    # اجرایی کردن فایل شل در لینوکس/مک
    if platform.system() != 'Windows':
        os.chmod(sh_path, 0o755)
    print_success("launch.sh ایجاد شد")

    # ============================================================
    # فایل README برای کاربر
    # ============================================================
    readme_content = '''
# 🌱 FarmTech - ProFertilizer

## 🚀 راهنمای نصب و اجرا

### پیش‌نیازها
- **Node.js** (نسخه 18 یا بالاتر)
- مرورگر (Chrome, Firefox, Edge)

### اجرای برنامه

#### در ویندوز:
1. فایل `launch.bat` را دوبار کلیک کنید
2. منتظر بمانید تا پیام "FarmTech is ready!" نمایش داده شود
3. مرورگر خود را باز کرده و به آدرس `http://localhost:3000` بروید

#### در لینوکس/مک:
1. ترمینال را باز کرده و به این پوشه بروید
2. دستور `chmod +x launch.sh` را اجرا کنید
3. دستور `./launch.sh` را اجرا کنید
4. مرورگر خود را باز کرده و به آدرس `http://localhost:3000` بروید

### اطلاعات ورود (پیش‌فرض)
- **شماره تلفن:** `09121234567`
- **رمز عبور:** `Test@123456`

### توقف برنامه
- در ویندوز: پنجره ترمینال را ببندید یا Ctrl+C بزنید
- در لینوکس/مک: Ctrl+C بزنید

### نکات مهم
- برای اجرا به اتصال اینترنت نیاز نیست (به جز نصب اولیه Node.js)
- تمام داده‌ها به صورت محلی ذخیره می‌شوند
- برای پشتیبان‌گیری، فایل `farmtech.db` را کپی کنید

---
© 2026 FarmTech - تمامی حقوق محفوظ است
'''
    
    readme_path = output_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print_success("README.txt ایجاد شد")

    return True

# ============================================================
# مرحله 4: ساخت فایل ZIP نهایی
# ============================================================
def create_zip_package():
    print_header("📦 مرحله 4: ساخت پکیج نهایی")
    
    output_dir = OUTPUT_DIR
    if not output_dir.exists():
        print_error("پوشه خروجی وجود ندارد!")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"FarmTech_Desktop_{timestamp}.zip"
    zip_path = PROJECT_DIR / zip_name
    
    print_info(f"ایجاد فایل: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(output_dir.parent)
                zipf.write(file_path, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print_success(f"پکیج نهایی ایجاد شد: {zip_path} ({size_mb:.2f} MB)")
    return True

# ============================================================
# مرحله 5: پاک‌سازی
# ============================================================
def cleanup():
    print_header("🧹 مرحله 5: پاک‌سازی")
    
    # حذف پوشه‌های موقت
    dirs_to_remove = [
        PROJECT_DIR / "build_temp",
        PROJECT_DIR / "backend" / "build",
        PROJECT_DIR / "backend" / "dist",
        PROJECT_DIR / "backend" / "farmtech.spec",
    ]
    
    for d in dirs_to_remove:
        if d.exists():
            if d.is_dir():
                shutil.rmtree(d)
            else:
                d.unlink()
            print_info(f"حذف شد: {d}")
    
    print_success("پاک‌سازی کامل شد")

# ============================================================
# اجرای اصلی
# ============================================================
def main():
    print_header("🌱 FarmTech - ساخت نسخه اجرایی دسکتاپ")
    
    print_info(f"سیستم عامل: {platform.system()}")
    print_info(f"پایتون: {sys.version}")
    print_info(f"پروژه: {PROJECT_DIR}")
    
    # 1. Build Frontend
    if not build_frontend():
        print_error("ساخت فرانت‌اند ناموفق بود!")
        sys.exit(1)
    
    # 2. Build Backend
    if not build_backend():
        print_error("ساخت بک‌اند ناموفق بود!")
        sys.exit(1)
    
    # 3. Create Launcher
    if not create_launcher():
        print_error("ساخت Launcher ناموفق بود!")
        sys.exit(1)
    
    # 4. Create ZIP
    if not create_zip_package():
        print_error("ساخت پکیج نهایی ناموفق بود!")
        sys.exit(1)
    
    # 5. Cleanup
    cleanup()
    
    print_header("🎉 ساخت نسخه اجرایی با موفقیت کامل شد!")
    print(f"\n{Colors.GREEN}📁 پکیج نهایی:{Colors.RESET}")
    print(f"   {PROJECT_DIR / 'FarmTech_Desktop_*.zip'}")
    print(f"\n{Colors.GREEN}📋 مراحل استفاده:{Colors.RESET}")
    print(f"   1. فایل ZIP را Extract کنید")
    print(f"   2. در ویندوز: launch.bat را اجرا کنید")
    print(f"   3. در لینوکس/مک: launch.sh را اجرا کنید")
    print(f"   4. مرورگر را باز کنید: http://localhost:3000")
    print(f"   5. با شماره 09121234567 و رمز Test@123456 وارد شوید")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏹️  عملیات متوقف شد{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"خطای غیرمنتظره: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)