<!-- frontend/src/components/layout/SystemBanner.vue -->
<!-- حالت تعمیر + اعلان‌های همگانی با سبک‌های مختلف (نوار، نوار متحرک، روبان، کارت، توست، گوشه، مودال) -->
<template>
  <div dir="rtl">
    <!-- نوارهای بالای صفحه -->
    <div v-if="maintenance.enabled || strips.length" class="relative z-[60]">
      <div v-if="maintenance.enabled" class="px-4 py-2 text-center text-sm font-medium bg-amber-500 text-white">
        🛠 {{ maintenance.message || 'سامانه در حال به‌روزرسانی است؛ ممکن است بعضی امکانات موقتاً در دسترس نباشند.' }}
      </div>
      <AnnouncementView v-for="a in strips" :key="a.id" :a="a" @dismiss="dismiss(a.id)" />
    </div>

    <!-- کارت شناور بالا -->
    <div v-if="cards.length" class="fixed top-16 inset-x-0 z-[65] flex flex-col items-center gap-2 px-3 pointer-events-none">
      <div v-for="a in cards" :key="a.id" class="pointer-events-auto w-full max-w-md ann-pop"><AnnouncementView :a="a" @dismiss="dismiss(a.id)" /></div>
    </div>

    <!-- توست پایین‌چپ و گوشهٔ پایین‌راست -->
    <div v-if="toasts.length" class="fixed bottom-4 left-4 z-[65] flex flex-col gap-2 pointer-events-none">
      <div v-for="a in toasts" :key="a.id" class="pointer-events-auto ann-pop"><AnnouncementView :a="a" @dismiss="dismiss(a.id)" /></div>
    </div>
    <div v-if="corners.length" class="fixed bottom-4 right-4 z-[65] flex flex-col gap-2 pointer-events-none">
      <div v-for="a in corners" :key="a.id" class="pointer-events-auto ann-pop"><AnnouncementView :a="a" @dismiss="dismiss(a.id)" /></div>
    </div>

    <!-- مودال (هر بار فقط یکی) -->
    <div v-if="modal" class="fixed inset-0 z-[90] bg-black/50 backdrop-blur-[2px] flex items-center justify-center p-4" @click.self="modal.dismissible !== false && dismiss(modal.id)">
      <AnnouncementView :a="modal" class="ann-pop" @dismiss="dismiss(modal.id)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue';
import axios from 'axios';
import AnnouncementView, { type Ann } from '@/components/common/AnnouncementView.vue';

type A = Ann & { id: number };
const API = import.meta.env.VITE_API_URL || '/api/v1';
const KEY = 'dismissed_announcements';

const maintenance = ref({ enabled: false, message: '' });
const items = ref<A[]>([]);
const dismissed = ref<number[]>(JSON.parse(localStorage.getItem(KEY) || '[]'));
const visible = computed(() => items.value.filter((a) => !dismissed.value.includes(a.id)));
const strips = computed(() => visible.value.filter((a) => !a.style || ['bar', 'ticker', 'ribbon'].includes(a.style)));
const cards = computed(() => visible.value.filter((a) => a.style === 'card').slice(0, 2));
const toasts = computed(() => visible.value.filter((a) => a.style === 'toast').slice(0, 3));
const corners = computed(() => visible.value.filter((a) => a.style === 'corner').slice(0, 2));
const modal = computed(() => visible.value.find((a) => a.style === 'modal') || null);

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

<style scoped>
.ann-pop { animation: ann-pop .28s ease-out; }
@keyframes ann-pop { from { opacity: 0; transform: translateY(8px) scale(.97); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) { .ann-pop { animation: none; } }
</style>
