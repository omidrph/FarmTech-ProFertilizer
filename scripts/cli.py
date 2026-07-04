#!/usr/bin/env python3
# scripts/cli.py
"""
FarmTech-ProFertilizer - CLI Management Tool
Improved version with dynamic ports, better error handling, and full English UI
"""

import os
import sys
import subprocess
import platform
import time
import socket
import signal
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple

# ============================================================
# Colorama Support (Optional)
# ============================================================
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = BRIGHT = ""

# ============================================================
# Base Configuration
# ============================================================
# Project root directory (parent of scripts folder)
BASE_DIR = Path(__file__).parent.parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
LOGS_DIR = BASE_DIR / "logs"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Default ports
DEFAULT_BACKEND_PORT = 8000
DEFAULT_FRONTEND_PORT = 3000

# ============================================================
# Colors Class
# ============================================================
class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

# ============================================================
# Helper Functions
# ============================================================
def is_port_available(port: int, host: str = '127.0.0.1') -> bool:
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_available_port(start_port: int, max_attempts: int = 20) -> int:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    raise RuntimeError(f"No available port found in range {start_port}-{start_port + max_attempts}")

def wait_for_service(url: str, timeout: int = 30) -> bool:
    """Wait for a service to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = urllib.request.urlopen(url, timeout=2)
            if response.status == 200:
                return True
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, OSError):
            time.sleep(0.5)
    return False

def get_python_executable() -> str:
    """Get Python executable path in venv"""
    if platform.system() == 'Windows':
        venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    else:
        venv_python = BACKEND_DIR / "venv" / "bin" / "python"
    
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def get_pip_executable() -> str:
    """Get pip executable path in venv"""
    if platform.system() == 'Windows':
        venv_pip = BACKEND_DIR / "venv" / "Scripts" / "pip.exe"
    else:
        venv_pip = BACKEND_DIR / "venv" / "bin" / "pip"
    
    if venv_pip.exists():
        return str(venv_pip)
    return "pip"

def kill_process_on_port(port: int) -> bool:
    """Try to kill process running on specified port"""
    try:
        if platform.system() == 'Windows':
            # Find PID using netstat
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if parts:
                            pid = parts[-1]
                            subprocess.run(f'taskkill /PID {pid} /F', shell=True, capture_output=True)
                            return True
        else:
            # Linux/Mac - use lsof
            result = subprocess.run(
                f'lsof -ti :{port}',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                    except:
                        pass
                return True
    except Exception as e:
        print(f"{Colors.RED}Error killing process: {e}{Colors.RESET}")
    return False

def ensure_logs_dir():
    """Ensure logs directory exists"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def check_directory_exists(path: Path, name: str) -> bool:
    """Check if directory exists and print error if not"""
    if not path.exists():
        print(f"{Colors.RED}Error: {name} directory not found: {path}{Colors.RESET}")
        return False
    return True

# ============================================================
# Display Functions
# ============================================================
def print_header():
    """Print application header"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}  🌱 FarmTech - ProFertilizer Management Tool{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}  📍 Platform: {platform.system()} | Python {platform.python_version()}{Colors.RESET}")
    print(f"{Colors.BLUE}  📁 Project:  {BASE_DIR}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_menu():
    """Print main menu"""
    print(f"{Colors.YELLOW}  Please select an option:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}{Colors.GREEN}1{Colors.RESET}  ▶️  Run Full Application (Backend + Frontend)")
    print(f"  {Colors.BOLD}{Colors.GREEN}2{Colors.RESET}  ▶️  Run Backend Only (FastAPI)")
    print(f"  {Colors.BOLD}{Colors.GREEN}3{Colors.RESET}  ▶️  Run Frontend Only (Vue)")
    print(f"  {Colors.BOLD}{Colors.GREEN}4{Colors.RESET}  📦 Install Dependencies")
    print(f"  {Colors.BOLD}{Colors.GREEN}5{Colors.RESET}  🧪 Run Tests")
    print(f"  {Colors.BOLD}{Colors.GREEN}6{Colors.RESET}  🏗️  Build Production Version")
    print(f"  {Colors.BOLD}{Colors.GREEN}7{Colors.RESET}  🧹 Clean Cache Files")
    print(f"  {Colors.BOLD}{Colors.YELLOW}8{Colors.RESET}  🔧 Free Occupied Ports")
    print(f"  {Colors.BOLD}{Colors.CYAN}9{Colors.RESET}  📊 View Logs")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}10{Colors.RESET} 🗄️  Reset Database (Create Fresh)")
    print(f"  {Colors.BOLD}{Colors.RED}0{Colors.RESET}  🚪 Exit")
    print()

# ============================================================
# 🆕 Reset Database Function
# ============================================================
def reset_database():
    """Reset and recreate database with all tables"""
    print(f"\n{Colors.BLUE}🗄️  Resetting Database...{Colors.RESET}")
    
    db_path = BACKEND_DIR / "farmtech.db"
    
    # 1. حذف دیتابیس قدیمی
    if db_path.exists():
        print(f"{Colors.YELLOW}⚠️  Removing old database...{Colors.RESET}")
        try:
            db_path.unlink()
            print(f"{Colors.GREEN}✅ Old database removed{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error removing database: {e}{Colors.RESET}")
            return
    
    # 2. ایجاد دیتابیس جدید با SQL مستقیم
    print(f"{Colors.BLUE}📦 Creating new database with all tables...{Colors.RESET}")
    
    # محتوای اسکریپت موقت
    temp_script_content = '''import sys
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "farmtech.db"

TABLES_SQL = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """,
    "user_sessions": """
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token VARCHAR(255) UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """,
    "reports": """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_name VARCHAR(100),
            plant_name VARCHAR(50),
            season VARCHAR(20),
            growth_stage VARCHAR(50),
            report_date VARCHAR(20),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """,
    "fertilizers": """
        CREATE TABLE IF NOT EXISTS fertilizers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(100) NOT NULL,
            brand VARCHAR(100),
            category VARCHAR(50),
            form VARCHAR(20),
            concentration FLOAT DEFAULT 100.0,
            elements JSON,
            price_per_kg FLOAT DEFAULT 0.0,
            is_acid BOOLEAN DEFAULT 0,
            acid_type VARCHAR(10),
            ph_level FLOAT,
            description TEXT,
            is_system_default BOOLEAN DEFAULT 0,
            source_system_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """,
    "water_analyses": """
        CREATE TABLE IF NOT EXISTS water_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            water_percentage FLOAT DEFAULT 80.0,
            wastewater_percentage FLOAT DEFAULT 20.0,
            water_salinity FLOAT DEFAULT 0.0,
            wastewater_values JSON,
            water_values JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
        )
    """,
    "calculations": """
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            target_values JSON,
            final_values JSON,
            reservoir_data JSON,
            calc_rows JSON,
            interpretation TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
        )
    """,
    "recipes": """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            is_system BOOLEAN DEFAULT 0,
            user_id INTEGER,
            target_values JSON NOT NULL,
            category VARCHAR(50),
            stage VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """,
    "water_analysis_templates": """
        CREATE TABLE IF NOT EXISTS water_analysis_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            water_percentage FLOAT DEFAULT 100.0,
            wastewater_percentage FLOAT DEFAULT 0.0,
            water_salinity FLOAT DEFAULT 0.8,
            water_salinity_unit VARCHAR(10) DEFAULT "dS/m",
            water_ph FLOAT,
            water_values JSON,
            wastewater_values JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """,
    "optimization_logs": """
        CREATE TABLE IF NOT EXISTS optimization_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_id INTEGER,
            target_values JSON NOT NULL,
            water_values JSON,
            fertilizers_selected JSON,
            optimization_options JSON,
            optimized_weights JSON,
            final_concentrations JSON,
            residual_error FLOAT,
            cost_total FLOAT,
            iterations INTEGER,
            convergence_time_ms FLOAT,
            ion_balance JSON,
            warnings JSON,
            suggestions JSON,
            is_successful BOOLEAN DEFAULT 1,
            error_message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
        )
    """
}

def main():
    db_path = Path(__file__).parent / "farmtech.db"
    
    print("📦 Creating database tables...")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        for table_name, sql in TABLES_SQL.items():
            try:
                cursor.execute(sql)
                print(f"   ✅ Table {table_name} created")
            except Exception as e:
                print(f"   ❌ Error creating {table_name}: {e}")
        
        conn.commit()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"\n📊 Tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
        
        print("\n✅ Database created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(temp_script_content)
        temp_script = f.name
    
    try:
        # اجرای اسکریپت موقت
        result = subprocess.run(
            [sys.executable, temp_script],
            cwd=str(BACKEND_DIR)
        )
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Database reset successfully!{Colors.RESET}")
            
            # بارگذاری داده‌های سیستمی
            print(f"{Colors.BLUE}🌱 Loading system data...{Colors.RESET}")
            load_system_data()
        else:
            print(f"{Colors.RED}❌ Failed to reset database{Colors.RESET}")
            
    finally:
        # حذف فایل موقت
        try:
            os.unlink(temp_script)
        except:
            pass

def load_system_data():
    """Load system fertilizers and recipes"""
    python_exe = get_python_executable()
    
    # بارگذاری کودهای سیستمی
    print(f"{Colors.BLUE}   📦 Loading system fertilizers...{Colors.RESET}")
    cmd = [
        python_exe, "-c",
        "from app.seeds.fertilizer_seeds import seed_system_fertilizers; "
        "from app.database import SessionLocal; "
        "db = SessionLocal(); "
        "stats = seed_system_fertilizers(db); "
        "db.commit(); db.close(); "
        "print(f'✅ {stats[\\\"added\\\"]} fertilizers added')"
    ]
    subprocess.run(cmd, cwd=str(BACKEND_DIR))
    
    # بارگذاری رسپی‌های سیستمی
    print(f"{Colors.BLUE}   📋 Loading system recipes...{Colors.RESET}")
    cmd = [
        python_exe, "-c",
        "from app.seeds.recipe_seeds import seed_system_recipes; "
        "from app.database import SessionLocal; "
        "db = SessionLocal(); "
        "stats = seed_system_recipes(db); "
        "db.commit(); db.close(); "
        "print(f'✅ {stats[\\\"added\\\"]} recipes added')"
    ]
    subprocess.run(cmd, cwd=str(BACKEND_DIR))
    
    # ایجاد کاربر تست
    print(f"{Colors.BLUE}   👤 Creating test user...{Colors.RESET}")
    cmd = [
        python_exe, "-c",
        "from app.crud import create_user, get_user_by_phone; "
        "from app.schemas import UserCreate; "
        "from app.database import SessionLocal; "
        "db = SessionLocal(); "
        "user = get_user_by_phone(db, '09121234567'); "
        "if not user: "
        "    user_data = UserCreate("
        "        first_name='تست', "
        "        last_name='سیستم', "
        "        phone_number='09121234567', "
        "        password='Test@123456'"
        "    ); "
        "    user = create_user(db, user_data); "
        "    print(f'✅ Test user created: ID={user.id}'); "
        "else: "
        "    print(f'✅ Test user already exists: ID={user.id}'); "
        "db.commit(); db.close()"
    ]
    subprocess.run(cmd, cwd=str(BACKEND_DIR))
    
    print(f"{Colors.GREEN}✅ System data loaded successfully!{Colors.RESET}")
    print(f"{Colors.BLUE}   👤 Test user: 09121234567{Colors.RESET}")
    print(f"{Colors.BLUE}   🔑 Password: Test@123456{Colors.RESET}")

# ============================================================
# Backend Functions
# ============================================================
def run_backend(port: Optional[int] = None, show_logs: bool = True) -> Tuple[Optional[subprocess.Popen], int]:
    """Run backend server and return process and port"""
    ensure_logs_dir()
    
    # Check backend directory
    if not check_directory_exists(BACKEND_DIR, "Backend"):
        return None, 0
    
    # Check virtual environment
    python_exe = get_python_executable()
    if not Path(python_exe).exists():
        print(f"{Colors.YELLOW}⚠️  Virtual environment not found. Installing dependencies...{Colors.RESET}")
        install_dependencies_backend()
        python_exe = get_python_executable()
    
    # Find available port
    if port is None:
        port = DEFAULT_BACKEND_PORT
    
    if not is_port_available(port):
        print(f"{Colors.YELLOW}⚠️  Port {port} is occupied. Searching for available port...{Colors.RESET}")
        try:
            port = find_available_port(port)
            print(f"{Colors.GREEN}✅ Port {port} selected{Colors.RESET}")
        except RuntimeError as e:
            print(f"{Colors.RED}❌ {e}{Colors.RESET}")
            return None, 0
    
    print(f"\n{Colors.BLUE}🚀 Starting Backend on port {port}...{Colors.RESET}")
    
    # Prepare command
    cmd = [
        python_exe, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
    # Log handling
    log_file = LOGS_DIR / "backend.log"
    if show_logs:
        log_handle = open(log_file, "w", encoding="utf-8")
        process = subprocess.Popen(
            cmd,
            cwd=str(BACKEND_DIR),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )
    else:
        process = subprocess.Popen(
            cmd,
            cwd=str(BACKEND_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    # Wait for backend to be ready
    print(f"{Colors.YELLOW}⏳ Waiting for Backend to start...{Colors.RESET}")
    if wait_for_service(f"http://localhost:{port}/health", timeout=30):
        print(f"{Colors.GREEN}✅ Backend is ready: http://localhost:{port}{Colors.RESET}")
        if show_logs:
            print(f"{Colors.BLUE}📄 Logs: {log_file}{Colors.RESET}")
        return process, port
    else:
        print(f"{Colors.RED}❌ Backend failed to start. Please check logs:{Colors.RESET}")
        print(f"{Colors.BLUE}   {log_file}{Colors.RESET}")
        # Show last 10 lines of log
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"\n{Colors.YELLOW}--- Last 10 log lines ---{Colors.RESET}")
                for line in lines[-10:]:
                    print(f"   {line.rstrip()}")
        except:
            pass
        return process, port

# ============================================================
# Frontend Functions
# ============================================================
def run_frontend(port: Optional[int] = None) -> Tuple[Optional[subprocess.Popen], int]:
    """Run frontend server and return process and port"""
    # Check frontend directory
    if not check_directory_exists(FRONTEND_DIR, "Frontend"):
        return None, 0
    
    # Check node_modules
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print(f"{Colors.YELLOW}⚠️  node_modules not found. Installing dependencies...{Colors.RESET}")
        install_dependencies_frontend()
    
    # Find available port
    if port is None:
        port = DEFAULT_FRONTEND_PORT
    
    if not is_port_available(port):
        print(f"{Colors.YELLOW}⚠️  Port {port} is occupied. Searching for available port...{Colors.RESET}")
        try:
            port = find_available_port(port)
            print(f"{Colors.GREEN}✅ Port {port} selected{Colors.RESET}")
        except RuntimeError as e:
            print(f"{Colors.RED}❌ {e}{Colors.RESET}")
            return None, 0
    
    print(f"\n{Colors.BLUE}🚀 Starting Frontend on port {port}...{Colors.RESET}")
    
    # Set environment variable for port
    env = os.environ.copy()
    env['PORT'] = str(port)
    
    # Use cmd.exe on Windows
    if platform.system() == 'Windows':
        cmd = f'set PORT={port}&& npm run dev'
    else:
        cmd = f'PORT={port} npm run dev'
    
    process = subprocess.Popen(
        cmd,
        cwd=str(FRONTEND_DIR),
        shell=True,
        env=env
    )
    
    # Wait for frontend to be ready
    print(f"{Colors.YELLOW}⏳ Waiting for Frontend to start...{Colors.RESET}")
    if wait_for_service(f"http://localhost:{port}", timeout=60):
        print(f"{Colors.GREEN}✅ Frontend is ready: http://localhost:{port}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️  Frontend may still be starting...{Colors.RESET}")
    
    return process, port

# ============================================================
# Dependency Installation
# ============================================================
def install_dependencies_backend():
    """Install backend dependencies"""
    print(f"\n{Colors.YELLOW}📦 Installing Backend Dependencies...{Colors.RESET}")
    
    # Create venv if it doesn't exist
    venv_dir = BACKEND_DIR / "venv"
    if not venv_dir.exists():
        print(f"{Colors.BLUE}🔧 Creating virtual environment...{Colors.RESET}")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Install requirements
    python_exe = get_python_executable()
    requirements = BACKEND_DIR / "requirements.txt"
    
    if requirements.exists():
        print(f"{Colors.BLUE}📦 Installing packages from requirements.txt...{Colors.RESET}")
        result = subprocess.run(
            [python_exe, "-m", "pip", "install", "-r", str(requirements), "--upgrade"],
            cwd=str(BACKEND_DIR)
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Backend dependencies installed{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Error installing backend dependencies{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ requirements.txt not found{Colors.RESET}")

def install_dependencies_frontend():
    """Install frontend dependencies"""
    print(f"\n{Colors.YELLOW}📦 Installing Frontend Dependencies...{Colors.RESET}")
    
    # Check npm
    npm_cmd = 'npm.cmd' if platform.system() == 'Windows' else 'npm'
    try:
        subprocess.run([npm_cmd, '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}❌ npm not found. Please install Node.js{Colors.RESET}")
        return
    
    # Install packages
    result = subprocess.run(
        [npm_cmd, 'install'],
        cwd=str(FRONTEND_DIR)
    )
    
    if result.returncode == 0:
        print(f"{Colors.GREEN}✅ Frontend dependencies installed{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Error installing frontend dependencies{Colors.RESET}")

def install_dependencies():
    """Install all dependencies"""
    print(f"\n{Colors.BLUE}📦 Installing All Dependencies...{Colors.RESET}")
    install_dependencies_backend()
    install_dependencies_frontend()
    print(f"\n{Colors.GREEN}✅ All dependencies installed successfully!{Colors.RESET}")

# ============================================================
# Test Functions
# ============================================================
def run_tests():
    """Run tests"""
    print(f"\n{Colors.BLUE}🧪 Running Tests...{Colors.RESET}")
    
    python_exe = get_python_executable()
    test_file = BACKEND_DIR / "tests" / "test_all.py"
    
    if not test_file.exists():
        print(f"{Colors.RED}❌ Test file not found: {test_file}{Colors.RESET}")
        return
    
    # Start backend first
    print(f"{Colors.YELLOW}⏳ Starting Backend for tests...{Colors.RESET}")
    backend_process, backend_port = run_backend(show_logs=False)
    
    if backend_process is None:
        print(f"{Colors.RED}❌ Backend failed to start. Tests cannot run{Colors.RESET}")
        return
    
    try:
        # Run tests
        print(f"{Colors.BLUE}🧪 Running tests...{Colors.RESET}")
        result = subprocess.run(
            [python_exe, str(test_file)],
            cwd=str(BACKEND_DIR)
        )
        
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✅ All tests passed{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ Some tests failed{Colors.RESET}")
    finally:
        # Stop backend
        print(f"{Colors.YELLOW}⏹️  Stopping Backend...{Colors.RESET}")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()

# ============================================================
# Build Functions
# ============================================================
def build_production():
    """Build production version"""
    print(f"\n{Colors.BLUE}🏗️  Building Production Version...{Colors.RESET}")
    
    # Backend
    print(f"\n{Colors.YELLOW}📦 Preparing Backend...{Colors.RESET}")
    pip_exe = get_pip_executable()
    
    result = subprocess.run(
        [pip_exe, "freeze"],
        cwd=str(BACKEND_DIR),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        requirements_file = BACKEND_DIR / "requirements.txt"
        with open(requirements_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        print(f"{Colors.GREEN}✅ requirements.txt updated{Colors.RESET}")
    
    # Frontend
    print(f"\n{Colors.YELLOW}📦 Building Frontend...{Colors.RESET}")
    npm_cmd = 'npm.cmd' if platform.system() == 'Windows' else 'npm'
    
    result = subprocess.run(
        [npm_cmd, 'run', 'build'],
        cwd=str(FRONTEND_DIR)
    )
    
    if result.returncode == 0:
        print(f"{Colors.GREEN}✅ Production version built{Colors.RESET}")
        print(f"{Colors.BLUE}📁 Location: {FRONTEND_DIR / 'dist'}{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Error building Frontend{Colors.RESET}")

# ============================================================
# Cache Cleaning
# ============================================================
def clean_cache():
    """Clean cache files"""
    print(f"\n{Colors.BLUE}🧹 Cleaning Cache Files...{Colors.RESET}")
    
    # Clean __pycache__ in backend
    for root, dirs, files in os.walk(BACKEND_DIR):
        for d in dirs:
            if d == "__pycache__":
                path = Path(root) / d
                try:
                    shutil.rmtree(path)
                    print(f"{Colors.GREEN}✅ Removed: {path}{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}❌ Error removing {path}: {e}{Colors.RESET}")
    
    # Clean .pytest_cache
    pytest_cache = BACKEND_DIR / ".pytest_cache"
    if pytest_cache.exists():
        try:
            shutil.rmtree(pytest_cache)
            print(f"{Colors.GREEN}✅ Removed: {pytest_cache}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    # Clean Frontend cache
    vite_cache = FRONTEND_DIR / "node_modules" / ".vite"
    if vite_cache.exists():
        try:
            shutil.rmtree(vite_cache)
            print(f"{Colors.GREEN}✅ Removed: {vite_cache}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    dist_dir = FRONTEND_DIR / "dist"
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
            print(f"{Colors.GREEN}✅ Removed: {dist_dir}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    # Clean logs
    if LOGS_DIR.exists():
        try:
            shutil.rmtree(LOGS_DIR)
            print(f"{Colors.GREEN}✅ Removed: {LOGS_DIR}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Cache cleaned successfully{Colors.RESET}")

# ============================================================
# Port Management
# ============================================================
def free_ports():
    """Free occupied ports"""
    print(f"\n{Colors.BLUE}🔧 Checking Occupied Ports...{Colors.RESET}")
    
    ports_to_check = [DEFAULT_BACKEND_PORT, DEFAULT_FRONTEND_PORT]
    
    for port in ports_to_check:
        if not is_port_available(port):
            print(f"{Colors.YELLOW}⚠️  Port {port} is occupied{Colors.RESET}")
            choice = input(f"Do you want to kill the process on port {port}? (y/n): ").strip().lower()
            if choice == 'y':
                if kill_process_on_port(port):
                    print(f"{Colors.GREEN}✅ Port {port} freed{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Could not kill process{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}✅ Port {port} is available{Colors.RESET}")

# ============================================================
# Log Viewing
# ============================================================
def view_logs():
    """View backend logs"""
    print(f"\n{Colors.BLUE}📊 Viewing Logs...{Colors.RESET}")
    
    log_file = LOGS_DIR / "backend.log"
    
    if not log_file.exists():
        print(f"{Colors.YELLOW}⚠️  No log file found: {log_file}{Colors.RESET}")
        print(f"{Colors.BLUE}💡 Run the backend first to generate logs{Colors.RESET}")
        return
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            print(f"{Colors.YELLOW}⚠️  Log file is empty{Colors.RESET}")
            return
        
        # Show last 50 lines
        print(f"\n{Colors.CYAN}--- Last 50 lines of {log_file.name} ---{Colors.RESET}")
        for line in lines[-50:]:
            print(line.rstrip())
        
        print(f"\n{Colors.CYAN}--- End of log ---{Colors.RESET}")
        print(f"{Colors.BLUE}📁 Full log: {log_file}{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading log file: {e}{Colors.RESET}")

# ============================================================
# Full Application
# ============================================================
def run_full():
    """Run full application (backend + frontend)"""
    print(f"\n{Colors.BLUE}🚀 Running Full Application...{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️  Press Ctrl+C to stop{Colors.RESET}\n")
    
    # Start Backend
    backend_process, backend_port = run_backend()
    
    if backend_process is None:
        print(f"{Colors.RED}❌ Backend failed to start{Colors.RESET}")
        return
    
    # Start Frontend
    frontend_process, frontend_port = run_frontend()
    
    if frontend_process is None:
        print(f"{Colors.RED}❌ Frontend failed to start{Colors.RESET}")
        backend_process.terminate()
        return
    
    print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}  ✅ Application is ready!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}  🌐 Frontend: http://localhost:{frontend_port}{Colors.RESET}")
    print(f"{Colors.BLUE}  🔌 Backend:  http://localhost:{backend_port}{Colors.RESET}")
    print(f"{Colors.BLUE}  📄 API Docs: http://localhost:{backend_port}/docs{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*70}{Colors.RESET}\n")
    
    try:
        # Wait for frontend to finish
        frontend_process.wait()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️  Stopping application...{Colors.RESET}")
    finally:
        # Stop processes
        print(f"{Colors.YELLOW}⏹️  Stopping Backend...{Colors.RESET}")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        
        print(f"{Colors.YELLOW}⏹️  Stopping Frontend...{Colors.RESET}")
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
        
        # On Windows, processes may still be running
        if platform.system() == 'Windows':
            time.sleep(1)
            kill_process_on_port(backend_port)
            kill_process_on_port(frontend_port)
        
        print(f"{Colors.GREEN}✅ Application stopped{Colors.RESET}")

# ============================================================
# Main Menu
# ============================================================
def main():
    """Main entry point"""
    while True:
        print_header()
        print_menu()
        
        choice = input(f"{Colors.CYAN}  Your choice: {Colors.RESET}").strip()
        
        if choice == '1':
            run_full()
        elif choice == '2':
            port_input = input(f"Backend port (default {DEFAULT_BACKEND_PORT}, Enter for auto): ").strip()
            port = int(port_input) if port_input else None
            process, actual_port = run_backend(port)
            if process:
                try:
                    print(f"{Colors.YELLOW}⏹️  Press Ctrl+C to stop{Colors.RESET}")
                    process.wait()
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}⏹️  Stopping Backend...{Colors.RESET}")
                    process.terminate()
        elif choice == '3':
            port_input = input(f"Frontend port (default {DEFAULT_FRONTEND_PORT}, Enter for auto): ").strip()
            port = int(port_input) if port_input else None
            process, actual_port = run_frontend(port)
            if process:
                try:
                    print(f"{Colors.YELLOW}⏹️  Press Ctrl+C to stop{Colors.RESET}")
                    process.wait()
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}⏹️  Stopping Frontend...{Colors.RESET}")
                    process.terminate()
        elif choice == '4':
            install_dependencies()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '5':
            run_tests()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '6':
            build_production()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '7':
            clean_cache()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '8':
            free_ports()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '9':
            view_logs()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '10':
            reset_database()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}❌ Invalid choice!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏹️  Application stopped{Colors.RESET}")
        sys.exit(0)