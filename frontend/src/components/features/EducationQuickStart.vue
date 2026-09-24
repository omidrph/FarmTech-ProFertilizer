<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- ============================================================ -->
    <!-- هدر معرفی -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">شروع سریع با سهند کود</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">مراحل گام‌به‌گام برای رسیدن به فرمول کودی دقیق</p>
        </div>
      </div>

      <!-- نوار پیشرفت کلی -->
      <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
        <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-2">
          <span>پیشرفت شما در مطالعه</span>
          <span class="tabular-nums">{{ progressPercent }}٪</span>
        </div>
        <div class="h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
          <div
            class="h-full rounded-full bg-primary-500 transition-all duration-500"
            :style="{ width: progressPercent + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مراحل -->
    <!-- ============================================================ -->
    <div class="space-y-3 sm:space-y-4">
      <div
        v-for="(step, index) in steps"
        :key="step.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700 shadow-md': openSteps[step.id] }"
        @click="toggleStep(step.id)"
      >
        <!-- هدر کارت -->
        <div class="p-4 sm:p-5">
          <div class="flex items-start gap-3 sm:gap-4">
            <!-- شماره مرحله -->
            <div
              class="flex-shrink-0 w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors"
              :class="getStepCircleClass(step, index)"
            >
              <svg v-if="isStepCompleted(step.id)" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
              </svg>
              <template v-else>{{ toPersianNum(index + 1) }}</template>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-2 mb-1">
                <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">{{ step.title }}</h4>
                <span
                  v-if="step.badge"
                  class="text-[10px] font-medium px-2 py-0.5 rounded-full"
                  :class="step.badge.class"
                >{{ step.badge.text }}</span>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{{ step.description }}</p>
            </div>

            <!-- آیکون باز/بسته -->
            <svg
              class="w-5 h-5 flex-shrink-0 mt-1 text-gray-400 transition-transform duration-300"
              :class="{ 'rotate-180': openSteps[step.id] }"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>

        <!-- محتوای بازشونده -->
        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="max-h-0 opacity-0"
          enter-to-class="max-h-[2000px] opacity-100"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="max-h-[2000px] opacity-100"
          leave-to-class="max-h-0 opacity-0"
        >
          <div v-show="openSteps[step.id]" class="overflow-hidden">
            <div class="px-4 sm:px-5 pb-5 pr-12 sm:pr-16 border-t border-gray-100 dark:border-gray-700 pt-4 space-y-4">

              <!-- جزئیات -->
              <div v-if="step.details.length">
                <h5 class="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  مراحل انجام
                </h5>
                <ol class="space-y-2">
                  <li
                    v-for="(detail, i) in step.details"
                    :key="i"
                    class="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-300 leading-relaxed"
                  >
                    <span class="flex-shrink-0 w-5 h-5 rounded-md bg-gray-100 dark:bg-gray-700 text-[10px] font-bold text-gray-500 dark:text-gray-400 flex items-center justify-center mt-0.5">
                      {{ toPersianNum(i + 1) }}
                    </span>
                    <span v-html="detail"></span>
                  </li>
                </ol>
              </div>

              <!-- نکات -->
              <div v-if="step.tips.length" class="bg-blue-50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-800/30 rounded-lg p-3">
                <h5 class="text-xs font-semibold text-blue-700 dark:text-blue-300 mb-1.5 flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  نکات مهم
                </h5>
                <ul class="space-y-1">
                  <li v-for="(tip, i) in step.tips" :key="i" class="text-xs text-blue-700 dark:text-blue-300 leading-relaxed flex items-start gap-1.5">
                    <span class="text-blue-500 mt-0.5">•</span>
                    <span v-html="tip"></span>
                  </li>
                </ul>
              </div>

              <!-- هشدارها -->
              <div v-if="step.warnings.length" class="bg-amber-50 dark:bg-amber-900/10 border border-amber-100 dark:border-amber-800/30 rounded-lg p-3">
                <h5 class="text-xs font-semibold text-amber-700 dark:text-amber-300 mb-1.5 flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                  </svg>
                  توجه
                </h5>
                <ul class="space-y-1">
                  <li v-for="(warning, i) in step.warnings" :key="i" class="text-xs text-amber-700 dark:text-amber-300 leading-relaxed flex items-start gap-1.5">
                    <span class="text-amber-500 mt-0.5">•</span>
                    <span v-html="warning"></span>
                  </li>
                </ul>
              </div>

            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- دکمه ریست -->
    <!-- ============================================================ -->
    <div v-if="visitedCount > 0" class="flex justify-center pt-2">
      <button
        @click="resetProgress"
        class="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors flex items-center gap-1.5"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        شروع مجدد مطالعه
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Step {
  id: string;
  title: string;
  description: string;
  details: string[];
  tips: string[];
  warnings: string[];
  badge?: { text: string; class: string };
}

const toPersianNum = (n: number): string => n.toLocaleString('fa-IR', { useGrouping: false });

const steps: Step[] = [
  {
    id: 'register',
    title: 'ثبت‌نام و ورود به حساب کاربری',
    description: 'با شماره تلفن همراه خود یک حساب کاربری ایجاد کنید و وارد سامانه شوید.',
    badge: { text: 'الزامی', class: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' },
    details: [
      'روی دکمه «ثبت‌نام» در صفحه ورود کلیک کنید.',
      'نام، نام خانوادگی، شماره تلفن همراه و رمز عبور خود را وارد کنید.',
      'شماره تلفن باید با <code class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">09</code> شروع شود و ۱۱ رقم باشد.',
      'رمز عبور باید حداقل ۸ کاراکتر و شامل حرف بزرگ، حرف کوچک، عدد و کاراکتر خاص باشد.',
      'پس از ثبت‌نام، به صورت خودکار وارد حساب کاربری خود می‌شوید.',
    ],
    tips: [
      'توکن احراز هویت تا ۲۴ ساعت معتبر است.',
      'می‌توانید با خیال راحت از سامانه در چند تب استفاده کنید.',
    ],
    warnings: [
      'شماره تلفن باید یکتا باشد و قبلاً ثبت نشده باشد.',
    ],
  },
  {
    id: 'create-report',
    title: 'ایجاد گزارش و تعریف مشخصات گیاه',
    description: 'برای شروع هر محاسبه، ابتدا یک گزارش جدید بسازید و مشخصات محصول خود را وارد کنید.',
    badge: { text: 'الزامی', class: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' },
    details: [
      'از منوی بالا، روی گزینه «گزارش» و سپس «جدید» کلیک کنید (<kbd class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">Ctrl+N</kbd>).',
      'نام گزارش، نام گیاه، فصل کشت، مرحله رشد و تاریخ را وارد کنید.',
      'سپس روی دکمه «ذخیره گزارش» کلیک کنید.',
    ],
    tips: [
      'برای هر دوره کشت یک گزارش جداگانه بسازید تا بتوانید نتایج را با هم مقایسه کنید.',
      'برای بازیابی گزارش‌های قبلی، از منوی «گزارش ← بازکردن» استفاده کنید (<kbd class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">Ctrl+O</kbd>).',
    ],
    warnings: [
      'بدون ایجاد گزارش، امکان استفاده از سایر بخش‌های سامانه وجود ندارد.',
    ],
  },
  {
    id: 'target-elements',
    title: 'تعیین عناصر هدف (رسپی)',
    description: 'مقادیر مورد نیاز گیاه خود را برای ۱۵ عنصر غذایی تعیین کنید یا از رسپی‌های آماده استفاده کنید.',
    badge: { text: 'الزامی', class: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' },
    details: [
      'به تب «عناصر هدف» بروید.',
      'می‌توانید مقادیر را به صورت دستی وارد کنید (واحد پیش‌فرض: <code class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">ppm</code>).',
      'یا از بخش «رسپی‌های آماده» (بیش از ۲۵ رسپی برای گوجه، خیار، فلفل، کاهو و...) استفاده کنید.',
      'واحد مورد نظر خود را از بین PPM، MEQ و MMOL انتخاب کنید.',
      'تعادل کاتیون/آنیون به صورت خودکار محاسبه می‌شود.',
    ],
    tips: [
      'برای صرفه‌جویی در زمان، ابتدا از یک رسپی آماده شروع کنید و سپس آن را ویرایش کنید.',
      'تغییرات شما به صورت خودکار در گزارش ذخیره می‌شوند.',
    ],
    warnings: [
      'اختلاف کاتیون و آنیون باید کمتر از <code class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">0.5 meq/L</code> باشد.',
    ],
  },
  {
    id: 'water-analysis',
    title: 'ثبت آنالیز آب و پساب',
    description: 'اطلاعات شیمیایی آب و پساب خود را وارد کنید تا در محاسبات لحاظ شود.',
    badge: { text: 'اختیاری (توصیه‌شده)', class: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' },
    details: [
      'به تب «آنالیز آب» بروید.',
      'درصد آب تازه و پساب را وارد کنید (مجموع باید ۱۰۰٪ باشد).',
      'شوری آب (EC) را وارد کنید و واحد آن را انتخاب کنید.',
      'مقادیر هر عنصر را برای آب تازه و پساب به صورت جداگانه وارد کنید.',
      'ستون «مقادیر تأمینی» به صورت خودکار محاسبه می‌شود.',
    ],
    tips: [
      'هرچه دقت ورودی‌های آنالیز آب بیشتر باشد، محاسبات دقیق‌تر خواهند بود.',
      'می‌توانید آنالیز آب را برای استفاده‌های بعدی به عنوان «قالب» ذخیره کنید.',
    ],
    warnings: [
      'در صورت نداشتن آنالیز آب، این مرحله را می‌توانید نادیده بگیرید، اما دقت محاسبه کاهش می‌یابد.',
    ],
  },
  {
    id: 'fertilizer-db',
    title: 'مدیریت پایگاه داده کودها',
    description: 'کودهای مورد نیاز خود را از پایگاه داده سیستم انتخاب یا کوپ کنید، یا کودهای شخصی جدید بسازید.',
    badge: { text: 'الزامی', class: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' },
    details: [
      'به تب «پایگاه داده کودها» بروید.',
      'بیش از <strong>۴۲ کود استاندارد ایرانی</strong> به صورت آماده در دسترس شماست.',
      'با کلیک روی «کوپ همه»، همه کودهای سیستمی به بخش شخصی شما منتقل می‌شوند.',
      'برای افزودن کود شخصی، روی «افزودن کود جدید» کلیک کنید.',
      'می‌توانید درصد خلوص، قیمت، فرم فیزیکی و سایر مشخصات را ویرایش کنید.',
    ],
    tips: [
      'کودهای سیستم را نمی‌توانید ویرایش یا حذف کنید؛ ابتدا کوپ کنید و سپس ویرایش.',
      'برای صرفه‌جویی در زمان، ابتدا کودهای پرکاربرد خود را به بخش شخصی اضافه کنید.',
    ],
    warnings: [
      'مجموع درصد عناصر یک کود باید حداکثر ۱۰۰٪ باشد.',
    ],
  },
  {
    id: 'optimize',
    title: 'بهینه‌سازی خودکار فرمول کودی',
    description: 'با یک کلیک، بهترین ترکیب ممکن از کودهای انتخابی خود را پیدا کنید.',
    badge: { text: 'هسته اصلی', class: 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400' },
    details: [
      'به تب «محاسبه خودکار مقدار کود» بروید.',
      'شماره گام‌ها را در نوار بالای صفحه مشاهده می‌کنید: تنظیمات مخزن، انتخاب کود، نتیجه.',
      'در گام اول، حجم مخزن اصلی، حجم استوک و نسبت تزریق را تنظیم کنید.',
      'در گام دوم، کودهای مورد نظر خود را از لیست انتخاب کنید (با کشیدن و رها کردن یا کلیک).',
      'حالت بهینه‌سازی خود را انتخاب کنید: دقیق‌ترین، کم‌تعدادترین یا ارزان‌ترین.',
      'روی دکمه «محاسبه» کلیک کنید تا الگوریتم NNLS بهترین ترکیب را پیدا کند.',
    ],
    tips: [
      'الگوریتم NNLS تضمین می‌کند هیچ وزن منفی برای کودها محاسبه نشود.',
      'می‌توانید پس از محاسبه، وزن هر کود را به صورت دستی ویرایش کنید.',
      'گزینه «تعادل یونی خودکار» را می‌توانید فعال کنید تا یون‌های پادبار به ترکیب اضافه شوند.',
    ],
    warnings: [
      'انتخاب کودهای ناسازگار (مثل کلسیم و سولفات در یک مخزن) باعث هشدار سیستم می‌شود.',
    ],
  },
  {
    id: 'ph-tool',
    title: 'استفاده از ابزارک محاسبه pH',
    description: 'مقدار دقیق اسید یا باز مورد نیاز برای تنظیم pH آب را محاسبه کنید.',
    badge: { text: 'اختیاری', class: 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400' },
    details: [
      'به تب «ابزارک‌ها» بروید و «ماشین حساب pH» را انتخاب کنید.',
      'دو روش محاسبه در اختیار شماست: <strong>مدل تئوری</strong> (سریع، برای آب ساده) و <strong>تیتراسیون واقعی</strong> (دقیق‌تر، برای محلول‌های ترکیبی).',
      'pH فعلی، pH هدف، دما، حجم و ماده شیمیایی را وارد کنید.',
      'روی «محاسبه دوز» کلیک کنید.',
      'نتیجه شامل مقدار اسید/باز مورد نیاز، برنامه تزریق مرحله‌ای و هشدارهای ایمنی است.',
    ],
    tips: [
      'برای آب ساده معمولاً مدل تئوری کافی است.',
      'برای محلول‌های غذایی ترکیبی، استفاده از روش تیتراسیون دقیق‌تر است.',
    ],
    warnings: [
      'همیشه از تجهیزات ایمنی مناسب استفاده کنید.',
      'اسید را به آب اضافه کنید، نه آب را به اسید.',
    ],
  },
  {
    id: 'reports',
    title: 'مشاهده، ذخیره و چاپ گزارش',
    description: 'نتایج خود را ذخیره کنید، بعداً بازیابی کنید و یا به صورت PDF چاپ بگیرید.',
    badge: { text: 'نهایی', class: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400' },
    details: [
      'پس از انجام محاسبه، در گام سوم (نتیجه) تمام اطلاعات فرمول نهایی را می‌بینید.',
      'روی دکمه «خروجی PDF» کلیک کنید تا گزارش حرفه‌ای چاپ شود.',
      'برای ذخیره، از منوی «گزارش ← ذخیره» استفاده کنید (<kbd class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">Ctrl+S</kbd>).',
      'برای بازیابی یک گزارش قبلی، از «گزارش ← بازکردن» استفاده کنید.',
    ],
    tips: [
      'گزارش‌های ذخیره‌شده شامل تمام محاسبات، فرمول نهایی، نمودارها و هشدارها هستند.',
      'می‌توانید تا ۲۵۰ گزارش در حساب کاربری خود ذخیره کنید.',
    ],
    warnings: [],
  },
];

// ============================================================
// State
// ============================================================
const openSteps = ref<Record<string, boolean>>({});
const visitedSteps = ref<Set<string>>(new Set());

const toggleStep = (id: string) => {
  openSteps.value[id] = !openSteps.value[id];
  if (openSteps.value[id]) {
    visitedSteps.value.add(id);
  }
};

const isStepCompleted = (id: string) => visitedSteps.value.has(id);

const visitedCount = computed(() => visitedSteps.value.size);
const progressPercent = computed(() => Math.round((visitedCount.value / steps.length) * 100));

const getStepCircleClass = (step: Step, index: number): string => {
  if (isStepCompleted(step.id)) {
    return 'bg-emerald-500 text-white';
  }
  if (index === 0 && visitedCount.value === 0) {
    return 'bg-primary-600 text-white ring-4 ring-primary-100 dark:ring-primary-900/40';
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400';
};

const resetProgress = () => {
  openSteps.value = {};
  visitedSteps.value = new Set();
};
</script>

<style scoped>
kbd {
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  padding: 0.1rem 0.35rem;
  border-radius: 0.25rem;
  border: 1px solid #d1d5db;
}
.dark kbd {
  border-color: #4b5563;
}
code {
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  padding: 0.05rem 0.3rem;
  border-radius: 0.25rem;
}
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>