<!-- frontend/src/components/features/calc/ManualAmountsPanel.vue -->
<!--
  محاسبهٔ دستی: کاربر مقدار هر کودِ انتخاب‌شده را برای «کل مخزن» می‌نویسد.
  پیش‌نمایش زنده‌ی عناصر هدف همین‌جا نشان داده می‌شود؛ محاسبهٔ کامل (تعادل یونی، EC، رسوب، مخازن)
  پس از زدن «محاسبه» در بک‌اند انجام می‌شود.
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between gap-2">
      <div>
        <h3 class="text-sm font-semibold text-gray-900 dark:text-white">مقدار کودها (محاسبهٔ دستی)</h3>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5">مقدار هر کود برای کل مخزن {{ fmt(tankVolume) }} لیتری</p>
      </div>
      <span class="text-[11px] text-gray-500 tabular-nums">هزینهٔ کل: <strong class="text-gray-800 dark:text-gray-100">{{ fmt(totalCost) }}</strong></span>
    </div>

    <div v-if="fertilizers.length === 0" class="py-10 text-center text-sm text-gray-500 dark:text-gray-400">
      ابتدا از بخش بالا کودهایی را انتخاب کنید.
    </div>

    <ul v-else class="divide-y divide-gray-100 dark:divide-gray-700">
      <li v-for="f in fertilizers" :key="f.id" class="px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3">
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ f.name }}
            <span v-if="f.isAcid || f.isBase" class="mr-1 text-[10px] px-1.5 py-0.5 rounded" :class="f.isBase ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'">{{ f.isBase ? 'باز' : 'اسید' }}</span>
            <span v-if="f.form === 'liquid'" class="mr-1 text-[10px] px-1.5 py-0.5 rounded bg-cyan-50 text-cyan-700 dark:bg-cyan-900/20 dark:text-cyan-300">مایع</span>
          </p>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5 tabular-nums">
            <template v-for="(el, i) in mainElements(f)" :key="el.symbol">{{ i ? ' · ' : '' }}{{ el.symbol }} {{ el.value }}٪</template>
          </p>
        </div>

        <div class="flex items-center gap-2">
          <input
            :value="rowOf(f).amount ?? ''"
            @input="setAmount(f, ($event.target as HTMLInputElement).value)"
            inputmode="decimal"
            placeholder="مقدار"
            class="w-28 px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500"
          />
          <select :value="rowOf(f).unit" @change="setUnit(f, ($event.target as HTMLSelectElement).value as AmountUnit)"
            class="h-[38px] px-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100">
            <option v-for="u in unitOptions(f)" :key="u.value" :value="u.value">{{ u.label }}</option>
          </select>
          <button type="button" @click="openHelper(f)" class="w-9 h-9 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-500 hover:text-primary-600 hover:border-primary-400 flex items-center justify-center" title="کمک‌محاسبه: مقدار لازم برای رسیدن به ppm دلخواه">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
          </button>
        </div>
        <p v-if="rowError(f)" class="text-[11px] text-rose-600 dark:text-rose-400 sm:basis-full">{{ rowError(f) }}</p>
      </li>
    </ul>

    <!-- پیش‌نمایش زنده -->
    <div v-if="targetRows.length" class="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50/60 dark:bg-gray-900/30">
      <p class="text-[11px] font-semibold text-gray-500 dark:text-gray-400 mb-2">پیش‌نمایش عناصر هدف (با احتساب آب)</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
        <div v-for="row in targetRows" :key="row.symbol" class="flex items-center gap-2 text-xs">
          <span class="w-12 font-medium text-gray-700 dark:text-gray-200">{{ row.symbol }}</span>
          <div class="flex-1 h-1.5 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
            <div class="h-full rounded-full" :class="row.pct > 115 ? 'bg-rose-500' : row.pct >= 90 ? 'bg-emerald-500' : 'bg-amber-500'" :style="{ width: Math.min(row.pct, 100) + '%' }"></div>
          </div>
          <span class="w-28 text-left text-gray-600 dark:text-gray-300 tabular-nums">{{ fmt(row.supplied, 1) }} / {{ fmt(row.target, 1) }}</span>
        </div>
      </div>
    </div>

    <!-- مودال کمک‌محاسبه -->
    <Teleport to="body">
      <div v-if="helper.open" class="fixed inset-0 z-[70] flex items-end sm:items-center justify-center p-0 sm:p-4">
        <div class="absolute inset-0 bg-gray-900/50" @click="helper.open = false"></div>
        <div class="relative w-full sm:max-w-sm bg-white dark:bg-gray-800 rounded-t-2xl sm:rounded-2xl shadow-2xl p-5 space-y-4">
          <div>
            <h4 class="text-base font-bold text-gray-900 dark:text-white">کمک‌محاسبه</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">{{ helper.fertilizer?.name }}</p>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">عنصر</label>
              <select v-model="helper.element" class="w-full h-[38px] px-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100">
                <option v-for="el in helperElements" :key="el.symbol" :value="el.symbol">{{ el.symbol }} ({{ el.value }}٪)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">ppm دلخواه</label>
              <input v-model="helper.ppm" inputmode="decimal" class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-gray-100" />
            </div>
          </div>
          <p v-if="helperResult" class="text-sm text-gray-700 dark:text-gray-200 leading-7">
            برای رسیدن به <strong>{{ helper.ppm }}</strong> ppm از <strong>{{ helper.element }}</strong> در مخزن {{ fmt(tankVolume) }} لیتری:
            <strong class="block text-lg text-primary-700 dark:text-primary-300 tabular-nums">{{ helperResult }}</strong>
          </p>
          <div class="flex gap-2 justify-end">
            <button type="button" @click="helper.open = false" class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-sm text-gray-700 dark:text-gray-200">بستن</button>
            <button type="button" :disabled="!helperGrams" @click="applyHelper" class="px-4 py-2 rounded-lg bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white text-sm font-medium">استفاده از این مقدار</button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import {
  amountToGrams, canShowVolume, defaultUnit, formatFertilizerAmount, unitOptions, type AmountUnit
} from '@/utils/fertilizerUnits';

type Row = { amount: number | null; unit: AmountUnit };

const props = defineProps<{
  fertilizers: any[];
  amounts: Record<string, Row>;
  fixedAmounts: Record<string, { amount: number; unit: AmountUnit }>;
  tankVolume: number;
  targets: Record<string, number>;
  water: Record<string, number>;
}>();
const emit = defineEmits<{ (e: 'update:amounts', v: Record<string, Row>): void }>();

const fmt = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d }).format(n);
const parse = (t: string): number | null => {
  const n = Number(t.replace(/[۰-۹]/g, (c) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(c))).replace(/٫/g, '.').replace(/,/g, '').trim());
  return Number.isFinite(n) && t.trim() !== '' ? n : null;
};

// مقدار اولیه: اگر برای اسید/باز مقدار ثابت داده شده همان را بگذار
watch(
  () => props.fertilizers.map((f) => f.id).join(','),
  () => {
    const next = { ...props.amounts };
    let changed = false;
    for (const f of props.fertilizers) {
      if (!next[f.id]) {
        const fx = props.fixedAmounts[f.id];
        next[f.id] = fx ? { amount: fx.amount, unit: fx.unit } : { amount: null, unit: defaultUnit(f) };
        changed = true;
      }
    }
    if (changed) emit('update:amounts', next);
  },
  { immediate: true }
);

const rowOf = (f: any): Row => props.amounts[f.id] || { amount: null, unit: defaultUnit(f) };
const setAmount = (f: any, text: string) =>
  emit('update:amounts', { ...props.amounts, [f.id]: { ...rowOf(f), amount: text.trim() === '' ? null : parse(text) } });
const setUnit = (f: any, unit: AmountUnit) =>
  emit('update:amounts', { ...props.amounts, [f.id]: { ...rowOf(f), unit } });

const gramsOf = (f: any): number => {
  const r = rowOf(f);
  if (!r.amount || r.amount <= 0) return 0;
  return amountToGrams(r.amount, r.unit, f.densityGMl) ?? 0;
};
const rowError = (f: any): string => {
  const r = rowOf(f);
  if (r.amount != null && r.amount < 0) return 'مقدار نمی‌تواند منفی باشد';
  if (r.amount && (r.unit === 'ml' || r.unit === 'l') && !canShowVolume(f)) return 'برای مصرف حجمی چگالی کود باید ثبت شود';
  return '';
};

const mainElements = (f: any) =>
  Object.entries(f.elements || {})
    .filter(([, v]) => Number(v) > 0)
    .map(([symbol, v]) => ({ symbol, value: Number(v) }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);

const totalCost = computed(() =>
  props.fertilizers.reduce((s, f) => s + (gramsOf(f) / 1000) * (f.pricePerKg || 0), 0)
);

const suppliedPpm = computed(() => {
  const out: Record<string, number> = { ...props.water };
  for (const f of props.fertilizers) {
    const g = gramsOf(f);
    if (g <= 0 || !(props.tankVolume > 0)) continue;
    for (const [el, pct] of Object.entries<any>(f.elements || {})) {
      if (Number(pct) > 0) out[el] = (out[el] || 0) + (g * (Number(pct) / 100) * ((f.concentration || 100) / 100) * 1000) / props.tankVolume;
    }
  }
  return out;
});

const targetRows = computed(() =>
  Object.entries(props.targets || {})
    .filter(([, t]) => Number(t) > 0)
    .map(([symbol, t]) => {
      const supplied = suppliedPpm.value[symbol] || 0;
      return { symbol, target: Number(t), supplied, pct: (supplied / Number(t)) * 100 };
    })
);

// ----- کمک‌محاسبه -----
const helper = reactive<{ open: boolean; fertilizer: any | null; element: string; ppm: string }>({
  open: false, fertilizer: null, element: '', ppm: ''
});
const helperElements = computed(() => (helper.fertilizer ? mainElements({ elements: helper.fertilizer.elements }) : []));
const openHelper = (f: any) => {
  helper.fertilizer = f;
  helper.element = mainElements(f)[0]?.symbol || '';
  const t = props.targets?.[helper.element];
  helper.ppm = t ? String(Math.round(t)) : '';
  helper.open = true;
};
const helperGrams = computed(() => {
  const f = helper.fertilizer;
  const ppm = parse(helper.ppm);
  if (!f || !ppm || ppm <= 0 || !helper.element) return 0;
  const pct = Number(f.elements?.[helper.element] || 0);
  if (pct <= 0) return 0;
  return (ppm * props.tankVolume) / (1000 * (pct / 100) * ((f.concentration || 100) / 100));
});
const helperResult = computed(() => (helperGrams.value ? formatFertilizerAmount(helperGrams.value, helper.fertilizer, true) : ''));
const applyHelper = () => {
  const f = helper.fertilizer;
  if (!f || !helperGrams.value) return;
  const useVolume = canShowVolume(f);
  const amount = useVolume ? helperGrams.value / f.densityGMl : helperGrams.value;
  emit('update:amounts', {
    ...props.amounts,
    [f.id]: { amount: Math.round(amount * 100) / 100, unit: useVolume ? 'ml' : 'g' }
  });
  helper.open = false;
};
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
