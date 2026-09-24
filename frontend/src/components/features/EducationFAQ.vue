<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- ============================================================ -->
    <!-- هدر معرفی -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">سوالات متداول</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">پاسخ به پرسش‌های رایج کاربران سهند کود</p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جستجو و فیلتر -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-3 sm:p-4 space-y-3">
      <!-- جستجو -->
      <div class="relative">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="جستجو در سوالات..."
          class="w-full px-4 py-2.5 pr-10 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all"
        />
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <button
          v-if="searchQuery"
          @click="searchQuery = ''"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- فیلتر دسته‌بندی -->
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="activeCategory = cat.id"
          class="px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
          :class="activeCategory === cat.id
            ? 'bg-primary-600 text-white'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'"
        >
          {{ cat.label }}
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- لیست سوالات -->
    <!-- ============================================================ -->
    <div v-if="filteredFAQs.length > 0" class="space-y-3">
      <div
        v-for="(faq, index) in filteredFAQs"
        :key="faq.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-200 hover:shadow-md"
        :class="{ 'border-primary-300 dark:border-primary-700': openFAQ === faq.id }"
      >
        <!-- سوال -->
        <button
          @click="toggleFAQ(faq.id)"
          class="w-full text-right px-4 sm:px-5 py-4 flex items-start justify-between gap-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div class="flex-1 min-w-0">
            <div class="flex items-start gap-2">
              <span class="flex-shrink-0 w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-[10px] font-bold flex items-center justify-center mt-0.5">
                {{ toPersianNum(index + 1) }}
              </span>
              <span class="text-sm sm:text-base font-medium text-gray-900 dark:text-white text-right">{{ faq.question }}</span>
            </div>
            <div class="flex flex-wrap gap-1.5 mt-2 pr-8">
              <span
                v-for="tag in faq.tags"
                :key="tag"
                class="text-[10px] px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full"
              >#{{ tag }}</span>
            </div>
          </div>
          <svg
            class="w-5 h-5 flex-shrink-0 mt-0.5 transition-transform duration-300 text-gray-400"
            :class="{ 'rotate-180': openFAQ === faq.id }"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>

        <!-- پاسخ -->
        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="max-h-0 opacity-0"
          enter-to-class="max-h-[2000px] opacity-100"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="max-h-[2000px] opacity-100"
          leave-to-class="max-h-0 opacity-0"
        >
          <div v-show="openFAQ === faq.id" class="overflow-hidden">
            <div class="px-4 sm:px-5 pb-4 pt-1 border-t border-gray-100 dark:border-gray-700">
              <div class="flex items-start gap-2 pt-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-md bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 text-[10px] font-bold flex items-center justify-center mt-0.5">
                  پ
                </span>
                <div class="text-sm text-gray-700 dark:text-gray-300 space-y-2 leading-relaxed [&_strong]:text-gray-900 [&_strong]:dark:text-white [&_code]:bg-gray-100 [&_code]:dark:bg-gray-700 [&_code]:px-1 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-xs [&_kbd]:bg-gray-100 [&_kbd]:dark:bg-gray-700 [&_kbd]:px-1.5 [&_kbd]:py-0.5 [&_kbd]:rounded [&_kbd]:text-xs [&_kbd]:font-mono [&_ul]:list-disc [&_ul]:pr-5 [&_ul]:space-y-1 [&_ol]:list-decimal [&_ol]:pr-5 [&_ol]:space-y-1" v-html="faq.answer"></div>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- حالت خالی -->
    <!-- ============================================================ -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 sm:p-12 text-center">
      <svg class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-gray-500 dark:text-gray-400 text-sm">هیچ سوالی با جستجوی شما مطابقت ندارد.</p>
      <button
        @click="resetFilters"
        class="mt-3 text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium"
      >
        نمایش همه سوالات
      </button>
    </div>

    <!-- ============================================================ -->
    <!-- پیشنهاد ارتباط -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800 p-4 sm:p-5 text-center">
      <p class="text-sm text-gray-700 dark:text-gray-300">
        سوالی دارید که در این لیست نیست؟
      </p>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
        از طریق بخش
        <router-link to="/" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium mx-1">ارتباط با ما</router-link>
        با تیم پشتیبانی سهند کود در تماس باشید.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
  tags: string[];
}

const toPersianNum = (n: number): string => n.toLocaleString('fa-IR', { useGrouping: false });

const searchQuery = ref('');
const activeCategory = ref('all');
const openFAQ = ref<string | null>(null);

const categories = [
  { id: 'all', label: 'همه' },
  { id: 'getting-started', label: 'شروع کار' },
  { id: 'fertilizer', label: 'کودها' },
  { id: 'calculation', label: 'محاسبات' },
  { id: 'optimization', label: 'بهینه‌سازی' },
  { id: 'water', label: 'آب و pH' },
  { id: 'reports', label: 'گزارش‌ها' },
  { id: 'technical', label: 'فنی' },
];

const faqs: FAQItem[] = [
  // ===== شروع کار =====
  {
    id: 'start-1',
    question: 'چگونه یک گزارش جدید ایجاد کنم؟',
    category: 'getting-started',
    tags: ['گزارش', 'شروع'],
    answer: `
      <p>برای ایجاد گزارش جدید:</p>
      <ol>
        <li>از منوی بالای صفحه روی «گزارش» کلیک کنید.</li>
        <li>گزینه «جدید» را انتخاب کنید (یا از کلید میانبر <kbd>Ctrl+N</kbd> استفاده کنید).</li>
        <li>مشخصات گیاه، فصل کشت، مرحله رشد و تاریخ را وارد کنید.</li>
        <li>روی «ذخیره گزارش» کلیک کنید.</li>
      </ol>
      <p><strong>نکته:</strong> بدون ایجاد گزارش، امکان استفاده از سایر بخش‌های سامانه وجود ندارد.</p>
    `,
  },
  {
    id: 'start-2',
    question: 'چگونه یک گزارش ذخیره‌شده را بازیابی کنم؟',
    category: 'getting-started',
    tags: ['گزارش', 'بازیابی'],
    answer: `
      <p>برای بازیابی گزارش‌های قبلی:</p>
      <ol>
        <li>از منوی بالا روی «گزارش» کلیک کنید.</li>
        <li>گزینه «بازکردن» را انتخاب کنید (یا <kbd>Ctrl+O</kbd>).</li>
        <li>در پنجره باز شده، لیست گزارش‌های شما نمایش داده می‌شود.</li>
        <li>روی «بارگذاری» گزارش مورد نظر کلیک کنید.</li>
      </ol>
      <p>تمام محاسبات، فرمول نهایی و هشدارهای قبلی به صورت کامل بازیابی می‌شوند.</p>
    `,
  },
  {
    id: 'start-3',
    question: 'چند گزارش می‌توانم در حساب کاربری خود داشته باشم؟',
    category: 'getting-started',
    tags: ['گزارش', 'محدودیت'],
    answer: `
      <p>شما می‌توانید تا <strong>۲۵۰ گزارش</strong> در حساب کاربری خود ذخیره کنید.</p>
      <p>اگر به سقف ظرفیت رسیدید، می‌توانید گزارش‌های قدیمی‌تر را حذف کنید تا فضا برای گزارش‌های جدید باز شود.</p>
    `,
  },
  // ===== کودها =====
  {
    id: 'fert-1',
    question: 'چند نوع کود در پایگاه داده سیستم وجود دارد؟',
    category: 'fertilizer',
    tags: ['کود', 'پایگاه داده'],
    answer: `
      <p>پایگاه داده سیستم شامل <strong>بیش از ۴۲ کود استاندارد ایرانی</strong> است که از برندهای معتبر مانند:</p>
      <ul>
        <li>اطلس</li>
        <li>رازک شیمی</li>
        <li>ردسا</li>
        <li>گل سم گرگان</li>
        <li>و سایر تولیدکنندگان</li>
      </ul>
      <p>گردآوری شده‌اند. این کودها شامل NPK، کلات‌های EDTA/EDDHA، سولفات‌ها، اسیدها و ریزمغذی‌ها هستند.</p>
    `,
  },
  {
    id: 'fert-2',
    question: 'تفاوت کود سیستمی و کود شخصی چیست؟',
    category: 'fertilizer',
    tags: ['کود', 'سیستمی', 'شخصی'],
    answer: `
      <p><strong>کودهای سیستمی:</strong></p>
      <ul>
        <li>توسط تیم سهند کود تعریف شده‌اند و قابل ویرایش یا حذف نیستند.</li>
        <li>برای استفاده، باید آن‌ها را «کوپ» کنید تا در بخش شخصی شما قرار بگیرند.</li>
      </ul>
      <p><strong>کودهای شخصی:</strong></p>
      <ul>
        <li>کودهایی که خودتان اضافه می‌کنید یا از سیستم کوپ می‌کنید.</li>
        <li>قابل ویرایش، حذف و تنظیم بر اساس نیاز شما هستند.</li>
      </ul>
    `,
  },
  {
    id: 'fert-3',
    question: 'چگونه کود شخصی جدید بسازم؟',
    category: 'fertilizer',
    tags: ['کود', 'افزودن'],
    answer: `
      <p>برای افزودن کود جدید:</p>
      <ol>
        <li>به تب «پایگاه داده کودها» بروید.</li>
        <li>روی دکمه «افزودن کود جدید» کلیک کنید.</li>
        <li>نام، برند، فرم فیزیکی، درصد خلوص و قیمت هر کیلوگرم را وارد کنید.</li>
        <li>درصد هر عنصر (N-NO3، P، K، Ca و...) را وارد کنید.</li>
        <li>روی «ذخیره» کلیک کنید.</li>
      </ol>
      <p><strong>توجه:</strong> مجموع درصد عناصر باید حداکثر ۱۰۰٪ باشد.</p>
    `,
  },
  // ===== محاسبات =====
  {
    id: 'calc-1',
    question: 'واحدهای اندازه‌گیری در سامانه چه هستند و چگونه تغییر می‌کنند؟',
    category: 'calculation',
    tags: ['واحد', 'PPM', 'MEQ', 'MMOL'],
    answer: `
      <p>سامانه از سه واحد اندازه‌گیری پشتیبانی می‌کند:</p>
      <ul>
        <li><strong>PPM/L</strong> (قسمت در میلیون) - واحد پیش‌فرض</li>
        <li><strong>MEQ/L</strong> (میلی‌اکی‌والان در لیتر)</li>
        <li><strong>MMOL/L</strong> (میلی‌مول در لیتر)</li>
      </ul>
      <p>برای تغییر واحد، در تب «عناصر هدف» یا «آنالیز آب»، از منوی کشویی بالای جدول استفاده کنید.</p>
    `,
  },
  {
    id: 'calc-2',
    question: 'تعادل یونی چیست و چرا مهم است؟',
    category: 'calculation',
    tags: ['تعادل یونی', 'کاتیون', 'آنیون'],
    answer: `
      <p><strong>تعادل یونی</strong> به برابری مجموع بارهای مثبت (کاتیون‌ها) و منفی (آنیون‌ها) در محلول غذایی گفته می‌شود.</p>
      <p>اهمیت آن:</p>
      <ul>
        <li>جذب بهینه عناصر توسط گیاه</li>
        <li>پیشگیری از تنش‌های تغذیه‌ای</li>
        <li>افزایش بازده محصول</li>
      </ul>
      <p>سامانه سهند کود به صورت خودکار تعادل یونی را محاسبه و در صورت نامتعادل بودن هشدار می‌دهد.</p>
    `,
  },
  {
    id: 'calc-3',
    question: 'چگونه pH و EC محلول نهایی محاسبه می‌شود؟',
    category: 'calculation',
    tags: ['pH', 'EC'],
    answer: `
      <p><strong>محاسبه EC:</strong> بر اساس فرمول استاندارد هیدروپونیک:</p>
      <p><code>EC (dS/m) = میانگین(مجموع meq/L کاتیون‌ها، مجموع meq/L آنیون‌ها) × 0.1</code></p>
      <p><strong>تخمین pH:</strong> بر اساس نسبت نیتروژن آمونیومی به کل نیتروژن محاسبه می‌شود. هرچه نسبت NH4 بیشتر باشد، pH محیط ریشه کاهش می‌یابد.</p>
      <p><strong>توجه:</strong> مقدار pH یک تخمین است و برای دقت بیشتر باید با pH متر اندازه‌گیری شود.</p>
    `,
  },
  // ===== بهینه‌سازی =====
  {
    id: 'opt-1',
    question: 'الگوریتم بهینه‌سازی NNLS چیست؟',
    category: 'optimization',
    tags: ['NNLS', 'بهینه‌سازی'],
    answer: `
      <p><strong>NNLS (کمترین مربعات نامنفی)</strong> یک الگوریتم ریاضی است که بهترین ترکیب از کودها را برای رسیدن به اهداف تغذیه‌ای پیدا می‌کند.</p>
      <p>مزیت اصلی آن:</p>
      <ul>
        <li>تضمین می‌کند هیچ وزن منفی برای کود محاسبه نشود.</li>
        <li>سرعت بالایی در حل مسائل بزرگ دارد.</li>
        <li>نتایج پایدار و قابل اتکا ارائه می‌دهد.</li>
      </ul>
    `,
  },
  {
    id: 'opt-2',
    question: 'تفاوت حالت‌های بهینه‌سازی «دقیق‌ترین»، «کم‌تعدادترین» و «ارزان‌ترین» چیست؟',
    category: 'optimization',
    tags: ['حالت بهینه‌سازی'],
    answer: `
      <ul>
        <li><strong>دقیق‌ترین:</strong> کمترین خطا نسبت به عناصر هدف را دارد (پیش‌فرض).</li>
        <li><strong>کم‌تعدادترین:</strong> با کمترین تعداد کود ممکن، شما را به هدف می‌رساند (مناسب برای تهیه ساده‌تر).</li>
        <li><strong>ارزان‌ترین:</strong> کم‌هزینه‌ترین ترکیب را پیدا می‌کند، حتی اگر دقت کمی کاهش یابد.</li>
      </ul>
    `,
  },
  {
    id: 'opt-3',
    question: 'چگونه از تعادل یونی خودکار استفاده کنم؟',
    category: 'optimization',
    tags: ['تعادل یونی خودکار', 'auto_balance'],
    answer: `
      <p>در تب «محاسبه خودکار مقدار کود»، پس از انتخاب کودها، روی «تنظیمات پیشرفته» کلیک کنید و گزینه <strong>«تعادل یونی خودکار»</strong> را فعال کنید.</p>
      <p>با فعال بودن این گزینه، اگر تعادل یونی برقرار نباشد، سیستم به صورت خودکار یون‌های پادبار (Na یا Cl) را اضافه می‌کند.</p>
    `,
  },
  // ===== آب و pH =====
  {
    id: 'water-1',
    question: 'چرا باید آنالیز آب را وارد کنم؟',
    category: 'water',
    tags: ['آب', 'آنالیز'],
    answer: `
      <p>آب منبع اصلی تأمین عناصر غذایی برای گیاهان است. با وارد کردن آنالیز آب، سامانه می‌تواند:</p>
      <ul>
        <li>عناصر موجود در آب را در محاسبات لحاظ کند.</li>
        <li>مقدار دقیق کودهای مورد نیاز را کاهش دهد.</li>
        <li>خطر شوری و رسوب را پیش‌بینی کند.</li>
      </ul>
      <p>هرچه دقت آنالیز آب بیشتر باشد، نتایج دقیق‌تر خواهند بود.</p>
    `,
  },
  {
    id: 'water-2',
    question: 'چگونه از ابزارک محاسبه pH استفاده کنم؟',
    category: 'water',
    tags: ['pH', 'ابزارک'],
    answer: `
      <p>برای استفاده از ابزارک pH:</p>
      <ol>
        <li>به تب «ابزارک‌ها» بروید و «ماشین حساب pH» را انتخاب کنید.</li>
        <li>روش محاسبه را انتخاب کنید (تئوری یا تیتراسیون).</li>
        <li>مشخصات محلول، pH فعلی، pH هدف و ماده شیمیایی را وارد کنید.</li>
        <li>روی «محاسبه دوز» کلیک کنید.</li>
      </ol>
      <p>نتیجه شامل مقدار دقیق اسید/باز، برنامه تزریق مرحله‌ای و هشدارهای ایمنی است.</p>
    `,
  },
  // ===== گزارش‌ها =====
  {
    id: 'report-1',
    question: 'چگونه گزارش PDF بسازم؟',
    category: 'reports',
    tags: ['PDF', 'چاپ'],
    answer: `
      <p>برای ساخت خروجی PDF:</p>
      <ol>
        <li>پس از انجام محاسبه، به گام «نتیجه» بروید.</li>
        <li>روی دکمه «خروجی PDF» کلیک کنید.</li>
        <li>در پنجره‌ای که باز می‌شود، گزینه «Save as PDF» را انتخاب کنید.</li>
      </ol>
      <p>گزارش PDF شامل خلاصه KPIs، جدول کودها، نمودار عناصر و هشدارها است.</p>
    `,
  },
  // ===== فنی =====
  {
    id: 'tech-1',
    question: 'داده‌های من کجا ذخیره می‌شوند؟',
    category: 'technical',
    tags: ['داده', 'امنیت', 'ذخیره'],
    answer: `
      <p>داده‌های شما در یک پایگاه داده امن PostgreSQL ذخیره می‌شوند. ویژگی‌های امنیتی:</p>
      <ul>
        <li>رمزنگاری رمز عبور با الگوریتم bcrypt</li>
        <li>مدیریت نشست‌های امن</li>
        <li>پشتیبانی از احراز هویت دو مرحله‌ای (2FA)</li>
        <li>محدودیت تعداد درخواست‌ها برای جلوگیری از حملات</li>
      </ul>
    `,
  },
  {
    id: 'tech-2',
    question: 'آیا امکان استفاده از سامانه به صورت آفلاین وجود دارد؟',
    category: 'technical',
    tags: ['آفلاین'],
    answer: `
      <p>خیر، سهند کود یک سامانه وب‌محور است و برای استفاده به اتصال اینترنت نیاز دارد. با این حال، تمام داده‌های شما روی سرور ذخیره می‌شوند و در هر زمان و از هر دستگاهی قابل دسترسی هستند.</p>
    `,
  },
  {
    id: 'tech-3',
    question: 'چند دستگاه می‌توانند همزمان از حساب من استفاده کنند؟',
    category: 'technical',
    tags: ['نشست', 'دستگاه'],
    answer: `
      <p>در هر لحظه فقط یک نشست فعال می‌تواند وجود داشته باشد. با ورود از دستگاه جدید، نشست قبلی به صورت خودکار بسته می‌شود.</p>
      <p><strong>نکته امنیتی:</strong> اگر متوجه ورود غیرمجاز به حساب خود شدید، فوراً رمز عبور خود را تغییر دهید.</p>
    `,
  },
];

const filteredFAQs = computed(() => {
  let result = faqs;
  if (activeCategory.value !== 'all') {
    result = result.filter(f => f.category === activeCategory.value);
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase();
    result = result.filter(f =>
      f.question.toLowerCase().includes(q) ||
      f.answer.toLowerCase().includes(q) ||
      f.tags.some(t => t.toLowerCase().includes(q))
    );
  }
  return result;
});

const toggleFAQ = (id: string) => {
  openFAQ.value = openFAQ.value === id ? null : id;
};

const resetFilters = () => {
  searchQuery.value = '';
  activeCategory.value = 'all';
};
</script>

<style scoped>
kbd, code {
  font-family: 'Courier New', monospace;
}
</style>