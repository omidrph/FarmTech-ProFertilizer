<!-- frontend/src/components/features/home/HomeRecentReports.vue -->
<!--
  نمایش سه گزارش اخیر (وقتی گزارشی باز نیست)
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <header class="px-4 sm:px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </span>
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">گزارش‌های اخیر</h3>
      </div>
      <span v-if="reports.length" class="text-[11px] text-gray-400 dark:text-gray-500 tabular-nums">
        {{ reports.length.toLocaleString('fa-IR') }} مورد
      </span>
    </header>

    <div class="p-3 sm:p-4">
      <div v-if="reports.length" class="space-y-2">
        <button
          v-for="r in reports"
          :key="r.id"
          type="button"
          @click="emit('open', r.id)"
          class="w-full flex items-center justify-between gap-3 px-3.5 py-3 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-primary-50/40 dark:hover:bg-primary-950/20 transition-colors text-right group"
        >
          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-gray-800 dark:text-gray-100 truncate">
              {{ r.report_name || 'بدون نام' }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">
              {{ [r.plant_name, r.season, r.growth_stage].filter(Boolean).join(' • ') || 'بدون مشخصات' }}
            </p>
          </div>
          <span class="flex-shrink-0 w-7 h-7 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 flex items-center justify-center group-hover:bg-primary-100 dark:group-hover:bg-primary-900/40 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </span>
        </button>
      </div>

      <div v-else class="py-8 text-center">
        <div class="w-14 h-14 mx-auto mb-3 rounded-full bg-gray-100 dark:bg-gray-700/60 flex items-center justify-center">
          <svg class="w-6 h-6 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400">هنوز گزارشی ذخیره نشده است</p>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">برای شروع، یک گزارش جدید ایجاد کنید</p>
      </div>
    </div>
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