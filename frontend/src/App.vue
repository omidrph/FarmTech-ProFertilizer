<template>
  <div id="app" class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAppStore } from '@/store/modules/appStore';

const appStore = useAppStore();

onMounted(() => {
  // Load theme from localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark');
    appStore.setTheme('dark');
  }

  // Set RTL direction
  document.documentElement.dir = 'rtl';
  document.documentElement.lang = 'fa';
});
</script>

<style>
@import '@/assets/styles/main.css';

/* Reset & Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Vazirmatn', 'Samim', 'Sahel', 'Iranian Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Scrollbar Customization */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark ::-webkit-scrollbar-track {
  background: #1a1a2e;
}

.dark ::-webkit-scrollbar-thumb {
  background: #333355;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #444466;
}
</style>