#!/usr/bin/env python3
# scripts/cli.py
"""
FarmTech-ProFertilizer - CLI Management Tool
Complete version with Docker support and PostgreSQL integration
Version: 2.0 - با قابلیت Migration خودکار
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
import tempfile
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
BASE_DIR = Path(__file__).parent.parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
LOGS_DIR = BASE_DIR / "logs"
SCRIPTS_DIR = BASE_DIR / "scripts"
MIGRATIONS_DIR = BASE_DIR / "migrations"

DEFAULT_BACKEND_PORT = 8000
DEFAULT_FRONTEND_PORT = 3000
DEFAULT_DB_PORT = 5432
DEFAULT_PGADMIN_PORT = 5050

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
# 🔧 Database Migration Functions (جدید)
# ============================================================

def run_migrations():
    """
    اجرای migration‌ها برای به‌روزرسانی دیتابیس
    این تابع فیلدهای جدید را به جدول‌های موجود اضافه می‌کند
    """
    print(f"\n{Colors.BLUE}🔄 Running database migrations...{Colors.RESET}")
    
    # SQL برای اضافه کردن فیلدهای جدید به جدول users
    user_migrations = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_attempts INTEGER DEFAULT 0;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP DEFAULT NULL;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_2fa_enabled BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS totp_secret VARCHAR(255) DEFAULT NULL;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS backup_codes JSON DEFAULT NULL;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP DEFAULT NULL;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_ip VARCHAR(45) DEFAULT NULL;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_user_agent VARCHAR(255) DEFAULT NULL;",
    ]
    
    # SQL برای اضافه کردن فیلدهای جدید به جدول user_sessions
    session_migrations = [
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45) DEFAULT NULL;",
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS user_agent VARCHAR(255) DEFAULT NULL;",
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
    ]
    
    # SQL برای ایجاد جدول‌های جدید
    new_tables = [
        """
        CREATE TABLE IF NOT EXISTS security_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            event_type VARCHAR(50) NOT NULL,
            severity VARCHAR(20) DEFAULT 'INFO',
            ip_address VARCHAR(45),
            user_agent VARCHAR(255),
            endpoint VARCHAR(255),
            method VARCHAR(10),
            details JSON,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token VARCHAR(255) UNIQUE NOT NULL,
            is_used BOOLEAN DEFAULT FALSE,
            ip_address VARCHAR(45),
            user_agent VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS optimization_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
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
            is_successful BOOLEAN DEFAULT TRUE,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    try:
        # اجرای migration‌ها روی دیتابیس
        for sql in user_migrations:
            _execute_sql(sql)
        
        for sql in session_migrations:
            _execute_sql(sql)
        
        for sql in new_tables:
            _execute_sql(sql)
        
        print(f"{Colors.GREEN}✅ Database migrations completed successfully!{Colors.RESET}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Migration failed: {e}{Colors.RESET}")
        return False


def _execute_sql(sql: str):
    """
    اجرای یک دستور SQL روی دیتابیس
    """
    try:
        cmd = [
            "docker-compose", "exec", "-T", "db", 
            "psql", "-U", "postgres", "-d", "farmtech_db",
            "-c", sql
        ]
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
        if result.returncode != 0 and "already exists" not in result.stderr:
            print(f"{Colors.YELLOW}⚠️ SQL Warning: {result.stderr}{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️ Could not execute SQL: {e}{Colors.RESET}")
        return False


# ============================================================
# 🔧 Database Reset Improved (بهبود یافته)
# ============================================================

def reset_database_improved():
    """
    ریست کامل دیتابیس با Migration خودکار
    """
    print(f"\n{Colors.BLUE}🗄️  Resetting PostgreSQL Database with Auto-Migration...{Colors.RESET}")
    
    # Check if docker is running
    try:
        subprocess.run(["docker", "ps"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}❌ Docker is not running or not installed{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 Please install Docker and start Docker Desktop{Colors.RESET}")
        return
    
    # Check if db container exists
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "farmtech-db" not in result.stdout:
        print(f"{Colors.YELLOW}⚠️  Database container not found. Please run Docker first.{Colors.RESET}")
        return
    
    # Confirm reset
    confirm = input(f"{Colors.YELLOW}⚠️  This will DELETE ALL DATA. Are you sure? (yes/no): {Colors.RESET}").strip().lower()
    if confirm != 'yes':
        print(f"{Colors.GREEN}❌ Operation cancelled.{Colors.RESET}")
        return
    
    # Stop and remove db container with volumes
    print(f"{Colors.YELLOW}⏳ Stopping and removing database container...{Colors.RESET}")
    subprocess.run(["docker-compose", "down", "-v"], cwd=str(BASE_DIR))
    
    # Start fresh
    print(f"{Colors.YELLOW}⏳ Starting fresh database container...{Colors.RESET}")
    subprocess.run(["docker-compose", "up", "-d", "db"], cwd=str(BASE_DIR))
    
    # Wait for db to be ready
    print(f"{Colors.YELLOW}⏳ Waiting for database to be ready...{Colors.RESET}")
    time.sleep(8)
    
    # Run migrations first (ایجاد جدول‌ها با فیلدهای جدید)
    print(f"{Colors.YELLOW}⏳ Running migrations...{Colors.RESET}")
    if not run_migrations():
        print(f"{Colors.RED}❌ Migrations failed. Please check manually.{Colors.RESET}")
        return
    
    # Initialize database with seed data
    print(f"{Colors.YELLOW}⏳ Initializing database with seed data...{Colors.RESET}")
    subprocess.run(
        ["docker-compose", "exec", "backend", "python", "scripts/init_db.py"],
        cwd=str(BASE_DIR)
    )
    
    print(f"{Colors.GREEN}✅ Database reset and migration completed successfully!{Colors.RESET}")


# ============================================================
# Display Functions
# ============================================================
def print_header():
    """Print application header"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}  🌱 FarmTech - ProFertilizer Management Tool v2.0{Colors.RESET}")
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
    print(f"  {Colors.BOLD}{Colors.MAGENTA}10{Colors.RESET} 🗄️  Reset Database (با Migration خودکار)")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}11{Colors.RESET} 🐳  Docker: Build and Run")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}12{Colors.RESET} 🐳  Docker: Stop and Remove")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}13{Colors.RESET} 🐳  Docker: View Logs")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}14{Colors.RESET} 🐘  Docker: Start pgAdmin")
    print(f"  {Colors.BOLD}{Colors.MAGENTA}15{Colors.RESET} 🔄  Run Migrations (به‌روزرسانی دیتابیس)")
    print(f"  {Colors.BOLD}{Colors.RED}0{Colors.RESET}  🚪 Exit")
    print()


# ============================================================
# Docker Management Functions
# ============================================================
def docker_build_and_run():
    """Build and run with Docker Compose"""
    print(f"\n{Colors.BLUE}🐳 Building and running with Docker Compose...{Colors.RESET}")
    
    # Check if .env exists
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        print(f"{Colors.YELLOW}⚠️  .env file not found. Creating from .env.example...{Colors.RESET}")
        env_example = BASE_DIR / ".env.example"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"{Colors.GREEN}✅ .env created from .env.example{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ .env.example not found{Colors.RESET}")
            return
    
    # Check docker-compose.yml
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print(f"{Colors.RED}❌ docker-compose.yml not found{Colors.RESET}")
        return
    
    # Build and run
    print(f"{Colors.YELLOW}⏳ Building and starting containers...{Colors.RESET}")
    result = subprocess.run(
        ["docker-compose", "up", "--build", "-d"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print(f"{Colors.GREEN}✅ Docker containers started successfully!{Colors.RESET}")
        print(f"\n{Colors.BLUE}  🌐 Frontend: http://localhost:3000{Colors.RESET}")
        print(f"{Colors.BLUE}  🔌 Backend:  http://localhost:8000{Colors.RESET}")
        print(f"{Colors.BLUE}  📄 API Docs: http://localhost:8000/docs{Colors.RESET}")
        print(f"{Colors.BLUE}  🗄️  Database: localhost:5432{Colors.RESET}")
        print(f"{Colors.BLUE}  🐘  pgAdmin:  http://localhost:5050{Colors.RESET}")
        print(f"{Colors.BLUE}       Email: admin@farmtech.com{Colors.RESET}")
        print(f"{Colors.BLUE}       Password: admin{Colors.RESET}")
        print(f"\n{Colors.YELLOW}📋 Useful commands:{Colors.RESET}")
        print(f"  docker-compose logs -f     # View logs")
        print(f"  docker-compose ps          # Check status")
        print(f"  docker-compose down        # Stop services")
        
        # Run migrations after startup
        print(f"\n{Colors.YELLOW}⏳ Running migrations...{Colors.RESET}")
        time.sleep(3)
        run_migrations()
    else:
        print(f"{Colors.RED}❌ Docker build failed{Colors.RESET}")

def docker_stop():
    """Stop and remove Docker containers"""
    print(f"\n{Colors.BLUE}🐳 Stopping and removing Docker containers...{Colors.RESET}")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print(f"{Colors.RED}❌ docker-compose.yml not found{Colors.RESET}")
        return
    
    result = subprocess.run(
        ["docker-compose", "down"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print(f"{Colors.GREEN}✅ Docker containers stopped and removed{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Failed to stop containers{Colors.RESET}")

def docker_logs():
    """View Docker logs"""
    print(f"\n{Colors.BLUE}🐳 Viewing Docker logs...{Colors.RESET}")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print(f"{Colors.RED}❌ docker-compose.yml not found{Colors.RESET}")
        return
    
    subprocess.run(
        ["docker-compose", "logs", "-f", "--tail=50"],
        cwd=str(BASE_DIR)
    )

def docker_pgadmin():
    """Start pgAdmin container"""
    print(f"\n{Colors.BLUE}🐘 Starting pgAdmin...{Colors.RESET}")
    
    # Check if pgadmin container already exists
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "farmtech-pgadmin" in result.stdout:
        print(f"{Colors.YELLOW}⚠️  pgAdmin container already exists. Starting it...{Colors.RESET}")
        subprocess.run(["docker", "start", "farmtech-pgadmin"], cwd=str(BASE_DIR))
    else:
        print(f"{Colors.YELLOW}⏳ Creating and starting pgAdmin container...{Colors.RESET}")
        subprocess.run([
            "docker", "run", "-d",
            "--name", "farmtech-pgadmin",
            "-p", "5050:80",
            "-e", "PGADMIN_DEFAULT_EMAIL=admin@farmtech.com",
            "-e", "PGADMIN_DEFAULT_PASSWORD=admin",
            "-e", "PGADMIN_CONFIG_SERVER_MODE=False",
            "-e", "PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED=False",
            "--network", "farmtech-profertilizer_farmtech-network",
            "--restart", "unless-stopped",
            "dpage/pgadmin4:latest"
        ], cwd=str(BASE_DIR))
    
    print(f"{Colors.GREEN}✅ pgAdmin is ready!{Colors.RESET}")
    print(f"{Colors.BLUE}  🌐 http://localhost:5050{Colors.RESET}")
    print(f"{Colors.BLUE}  📧 Email: admin@farmtech.com{Colors.RESET}")
    print(f"{Colors.BLUE}  🔑 Password: admin{Colors.RESET}")
    print(f"{Colors.YELLOW}💡 To connect to database, use:{Colors.RESET}")
    print(f"  Host: db{Colors.RESET}")
    print(f"  Port: 5432{Colors.RESET}")
    print(f"  Database: farmtech_db{Colors.RESET}")
    print(f"  Username: postgres{Colors.RESET}")
    print(f"  Password: postgres{Colors.RESET}")


# ============================================================
# Backend Functions
# ============================================================
def run_backend(port: Optional[int] = None, show_logs: bool = True) -> Tuple[Optional[subprocess.Popen], int]:
    """Run backend server and return process and port"""
    ensure_logs_dir()
    
    if not check_directory_exists(BACKEND_DIR, "Backend"):
        return None, 0
    
    python_exe = get_python_executable()
    if not Path(python_exe).exists():
        print(f"{Colors.YELLOW}⚠️  Virtual environment not found. Installing dependencies...{Colors.RESET}")
        install_dependencies_backend()
        python_exe = get_python_executable()
    
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
    
    cmd = [
        python_exe, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
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
    
    print(f"{Colors.YELLOW}⏳ Waiting for Backend to start...{Colors.RESET}")
    if wait_for_service(f"http://localhost:{port}/health", timeout=30):
        print(f"{Colors.GREEN}✅ Backend is ready: http://localhost:{port}{Colors.RESET}")
        if show_logs:
            print(f"{Colors.BLUE}📄 Logs: {log_file}{Colors.RESET}")
        return process, port
    else:
        print(f"{Colors.RED}❌ Backend failed to start. Please check logs:{Colors.RESET}")
        print(f"{Colors.BLUE}   {log_file}{Colors.RESET}")
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
    if not check_directory_exists(FRONTEND_DIR, "Frontend"):
        return None, 0
    
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print(f"{Colors.YELLOW}⚠️  node_modules not found. Installing dependencies...{Colors.RESET}")
        install_dependencies_frontend()
    
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
    
    env = os.environ.copy()
    env['PORT'] = str(port)
    
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
    
    venv_dir = BACKEND_DIR / "venv"
    if not venv_dir.exists():
        print(f"{Colors.BLUE}🔧 Creating virtual environment...{Colors.RESET}")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
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
    
    npm_cmd = 'npm.cmd' if platform.system() == 'Windows' else 'npm'
    try:
        subprocess.run([npm_cmd, '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}❌ npm not found. Please install Node.js{Colors.RESET}")
        return
    
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
    
    print(f"{Colors.YELLOW}⏳ Starting Backend for tests...{Colors.RESET}")
    backend_process, backend_port = run_backend(show_logs=False)
    
    if backend_process is None:
        print(f"{Colors.RED}❌ Backend failed to start. Tests cannot run{Colors.RESET}")
        return
    
    try:
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
    
    for root, dirs, files in os.walk(BACKEND_DIR):
        for d in dirs:
            if d == "__pycache__":
                path = Path(root) / d
                try:
                    shutil.rmtree(path)
                    print(f"{Colors.GREEN}✅ Removed: {path}{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}❌ Error removing {path}: {e}{Colors.RESET}")
    
    pytest_cache = BACKEND_DIR / ".pytest_cache"
    if pytest_cache.exists():
        try:
            shutil.rmtree(pytest_cache)
            print(f"{Colors.GREEN}✅ Removed: {pytest_cache}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
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
    
    ports_to_check = [DEFAULT_BACKEND_PORT, DEFAULT_FRONTEND_PORT, DEFAULT_DB_PORT, DEFAULT_PGADMIN_PORT]
    
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
    
    backend_process, backend_port = run_backend()
    
    if backend_process is None:
        print(f"{Colors.RED}❌ Backend failed to start{Colors.RESET}")
        return
    
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
        frontend_process.wait()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️  Stopping application...{Colors.RESET}")
    finally:
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
            reset_database_improved()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '11':
            docker_build_and_run()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '12':
            docker_stop()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '13':
            docker_logs()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '14':
            docker_pgadmin()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        elif choice == '15':
            run_migrations()
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