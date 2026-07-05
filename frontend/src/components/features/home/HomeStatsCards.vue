<!-- frontend/src/components/features/home/HomeStatsCards.vue -->
<template>
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
    <!-- کارت 1: تعادل یونی -->
    <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4" :class="ionBalanceStatus.borderClass">
      <div class="flex items-start justify-between mb-2">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center transition-colors" :class="ionBalanceStatus.bgClass">
          <svg class="w-5 h-5 sm:w-6 sm:h-6" :class="ionBalanceStatus.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <span class="px-2 py-0.5 rounded-full text-xs font-semibold" :class="ionBalanceStatus.badgeClass">
          {{ ionBalance.isBalanced ? 'متعادل' : 'نامتعادل' }}
        </span>
      </div>
      <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1 font-medium">تعادل یونی</h3>
      <div class="flex items-end gap-1">
        <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {{ ionBalance.cation.toFixed(2) }}
        </span>
        <span class="text-xs text-gray-400 mb-1">/</span>
        <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {{ ionBalance.anion.toFixed(2) }}
        </span>
      </div>
      <div class="flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-0.5">
        <span class="text-[10px] text-gray-400">کاتیون / آنیون (meq/L)</span>
        <span v-if="!ionBalance.isBalanced" class="text-[10px] px-1.5 py-0.5 bg-danger-50 dark:bg-danger-900/20 text-danger-600 dark:text-danger-400 rounded-full font-medium">
          اختلاف: {{ difference.toFixed(2) }} meq/L
        </span>
      </div>
    </div>

    <!-- کارت 2: عناصر فعال -->
    <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-primary-500">
      <div class="flex items-start justify-between mb-2">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400">
          {{ activeElementsCount }}/15
        </span>
      </div>
      <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1 font-medium">عناصر فعال</h3>
      <div class="flex items-baseline gap-2">
        <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {{ activeElementsCount }}
        </span>
        <span class="text-xs text-gray-400">عنصر</span>
      </div>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">دارای مقدار هدف</p>
    </div>

    <!-- کارت 3: مخازن فعال -->
    <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-success-500">
      <div class="flex items-start justify-between mb-2">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
        </div>
        <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-success-50 dark:bg-success-900/30 text-success-700 dark:text-success-400">
          {{ activeReservoirsCount }}/3
        </span>
      </div>
      <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1 font-medium">مخازن فعال</h3>
      <div class="flex items-baseline gap-2">
        <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {{ activeReservoirsCount }}
        </span>
        <span class="text-xs text-gray-400">مخزن</span>
      </div>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">A, B, C</p>
    </div>

    <!-- کارت 4: هزینه کل -->
    <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-warning-500">
      <div class="flex items-start justify-between mb-2">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-warning-50 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400">
          تومان
        </span>
      </div>
      <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1 font-medium">هزینه کل</h3>
      <div class="flex items-baseline gap-2">
        <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
          {{ formattedCost }}
        </span>
      </div>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">مجموع هزینه کودها</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ============================================================
// Props
// ============================================================
interface Props {
  ionBalance: { cation: number; anion: number; isBalanced: boolean };
  ionBalanceStatus: {
    borderClass: string;
    bgClass: string;
    iconClass: string;
    badgeClass: string;
  };
  activeElementsCount: number;
  activeReservoirsCount: number;
  totalCost: number;
}

const props = defineProps<Props>();

// ============================================================
// Computed
// ============================================================
const difference = computed(() => {
  return Math.abs(props.ionBalance.cation - props.ionBalance.anion);
});

const formattedCost = computed(() => {
  // حذف اعشار و فرمت با جداکننده هزارتایی
  return Math.round(props.totalCost).toLocaleString('fa-IR');
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>