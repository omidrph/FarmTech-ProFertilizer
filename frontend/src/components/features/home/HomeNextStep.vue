<!-- frontend/src/components/features/home/HomeNextStep.vue -->
<!-- حالت ۲ صفحه خانه: گزارش باز است ولی هنوز محاسبه‌ای انجام نشده؛ فقط «گام بعدی» را نشان می‌دهد -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex items-center justify-between gap-3">
      <div class="min-w-0">
        <p class="text-xs text-gray-500 dark:text-gray-400">گام بعدی</p>
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white mt-0.5">{{ title }}</h3>
      </div>
      <button
        type="button"
        @click="emit('go')"
        class="flex-shrink-0 px-4 py-2 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors"
      >
        {{ actionLabel }}
      </button>
    </div>

    <ul class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex flex-wrap gap-x-5 gap-y-2">
      <li
        v-for="step in steps"
        :key="step.key"
        class="flex items-center gap-1.5 text-xs"
        :class="step.done ? 'text-emerald-600 dark:text-emerald-400' : 'text-gray-500 dark:text-gray-400'"
      >
        <span
          class="w-4 h-4 rounded-full flex items-center justify-center flex-shrink-0"
          :class="step.done ? 'bg-emerald-500 text-white' : 'border border-gray-300 dark:border-gray-600'"
        >
          <svg v-if="step.done" class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
        </span>
        {{ step.label }}
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  actionLabel: string;
  steps: Array<{ key: string; label: string; done: boolean }>;
}>();

const emit = defineEmits<{
  (e: 'go'): void;
}>();
</script>
