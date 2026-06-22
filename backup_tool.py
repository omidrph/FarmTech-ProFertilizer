#!/usr/bin/env python3
"""
FarmTech-ProFertilizer Backup & Code Aggregation Tool
This script provides:
1. ZIP backup of the project (excluding unnecessary files)
2. Code aggregation - combines all code files into a single text file
"""

import os
import shutil
import zipfile
import datetime
import argparse
import sys
from pathlib import Path
from typing import List, Set

# ======================== CONFIGURATION ========================
PROJECT_DIR = Path(__file__).parent.absolute()
BACKUP_DIR = PROJECT_DIR.parent / "FarmTech_Backups"

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
    """
    Recursively finds all code files in the directory.
    If specific_folders is provided, only scans those folders.
    """
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
            
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                # Skip excluded files
                if should_exclude(file_path):
                    continue
                
                # Check if it's a code file
                if file_path.suffix in CODE_EXTENSIONS or file_path.name in CODE_EXTENSIONS:
                    code_files.append(file_path)
    
    return sorted(code_files)

def should_aggregate_file(file_path: Path) -> bool:
    """Determines if a file should be included in code aggregation."""
    # Exclude binary files, images, etc.
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', 
                         '.webp', '.svg', '.ttf', '.woff', '.woff2', '.eot',
                         '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip',
                         '.tar', '.gz', '.rar', '.7z', '.mp3', '.mp4', '.avi'}
    
    if file_path.suffix.lower() in binary_extensions:
        return False
    
    # Check file size (skip files larger than 1MB)
    if file_path.stat().st_size > 1024 * 1024:
        return False
    
    return True

def aggregate_code_to_file(output_file: Path, specific_folders: List[str] = None):
    """
    Aggregates all code files into a single text file.
    """
    print("\n" + "="*60)
    print("📚 Code Aggregation Tool")
    print("="*60)

    if not PROJECT_DIR.exists():
        print(f"❌ Project directory not found at: {PROJECT_DIR}")
        return False

    # Get all code files
    print("\n🔍 Scanning for code files...")
    code_files = get_all_code_files(PROJECT_DIR, specific_folders)
    
    if not code_files:
        print("❌ No code files found to aggregate.")
        return False

    print(f"✅ Found {len(code_files)} code files to aggregate.")

    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # Write header
            out_f.write("="*80 + "\n")
            out_f.write(f"CODE AGGREGATION REPORT\n")
            out_f.write(f"Project: FarmTech-ProFertilizer\n")
            out_f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out_f.write(f"Total files: {len(code_files)}\n")
            if specific_folders:
                out_f.write(f"Scanned folders: {', '.join(specific_folders)}\n")
            out_f.write("="*80 + "\n\n")

            # Process each file
            for idx, file_path in enumerate(code_files, 1):
                if not should_aggregate_file(file_path):
                    continue

                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as in_f:
                        content = in_f.read()
                    
                    # Write file header
                    rel_path = file_path.relative_to(PROJECT_DIR)
                    out_f.write(f"\n{'='*80}\n")
                    out_f.write(f"FILE {idx}/{len(code_files)}: {rel_path}\n")
                    out_f.write(f"Language: {file_path.suffix[1:] if file_path.suffix else 'Unknown'}\n")
                    out_f.write(f"Size: {file_path.stat().st_size:,} bytes\n")
                    out_f.write(f"{'='*80}\n\n")
                    
                    # Write file content
                    out_f.write(content)
                    out_f.write("\n\n")
                    
                    print(f"  ✅ Added: {rel_path}")
                    
                except UnicodeDecodeError:
                    print(f"  ⚠️  Skipping binary file: {file_path.name}")
                except Exception as e:
                    print(f"  ❌ Error reading {file_path.name}: {e}")

        # Calculate file size
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

# ======================== LIST BACKUPS ========================
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
        except:
            date_display = "Unknown date"
        print(f"{idx}. {file.name} - {date_display} - {size:.2f} MB")

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
        # All project
        output_file = BACKUP_DIR / f"FarmTech_All_Code_{timestamp}.txt"
        print("\n📂 Aggregating ALL code files...")
        return aggregate_code_to_file(output_file, None)
    
    elif choice == "2":
        # Backend only
        output_file = BACKUP_DIR / f"FarmTech_Backend_Code_{timestamp}.txt"
        print("\n📂 Aggregating backend code...")
        return aggregate_code_to_file(output_file, ["backend"])
    
    elif choice == "3":
        # Frontend only
        output_file = BACKUP_DIR / f"FarmTech_Frontend_Code_{timestamp}.txt"
        print("\n📂 Aggregating frontend code...")
        return aggregate_code_to_file(output_file, ["frontend"])
    
    elif choice == "4":
        # Custom folders
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
    print("\n📚 CODE AGGREGATION OPTIONS:")
    print("  5. 📚 Aggregate code into single file (with options)")
    print("  6. 📋 List aggregated code files")
    print("\n  7. 🚪 Exit")
    print("="*70)

def main():
    """Main entry point with interactive menu."""
    while True:
        show_main_menu()
        choice = input("\nPlease select an option (1-7): ").strip()
        
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
        
        elif choice == "6":
            list_aggregated_files()
        
        elif choice == "7":
            print("\n👋 Exiting. Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Please try again.")
        
        if choice not in ["5", "6", "7"]:
            input("\n🔹 Press any key to continue...")

if __name__ == "__main__":
    main()