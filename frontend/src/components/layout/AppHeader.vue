<template>
  <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50 transition-colors duration-200">
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
      <div class="flex items-center justify-between h-16 sm:h-20 lg:h-24">
        <!-- Logo -->
        <div class="flex items-center gap-3 sm:gap-4 flex-shrink-0">
          <img 
            src="/Logo.webp" 
            alt="FarmTech" 
            class="h-10 w-10 sm:h-14 sm:w-14 lg:h-16 lg:w-16 object-contain rounded-lg"
          />
          <div class="flex flex-col leading-tight">
            <h1 class="text-sm sm:text-base lg:text-xl font-bold text-gray-800 dark:text-white tracking-tight">
              سیستم هوشمند نسخه‌نویسی کود
            </h1>
          </div>
        </div>

        <!-- Mobile Menu Toggle -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          aria-label="منو"
        >
          <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Desktop Actions -->
        <div class="hidden lg:flex items-center gap-1 lg:gap-2">
          <!-- File Menu -->
          <div class="relative" ref="fileMenuRef">
            <button 
              @click="toggleFileMenu"
              class="flex items-center gap-1 lg:gap-2 px-2 lg:px-3 py-1.5 lg:py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 transition-all duration-200 text-xs lg:text-sm"
            >
              <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span class="hidden sm:inline">فایل</span>
              <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            
            <div 
              v-if="fileMenuOpen" 
              class="absolute left-0 mt-2 w-48 sm:w-56 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 py-1 z-50 overflow-hidden"
            >
              <button 
                @click="newReport" 
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                جدید
              </button>
              <button 
                @click="openReport" 
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                بازکردن
              </button>
              <button 
                @click="saveReport" 
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
                </svg>
                ذخیره
              </button>
              <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>
              <button 
                @click="deleteReport" 
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                حذف
              </button>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <button 
            v-for="tab in navTabs" 
            :key="tab.id"
            @click="setActiveTab(tab.id)"
            class="flex items-center gap-1 lg:gap-2 px-2 lg:px-3 py-1.5 lg:py-2 rounded-lg transition-all duration-200 text-xs lg:text-sm"
            :class="currentActiveTab === tab.id 
              ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400' 
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
          >
            <span v-html="tab.icon"></span>
            <span class="hidden sm:inline">{{ tab.label }}</span>
          </button>

          <!-- Theme Toggle -->
          <button 
            @click="toggleTheme"
            class="p-1.5 lg:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-all duration-200"
          >
            <svg v-if="isDarkMode" class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div 
      v-if="mobileMenuOpen" 
      class="lg:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-2 px-3 shadow-lg"
    >
      <div class="flex flex-col gap-1">
        <!-- File Menu (Mobile) -->
        <button 
          @click="toggleFileMenuMobile"
          class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 transition-colors text-sm"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span>فایل</span>
          <svg class="w-4 h-4 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <div v-if="fileMenuOpenMobile" class="mr-6 space-y-1">
          <button @click="newReport" class="block w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            جدید
          </button>
          <button @click="openReport" class="block w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            بازکردن
          </button>
          <button @click="saveReport" class="block w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            ذخیره
          </button>
          <button @click="deleteReport" class="block w-full text-right px-3 py-2 text-sm text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors">
            حذف
          </button>
        </div>

        <!-- Navigation Buttons (Mobile) -->
        <button 
          v-for="tab in navTabs" 
          :key="tab.id"
          @click="setActiveTab(tab.id); mobileMenuOpen = false"
          class="flex items-center gap-2 px-3 py-2 rounded-lg transition-all duration-200 text-sm"
          :class="currentActiveTab === tab.id 
            ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400' 
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
        >
          <span v-html="tab.icon"></span>
          <span>{{ tab.label }}</span>
        </button>

        <!-- Theme Toggle (Mobile) -->
        <button 
          @click="toggleTheme"
          class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors text-sm"
        >
          <svg v-if="isDarkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
          <span>تغییر تم</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

// ===== Props =====
interface Props {
  activeTab?: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:activeTab', value: string): void;
}>();

// ===== State =====
const isDarkMode = ref(false);
const fileMenuOpen = ref(false);
const fileMenuOpenMobile = ref(false);
const mobileMenuOpen = ref(false);
const fileMenuRef = ref<HTMLElement | null>(null);

// ===== Computed =====
// استفاده از computed برای به‌روزرسانی خودکار وقتی props تغییر می‌کند
const currentActiveTab = computed(() => props.activeTab || 'home');

// ===== Navigation Tabs =====
const navTabs = [
  { 
    id: 'home', 
    label: 'صفحه اصلی', 
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
    </svg>`
  },
  { 
    id: 'education', 
    label: 'آموزش', 
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
    </svg>`
  },
  { 
    id: 'contact', 
    label: 'ارتباط با ما', 
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
    </svg>`
  },
  { 
    id: 'about', 
    label: 'درباره', 
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>`
  }
];

// ===== Methods =====
const setActiveTab = (tabId: string) => {
  emit('update:activeTab', tabId);
};

const toggleFileMenu = () => {
  fileMenuOpen.value = !fileMenuOpen.value;
  if (fileMenuOpen.value) {
    fileMenuOpenMobile.value = false;
  }
};

const toggleFileMenuMobile = () => {
  fileMenuOpenMobile.value = !fileMenuOpenMobile.value;
  if (fileMenuOpenMobile.value) {
    fileMenuOpen.value = false;
  }
};

const closeFileMenu = () => {
  fileMenuOpen.value = false;
  fileMenuOpenMobile.value = false;
};

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
};

const newReport = () => {
  closeFileMenu();
  alert('ایجاد گزارش جدید (در حال توسعه)');
};

const openReport = () => {
  closeFileMenu();
  alert('باز کردن گزارش (در حال توسعه)');
};

const saveReport = () => {
  closeFileMenu();
  alert('ذخیره گزارش (در حال توسعه)');
};

const deleteReport = () => {
  closeFileMenu();
  if (confirm('آیا از حذف گزارش اطمینان دارید؟')) {
    alert('گزارش حذف شد (در حال توسعه)');
  }
};

// ===== Click Outside Handler =====
const handleClickOutside = (event: MouseEvent) => {
  if (fileMenuRef.value && !fileMenuRef.value.contains(event.target as Node)) {
    fileMenuOpen.value = false;
  }
};

// ===== Lifecycle =====
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  }
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// ===== Watch for mobile menu close on resize =====
watch(mobileMenuOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});
</script>

<style scoped>
/* Mobile menu animation */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Dark mode overrides */
.dark .bg-white {
  background-color: #1a1a2e;
}

.dark .border-gray-200 {
  border-color: #333355;
}
</style>