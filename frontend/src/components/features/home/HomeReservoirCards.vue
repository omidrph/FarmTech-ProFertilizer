<!-- frontend/src/components/features/home/HomeReservoirCards.vue -->
<template>
  <div class="card">
    <!-- هدر -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">
            توزیع مواد در مخازن
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            تقسیم‌بندی کودها بر اساس سازگاری شیمیایی
          </p>
        </div>
      </div>
      <!-- مجموع کل -->
      <div class="flex items-center gap-2 bg-gray-50 dark:bg-gray-700/30 px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
        </svg>
        <span class="text-xs text-gray-500 dark:text-gray-400">مجموع:</span>
        <span class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">
          {{ totalWeight.toFixed(2) }}
        </span>
        <span class="text-xs text-gray-400">گرم</span>
      </div>
    </div>

    <!-- کارت‌های مخازن -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
      <!-- مخزن A - آبی -->
      <div
        class="relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 p-3 sm:p-4 transition-all hover:shadow-lg group"
      >
        <div class="absolute top-0 right-0 w-24 h-24 rounded-full -mr-12 -mt-12 opacity-15 transition-opacity group-hover:opacity-25 bg-primary-100 dark:bg-primary-900/30"></div>
        <div class="absolute bottom-0 left-0 w-16 h-16 rounded-full -ml-8 -mb-8 opacity-10 bg-primary-100 dark:bg-primary-900/30"></div>
        
        <div class="relative">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2 min-w-0 flex-1">
              <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-primary-500 text-white flex items-center justify-center font-bold text-sm sm:text-lg shadow-md flex-shrink-0">
                A
              </div>
              <div class="min-w-0 flex-1">
                <h4 class="font-bold text-gray-900 dark:text-white text-xs sm:text-sm truncate">مخزن کلسیم</h4>
                <p class="text-[10px] sm:text-xs text-gray-500 dark:text-gray-400 truncate">کودهای کلسیمی</p>
              </div>
            </div>
            <span class="px-2 py-0.5 sm:px-2.5 sm:py-1 bg-primary-500 text-white rounded-lg text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0">
              {{ getReservoirTotal('A').toFixed(1) }}g
            </span>
          </div>
          
          <div v-if="reservoirData.A && reservoirData.A.length > 0" class="space-y-1.5 max-h-[200px] sm:max-h-[240px] overflow-y-auto thin-scrollbar">
            <div
              v-for="(item, idx) in reservoirData.A"
              :key="idx"
              class="flex items-center justify-between bg-white/70 dark:bg-gray-700/50 rounded-lg px-2.5 py-1.5 sm:px-3 sm:py-2 border border-gray-200 dark:border-gray-600 transition-all hover:bg-white dark:hover:bg-gray-700"
            >
              <span 
                class="text-[11px] sm:text-xs font-medium text-gray-700 dark:text-gray-300 flex-1 min-w-0 ml-2 truncate"
                :title="item.name"
              >
                {{ item.name }}
              </span>
              <span class="text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0 text-primary-600 dark:text-primary-400">
                {{ item.amount?.toFixed(2) || '0.00' }}g
              </span>
            </div>
          </div>
          <div v-else class="text-center py-6 sm:py-8">
            <svg class="w-8 h-8 sm:w-10 sm:h-10 mx-auto mb-1 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            <p class="text-[10px] sm:text-xs text-gray-400 dark:text-gray-500">خالی</p>
          </div>
        </div>
      </div>

      <!-- مخزن B - سبز -->
      <div
        class="relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 p-3 sm:p-4 transition-all hover:shadow-lg group"
      >
        <div class="absolute top-0 right-0 w-24 h-24 rounded-full -mr-12 -mt-12 opacity-15 transition-opacity group-hover:opacity-25 bg-success-100 dark:bg-success-900/30"></div>
        <div class="absolute bottom-0 left-0 w-16 h-16 rounded-full -ml-8 -mb-8 opacity-10 bg-success-100 dark:bg-success-900/30"></div>
        
        <div class="relative">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2 min-w-0 flex-1">
              <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-success-500 text-white flex items-center justify-center font-bold text-sm sm:text-lg shadow-md flex-shrink-0">
                B
              </div>
              <div class="min-w-0 flex-1">
                <h4 class="font-bold text-gray-900 dark:text-white text-xs sm:text-sm truncate">مخزن اصلی</h4>
                <p class="text-[10px] sm:text-xs text-gray-500 dark:text-gray-400 truncate">سایر کودها</p>
              </div>
            </div>
            <span class="px-2 py-0.5 sm:px-2.5 sm:py-1 bg-success-500 text-white rounded-lg text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0">
              {{ getReservoirTotal('B').toFixed(1) }}g
            </span>
          </div>
          
          <div v-if="reservoirData.B && reservoirData.B.length > 0" class="space-y-1.5 max-h-[200px] sm:max-h-[240px] overflow-y-auto thin-scrollbar">
            <div
              v-for="(item, idx) in reservoirData.B"
              :key="idx"
              class="flex items-center justify-between bg-white/70 dark:bg-gray-700/50 rounded-lg px-2.5 py-1.5 sm:px-3 sm:py-2 border border-gray-200 dark:border-gray-600 transition-all hover:bg-white dark:hover:bg-gray-700"
            >
              <span 
                class="text-[11px] sm:text-xs font-medium text-gray-700 dark:text-gray-300 flex-1 min-w-0 ml-2 truncate"
                :title="item.name"
              >
                {{ item.name }}
              </span>
              <span class="text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0 text-success-600 dark:text-success-400">
                {{ item.amount?.toFixed(2) || '0.00' }}g
              </span>
            </div>
          </div>
          <div v-else class="text-center py-6 sm:py-8">
            <svg class="w-8 h-8 sm:w-10 sm:h-10 mx-auto mb-1 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            <p class="text-[10px] sm:text-xs text-gray-400 dark:text-gray-500">خالی</p>
          </div>
        </div>
      </div>

      <!-- مخزن C - زرد -->
      <div
        class="relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 p-3 sm:p-4 transition-all hover:shadow-lg group"
      >
        <div class="absolute top-0 right-0 w-24 h-24 rounded-full -mr-12 -mt-12 opacity-15 transition-opacity group-hover:opacity-25 bg-warning-100 dark:bg-warning-900/30"></div>
        <div class="absolute bottom-0 left-0 w-16 h-16 rounded-full -ml-8 -mb-8 opacity-10 bg-warning-100 dark:bg-warning-900/30"></div>
        
        <div class="relative">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2 min-w-0 flex-1">
              <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-warning-500 text-white flex items-center justify-center font-bold text-sm sm:text-lg shadow-md flex-shrink-0">
                C
              </div>
              <div class="min-w-0 flex-1">
                <h4 class="font-bold text-gray-900 dark:text-white text-xs sm:text-sm truncate">مخزن اسید</h4>
                <p class="text-[10px] sm:text-xs text-gray-500 dark:text-gray-400 truncate">تنظیم pH</p>
              </div>
            </div>
            <span class="px-2 py-0.5 sm:px-2.5 sm:py-1 bg-warning-500 text-white rounded-lg text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0">
              {{ getReservoirTotal('C').toFixed(1) }}g
            </span>
          </div>
          
          <div v-if="reservoirData.C && reservoirData.C.length > 0" class="space-y-1.5 max-h-[200px] sm:max-h-[240px] overflow-y-auto thin-scrollbar">
            <div
              v-for="(item, idx) in reservoirData.C"
              :key="idx"
              class="flex items-center justify-between bg-white/70 dark:bg-gray-700/50 rounded-lg px-2.5 py-1.5 sm:px-3 sm:py-2 border border-gray-200 dark:border-gray-600 transition-all hover:bg-white dark:hover:bg-gray-700"
            >
              <span 
                class="text-[11px] sm:text-xs font-medium text-gray-700 dark:text-gray-300 flex-1 min-w-0 ml-2 truncate"
                :title="item.name"
              >
                {{ item.name }}
              </span>
              <span class="text-[10px] sm:text-xs font-bold tabular-nums flex-shrink-0 text-warning-600 dark:text-warning-400">
                {{ item.amount?.toFixed(2) || '0.00' }}g
              </span>
            </div>
          </div>
          <div v-else class="text-center py-6 sm:py-8">
            <svg class="w-8 h-8 sm:w-10 sm:h-10 mx-auto mb-1 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            <p class="text-[10px] sm:text-xs text-gray-400 dark:text-gray-500">خالی</p>
          </div>
        </div>
      </div>
    </div>

    <!-- فوتر -->
    <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex flex-wrap items-center gap-3 text-[10px] sm:text-xs text-gray-500 dark:text-gray-400">
          <span class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-primary-500"></span>
            <span>مخزن A</span>
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-success-500"></span>
            <span>مخزن B</span>
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-warning-500"></span>
            <span>مخزن C</span>
          </span>
        </div>
        <div class="flex items-center gap-1.5 text-[10px] text-gray-400 dark:text-gray-500">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span>تقسیم بر اساس سازگاری شیمیایی</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ============================================================
// Types
// ============================================================
interface ReservoirItem {
  name: string;
  amount: number;
}

interface Props {
  reservoirData: {
    A: ReservoirItem[];
    B: ReservoirItem[];
    C: ReservoirItem[];
  };
  totalWeight: number;
}

const props = defineProps<Props>();

// ============================================================
// Helper Functions
// ============================================================
const getReservoirTotal = (key: 'A' | 'B' | 'C'): number => {
  const data = props.reservoirData?.[key] || [];
  return data.reduce((sum: number, item: any) => sum + (item.amount || 0), 0);
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* اسکرول بار نازک */
.thin-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}

.thin-scrollbar::-webkit-scrollbar {
  width: 3px;
  height: 3px;
}

.thin-scrollbar::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 10px;
}

.thin-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
  transition: background 0.2s;
}

.thin-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.dark .thin-scrollbar {
  scrollbar-color: #4b5563 transparent;
}

.dark .thin-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .thin-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.group:hover .absolute {
  transition: opacity 0.3s ease;
}

@media (max-width: 640px) {
  .card {
    padding: 0.75rem;
  }
}

[title] {
  position: relative;
}
</style>