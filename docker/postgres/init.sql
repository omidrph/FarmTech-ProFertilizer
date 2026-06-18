-- ============================================
-- جدول کاربران (Users)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ایندکس برای جستجوی سریع‌تر با شماره تلفن
-- ============================================
CREATE INDEX idx_users_phone ON users(phone_number);

-- ============================================
-- تابع برای به‌روزرسانی خودکار updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================
-- تریگر برای به‌روزرسانی خودکار updated_at در جدول users
-- ============================================
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- درج یک کاربر نمونه برای تست
-- ============================================
INSERT INTO users (first_name, last_name, phone_number, password_hash)
VALUES (
    'علی',
    'محمدی',
    '09121234567',
    'hashed_password_here'
);

-- ============================================
-- مشاهده داده‌های جدول
-- ============================================
SELECT * FROM users;