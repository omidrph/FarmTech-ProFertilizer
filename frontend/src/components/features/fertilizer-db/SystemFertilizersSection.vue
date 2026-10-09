<!-- frontend/src/components/features/fertilizer-db/SystemFertilizersSection.vue -->
<!--
  دو دستهٔ کود آماده: «کودهای شرکتی» (محصولات برند مشخص با برگهٔ آزمایش) و «کودهای سیستمی» (استاندارد).
  هر دسته یک کارت فشرده است؛ فهرست کامل و کپی تکی/گروهی در مودال انجام می‌شود.
-->
<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
    <div
      v-for="g in groups"
      :key="g.key"
      class="rounded-xl border px-3.5 py-3 flex items-center gap-3 bg-white dark:bg-gray-800"
      :class="g.border"
    >
      <span class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0" :class="g.iconBg">
        <svg class="w-5 h-5" :class="g.iconText" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="g.icon"></svg>
      </span>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ g.title }}</p>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 tabular-nums">
          {{ g.items.length.toLocaleString('fa-IR') }} کود
          <template v-if="g.items.length">
            · <span :class="g.pending.length ? 'text-gray-500' : 'text-emerald-600 dark:text-emerald-400'">{{ (g.items.length - g.pending.length).toLocaleString('fa-IR') }} کپی‌شده</span>
          </template>
        </p>
      </div>
      <button type="button" @click="open = g.key" :disabled="!g.items.length"
        class="h-8 px-3 rounded-lg text-xs font-medium text-white disabled:opacity-40 transition-colors flex-shrink-0" :class="g.btn">
        مشاهده
      </button>
    </div>
  </div>

  <!-- مودال فهرست -->
  <Teleport to="body">
    <div v-if="current" class="fixed inset-0 z-[60] flex items-end sm:items-center justify-center p-0 sm:p-4" @keydown.esc="open = null">
      <div class="absolute inset-0 bg-gray-900/50 backdrop-blur-[2px]" @click="open = null"></div>
      <div class="relative w-full sm:max-w-2xl bg-white dark:bg-gray-800 rounded-t-2xl sm:rounded-2xl shadow-2xl max-h-[88vh] flex flex-col" role="dialog" aria-modal="true">
        <div class="px-5 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
          <div class="min-w-0 flex-1">
            <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ current.title }}</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ current.hint }}</p>
          </div>
          <button type="button" @click="open = null" class="w-8 h-8 rounded-lg text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700" aria-label="بستن">✕</button>
        </div>

        <div class="px-5 py-3 border-b border-gray-100 dark:border-gray-700 flex items-center gap-2">
          <input v-model="q" placeholder="جستجو…" class="flex-1 h-9 px-3 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500" />
          <button type="button" @click="copyGroup" :disabled="isCopying || !current.pending.length"
            class="h-9 px-3 rounded-lg text-xs font-medium text-white disabled:opacity-40 flex-shrink-0 transition-colors" :class="current.btn">
            {{ isCopying ? 'در حال کپی…' : `کپی همهٔ ${current.pending.length.toLocaleString('fa-IR')} مورد` }}
          </button>
        </div>

        <ul class="overflow-y-auto divide-y divide-gray-100 dark:divide-gray-700">
          <li v-for="f in filtered" :key="f.id" class="px-5 py-3 flex items-start gap-3">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-gray-900 dark:text-white flex flex-wrap items-center gap-1.5">
                {{ f.name }}
                <span v-if="f.isAcid" class="text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">اسید</span>
                <span v-if="f.isBase" class="text-[10px] px-1.5 py-0.5 rounded bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300">باز</span>
                <span class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300">{{ formLabel(f.form) }}</span>
              </p>
              <p class="mt-1 flex flex-wrap gap-1">
                <span v-for="[el, pct] in elementsOf(f)" :key="el" class="text-[10px] px-1.5 py-0.5 rounded border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 tabular-nums">{{ el }} {{ pct }}%</span>
              </p>
            </div>
            <span v-if="isCopied(f)" class="text-[11px] text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-1">کپی شد ✓</span>
            <button v-else type="button" @click="$emit('copy-single', f.id)" class="h-8 px-3 rounded-lg border border-gray-200 dark:border-gray-600 text-xs font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex-shrink-0">کپی</button>
          </li>
          <li v-if="!filtered.length" class="px-5 py-8 text-center text-sm text-gray-500">موردی یافت نشد.</li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const props = defineProps<{
  systemFertilizers: any[];
  userFertilizers?: any[];
  copyStatus: any;
  isCopying: boolean;
}>();
const emit = defineEmits<{
  (e: 'copy-all'): void;
  (e: 'copy-single', id: string): void;
  (e: 'copy-many', ids: string[]): void;
}>();

const open = ref<'company' | 'system' | null>(null);
const q = ref('');

// کود شرکتی = برند مشخص (غیر از «استاندارد»)؛ بقیه «سیستمی»
const isCompany = (f: any) => !!f.brand && f.brand !== 'استاندارد';
const copiedIds = computed(() => new Set((props.userFertilizers || []).map((u: any) => String(u.sourceSystemId)).filter((x) => x !== 'undefined' && x !== 'null')));
const isCopied = (f: any) => copiedIds.value.has(String(f.id));

const mk = (key: 'company' | 'system', title: string, hint: string, items: any[], theme: any) => ({
  key, title, hint, items, pending: items.filter((f) => !isCopied(f)), ...theme
});
const groups = computed(() => [
  mk('company', 'کودهای شرکتی', 'محصولات برندهای تجاری با مقادیر برگهٔ آزمایش', props.systemFertilizers.filter(isCompany), {
    border: 'border-teal-200 dark:border-teal-800', iconBg: 'bg-teal-100 dark:bg-teal-900/30', iconText: 'text-teal-600 dark:text-teal-400',
    btn: 'bg-teal-600 hover:bg-teal-700',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21h18M5 21V7l7-4 7 4v14M9 9h1m4 0h1M9 13h1m4 0h1M9 17h1m4 0h1" />'
  }),
  mk('system', 'کودهای سیستمی', 'کودهای استاندارد و پرکاربرد', props.systemFertilizers.filter((f) => !isCompany(f)), {
    border: 'border-indigo-200 dark:border-indigo-800', iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconText: 'text-indigo-600 dark:text-indigo-400',
    btn: 'bg-indigo-600 hover:bg-indigo-700',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3zm0 0v10c0 1.7 3.6 3 8 3s8-1.3 8-3V7M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" />'
  })
]);
const current = computed(() => groups.value.find((g) => g.key === open.value) || null);
const filtered = computed(() => {
  const t = q.value.trim().toLowerCase();
  const items = current.value?.items || [];
  return t ? items.filter((f: any) => `${f.name} ${f.brand || ''} ${f.category || ''}`.toLowerCase().includes(t)) : items;
});

const formLabel = (f?: string) => ({ liquid: 'مایع', powder: 'پودر', crystal: 'کریستال', granular: 'گرانول' } as Record<string, string>)[f || ''] || 'نامشخص';
const elementsOf = (f: any): Array<[string, number]> =>
  Object.entries(f.elements || {}).filter(([, v]) => Number(v) > 0).sort((a: any, b: any) => b[1] - a[1]).slice(0, 4) as any;

function copyGroup() {
  if (!current.value) return;
  emit('copy-many', current.value.pending.map((f: any) => String(f.id)));
}
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
