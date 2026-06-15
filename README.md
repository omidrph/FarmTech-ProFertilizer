<div dir="rtl" align="center">

# 🌱 نرم‌افزار تغذیه سبز (Green Nutrition)

### سیستم تخصصی محاسبه و مدیریت فرمول‌های تغذیه گیاه در کشت هیدروپونیک و گلخانه‌ای

[![Vue](https://img.shields.io/badge/Vue-3.4-42b883?logo=vue.js)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178c6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06b6d4?logo=tailwindcss)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 درباره پروژه

**نرم‌افزار تغذیه سبز** یک ابزار تخصصی و حرفه‌ای برای **محاسبه دقیق فرمول‌های کوددهی** در سیستم‌های کشت بدون خاک، هیدروپونیک و گلخانه‌ای است.

این نرم‌افزار با هدف ساده‌سازی فرآیند پیچیده محاسبه عناصر غذایی و کاهش خطاهای انسانی طراحی شده و به کشاورزان، متخصصین تغذیه گیاه و گلخانه‌داران کمک می‌کند تا:
- ✅ فرمول‌های غذایی دقیق و متعادل ایجاد کنند
- ✅ کیفیت آب و پساب را تحلیل کنند
- ✅ هزینه‌های مصرف کود را بهینه‌سازی نمایند
- ✅ گزارش‌های تفسیری حرفه‌ای دریافت کنند

---

## ✨ ویژگی‌های کلیدی

| ویژگی | توضیح |
|-------|-------|
| 🔬 **محاسبات دقیق** | دقت محاسبات تا ۴ رقم اعشار با پشتیبانی از واحدهای PPM، MEQ و MMOLS |
| 🌍 **دو زبانه** | پشتیبانی کامل از زبان‌های فارسی (راست‌چین) و انگلیسی (چپ‌چین) بدون نیاز به ریفرش |
| 🌙 **تم روز و شب** | قابلیت جابجایی بین تم روشن و تاریک با ذخیره خودکار در مرورگر |
| 🖨️ **چاپ گزارش** | دکمه پرینت در تمام صفحات با قابلیت چاپ فقط ناحیه محتوای اصلی |
| 📊 **تحلیل آب و پساب** | محاسبه ترکیب آب تامینی با قابلیت تعیین درصد اختلاط آب و پساب |
| ⚖️ **تعادل یونی** | محاسبه خودکار تعادل کاتیون و آنیون با نمایش هشدار در صورت عدم تعادل |
| 🧪 **مدیریت کودها** | CRUD کامل برای پایگاه داده کودها با قابلیت تعریف درصد عناصر |
| 📈 **تفسیر هوشمند** | تولید گزارش تفسیری کامل شامل کمبودها، سمیت و توصیه‌های اصلاحی |
| 🔄 **واکنش‌گرا** | به‌روزرسانی لحظه‌ای محاسبات با هر تغییر در ورودی‌ها |

---

## 🛠️ تکنولوژی‌های استفاده شده

### فرانت‌اند (Frontend)
Vue 3 (Composition API) + TypeScript + Vite
Pinia (State Management)
Vue Router 4
Tailwind CSS 3 (با پشتیبانی از RTL و تم تاریک)
Axios
vue-i18n (بین‌المللی‌سازی)

### بک‌اند (Backend)
Python 3.10+
FastAPI (فریمورک API)
SQLAlchemy (ORM)
Pydantic (مدیریت داده‌ها و اعتبارسنجی)
Uvicorn (سرور ASGI)
SQLite (توسعه) / PostgreSQL (تولید)
---

## 📁 ساختار پروژه
green-nutrition/
├── frontend/ # پروژه Vue.js
│ ├── src/
│ │ ├── components/ # کامپوننت‌های reusable
│ │ │ ├── common/ # دکمه، ورودی، جدول پایه
│ │ │ └── nutrition/ # کامپوننت‌های تخصصی تغذیه
│ │ ├── composables/ # Hookهای Vue (usePrinter, useCalculator)
│ │ ├── i18n/ # فایل‌های ترجمه (fa/en)
│ │ ├── layouts/ # لایه‌بندی اصلی
│ │ ├── pages/ # صفحات برنامه
│ │ ├── router/ # تنظیمات مسیریابی
│ │ ├── stores/ # Pinia stores (auth, fertilizers, calc)
│ │ ├── types/ # تعاریف TypeScript
│ │ └── utils/ # توابع کمکی (تبدیل واحد، فرمت اعداد)
│ └── package.json
│
├── backend/ # پروژه FastAPI
│ ├── app/
│ │ ├── api/ # Endpoints
│ │ ├── core/ # تنظیمات اصلی و دیتابیس
│ │ ├── models/ # مدل‌های SQLAlchemy
│ │ ├── schemas/ # مدل‌های Pydantic
│ │ └── services/ # منطق تجاری و محاسبات
│ └── requirements.txt
│
└── README.md

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Node.js 18+ و npm/pnpm
- Python 3.10+
- Git

### مرحله 1: کلون کردن پروژه
```bash
git clone https://github.com/your-username/green-nutrition.git
cd green-nutrition
cd frontend
npm install
npm run dev
پروژه فرانت‌اند روی http://localhost:5173 اجرا می‌شود.
مرحله 3: نصب و اجرای بک‌اند (در ترمینال جداگانه)
cd backend
python -m venv venv
source venv/bin/activate  # در Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
پروژه بک‌اند روی http://localhost:8000 اجرا می‌شود.
مستندات خودکار API در http://localhost:8000/docs قابل مشاهده است.

اعتبارات ورود (مرحله توسعه)
Username: admin
Password: 1234