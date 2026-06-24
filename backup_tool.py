#!/usr/bin/env python3
"""
FarmTech-ProFertilizer Backup & Code Aggregation Tool
This script provides:
1. ZIP backup of the project (excluding unnecessary files)
2. Code aggregation - combines all code files into a single text file
3. Database export - export SQLite database to JSON, SQL, CSV, or TXT
"""

import os
import shutil
import zipfile
import datetime
import argparse
import sys
import json
import csv
import sqlite3
from pathlib import Path
from typing import List, Set, Dict, Any, Optional

# ======================== CONFIGURATION ========================
PROJECT_DIR = Path(__file__).parent.absolute()
BACKUP_DIR = PROJECT_DIR.parent / "FarmTech_Backups"
DB_PATH = PROJECT_DIR / "backend" / "farmtech.db"

# Files and folders to EXCLUDE
EXCLUDE_DIRS = [
    "venv", "env", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".vite", "dist", "build", ".next", ".nuxt",
    ".git", ".idea", ".vscode", "logs", "temp", "tmp", "backup",
    "farmtech.db", "*.db", "*.sqlite3", ".DS_Store", "Thumbs.db",
    "coverage", ".nyc_output", "out", "target",
]

EXCLUDE_FILES = [
    ".env", "*.pyc", "*.pyo", "*.log", "*.pid",
    "package-lock.json", "yarn.lock", "poetry.lock",
    "*.min.js", "*.min.css", "*.map", "*.ico",
]

# File extensions to include in code aggregation
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', 
    '.scss', '.sass', '.less', '.json', '.xml', '.yaml', '.yml',
    '.toml', '.ini', '.cfg', '.conf', '.sh', '.bash', '.bat',
    '.sql', '.sqlite', '.md', '.txt', '.rst', '.env.example',
    '.gitignore', '.dockerignore', '.eslintrc', '.prettierrc',
}

# ======================== DATABASE FUNCTIONS ========================

def get_db_connection():
    """Create connection to SQLite database."""
    if not DB_PATH.exists():
        print(f"❌ Database file not found at: {DB_PATH}")
        return None
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def get_all_tables(conn) -> List[str]:
    """Get list of all tables in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    return tables

def get_table_data(conn, table_name: str) -> List[Dict[str, Any]]:
    """Get all data from a table."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_table_schema(conn, table_name: str) -> str:
    """Get CREATE TABLE statement for a table."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    return result[0] if result else ""

def export_db_to_json(output_file: Path) -> bool:
    """Export database to JSON format."""
    print(f"\n📤 Exporting database to JSON...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        tables = get_all_tables(conn)
        data = {}
        
        for table in tables:
            data[table] = get_table_data(conn, table)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Database exported to JSON: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return False
    finally:
        conn.close()

def export_db_to_sql(output_file: Path) -> bool:
    """Export database to SQL dump format."""
    print(f"\n📤 Exporting database to SQL...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        tables = get_all_tables(conn)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- ============================================================\n")
            f.write(f"-- Database Export: farmtech.db\n")
            f.write(f"-- Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- ============================================================\n\n")
            
            # Write schema
            f.write("-- ============================================================\n")
            f.write("-- SCHEMA\n")
            f.write("-- ============================================================\n\n")
            
            for table in tables:
                schema = get_table_schema(conn, table)
                if schema:
                    f.write(f"{schema};\n\n")
            
            # Write data
            f.write("-- ============================================================\n")
            f.write("-- DATA\n")
            f.write("-- ============================================================\n\n")
            
            f.write("PRAGMA foreign_keys=OFF;\n\n")
            f.write("BEGIN TRANSACTION;\n\n")
            
            for table in tables:
                rows = get_table_data(conn, table)
                if not rows:
                    continue
                
                columns = list(rows[0].keys())
                column_names = ', '.join(f'"{col}"' for col in columns)
                
                f.write(f"-- Table: {table}\n")
                
                for row in rows:
                    values = []
                    for col in columns:
                        val = row[col]
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, (dict, list)):
                            json_str = json.dumps(val, ensure_ascii=False)
                            escaped = json_str.replace("'", "''")
                            values.append(f"'{escaped}'")
                        else:
                            escaped = str(val).replace("'", "''")
                            values.append(f"'{escaped}'")
                    
                    values_str = ', '.join(values)
                    f.write(f"INSERT INTO \"{table}\" ({column_names}) VALUES ({values_str});\n")
                
                f.write("\n")
            
            f.write("\nCOMMIT;\n\n")
            f.write("PRAGMA foreign_keys=ON;\n")
        
        print(f"✅ Database exported to SQL: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error exporting to SQL: {e}")
        return False
    finally:
        conn.close()

def export_db_to_csv(output_dir: Path) -> bool:
    """Export database to CSV format (one file per table)."""
    print(f"\n📤 Exporting database to CSV...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        tables = get_all_tables(conn)
        exported = 0
        
        for table in tables:
            rows = get_table_data(conn, table)
            if not rows:
                continue
            
            csv_file = output_dir / f"{table}.csv"
            columns = list(rows[0].keys())
            
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=columns, delimiter=',')
                writer.writeheader()
                
                for row in rows:
                    # Convert all values to string for CSV
                    row_data = {}
                    for col in columns:
                        val = row[col]
                        if val is None:
                            row_data[col] = ''
                        elif isinstance(val, (dict, list)):
                            row_data[col] = json.dumps(val, ensure_ascii=False)
                        else:
                            row_data[col] = str(val)
                    writer.writerow(row_data)
            
            exported += 1
            print(f"  ✅ Table '{table}' → {csv_file}")
        
        print(f"✅ {exported} tables exported to CSV in: {output_dir}")
        return True
    
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False
    finally:
        conn.close()

def export_db_to_txt(output_file: Path) -> bool:
    """Export database to human-readable TXT format."""
    print(f"\n📤 Exporting database to TXT...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        tables = get_all_tables(conn)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("DATABASE EXPORT REPORT\n")
            f.write(f"Database: {DB_PATH}\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total tables: {len(tables)}\n")
            f.write("=" * 80 + "\n\n")
            
            for table in tables:
                rows = get_table_data(conn, table)
                
                f.write(f"\n{'='*80}\n")
                f.write(f"TABLE: {table}\n")
                f.write(f"Total rows: {len(rows)}\n")
                f.write(f"{'='*80}\n\n")
                
                if not rows:
                    f.write("(Empty table)\n\n")
                    continue
                
                columns = list(rows[0].keys())
                
                # Determine column widths
                col_widths = {}
                for col in columns:
                    max_width = len(col)
                    for row in rows:
                        val = row[col]
                        if val is not None:
                            width = len(str(val))
                            if width > max_width:
                                max_width = width
                    col_widths[col] = min(max_width + 2, 50)
                
                # Header
                header_parts = []
                for col in columns:
                    header_parts.append(f"{col:^{col_widths[col]}}")
                f.write("| " + " | ".join(header_parts) + " |\n")
                
                separator_parts = []
                for col in columns:
                    separator_parts.append("-" * col_widths[col])
                f.write("| " + " | ".join(separator_parts) + " |\n")
                
                # Data rows
                for row in rows:
                    row_parts = []
                    for col in columns:
                        val = row[col]
                        if val is None:
                            val_str = "NULL"
                        elif isinstance(val, (dict, list)):
                            val_str = json.dumps(val, ensure_ascii=False)[:50]
                        else:
                            val_str = str(val)[:50]
                        row_parts.append(f"{val_str:^{col_widths[col]}}")
                    f.write("| " + " | ".join(row_parts) + " |\n")
                
                f.write("\n")
        
        print(f"✅ Database exported to TXT: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error exporting to TXT: {e}")
        return False
    finally:
        conn.close()

def export_database(format_type: str = 'json') -> bool:
    """Export database in specified format."""
    if not DB_PATH.exists():
        print(f"\n❌ Database file not found at: {DB_PATH}")
        print("   Please make sure the database exists.")
        return False
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = DB_PATH.stem
    
    if format_type == 'json':
        output_file = BACKUP_DIR / f"{db_name}_export_{timestamp}.json"
        return export_db_to_json(output_file)
    
    elif format_type == 'sql':
        output_file = BACKUP_DIR / f"{db_name}_export_{timestamp}.sql"
        return export_db_to_sql(output_file)
    
    elif format_type == 'csv':
        output_dir = BACKUP_DIR / f"{db_name}_csv_{timestamp}"
        return export_db_to_csv(output_dir)
    
    elif format_type == 'txt':
        output_file = BACKUP_DIR / f"{db_name}_export_{timestamp}.txt"
        return export_db_to_txt(output_file)
    
    else:
        print(f"❌ Unknown format: {format_type}")
        return False

def export_all_formats() -> bool:
    """Export database in all formats."""
    print("\n" + "=" * 60)
    print("📤 Exporting database in ALL formats...")
    print("=" * 60)
    
    formats = ['json', 'sql', 'csv', 'txt']
    success_count = 0
    
    for fmt in formats:
        print(f"\n--- Exporting as {fmt.upper()} ---")
        if export_database(fmt):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(formats)} exports completed successfully.")
    return success_count == len(formats)

# ======================== BACKUP FUNCTIONS ========================

def create_backup_directory():
    """Creates the backup directory if it doesn't exist."""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
        print(f"✅ Backup directory created at: {BACKUP_DIR}")
    return BACKUP_DIR

def should_exclude(path: Path) -> bool:
    """Checks if a file or folder should be excluded from backup."""
    if path.is_dir():
        for exclude in EXCLUDE_DIRS:
            if path.name == exclude or path.name.startswith(f"{exclude}_"):
                return True
            if exclude.startswith("*") and path.suffix == exclude[1:]:
                return True
    
    if path.is_file():
        for pattern in EXCLUDE_FILES:
            if pattern.startswith("*") and path.suffix == pattern[1:]:
                return True
            if path.name == pattern:
                return True
            if path.suffix in [".pyc", ".pyo", ".log", ".pid"]:
                return True
    
    return False

def get_backup_filename() -> str:
    """Generates a backup filename with current timestamp."""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"FarmTech_Backup_{timestamp}.zip"

def create_zip_backup(source_dir: Path, zip_path: Path) -> bool:
    """Creates a zip file from the source directory, excluding specified items."""
    try:
        total_files = 0
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                root_path = Path(root)
                dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
                
                for file in files:
                    file_path = root_path / file
                    if should_exclude(file_path):
                        continue
                    
                    arcname = str(file_path.relative_to(source_dir.parent))
                    zipf.write(file_path, arcname)
                    total_files += 1
                    print(f"  📄 Adding: {arcname}")
        
        print(f"\n✅ Total files added: {total_files}")
        return True
    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        return False

def perform_backup():
    """Performs the complete backup process."""
    print("\n" + "="*60)
    print("🚀 Starting ZIP backup for FarmTech-ProFertilizer project")
    print("="*60)

    if not PROJECT_DIR.exists():
        print(f"❌ Project directory not found at: {PROJECT_DIR}")
        return False

    create_backup_directory()
    backup_filename = get_backup_filename()
    backup_filepath = BACKUP_DIR / backup_filename

    print(f"\n📁 Project path: {PROJECT_DIR}")
    print(f"📂 Backup destination: {backup_filepath}")
    print("\n⏳ Creating backup...")

    success = create_zip_backup(PROJECT_DIR, backup_filepath)

    if success:
        file_size = backup_filepath.stat().st_size / (1024 * 1024)
        print("\n" + "="*60)
        print(f"✅ Backup created successfully!")
        print(f"📁 Location: {backup_filepath}")
        print(f"📦 Size: {file_size:.2f} MB")
        print("="*60)
        return True
    else:
        print("\n❌ Backup operation failed.")
        return False

# ======================== CODE AGGREGATION FUNCTIONS ========================

def get_all_code_files(directory: Path, specific_folders: List[str] = None) -> List[Path]:
    """Recursively finds all code files in the directory."""
    code_files = []
    scan_dirs = []

    if specific_folders:
        for folder in specific_folders:
            folder_path = directory / folder
            if folder_path.exists() and folder_path.is_dir():
                scan_dirs.append(folder_path)
            else:
                print(f"⚠️  Warning: Folder '{folder}' not found, skipping...")
        if not scan_dirs:
            print("❌ No valid folders specified to scan.")
            return []
    else:
        scan_dirs = [directory]

    for scan_dir in scan_dirs:
        for root, dirs, files in os.walk(scan_dir):
            root_path = Path(root)
            
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                if should_exclude(file_path):
                    continue
                
                if file_path.suffix in CODE_EXTENSIONS or file_path.name in CODE_EXTENSIONS:
                    code_files.append(file_path)
    
    return sorted(code_files)

def should_aggregate_file(file_path: Path) -> bool:
    """Determines if a file should be included in code aggregation."""
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', 
                         '.webp', '.svg', '.ttf', '.woff', '.woff2', '.eot',
                         '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip',
                         '.tar', '.gz', '.rar', '.7z', '.mp3', '.mp4', '.avi'}
    
    if file_path.suffix.lower() in binary_extensions:
        return False
    
    if file_path.stat().st_size > 1024 * 1024:
        return False
    
    return True

def aggregate_code_to_file(output_file: Path, specific_folders: List[str] = None):
    """Aggregates all code files into a single text file."""
    print("\n" + "="*60)
    print("📚 Code Aggregation Tool")
    print("="*60)

    if not PROJECT_DIR.exists():
        print(f"❌ Project directory not found at: {PROJECT_DIR}")
        return False

    print("\n🔍 Scanning for code files...")
    code_files = get_all_code_files(PROJECT_DIR, specific_folders)
    
    if not code_files:
        print("❌ No code files found to aggregate.")
        return False

    print(f"✅ Found {len(code_files)} code files to aggregate.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write("="*80 + "\n")
            out_f.write("CODE AGGREGATION REPORT\n")
            out_f.write(f"Project: FarmTech-ProFertilizer\n")
            out_f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out_f.write(f"Total files: {len(code_files)}\n")
            if specific_folders:
                out_f.write(f"Scanned folders: {', '.join(specific_folders)}\n")
            out_f.write("="*80 + "\n\n")

            for idx, file_path in enumerate(code_files, 1):
                if not should_aggregate_file(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as in_f:
                        content = in_f.read()
                    
                    rel_path = file_path.relative_to(PROJECT_DIR)
                    out_f.write(f"\n{'='*80}\n")
                    out_f.write(f"FILE {idx}/{len(code_files)}: {rel_path}\n")
                    out_f.write(f"Language: {file_path.suffix[1:] if file_path.suffix else 'Unknown'}\n")
                    out_f.write(f"Size: {file_path.stat().st_size:,} bytes\n")
                    out_f.write(f"{'='*80}\n\n")
                    
                    out_f.write(content)
                    out_f.write("\n\n")
                    
                    print(f"  ✅ Added: {rel_path}")
                    
                except UnicodeDecodeError:
                    print(f"  ⚠️  Skipping binary file: {file_path.name}")
                except Exception as e:
                    print(f"  ❌ Error reading {file_path.name}: {e}")

        file_size = output_file.stat().st_size / (1024 * 1024)
        print("\n" + "="*60)
        print(f"✅ Code aggregation completed successfully!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Total files aggregated: {len(code_files)}")
        print(f"📦 File size: {file_size:.2f} MB")
        print("="*60)
        return True

    except Exception as e:
        print(f"❌ Error creating aggregation file: {e}")
        return False

# ======================== LIST FUNCTIONS ========================

def list_backups():
    """Displays a list of existing backup files."""
    if not BACKUP_DIR.exists():
        print("\n📂 Backup directory doesn't exist. Create a backup first.")
        return
    
    backup_files = sorted(BACKUP_DIR.glob("FarmTech_Backup_*.zip"))
    if not backup_files:
        print("\n📂 No backup files found.")
        return

    print("\n📋 List of available backups:")
    print("-" * 70)
    for idx, file in enumerate(backup_files, 1):
        size = file.stat().st_size / (1024 * 1024)
        date_str = file.name.replace("FarmTech_Backup_", "").replace(".zip", "")
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y%m%d_%H%M%S")
            date_display = date_obj.strftime('%Y/%m/%d %H:%M:%S')
        except ValueError:
            date_display = "Unknown date"
        print(f"{idx}. {file.name} - {date_display} - {size:.2f} MB")

def list_db_exports():
    """Displays a list of existing database export files."""
    if not BACKUP_DIR.exists():
        print("\n📂 Backup directory doesn't exist.")
        return
    
    export_files = []
    for pattern in ["*.json", "*.sql", "*.txt"]:
        export_files.extend(BACKUP_DIR.glob(f"farmtech_export_*{pattern}"))
    
    csv_dirs = list(BACKUP_DIR.glob("farmtech_csv_*"))
    export_files.extend(csv_dirs)
    
    if not export_files:
        print("\n📂 No database export files found.")
        return
    
    export_files = sorted(export_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("\n📋 List of database exports:")
    print("-" * 70)
    for idx, file in enumerate(export_files, 1):
        if file.is_dir():
            total_size = 0
            for f in file.rglob('*'):
                if f.is_file():
                    total_size += f.stat().st_size
            size = total_size / (1024 * 1024)
            type_str = "CSV (folder)"
        else:
            size = file.stat().st_size / (1024 * 1024)
            type_str = file.suffix[1:].upper()
        
        # Extract date from filename
        name_parts = file.name.replace("farmtech_export_", "").replace("farmtech_csv_", "")
        if '.' in name_parts:
            name_parts = name_parts.split('.')[0]
        
        try:
            date_obj = datetime.datetime.strptime(name_parts, "%Y%m%d_%H%M%S")
            date_display = date_obj.strftime('%Y/%m/%d %H:%M:%S')
        except ValueError:
            date_display = "Unknown date"
        
        print(f"{idx}. {file.name} - {type_str} - {date_display} - {size:.2f} MB")

def restore_backup():
    """Shows restore instructions."""
    print("\n♻️  Restore Backup Instructions")
    print("-" * 60)
    print("⚠️  To restore a backup, manually extract the zip file.")
    print("Example commands:")
    print(f"  # Linux/Mac:")
    print(f"  unzip {BACKUP_DIR}/FarmTech_Backup_<timestamp>.zip -d {PROJECT_DIR.parent}")
    print(f"  # Windows:")
    print(f"  Right-click > Extract Here")

def delete_backup():
    """Deletes a selected backup file."""
    if not BACKUP_DIR.exists():
        print("\n📂 Backup directory doesn't exist.")
        return

    backup_files = sorted(BACKUP_DIR.glob("FarmTech_Backup_*.zip"))
    if not backup_files:
        print("\n📂 No backup files to delete.")
        return

    print("\n🗑️  Select a backup file to delete:")
    for idx, file in enumerate(backup_files, 1):
        size = file.stat().st_size / (1024 * 1024)
        print(f"{idx}. {file.name} ({size:.2f} MB)")
    
    try:
        choice = input("\nEnter the file number to delete (or 0 to cancel): ").strip()
        if not choice.isdigit():
            print("❌ Invalid input.")
            return
        
        choice_num = int(choice)
        if choice_num == 0:
            print("❌ Operation cancelled.")
            return
        if 1 <= choice_num <= len(backup_files):
            file_to_delete = backup_files[choice_num - 1]
            confirm = input(f"Are you sure you want to delete {file_to_delete.name}? (y/n): ").strip().lower()
            if confirm == 'y':
                file_to_delete.unlink()
                print(f"✅ File {file_to_delete.name} deleted successfully.")
            else:
                print("❌ Operation cancelled.")
        else:
            print("❌ Invalid number.")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_db_export():
    """Deletes a selected database export file."""
    if not BACKUP_DIR.exists():
        print("\n📂 Backup directory doesn't exist.")
        return

    export_files = []
    for pattern in ["*.json", "*.sql", "*.txt"]:
        export_files.extend(BACKUP_DIR.glob(f"farmtech_export_*{pattern}"))
    
    csv_dirs = list(BACKUP_DIR.glob("farmtech_csv_*"))
    export_files.extend(csv_dirs)
    
    if not export_files:
        print("\n📂 No database export files to delete.")
        return
    
    export_files = sorted(export_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("\n🗑️  Select a database export to delete:")
    for idx, file in enumerate(export_files, 1):
        if file.is_dir():
            total_size = 0
            for f in file.rglob('*'):
                if f.is_file():
                    total_size += f.stat().st_size
            size = total_size / (1024 * 1024)
            type_str = "CSV (folder)"
        else:
            size = file.stat().st_size / (1024 * 1024)
            type_str = file.suffix[1:].upper()
        print(f"{idx}. {file.name} - {type_str} - {size:.2f} MB")
    
    try:
        choice = input("\nEnter the file number to delete (or 0 to cancel): ").strip()
        if not choice.isdigit():
            print("❌ Invalid input.")
            return
        
        choice_num = int(choice)
        if choice_num == 0:
            print("❌ Operation cancelled.")
            return
        if 1 <= choice_num <= len(export_files):
            file_to_delete = export_files[choice_num - 1]
            confirm = input(f"Are you sure you want to delete {file_to_delete.name}? (y/n): ").strip().lower()
            if confirm == 'y':
                if file_to_delete.is_dir():
                    shutil.rmtree(file_to_delete)
                else:
                    file_to_delete.unlink()
                print(f"✅ {file_to_delete.name} deleted successfully.")
            else:
                print("❌ Operation cancelled.")
        else:
            print("❌ Invalid number.")
    except Exception as e:
        print(f"❌ Error: {e}")

# ======================== AGGREGATION MENU ========================

def aggregate_menu():
    """Shows aggregation options menu."""
    print("\n" + "="*60)
    print("📚 Code Aggregation Options")
    print("="*60)
    print("1. 📁 Aggregate ALL code files (entire project)")
    print("2. 📁 Aggregate ONLY backend code (backend/ folder)")
    print("3. 📁 Aggregate ONLY frontend code (frontend/ folder)")
    print("4. 📁 Aggregate specific folders (custom)")
    print("5. 🔙 Back to main menu")
    print("="*60)

def handle_aggregation(choice: str):
    """Handles different aggregation options."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if choice == "1":
        output_file = BACKUP_DIR / f"FarmTech_All_Code_{timestamp}.txt"
        print("\n📂 Aggregating ALL code files...")
        return aggregate_code_to_file(output_file, None)
    
    elif choice == "2":
        output_file = BACKUP_DIR / f"FarmTech_Backend_Code_{timestamp}.txt"
        print("\n📂 Aggregating backend code...")
        return aggregate_code_to_file(output_file, ["backend"])
    
    elif choice == "3":
        output_file = BACKUP_DIR / f"FarmTech_Frontend_Code_{timestamp}.txt"
        print("\n📂 Aggregating frontend code...")
        return aggregate_code_to_file(output_file, ["frontend"])
    
    elif choice == "4":
        print("\n📂 Enter folder names (comma-separated, relative to project root):")
        print("Example: backend/app, frontend/src, scripts")
        folders_input = input("> ").strip()
        if not folders_input:
            print("❌ No folders specified.")
            return False
        
        folders = [f.strip() for f in folders_input.split(",")]
        output_file = BACKUP_DIR / f"FarmTech_Custom_Code_{timestamp}.txt"
        print(f"\n📂 Aggregating custom folders: {', '.join(folders)}")
        return aggregate_code_to_file(output_file, folders)
    
    elif choice == "5":
        return None
    
    else:
        print("❌ Invalid option.")
        return False

def list_aggregated_files():
    """Lists all aggregated text files."""
    if not BACKUP_DIR.exists():
        print("\n📂 Backup directory doesn't exist.")
        return
    
    agg_files = sorted(BACKUP_DIR.glob("FarmTech_*_Code_*.txt"))
    if not agg_files:
        print("\n📂 No aggregated code files found.")
        return

    print("\n📋 List of aggregated code files:")
    print("-" * 70)
    for idx, file in enumerate(agg_files, 1):
        size = file.stat().st_size / (1024 * 1024)
        print(f"{idx}. {file.name} - {size:.2f} MB")

# ======================== DATABASE EXPORT MENU ========================

def db_export_menu():
    """Shows database export options menu."""
    print("\n" + "="*60)
    print("🗄️  Database Export Options")
    print("="*60)
    print("1. 📄 Export as JSON (structured data)")
    print("2. 📄 Export as SQL (database dump)")
    print("3. 📄 Export as CSV (one file per table)")
    print("4. 📄 Export as TXT (human-readable)")
    print("5. 📤 Export ALL formats")
    print("6. 📋 List existing exports")
    print("7. 🗑️  Delete an export")
    print("8. 🔙 Back to main menu")
    print("="*60)

def handle_db_export(choice: str):
    """Handles different database export options."""
    if choice == "1":
        return export_database('json')
    elif choice == "2":
        return export_database('sql')
    elif choice == "3":
        return export_database('csv')
    elif choice == "4":
        return export_database('txt')
    elif choice == "5":
        return export_all_formats()
    elif choice == "6":
        list_db_exports()
        return True
    elif choice == "7":
        delete_db_export()
        return True
    elif choice == "8":
        return None
    else:
        print("❌ Invalid option.")
        return False

# ======================== MAIN MENU ========================

def show_main_menu():
    """Displays the main menu."""
    print("\n" + "="*70)
    print("🛡️  FarmTech-ProFertilizer - Backup & Code Aggregation Tool")
    print("="*70)
    print("📦 BACKUP OPTIONS:")
    print("  1. 📦 Create ZIP backup of entire project")
    print("  2. 📋 List existing backups")
    print("  3. ♻️  Restore backup guide")
    print("  4. 🗑️  Delete a backup file")
    print("\n🗄️  DATABASE OPTIONS:")
    print("  5. 🗄️  Export database (JSON, SQL, CSV, TXT)")
    print("  6. 📋 List database exports")
    print("  7. 🗑️  Delete database export")
    print("\n📚 CODE AGGREGATION OPTIONS:")
    print("  8. 📚 Aggregate code into single file (with options)")
    print("  9. 📋 List aggregated code files")
    print("\n  0. 🚪 Exit")
    print("="*70)

def main():
    """Main entry point with interactive menu."""
    create_backup_directory()
    
    while True:
        show_main_menu()
        choice = input("\nPlease select an option (0-9): ").strip()
        
        if choice == "1":
            perform_backup()
        
        elif choice == "2":
            list_backups()
        
        elif choice == "3":
            restore_backup()
        
        elif choice == "4":
            delete_backup()
        
        elif choice == "5":
            while True:
                db_export_menu()
                db_choice = input("\nSelect export option (1-8): ").strip()
                result = handle_db_export(db_choice)
                if result is None:
                    break
                if result:
                    input("\n🔹 Press any key to continue...")
        
        elif choice == "6":
            list_db_exports()
        
        elif choice == "7":
            delete_db_export()
        
        elif choice == "8":
            while True:
                aggregate_menu()
                agg_choice = input("\nSelect aggregation option (1-5): ").strip()
                if agg_choice == "5":
                    break
                result = handle_aggregation(agg_choice)
                if result is not None:
                    if result:
                        print("\n✅ Aggregation completed!")
                    input("\n🔹 Press any key to continue...")
                    break
        
        elif choice == "9":
            list_aggregated_files()
        
        elif choice == "0":
            print("\n👋 Exiting. Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Please try again.")
        
        if choice not in ["5", "6", "7", "8", "9", "0"]:
            input("\n🔹 Press any key to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting. Goodbye!")
        sys.exit(0)