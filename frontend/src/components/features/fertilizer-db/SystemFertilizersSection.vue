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
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ systemFertilizers.length }} کود استاندارد آماده برای کپی
            <span v-if="copyStatus.copiedCount > 0" class="text-success-600 dark:text-success-400">
              ({{ copyStatus.copiedCount }} مورد کپی شده)
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
        {{ isCopying ? 'در حال کپی...' : 'کپی همه کودهای سیستمی' }}
      </button>
    </div>

    <!-- نمایش کودهای سیستمی (به صورت جمع‌شده) -->
    <div class="mt-4">
      <button
        @click="showSystemFertilizers = !showSystemFertilizers"
        class="text-sm text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center gap-1"
      >
        <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': showSystemFertilizers }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
        {{ showSystemFertilizers ? 'بستن لیست کودهای سیستمی' : 'مشاهده کودهای سیستمی' }}
      </button>

      <div v-if="showSystemFertilizers" class="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-60 overflow-y-auto custom-scrollbar">
        <div
          v-for="fert in systemFertilizers"
          :key="fert.id"
          class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600 flex items-center justify-between"
        >
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ fert.name }}</p>
            <div class="flex items-center gap-2 mt-0.5 flex-wrap">
              <span class="text-[10px] px-1.5 py-0.5 bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded">{{ fert.category || 'متفرقه' }}</span>
              <span class="text-[10px] px-1.5 py-0.5 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 rounded">{{ fert.form || 'جامد' }}</span>
            </div>
          </div>
          <button
            @click="$emit('copy-single', fert.id)"
            class="p-1.5 rounded-lg text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition-colors"
            title="کپی این کود"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
            </svg>
          </button>
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
</style>