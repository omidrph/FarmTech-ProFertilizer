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

        <!-- User Info, Status, Version & Logout -->
        <div class="flex items-center gap-3 flex-wrap justify-center">
          <!-- User Info -->
          <button
            @click="goToProfile"
            class="flex items-center gap-1.5 px-2.5 py-1 text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <div class="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400 font-bold text-xs">
              {{ userInitials }}
            </div>
            <span class="hidden sm:inline font-medium">{{ userDisplayName }}</span>
            <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>

          <!-- Separator -->
          <span class="text-gray-300 dark:text-gray-600">|</span>

          <!-- Status Indicator -->
          <div class="flex items-center gap-1.5">
            <span 
              class="inline-block w-2.5 h-2.5 rounded-full animate-pulse"
              :class="{
                'bg-green-500': connectionStatus === 'connected',
                'bg-red-500': connectionStatus === 'disconnected',
                'bg-yellow-500': connectionStatus === 'checking'
              }"
            ></span>
            <span class="text-xs hidden sm:inline">
              {{ connectionStatusText }}
            </span>
          </div>
          
          <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono hidden sm:inline">
            v{{ version }}
          </span>

          <!-- دکمه خروج -->
          <button
            @click="handleLogout"
            class="flex items-center gap-1 px-2.5 py-1 text-xs text-danger-600 hover:text-danger-700 dark:text-danger-400 dark:hover:text-danger-300 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span class="hidden sm:inline">خروج</span>
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
  return '👤';
});

// ===== وضعیت اتصال =====
const connectionStatus = ref<'checking' | 'connected' | 'disconnected'>('checking');

const checkConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
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
    default: return 'در حال بررسی...';
  }
});

// ===== رفتن به پروفایل =====
const goToProfile = () => {
  router.push('/profile');
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
  // بررسی وضعیت کاربر
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