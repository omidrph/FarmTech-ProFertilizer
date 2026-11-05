<!-- frontend/src/components/features/fertilizer-db/FormMenu.vue -->
<!--
  منوی انتخاب «فرم برچسب» هر عنصر.
  - دسکتاپ: پاپ‌اور کنار دکمه (به بالا یا پایین باز می‌شود)
  - موبایل: برگهٔ پایین (bottom sheet) با نوار کشیدن و پس‌زمینهٔ تیره
  - هر ردیف: نشان فرمول، نام فارسی، و «درصد عنصر خالص» در آن فرم
  - فهرست‌های بلند جستجو دارند؛ گزینهٔ «کلات» جدا و برجسته است
-->
<template>
  <div class="fixed inset-0 z-[300]" :class="sheet ? 'bg-gray-900/45 backdrop-blur-[1px]' : ''" @click="$emit('close')"></div>
  <div
    class="fixed z-[310] flex flex-col bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-2xl overflow-hidden fm-pop"
    :class="sheet ? 'inset-x-0 bottom-0 rounded-t-3xl max-h-[82vh]' : 'rounded-2xl ring-1 ring-black/5'"
    :style="sheet ? undefined : panelStyle"
    dir="rtl" role="listbox" :aria-label="`فرم برچسب ${def.name}`"
  >
    <!-- نوار کشیدن (موبایل) -->
    <div v-if="sheet" class="flex justify-center pt-2.5"><span class="w-10 h-1.5 rounded-full bg-gray-300 dark:bg-gray-600"></span></div>

    <!-- سربرگ -->
    <div class="flex items-center gap-3 px-4 pt-3 pb-2.5 border-b border-gray-100 dark:border-gray-700/70 flex-shrink-0">
      <span class="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-bold flex-shrink-0" :class="symbolCls" dir="ltr">{{ def.symbol }}</span>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-bold text-gray-900 dark:text-white truncate">فرم برچسب · {{ def.name }}</p>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">همان شکلی را انتخاب کنید که روی بستهٔ محصول نوشته شده است</p>
      </div>
      <button v-if="sheet" type="button" class="p-1.5 -ml-1 rounded-lg text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700" @click="$emit('close')" aria-label="بستن">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
      </button>
    </div>

    <!-- جستجو (فقط برای فهرست‌های بلند) -->
    <div v-if="def.forms.length > 7" class="px-3 pt-2.5 flex-shrink-0">
      <div class="relative">
        <svg class="w-4 h-4 absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" /></svg>
        <input ref="searchEl" v-model="q" type="text" placeholder="جستجوی فرم (مثلاً نیترات یا KCl)…" dir="auto"
          class="w-full h-9 pr-9 pl-3 text-sm rounded-xl bg-gray-100 dark:bg-gray-700/60 border border-transparent focus:border-primary-400 focus:bg-white dark:focus:bg-gray-700 outline-none text-gray-900 dark:text-gray-100 placeholder-gray-400" />
      </div>
    </div>

    <!-- فهرست -->
    <div class="flex-1 min-h-0 overflow-y-auto px-2 py-2 space-y-1 fm-scroll">
      <button v-for="fm in shown" :key="fm.key" type="button" role="option" :aria-selected="selectedKey === fm.key" @click="$emit('select', fm.key)"
        class="group w-full flex items-center gap-3 px-2.5 py-2 rounded-xl text-right transition-colors border"
        :class="selectedKey === fm.key
          ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-700/60'
          : 'border-transparent hover:bg-gray-50 dark:hover:bg-gray-700/50'">
        <span class="min-w-[4.2rem] max-w-[8rem] text-center px-2 py-1 rounded-lg text-[12px] font-semibold font-mono truncate transition-colors" dir="ltr"
          :class="selectedKey === fm.key ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 group-hover:bg-white dark:group-hover:bg-gray-600'">{{ fm.label }}</span>
        <span class="flex-1 min-w-0 text-[13px] leading-5 text-gray-700 dark:text-gray-200 truncate">{{ fm.hint }}</span>
        <span class="flex-shrink-0 text-[11px] tabular-nums px-1.5 py-0.5 rounded-md" :class="fm.factor >= 0.9999 ? 'text-emerald-700 bg-emerald-50 dark:bg-emerald-900/20 dark:text-emerald-300' : 'text-gray-500 dark:text-gray-400'" dir="ltr" :title="`هر ۱۰۰ گرم از این ماده = ${(fm.factor * 100).toFixed(1)} گرم ${def.symbol}`">
          {{ (fm.factor * 100).toLocaleString('fa-IR', { maximumFractionDigits: 1 }) }}٪
        </span>
        <svg class="w-4 h-4 flex-shrink-0 text-primary-600 transition-opacity" :class="selectedKey === fm.key ? 'opacity-100' : 'opacity-0'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
      </button>
      <p v-if="!shown.length" class="py-6 text-center text-sm text-gray-400">فرمی با این عبارت پیدا نشد</p>
    </div>

    <!-- کلات -->
    <div v-if="canChelate" class="p-2 border-t border-gray-100 dark:border-gray-700/70 flex-shrink-0 bg-gray-50/60 dark:bg-gray-900/30">
      <button type="button" @click="$emit('chelate')"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all hover:shadow-sm"
        :class="chelateSelected ? 'bg-violet-100 dark:bg-violet-900/30 border-violet-300 dark:border-violet-700' : 'bg-violet-50/70 dark:bg-violet-900/10 border-violet-200 dark:border-violet-800/50 hover:bg-violet-50'">
        <span class="w-8 h-8 rounded-lg bg-violet-600 text-white flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>
        </span>
        <span class="flex-1 text-right min-w-0">
          <span class="block text-[13px] font-semibold text-violet-800 dark:text-violet-200">کلات {{ def.name }}</span>
          <span class="block text-[11px] text-violet-700/80 dark:text-violet-300/80 truncate">هر نوع عامل کلات‌ساز · هر درصدی که روی برچسب است</span>
        </span>
        <svg class="w-4 h-4 text-violet-500 rotate-180 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue';
import type { ElementDef } from '@/utils/labelForms';

const props = defineProps<{
  def: ElementDef;
  selectedKey: string;
  canChelate: boolean;
  chelateSelected: boolean;
  sheet: boolean;
  panelStyle: Record<string, string> | null;
  symbolCls: string;
}>();
defineEmits<{ (e: 'select', key: string): void; (e: 'chelate'): void; (e: 'close'): void }>();

const q = ref('');
const searchEl = ref<HTMLInputElement | null>(null);
const norm = (t: string) => t.toLowerCase().replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/\u200c/g, ' ');
const shown = computed(() => {
  const t = norm(q.value.trim());
  if (!t) return props.def.forms;
  return props.def.forms.filter((f) => norm(`${f.label} ${f.hint} ${f.key}`).includes(t));
});
onMounted(async () => { await nextTick(); if (!props.sheet) searchEl.value?.focus(); });
</script>

<style scoped>
.fm-pop { animation: fm-in .16s ease-out; }
@keyframes fm-in { from { opacity: 0; transform: translateY(6px) scale(.985); } to { opacity: 1; transform: none; } }
.fm-pop.inset-x-0 { animation: fm-sheet .22s cubic-bezier(.22,1,.36,1); }
@keyframes fm-sheet { from { transform: translateY(100%); } to { transform: none; } }
.fm-scroll { scrollbar-width: thin; }
@media (prefers-reduced-motion: reduce) { .fm-pop, .fm-pop.inset-x-0 { animation: none; } }
</style>
