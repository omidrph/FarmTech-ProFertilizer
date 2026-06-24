<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- مقدمه -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
      <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
        <span class="text-2xl">❓</span>
        سوالات متداول
      </h3>
      <p class="text-gray-600 dark:text-gray-400 text-sm sm:text-base">
        پاسخ به سوالات رایج کاربران درباره نرم‌افزار FarmTech - ProFertilizer
      </p>
    </div>

    <!-- جستجو -->
    <div class="relative">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="جستجو در سوالات..."
        class="w-full px-4 py-3 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
      />
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
    </div>

    <!-- تعداد نتایج -->
    <div v-if="filteredFAQs.length > 0" class="text-sm text-gray-500 dark:text-gray-400">
      {{ filteredFAQs.length }} سوال پیدا شد
    </div>

    <!-- لیست سوالات -->
    <div class="space-y-3">
      <div 
        v-for="(faq, index) in filteredFAQs" 
        :key="index"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-200 hover:shadow-md"
        :class="{ 'border-primary-300 dark:border-primary-700': faq.open }"
      >
        <!-- سوال -->
        <button
          @click="toggleFAQ(index)"
          class="w-full text-right px-4 sm:px-6 py-3 sm:py-4 flex items-start justify-between gap-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-primary-600 dark:text-primary-400 font-bold text-sm sm:text-base">سوال:</span>
              <span class="text-sm sm:text-base font-medium text-gray-900 dark:text-white">{{ faq.question }}</span>
            </div>
            <div class="flex flex-wrap gap-2 mt-1">
              <span 
                v-for="tag in faq.tags" 
                :key="tag"
                class="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': faq.open }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </button>

        <!-- پاسخ (قابل باز/بسته شدن) -->
        <div 
          v-show="faq.open"
          class="px-4 sm:px-6 pb-3 sm:pb-4 pt-1 border-t border-gray-100 dark:border-gray-700"
        >
          <div class="flex items-start gap-2">
            <span class="text-success-600 dark:text-success-400 font-bold text-sm sm:text-base">پاسخ:</span>
            <div class="text-sm sm:text-base text-gray-700 dark:text-gray-300 space-y-2" v-html="faq.answer"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- پیام عدم وجود نتیجه -->
    <div v-if="filteredFAQs.length === 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 sm:p-12 text-center">
      <svg class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-gray-500 dark:text-gray-400">هیچ سوالی با جستجوی شما پیدا نشد.</p>
      <button @click="searchQuery = ''" class="mt-2 text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm">
        نمایش همه سوالات
      </button>
    </div>

    <!-- پیشنهاد ارتباط -->
    <div class="bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800 p-4 sm:p-6 text-center">
      <p class="text-gray-700 dark:text-gray-300 text-sm sm:text-base">
        سوالی دارید که در این لیست نیست؟
      </p>
      <p class="text-gray-500 dark:text-gray-400 text-xs sm:text-sm mt-1">
        از طریق بخش <router-link to="/" @click="navigateToContact" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium">ارتباط با ما</router-link> با تیم پشتیبانی در تماس باشید.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// ===== Types =====
interface FAQItem {
  question: string;
  answer: string;
  tags: string[];
  open: boolean;
}

// ===== State =====
const searchQuery = ref('');

// ===== Data =====
const faqs = ref<FAQItem[]>([
  {
    question: 'چطور یک کود جدید به پایگاه داده اضافه کنم؟',
    answer: `
      <p>برای افزودن کود جدید مراحل زیر را دنبال کنید:</p>
      <ol class="list-decimal list-inside mr-4 space-y-1">
        <li>به تب <strong>خانه</strong> و سپس <strong>پایگاه داده کودها</strong> بروید</li>
        <li>روی دکمه <strong>افزودن کود جدید</strong> کلیک کنید</li>
        <li>نام کود، قیمت هر کیلوگرم و درصد عناصر را وارد کنید</li>
        <li>برای ذخیره، روی <strong>ذخیره</strong> کلیک کنید</li>
      </ol>
      <p class="mt-2 text-yellow-600 dark:text-yellow-400 text-sm">⚠️ توجه: درصد عناصر باید بین ۰ تا ۱۰۰ باشد.</p>
    `,
    tags: ['کود', 'پایگاه داده', 'افزودن'],
    open: false
  },
  {
    question: 'واحدهای اندازه‌گیری در نرم‌افزار چیست و چگونه تغییر کنم؟',
    answer: `
      <p>نرم‌افزار از سه واحد اندازه‌گیری پشتیبانی می‌کند:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li><strong>PPM/L</strong> (قسمت در میلیون) - واحد پیش‌فرض</li>
        <li><strong>MEQ/L</strong> (میلی‌اکی والان در لیتر)</li>
        <li><strong>MMOLS/L</strong> (میلی‌مول در لیتر)</li>
      </ul>
      <p class="mt-2">برای تغییر واحد، در بخش‌های <strong>عناصر هدف</strong> یا <strong>آنالیز آب</strong>، از منوی کشویی <strong>"واحد"</strong> استفاده کنید.</p>
    `,
    tags: ['واحد', 'اندازه‌گیری', 'PPM', 'MEQ', 'MMOL'],
    open: false
  },
  {
    question: 'تعادل یونی چیست و چرا مهم است؟',
    answer: `
      <p><strong>تعادل یونی</strong> به برابری مجموع بارهای مثبت (کاتیون‌ها) و منفی (آنیون‌ها) در محلول غذایی گفته می‌شود.</p>
      <p class="mt-2">اهمیت تعادل یونی:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li>جذب بهینه عناصر توسط گیاه</li>
        <li>پیشگیری از تنش‌های تغذیه‌ای</li>
        <li>افزایش بازده محصول</li>
      </ul>
      <p class="mt-2 text-green-600 dark:text-green-400 text-sm">✅ نرم‌افزار به صورت خودکار تعادل یونی را محاسبه و در صورت نامتعادل بودن هشدار می‌دهد.</p>
    `,
    tags: ['تعادل یونی', 'کاتیون', 'آنیون', 'تغذیه'],
    open: false
  },
  {
    question: 'چطور می‌توانم گزارش را چاپ کنم؟',
    answer: `
      <p>برای چاپ گزارش از هر بخشی از نرم‌افزار، کافیست روی دکمه <strong>🖨️ چاپ</strong> که در پایین هر تب وجود دارد کلیک کنید.</p>
      <p class="mt-2">همچنین می‌توانید از کلیدهای میانبر زیر استفاده کنید:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li><kbd class="bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded text-xs">Ctrl + P</kbd> (ویندوز/لینوکس)</li>
        <li><kbd class="bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded text-xs">Cmd + P</kbd> (مک)</li>
      </ul>
      <p class="mt-2 text-blue-600 dark:text-blue-400 text-sm">💡 نکته: قبل از چاپ، می‌توانید از حالت <strong>پیش‌نمایش چاپ</strong> مرورگر خود استفاده کنید.</p>
    `,
    tags: ['چاپ', 'گزارش', 'پرینت'],
    open: false
  },
  {
    question: 'آیا می‌توانم از نرم‌افزار به صورت آفلاین استفاده کنم؟',
    answer: `
      <p>نرم‌افزار <strong>FarmTech - ProFertilizer</strong> به صورت <strong>آفلاین</strong> کار می‌کند و تمام داده‌ها در دیتابیس محلی (SQLite) ذخیره می‌شوند.</p>
      <p class="mt-2">مزایای استفاده آفلاین:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li>بدون نیاز به اتصال اینترنت</li>
        <li>سرعت بالا در پردازش</li>
        <li>امنیت بیشتر داده‌ها</li>
      </ul>
      <p class="mt-2 text-yellow-600 dark:text-yellow-400 text-sm">⚠️ توجه: برای نصب اولیه و به‌روزرسانی‌ها به اتصال اینترنت نیاز دارید.</p>
    `,
    tags: ['آفلاین', 'اینترنت', 'دیتابیس', 'محلی'],
    open: false
  },
  {
    question: 'فرمول‌های محاسباتی نرم‌افزار بر چه اساسی است؟',
    answer: `
      <p>محاسبات نرم‌افزار بر اساس اصول علمی زیر انجام می‌شود:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li><strong>تبدیل واحدها:</strong> PPM ↔ MEQ ↔ MMOL با استفاده از وزن مولکولی و ظرفیت یونی</li>
        <li><strong>تعادل یونی:</strong> مجموع کاتیون‌ها = مجموع آنیون‌ها (با تلرانس ۰.۵)</li>
        <li><strong>محاسبه سهم کود:</strong> (وزن × درصد عنصر × خلوص) ÷ ۱۰۰</li>
        <li><strong>محاسبه هزینه:</strong> (وزن ÷ ۱۰۰۰) × قیمت هر کیلوگرم</li>
      </ul>
      <p class="mt-2 text-purple-600 dark:text-purple-400 text-sm">🔬 فرمول‌ها بر اساس استانداردهای بین‌المللی تغذیه گیاهان طراحی شده‌اند.</p>
    `,
    tags: ['فرمول', 'محاسبه', 'علمی', 'استاندارد'],
    open: false
  },
  {
    question: 'چطور می‌توانم داده‌های خود را پشتیبان‌گیری کنم؟',
    answer: `
      <p>برای پشتیبان‌گیری از داده‌های خود، می‌توانید از روش‌های زیر استفاده کنید:</p>
      <ol class="list-decimal list-inside mr-4 space-y-1">
        <li><strong>پشتیبان‌گیری دستی:</strong> فایل <code class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">farmtech.db</code> را کپی کنید</li>
        <li><strong>استفاده از ابزار backup_tool.py:</strong> در ریشه پروژه وجود دارد</li>
        <li><strong>خروجی JSON:</strong> از طریق API می‌توانید داده‌ها را به صورت JSON دریافت کنید</li>
      </ol>
      <p class="mt-2 text-green-600 dark:text-green-400 text-sm">✅ پیشنهاد می‌شود به صورت دوره‌ای از داده‌های خود پشتیبان‌گیری کنید.</p>
    `,
    tags: ['پشتیبان', 'بکاپ', 'داده', 'امنیت'],
    open: false
  },
  {
    question: 'آیا نرم‌افزار از چند زبان پشتیبانی می‌کند؟',
    answer: `
      <p>در حال حاضر نرم‌افزار به دو زبان زیر در دسترس است:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li><strong>فارسی</strong> (زبان پیش‌فرض)</li>
        <li><strong>انگلیسی</strong> (در حال توسعه)</li>
      </ul>
      <p class="mt-2 text-blue-600 dark:text-blue-400 text-sm">💡 برای تغییر زبان، از بخش تنظیمات (در حال توسعه) استفاده کنید.</p>
    `,
    tags: ['زبان', 'فارسی', 'انگلیسی', 'چندزبانه'],
    open: false
  },
  {
    question: 'چه عناصری در نرم‌افزار قابل تنظیم هستند؟',
    answer: `
      <p>نرم‌افزار از ۱۵ عنصر اصلی تغذیه گیاه پشتیبانی می‌کند:</p>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-1 mt-2">
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">N-NO3</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">P</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">S</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">N-NH4</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">K</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Ca</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Mg</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Na</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Cl</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Fe</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Mn</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Zn</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">B</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Cu</span>
        <span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs text-center">Mo</span>
      </div>
      <p class="mt-2 text-gray-500 dark:text-gray-400 text-xs">* عناصر پرکاربرد و ضروری برای تغذیه گیاهان</p>
    `,
    tags: ['عناصر', 'تغذیه', 'جدول تناوبی'],
    open: false
  },
  {
    question: 'چطور می‌توانم با تیم پشتیبانی تماس بگیرم؟',
    answer: `
      <p>برای ارتباط با تیم پشتیبانی FarmTech از روش‌های زیر استفاده کنید:</p>
      <ul class="list-disc list-inside mr-4 space-y-1">
        <li><strong>تلفن:</strong> ۰۲۱-۱۲۳۴۵۶۷۸</li>
        <li><strong>ایمیل:</strong> info@farmtech.ir</li>
        <li><strong>بخش ارتباط با ما:</strong> در منوی اصلی نرم‌افزار</li>
      </ul>
      <p class="mt-2 text-green-600 dark:text-green-400 text-sm">✅ تیم پشتیبانی در ساعات کاری پاسخگوی شما خواهد بود.</p>
    `,
    tags: ['پشتیبانی', 'تماس', 'ارتباط'],
    open: false
  }
]);

// ===== Computed =====
const filteredFAQs = computed(() => {
  if (!searchQuery.value.trim()) {
    return faqs.value;
  }
  const query = searchQuery.value.trim().toLowerCase();
  return faqs.value.filter(faq => 
    faq.question.toLowerCase().includes(query) ||
    faq.answer.toLowerCase().includes(query) ||
    faq.tags.some(tag => tag.toLowerCase().includes(query))
  );
});

// ===== Methods =====
const toggleFAQ = (index: number) => {
  faqs.value[index].open = !faqs.value[index].open;
};

const navigateToContact = () => {
  // این تابع توسط کامپوننت والد مدیریت می‌شود
  // از طریق emit یا router
  router.push('/');
  // در اینجا باید تب contact فعال شود
  // این کار در MainLayout انجام می‌شود
};
</script>

<style scoped>
kbd {
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  background-color: #f3f4f6;
  padding: 0.1rem 0.4rem;
  border-radius: 0.25rem;
  border: 1px solid #d1d5db;
}

.dark kbd {
  background-color: #374151;
  border-color: #4b5563;
}

code {
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  background-color: #f3f4f6;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
}

.dark code {
  background-color: #374151;
}

.list-decimal {
  list-style-type: decimal;
}

.list-inside {
  list-style-position: inside;
}
</style>