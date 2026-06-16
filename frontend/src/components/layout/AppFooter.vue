<template>
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-4 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
        <!-- Copyright -->
        <div class="flex items-center gap-2">
          <span>© ۱۴۰۵</span>
          <span class="font-medium text-primary-600 dark:text-primary-400">تغذیه سبز</span>
          <span>|</span>
          <span>تمامی حقوق محفوظ است</span>
        </div>

        <!-- Version & Links -->
        <div class="flex items-center gap-4">
          <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
            v{{ version }}
          </span>
          
          <button 
            v-for="link in footerLinks" 
            :key="link.id"
            @click="navigateTo(link.id)"
            class="hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          >
            {{ link.label }}
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// ===== Props =====
interface Props {
  version?: string;
}

const props = withDefaults(defineProps<Props>(), {
  version: '0.1.0'
});

// ===== Emits =====
const emit = defineEmits<{
  (e: 'navigate', tab: string): void;
}>();

// ===== Data =====
const footerLinks = ref([
  { id: 'home', label: 'خانه' },
  { id: 'about', label: 'درباره' },
  { id: 'contact', label: 'ارتباط با ما' },
  { id: 'education', label: 'آموزش' }
]);

// ===== Methods =====
const navigateTo = (tab: string) => {
  emit('navigate', tab);
};
</script>

<style scoped>
footer {
  box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.05);
}

.dark footer {
  box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.3);
}
</style>