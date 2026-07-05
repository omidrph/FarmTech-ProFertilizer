<!-- frontend/src/components/features/home/HomeElementsTable.vue -->
<template>
  <div class="card">
    <div class="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">
            مقایسه هدف و محلول نهایی
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            بررسی دقیق مقادیر هدف در برابر مقادیر تامین شده
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs text-gray-500 dark:text-gray-400">واحد:</span>
        <span class="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-lg text-xs font-semibold text-gray-700 dark:text-gray-300">
          {{ displayUnit }}
        </span>
      </div>
    </div>

    <!-- جدول -->
    <div class="overflow-x-auto -mx-4 sm:mx-0">
      <div class="inline-block min-w-full align-middle px-4 sm:px-0">
        <table class="min-w-full border-collapse">
          <thead>
            <tr>
              <th class="sticky left-0 z-10 bg-gray-50 dark:bg-gray-700 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                عنصر
              </th>
              <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                هدف
              </th>
              <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                تامین شده
              </th>
              <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[120px]">
                وضعیت خطا
              </th>
              <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                اختلاف
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="item in elementsData"
              :key="item.element"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
            >
              <td class="sticky left-0 z-10 bg-white dark:bg-gray-800 px-3 py-3 text-right">
                <div class="flex items-center gap-2">
                  <span
                    class="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold"
                    :class="getElementBadgeClass(item.element)"
                  >
                    {{ getElementSymbol(item.element) }}
                  </span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ item.element }}
                  </span>
                </div>
              </td>
              <td class="px-3 py-3 text-center">
                <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 tabular-nums">
                  {{ formatNumber(item.target) }}
                </span>
              </td>
              <td class="px-3 py-3 text-center">
                <span class="text-sm font-semibold tabular-nums" :class="getActualValueClass(item)">
                  {{ formatNumber(item.actual) }}
                </span>
              </td>
              <td class="px-3 py-3">
                <div class="flex items-center gap-2">
                  <div class="relative flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div class="absolute top-0 left-1/2 w-0.5 h-full bg-gray-400/50 dark:bg-gray-500/50 z-10"></div>
                    <div
                      v-if="getErrorPercent(item) < 0"
                      class="absolute top-0 h-full rounded-full transition-all duration-700 ease-out"
                      :class="getErrorBarClass(item)"
                      :style="getErrorBarStyle(item)"
                    ></div>
                    <div
                      v-else-if="getErrorPercent(item) > 0"
                      class="absolute top-0 h-full rounded-full transition-all duration-700 ease-out"
                      :class="getErrorBarClass(item)"
                      :style="getErrorBarStyle(item)"
                    ></div>
                    <div
                      v-else
                      class="absolute top-0 left-0 h-full w-full rounded-full transition-all duration-700 ease-out bg-success-500"
                    ></div>
                  </div>
                  <span class="text-xs font-semibold min-w-[45px] text-right tabular-nums" :class="getProgressTextClass(item)">
                    {{ getProgressDisplay(item) }}
                  </span>
                </div>
              </td>
              <td class="px-3 py-3 text-center">
                <!-- اگر هدف و تامین هر دو صفر باشند -->
                <span
                  v-if="item.target === 0 && item.actual === 0"
                  class="text-xs text-gray-400 dark:text-gray-500 tabular-nums"
                >
                  —
                </span>
                <!-- اگر اختلاف وجود داشته باشد -->
                <span
                  v-else-if="item.difference !== 0"
                  class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold tabular-nums"
                  :class="getDiffClass(item)"
                >
                  <svg v-if="item.difference > 0" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                  </svg>
                  <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                  {{ formatNumber(Math.abs(item.difference)) }}
                </span>
                <!-- اگر اختلاف صفر باشد -->
                <span
                  v-else
                  class="text-xs text-gray-400 dark:text-gray-500 tabular-nums"
                >
                  {{ formatNumber(0) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- راهنمای رنگ‌ها -->
    <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-wrap items-center gap-3 text-xs">
        <span class="text-gray-500 dark:text-gray-400 font-medium">راهنما:</span>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-success-500"></span>
          <span class="text-gray-600 dark:text-gray-400">خطا 0% (دقیق)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-emerald-400 dark:bg-emerald-600"></span>
          <span class="text-gray-600 dark:text-gray-400">کمبود جزئی (0-10%)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-amber-500"></span>
          <span class="text-gray-600 dark:text-gray-400">کمبود متوسط (10-20%)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-rose-500"></span>
          <span class="text-gray-600 dark:text-gray-400">کمبود شدید (&gt;20%)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-orange-500"></span>
          <span class="text-gray-600 dark:text-gray-400">بیشبود</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-gray-300 dark:bg-gray-600"></span>
          <span class="text-gray-600 dark:text-gray-400">بدون هدف</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ============================================================
// Props
// ============================================================
interface ElementItem {
  element: string;
  target: number;
  actual: number;
  difference: number;
  progressPercent: number;
}

interface Props {
  elementsData: ElementItem[];
  targetUnit?: string;
}

const props = withDefaults(defineProps<Props>(), {
  targetUnit: 'ppm'
});

// ============================================================
// Computed
// ============================================================
const displayUnit = computed(() => {
  return (props.targetUnit || 'ppm').toUpperCase();
});

// ============================================================
// Helper Functions - فرمت‌کننده یکدست اعداد
// ============================================================
const formatNumber = (value: number): string => {
  if (value === undefined || value === null || isNaN(value)) return '۰٫۰۰';
  return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',').replace(/\./g, '٫');
};

// ============================================================
// Helper Functions - عناصر
// ============================================================
const getElementSymbol = (element: string): string => {
  const symbols: Record<string, string> = {
    'N-NO3': 'N', 'P': 'P', 'S': 'S', 'N-NH4': 'N', 'K': 'K',
    'Ca': 'Ca', 'Mg': 'Mg', 'Na': 'Na', 'Cl': 'Cl', 'Fe': 'Fe',
    'Mn': 'Mn', 'Zn': 'Zn', 'B': 'B', 'Cu': 'Cu', 'Mo': 'Mo'
  };
  return symbols[element] || element.substring(0, 2);
};

const getElementBadgeClass = (element: string): string => {
  const macroElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg'];
  const microElements = ['Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];
  
  if (macroElements.includes(element)) {
    return 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400';
  } else if (microElements.includes(element)) {
    return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400';
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400';
};

// ============================================================
// Helper Functions - Progress Bar
// ============================================================
const getErrorPercent = (item: ElementItem): number => {
  if (item.target === 0) return 0;
  return (item.difference / item.target) * 100;
};

const getProgressDisplay = (item: ElementItem): string => {
  if (item.target === 0) return '—';
  const error = getErrorPercent(item);
  const absError = Math.abs(error);
  if (absError < 0.01) return '۰%';
  if (error > 0) return `+${absError.toFixed(1)}%`;
  return `${absError.toFixed(1)}%`;
};

const getErrorBarClass = (item: ElementItem): string => {
  if (item.target === 0) return 'bg-gray-300 dark:bg-gray-600';
  const error = getErrorPercent(item);
  const absError = Math.abs(error);
  
  if (absError < 0.01) return 'bg-success-500';
  if (error > 0) {
    if (absError <= 5) return 'bg-orange-400 dark:bg-orange-500';
    if (absError <= 10) return 'bg-orange-500 dark:bg-orange-600';
    if (absError <= 20) return 'bg-rose-500 dark:bg-rose-600';
    return 'bg-rose-600 dark:bg-rose-700';
  } else {
    if (absError <= 5) return 'bg-emerald-400 dark:bg-emerald-500';
    if (absError <= 10) return 'bg-emerald-500 dark:bg-emerald-600';
    if (absError <= 20) return 'bg-amber-500 dark:bg-amber-600';
    return 'bg-rose-500 dark:bg-rose-600';
  }
};

const getErrorBarStyle = (item: ElementItem): Record<string, string> => {
  if (item.target === 0) {
    return { width: '0%', left: '50%' };
  }
  
  const error = getErrorPercent(item);
  const absError = Math.min(Math.abs(error), 30);
  const percentage = (absError / 30) * 50;

  if (Math.abs(error) < 0.01) {
    return { width: '100%', left: '0%' };
  }

  if (error > 0) {
    return { 
      width: `${Math.min(percentage, 50)}%`, 
      left: '50%',
      borderRadius: '0 999px 999px 0'
    };
  } else {
    return { 
      width: `${Math.min(percentage, 50)}%`, 
      left: `${50 - Math.min(percentage, 50)}%`,
      borderRadius: '999px 0 0 999px'
    };
  }
};

const getProgressTextClass = (item: ElementItem): string => {
  if (item.target === 0) return 'text-gray-400 dark:text-gray-500';
  const error = getErrorPercent(item);
  const absError = Math.abs(error);
  
  if (absError < 0.01) return 'text-success-600 dark:text-success-400';
  if (error > 0) {
    if (absError <= 5) return 'text-orange-500 dark:text-orange-400';
    if (absError <= 10) return 'text-orange-600 dark:text-orange-500';
    if (absError <= 20) return 'text-rose-600 dark:text-rose-400';
    return 'text-rose-700 dark:text-rose-500';
  } else {
    if (absError <= 5) return 'text-emerald-600 dark:text-emerald-400';
    if (absError <= 10) return 'text-emerald-700 dark:text-emerald-500';
    if (absError <= 20) return 'text-amber-600 dark:text-amber-400';
    return 'text-rose-600 dark:text-rose-400';
  }
};

const getActualValueClass = (item: ElementItem): string => {
  if (item.target === 0) {
    if (item.actual === 0) return 'text-gray-400 dark:text-gray-500';
    return 'text-warning-600 dark:text-warning-400';
  }
  const error = getErrorPercent(item);
  const absError = Math.abs(error);
  
  if (absError < 0.01) return 'text-success-600 dark:text-success-400';
  if (absError <= 5) return 'text-emerald-600 dark:text-emerald-400';
  if (absError <= 10) return 'text-emerald-700 dark:text-emerald-500';
  if (absError <= 20) return 'text-amber-600 dark:text-amber-400';
  return 'text-rose-600 dark:text-rose-400';
};

const getDiffClass = (item: ElementItem): string => {
  if (item.target === 0) return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400';
  const error = getErrorPercent(item);
  const absError = Math.abs(error);
  
  if (absError < 0.01) return 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400';
  if (absError <= 5) return 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400';
  if (absError <= 10) return 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400';
  if (absError <= 20) return 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400';
  return 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400';
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>