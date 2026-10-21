<template>
  <Transition name="dl-card">
    <aside
      v-if="visible && links.length"
      class="fixed z-40 bottom-3 inset-x-3 lg:inset-x-auto lg:bottom-6 lg:right-6 lg:w-80 rounded-2xl p-3.5 border shadow-lg
             bg-white/95 dark:bg-gray-800/95 border-gray-200 dark:border-gray-700 backdrop-blur-md
             lg:bg-white/10 lg:dark:bg-white/10 lg:border-white/20 lg:shadow-none"
    >
      <button type="button" @click="close" aria-label="بستن"
        class="absolute top-2.5 left-2.5 text-gray-400 hover:text-gray-600 lg:text-white/60 lg:hover:text-white transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
      </button>

      <p class="text-sm font-bold text-gray-900 dark:text-white lg:text-white">نسخهٔ اندروید</p>
      <p class="text-xs text-gray-500 dark:text-gray-400 lg:text-primary-100 mt-0.5 mb-3">روی گوشی نصب کنید و گزارش‌هایتان را همه‌جا ببینید.</p>

      <div class="flex flex-wrap gap-2">
        <a v-for="l in links" :key="l.key" :href="l.href" :target="l.key === 'apk' ? undefined : '_blank'" rel="noopener"
           :download="l.key === 'apk' ? '' : undefined"
           class="flex-1 min-w-[5.5rem] text-center text-xs font-semibold px-3 py-2 rounded-lg transition-colors"
           :class="l.key === 'apk'
             ? 'bg-primary-600 hover:bg-primary-700 text-white lg:bg-white lg:hover:bg-primary-50 lg:text-primary-700'
             : 'bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-100 lg:bg-white/15 lg:hover:bg-white/25 lg:text-white'">
          {{ l.label }}
        </a>
      </div>

      <p v-if="hasApk" class="text-[11px] leading-relaxed text-gray-400 dark:text-gray-500 lg:text-primary-200 mt-2.5">
        برای نصب، گزینهٔ «نصب از منابع ناشناس» را در تنظیمات گوشی فعال کنید.
      </p>
    </aside>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { APP_LINKS } from '@/config/appLinks';

const KEY = 'dl_card_closed';
const visible = ref(false);

const links = computed(() => [
  { key: 'bazaar', label: 'کافه‌بازار', href: APP_LINKS.bazaar },
  { key: 'myket', label: 'مایکت', href: APP_LINKS.myket },
  { key: 'apk', label: 'دانلود مستقیم (APK)', href: APP_LINKS.apk },
].filter((l) => !!l.href));
const hasApk = computed(() => !!APP_LINKS.apk);

const close = () => {
  visible.value = false;
  try { sessionStorage.setItem(KEY, '1'); } catch { /* ignore */ }
};

onMounted(() => {
  let closed = false;
  try { closed = sessionStorage.getItem(KEY) === '1'; } catch { /* ignore */ }
  if (!closed) setTimeout(() => (visible.value = true), 1400);
});
</script>

<style scoped>
.dl-card-enter-active { transition: transform .7s cubic-bezier(.22,1,.36,1), opacity .6s ease; }
.dl-card-leave-active { transition: transform .35s ease, opacity .3s ease; }
.dl-card-enter-from, .dl-card-leave-to { opacity: 0; transform: translateY(120%); }
@media (min-width: 1024px) {
  .dl-card-enter-from, .dl-card-leave-to { transform: translate(40px, 40px) scale(.96); }
}
@media (prefers-reduced-motion: reduce) {
  .dl-card-enter-active, .dl-card-leave-active { transition: opacity .2s ease; }
  .dl-card-enter-from, .dl-card-leave-to { transform: none; }
}
</style>
