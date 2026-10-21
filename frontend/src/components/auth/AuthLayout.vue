<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-950 dark:via-gray-900 dark:to-primary-950 flex relative overflow-hidden">
    <button type="button" @click="toggleTheme"
      class="absolute top-4 left-4 z-50 p-2.5 rounded-xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm"
      :title="isDark ? 'حالت روشن' : 'حالت تاریک'">
      <svg v-if="isDark" class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
      <svg v-else class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>
    </button>

    <AuthShowcase />

    <div class="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-8 pb-32 lg:pb-8">
      <div class="w-full max-w-md">
        <div class="lg:hidden text-center mb-6">
          <div class="relative inline-block">
            <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-xl"></div>
            <img src="/Logo.webp" alt="سهند کود" class="relative h-20 w-20 object-contain" />
          </div>
        </div>

        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ title }}</h1>
          <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{{ subtitle }}</p>
        </div>

        <slot />

        <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <p class="text-xs text-center text-gray-500 dark:text-gray-400">© ۱۴۰۵ سهند کود — سیستم هوشمند نسخه‌نویسی کود</p>
        </div>
      </div>
    </div>

    <AppDownloadCard />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AuthShowcase from './AuthShowcase.vue';
import AppDownloadCard from './AppDownloadCard.vue';

defineProps<{ title: string; subtitle?: string }>();

const isDark = ref(false);
const toggleTheme = () => {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle('dark', isDark.value);
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
};
onMounted(() => {
  if (localStorage.getItem('theme') === 'dark') {
    isDark.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>