<!-- frontend/src/components/features/calc/CSVExport.vue -->
<template>
  <div>
    <button
      @click="exportCSV"
      :disabled="!hasResult || isExporting"
      class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors duration-200"
    >
      <svg v-if="!isExporting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      {{ isExporting ? 'در حال ایجاد...' : 'خروجی CSV' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCSVExport } from '../../../composables/useCSVExport';

// ===== Props =====
interface Props {
  result: any | null;
  fertilizers: any[];
  targetValues: Record<string, number>;
  filename?: string;
}

const props = defineProps<Props>();

// ===== State =====
const isExporting = ref(false);

// ===== Computed =====
const hasResult = computed(() => props.result !== null);

// ===== Composables =====
const { exportOptimizationResult } = useCSVExport();

// ===== Methods =====
const exportCSV = async () => {
  if (!props.result) return;
  
  isExporting.value = true;
  try {
    const filename = props.filename || `بهینه‌سازی_کود_${new Date().toLocaleDateString('fa-IR').replace(/\//g, '-')}`;
    await exportOptimizationResult(
      props.result,
      props.fertilizers,
      props.targetValues,
      filename
    );
  } catch (error: any) {
    console.error('Error exporting CSV:', error);
    // emit error or show toast
  } finally {
    isExporting.value = false;
  }
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>