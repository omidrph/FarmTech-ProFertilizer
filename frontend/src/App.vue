<template>
  <div id="app" class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import { useAppStore } from '@/store/modules/appStore';
import { useAuth } from '@/composables/useAuth';

const appStore = useAppStore();
const { user, logout } = useAuth();

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

  // ============================================================
  // ✅ پاک کردن state در صورت بسته شدن صفحه
  // ============================================================
  const handleBeforeUnload = () => {
    // اگر کاربر لاگین نیست، همه چیز را پاک کن
    const token = localStorage.getItem('access_token');
    if (!token) {
      localStorage.removeItem('access_token');
    }
  };

  // ============================================================
  // ✅ گوش دادن به تغییرات روتر برای بررسی وضعیت احراز هویت
  // ============================================================
  const handleVisibilityChange = () => {
    if (document.hidden) {
      // صفحه مخفی شد - کاری نکن
      return;
    }
    
    // صفحه دوباره قابل مشاهده شد - بررسی کن که آیا کاربر لاگین است
    const token = localStorage.getItem('access_token');
    const cookieToken = document.cookie.split(';').find(c => c.trim().startsWith('access_token='));
    
    // اگر توکنی وجود ندارد و کاربر قبلاً لاگین بوده، logout کن
    if (!token && !cookieToken && user.value) {
      console.log('🔒 Session expired, logging out...');
      logout();
      window.location.href = '/login';
    }
  };

  window.addEventListener('beforeunload', handleBeforeUnload);
  document.addEventListener('visibilitychange', handleVisibilityChange);

  // ============================================================
  // ✅ پاک کردن event listener ها هنگام unmount
  // ============================================================
  onUnmounted(() => {
    window.removeEventListener('beforeunload', handleBeforeUnload);
    document.removeEventListener('visibilitychange', handleVisibilityChange);
  });
});

// ============================================================
// ✅ استفاده از Custom Event برای خروج از همه جا
// ============================================================
window.addEventListener('force-logout', async () => {
  const { logout } = useAuth();
  await logout();
  window.location.href = '/login';
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

/* RTL Support for all elements */
[dir="rtl"] {
  text-align: right;
}

[dir="ltr"] {
  text-align: left;
}

/* Selection color */
::selection {
  background-color: #2563eb;
  color: #ffffff;
}

.dark ::selection {
  background-color: #3b82f6;
  color: #ffffff;
}
</style>