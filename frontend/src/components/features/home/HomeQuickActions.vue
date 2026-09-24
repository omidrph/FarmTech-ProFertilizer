<!-- frontend/src/components/features/home/HomeQuickActions.vue -->
<!-- اقدام‌های سریع بعد از محاسبه -->
<template>
  <div class="flex flex-wrap items-center gap-2">
    <button
      type="button"
      @click="emit('recalculate')"
      class="flex-1 sm:flex-none inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      محاسبه مجدد
    </button>
    <button
      type="button"
      @click="emit('edit-targets')"
      class="flex-1 sm:flex-none inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke-width="2" /><circle cx="12" cy="12" r="6" stroke-width="2" /><circle cx="12" cy="12" r="2" stroke-width="2" />
      </svg>
      ویرایش عناصر هدف
    </button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'recalculate'): void;
  (e: 'edit-targets'): void;
}>();
</script>
