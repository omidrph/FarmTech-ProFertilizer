<!-- frontend/src/components/features/home/HomeAttentionList.vue -->
<!--
  خطاها و هشدارهای صفحهٔ خانه
  ------------------------------------------------------------
  چهار نوع: خطا (قرمز)، خطای اصلاح pH (بنفش)، هشدار (کهربایی)، نکته (آبی). مرتب‌شده بر اساس شدت؛
  حداکثر ۴ مورد نشان داده می‌شود و بقیه با «نمایش همه».
-->
<template>
  <section v-if="items.length" class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <header class="px-4 sm:px-5 py-3 border-b border-gray-100 dark:border-gray-700 flex items-center gap-2.5 flex-wrap">
      <span class="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center">
        <svg class="w-4 h-4 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z" /></svg>
      </span>
      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">خطاها و هشدارها</h3>
      <div class="flex items-center gap-1.5 mr-auto">
        <span v-for="c in counts" :key="c.kind" class="text-[11px] font-medium px-2 py-0.5 rounded-full tabular-nums" :class="styles[c.kind].chip">{{ c.n.toLocaleString('fa-IR') }} {{ styles[c.kind].label }}</span>
      </div>
    </header>

    <ul class="p-3 sm:p-4 grid grid-cols-1 lg:grid-cols-2 gap-2.5">
      <li v-for="(item, i) in shown" :key="i" class="flex items-start gap-3 rounded-xl border p-3 transition-colors" :class="styles[item.kind].box">
        <span class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center" :class="styles[item.kind].icon">
          <svg v-if="item.kind === 'ph'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4a2 2 0 001.8-3l-5-9V3" /></svg>
          <svg v-else-if="item.kind === 'info'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z" /></svg>
        </span>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-semibold leading-6" :class="styles[item.kind].title">{{ item.title }}</p>
          <p v-if="item.text" class="text-xs leading-5 mt-0.5" :class="styles[item.kind].text">{{ item.text }}</p>
          <p v-if="item.hint" class="text-[11px] leading-5 mt-1 opacity-80" :class="styles[item.kind].text">راهنما: {{ item.hint }}</p>
        </div>
      </li>
    </ul>

    <footer v-if="items.length > LIMIT" class="px-4 pb-3 -mt-1 flex justify-center">
      <button type="button" @click="all = !all" class="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
        {{ all ? 'نمایش کمتر' : `نمایش همه (${items.length.toLocaleString('fa-IR')})` }}
      </button>
    </footer>
  </section>
  <section v-else class="flex items-center gap-2.5 rounded-2xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/15 px-4 py-3">
    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
    <p class="text-sm text-emerald-800 dark:text-emerald-200">هیچ خطا یا هشداری برای این فرمول ثبت نشده است.</p>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

type Kind = 'danger' | 'warn' | 'ph' | 'info';
interface Item { kind: Kind; title: string; text?: string; hint?: string }
const props = defineProps<{ items: Item[] }>();
defineEmits<{ (e: 'details'): void }>();

const LIMIT = 4;
const all = ref(false);
const shown = computed(() => (all.value ? props.items : props.items.slice(0, LIMIT)));
const counts = computed(() =>
  (['danger', 'ph', 'warn', 'info'] as Kind[]).map((kind) => ({ kind, n: props.items.filter((i) => i.kind === kind).length })).filter((c) => c.n)
);

const styles: Record<Kind, { box: string; icon: string; title: string; text: string; chip: string; label: string }> = {
  danger: { box: 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-700/60', icon: 'bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400', title: 'text-rose-800 dark:text-rose-200', text: 'text-rose-700 dark:text-rose-300', chip: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300', label: 'خطا' },
  ph: { box: 'bg-violet-50 dark:bg-violet-950/40 border-violet-300 dark:border-violet-700/60', icon: 'bg-violet-600 text-white', title: 'text-violet-900 dark:text-violet-100', text: 'text-violet-700 dark:text-violet-300', chip: 'bg-violet-100 text-violet-700 dark:bg-violet-900/40 dark:text-violet-300', label: 'خطای pH' },
  warn: { box: 'bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-700/60', icon: 'bg-amber-100 dark:bg-amber-900/50 text-amber-600 dark:text-amber-400', title: 'text-amber-800 dark:text-amber-200', text: 'text-amber-700 dark:text-amber-300', chip: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300', label: 'هشدار' },
  info: { box: 'bg-sky-50 dark:bg-sky-950/40 border-sky-200 dark:border-sky-700/60', icon: 'bg-sky-100 dark:bg-sky-900/50 text-sky-600 dark:text-sky-400', title: 'text-sky-800 dark:text-sky-200', text: 'text-sky-700 dark:text-sky-300', chip: 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300', label: 'نکته' }
};
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
