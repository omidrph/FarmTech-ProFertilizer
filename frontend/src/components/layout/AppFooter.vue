<template>
  <!-- 
    تغییرات اصلی برای موبایل:
    - fixed bottom-0 left-0 right-0 z-50: چسبیدن به پایین صفحه
    - sm:relative: در دسکتاپ حالت عادی داشته باشد
    - shadow-[0_-4px_...]: سایه رو به بالا برای جدا شدن از محتوا
  -->
  <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 transition-colors duration-200 sm:py-3 relative sm:relative fixed bottom-0 left-0 right-0 z-50 sm:z-auto shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] sm:shadow-none">
    
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

          <!-- وضعیت اتصال (فقط در دسکتاپ نمایش داده می‌شود) -->
          <div class="hidden sm:flex items-center gap-1.5 px-2 py-1 flex-shrink-0">
            <span
              class="inline-block w-2.5 h-2.5 rounded-full"
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
            <svg class="w-5 h-5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"/>
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
    // 🔧 قبلاً وقتی VITE_API_URL برابر مسیر نسبی "/api/v1" بود، بعد از
    // .replace('/api/v1', '') مقدار به رشته‌ی خالی "" تبدیل می‌شد که در
    // جاوااسکریپت falsy است، پس همیشه با "|| 'http://localhost:8000'"
    // جایگزین می‌شد. یعنی این چک اتصال در پروڈاکشن همیشه سعی می‌کرد به
    // localhost:8000 روی سیستم خودِ کاربر وصل شود (که هیچ‌وقت جواب
    // نمی‌داد) و وضعیت همیشه "قطع" نشان داده می‌شد، حتی وقتی سرور سالم
    // بود. اکنون اگر آدرس نسبی باشد، baseUrl خالی می‌ماند و درخواست به
    // مسیر نسبی "/health" ارسال می‌شود که nginx آن را به بک‌اند
    // پروکسی می‌کند (بدون فال‌بک اشتباه به localhost).
    const rawApiUrl = import.meta.env.VITE_API_URL || '/api/v1';
    const baseUrl = rawApiUrl.replace('/api/v1', '');
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

// ============================================================
// ✅ خروج از حساب - نسخه اصلاح شده
// ============================================================
const handleLogout = async () => {
  // بررسی اینکه کاربر واقعاً لاگین است
  if (!user.value) {
    // اگر کاربر لاگین نیست، مستقیم به صفحه ورود برو
    await router.push('/login');
    return;
  }

  // تأیید از کاربر
  if (!confirm('آیا از خروج از حساب خود اطمینان دارید؟')) {
    return;
  }

  try {
    // 1. اجرای تابع logout که توکن را پاک می‌کند
    await logout();
    
    // 2. پاک کردن state کاربر
    user.value = null;
    
    // 3. پاک کردن localStorage
    localStorage.removeItem('access_token');
    
    // 4. پاک کردن cookie (از طریق سرور انجام می‌شود ولی برای اطمینان)
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    
    // 5. هدایت به صفحه ورود
    await router.push('/login');
    
    // 6. رفرش کامل صفحه برای پاک شدن کامل state
    // این کار باعث می‌شود همه چیز ریست شود
    window.location.href = '/login';
    
  } catch (error) {
    console.error('❌ Error during logout:', error);
    // اگر خطایی رخ داد، باز هم کاربر را به صفحه ورود ببر
    await router.push('/login');
    window.location.href = '/login';
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