<!-- frontend/src/views/AdminView.vue -->
<!-- پنل مدیریت: هم‌سبک هدر و زیرمنوی خود برنامه؛ فقط نقش admin (راه‌نگهبان روتر + بررسی سمت سرور) -->
<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200 flex flex-col" dir="rtl">
    <!-- هدر (همان قالب هدر برنامه) -->
    <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex items-center justify-between gap-3 h-14 sm:h-16">
          <div class="flex items-center gap-2.5 min-w-0">
            <img src="/Logo.webp" alt="سهند کود" class="h-10 w-10 sm:h-12 sm:w-12 object-contain rounded-lg flex-shrink-0" />
            <div class="leading-tight min-w-0">
              <h1 class="text-base sm:text-lg font-bold text-gray-800 dark:text-white truncate">پنل مدیریت</h1>
              <p class="text-[10px] text-gray-500 dark:text-gray-400 truncate hidden sm:block">سهند کود · {{ me?.full_name }}</p>
            </div>
          </div>

          <!-- جستجوی سریع کاربر -->
          <form class="hidden md:flex flex-1 max-w-sm" @submit.prevent="quickSearch">
            <div class="relative w-full">
              <svg class="w-4 h-4 absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" /></svg>
              <input ref="searchEl" v-model="searchText" class="w-full pr-9 pl-10 py-2 text-sm rounded-xl bg-gray-100 dark:bg-gray-800 border border-transparent focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 outline-none transition" placeholder="جستجوی کاربر (نام یا شماره)…" />
              <kbd class="absolute left-2.5 top-1/2 -translate-y-1/2 text-[10px] px-1.5 py-0.5 rounded bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-400">/</kbd>
            </div>
          </form>

          <div class="flex items-center gap-1.5 flex-shrink-0">
            <button class="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition" :title="dark ? 'حالت روشن' : 'حالت تیره'" @click="toggleTheme">
              <svg v-if="!dark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" /></svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" /></svg>
            </button>
            <router-link to="/" class="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 text-sm transition">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" /></svg>
              <span class="hidden sm:inline">بازگشت به برنامه</span>
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- زیرمنو (همان استایل تب‌های برنامه) -->
    <nav class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-14 sm:top-16 z-40" aria-label="بخش‌های مدیریت">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex items-center gap-1 overflow-x-auto py-1 scrollbar-hide snap-x snap-mandatory">
          <button v-for="t in tabs" :key="t.k" @click="go(t.k)"
            class="relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all duration-200 text-sm whitespace-nowrap snap-start flex-shrink-0"
            :class="tab === t.k ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" :d="t.icon" /></svg>
            <span>{{ t.l }}</span>
            <span v-if="tab === t.k" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-0.5 bg-primary-600 dark:bg-primary-400 rounded-full"></span>
          </button>
        </div>
      </div>
    </nav>

    <main class="flex-1 max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-6 w-full">
      <div v-if="denied" class="ad-card p-10 text-center text-sm text-gray-500">دسترسی به این بخش فقط برای مدیران سیستم است.</div>
      <Transition v-else-if="me" name="ad-fade" mode="out-in">
        <AdminDashboard v-if="tab === 'dashboard'" key="d" :name="me.full_name" @open-user="openUser" @go="go" />
        <AdminUsers v-else-if="tab === 'users'" :key="'u' + usersKey" :self-id="me.id" :open-user-id="pendingUser" :initial-query="initialQuery" />
        <AdminFertilizers v-else-if="tab === 'fertilizers'" key="f" />
        <AdminCalculations v-else-if="tab === 'calculations'" key="c" />
        <AdminLogs v-else-if="tab === 'logs'" key="l" />
        <AdminAnnouncements v-else-if="tab === 'announcements'" key="a" />
        <AdminSettings v-else-if="tab === 'settings'" key="s" />
      </Transition>
      <div v-else class="ad-card p-10 text-center text-sm text-gray-500 animate-pulse">در حال بررسی دسترسی…</div>
    </main>

    <!-- توست‌ها -->
    <div class="fixed bottom-4 right-1/2 translate-x-1/2 z-[120] space-y-2 w-[min(92vw,24rem)] pointer-events-none">
      <TransitionGroup name="ad-toast">
        <div v-for="t in toasts" :key="t.id" class="flex items-center gap-2.5 px-4 py-3 rounded-xl text-sm text-white shadow-xl backdrop-blur" :class="t.type === 'error' ? 'bg-rose-600/95' : 'bg-gray-900/95 dark:bg-emerald-600/95'">
          <svg v-if="t.type === 'error'" class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>
          <svg v-else class="w-5 h-5 flex-shrink-0 text-emerald-400 dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{{ t.msg }}</span>
        </div>
      </TransitionGroup>
    </div>

    <!-- تأیید -->
    <AppModal :open="confirmState.open" :title="confirmState.title" size="sm" @close="answerConfirm(false)">
      <p class="text-sm text-gray-600 dark:text-gray-300 leading-7">{{ confirmState.message || 'آیا مطمئن هستید؟' }}</p>
      <template #footer>
        <div class="flex justify-end gap-2 p-3">
          <button class="ad-btn" @click="answerConfirm(false)">انصراف</button>
          <button :class="confirmState.danger ? 'ad-btn-danger' : 'ad-btn-primary'" @click="answerConfirm(true)">{{ confirmState.confirmText }}</button>
        </div>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import AppModal from '@/components/common/AppModal.vue';
import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import AdminUsers from '@/components/admin/AdminUsers.vue';
import AdminFertilizers from '@/components/admin/AdminFertilizers.vue';
import AdminCalculations from '@/components/admin/AdminCalculations.vue';
import AdminLogs from '@/components/admin/AdminLogs.vue';
import AdminAnnouncements from '@/components/admin/AdminAnnouncements.vue';
import AdminSettings from '@/components/admin/AdminSettings.vue';
import { answerConfirm, confirmState, toasts } from '@/components/admin/adminUi';
import '@/components/admin/admin.css';

const tabs = [
  { k: 'dashboard', l: 'داشبورد', icon: 'M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z' },
  { k: 'users', l: 'کاربران', icon: 'M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0z' },
  { k: 'fertilizers', l: 'کودهای سیستمی', icon: 'M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5' },
  { k: 'calculations', l: 'محاسبه‌ها', icon: 'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z' },
  { k: 'logs', l: 'لاگ‌ها', icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z' },
  { k: 'announcements', l: 'اعلان‌ها', icon: 'M10.34 15.84c-.688-.06-1.386-.09-2.09-.09H7.5a4.5 4.5 0 110-9h.75c.704 0 1.402-.03 2.09-.09m0 9.18c.253.962.584 1.892.985 2.783.247.55.06 1.21-.463 1.511l-.657.38c-.551.318-1.26.117-1.527-.461a20.845 20.845 0 01-1.44-4.282m3.102.069a18.03 18.03 0 01-.59-4.59c0-1.586.205-3.124.59-4.59m0 9.18a23.848 23.848 0 018.835 2.535M10.34 6.66a23.847 23.847 0 008.835-2.535m0 0A23.74 23.74 0 0018.795 3m.38 1.125a23.91 23.91 0 011.014 5.395m-1.014 8.855c-.118.38-.245.754-.38 1.125m.38-1.125a23.91 23.91 0 001.014-5.395m0-3.46c.495.413.811 1.035.811 1.73 0 .695-.316 1.317-.811 1.73m0-3.46a24.347 24.347 0 010 3.46' },
  { k: 'settings', l: 'تنظیمات و سلامت', icon: 'M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281zM15 12a3 3 0 11-6 0 3 3 0 016 0z' }
];
const route = useRoute();
const router = useRouter();
const tab = ref<string>(tabs.some((t) => t.k === route.query.tab) ? String(route.query.tab) : 'dashboard');
const me = ref<{ id: number; full_name: string; role: string } | null>(null);
const denied = ref(false);
const pendingUser = ref<number | null>(null);
const usersKey = ref(0);
const initialQuery = ref('');
const searchText = ref('');
const searchEl = ref<HTMLInputElement | null>(null);
const dark = ref(document.documentElement.classList.contains('dark'));

const go = (k: string) => { tab.value = k; pendingUser.value = null; initialQuery.value = ''; router.replace({ query: { tab: k } }); };
const openUser = (id: number) => { pendingUser.value = id; initialQuery.value = ''; usersKey.value++; tab.value = 'users'; router.replace({ query: { tab: 'users' } }); };
const quickSearch = () => { initialQuery.value = searchText.value.trim(); pendingUser.value = null; usersKey.value++; tab.value = 'users'; router.replace({ query: { tab: 'users' } }); };
const toggleTheme = () => {
  dark.value = !dark.value;
  document.documentElement.classList.toggle('dark', dark.value);
  localStorage.setItem('theme', dark.value ? 'dark' : 'light');
};
watch(() => route.query.tab, (v) => { if (typeof v === 'string' && tabs.some((t) => t.k === v)) tab.value = v; });

// میان‌بر «/» برای جستجوی سریع
const onKey = (e: KeyboardEvent) => {
  const el = e.target as HTMLElement;
  if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(el?.tagName)) { e.preventDefault(); searchEl.value?.focus(); }
};

onMounted(async () => {
  window.addEventListener('keydown', onKey);
  try {
    const cookie = document.cookie.split(';').map((c) => c.trim()).find((c) => c.startsWith('access_token='));
    const token = cookie ? cookie.substring('access_token='.length) : localStorage.getItem('access_token');
    const r = await axios.get((import.meta.env.VITE_API_URL || '/api/v1') + '/auth/me', { headers: { Authorization: `Bearer ${token}` }, withCredentials: true });
    if (r.data.role !== 'admin') { denied.value = true; setTimeout(() => router.replace('/'), 1200); return; }
    me.value = r.data;
  } catch { router.replace('/login'); }
});
onUnmounted(() => window.removeEventListener('keydown', onKey));
</script>

<style>
.ad-fade-enter-active, .ad-fade-leave-active { transition: opacity .18s ease, transform .18s ease; }
.ad-fade-enter-from { opacity: 0; transform: translateY(6px); }
.ad-fade-leave-to { opacity: 0; }
.ad-toast-enter-active, .ad-toast-leave-active { transition: all .25s ease; }
.ad-toast-enter-from, .ad-toast-leave-to { opacity: 0; transform: translateY(12px) scale(.96); }
.scrollbar-hide::-webkit-scrollbar { display: none; }
@media (prefers-reduced-motion: reduce) { .ad-fade-enter-active, .ad-fade-leave-active, .ad-toast-enter-active, .ad-toast-leave-active { transition: none; } }
</style>
