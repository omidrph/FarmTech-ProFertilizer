# 🌱 FarmTech - ProFertilizer

**سیستم هوشمند نسخه‌نویسی کود برای گلخانه‌ها و کشت‌های بدون خاک**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3.4.0-4FC08D?logo=vuedotjs)](https://vuejs.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4.0-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?logo=docker)](https://docker.com)

---

## 📋 نمای کلی

**FarmTech - ProFertilizer** یک نرم‌افزار تخصصی برای **محاسبه، تحلیل و مدیریت فرمول‌های تغذیه گیاه** در سیستم‌های کشت بدون خاک، هیدروپونیک و گلخانه‌های مدرن است. این نرم‌افزار با بهره‌گیری از الگوریتم‌های علمی معتبر و پایگاه داده‌ای جامع از کودهای ایرانی، امکان محاسبه دقیق فرمول غذایی، تحلیل آب و پساب، تعادل یونی و بهینه‌سازی هزینه را فراهم می‌کند.

---

## 🚀 ویژگی‌های کلیدی

| ویژگی | توضیح |
|-------|-------|
| 🔐 **احراز هویت امن** | ثبت‌نام و ورود با توکن‌های نشست ذخیره‌شده در دیتابیس |
| 💧 **آنالیز آب و پساب** | محاسبه خودکار مقادیر تامینی بر اساس درصد اختلاط آب و پساب |
| 🎯 **عناصر هدف** | تعیین سطح دقیق عناصر غذایی با اعتبارسنجی تعادل یونی |
| 🧠 **بهینه‌سازی خودکار** | استفاده از الگوریتم NNLS برای محاسبه بهترین ترکیب کودها |
| 🧪 **پایگاه داده کودها** | بیش از ۴۲ کود ایرانی به‌همراه ترکیب عناصر و قیمت |
| 📊 **تفسیر هوشمند** | تولید گزارش‌های جامع با توصیه‌های اصلاحی |
| 🗄️ **مدیریت مخازن** | تقسیم خودکار کودها در مخازن A، B و C بر اساس سازگاری شیمیایی |
| 🌓 **حالت روشن/تاریک** | نمایش مطابق با نور محیط |
| 🌐 **دو زبانه** | پشتیبانی کامل از زبان‌های فارسی و انگلیسی |
| 🖨️ **چاپ گزارش** | خروجی قابل چاپ از تمام بخش‌ها |

---

## 🏗️ معماری فنی

| لایه | فناوری |
|------|--------|
| **فرانت‌اند** | Vue 3، TypeScript، Tailwind CSS، Vite، Pinia |
| **بک‌اند** | FastAPI، Python 3.11، SQLAlchemy |
| **دیتابیس** | PostgreSQL 15 (با پشتیبانی از SQLite برای توسعه) |
| **احراز هویت** | توکن‌های نشست با ذخیره‌سازی در دیتابیس |
| **بهینه‌سازی** | NumPy، SciPy (الگوریتم NNLS) |
| **HTTP Client** | Axios |
| **Containerization** | Docker، Docker Compose |

---

## 📁 ساختار پروژه
FarmTech-ProFertilizer/
│
├── backend/ 📁 بک‌اند FastAPI
│ ├── app/
│ │ ├── main.py 🚀 نقطه ورود برنامه
│ │ ├── config.py ⚙️ تنظیمات (PostgreSQL)
│ │ ├── models.py 📊 مدل‌های دیتابیس
│ │ ├── schemas.py 📝 طرح‌های Pydantic
│ │ ├── crud.py 📂 عملیات CRUD
│ │ ├── security.py 🔒 احراز هویت و توکن
│ │ ├── database.py 🗄️ اتصال به PostgreSQL
│ │ ├── routes/ 🛣️ مسیرهای API
│ │ └── seeds/ 🌱 داده‌های اولیه (کودها، رسپی‌ها)
│ ├── tests/ 🧪 تست‌های جامع
│ └── requirements.txt 📦 وابستگی‌ها
│
├── frontend/ 📁 فرانت‌اند Vue 3
│ ├── src/
│ │ ├── components/ 📁 کامپوننت‌ها
│ │ ├── store/ 📁 مدیریت State (Pinia)
│ │ ├── composables/ 📁 توابع ترکیبی
│ │ ├── services/ 📁 ارتباط با API
│ │ ├── types/ 📁 تعاریف TypeScript
│ │ └── views/ 📁 صفحات اصلی
│ ├── public/fonts/ 📁 فونت‌های فارسی
│ ├── package.json 📦 وابستگی‌ها
│ └── vite.config.ts ⚙️ تنظیمات Vite
│
├── scripts/ 📁 اسکریپت‌های مدیریتی
│ ├── cli.py 🖥️ منوی خط فرمان (CLI)
│ ├── init_db.py 🗄️ مقداردهی اولیه دیتابیس│ └── init_db.sql 🗄️ اسکریپت SQL اولیه
│
├── docker-compose.yml 🐳 Docker Compose
├── Dockerfile.backend 🐳 Dockerfile بک‌اند
├── Dockerfile.frontend 🐳 Dockerfile فرانت‌اند
├── .env 🔐 متغیرهای محیطی
├── .env.example 📄 نمونه متغیرهای محیطی
└── README.md 📄 این مستندات

text

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Docker 24.0+
- Docker Compose 2.20+
- Git

### روش سریع با Docker

```bash
# ۱. کلون کردن مخزن
git clone https://github.com/yourusername/FarmTech-ProFertilizer.git
cd FarmTech-ProFertilizer

# ۲. کپی و ویرایش فایل محیطی
cp .env.example .env
# ویرایش .env با تنظیمات مورد نظر

# ۳. ساختن و اجرای سرویس‌ها
docker-compose up --build -d

# ۴. بررسی وضعیت
docker-compose ps

# ۵. مشاهده لاگ‌ها
docker-compose logs -f

# ۶. مقداردهی اولیه دیتابیس (اختیاری - خودکار انجام می‌شود)
docker-compose exec backend python scripts/init_db.py
روش دستی (بدون Docker)
bash
# ----- بک‌اند -----
cd backend
python -m venv venv
source venv/bin/activate        # در ویندوز: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ----- فرانت‌اند (در ترمینال جدید) -----
cd frontend
npm install
npm run dev
🌐 دسترسی به برنامه
سرویس	آدرس
فرانت‌اند	http://localhost:3000
بک‌اند (API)	http://localhost:8000
مستندات API	http://localhost:8000/docs
سلامت سرور	http://localhost:8000/health
اطلاعات کاربر تست
فیلد	مقدار
شماره تلفن	09121234567
رمز عبور	Test@123456
🧪 اجرای تست‌ها
bash
# با Docker
docker-compose exec backend python tests/test_all.py

# یا از طریق CLI
python scripts/cli.py
# سپس گزینه ۵ را انتخاب کنید
🐳 دستورات مفید Docker
bash
# مشاهده لاگ‌های یک سرویس خاص
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# ورود به کانتینر بک‌اند
docker-compose exec backend bash

# ورود به دیتابیس
docker-compose exec db psql -U postgres -d farmtech_db

# توقف سرویس‌ها
docker-compose down

# توقف و حذف کامل داده‌ها
docker-compose down -v

# بازسازی و اجرا
docker-compose up --build -d

# بررسی وضعیت سلامت
docker-compose ps

# مشاهده استفاده از منابع
docker stats
💾 بکاپ دیتابیس
bash
# بکاپ گرفتن از دیتابیس
docker-compose exec db pg_dump -U postgres -d farmtech_db > backup_$(date +%Y%m%d_%H%M%S).sql

# ریستور بکاپ
cat backup.sql | docker-compose exec -T db psql -U postgres -d farmtech_db
🔧 عیب‌یابی
❌ خطای اتصال به دیتابیس
bash
# بررسی آمادگی دیتابیس
docker-compose exec db pg_isready -U postgres

# مشاهده لاگ‌های دیتابیس
docker-compose logs db

# ریستارت دیتابیس
docker-compose restart db
❌ خطای psycopg2
bash
# اطمینان از نصب پکیج‌های مورد نیاز در Dockerfile
apt-get install -y gcc libpq-dev
❌ خطای پورت درگیر
bash
# بررسی پورت‌های درگیر
sudo lsof -i :8000
sudo lsof -i :3000
sudo lsof -i :5432

# کشتن پروسه درگیر
sudo kill -9 <PID>
🧠 الگوریتم محاسبه
قلب محاسباتی برنامه بر اساس روش NNLS (Non-Negative Least Squares) طراحی شده است:

ساخت ماتریس ضرایب: سهم هر عنصر از هر کود (با در نظر گرفتن خلوص) محاسبه می‌شود.

کسر کیفیت آب: عناصر موجود در آب از نیاز خالص کسر می‌شوند.

بهینه‌سازی: با قید غیرمنفی بودن وزن‌ها، بهترین ترکیب کودها محاسبه می‌شود.

اعتبارسنجی: تعادل یونی، بررسی رسوب و درصد تحقق اهداف بررسی می‌شود.

توزیع مخازن: مواد به‌صورت خودکار در مخازن A، B و C توزیع می‌شوند.

📚 منابع علمی
هوارد رش (Howard Resh) – مرجع استاندارد تغذیه در هیدروپونیک

دانشگاه فلوریدا – رسپی‌های گوجه‌فرنگی در مراحل مختلف رشد

داگلاس پکنپا (Douglas Peckenpaugh) – فرمول‌های تخصصی

نرخنامه سال ۱۴۰۵ وزارت جهاد کشاورزی – قیمت و ترکیب کودهای ایرانی

👨‍💻 توسعه‌دهنده
امید رحمانی
توسعه‌دهنده ارشد و طراح سیستم

ایمیل: info@farmtech.ir

گیت‌هاب: github.com/omidrph

📄 مجوز
نرم‌افزار اختصاصی (Proprietary)

© ۲۰۲۶ FarmTech. تمامی حقوق محفوظ است.

این نرم‌افزار متعلق به FarmTech بوده و هرگونه کپی، توزیع، تغییر یا استفاده غیرمجاز از آن ممنوع می‌باشد.
برای دریافت مجوز، با ایمیل زیر تماس بگیرید:
📧 info@farmtech.ir

📞 ارتباط با ما
ایمیل: info@farmtech.ir

وب‌سایت: www.farmtech.ir

تلفن: ۰۲۱-۸۸۴۱۴۶۷۹


========================
# ===== توقف سرویس‌ها =====
docker-compose down

# ===== توقف و حذف کامل داده‌ها (دیتابیس پاک می‌شود) =====
docker-compose down -v

# ===== ری‌استارت یک سرویس =====
docker-compose restart backend
docker-compose restart frontend

# ===== بازسازی و اجرا =====
docker-compose up --build -d

# ===== ورود به شل بک‌اند =====
docker-compose exec backend bash

# ===== ورود به شل فرانت‌اند =====
docker-compose exec frontend sh

# ===== ورود به دیتابیس =====
docker-compose exec db psql -U postgres -d farmtech_db