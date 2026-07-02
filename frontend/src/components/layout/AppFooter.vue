<template>
  <!-- 
    تغییرات اصلی برای موبایل:
    - fixed bottom-0 left-0 right-0 z-50: چسبیدن به پایین صفحه
    - sm:relative: در دسکتاپ حالت عادی داشته باشد
    - shadow-[0_-4px_...]: سایه رو به بالا برای جدا شدن از محتوا
  -->
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-auto transition-colors duration-200 sm:py-3 relative sm:relative fixed bottom-0 left-0 right-0 z-50 sm:z-auto shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] sm:shadow-none">
    
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 w-full">
      
      <!-- کانتینر اصلی: در موبایل flex-row و justify-around، در دسکتاپ flex-col/sm:flex-row -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
        
        <!-- بخش 1: کپی‌رایت (فقط در دسکتاپ نمایش داده می‌شود) -->
        <div class="hidden sm:flex items-center gap-2 flex-wrap justify-center">
          <img src="/favicon.webp" alt="سهند کود" class="h-6 w-6 rounded object-contain" />
          <span>© ۱۴۰۵</span>
          <span class="font-medium text-primary-600 dark:text-primary-400">سهند کود</span>
          <span>| تمامی حقوق محفوظ است</span>
        </div>

        <!-- بخش 2: منوی ناوبری موبایل / اطلاعات کاربر دسکتاپ -->
        <!-- در موبایل: کل عرض را می‌گیرد و آیتم‌ها را پخش می‌کند (justify-between) -->
        <div class="flex items-center justify-between w-full sm:w-auto sm:justify-end sm:gap-3 py-2 sm:py-0">
          
          <!-- دکمه پروفایل (نمایش نام کامل در موبایل و دسکتاپ) -->
          <button
            @click="openProfileModal"
            class="flex flex-col sm:flex-row items-center gap-1 sm:gap-1.5 px-2 sm:px-2.5 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors group flex-1 sm:flex-none justify-center"
            title="پروفایل کاربری"
          >
            <div class="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400 font-bold text-xs group-hover:bg-primary-200 dark:group-hover:bg-primary-900/50 transition-colors">
              {{ userInitials }}
            </div>
            <!-- نمایش نام کامل در هر دو حالت -->
            <span class="text-[10px] sm:text-xs font-medium">{{ userDisplayName }}</span>
          </button>

          <!-- وضعیت اتصال (فقط در دسکتاپ نمایش داده می‌شود - حذف شده از موبایل) -->
          <div class="hidden sm:flex items-center gap-1.5 px-2 py-1 flex-shrink-0">
            <span
              class="inline-block w-2.5 h-2.5 rounded-full animate-pulse"
              :class="{
                'bg-green-500': connectionStatus === 'connected',
                'bg-red-500': connectionStatus === 'disconnected',
                'bg-yellow-500': connectionStatus === 'checking'
              }"
              :title="connectionStatusText"
            ></span>
            <span class="text-xs">
              {{ connectionStatusText }}
            </span>
          </div>

          <!-- نسخه برنامه (فقط دسکتاپ) -->
          <span class="hidden sm:inline-block px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
            v{{ version }}
          </span>

          <!-- دکمه خروج -->
          <button
            @click="handleLogout"
            class="flex flex-col sm:flex-row items-center gap-1 sm:gap-1 px-2 sm:px-2.5 py-1 text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors flex-1 sm:flex-none justify-center"
            title="خروج از حساب"
          >
            <svg class="w-5 h-5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span class="text-[10px] sm:text-xs mt-1 sm:mt-0">خروج</span>
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

interface Props {
  version?: string;
}

const props = withDefaults(defineProps<Props>(), {
  version: '0.1.0'
});

const router = useRouter();
const { logout, checkAuth, user } = useAuth();

// ===== اطلاعات کاربر =====
const userDisplayName = computed(() => {
  if (user.value) {
    return user.value.full_name || `${user.value.first_name} ${user.value.last_name}`;
  }
  return 'کاربر';
});

const userInitials = computed(() => {
  if (user.value) {
    const first = user.value.first_name?.charAt(0) || '';
    const last = user.value.last_name?.charAt(0) || '';
    return (first + last).toUpperCase();
  }
  return '?';
});

// ===== وضعیت اتصال =====
const connectionStatus = ref<'checking' | 'connected' | 'disconnected'>('checking');

const checkConnection = async () => {
  try {
    // استفاده از آدرس نسبی یا متغیر محیطی بهتر است، اما برای سازگاری با کد قبلی:
    const baseUrl = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000';
    const response = await fetch(`${baseUrl}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(3000),
    });
    connectionStatus.value = response.ok ? 'connected' : 'disconnected';
  } catch {
    connectionStatus.value = 'disconnected';
  }
};

const connectionStatusText = computed(() => {
  switch (connectionStatus.value) {
    case 'connected': return 'متصل';
    case 'disconnected': return 'قطع';
    default: return 'بررسی...';
  }
});

// ===== باز کردن مودال پروفایل =====
const openProfileModal = () => {
  window.dispatchEvent(new CustomEvent('open-profile-modal'));
};

// ===== خروج از حساب =====
const handleLogout = async () => {
  if (confirm('آیا از خروج از حساب خود اطمینان دارید؟')) {
    logout();
    await router.push('/login');
  }
};

let intervalId: number | null = null;

onMounted(() => {
  checkConnection();
  intervalId = window.setInterval(checkConnection, 30000);
  checkAuth();
});

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>