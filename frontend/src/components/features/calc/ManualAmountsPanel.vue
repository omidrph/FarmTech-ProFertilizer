
<!-- frontend/src/components/features/calc/ManualAmountsPanel.vue -->
<!--
  محاسبهٔ دستی: مقدار هر کودِ انتخاب‌شده را برای «کل مخزن» می‌نویسید.
  طراحی: جستجو + فیلتر «فقط پرشده‌ها»، هر کود یک کارت فشرده با ورودی و واحد (انتخاب کپسولی)،
  و پیش‌نمایش زندهٔ پوشش عناصر هدف (با احتساب آب).
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- سربرگ -->
    <header class="px-4 sm:px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3 flex-wrap">
      <span class="w-9 h-9 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
      </span>
      <div class="min-w-0 flex-1">
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">مقدار کودها (محاسبهٔ دستی)</h3>
        <p class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400">مقدار هر کود را برای کل مخزن {{ fmt(tankVolume) }} لیتری بنویسید</p>
      </div>
      <div class="flex items-center gap-2 text-[11px] tabular-nums">
        <span class="px-2.5 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">پرشده: <strong>{{ filledCount }}</strong> از {{ fertilizers.length }}</span>
        <span class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300">هزینه: <strong>{{ fmt(totalCost) }}</strong> تومان</span>
      </div>
    </header>

    <div v-if="fertilizers.length === 0" class="py-12 px-6 text-center">
      <p class="text-sm text-gray-600 dark:text-gray-300">هنوز کودی انتخاب نشده است.</p>
      <p class="text-xs text-gray-400 mt-1">از لیست بالا کودهای مورد نظرتان را اضافه کنید تا اینجا مقدار بنویسید.</p>
    </div>

    <template v-else>
      <!-- ابزار -->
      <div class="px-4 sm:px-5 py-3 flex items-center gap-2 border-b border-gray-100 dark:border-gray-700">
        <div class="relative flex-1">
          <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" /></svg>
          <input v-model="q" placeholder="جستجو: نام، فرمول یا عنصر" class="w-full h-9 pr-9 pl-3 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-primary-500" />
        </div>
        <button type="button" @click="onlyFilled = !onlyFilled" class="h-9 px-3 rounded-lg border text-xs font-medium transition-colors flex-shrink-0"
          :class="onlyFilled ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'">فقط پرشده‌ها</button>
        <button type="button" v-if="filledCount" @click="clearAll" class="h-9 px-3 rounded-lg border border-gray-200 dark:border-gray-600 text-xs font-medium text-gray-600 dark:text-gray-300 hover:text-rose-600 hover:border-rose-300 flex-shrink-0">پاک‌کردن</button>
      </div>

      <!-- کارت‌های کود -->
      <ul class="p-3 sm:p-4 grid grid-cols-1 xl:grid-cols-2 gap-2.5">
        <li v-for="f in visible" :key="f.id" class="rounded-xl border p-3 transition-colors"
          :class="gramsOf(f) > 0 ? 'border-primary-300 dark:border-primary-700 bg-primary-50/40 dark:bg-primary-900/10' : 'border-gray-200 dark:border-gray-700'">
          <div class="flex items-start gap-2">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-semibold text-gray-900 dark:text-white flex flex-wrap items-center gap-1.5">
                <span class="truncate">{{ f.name }}</span>
                <span v-if="f.isAcid || f.isBase" class="text-[10px] px-1.5 py-0.5 rounded" :class="f.isBase ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'">{{ f.isBase ? 'باز' : 'اسید' }}</span>
                <span v-if="isCompany(f)" class="text-[10px] px-1.5 py-0.5 rounded bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300">{{ f.brand }}</span>
                <span v-if="f.form === 'liquid'" class="text-[10px] px-1.5 py-0.5 rounded bg-cyan-50 text-cyan-700 dark:bg-cyan-900/20 dark:text-cyan-300">مایع</span>
              </p>
              <p v-if="f.formula" class="mt-0.5 text-[11px] text-gray-500 dark:text-gray-400" dir="ltr" style="text-align:right">{{ f.formula }}</p>
              <p class="mt-1 flex flex-wrap gap-1">
                <span v-for="el in mainElements(f)" :key="el.symbol" class="text-[10px] px-1.5 py-0.5 rounded border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 tabular-nums">{{ el.symbol }} {{ el.value }}٪</span>
              </p>
            </div>
            <button type="button" @click="openHelper(f)" class="w-8 h-8 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-400 hover:text-primary-600 hover:border-primary-400 flex items-center justify-center flex-shrink-0" title="کمک‌محاسبه: مقدار لازم برای رسیدن به ppm دلخواه">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
            </button>
          </div>

          <div class="mt-2.5 flex items-center gap-2">
            <div class="relative flex-1">
              <input :value="rowOf(f).amount ?? ''" @input="setAmount(f, ($event.target as HTMLInputElement).value)" inputmode="decimal" dir="ltr" placeholder="0"
                class="w-full h-10 px-3 text-center tabular-nums text-sm font-semibold rounded-lg border bg-white dark:bg-gray-900 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
                :class="rowError(f) ? 'border-rose-400' : 'border-gray-200 dark:border-gray-600'" />
            </div>
            <div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-600 overflow-hidden flex-shrink-0">
              <button v-for="u in unitOptions(f)" :key="u.value" type="button" @click="setUnit(f, u.value)"
                class="h-10 px-2.5 text-[11px] font-medium transition-colors"
                :class="rowOf(f).unit === u.value ? 'bg-primary-600 text-white' : 'bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'">{{ u.label }}</button>
            </div>
          </div>
          <p v-if="rowError(f)" class="mt-1 text-[11px] text-rose-600 dark:text-rose-400">{{ rowError(f) }}</p>
          <p v-else-if="gramsOf(f) > 0" class="mt-1 text-[11px] text-gray-500 dark:text-gray-400 tabular-nums">
            معادل {{ fmt(gramsOf(f), 1) }} گرم · هزینه {{ fmt((gramsOf(f) / 1000) * (f.pricePerKg || 0)) }} تومان
          </p>
        </li>
        <li v-if="!visible.length" class="col-span-full py-8 text-center text-sm text-gray-500">موردی یافت نشد.</li>
      </ul>

      <!-- پیش‌نمایش زنده: ماکرو و میکرو جدا، رنگ سه‌سطحی (۵٪ / ۱۰٪) -->
      <div v-if="targetRows.length" class="px-4 sm:px-5 py-3.5 border-t border-gray-100 dark:border-gray-700 bg-gray-50/70 dark:bg-gray-900/30 space-y-3">
        <p class="text-xs font-semibold text-gray-600 dark:text-gray-300">پیش‌نمایش زندهٔ پوشش عناصر هدف (با احتساب آب)</p>
        <div v-for="g in previewGroups" :key="g.group">
          <div v-if="g.count" class="mb-2 flex items-center justify-between gap-2 rounded-lg border px-3 py-1.5 text-[11px]" :class="[LEVEL_CLASS[g.level].bg, LEVEL_CLASS[g.level].border]">
            <span class="font-bold text-gray-800 dark:text-gray-100">{{ GROUP_TITLES[g.group] }}</span>
            <span class="tabular-nums" :class="LEVEL_CLASS[g.level].text">
              میانگین خطا {{ faNum(g.meanAbs, 1) }}٪ · {{ LEVEL_LABEL[g.level] }}
            </span>
          </div>
          <div v-if="g.count" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
            <div v-for="row in g.rows" :key="row.element" class="rounded-lg bg-white dark:bg-gray-800 border px-2.5 py-2" :class="LEVEL_CLASS[row.level].border">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-bold text-gray-700 dark:text-gray-200">{{ row.element }}</span>
                <span class="tabular-nums" :class="LEVEL_CLASS[row.level].text">{{ faNum(row.absPct, 1) }}٪ {{ row.deviationPct >= 0 ? 'بیش' : 'کم' }}</span>
              </div>
              <div class="mt-1.5 h-1.5 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
                <div class="h-full rounded-full" :class="LEVEL_CLASS[row.level].dot" :style="{ width: Math.min((row.actual / row.target) * 100, 100) + '%' }"></div>
              </div>
              <p class="mt-1 text-[10px] text-gray-400 tabular-nums">{{ fmt(row.actual, 1) }} / {{ fmt(row.target, 1) }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- مودال کمک‌محاسبه -->
    <Teleport to="body">
      <div v-if="helper.open" class="fixed inset-0 z-[70] flex items-end sm:items-center justify-center p-0 sm:p-4">
        <div class="absolute inset-0 bg-gray-900/50 backdrop-blur-[2px]" @click="helper.open = false"></div>
        <div class="relative w-full sm:max-w-sm bg-white dark:bg-gray-800 rounded-t-2xl sm:rounded-2xl shadow-2xl p-5 space-y-4">
          <div><h4 class="text-base font-bold text-gray-900 dark:text-white">کمک‌محاسبه</h4><p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 truncate">{{ helper.fertilizer?.name }}</p></div>
          <div class="grid grid-cols-2 gap-2">
            <div><label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">عنصر</label>
              <select v-model="helper.element" class="w-full h-10 px-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100"><option v-for="el in helperElements" :key="el.symbol" :value="el.symbol">{{ el.symbol }} ({{ el.value }}٪)</option></select></div>
            <div><label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">ppm دلخواه</label>
              <input v-model="helper.ppm" inputmode="decimal" class="w-full h-10 px-3 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-gray-100" /></div>
          </div>
          <p v-if="helperResult" class="text-sm text-gray-700 dark:text-gray-200 leading-7">برای رسیدن به <strong>{{ helper.ppm }}</strong> ppm از <strong>{{ helper.element }}</strong> در {{ fmt(tankVolume) }} لیتر:
            <strong class="block text-lg text-primary-700 dark:text-primary-300 tabular-nums">{{ helperResult }}</strong></p>
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
import { computed, reactive, ref, watch } from 'vue';
import { computeGroupErrors, faNum, GROUP_TITLES, LEVEL_CLASS, LEVEL_LABEL } from '@/utils/errorLevels';
import { amountToGrams, canShowVolume, defaultUnit, formatFertilizerAmount, unitOptions, type AmountUnit } from '@/utils/fertilizerUnits';

type Row = { amount: number | null; unit: AmountUnit };
const props = defineProps<{
  fertilizers: any[]; amounts: Record<string, Row>;
  fixedAmounts: Record<string, { amount: number; unit: AmountUnit }>;
  tankVolume: number; targets: Record<string, number>; water: Record<string, number>;
}>();
const emit = defineEmits<{ (e: 'update:amounts', v: Record<string, Row>): void }>();

const fmt = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d }).format(n);
const parse = (t: string): number | null => {
  const n = Number(t.replace(/[۰-۹]/g, (c) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(c))).replace(/٫/g, '.').replace(/,/g, '').trim());
  return Number.isFinite(n) && t.trim() !== '' ? n : null;
};
const isCompany = (f: any) => !!f.brand && f.brand.trim() !== '' && f.brand.trim() !== 'استاندارد';

watch(() => props.fertilizers.map((f) => f.id).join(','), () => {
  const next = { ...props.amounts }; let changed = false;
  for (const f of props.fertilizers) if (!next[f.id]) {
    const fx = props.fixedAmounts[f.id];
    next[f.id] = fx ? { amount: fx.amount, unit: fx.unit } : { amount: null, unit: defaultUnit(f) }; changed = true;
  }
  if (changed) emit('update:amounts', next);
}, { immediate: true });

const EL_FA: Record<string, string> = { 'N-NO3': 'نیترات نیتروژن', 'N-NH4': 'آمونیوم نیتروژن', P: 'فسفر فسفات', K: 'پتاسیم', Ca: 'کلسیم', Mg: 'منیزیم', S: 'گوگرد سولفات', Na: 'سدیم', Cl: 'کلر', Fe: 'آهن', Mn: 'منگنز', Zn: 'روی', B: 'بور', Cu: 'مس', Mo: 'مولیبدن', Si: 'سیلیسیم' };
const matchQ = (f: any): boolean => {
  const tokens = q.value.toLowerCase().split(/\s+/).filter(Boolean);
  if (!tokens.length) return true;
  const els = Object.entries(f.elements || {}).filter(([, v]) => Number(v) > 0).map(([k]) => `${k} ${EL_FA[k] || ''}`).join(' ');
  const hay = `${f.name} ${f.brand || ''} ${f.formula || ''} ${els} ${f.isAcid ? 'اسید' : ''} ${f.isBase ? 'باز' : ''} ${f.form === 'liquid' ? 'مایع' : ''}`.toLowerCase();
  return tokens.every((t) => hay.includes(t));
};
const q = ref(''); const onlyFilled = ref(false);
const rowOf = (f: any): Row => props.amounts[f.id] || { amount: null, unit: defaultUnit(f) };
const setAmount = (f: any, text: string) => emit('update:amounts', { ...props.amounts, [f.id]: { ...rowOf(f), amount: text.trim() === '' ? null : parse(text) } });
const setUnit = (f: any, unit: AmountUnit) => emit('update:amounts', { ...props.amounts, [f.id]: { ...rowOf(f), unit } });
const gramsOf = (f: any): number => { const r = rowOf(f); return r.amount && r.amount > 0 ? amountToGrams(r.amount, r.unit, f.densityGMl) ?? 0 : 0; };
const rowError = (f: any): string => {
  const r = rowOf(f);
  if (r.amount != null && r.amount < 0) return 'مقدار نمی‌تواند منفی باشد';
  if (r.amount && (r.unit === 'ml' || r.unit === 'l') && !canShowVolume(f)) return 'برای مصرف حجمی، چگالی کود باید ثبت شود';
  return '';
};
const filledCount = computed(() => props.fertilizers.filter((f) => gramsOf(f) > 0).length);
const visible = computed(() => props.fertilizers.filter((f) => (!onlyFilled.value || gramsOf(f) > 0) && (!q.value.trim() || matchQ(f))));
const clearAll = () => emit('update:amounts', Object.fromEntries(props.fertilizers.map((f) => [f.id, { amount: null, unit: defaultUnit(f) }])));

const mainElements = (f: any) => Object.entries(f.elements || {}).filter(([, v]) => Number(v) > 0).map(([symbol, v]) => ({ symbol, value: Math.round(Number(v) * 100) / 100 })).sort((a, b) => b.value - a.value).slice(0, 4);
const totalCost = computed(() => props.fertilizers.reduce((s, f) => s + (gramsOf(f) / 1000) * (f.pricePerKg || 0), 0));
const suppliedPpm = computed(() => {
  const out: Record<string, number> = { ...props.water };
  for (const f of props.fertilizers) { const g = gramsOf(f); if (g <= 0 || !(props.tankVolume > 0)) continue;
    for (const [el, pct] of Object.entries<any>(f.elements || {})) if (Number(pct) > 0) out[el] = (out[el] || 0) + (g * (Number(pct) / 100) * ((f.concentration || 100) / 100) * 1000) / props.tankVolume; }
  return out;
});
const previewGroups = computed(() => { const g = computeGroupErrors(props.targets || {}, suppliedPpm.value); return [g.macro, g.micro]; });
const targetRows = computed(() => Object.entries(props.targets || {}).filter(([, t]) => Number(t) > 0).map(([symbol, t]) => { const supplied = suppliedPpm.value[symbol] || 0; return { symbol, target: Number(t), supplied, pct: (supplied / Number(t)) * 100 }; }));

// ----- کمک‌محاسبه -----
const helper = reactive<{ open: boolean; fertilizer: any | null; element: string; ppm: string }>({ open: false, fertilizer: null, element: '', ppm: '' });
const helperElements = computed(() => (helper.fertilizer ? mainElements({ elements: helper.fertilizer.elements }) : []));
const openHelper = (f: any) => { helper.fertilizer = f; helper.element = mainElements(f)[0]?.symbol || ''; const t = props.targets?.[helper.element]; helper.ppm = t ? String(Math.round(t)) : ''; helper.open = true; };
const helperGrams = computed(() => {
  const f = helper.fertilizer; const ppm = parse(helper.ppm);
  if (!f || !ppm || ppm <= 0 || !helper.element) return 0;
  const pct = Number(f.elements?.[helper.element] || 0);
  return pct <= 0 ? 0 : (ppm * props.tankVolume) / (1000 * (pct / 100) * ((f.concentration || 100) / 100));
});
const helperResult = computed(() => (helperGrams.value ? formatFertilizerAmount(helperGrams.value, helper.fertilizer, true) : ''));
const applyHelper = () => {
  const f = helper.fertilizer; if (!f || !helperGrams.value) return;
  const vol = canShowVolume(f); const amount = vol ? helperGrams.value / f.densityGMl : helperGrams.value;
  emit('update:amounts', { ...props.amounts, [f.id]: { amount: Math.round(amount * 100) / 100, unit: vol ? 'ml' : 'g' } });
  helper.open = false;
};
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
