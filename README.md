FarmTech-ProFertilizer/
│
├── .vscode/                          ✅ تنظیمات VS Code
│   └── settings.json
│
├── backend/                          ✅ بک‌اند FastAPI
│   ├── app/                          ✅ کدهای اصلی برنامه
│   │   ├── __pycache__/              (فایل‌های کش پایتون - قابل نادیده گرفتن)
│   │   ├── __init__.py               ✅
│   │   ├── config.py                 ✅ تنظیمات برنامه
│   │   ├── crud.py                   ✅ عملیات پایه دیتابیس
│   │   ├── database.py               ✅ اتصال به دیتابیس
│   │   ├── main.py                   ✅ نقطه ورود اصلی
│   │   ├── models.py                 ✅ مدل‌های دیتابیس
│   │   ├── routes.py                 ✅ مسیرهای API
│   │   ├── schemas.py                ✅ طرح‌های Pydantic
│   │   ├── security.py               ✅ امنیت و احراز هویت
│   │   ├── services.py               ✅ منطق کسب‌وکار
│   │   └── utils.py                  ✅ ابزارهای کمکی
│   │
│   ├── migrations/                   ✅ مهاجرت‌های دیتابیس
│   │   ├── versions/                 (خالی - برای آینده)
│   │   └── alembic.ini               ✅
│   │
│   ├── tests/                        ✅ تست‌ها
│   │   ├── test_api.py               ✅ (خالی - نیاز به پر شدن)
│   │   └── test_services.py          ✅ (خالی - نیاز به پر شدن)
│   │
│   ├── venv/                         ✅ محیط مجازی پایتون
│   │   ├── Include/
│   │   ├── Lib/
│   │   ├── Scripts/
│   │   └── pyvenv.cfg
│   │
│   ├── .env                          ✅ متغیرهای محیطی
│   ├── .env.example                  ✅ نمونه متغیرهای محیطی
│   ├── .gitignore                    ✅
│   ├── docker-compose.yml            ✅
│   ├── Dockerfile                    ✅
│   └── requirements.txt              ✅ وابستگی‌ها
│
├── docker/                           ✅ تنظیمات Docker
│   ├── postgres/
│   │   └── init.sql                  ✅ (خالی - نیاز به اسکریپت)
│   └── docker-compose.yml            ✅
│
├── frontend/                         ✅ فرانت‌اند Vue.js
│   ├── .vscode/
│   │   └── extensions.json           ✅
│   ├── public/
│   │   ├── fonts/                    ✅ فونت‌های فارسی (۲۳ فایل)
│   │   ├── favicon.webp              ✅
│   │   └── Logo.webp                 ✅
│   ├── src/
│   │   ├── assets/
│   │   │   ├── css/
│   │   │   │   └── main.css          ✅
│   │   │   ├── styles/
│   │   │   │   ├── fonts.css         ✅
│   │   │   │   ├── main.css          ✅
│   │   │   │   └── print.css         ✅
│   │   │   ├── hero.png              ✅
│   │   │   ├── vite.svg              ✅
│   │   │   └── vue.svg               ✅
│   │   ├── components/
│   │   │   ├── common/               ✅ کامپوننت‌های عمومی
│   │   │   │   ├── AppButton.vue     ✅
│   │   │   │   ├── AppInput.vue      ✅
│   │   │   │   └── AppSelect.vue     ✅
│   │   │   ├── features/             ✅ کامپوننت‌های ویژگی‌ها
│   │   │   │   ├── FertilizerCalcTab.vue    ✅
│   │   │   │   ├── FertilizerDBTab.vue      ✅
│   │   │   │   ├── HomeTab.vue              ✅
│   │   │   │   ├── InterpretationTab.vue    ✅
│   │   │   │   ├── ReportHeader.vue         ✅
│   │   │   │   ├── TargetElementsTab.vue    ✅
│   │   │   │   └── WaterAnalysisTab.vue     ✅
│   │   │   └── layout/               ✅ کامپوننت‌های چیدمان
│   │   │       ├── AppFooter.vue     ✅
│   │   │       └── AppHeader.vue     ✅
│   │   ├── composables/              ✅ توابع ترکیبی
│   │   │   ├── useCalculations.ts    ✅
│   │   │   ├── usePrint.ts           ✅
│   │   │   └── useValidation.ts      ✅
│   │   ├── router/
│   │   │   └── index.ts              ✅
│   │   ├── store/                    ✅ مدیریت state
│   │   │   ├── modules/
│   │   │   │   ├── appStore.ts       ✅
│   │   │   │   ├── calcStore.ts      ✅
│   │   │   │   ├── fertilizerStore.ts✅
│   │   │   │   ├── reportStore.ts    ✅
│   │   │   │   ├── targetStore.ts    ✅
│   │   │   │   └── waterStore.ts     ✅
│   │   │   └── index.ts              ✅
│   │   ├── types/
│   │   │   └── index.ts              ✅
│   │   ├── utils/
│   │   │   ├── constants.ts          ✅
│   │   │   └── helpers.ts            ✅
│   │   ├── views/
│   │   │   └── MainLayout.vue        ✅
│   │   ├── App.vue                   ✅
│   │   ├── main.ts                   ✅
│   │   └── style.css                 ✅
│   ├── .env                          ✅
│   ├── .gitignore                    ✅
│   ├── index.html                    ✅
│   ├── package-lock.json             ✅
│   ├── package.json                  ✅
│   ├── postcss.config.js             ✅
│   ├── tailwind.config.js            ✅
│   ├── tsconfig.app.json             ✅
│   ├── tsconfig.json                 ✅
│   ├── tsconfig.node.json            ✅
│   └── vite.config.ts                ✅
│
├── .env                              ✅
├── FarmTech-Docker.session.sql       (فایل موقت - قابل حذف)
├── int_DB.txt                        (فایل اطلاعات - قابل نگهداری)
└── README.md                         ✅