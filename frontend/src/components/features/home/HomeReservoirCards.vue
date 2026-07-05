<!-- frontend/src/components/features/home/HomeReservoirCards.vue -->
<template>
  <div class="card">
    <div class="flex items-center gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
      <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
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

    <!-- کارت‌های مخازن -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="(reservoir, key) in reservoirData"
        :key="key"
        class="relative overflow-hidden rounded-xl border-2 p-4 transition-all hover:shadow-lg"
        :class="getReservoirBorderClass(key)"
      >
        <div class="absolute top-0 right-0 w-20 h-20 rounded-full -mr-10 -mt-10 opacity-50" :class="getReservoirBgClass(key)"></div>
        <div class="relative">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-10 h-10 rounded-lg text-white flex items-center justify-center font-bold text-lg shadow-md" :class="getReservoirColorClass(key)">
                {{ key }}
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white text-sm">{{ getReservoirName(key) }}</h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ getReservoirDesc(key) }}</p>
              </div>
            </div>
            <span class="px-2 py-1 text-white rounded-lg text-xs font-bold tabular-nums" :class="getReservoirColorClass(key)">
              {{ getReservoirTotal(key).toFixed(2) }}g
            </span>
          </div>
          
          <div v-if="reservoir.length > 0" class="space-y-2 max-h-[200px] overflow-y-auto custom-scrollbar">
            <div
              v-for="(item, idx) in reservoir"
              :key="idx"
              class="flex items-center justify-between bg-white dark:bg-gray-700/50 rounded-lg px-3 py-2 border"
              :class="getReservoirItemBorderClass(key)"
            >
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 truncate max-w-[100px] sm:max-w-[120px]">
                {{ item.name }}
              </span>
              <span class="text-xs font-bold tabular-nums" :class="getReservoirItemTextClass(key)">
                {{ item.amount?.toFixed(3) || '0.000' }}g
              </span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-xs text-gray-400 dark:text-gray-500">
            <svg class="w-8 h-8 mx-auto mb-1 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            خالی
          </div>
        </div>
      </div>
    </div>

    <!-- جمع کل -->
    <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-4 text-sm">
          <div class="flex items-center gap-2">
            <span class="text-gray-500 dark:text-gray-400 font-medium">مجموع کل:</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">
              {{ totalWeight.toFixed(2) }} گرم
            </span>
          </div>
        </div>
        <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span>مخازن بر اساس سازگاری شیمیایی تقسیم شده‌اند</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ============================================================
// Props
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
const getReservoirColorClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'bg-primary-500',
    'B': 'bg-success-500',
    'C': 'bg-warning-500'
  };
  return classes[key] || 'bg-gray-500';
};

const getReservoirBorderClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'border-primary-200 dark:border-primary-800',
    'B': 'border-success-200 dark:border-success-800',
    'C': 'border-warning-200 dark:border-warning-800'
  };
  return classes[key] || 'border-gray-200 dark:border-gray-700';
};

const getReservoirBgClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'bg-primary-100 dark:bg-primary-900/30',
    'B': 'bg-success-100 dark:bg-success-900/30',
    'C': 'bg-warning-100 dark:bg-warning-900/30'
  };
  return classes[key] || 'bg-gray-100 dark:bg-gray-700/30';
};

const getReservoirName = (key: string): string => {
  const names: Record<string, string> = {
    'A': 'مخزن کلسیم',
    'B': 'مخزن اصلی',
    'C': 'مخزن اسید'
  };
  return names[key] || key;
};

const getReservoirDesc = (key: string): string => {
  const descs: Record<string, string> = {
    'A': 'کودهای کلسیمی',
    'B': 'سایر کودها',
    'C': 'تنظیم pH'
  };
  return descs[key] || '';
};

const getReservoirItemBorderClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'border-primary-100 dark:border-primary-900/50',
    'B': 'border-success-100 dark:border-success-900/50',
    'C': 'border-warning-100 dark:border-warning-900/50'
  };
  return classes[key] || 'border-gray-100 dark:border-gray-700';
};

const getReservoirItemTextClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'text-primary-600 dark:text-primary-400',
    'B': 'text-success-600 dark:text-success-400',
    'C': 'text-warning-600 dark:text-warning-400'
  };
  return classes[key] || 'text-gray-600 dark:text-gray-400';
};

const getReservoirTotal = (key: string): number => {
  const data = props.reservoirData?.[key as keyof typeof props.reservoirData] || [];
  return data.reduce((sum: number, item: any) => sum + (item.amount || 0), 0);
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
</style>