<!-- frontend/src/components/features/fertilizer-db/SystemFertilizersSection.vue -->
<template>
  <div class="bg-gradient-to-br from-indigo-50 to-white dark:from-indigo-900/20 dark:to-gray-800 rounded-xl shadow-sm border border-indigo-200 dark:border-indigo-800 p-5">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
          <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-bold text-gray-900 dark:text-white">کودهای سیستمی</h3>
          <p class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <span>{{ systemFertilizers.length }} کود استاندارد آماده</span>
            <span v-if="copyStatus.copiedCount > 0" class="text-success-600 dark:text-success-400">
              • {{ copyStatus.copiedCount }} مورد کپی شده
            </span>
          </p>
        </div>
      </div>
      
      <button
        @click="$emit('copy-all')"
        :disabled="isCopying || systemFertilizers.length === 0"
        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2 shadow-sm hover:shadow-md"
      >
        <svg v-if="!isCopying" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
        </svg>
        <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        {{ isCopying ? 'در حال کپی...' : 'کپی همه' }}
      </button>
    </div>

    <!-- نمایش کودهای سیستمی -->
    <div class="mt-4">
      <button
        @click="showSystemFertilizers = !showSystemFertilizers"
        class="text-sm text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center gap-1"
      >
        <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': showSystemFertilizers }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
        {{ showSystemFertilizers ? 'بستن لیست' : 'مشاهده لیست کودهای سیستمی' }}
      </button>

      <div v-if="showSystemFertilizers" class="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-60 overflow-y-auto custom-scrollbar">
        <div
          v-for="fert in systemFertilizers"
          :key="fert.id"
          class="relative group bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600 flex items-center justify-between hover:border-indigo-300 dark:hover:border-indigo-700 transition-all"
        >
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span 
                class="w-2 h-2 rounded-full flex-shrink-0"
                :class="fert.isAcid ? 'bg-warning-500' : 'bg-indigo-500'"
              ></span>
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ fert.name }}</p>
            </div>
            <div class="flex items-center gap-2 mt-0.5 flex-wrap">
              <span class="text-[10px] px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded">{{ fert.category || 'متفرقه' }}</span>
              <span 
                class="text-[10px] px-1.5 py-0.5 rounded"
                :class="getFormBadgeClass(fert)"
              >
                {{ getFormLabel(fert.form) }}
              </span>
            </div>
          </div>
          
          <!-- دکمه کپی -->
          <button
            @click="$emit('copy-single', fert.id)"
            class="p-1.5 rounded-lg text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition-colors"
            title="کپی این کود"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
            </svg>
          </button>

          <!-- ============================================================ -->
          <!-- Tooltip با عناصر کود - در هاور نمایش داده می‌شود -->
          <!-- ============================================================ -->
          <div 
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-50 w-64"
          >
            <div class="bg-gray-900 dark:bg-gray-800 text-white text-xs rounded-lg shadow-2xl p-3 border border-gray-700 dark:border-gray-600">
              <p class="font-semibold text-indigo-400 mb-2 text-center">عناصر تشکیل‌دهنده</p>
              
              <div v-if="hasElements(fert)" class="grid grid-cols-2 gap-x-3 gap-y-1">
                <div
                  v-for="(percentage, element) in getActiveElements(fert)"
                  :key="element"
                  class="flex justify-between items-center"
                >
                  <span class="font-medium" :class="getElementTextColor(element)">{{ element }}</span>
                  <span class="font-mono tabular-nums text-gray-300">{{ percentage }}%</span>
                </div>
              </div>
              
              <div v-else class="text-center text-gray-400 py-1">
                بدون عنصر
              </div>
              
              <!-- فلش tooltip -->
              <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                <div class="border-8 border-transparent border-t-gray-900 dark:border-t-gray-800"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// ============================================================
// Props
// ============================================================
defineProps<{
  systemFertilizers: any[];
  copyStatus: {
    hasSystemFertilizers: boolean;
    hasCopiedSystemFertilizers: boolean;
    systemCount: number;
    copiedCount: number;
  };
  isCopying: boolean;
}>();

// ============================================================
// Emits
// ============================================================
defineEmits<{
  (e: 'copy-all'): void;
  (e: 'copy-single', id: string): void;
}>();

// ============================================================
// State
// ============================================================
const showSystemFertilizers = ref(false);

// ============================================================
// Methods
// ============================================================
const getFormLabel = (form: string | undefined): string => {
  const labels: Record<string, string> = {
    liquid: 'مایع',
    powder: 'پودر',
    crystal: 'کریستال',
    granular: 'گرانول'
  };
  return form ? labels[form] || form : 'نامشخص';
};

const getFormBadgeClass = (fertilizer: any): string => {
  if (fertilizer.isAcid) {
    return 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400';
  }
  
  const classes: Record<string, string> = {
    liquid: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    powder: 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    crystal: 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-400',
    granular: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
  };
  return classes[fertilizer.form] || 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
};

const hasElements = (fertilizer: any): boolean => {
  if (!fertilizer.elements) return false;
  return Object.values(fertilizer.elements).some((v: any) => v && v > 0);
};

const getActiveElements = (fertilizer: any): Record<string, number> => {
  if (!fertilizer.elements) return {};
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(fertilizer.elements)) {
    if (value && (value as number) > 0) {
      result[key] = value as number;
    }
  }
  return result;
};

const getElementTextColor = (element: string): string => {
  const cationElements = ['N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Fe', 'Mn', 'Zn', 'Cu'];
  const anionElements = ['N-NO3', 'P', 'S', 'Cl', 'B', 'Mo'];
  
  if (cationElements.includes(element)) {
    return 'text-blue-400';
  } else if (anionElements.includes(element)) {
    return 'text-red-400';
  }
  return 'text-gray-400';
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>