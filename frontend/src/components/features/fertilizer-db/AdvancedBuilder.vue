<!-- frontend/src/components/features/fertilizer-db/AdvancedBuilder.vue -->
<!--
  حالت «پیشرفته»: هر ترکیب و هر تعداد جزء را آزادانه بنویسید؛ برنامه خودش عنصرهای اصلی را بیرون می‌کشد.
  هر ردیف = «فرمول شیمیایی» + «درصد وزنیِ آن جزء در محصول»
  مثال‌ها:  KNO3 ۵۰٪  +  Ca(NO3)2·4H2O ۳۰٪   |   K2O ۲۰٪ (فرم اکسیدی)   |   (NH4)2SO4 ۱۰۰٪
  نتیجه (درصد عنصر خالص) با یک دکمه در جدول عناصر ثبت می‌شود.
-->
<template>
  <div class="rounded-xl border border-teal-200 dark:border-teal-800/50 bg-teal-50/50 dark:bg-teal-900/10 p-3 space-y-3">
    <div>
      <p class="text-sm font-semibold text-teal-800 dark:text-teal-300">حالت پیشرفته — ساخت ترکیب دلخواه</p>
      <p class="text-[11px] leading-5 text-gray-600 dark:text-gray-400 mt-0.5">
        فرمول هر جزء را بنویسید و بگویید چند درصد از محصول است؛ هر تعداد ردیف مجاز است. پرانتز، آب تبلور (<span dir="ltr">·4H₂O</span>)، اکسیدها (<span dir="ltr">P2O5، K2O</span>) و یون‌ها (<span dir="ltr">NO3⁻</span>) پشتیبانی می‌شوند.
      </p>
    </div>

    <!-- ردیف‌ها -->
    <div class="space-y-2">
      <div v-for="(r, i) in rows" :key="r.id" class="rounded-xl bg-white dark:bg-gray-800 border p-2.5 space-y-1.5"
        :class="states[i].error ? 'border-danger-300 dark:border-danger-700' : 'border-gray-200 dark:border-gray-700'">
        <div class="flex items-center gap-2">
          <span class="w-6 text-center text-[11px] text-gray-400 tabular-nums">{{ (i + 1).toLocaleString('fa-IR') }}</span>
          <input v-model="r.formula" dir="ltr" placeholder="مثلاً Ca(NO3)2·4H2O" spellcheck="false"
            class="flex-1 min-w-0 h-9 px-2.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 font-mono" />
          <div class="flex items-center gap-1 flex-shrink-0">
            <input v-model.number="r.amount" type="number" min="0" max="100" step="0.01" dir="ltr" placeholder="۰"
              class="w-20 h-9 px-2 text-sm text-center rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 font-semibold" />
            <span class="text-xs text-gray-500">٪</span>
          </div>
          <button type="button" @click="rows.splice(i, 1)" class="p-1.5 rounded-lg text-gray-400 hover:text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20" title="حذف ردیف">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <!-- وضعیت تحلیل -->
        <p v-if="states[i].error" class="pr-8 text-[11px] text-danger-600 dark:text-danger-400">{{ states[i].error }}</p>
        <div v-else-if="states[i].analysis" class="pr-8 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-gray-500 dark:text-gray-400">
          <span>جرم مولی <b class="tabular-nums text-gray-700 dark:text-gray-200">{{ states[i].analysis.mass.toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}</b></span>
          <span v-for="(v, k) in states[i].analysis.elements" :key="k" class="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 tabular-nums">{{ symbol(String(k)) }} <span dir="ltr">{{ (v * 100).toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪</span></span>
          <label v-if="states[i].analysis.genericN" class="flex items-center gap-1.5">
            نیتروژن غیرنیترات/آمونیوم را ثبت کن به‌عنوان
            <select v-model="r.genericN" class="h-6 px-1 text-[11px] rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700">
              <option value="N-NH4">آمونیومی</option><option value="N-NO3">نیتراتی</option>
            </select>
          </label>
          <span v-for="(v, k) in states[i].analysis.untracked" :key="'u' + k" class="text-amber-600 dark:text-amber-400"><span dir="ltr">{{ k }} {{ (v * 100).toLocaleString('fa-IR', { maximumFractionDigits: 1 }) }}٪</span> (در محاسبات دنبال نمی‌شود)</span>
        </div>
      </div>
    </div>

    <!-- افزودن -->
    <div class="flex flex-wrap items-center gap-2">
      <button type="button" @click="addRow()" class="h-9 px-3 rounded-lg text-sm font-medium bg-teal-600 text-white hover:bg-teal-700">+ ردیف خالی</button>
      <select v-model="quick" @change="addQuick" class="h-9 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
        <option value="">افزودن سریع از ترکیب‌های رایج…</option>
        <optgroup v-for="g in QUICK" :key="g.title" :label="g.title">
          <option v-for="c in g.items" :key="c.f" :value="c.f">{{ c.n }} — {{ c.f }}</option>
        </optgroup>
      </select>
    </div>

    <!-- نتیجه -->
    <div v-if="hasResult" class="rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-3 space-y-2">
      <div class="flex items-center justify-between gap-2 flex-wrap">
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-100">عنصرهای استخراج‌شده (درصد عنصر خالص در محصول)</p>
        <p class="text-[11px] tabular-nums" :class="amountSum > 100.0001 ? 'text-danger-600 font-semibold' : 'text-gray-500 dark:text-gray-400'">
          مجموع اجزا: {{ amountSum.toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪ از محصول
          <template v-if="amountSum <= 100.0001 && amountSum > 0"> · باقی‌مانده (حامل/ناخالصی): {{ (100 - amountSum).toLocaleString('fa-IR', { maximumFractionDigits: 2 }) }}٪</template>
        </p>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5">
        <div v-for="e in resultList" :key="e.key" class="flex items-center justify-between gap-2 rounded-lg px-2.5 py-1.5 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/50">
          <span class="text-xs text-gray-700 dark:text-gray-200">{{ e.name }}</span>
          <b class="text-sm tabular-nums text-emerald-700 dark:text-emerald-300" dir="ltr">{{ e.pct.toLocaleString('fa-IR', { maximumFractionDigits: 4 }) }}%</b>
        </div>
      </div>
      <p v-if="amountSum > 100.0001" class="text-[11px] text-danger-600 dark:text-danger-400">مجموع اجزا از ۱۰۰٪ بیشتر است؛ مقدارها را بررسی کنید.</p>
      <div class="flex flex-wrap items-center gap-2 pt-1">
        <button type="button" :disabled="!canApply" @click="apply" class="h-9 px-4 rounded-lg text-sm font-semibold bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-40 disabled:cursor-not-allowed">
          اعمال روی جدول عناصر
        </button>
        <button type="button" @click="rows.splice(0)" class="h-9 px-3 rounded-lg text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700">پاک کردن ردیف‌ها</button>
      </div>
      <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">با اعمال، مقدار فعلی جدول عناصر جایگزین می‌شود (به‌صورت عنصر خالص) و می‌توانید بعداً دستی ویرایش کنید.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { analyse, FormulaError, parseFormula, type Analysis } from '@/utils/chemFormula';
import { ELEMENT_DEFS, getElementDef, prettyFormula } from '@/utils/labelForms';

const props = defineProps<{ entries: Record<string, { form: string; value: number | null }> }>();
const emit = defineEmits<{ (e: 'applied', info: { formula: string | null }): void }>();

interface Row { id: number; formula: string; amount: number | null; genericN: 'N-NH4' | 'N-NO3' }
let seq = 0;
const rows = reactive<Row[]>([]);
const quick = ref('');

const QUICK = [
  { title: 'نیتروژن', items: [
    { n: 'نیترات پتاسیم', f: 'KNO3' }, { n: 'نیترات کلسیم ۴آبه', f: 'Ca(NO3)2·4H2O' }, { n: 'نیترات منیزیم', f: 'Mg(NO3)2·6H2O' },
    { n: 'نیترات آمونیوم', f: 'NH4NO3' }, { n: 'سولفات آمونیوم', f: '(NH4)2SO4' }, { n: 'اوره', f: 'CO(NH2)2' }] },
  { title: 'فسفر و پتاسیم', items: [
    { n: 'مونوپتاسیم فسفات', f: 'KH2PO4' }, { n: 'مونوآمونیوم فسفات', f: 'NH4H2PO4' }, { n: 'اسید فسفریک', f: 'H3PO4' },
    { n: 'سولفات پتاسیم', f: 'K2SO4' }, { n: 'کلرید پتاسیم', f: 'KCl' }, { n: 'پنتااکسید فسفر (P₂O₅)', f: 'P2O5' }, { n: 'اکسید پتاسیم (K₂O)', f: 'K2O' }] },
  { title: 'کلسیم، منیزیم و گوگرد', items: [
    { n: 'سولفات منیزیم ۷آبه', f: 'MgSO4·7H2O' }, { n: 'گچ', f: 'CaSO4·2H2O' }, { n: 'اکسید منیزیم', f: 'MgO' }, { n: 'اکسید کلسیم', f: 'CaO' }, { n: 'اسید سولفوریک', f: 'H2SO4' }] },
  { title: 'ریزمغذی‌ها', items: [
    { n: 'سولفات آهن ۷آبه', f: 'FeSO4·7H2O' }, { n: 'سولفات منگنز یک‌آبه', f: 'MnSO4·H2O' }, { n: 'سولفات روی ۷آبه', f: 'ZnSO4·7H2O' },
    { n: 'سولفات مس ۵آبه', f: 'CuSO4·5H2O' }, { n: 'اسید بوریک', f: 'H3BO3' }, { n: 'سولوبور', f: 'Na2B8O13·4H2O' }, { n: 'مولیبدات سدیم ۲آبه', f: 'Na2MoO4·2H2O' }] },
];

const addRow = (formula = '') => { rows.push({ id: ++seq, formula, amount: null, genericN: 'N-NH4' }); };
const addQuick = () => { if (quick.value) addRow(quick.value); quick.value = ''; };
addRow();

// تحلیل هر ردیف (واکنشی)
const states = computed(() =>
  rows.map((r) => {
    if (!r.formula.trim()) return { analysis: null as Analysis | null, error: '' };
    try { return { analysis: analyse(parseFormula(r.formula), r.genericN), error: '' }; }
    catch (e) { return { analysis: null, error: e instanceof FormulaError ? e.message : 'فرمول معتبر نیست' }; }
  })
);
const amountSum = computed(() => rows.reduce((s, r, i) => s + (states.value[i].analysis ? Number(r.amount) || 0 : 0), 0));
const totals = computed<Record<string, number>>(() => {
  const t: Record<string, number> = {};
  rows.forEach((r, i) => {
    const a = states.value[i].analysis;
    const amt = Number(r.amount) || 0;
    if (!a || !(amt > 0)) return;
    for (const [k, frac] of Object.entries(a.elements)) t[k] = (t[k] || 0) + amt * frac;
  });
  return t;
});
const resultList = computed(() =>
  ELEMENT_DEFS.filter((d) => (totals.value[d.key] || 0) > 0.00005)
    .map((d) => ({ key: d.key, name: d.name, pct: Math.round(totals.value[d.key] * 10000) / 10000 }))
);
const hasResult = computed(() => resultList.value.length > 0);
const canApply = computed(() => hasResult.value && amountSum.value <= 100.0001 && resultList.value.every((e) => e.pct <= 100));
const symbol = (k: string) => (k === 'N-NO3' ? 'N نیترات' : k === 'N-NH4' ? 'N آمونیوم' : getElementDef(k)?.symbol || k);

const apply = () => {
  const filled = ELEMENT_DEFS.some((d) => Number(props.entries[d.key]?.value) > 0);
  if (filled && !confirm('مقدار فعلی جدول عناصر با نتیجهٔ این ترکیب جایگزین شود؟')) return;
  for (const d of ELEMENT_DEFS) props.entries[d.key] = { form: d.key.startsWith('N-') ? 'N' : d.key, value: null };
  for (const e of resultList.value) {
    const d = getElementDef(e.key)!;
    props.entries[e.key] = { form: d.key.startsWith('N-') ? 'N' : d.key, value: e.pct };
  }
  // اگر فقط یک جزء با ۱۰۰٪ بود، فرمول همان جزء را برای فیلد «فرمول» پیشنهاد بده
  const used = rows.filter((r, i) => states.value[i].analysis && Number(r.amount) > 0);
  emit('applied', { formula: used.length === 1 ? prettyFormula(used[0].formula.replace(/[·.]/g, '·')) : null });
};

</script>

<style scoped>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; appearance: textfield; }
input:focus, select:focus { outline: none; }
</style>
