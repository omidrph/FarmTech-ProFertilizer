<!-- frontend/src/components/features/calc/StockSettings.vue -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    
    <!-- عنوان -->
    <div class="flex items-center gap-2 mb-4">
      <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
        </svg>
      </div>
      <div>
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">تنظیمات استوک</h3>
        <p class="text-xs text-gray-500 dark:text-gray-400">محلول غلیظی که در مخزن استوک ساخته می‌شود</p>
      </div>
    </div>

    <!-- سه فیلد اصلی -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
      
      <!-- ۱. نسبت تزریق -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
            نسبت تزریق دستگاه
          </span>
        </label>
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-500 dark:text-gray-400">1 :</span>
          <input
            type="number"
            :value="injectionRatio"
            @input="updateInjectionRatio($event)"
            min="1"
            class="flex-1 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            placeholder="مثلاً ۱۰۰"
          />
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">۱ لیتر استوک → {{ injectionRatio }} لیتر محلول نهایی</p>
      </div>

      <!-- ۲. حجم سطل استوک -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
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
            class="flex-1 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
          <span class="text-sm text-gray-500 dark:text-gray-400 min-w-[40px]">لیتر</span>
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">سطل استوک معمولاً ۲۵ لیتری است</p>
      </div>

      <!-- ۳. حجم مخزن اصلی -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
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
            class="flex-1 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
          <span class="text-sm text-gray-500 dark:text-gray-400 min-w-[40px]">لیتر</span>
        </div>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">مخزن اصلی معمولاً ۵۰۰۰ لیتری است</p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- اطلاعات مفید برای کاربر -->
    <!-- ============================================================ -->
    <div class="mt-4 p-3 bg-primary-50 dark:bg-primary-900/10 rounded-lg border border-primary-200 dark:border-primary-800">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
        
        <!-- تعداد سطل‌های استوک مورد نیاز -->
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <div>
            <p class="text-xs text-gray-500 dark:text-gray-400">تعداد سطل استوک</p>
            <p class="font-bold text-gray-900 dark:text-white tabular-nums">
              {{ Math.ceil(mainTankVolume / (stockVolume * injectionRatio)) || 0 }}
            </p>
          </div>
        </div>

        <!-- حجم کل استوک مورد نیاز -->
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
          <div>
            <p class="text-xs text-gray-500 dark:text-gray-400">حجم کل استوک مورد نیاز</p>
            <p class="font-bold text-gray-900 dark:text-white tabular-nums">
              {{ (mainTankVolume / injectionRatio).toFixed(1) }} <span class="text-xs font-normal text-gray-500">لیتر</span>
            </p>
          </div>
        </div>

        <!-- نسبت تزریق -->
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
          <div>
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
import { computed } from 'vue';

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