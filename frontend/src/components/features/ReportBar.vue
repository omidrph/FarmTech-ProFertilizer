<!-- frontend/src/components/features/ReportBar.vue -->
<!--
  نوار باریک اطلاعات گزارش برای همه‌ی تب‌ها به‌جز «خانه».
  فقط نمایش می‌دهد؛ ویرایش مشخصات فقط در تب خانه ممکن است.
-->
<template>
  <div class="flex items-center gap-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2">
    <svg class="w-4 h-4 text-primary-600 dark:text-primary-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
    </svg>

    <div class="min-w-0 flex-1 flex items-baseline gap-x-2 overflow-hidden">
      <span class="text-sm font-semibold text-gray-900 dark:text-white truncate flex-shrink-0 max-w-[45%]">
        {{ reportName || 'گزارش بدون نام' }}
      </span>
      <span v-if="meta" class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ meta }}</span>
    </div>

    <button
      type="button"
      @click="emit('edit')"
      class="flex-shrink-0 text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline"
    >
      ویرایش
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  reportDate: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'edit'): void;
}>();

const meta = computed(() =>
  [props.plantName, props.season, props.growthStage, props.reportDate].filter(Boolean).join(' • ')
);
</script>
