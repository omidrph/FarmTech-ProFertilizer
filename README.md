# 🌱 FarmTech - ProFertilizer

**Smart Digital Fertilizer Prescription System**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3.4.0-4FC08D?logo=vuedotjs)](https://vuejs.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4.0-06B6D4?logo=tailwindcss)](https://tailwindcss.com)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57?logo=sqlite)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

---

## 📋 Overview

**FarmTech - ProFertilizer** is a specialized software for calculating, analyzing, and managing plant nutrition formulas in soilless cultivation systems, hydroponics, and greenhouses. It provides water and wastewater analysis, target element determination, automatic fertilizer calculation, fertilizer database management, and intelligent data interpretation.

---

## ⚠️ Important Notice

**This software is proprietary and NOT open source.**

- © 2025 FarmTech. All rights reserved.
- No part of this software may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the copyright holder.
- Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.
- For licensing inquiries, please contact: info@farmtech.ir

---

## ✨ Features

- 🔐 **User Authentication** – Secure login and registration with session-based tokens
- 💧 **Water & Wastewater Analysis** – Calculate final values based on water mixing ratios
- 🎯 **Target Elements** – Set desired nutrient levels with ion balance validation
- 🧮 **Automatic Fertilizer Calculation** – Calculate exact fertilizer amounts based on target values
- 📚 **Fertilizer Database** – Manage fertilizers, acids, and their elemental compositions
- 📊 **Data Interpretation** – Generate comprehensive reports with smart recommendations
- 🌓 **Light/Dark Theme** – Comfortable viewing in any lighting condition
- 🌐 **Persian & English** – Full bilingual support
- 🖨️ **Print Reports** – Export any page as a printable report

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue 3, TypeScript, Tailwind CSS, Vite |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy |
| **Database** | SQLite |
| **Authentication** | Session-based tokens with database storage |
| **State Management** | Pinia |
| **HTTP Client** | Axios |

---

## 📁 Project Structure

FarmTech-ProFertilizer/
│
├── .vscode/                          📁 تنظیمات VS Code
│   └── settings.json                 🔧 تنظیمات ویرایشگر
│
├── backend/                          📁 بک‌اند FastAPI
│   ├── app/                          📁 کدهای اصلی برنامه
│   │   ├── __init__.py               📄 پکیج اصلی
│   │   ├── config.py                 ⚙️ تنظیمات برنامه (SQLite)
│   │   ├── crud.py                   📂 عملیات پایه دیتابیس
│   │   ├── database.py               🗄️ اتصال به SQLite
│   │   ├── main.py                   🚀 نقطه ورود اصلی
│   │   ├── models.py                 📊 مدل‌های دیتابیس
│   │   ├── routes.py                 🛣️ مسیرهای API
│   │   ├── schemas.py                📝 طرح‌های Pydantic
│   │   ├── security.py               🔒 امنیت و احراز هویت
│   │   ├── services.py               🧮 منطق کسب‌وکار
│   │   └── utils.py                  🛠️ ابزارهای کمکی
│   │
│   ├── tests/                        📁 تست‌ها
│   │   ├── test_api.py               🧪 تست API
│   │   └── test_services.py          🧪 تست سرویس‌ها
│   │
│   ├── .env                          🔐 متغیرهای محیطی
│   ├── .env.example                  📄 نمونه متغیرهای محیطی
│   ├── .gitignore                    📄 نادیده‌گرفتن فایل‌ها
│   └── requirements.txt              📦 وابستگی‌های پایتون
│
├── frontend/                         📁 فرانت‌اند Vue.js
│   ├── .vscode/                      📁 تنظیمات VS Code
│   │   └── extensions.json           🔧 اکستنشن‌های پیشنهادی
│   │
│   ├── public/                       📁 فایل‌های عمومی
│   │   ├── fonts/                    📁 فونت‌های فارسی (۲۳ فایل)
│   │   ├── favicon.webp              🖼️ آیکون مرورگر
│   │   └── Logo.webp                 🖼️ لوگوی برنامه
│   │
│   ├── src/                          📁 کدهای اصلی فرانت‌اند
│   │   ├── assets/                   📁 فایل‌های استاتیک
│   │   │   ├── css/                  📁 استایل‌های CSS
│   │   │   │   └── main.css          🎨 استایل اصلی
│   │   │   ├── styles/               📁 استایل‌های اضافی
│   │   │   │   ├── fonts.css         🎨 تنظیمات فونت
│   │   │   │   ├── main.css          🎨 استایل اصلی
│   │   │   │   └── print.css         🖨️ استایل چاپ
│   │   │   ├── hero.png              🖼️ تصویر هدر
│   │   │   ├── vite.svg              🖼️ آیکون Vite
│   │   │   └── vue.svg               🖼️ آیکون Vue
│   │   │
│   │   ├── components/               📁 کامپوننت‌ها
│   │   │   ├── common/               📁 کامپوننت‌های عمومی
│   │   │   │   ├── AppButton.vue     🔘 دکمه سفارشی
│   │   │   │   ├── AppInput.vue      📝 ورودی سفارشی
│   │   │   │   └── AppSelect.vue     📋 انتخابگر سفارشی
│   │   │   │
│   │   │   ├── features/             📁 کامپوننت‌های ویژگی‌ها
│   │   │   │   ├── FertilizerCalcTab.vue    🧮 محاسبه کود
│   │   │   │   ├── FertilizerDBTab.vue      📚 پایگاه داده کودها
│   │   │   │   ├── HomeTab.vue              🏠 صفحه اصلی
│   │   │   │   ├── InterpretationTab.vue    📊 تفسیر داده‌ها
│   │   │   │   ├── ReportHeader.vue         📋 هدر گزارش
│   │   │   │   ├── TargetElementsTab.vue    🎯 عناصر هدف
│   │   │   │   └── WaterAnalysisTab.vue     💧 آنالیز آب
│   │   │   │
│   │   │   └── layout/               📁 کامپوننت‌های چیدمان
│   │   │       ├── AppFooter.vue     🦶 فوتر
│   │   │       └── AppHeader.vue     📌 هدر
│   │   │
│   │   ├── composables/              📁 توابع ترکیبی
│   │   │   ├── useCalculations.ts    🧮 محاسبات
│   │   │   ├── usePrint.ts           🖨️ چاپ
│   │   │   └── useValidation.ts      ✅ اعتبارسنجی
│   │   │
│   │   ├── router/                   📁 مسیریابی
│   │   │   └── index.ts              🛣️ مسیرها
│   │   │
│   │   ├── store/                    📁 مدیریت state
│   │   │   ├── modules/              📁 ماژول‌های store
│   │   │   │   ├── appStore.ts       🌐 تنظیمات برنامه
│   │   │   │   ├── calcStore.ts      🧮 محاسبات
│   │   │   │   ├── fertilizerStore.ts🧪 کودها
│   │   │   │   ├── reportStore.ts    📋 گزارش‌ها
│   │   │   │   ├── targetStore.ts    🎯 عناصر هدف
│   │   │   │   └── waterStore.ts     💧 آنالیز آب
│   │   │   └── index.ts              📄 نقطه ورود store
│   │   │
│   │   ├── types/                    📁 تعاریف TypeScript
│   │   │   └── index.ts              📄 نوع‌های全局
│   │   │
│   │   ├── utils/                    📁 ابزارهای کمکی
│   │   │   ├── constants.ts          📌 ثابت‌ها
│   │   │   └── helpers.ts            🛠️ توابع کمکی
│   │   │
│   │   ├── views/                    📁 صفحات اصلی
│   │   │   └── MainLayout.vue        📄 چیدمان اصلی
│   │   │
│   │   ├── App.vue                   📄 کامپوننت ریشه
│   │   ├── main.ts                   🚀 نقطه ورود
│   │   └── style.css                 🎨 استایل سراسری
│   │
│   ├── .env                          🔐 متغیرهای محیطی
│   ├── .gitignore                    📄 نادیده‌گرفتن فایل‌ها
│   ├── index.html                    📄 صفحه اصلی HTML
│   ├── package.json                  📦 وابستگی‌های Node.js
│   ├── postcss.config.js             ⚙️ تنظیمات PostCSS
│   ├── tailwind.config.js            ⚙️ تنظیمات Tailwind
│   ├── tsconfig.json                 ⚙️ تنظیمات TypeScript
│   └── vite.config.ts                ⚙️ تنظیمات Vite
│
├── scripts/                          📁 اسکریپت‌های کمکی (جدید)
│   ├── deploy.sh                     🚀 اسکریپت استقرار لینوکس
│   ├── deploy.bat                    🚀 اسکریپت استقرار ویندوز
│   └── cli.py                        🖥️ منوی CLI
│
├── docker-compose.yml                🐳 Docker Compose (جدید)
├── Dockerfile                        🐳 Dockerfile (جدید)
├── .env                              🔐 متغیرهای محیطی اصلی
├── int_DB.txt                        📄 اطلاعات دیتابیس (قابل نگهداری)
├── README.md                         📄 مستندات پروژه
└── setup.py                          📄 اسکریپت نصب

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/FarmTech-ProFertilizer.git
cd FarmTech-ProFertilizer

# 2. Run the CLI installer
python scripts/cli.py

# 3. Select option 4 to install dependencies
# 4. Select option 1 to run the full application
Manual Installation
bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
Access the Application
Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Docs: http://localhost:8000/docs

Health Check: http://localhost:8000/health
🧪 Running Tests
bash
cd backend
python tests/test_all.py
Or use the CLI menu (option 5).
🐳 Docker Deployment
bash
# Build and run
docker-compose up --build

# Stop
docker-compose down
🔧 Environment Variables
Create a .env file in the root directory:

env
# Database
DATABASE_URL=sqlite:///./farmtech.db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Application
APP_NAME=FarmTech - ProFertilizer
APP_VERSION=0.1.0
DEBUG=True

# API
VITE_API_URL=http://localhost:8000/api/v1
📸 Screenshots
(Add screenshots here)

👨‍💻 Developer
Omid Rahmani

GitHub: omidrph

Email: info@farmtech.ir

🏢 Organization
FarmTech
Smart Agriculture Solutions

🤖 AI Assistance
This project was developed with assistance from AI technologies to accelerate development and enhance code quality.

📄 License
Proprietary License

© 2026 FarmTech. All rights reserved.

This software is the exclusive property of FarmTech. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited. For licensing inquiries, please contact: info@farmtech.ir

📞 Contact
Email: info@farmtech.ir

Website: www.farmtech.ir

Phone: +98 910 473 9718

Made with ❤️ by FarmTech Team