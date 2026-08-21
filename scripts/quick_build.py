#!/usr/bin/env python3
# scripts/quick_build.py
"""
FarmTech - Quick Docker Builder
Version: 3.0 - Fast & Lightweight
"""

import os
import sys
import subprocess
import platform
import time
import shutil
from pathlib import Path

# ============================================================
# Configuration
# ============================================================
BASE_DIR = Path(__file__).parent.parent.absolute()
COMPOSE_FILE = BASE_DIR / "docker-compose.yml"
ENV_FILE = BASE_DIR / ".env"
ENV_EXAMPLE = BASE_DIR / ".env.example"

# ============================================================
# Helper Functions
# ============================================================

def print_header():
    """Print simple header"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print("=" * 60)
    print("  🚀 FarmTech - Quick Docker Builder")
    print("=" * 60)
    print(f"  Project: {BASE_DIR.name}")
    print("=" * 60)
    print()

def check_prerequisites():
    """Check if Docker and required files exist"""
    # Check Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Docker is not installed or not running!")
        print("[INFO] Please install Docker Desktop and start it.")
        return False
    
    # Check docker-compose.yml
    if not COMPOSE_FILE.exists():
        print(f"[ERROR] docker-compose.yml not found at: {COMPOSE_FILE}")
        return False
    
    # Check/create .env
    if not ENV_FILE.exists():
        if ENV_EXAMPLE.exists():
            print("[INFO] Creating .env from .env.example...")
            shutil.copy(ENV_EXAMPLE, ENV_FILE)
            print("[SUCCESS] .env created!")
        else:
            print("[WARNING] No .env or .env.example found. Creating minimal .env...")
            with open(ENV_FILE, 'w') as f:
                f.write("""# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=farmtech_db

# Backend Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""")
            print("[SUCCESS] .env created with default values!")
    
    return True

# ============================================================
# Fast Build Functions
# ============================================================

def fast_build():
    """Build and run with maximum speed using cache"""
    print("\n[INFO] 🔨 Starting fast build with Docker cache...")
    print("[INFO] Using BuildKit for faster builds...")
    print("[INFO] Docker images will be cached for future runs\n")
    
    # Set BuildKit environment variable for faster builds
    env = os.environ.copy()
    env["DOCKER_BUILDKIT"] = "1"
    env["COMPOSE_DOCKER_CLI_BUILD"] = "1"
    env["BUILDKIT_PROGRESS"] = "plain"
    
    # Build with cache
    print("[1/3] Building images (using cache)...")
    build_result = subprocess.run(
        ["docker-compose", "build", "--parallel"],
        cwd=str(BASE_DIR),
        env=env
    )
    
    if build_result.returncode != 0:
        print("[ERROR] Build failed!")
        return False
    
    # Start containers
    print("\n[2/3] Starting containers...")
    start_result = subprocess.run(
        ["docker-compose", "up", "-d"],
        cwd=str(BASE_DIR),
        env=env
    )
    
    if start_result.returncode != 0:
        print("[ERROR] Failed to start containers!")
        return False
    
    # Wait for services to be ready
    print("\n[3/3] Waiting for services to be ready...")
    time.sleep(5)
    
    # Check status
    print("\n" + "=" * 60)
    print("  ✅ SUCCESS! Containers are running")
    print("=" * 60)
    print()
    print("  📍 Services:")
    print("  ─────────────────────────────────────")
    print("  🌐 Frontend:  http://localhost:3000")
    print("  🖥️  Backend:   http://localhost:8000")
    print("  📚 API Docs:  http://localhost:8000/docs")
    print("  🗄️  Database:  localhost:5432")
    print("  📊 pgAdmin:   http://localhost:5050")
    print()
    print("  🔑 Default Credentials:")
    print("  ─────────────────────────────────────")
    print("  Email:    admin@farmtech.com")
    print("  Password: admin")
    print()
    print("  💡 Useful Commands:")
    print("  ─────────────────────────────────────")
    print("  docker-compose logs -f     # View logs")
    print("  docker-compose ps          # Check status")
    print("  docker-compose down        # Stop services")
    print("=" * 60)
    
    return True

def quick_build_without_backend_build():
    """Skip backend build if possible (for faster startup)"""
    print("\n[INFO] ⚡ Quick start - using existing images if available...")
    
    env = os.environ.copy()
    env["DOCKER_BUILDKIT"] = "1"
    
    # Try to start existing containers first
    print("[1/2] Trying to start existing containers...")
    start_result = subprocess.run(
        ["docker-compose", "up", "-d"],
        cwd=str(BASE_DIR),
        env=env
    )
    
    if start_result.returncode == 0:
        print("[SUCCESS] Containers started successfully!")
        print("\n  🌐 Frontend: http://localhost:3000")
        print("  🖥️  Backend:  http://localhost:8000")
        return True
    
    # If failed, build from scratch
    print("[2/2] No existing containers found. Building from scratch...")
    return fast_build()

def run_migrations_fast():
    """Run migrations quickly"""
    print("\n[INFO] Running database migrations...")
    
    # Simple migration check
    result = subprocess.run(
        ["docker-compose", "exec", "-T", "backend", "python", "-c", 
         "import sys; sys.path.append('/app'); from app.database import engine, Base; Base.metadata.create_all(bind=engine)"],
        cwd=str(BASE_DIR),
        capture_output=True
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Migrations completed!")
    else:
        print("[WARNING] Migrations may have issues, but containers are running.")
        print("[INFO] You can run migrations manually using option 14.")

# ============================================================
# Main Function
# ============================================================

def main():
    """Main entry point"""
    print_header()
    
    # Check prerequisites
    if not check_prerequisites():
        input("\nPress Enter to exit...")
        return
    
    # Ask user which mode
    print("\n  Select build mode:")
    print("  ─────────────────────────────")
    print("  1. Full build (use cache)")
    print("  2. Quick start (skip build if possible)")
    print("  3. Clean build (no cache)")
    print()
    
    choice = input("  Your choice (1-3, default: 1): ").strip() or "1"
    
    if choice == "3":
        # Clean build - remove cache
        print("\n[INFO] Performing clean build...")
        subprocess.run(["docker-compose", "build", "--no-cache", "--parallel"], cwd=str(BASE_DIR))
        build_success = True
    elif choice == "2":
        build_success = quick_build_without_backend_build()
    else:
        build_success = fast_build()
    
    if not build_success:
        print("\n[ERROR] Build failed!")
        input("\nPress Enter to exit...")
        return
    
    # Run migrations
    run_migrations_fast()
    
    print("\n" + "=" * 60)
    print("  🎉 All done! System is ready.")
    print("=" * 60)
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)