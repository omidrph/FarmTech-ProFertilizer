<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-3 sm:py-4 mt-auto">
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
        <!-- Copyright -->
        <div class="flex items-center gap-2 flex-wrap justify-center">
          <img src="/favicon.webp" alt="FarmTech" class="h-5 w-5 sm:h-6 sm:w-6 rounded object-contain" />
          <span>© ۱۴۰۵</span>
          <span class="font-medium text-primary-600 dark:text-primary-400">سیستم هوشمند نسخه‌نویسی کود</span>
          <span>|</span>
          <span>تمامی حقوق محفوظ است</span>
        </div>

        <!-- Version -->
        <div class="flex items-center gap-3">
          <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
            v{{ version }}
          </span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
interface Props {
  version?: string;
}

const props = withDefaults(defineProps<Props>(), {
  version: '0.1.0'
});
</script>