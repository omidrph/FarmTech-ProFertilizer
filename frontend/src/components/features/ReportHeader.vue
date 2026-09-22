<!-- frontend/src/components/features/ReportHeader.vue -->
<template>
  <!-- ============================================================ -->
  <!-- حالت بزرگ: فقط وقتی هیچ گزارشی باز نیست (صفحه خانه) -->
  <!-- ============================================================ -->
  <div
    v-if="large"
    class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-5 sm:p-8"
  >
    <div class="flex items-center gap-2.5 mb-1.5">
      <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <div>
        <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">شروع یک گزارش جدید</h2>
        <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">اطلاعات زیر را وارد و از منوی «گزارش → ذخیره» ثبت کن</p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4 mt-5">
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">نام گزارش</label>
        <input type="text" :value="reportName" @input="updateReportName($event)" placeholder="نام گزارش..." class="field-input" />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">نام گیاه</label>
        <input type="text" :value="plantName" @input="updatePlantName($event)" placeholder="مثال: گوجه فرنگی" class="field-input" />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">فصل</label>
        <select :value="season" @change="updateSeason($event)" class="field-input">
          <option value="">انتخاب فصل...</option>
          <option value="بهار">🌱 بهار</option>
          <option value="تابستان">☀️ تابستان</option>
          <option value="پاییز">🍂 پاییز</option>
          <option value="زمستان">❄️ زمستان</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">مرحله رشد</label>
        <select :value="growthStage" @change="updateGrowthStage($event)" class="field-input">
          <option value="">انتخاب مرحله...</option>
          <option value="استقرار نشا">🌱 استقرار نشا</option>
          <option value="رشد رویشی">🌿 رشد رویشی</option>
          <option value="گلدهی">🌸 گلدهی</option>
          <option value="رسیدگی">🍎 رسیدگی</option>
          <option value="میوه‌دهی">🍅 میوه‌دهی</option>
          <option value="پایان دوره">🌾 پایان دوره</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">تاریخ</label>
        <input type="text" :value="reportDate" @input="updateReportDate($event)" placeholder="مثال: ۱۴۰۵/۰۳/۲۶" class="field-input" />
      </div>
    </div>

    <!-- آموزش اولیه، فقط همین‌جا -->
    <ol class="mt-6 pt-5 border-t border-gray-100 dark:border-gray-700 grid grid-cols-1 sm:grid-cols-3 gap-3">
      <li class="flex items-start gap-2.5">
        <span class="w-6 h-6 rounded-full bg-primary-600 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">۱</span>
        <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400">فیلدهای بالا را پر کن (حداقل نام گزارش)</p>
      </li>
      <li class="flex items-start gap-2.5">
        <span class="w-6 h-6 rounded-full bg-primary-600 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">۲</span>
        <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400">از منوی بالا «گزارش → ذخیره» را بزن</p>
      </li>
      <li class="flex items-start gap-2.5">
        <span class="w-6 h-6 rounded-full bg-primary-600 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">۳</span>
        <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400">بعد از ذخیره، آنالیز آب و عناصر هدف و محاسبه کود باز می‌شوند</p>
      </li>
    </ol>
  </div>

  <!-- ============================================================ -->
  <!-- حالت فشرده: در همه تب‌های دیگر و صفحه خانه بعد از ساخت گزارش -->
  <!-- ============================================================ -->
  <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    <button
      type="button"
      @click="expanded = !expanded"
      class="w-full flex items-center justify-between gap-2 px-3 py-2 text-right"
    >
      <span class="flex items-center gap-2 min-w-0">
        <svg class="w-4 h-4 text-primary-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span class="text-sm font-medium text-gray-800 dark:text-gray-100 truncate">{{ reportName || 'بدون نام' }}</span>
        <span v-if="plantName" class="text-xs text-gray-400 truncate hidden sm:inline">• {{ plantName }}</span>
      </span>
      <svg class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform" :class="expanded ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>

    <div v-show="expanded" class="px-3 pb-3 pt-1 border-t border-gray-100 dark:border-gray-700">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2">
        <div>
          <label class="block text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1">نام گزارش</label>
          <input type="text" :value="reportName" @input="updateReportName($event)" class="field-input-sm" />
        </div>
        <div>
          <label class="block text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1">نام گیاه</label>
          <input type="text" :value="plantName" @input="updatePlantName($event)" class="field-input-sm" />
        </div>
        <div>
          <label class="block text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1">فصل</label>
          <select :value="season" @change="updateSeason($event)" class="field-input-sm">
            <option value="">-</option>
            <option value="بهار">🌱 بهار</option>
            <option value="تابستان">☀️ تابستان</option>
            <option value="پاییز">🍂 پاییز</option>
            <option value="زمستان">❄️ زمستان</option>
          </select>
        </div>
        <div>
          <label class="block text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1">مرحله رشد</label>
          <select :value="growthStage" @change="updateGrowthStage($event)" class="field-input-sm">
            <option value="">-</option>
            <option value="استقرار نشا">🌱 استقرار نشا</option>
            <option value="رشد رویشی">🌿 رشد رویشی</option>
            <option value="گلدهی">🌸 گلدهی</option>
            <option value="رسیدگی">🍎 رسیدگی</option>
            <option value="میوه‌دهی">🍅 میوه‌دهی</option>
            <option value="پایان دوره">🌾 پایان دوره</option>
          </select>
        </div>
        <div>
          <label class="block text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1">تاریخ</label>
          <input type="text" :value="reportDate" @input="updateReportDate($event)" class="field-input-sm" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  reportDate: string;
  // 🆕 حالت بزرگ فقط در صفحه خانه و وقتی گزارشی باز نیست
  large?: boolean;
}

const props = withDefaults(defineProps<Props>(), { large: false });

const emit = defineEmits<{
  (e: 'update:reportName', value: string): void;
  (e: 'update:plantName', value: string): void;
  (e: 'update:season', value: string): void;
  (e: 'update:growthStage', value: string): void;
  (e: 'update:reportDate', value: string): void;
}>();

// 🆕 در حالت فشرده، پیش‌فرض بسته است تا فضای کمی بگیرد
const expanded = ref(false);

const updateReportName = (event: Event) => emit('update:reportName', (event.target as HTMLInputElement).value);
const updatePlantName = (event: Event) => emit('update:plantName', (event.target as HTMLInputElement).value);
const updateSeason = (event: Event) => emit('update:season', (event.target as HTMLSelectElement).value);
const updateGrowthStage = (event: Event) => emit('update:growthStage', (event.target as HTMLSelectElement).value);
const updateReportDate = (event: Event) => emit('update:reportDate', (event.target as HTMLInputElement).value);
</script>

<style scoped>
.field-input {
  @apply w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200;
}
.field-input-sm {
  @apply w-full px-2 py-1.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200;
}
select {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.6rem center;
  background-size: 0.9rem;
  padding-left: 2rem;
}
.dark select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}
</style>
