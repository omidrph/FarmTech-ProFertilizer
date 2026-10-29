<!-- frontend/src/components/layout/SystemBanner.vue -->
<!-- نوار بالای برنامه: حالت تعمیر + اعلان‌های همگانی (از پنل مدیریت) -->
<template>
  <div v-if="maintenance.enabled || visible.length" class="relative z-[60]" dir="rtl">
    <div v-if="maintenance.enabled" class="px-4 py-2 text-center text-sm font-medium bg-amber-500 text-white">
      🛠 {{ maintenance.message || 'سامانه در حال به‌روزرسانی است؛ ممکن است بعضی امکانات موقتاً در دسترس نباشند.' }}
    </div>
    <div v-for="a in visible" :key="a.id" class="px-4 py-2 text-sm flex items-start justify-between gap-3" :class="cls[a.level] || cls.info">
      <p class="min-w-0"><b>{{ a.title }}</b><span v-if="a.body" class="opacity-90"> — {{ a.body }}</span></p>
      <button class="flex-shrink-0 opacity-80 hover:opacity-100 text-lg leading-none" aria-label="بستن اعلان" @click="dismiss(a.id)">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue';
import axios from 'axios';

interface Ann { id: number; title: string; body?: string; level: string }
const API = import.meta.env.VITE_API_URL || '/api/v1';
const KEY = 'dismissed_announcements';

const maintenance = ref({ enabled: false, message: '' });
const items = ref<Ann[]>([]);
const dismissed = ref<number[]>(JSON.parse(localStorage.getItem(KEY) || '[]'));
const visible = computed(() => items.value.filter((a) => !dismissed.value.includes(a.id)));
const cls: Record<string, string> = {
  info: 'bg-sky-600 text-white', success: 'bg-emerald-600 text-white', warning: 'bg-amber-500 text-white', danger: 'bg-rose-600 text-white'
};

async function load() {
  try {
    const cookie = document.cookie.split(';').map((c) => c.trim()).find((c) => c.startsWith('access_token='));
    const token = cookie ? cookie.substring('access_token='.length) : localStorage.getItem('access_token');
    const r = await axios.get(`${API}/system/status`, { timeout: 6000, withCredentials: true, headers: token ? { Authorization: `Bearer ${token}` } : {} });
    maintenance.value = r.data.maintenance;
    items.value = r.data.announcements || [];
  } catch { /* بی‌صدا: نبودن اعلان نباید برنامه را مختل کند */ }
}
function dismiss(id: number) {
  dismissed.value = [...dismissed.value, id].slice(-50);
  localStorage.setItem(KEY, JSON.stringify(dismissed.value));
}

let timer: number | undefined;
onMounted(() => { load(); timer = window.setInterval(load, 5 * 60 * 1000); });
onUnmounted(() => clearInterval(timer));
</script>
