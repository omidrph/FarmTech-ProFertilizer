<!-- frontend/src/components/features/calc/StockSettings.vue -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5">

    <!-- عنوان -->
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
        </svg>
      </div>
      <div class="min-w-0">
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">تنظیمات استوک</h3>
        <p class="text-xs text-gray-500 dark:text-gray-400">محلول غلیظی که در مخزن استوک ساخته می‌شود</p>
      </div>
    </div>

    <!-- سه فیلد اصلی -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">

      <!-- ۱. نسبت تزریق -->
      <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-3 sm:p-0 sm:border-0">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-primary-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            نسبت تزریق دستگاه
          </span>
        </label>
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-500 dark:text-gray-400 flex-shrink-0">1 :</span>
          <input
            type="number"
            :value="injectionRatio"
            @input="updateInjectionRatio($event)"
            min="1"
            class="w-full min-w-0 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            placeholder="مثلاً ۱۰۰"
          />
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5">۱ لیتر استوک → {{ injectionRatio }} لیتر محلول نهایی</p>
      </div>

      <!-- ۲. حجم سطل استوک -->
      <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-3 sm:p-0 sm:border-0">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6l.5 4M9 3L7.5 15.5A2 2 0 009.48 18h5.04a2 2 0 001.98-2.5L15 7M9 3l-.5 4m6.5-4l.5 4M5.5 12h13"/>
            </svg>
            حجم سطل استوک
          </span>
        </label>
        <div class="flex items-center gap-2">
          <input
            type="number"
            :value="stockVolume"
            @input="updateStockVolume($event)"
            min="1"
            class="w-full min-w-0 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
          <span class="text-sm text-gray-500 dark:text-gray-400 flex-shrink-0">لیتر</span>
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5">سطل استوک معمولاً ۲۵ لیتری است</p>
      </div>

      <!-- ۳. حجم مخزن اصلی -->
      <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-3 sm:p-0 sm:border-0">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <ellipse cx="12" cy="5.5" rx="7" ry="2.5" stroke-width="2"/>
              <path stroke-linecap="round" stroke-width="2" d="M5 5.5v10c0 1.38 3.13 2.5 7 2.5s7-1.12 7-2.5v-10"/>
              <path stroke-linecap="round" stroke-width="2" d="M5 11.5c0 1.38 3.13 2.5 7 2.5s7-1.12 7-2.5"/>
            </svg>
            حجم مخزن اصلی
          </span>
        </label>
        <div class="flex items-center gap-2">
          <input
            type="number"
            :value="mainTankVolume"
            @input="updateMainTankVolume($event)"
            min="1"
            class="w-full min-w-0 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
          <span class="text-sm text-gray-500 dark:text-gray-400 flex-shrink-0">لیتر</span>
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5">مخزن اصلی معمولاً ۵۰۰۰ لیتری است</p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- اطلاعات مفید برای کاربر -->
    <!-- ============================================================ -->
    <div class="mt-4 p-3 bg-primary-50 dark:bg-primary-900/10 rounded-lg border border-primary-200 dark:border-primary-800">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3">

        <!-- تعداد سطل‌های استوک مورد نیاز -->
        <div class="flex items-center gap-2 bg-white/70 dark:bg-gray-800/40 rounded-lg p-2 sm:bg-transparent sm:dark:bg-transparent sm:p-0">
          <span class="w-8 h-8 rounded-lg bg-white dark:bg-gray-800 flex items-center justify-center flex-shrink-0 sm:bg-transparent sm:dark:bg-transparent">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
          </span>
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">تعداد سطل استوک</p>
            <p class="font-bold text-gray-900 dark:text-white tabular-nums">
              {{ Math.ceil(mainTankVolume / (stockVolume * injectionRatio)) || 0 }}
            </p>
          </div>
        </div>

        <!-- حجم کل استوک مورد نیاز -->
        <div class="flex items-center gap-2 bg-white/70 dark:bg-gray-800/40 rounded-lg p-2 sm:bg-transparent sm:dark:bg-transparent sm:p-0">
          <span class="w-8 h-8 rounded-lg bg-white dark:bg-gray-800 flex items-center justify-center flex-shrink-0 sm:bg-transparent sm:dark:bg-transparent">
            <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6l.5 4M9 3L7.5 15.5A2 2 0 009.48 18h5.04a2 2 0 001.98-2.5L15 7M9 3l-.5 4m6.5-4l.5 4M5.5 12h13"/>
            </svg>
          </span>
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">حجم کل استوک مورد نیاز</p>
            <p class="font-bold text-gray-900 dark:text-white tabular-nums">
              {{ (mainTankVolume / injectionRatio).toFixed(1) }} <span class="text-xs font-normal text-gray-500">لیتر</span>
            </p>
          </div>
        </div>

        <!-- نسبت تزریق -->
        <div class="flex items-center gap-2 bg-white/70 dark:bg-gray-800/40 rounded-lg p-2 sm:bg-transparent sm:dark:bg-transparent sm:p-0">
          <span class="w-8 h-8 rounded-lg bg-white dark:bg-gray-800 flex items-center justify-center flex-shrink-0 sm:bg-transparent sm:dark:bg-transparent">
            <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </span>
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">نسبت تزریق</p>
            <p class="font-bold text-gray-900 dark:text-white tabular-nums">
              1 : {{ injectionRatio }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Props =====
interface Props {
  mainTankVolume: number;
  stockVolume: number;
  injectionRatio: number;
}

const props = defineProps<Props>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:mainTankVolume', value: number): void;
  (e: 'update:stockVolume', value: number): void;
  (e: 'update:injectionRatio', value: number): void;
}>();

// ===== Methods =====
const updateMainTankVolume = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:mainTankVolume', parseFloat(target.value) || 0);
};

const updateStockVolume = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:stockVolume', parseFloat(target.value) || 0);
};

const updateInjectionRatio = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:injectionRatio', parseFloat(target.value) || 0);
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>
