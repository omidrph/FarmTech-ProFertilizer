<template>
  <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <img src="/Logo.webp" alt="FarmTech" class="h-10 w-auto" />
          <div>
            <h1 class="text-xl font-bold text-primary-600 dark:text-primary-400 leading-tight">
              تغذیه سبز
            </h1>
            <span class="text-xs text-gray-500 dark:text-gray-400">Green Nutrition</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-2">
          <!-- منوی فایل -->
          <div class="relative" @click.stop>
            <button 
              @click="fileMenuOpen = !fileMenuOpen"
              class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
              <span class="text-sm text-gray-700 dark:text-gray-300">فایل</span>
            </button>
            
            <div v-if="fileMenuOpen" class="absolute left-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
              <button @click="newReport" class="block w-full text-right px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                جدید
              </button>
              <button @click="openReport" class="block w-full text-right px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                بازکردن
              </button>
              <button @click="saveReport" class="block w-full text-right px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                ذخیره
              </button>
              <button @click="deleteReport" class="block w-full text-right px-4 py-2 text-sm text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors">
                حذف
              </button>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <button 
            v-for="tab in navTabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            :class="activeTab === tab.id ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20' : 'text-gray-600 dark:text-gray-400'"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            <span class="text-sm hidden sm:inline">{{ tab.label }}</span>
          </button>

          <!-- Theme Toggle -->
          <button 
            @click="toggleTheme"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg v-if="isDarkMode" class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const isDarkMode = ref(false);
const fileMenuOpen = ref(false);
const activeTab = defineModel<string>('activeTab', { default: 'home' });

const navTabs = [
  { id: 'home', label: 'صفحه اصلی', icon: 'HomeIcon' },
  { id: 'education', label: 'آموزش', icon: 'EducationIcon' },
  { id: 'contact', label: 'ارتباط با ما', icon: 'ContactIcon' },
  { id: 'about', label: 'درباره', icon: 'AboutIcon' }
];

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
};

const newReport = () => { /* ... */ fileMenuOpen.value = false; };
const openReport = () => { /* ... */ fileMenuOpen.value = false; };
const saveReport = () => { /* ... */ fileMenuOpen.value = false; };
const deleteReport = () => { /* ... */ fileMenuOpen.value = false; };

onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>