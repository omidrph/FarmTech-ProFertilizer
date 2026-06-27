# 🌱 FarmTech - ProFertilizer

**سیستم هوشمند نسخه‌نویسی کود برای گلخانه‌ها و کشت‌های بدون خاک**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3.4.0-4FC08D?logo=vuedotjs)](https://vuejs.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4.0-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57?logo=sqlite)](https://sqlite.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

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
| **دیتابیس** | SQLite (محلی و بدون نیاز به سرور) |
| **احراز هویت** | توکن‌های نشست با ذخیره‌سازی در دیتابیس |
| **بهینه‌سازی** | NumPy، SciPy (الگوریتم NNLS) |
| **HTTP Client** | Axios |

---

## 📁 ساختار پروژه
FarmTech-ProFertilizer/
│
├── backend/ 📁 بک‌اند FastAPI
│ ├── app/
│ │ ├── main.py 🚀 نقطه ورود برنامه
│ │ ├── config.py ⚙️ تنظیمات (SQLite)
│ │ ├── models.py 📊 مدل‌های دیتابیس
│ │ ├── schemas.py 📝 طرح‌های Pydantic
│ │ ├── crud.py 📂 عملیات CRUD
│ │ ├── services.py 🧮 الگوریتم‌های محاسباتی (NNLS)
│ │ ├── security.py 🔒 احراز هویت و توکن
│ │ ├── routes/ 🛣️ مسیرهای API
│ │ └── seeds/ 🌱 داده‌های اولیه (کودها، رسپی‌ها)
│ │
│ ├── tests/ 🧪 تست‌های جامع
│ ├── requirements.txt 📦 وابستگی‌ها
│ └── farmtech.db 🗄️ فایل دیتابیس
│
├── frontend/ 📁 فرانت‌اند Vue 3
│ ├── src/
│ │ ├── components/ 📁 کامپوننت‌ها
│ │ │ ├── features/ ویژگی‌های اصلی
│ │ │ ├── common/ کامپوننت‌های عمومی
│ │ │ └── layout/ چیدمان (هدر، فوتر)
│ │ │
│ │ ├── store/ 📁 مدیریت State (Pinia)
│ │ ├── composables/ 📁 توابع ترکیبی
│ │ ├── services/ 📁 ارتباط با API
│ │ ├── types/ 📁 تعاریف TypeScript
│ │ ├── utils/ 📁 ابزارهای کمکی
│ │ └── views/ 📁 صفحات اصلی
│ │
│ ├── public/fonts/ 📁 فونت‌های فارسی (۲۳ فایل)
│ ├── index.html 📄 صفحه اصلی
│ ├── package.json 📦 وابستگی‌ها
│ └── vite.config.ts ⚙️ تنظیمات Vite
│
├── scripts/ 📁 اسکریپت‌های مدیریتی
│ ├── cli.py 🖥️ منوی خط فرمان (CLI)
│ ├── deploy.sh 🚀 استقرار در لینوکس
│ └── deploy.bat 🚀 استقرار در ویندوز
│
├── docker-compose.yml 🐳 Docker Compose
├── Dockerfile 🐳 Dockerfile
└── README.md 📄 این مستندات
---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.11 یا بالاتر
- Node.js 18 یا بالاتر
- npm یا yarn

### روش سریع (با CLI)

```bash
# ۱. کلون کردن مخزن
git clone https://github.com/yourusername/FarmTech-ProFertilizer.git
cd FarmTech-ProFertilizer

# ۲. اجرای منوی مدیریتی
python scripts/cli.py

# ۳. انتخاب گزینه ۴ برای نصب وابستگی‌ها
# ۴. انتخاب گزینه ۱ برای اجرای کامل برنامه
روش دستی
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
سلامت سرور http://localhost:8000/health
🧪 اجرای تست‌ها
bash
cd backend
python tests/test_all.py
یا از طریق منوی CLI (گزینه ۵).
🐳 استقرار با Docker
bash
# ساخت و اجرا
docker-compose up --build

# توقف
docker-compose down
🔧 متغیرهای محیطی
فایل .env در ریشه پروژه:

env
# دیتابیس
DATABASE_URL=sqlite:///./farmtech.db

# امنیت
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# برنامه
APP_NAME=FarmTech - ProFertilizer
APP_VERSION=0.1.0
DEBUG=True

# API (فرانت‌اند)
VITE_API_URL=http://localhost:8000/api/v1

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

🏢 سازمان
FarmTech
راهکارهای هوشمند کشاورزی

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