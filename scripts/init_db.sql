-- scripts/init_db.sql
-- اسکریپت مقداردهی اولیه دیتابیس PostgreSQL

-- اطمینان از وجود دیتابیس (اگر قبلاً ایجاد نشده باشد)
SELECT 'CREATE DATABASE farmtech_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'farmtech_db')\gexec

-- اتصال به دیتابیس
\c farmtech_db;

-- ایجاد پسوندهای مورد نیاز
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- تنظیمات اولیه
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

-- ایجاد schema عمومی (در صورت نیاز)
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO public;

-- اطلاع از موفقیت
SELECT '✅ Database initialization completed successfully!' as message;