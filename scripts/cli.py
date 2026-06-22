#!/usr/bin/env python3
# scripts/cli.py
"""Command Line Interface for FarmTech Project Management"""

import os
import sys
import subprocess
import platform
import time
from colorama import init, Fore, Style

# Enable colors on Windows
init(autoreset=True)

class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

def print_header():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}  🌱 FarmTech - ProFertilizer{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}  📍 {platform.system()} | Python {platform.python_version()}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def print_menu():
    print(f"{Colors.YELLOW}  Please select an option:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}{Colors.GREEN}1{Colors.RESET}  ▶️  Run Full Application (Backend + Frontend)")
    print(f"  {Colors.BOLD}{Colors.GREEN}2{Colors.RESET}  ▶️  Run Backend Only (FastAPI)")
    print(f"  {Colors.BOLD}{Colors.GREEN}3{Colors.RESET}  ▶️  Run Frontend Only (Vue)")
    print(f"  {Colors.BOLD}{Colors.GREEN}4{Colors.RESET}  ▶️  Install Dependencies")
    print(f"  {Colors.BOLD}{Colors.GREEN}5{Colors.RESET}  ▶️  Run Tests")
    print(f"  {Colors.BOLD}{Colors.GREEN}6{Colors.RESET}  ▶️  Build Production Version")
    print(f"  {Colors.BOLD}{Colors.GREEN}7{Colors.RESET}  ▶️  Clean Cache Files")
    print(f"  {Colors.BOLD}{Colors.RED}8{Colors.RESET}  ▶️  Exit")
    print()

def run_command(cmd, cwd=None, capture_output=False):
    """Execute command and display output"""
    try:
        if platform.system() == 'Windows':
            if capture_output:
                result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
                return result.stdout.strip() if result.returncode == 0 else None
            else:
                subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        else:
            if capture_output:
                result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
                return result.stdout.strip() if result.returncode == 0 else None
            else:
                subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Command execution failed: {e}{Colors.RESET}")
        return False

def find_npm():
    """Find npm executable path on Windows"""
    if platform.system() == 'Windows':
        # Try to find npm in common locations
        possible_paths = [
            'npm.cmd',
            'C:\\Program Files\\nodejs\\npm.cmd',
            'C:\\Program Files (x86)\\nodejs\\npm.cmd',
            os.path.expanduser('~\\AppData\\Roaming\\npm\\npm.cmd')
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        # Try using where command
        result = run_command('where npm', capture_output=True)
        if result:
            return result.strip()
    return 'npm'

def run_backend():
    print(f"\n{Colors.BLUE}🚀 Starting Backend...{Colors.RESET}")
    os.chdir('backend')
    run_command('uvicorn app.main:app --reload --host 0.0.0.0 --port 8000')
    os.chdir('..')

def run_frontend():
    print(f"\n{Colors.BLUE}🚀 Starting Frontend...{Colors.RESET}")
    os.chdir('frontend')
    if platform.system() == 'Windows':
        run_command('npm run dev')
    else:
        run_command('npm run dev')
    os.chdir('..')

def install_dependencies():
    print(f"\n{Colors.BLUE}📦 Installing Dependencies...{Colors.RESET}")
    
    # Backend
    print(f"{Colors.YELLOW}📦 Installing Backend Dependencies...{Colors.RESET}")
    os.chdir('backend')
    if platform.system() == 'Windows':
        run_command('python -m venv venv')
        run_command('venv\\Scripts\\activate && pip install -r requirements.txt')
    else:
        run_command('python3 -m venv venv')
        run_command('source venv/bin/activate && pip install -r requirements.txt')
    os.chdir('..')
    
    # Frontend
    print(f"{Colors.YELLOW}📦 Installing Frontend Dependencies...{Colors.RESET}")
    os.chdir('frontend')
    run_command('npm install')
    os.chdir('..')
    
    print(f"{Colors.GREEN}✅ All dependencies installed successfully!{Colors.RESET}")

def run_tests():
    print(f"\n{Colors.BLUE}🧪 Running Tests...{Colors.RESET}")
    os.chdir('backend')
    if platform.system() == 'Windows':
        run_command('venv\\Scripts\\activate && python tests/test_all.py')
    else:
        run_command('source venv/bin/activate && python tests/test_all.py')
    os.chdir('..')

def build_production():
    print(f"\n{Colors.BLUE}🏗️ Building Production Version...{Colors.RESET}")
    
    # Backend
    print(f"{Colors.YELLOW}📦 Preparing Backend...{Colors.RESET}")
    os.chdir('backend')
    if platform.system() == 'Windows':
        run_command('venv\\Scripts\\activate && pip freeze > requirements.txt')
    else:
        run_command('source venv/bin/activate && pip freeze > requirements.txt')
    os.chdir('..')
    
    # Frontend
    print(f"{Colors.YELLOW}📦 Building Frontend...{Colors.RESET}")
    os.chdir('frontend')
    run_command('npm run build')
    os.chdir('..')
    
    print(f"{Colors.GREEN}✅ Production version built successfully!{Colors.RESET}")

def clean_cache():
    print(f"\n{Colors.BLUE}🧹 Cleaning Cache Files...{Colors.RESET}")
    
    # Python cache
    run_command('find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true')
    run_command('find . -type f -name "*.pyc" -delete 2>/dev/null || true')
    
    # Frontend cache
    os.chdir('frontend')
    run_command('rm -rf node_modules/.vite 2>/dev/null || true')
    run_command('rm -rf dist 2>/dev/null || true')
    os.chdir('..')
    
    # Backend cache
    os.chdir('backend')
    run_command('rm -rf .pytest_cache 2>/dev/null || true')
    os.chdir('..')
    
    print(f"{Colors.GREEN}✅ Cache cleaned successfully!{Colors.RESET}")

def run_full():
    print(f"\n{Colors.BLUE}🚀 Running Full Application...{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️ Press Ctrl+C to stop{Colors.RESET}")
    
    # Start Backend in background
    print(f"{Colors.GREEN}▶️  Starting Backend...{Colors.RESET}")
    os.chdir('backend')
    if platform.system() == 'Windows':
        backend_process = subprocess.Popen(
            'uvicorn app.main:app --reload --host 0.0.0.0 --port 8000',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        backend_process = subprocess.Popen(
            ['uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    os.chdir('..')
    
    time.sleep(3)
    print(f"{Colors.GREEN}✅ Backend running on http://localhost:8000{Colors.RESET}")
    
    # Start Frontend
    print(f"{Colors.GREEN}▶️  Starting Frontend...{Colors.RESET}")
    os.chdir('frontend')
    if platform.system() == 'Windows':
        frontend_process = subprocess.Popen(
            'npm run dev',
            shell=True
        )
    else:
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev']
        )
    os.chdir('..')
    
    try:
        frontend_process.wait()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏹️  Stopping application...{Colors.RESET}")
        backend_process.terminate()
        frontend_process.terminate()

def main():
    while True:
        print_header()
        print_menu()
        
        choice = input(f"{Colors.CYAN}  Your choice: {Colors.RESET}")
        
        if choice == '1':
            run_full()
        elif choice == '2':
            run_backend()
        elif choice == '3':
            run_frontend()
        elif choice == '4':
            install_dependencies()
        elif choice == '5':
            run_tests()
        elif choice == '6':
            build_production()
        elif choice == '7':
            clean_cache()
        elif choice == '8':
            print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}❌ Invalid choice!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏹️  Application stopped.{Colors.RESET}")
        sys.exit(0)