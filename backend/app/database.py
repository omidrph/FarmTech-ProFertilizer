# backend/app/database.py
"""اتصال و مدیریت دیتابیس SQLite"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
import sqlite3
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

# ===== ایجاد اتصال به SQLite =====
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # مخصوص SQLite
)

# ===== ایجاد SessionLocal =====
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ===== ایجاد کلاس پایه برای مدل‌ها =====
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    وابستگی برای دریافت Session دیتابیس
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    ایجاد تمام جدول‌ها در دیتابیس
    ✅ اصلاح شده: استفاده از SQL مستقیم در صورت失败
    """
    try:
        # ابتدا سعی می‌کنیم با SQLAlchemy ایجاد کنیم
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully with SQLAlchemy")
        return True
    except Exception as e:
        logger.warning(f"⚠️ SQLAlchemy failed: {e}")
        logger.info("🔄 Trying direct SQL...")
        return _create_tables_direct()


def _create_tables_direct():
    """
    ایجاد جدول‌ها با SQL مستقیم (در صورت失败 SQLAlchemy)
    """
    db_path = Path(__file__).parent.parent / "farmtech.db"
    
    # تعریف جدول‌ها با SQL مستقیم
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
                water_salinity_unit VARCHAR(10) DEFAULT 'dS/m',
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
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        for table_name, sql in TABLES_SQL.items():
            try:
                cursor.execute(sql)
                logger.info(f"✅ Table {table_name} created")
            except Exception as e:
                logger.warning(f"⚠️ Error creating {table_name}: {e}")
        
        conn.commit()
        conn.close()
        logger.info("✅ All tables created successfully with direct SQL")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create tables with direct SQL: {e}")
        return False


def drop_tables():
    """حذف تمام جدول‌ها از دیتابیس (فقط برای توسعه)"""
    Base.metadata.drop_all(bind=engine)