🌱 FarmTech - ProFertilizer
سیستم هوشمند نسخه‌نویسی کود برای گلخانه‌ها و کشت‌های بدون خاک
https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi
https://img.shields.io/badge/Vue-3.4.0-4FC08D?logo=vuedotjs
https://img.shields.io/badge/Tailwind-3.4.0-06B6D4?logo=tailwindcss
https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql
https://img.shields.io/badge/Python-3.11+-3776AB?logo=python
https://img.shields.io/badge/Docker-24.0+-2496ED?logo=docker

📋 فهرست مطالب
نمای کلی

ویژگی‌های کلیدی

معماری الگوریتمی

معماری فنی

ساختار پروژه

نصب و راه‌اندازی

دسترسی به برنامه

اجرای تست‌ها

دستورات مفید Docker

بکاپ دیتابیس

عیب‌یابی

منابع علمی

توسعه‌دهنده

مجوز

📋 نمای کلی
FarmTech - ProFertilizer یک نرم‌افزار تخصصی برای محاسبه، تحلیل و مدیریت فرمول‌های تغذیه گیاه در سیستم‌های کشت بدون خاک، هیدروپونیک و گلخانه‌های مدرن است. این نرم‌افزار با بهره‌گیری از الگوریتم‌های علمی معتبر و پایگاه داده‌ای جامع از کودها، امکان محاسبه دقیق فرمول غذایی، تحلیل آب و پساب، تعادل یونی و بهینه‌سازی هزینه را فراهم می‌کند.

🎯 چکیده اجرایی
ProFertilizer یک سامانه جامع و مبتنی بر علم تغذیه گیاه است که فرآیند پیچیده‌ی فرمول‌نویسی کود در سیستم‌های کشت بدون خاک، هیدروپونیک، و گلخانه‌های مدرن را هوشمندسازی می‌کند. این نرم‌افزار که محصول شرکت فارم تک است، با ترکیب دانش شیمی کشاورزی، الگوریتم‌های بهینه‌سازی عددی، و مهندسی نرم‌افزار، امکان محاسبه‌ی دقیق ترکیب کودها، تحلیل کیفی آب، پایش تعادل یونی، و بهینه‌سازی اقتصادی را برای گلخانه‌داران، مشاوران تغذیه، و کارشناسان کشاورزی فراهم می‌آورد.

هسته‌ی الگوریتمی این سامانه بر مبنای روش NNLS (Non-Negative Least Squares) طراحی شده است که با افزودن لایه‌های تخصصی اعتبارسنجی چون تعادل یونی، بررسی رسوب‌گذاری، محاسبه‌ی EC و pH، و توزیع هوشمند مخازن، به یک راهکار کامل و قابل اتکا برای نیازهای پیچیده‌ی تغذیه‌ی گیاهان در محیط‌های کنترل‌شده تبدیل شده است.

شاخص عملکرد	مقدار
دقت تحقق عناصر هدف	۹۵-۱۰۰%
خطای باقی‌مانده (Residual Error)	< ۱۰ واحد
زمان همگرایی	< ۵۰ میلی‌ثانیه
عناصر پشتیبانی‌شده	۱۵ عنصر اصلی
تعداد کودهای سیستمی	۴۲ کود استاندارد
تلرانس تعادل یونی	۰.۵ meq/L
🚀 ویژگی‌های کلیدی
ویژگی	توضیح
🔐 احراز هویت امن	ثبت‌نام و ورود با توکن‌های نشست ذخیره‌شده در دیتابیس
💧 آنالیز آب و پساب	محاسبه خودکار مقادیر تامینی بر اساس درصد اختلاط آب و پساب
🎯 عناصر هدف	تعیین سطح دقیق عناصر غذایی با اعتبارسنجی تعادل یونی
🧠 بهینه‌سازی خودکار	استفاده از الگوریتم NNLS برای محاسبه بهترین ترکیب کودها
🧪 پایگاه داده کودها	بیش از ۴۲ کود استاندارد به‌همراه ترکیب عناصر و قیمت
📊 تفسیر هوشمند	تولید گزارش‌های جامع با توصیه‌های اصلاحی
🗄️ مدیریت مخازن	تقسیم خودکار کودها در مخازن A، B و C بر اساس سازگاری شیمیایی
🌓 حالت روشن/تاریک	نمایش مطابق با نور محیط
🌐 دو زبانه	پشتیبانی کامل از زبان‌های فارسی و انگلیسی
🖨️ چاپ گزارش	خروجی قابل چاپ از تمام بخش‌ها
🧠 معماری الگوریتمی
هسته الگوریتمی: NNLS و روش‌های بهینه‌سازی
فرمول‌بندی ریاضی مسئله
مسئله‌ی فرمول‌نویسی کود را می‌توان به صورت زیر فرمول‌بندی کرد:

min
⁡
x
≥
0
∥
A
x
−
b
∥
2
2
min 
x≥0
​
 ∥Ax−b∥ 
2
2
​
 

که در آن:

A ∈ ℝᵐˣⁿ = ماتریس ضرایب (m عنصر، n کود)

x ∈ ℝⁿ = بردار وزن‌ها (مقدار مصرف هر کود)

b ∈ ℝᵐ = بردار اهداف (نیاز خالص هر عنصر)

ساخت ماتریس ضرایب (A)
هر ستون از ماتریس A مربوط به یک کود است و هر سطر مربوط به یک عنصر. مقدار هر خانه به صورت زیر محاسبه می‌شود:

A
i
j
=
درصد عنصر 
i
 در کود 
j
100
×
خلوص کود 
j
A 
ij
​
 = 
100
درصد عنصر i در کود j
​
 ×خلوص کود j

بردار هدف (b)
بردار هدف با کسر عناصر موجود در آب از مقادیر هدف محاسبه می‌شود:

b
i
=
max
⁡
(
0
,
Target
i
−
Water
i
)
b 
i
​
 =max(0,Target 
i
​
 −Water 
i
​
 )

الگوریتم NNLS
الگوریتم NNLS توسط Lawson و Hanson در سال ۱۹۷۴ معرفی شد و یکی از پایدارترین روش‌ها برای حل مسائل حداقل مربعات با قید غیرمنفی است.

python
from scipy.optimize import nnls

def optimize_with_nnls(A, b):
    weights, residual = nnls(A, b)
    return weights, residual
روش‌های جایگزین
روش	فرمول	مزایا	معایب
NNLS	
min
⁡
∥
A
x
−
b
∥
2
min∥Ax−b∥ 
2
  با 
x
≥
0
x≥0	تضمین غیرمنفی، پایدار	سرعت متوسط
LSQ-Linear	
min
⁡
∥
A
x
−
b
∥
2
min∥Ax−b∥ 
2
 	سرعت بالا	ممکن است جواب منفی بدهد
Cost-based	
min
⁡
(
∥
A
x
−
b
∥
2
+
λ
∑
x
i
c
i
)
min(∥Ax−b∥ 
2
 +λ∑x 
i
​
 c 
i
​
 )	بهینه‌سازی هزینه	پیچیده‌تر
🏗️ معماری فنی
لایه	فناوری
فرانت‌اند	Vue 3، TypeScript، Tailwind CSS، Vite، Pinia
بک‌اند	FastAPI، Python 3.11، SQLAlchemy
دیتابیس	PostgreSQL 15 (با پشتیبانی از SQLite برای توسعه)
احراز هویت	توکن‌های نشست با ذخیره‌سازی در دیتابیس
بهینه‌سازی	NumPy، SciPy (الگوریتم NNLS)
HTTP Client	Axios
Containerization	Docker، Docker Compose
📁 ساختار پروژه
text
FarmTech-ProFertilizer/
│
├── backend/                              # 📁 بک‌اند FastAPI
│   ├── app/
│   │   ├── main.py                       # 🚀 نقطه ورود برنامه
│   │   ├── config.py                     # ⚙️ تنظیمات (PostgreSQL)
│   │   ├── models.py                     # 📊 مدل‌های دیتابیس
│   │   ├── schemas.py                    # 📝 طرح‌های Pydantic
│   │   ├── crud.py                       # 📂 عملیات CRUD
│   │   ├── security.py                   # 🔒 احراز هویت و توکن
│   │   ├── database.py                   # 🗄️ اتصال به PostgreSQL
│   │   ├── routes/                       # 🛣️ مسیرهای API
│   │   └── seeds/                        # 🌱 داده‌های اولیه
│   ├── tests/                            # 🧪 تست‌های جامع
│   └── requirements.txt                  # 📦 وابستگی‌ها
│
├── frontend/                             # 📁 فرانت‌اند Vue 3
│   ├── src/
│   │   ├── components/                   # 📁 کامپوننت‌ها
│   │   ├── store/                        # 📁 مدیریت State (Pinia)
│   │   ├── composables/                  # 📁 توابع ترکیبی
│   │   ├── services/                     # 📁 ارتباط با API
│   │   ├── types/                        # 📁 تعاریف TypeScript
│   │   └── views/                        # 📁 صفحات اصلی
│   ├── public/fonts/                     # 📁 فونت‌های فارسی
│   ├── package.json                      # 📦 وابستگی‌ها
│   └── vite.config.ts                    # ⚙️ تنظیمات Vite
│
├── scripts/                              # 📁 اسکریپت‌های مدیریتی
│   ├── cli.py                            # 🖥️ منوی خط فرمان (CLI)
│   └── init_db.py                        # 🗄️ مقداردهی اولیه دیتابیس
│
├── docker-compose.yml                    # 🐳 Docker Compose
├── Dockerfile.backend                    # 🐳 Dockerfile بک‌اند
├── Dockerfile.frontend                   # 🐳 Dockerfile فرانت‌اند
├── .env                                  # 🔐 متغیرهای محیطی
├── .env.example                          # 📄 نمونه متغیرهای محیطی
└── README.md                             # 📄 این مستندات
🚀 نصب و راه‌اندازی
پیش‌نیازها
Docker 24.0+

Docker Compose 2.20+

Git

روش سریع با Docker
bash
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

# ری‌استارت یک سرویس
docker-compose restart backend
docker-compose restart frontend

# ورود به شل فرانت‌اند
docker-compose exec frontend sh
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
📚 منابع علمی
Resh, H. M. (2012). Hydroponic Food Production: A Definitive Guidebook for the Advanced Home Gardener and the Commercial Hydroponic Grower. CRC Press.

Jones, J. B. (2016). Hydroponics: A Practical Guide for the Soilless Grower. CRC Press.

Lawson, C. L., & Hanson, R. J. (1974). Solving Least Squares Problems. Prentice-Hall.

Peckenpaugh, D. (2015). Hydroponic Solutions: Volume 1. Growing Edge Publications.

University of Florida, IFAS Extension. (2020). Tomato Production in Florida.

Nielsen, N. E. (2006). Plant Nutrition and Fertilization. Springer.

Barker, A. V. & Pilbeam, D. J. (2007). Handbook of Plant Nutrition. CRC Press.

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