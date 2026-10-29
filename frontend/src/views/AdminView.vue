<!-- frontend/src/views/AdminView.vue -->
<!-- پنل مدیریت: فقط نقش admin (راه‌نگهبان روتر + بررسی سمت سرور) -->
<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950" dir="rtl">
    <header class="sticky top-0 z-40 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 h-14 flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5 min-w-0">
          <img src="/Logo.webp" alt="" class="h-9 w-9 object-contain rounded-lg" />
          <div class="leading-tight min-w-0">
            <h1 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white truncate">پنل مدیریت سهند کود</h1>
            <p class="text-[10px] text-gray-500 hidden sm:block">{{ me?.full_name }} · مدیر</p>
          </div>
        </div>
        <router-link to="/" class="ad-btn ad-btn-sm flex-shrink-0">بازگشت به برنامه</router-link>
      </div>
      <nav class="max-w-7xl mx-auto px-2 sm:px-4 flex gap-1 overflow-x-auto" aria-label="بخش‌های مدیریت">
        <button v-for="t in tabs" :key="t.k" @click="go(t.k)"
          class="px-3 py-2.5 text-sm whitespace-nowrap border-b-2 transition-colors"
          :class="tab === t.k ? 'border-primary-600 text-primary-700 dark:text-primary-300 font-semibold' : 'border-transparent text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'">{{ t.l }}</button>
      </nav>
    </header>

    <main class="max-w-7xl mx-auto px-3 sm:px-4 py-4">
      <div v-if="denied" class="ad-card p-10 text-center text-sm text-gray-500">دسترسی به این بخش فقط برای مدیران سیستم است.</div>
      <template v-else-if="me">
        <AdminDashboard v-if="tab === 'dashboard'" @open-user="openUser" />
        <AdminUsers v-else-if="tab === 'users'" :key="usersKey" :self-id="me.id" :open-user-id="pendingUser" />
        <AdminFertilizers v-else-if="tab === 'fertilizers'" />
        <AdminCalculations v-else-if="tab === 'calculations'" />
        <AdminLogs v-else-if="tab === 'logs'" />
        <AdminAnnouncements v-else-if="tab === 'announcements'" />
        <AdminSettings v-else-if="tab === 'settings'" />
      </template>
      <div v-else class="ad-card p-10 text-center text-sm text-gray-500">در حال بررسی دسترسی…</div>
    </main>

    <!-- توست‌ها -->
    <div class="fixed bottom-4 right-1/2 translate-x-1/2 z-[120] space-y-2 w-[min(92vw,22rem)] pointer-events-none">
      <div v-for="t in toasts" :key="t.id" class="px-4 py-2.5 rounded-xl text-sm text-white shadow-lg" :class="t.type === 'error' ? 'bg-rose-600' : 'bg-emerald-600'">{{ t.msg }}</div>
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
import { onMounted, ref, watch } from 'vue';
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
  { k: 'dashboard', l: 'داشبورد' }, { k: 'users', l: 'کاربران' }, { k: 'fertilizers', l: 'کودهای سیستمی' },
  { k: 'calculations', l: 'محاسبه‌ها' }, { k: 'logs', l: 'لاگ‌ها' }, { k: 'announcements', l: 'اعلان‌ها' }, { k: 'settings', l: 'تنظیمات و سلامت' }
];
const route = useRoute();
const router = useRouter();
const tab = ref<string>(tabs.some((t) => t.k === route.query.tab) ? String(route.query.tab) : 'dashboard');
const me = ref<{ id: number; full_name: string; role: string } | null>(null);
const denied = ref(false);
const pendingUser = ref<number | null>(null);
const usersKey = ref(0);

const go = (k: string) => { tab.value = k; pendingUser.value = null; router.replace({ query: { tab: k } }); };
const openUser = (id: number) => { pendingUser.value = id; usersKey.value++; tab.value = 'users'; router.replace({ query: { tab: 'users' } }); };
watch(() => route.query.tab, (v) => { if (typeof v === 'string' && tabs.some((t) => t.k === v)) tab.value = v; });

onMounted(async () => {
  try {
    const cookie = document.cookie.split(';').map((c) => c.trim()).find((c) => c.startsWith('access_token='));
    const token = cookie ? cookie.substring('access_token='.length) : localStorage.getItem('access_token');
    const r = await axios.get((import.meta.env.VITE_API_URL || '/api/v1') + '/auth/me', { headers: { Authorization: `Bearer ${token}` }, withCredentials: true });
    if (r.data.role !== 'admin') { denied.value = true; setTimeout(() => router.replace('/'), 1200); return; }
    me.value = r.data;
  } catch { router.replace('/login'); }
});
</script>
