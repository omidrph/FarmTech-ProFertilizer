<!-- frontend/src/components/features/widgets/PhCalculatorWidget.vue -->
<!--
  ابزارک «ماشین حساب PH»
  ------------------------------------------------------------
  دو مسیر (مطابق گزارش فنی اصلاح‌شده – نسخه ۳٫۰):
    ۱) مدل تئوریک سیستم کربنات (فقط آب ساده)
    ۲) تیتراسیون واقعی نمونه (پیشنهادی برای محلول‌های غذایی/ترکیبی)
  هیچ جدول عمومی «pH هدف → آلکالینیتی» استفاده نمی‌شود.
  منطق محاسبه در ph/phDose.ts و ph/phChemistry.ts است.
-->
<template>
  <div class="space-y-5 sm:space-y-6">

    <!-- ===================== انتخاب روش ===================== -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
      <button
        v-for="m in methods"
        :key="m.id"
        type="button"
        @click="method = m.id"
        class="text-right rounded-xl border-2 px-4 py-3 transition-colors"
        :class="method === m.id
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
        :aria-pressed="method === m.id"
      >
        <span class="flex items-center justify-between gap-2">
          <span class="text-sm font-bold" :class="method === m.id ? 'text-primary-700 dark:text-primary-300' : 'text-gray-900 dark:text-white'">{{ m.title }}</span>
          <span
            v-if="m.badge"
            class="text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300"
          >{{ m.badge }}</span>
        </span>
        <span class="block mt-1 text-xs text-gray-500 dark:text-gray-400 leading-5">{{ m.subtitle }}</span>
      </button>
    </div>

    <!-- راهنمای روش -->
    <div
      v-if="method === 'theoretical'"
      class="rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3 text-xs sm:text-sm text-amber-900 dark:text-amber-200 leading-6"
    >
      این مدل فقط برای آب یا محلولی است که ظرفیت اسیدی/بازی آن عمدتاً از کربنات و بی‌کربنات می‌آید. برای محلول غذایی (فسفات، آمونیوم، اسیدهای آلی) از «تیتراسیون واقعی» استفاده کنید.
    </div>
    <div
      v-else
      class="rounded-xl border border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/20 px-4 py-3 text-xs sm:text-sm text-primary-900 dark:text-primary-200 leading-6"
    >
      از محلول واقعی نمونه‌ای با حجم مشخص بگیرید، {{ direction === 'base' ? 'باز' : 'اسید' }} استاندارد را مرحله‌ای اضافه کنید و پس از اختلاط، pH هر مرحله را ثبت کنید. دوز از منحنی همان نمونه به‌دست می‌آید.
    </div>

    <!-- ===================== مشخصات محلول ===================== -->
    <section>
      <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">مشخصات محلول</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <div>
          <label for="ph-volume" class="field-label">حجم محلول</label>
          <div class="flex gap-2">
            <input id="ph-volume" v-model="form.volume" type="text" inputmode="decimal" placeholder="مثلاً ۱۰۰۰" class="field-input flex-1 min-w-0" :class="bad(form.volume) && 'field-invalid'" />
            <select v-model="form.volumeUnit" class="field-input !w-24 flex-shrink-0" aria-label="واحد حجم">
              <option value="L">لیتر</option>
              <option value="m3">متر مکعب</option>
            </select>
          </div>
        </div>
        <div>
          <label for="ph-current" class="field-label">pH فعلی</label>
          <input id="ph-current" v-model="form.currentPH" type="text" inputmode="decimal" placeholder="مثلاً ۸٫۲" class="field-input" :class="bad(form.currentPH) && 'field-invalid'" />
        </div>
        <div>
          <label for="ph-target" class="field-label">pH هدف</label>
          <input id="ph-target" v-model="form.targetPH" type="text" inputmode="decimal" placeholder="مثلاً ۶٫۰" class="field-input" :class="bad(form.targetPH) && 'field-invalid'" />
        </div>
        <div>
          <label for="ph-temp" class="field-label">دما (°C)</label>
          <input id="ph-temp" v-model="form.temperature" type="text" inputmode="decimal" placeholder="۲۵" class="field-input" :class="bad(form.temperature) && 'field-invalid'" />
        </div>
      </div>
      <p v-if="direction" class="mt-2 text-xs text-gray-500 dark:text-gray-400">
        {{ direction === 'acid' ? 'کاهش pH: با «اسید» انجام می‌شود.' : 'افزایش pH: با «باز» انجام می‌شود.' }}
      </p>
    </section>

    <!-- ===================== ورودی‌های مدل تئوریک ===================== -->
    <section v-if="method === 'theoretical'">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">مشخصات شیمیایی نمونه</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div>
          <label for="ph-sample-type" class="field-label">نوع نمونه</label>
          <select id="ph-sample-type" v-model="form.sampleType" class="field-input">
            <option value="simple">آب ساده (سیستم کربناتی غالب است)</option>
            <option value="complex">محلول غذایی یا ترکیبی</option>
          </select>
        </div>
        <div>
          <label for="ph-alk" class="field-label">آلکالینیتی</label>
          <div class="flex gap-2">
            <input id="ph-alk" v-model="form.alkalinity" type="text" inputmode="decimal" placeholder="مثلاً ۲۰۰" class="field-input flex-1 min-w-0" :class="form.sampleType === 'simple' && bad(form.alkalinity) && 'field-invalid'" />
            <select v-model="form.alkUnit" class="field-input !w-32 flex-shrink-0" aria-label="واحد آلکالینیتی">
              <option value="mgL">mg/L as CaCO₃</option>
              <option value="meqL">meq/L</option>
            </select>
          </div>
        </div>
      </div>

      <div
        v-if="form.sampleType === 'complex'"
        class="mt-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3"
      >
        <p class="text-xs sm:text-sm text-amber-900 dark:text-amber-200 leading-6">برای محلول غذایی یا ترکیبی، مدل کربناتی قابل اتکا نیست.</p>
        <button type="button" @click="method = 'titration'" class="text-xs font-medium text-amber-900 dark:text-amber-200 underline flex-shrink-0 text-right">رفتن به تیتراسیون واقعی</button>
      </div>
    </section>

    <!-- ===================== ورودی‌های تیتراسیون ===================== -->
    <section v-else>
      <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">داده‌های تیتراسیون</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div>
          <label for="ph-normality" class="field-label">نرمالیته‌ی تیترانت (N)</label>
          <input id="ph-normality" v-model="form.normality" type="text" inputmode="decimal" placeholder="۰٫۱" class="field-input" :class="bad(form.normality) && 'field-invalid'" />
        </div>
        <div>
          <label for="ph-sample-vol" class="field-label">حجم نمونه‌ی تیتراسیون (mL)</label>
          <input id="ph-sample-vol" v-model="form.sampleVolumeMl" type="text" inputmode="decimal" placeholder="۱۰۰" class="field-input" :class="bad(form.sampleVolumeMl) && 'field-invalid'" />
        </div>
      </div>

      <div class="mt-4 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="grid grid-cols-[1fr_1fr_2.25rem] gap-2 px-3 py-2 bg-gray-50 dark:bg-gray-700/40 text-[11px] font-medium text-gray-500 dark:text-gray-400">
          <span>حجم تجمعی تیترانت (mL)</span>
          <span>pH</span>
          <span></span>
        </div>

        <!-- نقطه‌ی اولیه (خودکار) -->
        <div class="grid grid-cols-[1fr_1fr_2.25rem] gap-2 px-3 py-2 border-t border-gray-100 dark:border-gray-700 items-center">
          <span class="field-input !bg-gray-100 dark:!bg-gray-700 text-gray-500 dark:text-gray-400 tabular-nums">۰ (نقطه‌ی اولیه)</span>
          <span class="field-input !bg-gray-100 dark:!bg-gray-700 text-gray-500 dark:text-gray-400 tabular-nums">{{ form.currentPH || 'pH فعلی' }}</span>
          <span></span>
        </div>

        <div
          v-for="(row, i) in rows"
          :key="row.id"
          class="px-3 py-2 border-t border-gray-100 dark:border-gray-700"
        >
          <div class="grid grid-cols-[1fr_1fr_2.25rem] gap-2 items-center">
            <input v-model="row.volume" type="text" inputmode="decimal" :placeholder="`نقطه ${(i + 1).toLocaleString('fa-IR')}`" class="field-input" :class="rowBad(row, 'volume') && 'field-invalid'" :aria-label="`حجم تیترانت نقطه ${i + 1}`" />
            <input v-model="row.pH" type="text" inputmode="decimal" placeholder="pH" class="field-input" :class="rowBad(row, 'pH') && 'field-invalid'" :aria-label="`pH نقطه ${i + 1}`" />
            <button
              type="button"
              @click="removeRow(row.id)"
              :disabled="rows.length <= 1"
              class="w-9 h-9 flex items-center justify-center rounded-lg text-gray-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              :aria-label="`حذف نقطه ${i + 1}`"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p v-if="slopes[row.id] !== undefined" class="mt-1 text-[11px] text-gray-400 dark:text-gray-500 tabular-nums">
            ΔpH/ΔV: {{ slopes[row.id] }}
          </p>
        </div>

        <div class="px-3 py-2.5 border-t border-gray-100 dark:border-gray-700">
          <button
            type="button"
            @click="addRow"
            :disabled="rows.length >= MAX_ROWS"
            class="inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline disabled:opacity-40 disabled:no-underline"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v12m6-6H6" />
            </svg>
            افزودن نقطه
          </button>
        </div>
      </div>

      <div v-if="chartPoints.length >= 2" class="mt-4">
        <PhTitrationChart :points="chartPoints" :target-p-h="targetPHValue" :dose-ml="chartDoseMl" />
      </div>
    </section>

    <!-- ===================== ماده شیمیایی ===================== -->
    <section>
      <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">ماده شیمیایی</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
        <div>
          <label for="ph-chem" class="field-label">ماده</label>
          <select id="ph-chem" v-model="chemicalId" class="field-input">
            <option v-for="c in availableChemicals" :key="c.id" :value="c.id">
              {{ c.custom ? c.name : `${c.name} (${c.formula})` }}
            </option>
          </select>
        </div>
        <div>
          <label for="ph-purity" class="field-label">خلوص تجاری (٪ وزنی)</label>
          <input id="ph-purity" v-model="chemFields[chemicalId].purity" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields[chemicalId].purity) && 'field-invalid'" />
        </div>
        <div>
          <label for="ph-density" class="field-label">چگالی (g/mL)</label>
          <input id="ph-density" v-model="chemFields[chemicalId].density" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields[chemicalId].density) && 'field-invalid'" />
        </div>
        <template v-if="selectedBase.custom">
          <div>
            <label for="ph-mw" class="field-label">جرم مولی (g/mol)</label>
            <input id="ph-mw" v-model="chemFields[chemicalId].mw" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields[chemicalId].mw) && 'field-invalid'" />
          </div>
          <div>
            <label for="ph-z" class="field-label">ظرفیت مؤثر (z)</label>
            <input id="ph-z" v-model="chemFields[chemicalId].z" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields[chemicalId].z) && 'field-invalid'" />
          </div>
        </template>
      </div>

      <p class="mt-2 text-xs text-gray-500 dark:text-gray-400 leading-6">
        <template v-if="!selectedBase.custom">
          جرم مولی {{ selectedBase.mw.toLocaleString('fa-IR') }} g/mol ·
          {{ selectedBase.z === 'phosphoric' ? 'ظرفیت مؤثر: وابسته به pH هدف (محاسبه‌ی خودکار)' : `ظرفیت مؤثر z = ${Number(selectedBase.z).toLocaleString('fa-IR')}` }} ·
        </template>
        مقادیر خلوص و چگالی نمونه‌اند؛ مقدار واقعی محصول خود را از برگه‌ی مشخصات وارد کنید.
      </p>
    </section>

    <!-- ===================== عملیات ===================== -->
    <div class="flex flex-col-reverse sm:flex-row sm:items-center gap-2 sm:gap-3">
      <button
        type="button"
        @click="reset"
        class="w-full sm:w-auto px-5 py-3 sm:py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        پاک‌سازی
      </button>
      <button
        type="button"
        @click="calculate"
        class="w-full sm:w-auto px-8 py-3 sm:py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors"
      >
        محاسبه دوز
      </button>
    </div>

    <!-- ===================== خطا ===================== -->
    <div
      v-if="errorMessage"
      ref="errorRef"
      class="rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3"
      role="alert"
    >
      <p class="text-sm text-rose-800 dark:text-rose-200 leading-6">{{ errorMessage }}</p>
      <button
        v-if="needTitration && method === 'theoretical'"
        type="button"
        @click="method = 'titration'"
        class="mt-2 text-sm font-medium text-rose-800 dark:text-rose-200 underline"
      >
        رفتن به تیتراسیون واقعی
      </button>
    </div>

    <!-- ===================== نتیجه ===================== -->
    <div v-if="result && result.ok" ref="resultRef">
      <PhResultPanel
        :result="result"
        :chemical="chemical"
        :volume-l="lastVolumeL"
        :target-p-h="lastTargetPH"
        :stale="stale"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick } from 'vue';
import { CHEMICALS, calculateTheoretical, calculateTitration } from './ph/phDose';
import type { Chemical, DoseResult } from './ph/phDose';
import { parseNum } from './ph/phFormat';
import PhResultPanel from './ph/PhResultPanel.vue';
import PhTitrationChart from './ph/PhTitrationChart.vue';

type Method = 'theoretical' | 'titration';

const MAX_ROWS = 20;

const methods: Array<{ id: Method; title: string; subtitle: string; badge?: string }> = [
  { id: 'theoretical', title: 'مدل تئوریک', subtitle: 'برای آب ساده با غلبه‌ی سیستم کربنات؛ فقط با آلکالینیتی و pH' },
  { id: 'titration', title: 'تیتراسیون واقعی', subtitle: 'از نمونه‌ی واقعی؛ مناسب محلول‌های غذایی و ترکیبی', badge: 'دقیق‌تر' }
];

// ============================================================
// State
// ============================================================
const method = ref<Method>('theoretical');

const defaultForm = () => ({
  volume: '',
  volumeUnit: 'L' as 'L' | 'm3',
  currentPH: '',
  targetPH: '',
  temperature: '25',
  alkalinity: '',
  alkUnit: 'mgL' as 'mgL' | 'meqL',
  sampleType: 'simple' as 'simple' | 'complex',
  normality: '0.1',
  sampleVolumeMl: '100'
});
const form = reactive(defaultForm());

const initialChemFields = () =>
  Object.fromEntries(
    CHEMICALS.map(c => [
      c.id,
      { mw: String(c.mw), z: c.z === 'phosphoric' ? '' : String(c.z), purity: String(c.purityPct), density: String(c.densityGmL) }
    ])
  ) as Record<string, { mw: string; z: string; purity: string; density: string }>;

const chemicalId = ref('hcl');
const chemFields = reactive(initialChemFields());

let rowSeq = 0;
const newRow = () => ({ id: ++rowSeq, volume: '', pH: '' });
const rows = ref([newRow(), newRow(), newRow(), newRow()]);

const submitted = ref(false);
const errorMessage = ref('');
const needTitration = ref(false);
const result = ref<DoseResult | null>(null);
const stale = ref(false);
const lastVolumeL = ref(1);
const lastTargetPH = ref(7);

const resultRef = ref<HTMLElement | null>(null);
const errorRef = ref<HTMLElement | null>(null);

// ============================================================
// Computed
// ============================================================
const currentPHValue = computed(() => parseNum(form.currentPH));
const targetPHValue = computed(() => parseNum(form.targetPH));

const direction = computed<'acid' | 'base' | null>(() => {
  const a = currentPHValue.value;
  const b = targetPHValue.value;
  if (a === null || b === null || Math.abs(a - b) < 0.005) return null;
  return b < a ? 'acid' : 'base';
});

const availableChemicals = computed(() =>
  direction.value ? CHEMICALS.filter(c => c.kind === direction.value) : CHEMICALS
);

watch(direction, d => {
  if (!d) return;
  const current = CHEMICALS.find(c => c.id === chemicalId.value);
  if (!current || current.kind !== d) {
    chemicalId.value = CHEMICALS.find(c => c.kind === d)!.id;
  }
});

const selectedBase = computed(() => CHEMICALS.find(c => c.id === chemicalId.value) || CHEMICALS[0]);

const chemical = computed<Chemical>(() => {
  const base = selectedBase.value;
  const f = chemFields[base.id];
  return {
    ...base,
    mw: parseNum(f.mw) ?? NaN,
    z: base.z === 'phosphoric' ? 'phosphoric' : (parseNum(f.z) ?? NaN),
    purityPct: parseNum(f.purity) ?? NaN,
    densityGmL: parseNum(f.density) ?? NaN
  };
});

// نقاط معتبر برای نمودار و شیب‌ها
const validRows = computed(() =>
  rows.value
    .map(r => ({ id: r.id, volumeMl: parseNum(r.volume), pH: parseNum(r.pH) }))
    .filter((r): r is { id: number; volumeMl: number; pH: number } => r.volumeMl !== null && r.pH !== null && r.volumeMl > 0)
);

const chartPoints = computed(() => {
  if (currentPHValue.value === null) return [];
  return [{ volumeMl: 0, pH: currentPHValue.value }, ...validRows.value.map(r => ({ volumeMl: r.volumeMl, pH: r.pH }))];
});

const chartDoseMl = computed(() => {
  const r = result.value;
  return r && r.ok && r.titration && !stale.value ? r.titration.doseMl : null;
});

// ΔpH/ΔV هر نقطه نسبت به نقطه‌ی قبلی (بر اساس ترتیب حجم)
const slopes = computed<Record<number, string>>(() => {
  const out: Record<number, string> = {};
  if (currentPHValue.value === null) return out;
  const ordered = [...validRows.value].sort((a, b) => a.volumeMl - b.volumeMl);
  let prevV = 0;
  let prevPH = currentPHValue.value;
  for (const r of ordered) {
    const dv = r.volumeMl - prevV;
    if (dv > 0) out[r.id] = ((r.pH - prevPH) / dv).toLocaleString('fa-IR', { maximumFractionDigits: 2 });
    prevV = r.volumeMl;
    prevPH = r.pH;
  }
  return out;
});

// ============================================================
// اعتبارسنجی نمایشی (قاب قرمز فقط بعد از اولین تلاش برای محاسبه)
// ============================================================
const bad = (value: string) => submitted.value && parseNum(value) === null;

const rowBad = (row: { volume: string; pH: string }, field: 'volume' | 'pH') => {
  if (!submitted.value) return false;
  const touched = row.volume.trim() !== '' || row.pH.trim() !== '';
  return touched && parseNum(row[field]) === null;
};

// ============================================================
// Rows
// ============================================================
const addRow = () => {
  if (rows.value.length < MAX_ROWS) rows.value.push(newRow());
};
const removeRow = (id: number) => {
  if (rows.value.length > 1) rows.value = rows.value.filter(r => r.id !== id);
};

// ============================================================
// Actions
// ============================================================
const fail = (message: string, needsTitration = false) => {
  result.value = null;
  errorMessage.value = message;
  needTitration.value = needsTitration;
  nextTick(() => errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' }));
};

const calculate = () => {
  submitted.value = true;
  errorMessage.value = '';
  needTitration.value = false;
  stale.value = false;

  const volume = parseNum(form.volume);
  const currentPH = currentPHValue.value;
  const targetPH = targetPHValue.value;
  const temperatureC = parseNum(form.temperature);

  if (volume === null) return fail('حجم محلول را وارد کنید.');
  if (currentPH === null) return fail('pH فعلی را وارد کنید.');
  if (targetPH === null) return fail('pH هدف را وارد کنید.');
  if (temperatureC === null) return fail('دما را وارد کنید.');

  const volumeL = form.volumeUnit === 'm3' ? volume * 1000 : volume;
  const base = { volumeL, currentPH, targetPH, temperatureC, chemical: chemical.value };

  let outcome: DoseResult;

  if (method.value === 'theoretical') {
    let alkMgL = parseNum(form.alkalinity);
    if (alkMgL === null && form.sampleType === 'simple') return fail('آلکالینیتی نمونه را وارد کنید.');
    if (alkMgL !== null && form.alkUnit === 'meqL') alkMgL *= 50;
    outcome = calculateTheoretical({ ...base, alkalinityMgL: alkMgL ?? 0, sampleType: form.sampleType });
  } else {
    const normality = parseNum(form.normality);
    const sampleVolumeMl = parseNum(form.sampleVolumeMl);
    if (normality === null) return fail('نرمالیته‌ی تیترانت را وارد کنید.');
    if (sampleVolumeMl === null) return fail('حجم نمونه‌ی تیتراسیون را وارد کنید.');

    const points: Array<{ volumeMl: number; pH: number }> = [];
    for (const [i, row] of rows.value.entries()) {
      const empty = row.volume.trim() === '' && row.pH.trim() === '';
      if (empty) continue;
      const v = parseNum(row.volume);
      const p = parseNum(row.pH);
      if (v === null || p === null) return fail(`نقطه‌ی ${(i + 1).toLocaleString('fa-IR')} کامل یا معتبر نیست (هم حجم و هم pH لازم است).`);
      points.push({ volumeMl: v, pH: p });
    }
    outcome = calculateTitration({ ...base, normality, sampleVolumeMl, points });
  }

  if (!outcome.ok) return fail(outcome.error, outcome.needTitration);

  lastVolumeL.value = volumeL;
  lastTargetPH.value = targetPH;
  result.value = outcome;
  nextTick(() => resultRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'start' }));
};

const reset = () => {
  Object.assign(form, defaultForm());
  Object.assign(chemFields, initialChemFields());
  chemicalId.value = 'hcl';
  rows.value = [newRow(), newRow(), newRow(), newRow()];
  submitted.value = false;
  errorMessage.value = '';
  needTitration.value = false;
  result.value = null;
  stale.value = false;
};

// اگر بعد از محاسبه ورودی‌ها عوض شدند، نتیجه «قدیمی» علامت می‌خورد
const signature = computed(() =>
  JSON.stringify([method.value, form, chemicalId.value, chemFields[chemicalId.value], rows.value])
);
watch(signature, () => {
  if (result.value) stale.value = true;
});
</script>

<style scoped>
.field-label {
  @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5;
}
.field-input {
  @apply w-full px-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all;
}
.field-invalid {
  @apply border-rose-400 dark:border-rose-500 bg-rose-50/60 dark:bg-rose-900/10;
}
select.field-input {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 0.9rem;
  padding-left: 2rem;
}
</style>
