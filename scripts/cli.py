#!/usr/bin/env python3
# scripts/cli.py
"""
FarmTech-ProFertilizer - Docker Management Tool
Version: 2.0 - Docker Only
"""

import os
import sys
import subprocess
import platform
import time
import socket
import shutil
from pathlib import Path
from typing import Optional

# ============================================================
# Base Configuration
# ============================================================
BASE_DIR = Path(__file__).parent.parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
LOGS_DIR = BASE_DIR / "logs"

DEFAULT_BACKEND_PORT = 8000
DEFAULT_FRONTEND_PORT = 3000
DEFAULT_DB_PORT = 5432
DEFAULT_PGADMIN_PORT = 5050

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

def check_directory_exists(path: Path, name: str) -> bool:
    """Check if directory exists and print error if not"""
    if not path.exists():
        print(f"[ERROR] {name} directory not found: {path}")
        return False
    return True

def get_timestamp() -> str:
    """Get current timestamp for backup files"""
    return time.strftime("%Y%m%d_%H%M%S")


# ============================================================
# Docker Management Functions
# ============================================================

def docker_build_and_run():
    """Build and run with Docker Compose"""
    print("\n[INFO] Building and running with Docker Compose...")
    
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        print("[WARNING] .env file not found. Creating from .env.example...")
        env_example = BASE_DIR / ".env.example"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("[SUCCESS] .env created from .env.example")
        else:
            print("[ERROR] .env.example not found")
            return
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    print("[INFO] Building and starting containers...")
    result = subprocess.run(
        ["docker-compose", "up", "--build", "-d"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Docker containers started successfully!")
        print("")
        print("  Frontend: http://localhost:3000")
        print("  Backend:  http://localhost:8000")
        print("  API Docs: http://localhost:8000/docs")
        print("  Database: localhost:5432")
        print("  pgAdmin:  http://localhost:5050")
        print("       Email: admin@farmtech.com")
        print("       Password: admin")
        print("")
        print("Useful commands:")
        print("  docker-compose logs -f     # View logs")
        print("  docker-compose ps          # Check status")
        print("  docker-compose down        # Stop services")
        
        print("[INFO] Running migrations...")
        time.sleep(3)
        run_migrations()
    else:
        print("[ERROR] Docker build failed")


def docker_stop():
    """Stop and remove Docker containers"""
    print("\n[INFO] Stopping and removing Docker containers...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    result = subprocess.run(
        ["docker-compose", "down"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Docker containers stopped and removed")
    else:
        print("[ERROR] Failed to stop containers")


def docker_stop_keep_volumes():
    """Stop Docker containers but keep volumes"""
    print("\n[INFO] Stopping Docker containers (keeping volumes)...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    result = subprocess.run(
        ["docker-compose", "stop"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Docker containers stopped (volumes preserved)")
    else:
        print("[ERROR] Failed to stop containers")


def docker_start():
    """Start existing Docker containers"""
    print("\n[INFO] Starting Docker containers...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    result = subprocess.run(
        ["docker-compose", "start"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Docker containers started")
    else:
        print("[ERROR] Failed to start containers")


def docker_restart():
    """Restart Docker containers"""
    print("\n[INFO] Restarting Docker containers...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    result = subprocess.run(
        ["docker-compose", "restart"],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Docker containers restarted")
    else:
        print("[ERROR] Failed to restart containers")


def docker_restart_service(service: str):
    """Restart a specific service"""
    print(f"\n[INFO] Restarting {service}...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    result = subprocess.run(
        ["docker-compose", "restart", service],
        cwd=str(BASE_DIR)
    )
    
    if result.returncode == 0:
        print(f"[SUCCESS] {service} restarted")
    else:
        print(f"[ERROR] Failed to restart {service}")


def docker_status():
    """Show status of all containers"""
    print("\n[INFO] Container status:")
    print("")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    subprocess.run(
        ["docker-compose", "ps"],
        cwd=str(BASE_DIR)
    )


def docker_logs():
    """View Docker logs"""
    print("\n[INFO] Viewing Docker logs...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    subprocess.run(
        ["docker-compose", "logs", "-f", "--tail=50"],
        cwd=str(BASE_DIR)
    )


def docker_logs_service(service: str):
    """View logs for a specific service"""
    print(f"\n[INFO] Viewing logs for {service}...")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    subprocess.run(
        ["docker-compose", "logs", "-f", "--tail=50", service],
        cwd=str(BASE_DIR)
    )


def docker_pgadmin():
    """Start pgAdmin container"""
    print("\n[INFO] Starting pgAdmin...")
    
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "farmtech-pgadmin" in result.stdout:
        print("[WARNING] pgAdmin container already exists. Starting it...")
        subprocess.run(["docker", "start", "farmtech-pgadmin"], cwd=str(BASE_DIR))
    else:
        print("[INFO] Creating and starting pgAdmin container...")
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
    
    print("[SUCCESS] pgAdmin is ready!")
    print("  URL: http://localhost:5050")
    print("  Email: admin@farmtech.com")
    print("  Password: admin")
    print("")
    print("To connect to database, use:")
    print("  Host: db")
    print("  Port: 5432")
    print("  Database: farmtech_db")
    print("  Username: postgres")
    print("  Password: postgres")


def docker_exec_backend(cmd: str):
    """Execute command in backend container"""
    print(f"\n[INFO] Executing in backend: {cmd}")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    subprocess.run(
        ["docker-compose", "exec", "backend", "sh", "-c", cmd],
        cwd=str(BASE_DIR)
    )


def docker_exec_db(cmd: str):
    """Execute command in database container"""
    print(f"\n[INFO] Executing in database: {cmd}")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if not compose_file.exists():
        print("[ERROR] docker-compose.yml not found")
        return
    
    subprocess.run(
        ["docker-compose", "exec", "db", "sh", "-c", cmd],
        cwd=str(BASE_DIR)
    )


def clean_docker_volumes():
    """Clean Docker volumes"""
    print("\n[INFO] Cleaning Docker volumes...")
    
    confirm = input("[WARNING] This will remove ALL unused Docker volumes. Are you sure? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[INFO] Operation cancelled.")
        return
    
    subprocess.run(["docker", "volume", "prune", "-f"], cwd=str(BASE_DIR))
    print("[SUCCESS] Docker volumes cleaned")


def clean_docker_all():
    """Clean all Docker resources (containers, volumes, images)"""
    print("\n[INFO] Cleaning all Docker resources...")
    
    confirm = input("[WARNING] This will remove ALL containers, volumes, and images. Are you sure? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[INFO] Operation cancelled.")
        return
    
    # Stop and remove containers
    print("[INFO] Stopping and removing containers...")
    subprocess.run(["docker-compose", "down", "-v"], cwd=str(BASE_DIR))
    
    # Remove unused images
    print("[INFO] Removing unused images...")
    subprocess.run(["docker", "image", "prune", "-f"], cwd=str(BASE_DIR))
    
    print("[SUCCESS] All Docker resources cleaned")


def check_ports_status():
    """Check all ports status"""
    print("\n[INFO] Checking ports status...")
    
    ports = [
        (DEFAULT_BACKEND_PORT, "Backend"),
        (DEFAULT_FRONTEND_PORT, "Frontend"),
        (DEFAULT_DB_PORT, "Database"),
        (DEFAULT_PGADMIN_PORT, "pgAdmin")
    ]
    
    for port, name in ports:
        if is_port_available(port):
            print(f"  [OK] Port {port} ({name}) is available")
        else:
            print(f"  [FAIL] Port {port} ({name}) is occupied")


# ============================================================
# Database Functions
# ============================================================

def run_migrations():
    """Run database migrations"""
    print("\n[INFO] Running database migrations...")
    
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
    
    session_migrations = [
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45) DEFAULT NULL;",
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS user_agent VARCHAR(255) DEFAULT NULL;",
        "ALTER TABLE user_sessions ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
    ]
    
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
        for sql in user_migrations:
            _execute_sql(sql)
        
        for sql in session_migrations:
            _execute_sql(sql)
        
        for sql in new_tables:
            _execute_sql(sql)
        
        print("[SUCCESS] Database migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        return False


def _execute_sql(sql: str):
    """Execute SQL command on database"""
    try:
        cmd = [
            "docker-compose", "exec", "-T", "db", 
            "psql", "-U", "postgres", "-d", "farmtech_db",
            "-c", sql
        ]
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
        if result.returncode != 0 and "already exists" not in result.stderr:
            print(f"[WARNING] SQL Warning: {result.stderr}")
        return True
    except Exception as e:
        print(f"[WARNING] Could not execute SQL: {e}")
        return False


def reset_database():
    """Reset database with auto-migration"""
    print("\n[INFO] Resetting PostgreSQL Database with Auto-Migration...")
    
    try:
        subprocess.run(["docker", "ps"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Docker is not running or not installed")
        print("[INFO] Please install Docker and start Docker Desktop")
        return
    
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "farmtech-db" not in result.stdout:
        print("[WARNING] Database container not found. Please run Docker first.")
        return
    
    confirm = input("[WARNING] This will DELETE ALL DATA. Are you sure? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[INFO] Operation cancelled.")
        return
    
    print("[INFO] Stopping and removing database container...")
    subprocess.run(["docker-compose", "down", "-v"], cwd=str(BASE_DIR))
    
    print("[INFO] Starting fresh database container...")
    subprocess.run(["docker-compose", "up", "-d", "db"], cwd=str(BASE_DIR))
    
    print("[INFO] Waiting for database to be ready...")
    time.sleep(8)
    
    print("[INFO] Running migrations...")
    if not run_migrations():
        print("[ERROR] Migrations failed. Please check manually.")
        return
    
    print("[INFO] Initializing database with seed data...")
    subprocess.run(
        ["docker-compose", "exec", "backend", "python", "scripts/init_db.py"],
        cwd=str(BASE_DIR)
    )
    
    print("[SUCCESS] Database reset and migration completed successfully!")


def backup_database():
    """Backup PostgreSQL database"""
    print("\n[INFO] Backing up database...")
    
    try:
        subprocess.run(["docker", "ps"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Docker is not running or not installed")
        return
    
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "farmtech-db" not in result.stdout:
        print("[WARNING] Database container is not running.")
        return
    
    timestamp = get_timestamp()
    backup_dir = BASE_DIR / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"farmtech_backup_{timestamp}.sql"
    
    print(f"[INFO] Creating backup: {backup_file}")
    
    with open(backup_file, "w") as f:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "pg_dump", "-U", "postgres", "farmtech_db"],
            cwd=str(BASE_DIR),
            stdout=f,
            stderr=subprocess.PIPE
        )
    
    if result.returncode == 0:
        file_size = backup_file.stat().st_size / (1024 * 1024)
        print(f"[SUCCESS] Database backup completed!")
        print(f"  File: {backup_file}")
        print(f"  Size: {file_size:.2f} MB")
        
        # List all backups
        list_backups()
    else:
        print(f"[ERROR] Backup failed: {result.stderr.decode() if result.stderr else 'Unknown error'}")


def restore_database():
    """Restore PostgreSQL database from backup"""
    print("\n[INFO] Restoring database from backup...")
    
    backup_dir = BASE_DIR / "backups"
    if not backup_dir.exists():
        print("[ERROR] No backups directory found")
        return
    
    backups = sorted(backup_dir.glob("farmtech_backup_*.sql"), reverse=True)
    if not backups:
        print("[ERROR] No backup files found")
        return
    
    print("\n  Available backups:")
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / (1024 * 1024)
        print(f"  {i}. {backup.name} ({size:.2f} MB)")
    
    print("")
    choice = input("  Enter backup number to restore (0 to cancel): ").strip()
    
    if not choice.isdigit():
        print("[ERROR] Invalid choice")
        return
    
    idx = int(choice)
    if idx == 0:
        print("[INFO] Operation cancelled.")
        return
    
    if idx < 1 or idx > len(backups):
        print("[ERROR] Invalid backup number")
        return
    
    backup_file = backups[idx - 1]
    
    confirm = input(f"[WARNING] Restore from {backup_file.name}? This will OVERWRITE current data. (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[INFO] Operation cancelled.")
        return
    
    print(f"[INFO] Restoring from: {backup_file}")
    
    with open(backup_file, "r") as f:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "psql", "-U", "postgres", "farmtech_db"],
            cwd=str(BASE_DIR),
            stdin=f,
            stderr=subprocess.PIPE
        )
    
    if result.returncode == 0:
        print("[SUCCESS] Database restored successfully!")
    else:
        print(f"[ERROR] Restore failed: {result.stderr.decode() if result.stderr else 'Unknown error'}")


def list_backups():
    """List all available backups"""
    backup_dir = BASE_DIR / "backups"
    if not backup_dir.exists():
        print("[INFO] No backups found")
        return
    
    backups = sorted(backup_dir.glob("farmtech_backup_*.sql"), reverse=True)
    if not backups:
        print("[INFO] No backups found")
        return
    
    print("\n  Available backups:")
    total_size = 0
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / (1024 * 1024)
        total_size += size
        print(f"  {i}. {backup.name} ({size:.2f} MB)")
    
    print(f"\n  Total backups: {len(backups)}")
    print(f"  Total size: {total_size:.2f} MB")


def delete_backup():
    """Delete a backup file"""
    print("\n[INFO] Delete backup...")
    
    backup_dir = BASE_DIR / "backups"
    if not backup_dir.exists():
        print("[ERROR] No backups directory found")
        return
    
    backups = sorted(backup_dir.glob("farmtech_backup_*.sql"), reverse=True)
    if not backups:
        print("[ERROR] No backup files found")
        return
    
    print("\n  Available backups:")
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / (1024 * 1024)
        print(f"  {i}. {backup.name} ({size:.2f} MB)")
    
    print("")
    choice = input("  Enter backup number to delete (0 to cancel): ").strip()
    
    if not choice.isdigit():
        print("[ERROR] Invalid choice")
        return
    
    idx = int(choice)
    if idx == 0:
        print("[INFO] Operation cancelled.")
        return
    
    if idx < 1 or idx > len(backups):
        print("[ERROR] Invalid backup number")
        return
    
    backup_file = backups[idx - 1]
    confirm = input(f"[WARNING] Delete {backup_file.name}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[INFO] Operation cancelled.")
        return
    
    backup_file.unlink()
    print(f"[SUCCESS] Backup deleted: {backup_file.name}")


# ============================================================
# Display Functions
# ============================================================

def print_header():
    """Print application header"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print("=" * 70)
    print("  FarmTech - ProFertilizer Docker Management Tool")
    print("=" * 70)
    print(f"  Platform: {platform.system()}")
    print(f"  Project:  {BASE_DIR}")
    print("=" * 70)
    print()


def print_menu():
    """Print main menu"""
    print("  Please select an option:")
    print()
    print("  === DOCKER MANAGEMENT ===")
    print("  1  Build and Run")
    print("  2  Stop and Remove")
    print("  3  Stop (Keep Volumes)")
    print("  4  Start")
    print("  5  Restart All")
    print("  6  Restart Service")
    print("  7  Status")
    print("  8  View Logs")
    print("  9  View Service Logs")
    print(" 10  Start pgAdmin")
    print(" 11  Execute in Backend")
    print(" 12  Execute in Database")
    print("")
    print("  === DATABASE MANAGEMENT ===")
    print(" 13  Reset Database (with Auto-Migration)")
    print(" 14  Run Migrations")
    print(" 15  Backup Database")
    print(" 16  Restore Database")
    print(" 17  List Backups")
    print(" 18  Delete Backup")
    print("")
    print("  === CLEANUP ===")
    print(" 19  Clean Docker Volumes")
    print(" 20  Clean All (Containers + Volumes + Images)")
    print("")
    print("  === UTILITIES ===")
    print(" 21  Check Ports Status")
    print("")
    print("  0  Exit")
    print()


# ============================================================
# Main Menu
# ============================================================

def main():
    """Main entry point"""
    while True:
        print_header()
        print_menu()
        
        choice = input("  Your choice: ").strip()
        
        if choice == '1':
            docker_build_and_run()
            input("\nPress Enter to continue...")
        elif choice == '2':
            docker_stop()
            input("\nPress Enter to continue...")
        elif choice == '3':
            docker_stop_keep_volumes()
            input("\nPress Enter to continue...")
        elif choice == '4':
            docker_start()
            input("\nPress Enter to continue...")
        elif choice == '5':
            docker_restart()
            input("\nPress Enter to continue...")
        elif choice == '6':
            print("\n  Available services: backend, frontend, db, pgadmin")
            service = input("  Enter service name: ").strip()
            if service:
                docker_restart_service(service)
            input("\nPress Enter to continue...")
        elif choice == '7':
            docker_status()
            input("\nPress Enter to continue...")
        elif choice == '8':
            docker_logs()
            input("\nPress Enter to continue...")
        elif choice == '9':
            print("\n  Available services: backend, frontend, db, pgadmin")
            service = input("  Enter service name: ").strip()
            if service:
                docker_logs_service(service)
            input("\nPress Enter to continue...")
        elif choice == '10':
            docker_pgadmin()
            input("\nPress Enter to continue...")
        elif choice == '11':
            cmd = input("  Enter command to execute in backend: ").strip()
            if cmd:
                docker_exec_backend(cmd)
            input("\nPress Enter to continue...")
        elif choice == '12':
            cmd = input("  Enter command to execute in database: ").strip()
            if cmd:
                docker_exec_db(cmd)
            input("\nPress Enter to continue...")
        elif choice == '13':
            reset_database()
            input("\nPress Enter to continue...")
        elif choice == '14':
            run_migrations()
            input("\nPress Enter to continue...")
        elif choice == '15':
            backup_database()
            input("\nPress Enter to continue...")
        elif choice == '16':
            restore_database()
            input("\nPress Enter to continue...")
        elif choice == '17':
            list_backups()
            input("\nPress Enter to continue...")
        elif choice == '18':
            delete_backup()
            input("\nPress Enter to continue...")
        elif choice == '19':
            clean_docker_volumes()
            input("\nPress Enter to continue...")
        elif choice == '20':
            clean_docker_all()
            input("\nPress Enter to continue...")
        elif choice == '21':
            check_ports_status()
            input("\nPress Enter to continue...")
        elif choice == '0':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("[ERROR] Invalid choice!")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Application stopped")
        sys.exit(0)