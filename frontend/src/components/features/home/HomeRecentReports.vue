<!-- frontend/src/components/features/home/HomeRecentReports.vue -->
<!-- حالت ۱ صفحه خانه: هنوز گزارشی باز نیست؛ تا سه گزارش اخیر را نشان می‌دهد -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex items-center justify-between gap-3 mb-3">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">گزارش‌های اخیر</h3>
      <span v-if="reports.length" class="text-xs text-gray-400 dark:text-gray-500">
        {{ reports.length.toLocaleString('fa-IR') }} مورد
      </span>
    </div>

    <div v-if="reports.length" class="space-y-1.5">
      <button
        v-for="r in reports"
        :key="r.id"
        type="button"
        @click="emit('open', r.id)"
        class="w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-primary-50/40 dark:hover:bg-primary-900/10 transition-colors text-right"
      >
        <span class="min-w-0">
          <span class="block text-sm font-medium text-gray-800 dark:text-gray-100 truncate">{{ r.report_name || 'بدون نام' }}</span>
          <span class="block text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">
            {{ [r.plant_name, r.season, r.growth_stage].filter(Boolean).join(' • ') || 'بدون مشخصات' }}
          </span>
        </span>
        <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
    </div>

    <p v-else class="py-4 text-center text-sm text-gray-500 dark:text-gray-400">
      هنوز گزارشی ذخیره نشده است.
    </p>
  </section>
</template>

<script setup lang="ts">
import type { ReportListItem } from '@/store/modules/reportStore';

defineProps<{
  reports: ReportListItem[];
}>();

const emit = defineEmits<{
  (e: 'open', id: number): void;
}>();
</script>
