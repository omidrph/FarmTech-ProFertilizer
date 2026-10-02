<!-- frontend/src/components/features/PhCalculatorTab.vue -->
<!--
  تب «PH» — اصلاح pH با اسید/باز (منطق جدید)
  ------------------------------------------------------------
  سناریوی واقعی گلخانه: استوک ساخته و در مخزن اصلی ریخته می‌شود؛ سپس pH فعلی
  اندازه‌گیری می‌شود و اسید/باز اضافه می‌شود تا به pH هدف برسد.

  دو حالت (هر دو به «مقدار برای کل مخزن» می‌رسند):
    • آزمون روی نمونه: مثلاً ۵ لیتر از مخزن ۵۰۰۰ لیتری برداشته می‌شود، مرحله‌به‌مرحله
      اسید اضافه و pH خوانده می‌شود، و مقدار نهایی با نسبت حجم به کل مخزن تعمیم می‌یابد.
    • رسپی (دوز مشخص): کاربر از قبل می‌داند چقدر اسید لازم است.

  فقط اسید/بازهایی که در پایگاه‌داده‌ی کود خود کاربر هستند قابل انتخاب‌اند.
  همه‌ی محاسبات در بک‌اند (app/core/ph_calculator) انجام می‌شود.
-->
<template>
  <div class="space-y-5 sm:space-y-6">

    <!-- ===================== سربرگ ===================== -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6l.5 4M9 3L7.5 15.5A2 2 0 009.48 18h5.04a2 2 0 001.98-2.5L15 7M9 3l-.5 4m6.5-4l.5 4M5.5 12h13" />
          </svg>
        </div>
        <div class="min-w-0">
          <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">اصلاح pH</h2>
          <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
            مقدار اسید یا باز لازم برای رساندن pH مخزن به هدف — و اثر آن بر عناصر و EC
          </p>
        </div>
      </div>

      <div v-if="!reportStore.hasActiveReport" class="mt-3 rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">
        گزارشی باز نیست؛ محاسبه کار می‌کند ولی ثبت در تاریخچه و اعمال در محاسبهٔ کود نیاز به یک گزارش دارد.
      </div>
      <div v-if="activeBanner" class="mt-3 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-2 text-xs leading-6 text-emerald-800 dark:text-emerald-200">
        اصلاح فعال این گزارش: <strong>{{ activeBanner.chemical_name }}</strong> —
        {{ fmtDose(activeBanner.dose_tank, activeBanner.dose_unit) }} برای {{ fmt(activeBanner.tank_volume_l, 0) }} لیتر.
        عناصر آن در «محاسبهٔ کود» لحاظ می‌شود.
      </div>
    </section>

    <!-- ===================== ۱) انتخاب ماده ===================== -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-3">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">۱. اسید یا باز مورد استفاده</h3>

      <p v-if="phStore.isLoadingAdjusters" class="text-sm text-gray-500">در حال بارگذاری…</p>

      <div v-else-if="phStore.adjusters.length === 0" class="rounded-xl border border-dashed border-gray-300 dark:border-gray-600 px-4 py-5 text-center">
        <p class="text-sm text-gray-700 dark:text-gray-200">در پایگاه‌داده کود شما هنوز اسید یا بازی ثبت نشده است.</p>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-6">
          از «پایگاه‌داده کود» یک اسید (مثل نیتریک یا فسفریک) یا باز (مثل KOH) اضافه کنید تا اینجا ظاهر شود.
        </p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <button
          v-for="opt in phStore.adjusters"
          :key="opt.fertilizer_id"
          type="button"
          @click="selectAdjuster(opt.fertilizer_id)"
          class="text-right rounded-xl border px-3 py-2.5 transition-colors"
          :class="form.fertilizerId === opt.fertilizer_id
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 ring-1 ring-primary-500'
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-500'"
        >
          <span class="flex items-center gap-2">
            <span class="text-[10px] px-1.5 py-0.5 rounded font-medium"
              :class="opt.kind === 'acid'
                ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'
                : 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300'">
              {{ opt.kind === 'acid' ? 'اسید' : 'باز' }}
            </span>
            <span class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ opt.name }}</span>
          </span>
          <span class="block text-[11px] text-gray-500 dark:text-gray-400 mt-1">
            خلوص {{ fmt(opt.concentration, 1) }}٪ · مصرف به {{ opt.dose_unit === 'ml' ? 'میلی‌لیتر' : 'گرم' }}
            <template v-if="Object.keys(opt.elements_pct).length"> · {{ elementsText(opt.elements_pct) }}</template>
          </span>
        </button>
      </div>

      <div v-if="selected && selected.warnings.length" class="space-y-1.5">
        <div v-for="(w, i) in selected.warnings" :key="i" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">
          {{ w }}
        </div>
      </div>
    </section>

    <!-- ===================== ۲) روش ===================== -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-4">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">۲. چطور مقدار را به‌دست بیاوریم؟</h3>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <button v-for="m in modes" :key="m.id" type="button" @click="setMode(m.id)"
          class="text-right rounded-xl border px-3 py-2.5 transition-colors"
          :class="form.mode === m.id
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 ring-1 ring-primary-500'
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-500'">
          <span class="block text-sm font-medium text-gray-900 dark:text-white">{{ m.title }}</span>
          <span class="block text-[11px] text-gray-500 dark:text-gray-400 mt-0.5 leading-5">{{ m.subtitle }}</span>
        </button>
      </div>

      <!-- فیلدهای مشترک -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label class="field-label">حجم مخزن اصلی (لیتر)</label>
          <input v-model="form.tankVolume" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && !isPos(form.tankVolume) }" placeholder="مثلاً ۵۰۰۰" />
        </div>
        <div>
          <label class="field-label">pH فعلی محلول{{ form.mode === 'known' ? ' (اختیاری)' : '' }}</label>
          <input v-model="form.initialPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && invalid.initialPh }" placeholder="مثلاً ۷٫۸" />
        </div>
        <div>
          <label class="field-label">pH هدف{{ form.mode === 'known' ? ' (اختیاری)' : '' }}</label>
          <input v-model="form.targetPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && invalid.targetPh }" placeholder="مثلاً ۶٫۰" />
          <p v-if="phContextRange" class="text-[11px] text-gray-400 mt-1">بازهٔ مطلوب معمول: {{ phContextRange }}</p>
        </div>
      </div>

      <!-- ===== آزمون روی نمونه ===== -->
      <template v-if="form.mode === 'trial'">
        <div class="rounded-xl bg-gray-50 dark:bg-gray-900/30 border border-gray-200 dark:border-gray-700 px-3 py-2.5 text-xs leading-6 text-gray-600 dark:text-gray-300">
          مقداری از محلول مخزن (مثلاً یک سطل ۵ لیتری) را بردارید. pH آن را بخوانید، کمی {{ unitWord }} اضافه کنید، خوب هم بزنید، pH را بخوانید و تکرار کنید تا به هدف برسید. هر مرحله را زیر ثبت کنید.
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="field-label">حجم نمونه (لیتر)</label>
            <input v-model="form.sampleVolume" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && !isPos(form.sampleVolume) }" placeholder="مثلاً ۵" />
          </div>
          <div class="sm:col-span-2 flex items-end">
            <p v-if="scalePreview" class="text-xs text-gray-500 dark:text-gray-400 pb-2.5">
              ضریب مقیاس‌دهی به مخزن: <strong class="text-gray-800 dark:text-gray-100 tabular-nums">×{{ fmt(scalePreview, 0) }}</strong>
            </p>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="field-label !mb-0">مراحل آزمون</label>
            <span class="text-[11px] text-gray-400">مقدار هر مرحله «اضافه‌شده در همان مرحله» است</span>
          </div>
          <div class="space-y-2">
            <div v-for="(row, i) in form.steps" :key="row.id" class="grid grid-cols-[1.5rem_1fr_1fr_auto] gap-2 items-center">
              <span class="text-[11px] text-gray-400 text-center tabular-nums">{{ i + 1 }}</span>
              <div class="relative">
                <input v-model="row.amount" inputmode="decimal" class="field-input !pl-10" :class="{ 'field-invalid': submitted && invalid.steps[i] }" :placeholder="`مقدار (${unitShort})`" />
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[11px] text-gray-400">{{ unitShort }}</span>
              </div>
              <input v-model="row.ph" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && invalid.steps[i] }" placeholder="pH بعد از افزودن" />
              <button type="button" @click="removeStep(row.id)" :disabled="form.steps.length === 1" class="w-8 h-8 rounded-lg text-gray-400 hover:text-rose-500 disabled:opacity-30" aria-label="حذف مرحله">✕</button>
            </div>
          </div>
          <div class="flex items-center justify-between mt-2">
            <button type="button" @click="addStep" :disabled="form.steps.length >= MAX_STEPS" class="text-xs font-medium text-primary-600 dark:text-primary-400 disabled:opacity-40">+ مرحلهٔ بعد</button>
            <span v-if="cumulativeText" class="text-[11px] text-gray-500 tabular-nums">مجموع تاکنون: {{ cumulativeText }}</span>
          </div>
        </div>

        <PhCurveChart v-if="livePoints.length >= 2 && num(form.targetPh) != null" :points="livePoints" :target-ph="num(form.targetPh) as number" :unit-label="unitShort" />
      </template>

      <!-- ===== رسپی ===== -->
      <template v-else>
        <div class="rounded-xl bg-gray-50 dark:bg-gray-900/30 border border-gray-200 dark:border-gray-700 px-3 py-2.5 text-xs leading-6 text-gray-600 dark:text-gray-300">
          اگر برای این رسپی از قبل می‌دانید چقدر {{ unitWord }} لازم است (مثلاً از ساخت قبلی)، همان مقدار را بنویسید؛ به حجم مخزن مقیاس داده می‌شود.
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="field-label">مقدار {{ unitWord }} در رسپی ({{ unitShort }})</label>
            <input v-model="form.doseAmount" inputmode="decimal" class="field-input" :class="{ 'field-invalid': submitted && !isPos(form.doseAmount) }" placeholder="مثلاً ۸۰۰" />
          </div>
          <div>
            <label class="field-label">این مقدار برای چند لیتر محلول است؟</label>
            <input v-model="form.doseBasis" inputmode="decimal" class="field-input" :placeholder="form.tankVolume ? `خالی = ${form.tankVolume} (همان مخزن)` : 'مثلاً ۱۰۰۰'" />
          </div>
        </div>
      </template>

      <!-- پیشرفته -->
      <details v-if="selected && selected.dose_unit === 'ml'" class="group">
        <summary class="cursor-pointer text-xs font-medium text-gray-500 dark:text-gray-400 select-none">تنظیمات پیشرفته (چگالی دقیق ماده)</summary>
        <div class="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="field-label">چگالی (g/mL) — اختیاری</label>
            <input v-model="form.density" inputmode="decimal" class="field-input" :placeholder="selected.density_g_ml ? `مرجع تقریبی: ${fmt(selected.density_g_ml, 3)}` : 'از برگهٔ مشخصات (SDS) محصول'" />
          </div>
          <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5 self-end pb-2">
            چگالی فقط برای تبدیل میلی‌لیتر به گرم و محاسبهٔ عناصر واردشده به کار می‌رود. اگر خالی بماند از جدول مرجع استفاده می‌شود.
          </p>
        </div>
      </details>
    </section>

    <!-- ===================== عملیات ===================== -->
    <div class="flex flex-col-reverse sm:flex-row sm:items-center gap-2 sm:gap-3">
      <button type="button" @click="resetForm" class="w-full sm:w-auto px-5 py-3 sm:py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
        پاک‌سازی
      </button>
      <button type="button" @click="calculate" :disabled="phStore.isCalculating || !selected" class="w-full sm:w-auto px-8 py-3 sm:py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 disabled:opacity-60 text-white text-sm font-medium transition-colors">
        {{ phStore.isCalculating ? 'در حال محاسبه…' : 'محاسبه مقدار برای مخزن' }}
      </button>
    </div>

    <!-- ===================== خطا ===================== -->
    <div v-if="phStore.errorMessage" ref="errorRef" role="alert" class="rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3">
      <p class="text-sm text-rose-800 dark:text-rose-200 leading-6">{{ phStore.errorMessage }}</p>
    </div>

    <!-- ===================== نتیجه + ثبت ===================== -->
    <div v-if="phStore.result" ref="resultRef" class="space-y-3">
      <div v-if="stale" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs text-amber-800 dark:text-amber-200">
        ورودی‌ها بعد از آخرین محاسبه تغییر کرده‌اند؛ دوباره محاسبه کنید.
      </div>
      <div :class="{ 'opacity-60': stale }">
        <PhResultPanel :result="phStore.result" />
      </div>

      <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 space-y-3">
        <h3 class="text-sm font-bold text-gray-900 dark:text-white">ثبت این اصلاح</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="sm:col-span-3">
            <label class="field-label">یادداشت (اختیاری)</label>
            <input v-model="saveForm.note" maxlength="500" class="field-input" placeholder="مثلاً: آب چاه، ساخت دوم" />
          </div>
          <div>
            <label class="field-label">EC قبل از اصلاح (اختیاری)</label>
            <input v-model="saveForm.ecBefore" inputmode="decimal" class="field-input" placeholder="dS/m" />
          </div>
          <div>
            <label class="field-label">EC بعد از اصلاح (اختیاری)</label>
            <input v-model="saveForm.ecAfter" inputmode="decimal" class="field-input" placeholder="dS/m" />
          </div>
        </div>
        <div class="flex flex-col sm:flex-row gap-2">
          <button type="button" @click="save(true)" :disabled="!canSave" class="px-5 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-sm font-medium transition-colors">
            {{ phStore.isSaving ? 'در حال ثبت…' : 'ثبت و اعمال در محاسبهٔ کود' }}
          </button>
          <button type="button" @click="save(false)" :disabled="!canSave" class="px-5 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors">
            فقط ثبت در تاریخچه
          </button>
        </div>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">
          «اعمال» یعنی در محاسبهٔ بعدیِ کود، عناصر این اسید/باز مثل آب منبع پایه لحاظ شوند: سهم کودهای دیگر کم می‌شود و تعادل یونی و EC با آن دوباره محاسبه می‌گردد. فقط یک اصلاح در هر گزارش فعال است.
        </p>
        <p v-if="saveMessage" class="text-xs text-emerald-700 dark:text-emerald-300">{{ saveMessage }}</p>
      </section>
    </div>

    <!-- ===================== تاریخچه ===================== -->
    <PhHistoryPanel
      v-if="reportStore.hasActiveReport"
      :items="phStore.history"
      @reuse="reuse"
      @apply="(id) => toggleApply(id, true)"
      @unapply="(id) => toggleApply(id, false)"
      @delete="onDelete"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';
import { usePhStore } from '@/store/modules/phStore';
import { useReportStore } from '@/store/modules/reportStore';
import type { PhAdjustmentItem, PhAdjustmentRequest, PhMode } from '@/services/apiService';
import { parseNum, fmt, fmtDose } from './ph/phFormat';
import PhResultPanel from './ph/PhResultPanel.vue';
import PhCurveChart from './ph/PhCurveChart.vue';
import PhHistoryPanel from './ph/PhHistoryPanel.vue';

const MAX_STEPS = 30;

const phStore = usePhStore();
const reportStore = useReportStore();

const modes: Array<{ id: PhMode; title: string; subtitle: string }> = [
  { id: 'trial', title: 'آزمون روی نمونه', subtitle: 'مقداری از محلول را برمی‌دارم، اسید/باز می‌ریزم و pH را می‌خوانم؛ نتیجه به کل مخزن تعمیم داده شود.' },
  { id: 'known', title: 'رسپی (دوز مشخص)', subtitle: 'برای این رسپی از قبل می‌دانم چقدر اسید/باز لازم است.' }
];

let rowSeq = 0;
const newStep = () => ({ id: ++rowSeq, amount: '', ph: '' });

const defaultForm = () => ({
  mode: 'trial' as PhMode,
  fertilizerId: null as number | null,
  tankVolume: '',
  initialPh: '',
  targetPh: '',
  sampleVolume: '5',
  steps: [newStep(), newStep()],
  doseAmount: '',
  doseBasis: '',
  density: ''
});
const form = reactive(defaultForm());
const saveForm = reactive({ note: '', ecBefore: '', ecAfter: '' });

const submitted = ref(false);
const stale = ref(false);
const saveMessage = ref('');
const resultRef = ref<HTMLElement | null>(null);
const errorRef = ref<HTMLElement | null>(null);

const num = (v: string): number | null => parseNum(v);
const isPos = (v: string): boolean => {
  const n = parseNum(v);
  return n !== null && n > 0;
};

// ============================================================
// مشتقات
// ============================================================
const selected = computed(() => phStore.adjusters.find((a) => a.fertilizer_id === form.fertilizerId) || null);
const unitShort = computed(() => (selected.value?.dose_unit === 'g' ? 'g' : 'mL'));
const unitWord = computed(() => (selected.value?.kind === 'base' ? 'باز' : 'اسید'));
const activeBanner = computed(() => phStore.context?.active || null);

const phContextRange = computed(() => {
  const r = phStore.context?.target_ph_range;
  return r && r.length === 2 ? `${fmt(r[0], 1)} تا ${fmt(r[1], 1)}` : '';
});

const scalePreview = computed(() => {
  const t = num(form.tankVolume);
  const s = num(form.sampleVolume);
  return t && s && t > 0 && s > 0 ? t / s : null;
});

const livePoints = computed(() => {
  const init = num(form.initialPh);
  if (init == null) return [];
  const pts = [{ amount: 0, ph: init }];
  let total = 0;
  for (const r of form.steps) {
    const a = num(r.amount);
    const p = num(r.ph);
    if (a == null || a <= 0 || p == null) break;
    total += a;
    pts.push({ amount: total, ph: p });
  }
  return pts;
});

const cumulativeText = computed(() => {
  const total = form.steps.reduce((s, r) => s + (num(r.amount) || 0), 0);
  return total > 0 ? `${fmt(total, 2)} ${unitShort.value}` : '';
});

const phOk = (v: string) => {
  const n = num(v);
  return n != null && n >= 0 && n <= 14;
};

const invalid = computed(() => ({
  initialPh: form.mode === 'trial' ? !phOk(form.initialPh) : form.initialPh.trim() !== '' && !phOk(form.initialPh),
  targetPh: form.mode === 'trial' ? !phOk(form.targetPh) : form.targetPh.trim() !== '' && !phOk(form.targetPh),
  steps: form.steps.map((r) => !(num(r.amount) != null && (num(r.amount) as number) > 0 && phOk(r.ph)))
}));

const canSave = computed(() => !!phStore.result && !stale.value && reportStore.hasActiveReport && !phStore.isSaving);

// ============================================================
// تغییر فرم → نتیجه قدیمی می‌شود
// ============================================================
watch(
  () => JSON.stringify(form),
  () => {
    if (phStore.result) stale.value = true;
    saveMessage.value = '';
  }
);

// ============================================================
// اقدامات
// ============================================================
function selectAdjuster(id: number) {
  form.fertilizerId = id;
  form.density = '';
}

function setMode(mode: PhMode) {
  form.mode = mode;
}

function addStep() {
  if (form.steps.length < MAX_STEPS) form.steps.push(newStep());
}
function removeStep(id: number) {
  if (form.steps.length > 1) form.steps.splice(form.steps.findIndex((r) => r.id === id), 1);
}

function elementsText(el: Record<string, number>): string {
  return Object.entries(el)
    .map(([k, v]) => `${k} ${fmt(v, 1)}٪`)
    .join('، ');
}

function buildPayload(): PhAdjustmentRequest | null {
  if (!form.fertilizerId) {
    phStore.errorMessage = 'ابتدا اسید یا باز را انتخاب کنید.';
    return null;
  }
  const tank = num(form.tankVolume);
  if (!tank || tank <= 0) {
    phStore.errorMessage = 'حجم مخزن را وارد کنید.';
    return null;
  }

  const base: PhAdjustmentRequest = {
    mode: form.mode,
    fertilizer_id: form.fertilizerId,
    tank_volume_l: tank,
    initial_ph: num(form.initialPh),
    target_ph: num(form.targetPh),
    density_g_ml: num(form.density)
  };

  if (form.mode === 'trial') {
    if (invalid.value.initialPh || invalid.value.targetPh) {
      phStore.errorMessage = 'pH فعلی و pH هدف را (بین ۰ تا ۱۴) وارد کنید.';
      return null;
    }
    const sample = num(form.sampleVolume);
    if (!sample || sample <= 0) {
      phStore.errorMessage = 'حجم نمونه را وارد کنید.';
      return null;
    }
    // ردیف‌های کاملاً خالی نادیده گرفته می‌شوند؛ ردیف نیمه‌کاره خطاست
    const filled = form.steps.filter((r) => r.amount.trim() !== '' || r.ph.trim() !== '');
    if (filled.length === 0 || filled.some((r) => invalid.value.steps[form.steps.indexOf(r)])) {
      phStore.errorMessage = 'هر مرحله باید هم مقدار (بزرگ‌تر از صفر) و هم pH معتبر داشته باشد.';
      return null;
    }
    base.sample_volume_l = sample;
    base.steps = filled.map((r) => ({ amount: num(r.amount) as number, ph: num(r.ph) as number }));
  } else {
    const dose = num(form.doseAmount);
    if (!dose || dose <= 0) {
      phStore.errorMessage = 'مقدار ماده در رسپی را وارد کنید.';
      return null;
    }
    if ((invalid.value.initialPh || invalid.value.targetPh)) {
      phStore.errorMessage = 'pH وارد‌شده معتبر نیست (۰ تا ۱۴).';
      return null;
    }
    base.dose_amount = dose;
    base.dose_basis_volume_l = num(form.doseBasis);
  }
  return base;
}

async function calculate() {
  submitted.value = true;
  phStore.errorMessage = null;
  saveMessage.value = '';
  const payload = buildPayload();
  if (!payload) {
    await nextTick();
    errorRef.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  const ok = await phStore.calculate(payload);
  stale.value = false;
  await nextTick();
  (ok ? resultRef.value : errorRef.value)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function save(apply: boolean) {
  const payload = buildPayload();
  if (!payload) return;
  const item = await phStore.save({
    ...payload,
    note: saveForm.note.trim() || null,
    ec_before: num(saveForm.ecBefore),
    ec_after: num(saveForm.ecAfter),
    apply
  });
  if (item) {
    saveMessage.value = apply
      ? 'ثبت شد و در محاسبهٔ کود اعمال می‌شود؛ در صفحهٔ «محاسبه کود» دوباره محاسبه را بزنید.'
      : 'در تاریخچه ثبت شد.';
  }
}

async function toggleApply(id: number, applied: boolean) {
  const ok = await phStore.setApplied(id, applied);
  if (ok) {
    saveMessage.value = applied
      ? 'اعمال شد؛ در صفحهٔ «محاسبه کود» دوباره محاسبه را بزنید.'
      : 'اعمال این مورد لغو شد؛ محاسبهٔ بعدی بدون آن انجام می‌شود.';
  }
}

async function onDelete(id: number) {
  await phStore.remove(id);
}

function reuse(item: PhAdjustmentItem) {
  Object.assign(form, defaultForm());
  form.mode = item.mode;
  form.fertilizerId = item.fertilizer_id ?? null;
  form.tankVolume = String(item.tank_volume_l);
  form.initialPh = item.initial_ph != null ? String(item.initial_ph) : '';
  form.targetPh = item.target_ph != null ? String(item.target_ph) : '';
  if (item.mode === 'trial') {
    form.sampleVolume = item.sample_volume_l != null ? String(item.sample_volume_l) : '5';
    form.steps = (item.trial_steps || []).map((s) => ({ id: ++rowSeq, amount: String(s.amount), ph: String(s.ph) }));
    if (form.steps.length === 0) form.steps = [newStep()];
  } else {
    form.doseAmount = String(item.dose_per_1000l);
    form.doseBasis = '1000';
  }
  if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetForm() {
  const keepTank = form.tankVolume;
  Object.assign(form, defaultForm());
  form.tankVolume = keepTank;
  form.targetPh = phStore.context ? String(phStore.context.suggested_target_ph) : '';
  saveForm.note = saveForm.ecBefore = saveForm.ecAfter = '';
  submitted.value = false;
  stale.value = false;
  saveMessage.value = '';
  phStore.clearResult();
}

// ============================================================
// بارگذاری اولیه و پیش‌پرکردن از زمینهٔ گزارش
// ============================================================
function prefillFromContext() {
  const ctx = phStore.context;
  if (!ctx) return;
  if (!form.tankVolume && ctx.tank_volume_l) form.tankVolume = String(ctx.tank_volume_l);
  if (!form.targetPh) form.targetPh = String(ctx.suggested_target_ph);
}

onMounted(async () => {
  await phStore.refreshAll();
  prefillFromContext();
});

// تعویض گزارش → تاریخچه و زمینه دوباره
watch(
  () => reportStore.currentReportId,
  async () => {
    phStore.reset();
    form.tankVolume = '';
    form.targetPh = '';
    form.initialPh = '';
    await phStore.refreshAll();
    prefillFromContext();
  }
);
</script>

<style scoped>
.field-label {
  @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5;
}
.field-input {
  @apply w-full px-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition;
}
.field-invalid {
  @apply border-rose-400 dark:border-rose-500 bg-rose-50/60 dark:bg-rose-900/10;
}
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
