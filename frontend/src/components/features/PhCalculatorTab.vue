<!-- frontend/src/components/features/PhCalculatorTab.vue -->
<!--
  تب «PH» — اصلاح pH با اسید/باز (۳ مرحلهٔ ساده، هم‌سبک «محاسبه کود»)
    ۱) اطلاعات: ماده، حجم مخزن، حجم نمونه، pH فعلی و هدف
    ۲) آزمون: افزودن مرحله‌ای ماده به نمونه و ثبت pH
    ۳) نتیجه: مقدار برای کل مخزن + ثبت و اعمال در «محاسبه کود»
  سمت چپ همیشه نمای بصری زنده (گیج pH + مسیر نمونه ← مخزن) است.
  اگر مقدار اسید/باز را از قبل می‌دانید، آن را در «محاسبه کود ← انتخاب کود» وارد کنید.
-->
<template>
  <div>
    <!-- ===================== سربرگ + مراحل + ناوبری ===================== -->
    <nav class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-3 sm:p-4 mb-4">
      <ol class="flex items-stretch gap-1.5 sm:gap-2">
        <li v-for="(step, index) in steps" :key="step.id" class="flex items-start flex-1 min-w-0">
          <button type="button" @click="goToStep(step.id)" :disabled="!isStepReachable(step.id)"
            class="flex flex-col sm:flex-row items-center justify-center sm:justify-start gap-1 sm:gap-2 min-w-0 w-full text-center sm:text-right rounded-lg border px-2 py-2 sm:py-2.5 min-h-[52px] transition-colors disabled:cursor-not-allowed"
            :class="currentStep === step.id
              ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800 shadow-sm'
              : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-gray-50 dark:hover:bg-gray-700/40 disabled:hover:bg-white dark:disabled:hover:bg-gray-800'">
            <span class="w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 transition-colors" :class="stepCircleClass(step.id)">
              <svg v-if="isStepDone(step.id)" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" /></svg>
              <template v-else>{{ index + 1 }}</template>
            </span>
            <span class="min-w-0">
              <span class="block text-[11px] sm:text-sm font-semibold truncate leading-tight" :class="currentStep === step.id ? 'text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300'">{{ step.title }}</span>
              <span class="hidden sm:block text-[11px] text-gray-400 truncate">{{ step.subtitle }}</span>
            </span>
          </button>
          <span v-if="index < steps.length - 1" class="h-0.5 flex-1 mx-1 sm:mx-2 mt-3.5 sm:mt-4 rounded-full transition-colors" :class="isStepDone(step.id) ? 'bg-primary-500' : 'bg-gray-200 dark:bg-gray-700'"></span>
        </li>
      </ol>

      <!-- دکمه‌ها (همان آیکون‌ها و شکل صفحهٔ محاسبه کود؛ جای ثابت) -->
      <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center gap-2">
        <button v-if="currentStep > 1" type="button" @click="goToStep(currentStep - 1)"
          class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          قبلی
        </button>
        <button type="button" @click="showReset = true"
          class="inline-flex items-center gap-1.5 px-3 py-2.5 text-sm font-medium rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3M4 7h16" /></svg>
          <span class="hidden sm:inline">بازنشانی</span>
        </button>
        <div class="flex-1"></div>
        <button v-if="currentStep === 1" type="button" @click="next1" class="primary-btn">
          ادامه: آزمون
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>
        <button v-else-if="currentStep === 2" type="button" @click="calculate" :disabled="phStore.isCalculating" class="primary-btn">
          <svg v-if="!phStore.isCalculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
          {{ phStore.isCalculating ? 'در حال محاسبه...' : 'محاسبه مقدار برای مخزن' }}
        </button>
        <button v-else type="button" @click="save" :disabled="!canSave" class="primary-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          {{ phStore.isSaving ? 'در حال ثبت...' : 'ثبت و اعمال در محاسبه کود' }}
        </button>
      </div>
    </nav>

    <div v-if="!reportStore.hasActiveReport" class="mb-3 rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">گزارشی باز نیست؛ محاسبه کار می‌کند ولی ثبت و اعمال در محاسبهٔ کود نیاز به یک گزارش دارد.</div>
    <div v-if="activeBanner" class="mb-3 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-2 text-xs leading-6 text-emerald-800 dark:text-emerald-200">
      اصلاح فعال این گزارش: <strong>{{ activeBanner.chemical_name }}</strong> — {{ fmtDose(activeBanner.dose_tank, activeBanner.dose_unit) }} برای {{ fmt(activeBanner.tank_volume_l, 0) }} لیتر.
    </div>

    <PhHistoryPanel v-if="reportStore.hasActiveReport" class="mb-4" :items="phStore.history" @reuse="reuse" @apply="(id) => toggleApply(id, true)" @unapply="(id) => toggleApply(id, false)" @delete="onDelete" @update="onUpdate" />

    <!-- ===================== محتوا: فرم + نمای بصری ===================== -->
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-4 items-start">
      <div class="lg:col-span-3 space-y-4 order-2 lg:order-1">
        <Transition name="step" mode="out-in">

          <!-- ───── مرحله ۱ ───── -->
          <section v-if="currentStep === 1" key="s1" class="card space-y-5">
            <div>
              <h3 class="card-title">کدام اسید یا باز؟</h3>
              <p v-if="phStore.isLoadingAdjusters" class="text-sm text-gray-500 mt-2">در حال بارگذاری…</p>
              <div v-else-if="phStore.adjusters.length === 0" class="mt-3 rounded-xl border border-dashed border-gray-300 dark:border-gray-600 px-4 py-5 text-center">
                <p class="text-sm text-gray-700 dark:text-gray-200">هنوز اسید یا بازی در پایگاه‌داده کود شما نیست.</p>
                <p class="text-xs text-gray-500 mt-1 leading-6">از «پایگاه داده کود» یک اسید یا باز اضافه کنید.</p>
              </div>
              <div v-else class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
                <button v-for="opt in phStore.adjusters" :key="opt.fertilizer_id" type="button" @click="selectAdjuster(opt.fertilizer_id)"
                  class="text-right rounded-xl border px-3 py-2.5 transition-colors flex items-center gap-2.5"
                  :class="form.fertilizerId === opt.fertilizer_id ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 ring-1 ring-primary-500' : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'">
                  <span class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-bold" :class="opt.kind === 'acid' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300' : 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300'">{{ opt.kind === 'acid' ? 'اسید' : 'باز' }}</span>
                  <span class="min-w-0">
                    <span class="block text-sm font-medium text-gray-900 dark:text-white truncate">{{ opt.name }}</span>
                    <span class="block text-[11px] text-gray-500 dark:text-gray-400">خلوص {{ fmt(opt.concentration, 1) }}٪ · {{ opt.dose_unit === 'ml' ? 'میلی‌لیتر' : 'گرم' }}</span>
                  </span>
                </button>
              </div>
              <div v-if="selected && selected.warnings.length" class="mt-2 space-y-1.5">
                <div v-for="(w, i) in selected.warnings" :key="i" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">{{ w }}</div>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="field-label">حجم مخزن اصلی (لیتر)</label>
                <input v-model="form.tankVolume" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched1 && !isPos(form.tankVolume) }" placeholder="مثلاً ۵۰۰۰" />
              </div>
              <div>
                <label class="field-label">حجم نمونه (لیتر)</label>
                <div class="flex gap-1.5">
                  <input v-model="form.sampleVolume" inputmode="decimal" class="field-input !w-20 flex-shrink-0" :class="{ 'field-invalid': touched1 && !isPos(form.sampleVolume) }" />
                  <button v-for="v in samplePresets" :key="v" type="button" @click="form.sampleVolume = String(v)" class="chip" :class="num(form.sampleVolume) === v ? 'chip-on' : ''">{{ fmt(v) }}</button>
                </div>
              </div>
              <div>
                <label class="field-label">pH فعلی محلول</label>
                <input v-model="form.initialPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched1 && !phOk(form.initialPh) }" placeholder="مثلاً ۷٫۸" />
              </div>
              <div>
                <label class="field-label">pH هدف <span v-if="phRangeText" class="font-normal text-gray-400">(معمول {{ phRangeText }})</span></label>
                <input v-model="form.targetPh" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched1 && !phOk(form.targetPh) }" placeholder="مثلاً ۶٫۰" />
              </div>
            </div>
            <p v-if="scale" class="text-xs text-gray-500 dark:text-gray-400">نمونهٔ بزرگ‌تر دقت بیشتری می‌دهد. ضریب مقیاس‌دهی به مخزن: <strong class="text-gray-800 dark:text-gray-100 tabular-nums">×{{ fmt(scale, scale < 10 ? 1 : 0) }}</strong></p>
            <div v-if="directionWarning" class="rounded-lg border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-3 py-2 text-xs leading-6 text-rose-800 dark:text-rose-200">{{ directionWarning }}</div>
            <p v-if="phStore.errorMessage && currentStep === 1" class="text-xs text-rose-600 dark:text-rose-400">{{ phStore.errorMessage }}</p>
          </section>

          <!-- ───── مرحله ۲ ───── -->
          <section v-else-if="currentStep === 2" key="s2" class="card space-y-4">
            <div>
              <h3 class="card-title">آزمون روی نمونه</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-6">کمی {{ unitWord }} به نمونه بریزید، خوب هم بزنید، pH را بخوانید و ثبت کنید؛ تا رسیدن به هدف تکرار کنید.</p>
            </div>
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="stat"><p>pH فعلی</p><b :class="phStatusClass">{{ latestPh != null ? fmt(latestPh, 2) : '—' }}</b></div>
              <div class="stat"><p>هدف</p><b>{{ fmt(num(form.targetPh) ?? 0, 2) }}</b></div>
              <div class="stat"><p>مصرف تاکنون</p><b>{{ fmt(cumulative, 2) }} <small>{{ unitShort }}</small></b></div>
            </div>
            <div v-if="nextHint" class="rounded-lg bg-primary-50/70 dark:bg-primary-900/10 border border-primary-200 dark:border-primary-800 px-3 py-2 text-xs leading-6 text-primary-800 dark:text-primary-200">{{ nextHint }}</div>

            <div class="space-y-2">
              <div v-for="(row, i) in form.steps" :key="row.id" class="grid grid-cols-[1.75rem_1fr_1fr_1.75rem] gap-2 items-center">
                <span class="w-7 h-7 rounded-full bg-gray-100 dark:bg-gray-700 text-[11px] font-bold text-gray-500 dark:text-gray-300 flex items-center justify-center tabular-nums">{{ fmt(i + 1) }}</span>
                <div class="relative">
                  <input v-model="row.amount" inputmode="decimal" class="field-input !pl-11" :class="{ 'field-invalid': touched3 && rowInvalid(row) }" placeholder="مقدار اضافه‌شده" />
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[11px] text-gray-400">{{ unitShort }}</span>
                </div>
                <input v-model="row.ph" inputmode="decimal" class="field-input" :class="{ 'field-invalid': touched3 && rowInvalid(row) }" placeholder="pH بعد از افزودن" />
                <button type="button" @click="removeStep(row.id)" :disabled="form.steps.length === 1" class="w-7 h-7 rounded-md text-gray-400 hover:text-rose-500 disabled:opacity-30" aria-label="حذف مرحله">✕</button>
              </div>
            </div>
            <button type="button" @click="addStep" :disabled="form.steps.length >= MAX_STEPS" class="text-xs font-medium text-primary-600 dark:text-primary-400 disabled:opacity-40">+ مرحلهٔ بعد</button>

            <details v-if="livePoints.length >= 2 && num(form.targetPh) != null" class="group rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/20">
              <summary class="cursor-pointer select-none px-3 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 flex items-center justify-between">نمودار منحنی pH
                <svg class="w-4 h-4 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg></summary>
              <div class="px-2 pb-2"><PhCurveChart :points="livePoints" :target-ph="num(form.targetPh) as number" :unit-label="unitShort" /></div>
            </details>

            <details v-if="selected && selected.dose_unit === 'ml'" class="rounded-xl border border-gray-200 dark:border-gray-700 px-3 py-2.5">
              <summary class="cursor-pointer select-none text-xs font-medium text-gray-600 dark:text-gray-300">چگالی دقیق ماده (اختیاری)</summary>
              <input v-model="form.density" inputmode="decimal" class="field-input mt-2" :placeholder="selected.density_g_ml ? `ثبت‌شده: ${fmt(selected.density_g_ml, 3)} g/mL` : 'از برگهٔ مشخصات (SDS)'" />
            </details>
            <p v-if="phStore.errorMessage && currentStep === 2" class="text-xs text-rose-600 dark:text-rose-400">{{ phStore.errorMessage }}</p>
          </section>

          <!-- ───── مرحله ۳ ───── -->
          <div v-else key="s3" class="space-y-4">
            <div v-if="phStore.errorMessage && !phStore.result" ref="errorRef" role="alert" class="rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3">
              <p class="text-sm text-rose-800 dark:text-rose-200 leading-6">{{ phStore.errorMessage }}</p>
              <button type="button" @click="goToStep(2)" class="mt-2 text-xs font-medium text-rose-700 dark:text-rose-300 underline">بازگشت به آزمون</button>
            </div>
            <template v-if="phStore.result">
              <div v-if="stale" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs text-amber-800 dark:text-amber-200">ورودی‌ها بعد از آخرین محاسبه تغییر کرده‌اند؛ دوباره محاسبه کنید.</div>
              <div :class="{ 'opacity-60': stale }"><PhResultPanel :result="phStore.result" /></div>
              <section class="card space-y-3">
                <h3 class="card-title">جزئیات اختیاری برای تاریخچه</h3>
                <input v-model="saveForm.note" maxlength="500" class="field-input" placeholder="یادداشت (مثلاً: آب چاه، ساخت دوم)" />
                <div class="grid grid-cols-2 gap-2">
                  <input v-model="saveForm.ecBefore" inputmode="decimal" class="field-input" placeholder="EC قبل (dS/m)" />
                  <input v-model="saveForm.ecAfter" inputmode="decimal" class="field-input" placeholder="EC بعد (dS/m)" />
                </div>
                <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">با «ثبت و اعمال» (دکمهٔ بالا) نتیجه ثبت و مستقیماً در محاسبه کود اعمال می‌شود: سهم کودهای دیگر کم می‌شود و تعادل یونی و EC دوباره محاسبه می‌گردد. در هر گزارش یک اصلاح فعال است.</p>
                <p v-if="!reportStore.hasActiveReport" class="text-[11px] text-amber-700 dark:text-amber-300">برای ثبت، ابتدا یک گزارش باز یا ذخیره کنید.</p>
                <p v-if="saveError" class="text-xs text-rose-600 dark:text-rose-400">{{ saveError }}</p>
              </section>
            </template>
          </div>
        </Transition>
      </div>

      <!-- نمای بصری (دسکتاپ: چسبیده؛ موبایل: بالای فرم) -->
      <aside class="lg:col-span-2 order-1 lg:order-2 lg:sticky lg:top-24">
        <PhVisual :ph="visualPh" :target-ph="num(form.targetPh)" :kind="selected?.kind ?? null" :tank-volume="num(form.tankVolume)" :sample-volume="num(form.sampleVolume)" :scale="scale" :dose-label="currentStep === 3 ? doseLabel : ''" :dropper="currentStep === 2" :live="currentStep >= 2" />
      </aside>
    </div>

    <!-- تأیید بازنشانی -->
    <Teleport to="body">
      <div v-if="showReset" class="fixed inset-0 z-[70] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/50" @click="showReset = false"></div>
        <div class="relative w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-5">
          <h4 class="text-base font-bold text-gray-900 dark:text-white">بازنشانی اصلاح pH؟</h4>
          <p class="text-sm text-gray-600 dark:text-gray-300 mt-2 leading-6">ورودی‌ها و نتیجهٔ فعلی پاک می‌شود (تاریخچهٔ ثبت‌شده می‌ماند).</p>
          <div class="mt-4 flex gap-2 justify-end">
            <button type="button" @click="showReset = false" class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-sm text-gray-700 dark:text-gray-200">انصراف</button>
            <button type="button" @click="resetAll(); showReset = false" class="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-sm font-medium">بازنشانی</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';
import { usePhStore } from '@/store/modules/phStore';
import { useReportStore } from '@/store/modules/reportStore';
import type { PhAdjustmentItem, PhAdjustmentRequest } from '@/services/apiService';
import { parseNum, fmt, fmtDose } from './ph/phFormat';
import PhResultPanel from './ph/PhResultPanel.vue';
import PhCurveChart from './ph/PhCurveChart.vue';
import PhHistoryPanel from './ph/PhHistoryPanel.vue';
import PhVisual from './ph/PhVisual.vue';

const emit = defineEmits<{ (e: 'applied', id: number): void }>();
const MAX_STEPS = 30;
const samplePresets = [5, 10, 20];
const phStore = usePhStore();
const reportStore = useReportStore();

type StepId = 1 | 2 | 3;
const steps: Array<{ id: StepId; title: string; subtitle: string }> = [
  { id: 1, title: 'اطلاعات', subtitle: 'ماده، مخزن و pH' },
  { id: 2, title: 'آزمون', subtitle: 'افزودن به نمونه' },
  { id: 3, title: 'نتیجه', subtitle: 'مقدار مخزن و ثبت' }
];
const currentStep = ref<StepId>(1);
const touched1 = ref(false);
const touched3 = ref(false);
const showReset = ref(false);

let rowSeq = 0;
const newStep = () => ({ id: ++rowSeq, amount: '', ph: '' });
const defaultForm = () => ({ fertilizerId: null as number | null, tankVolume: '', sampleVolume: '5', initialPh: '', targetPh: '', steps: [newStep(), newStep()], density: '' });
const form = reactive(defaultForm());
const saveForm = reactive({ note: '', ecBefore: '', ecAfter: '' });
const stale = ref(false);
const saveError = ref('');
const errorRef = ref<HTMLElement | null>(null);

const num = (v: string | number | null | undefined): number | null => (v === null || v === undefined ? null : typeof v === 'number' ? v : parseNum(v));
const isPos = (v: string) => { const n = parseNum(v); return n !== null && n > 0; };
const phOk = (v: string) => { const n = parseNum(v); return n !== null && n >= 0 && n <= 14; };
const rowInvalid = (r: { amount: string; ph: string }) => {
  if (r.amount.trim() === '' && r.ph.trim() === '') return false;
  const a = parseNum(r.amount);
  return !(a !== null && a > 0 && phOk(r.ph));
};

const selected = computed(() => phStore.adjusters.find((a) => a.fertilizer_id === form.fertilizerId) || null);
const unitShort = computed(() => (selected.value?.dose_unit === 'g' ? 'g' : 'mL'));
const unitWord = computed(() => (selected.value?.kind === 'base' ? 'باز' : 'اسید'));
const activeBanner = computed(() => phStore.context?.active || null);
const phRangeText = computed(() => { const r = phStore.context?.target_ph_range; return r && r.length === 2 ? `${fmt(r[0], 1)} تا ${fmt(r[1], 1)}` : ''; });
const scale = computed(() => { const t = num(form.tankVolume), s = num(form.sampleVolume); return t && s && t > 0 && s > 0 ? t / s : null; });

const directionWarning = computed(() => {
  const i = num(form.initialPh), t = num(form.targetPh), kind = selected.value?.kind;
  if (i == null || t == null || !kind) return '';
  if (Math.abs(i - t) < 1e-9) return 'pH فعلی و هدف یکسان‌اند؛ اصلاحی لازم نیست.';
  if (t < i && kind === 'base') return 'برای کاهش pH باید «اسید» انتخاب کنید.';
  if (t > i && kind === 'acid') return 'برای افزایش pH باید «باز» انتخاب کنید.';
  return '';
});

const livePoints = computed(() => {
  const init = num(form.initialPh);
  if (init == null) return [];
  const pts = [{ amount: 0, ph: init }]; let total = 0;
  for (const r of form.steps) {
    const a = parseNum(r.amount), p = parseNum(r.ph);
    if (a == null || a <= 0 || p == null) break;
    total += a; pts.push({ amount: total, ph: p });
  }
  return pts;
});
const latestPh = computed(() => (livePoints.value.length ? livePoints.value[livePoints.value.length - 1].ph : num(form.initialPh)));
const cumulative = computed(() => (livePoints.value.length ? livePoints.value[livePoints.value.length - 1].amount : 0));
const visualPh = computed(() => (currentStep.value === 3 && phStore.result?.final_ph != null ? phStore.result.final_ph : currentStep.value === 1 ? num(form.initialPh) : latestPh.value));
const phStatusClass = computed(() => {
  const p = latestPh.value, t = num(form.targetPh);
  if (p == null || t == null) return '';
  const d = Math.abs(p - t);
  return d <= 0.1 ? 'text-emerald-600 dark:text-emerald-400' : d <= 0.5 ? 'text-amber-600 dark:text-amber-400' : '';
});

const nextHint = computed(() => {
  const t = num(form.targetPh), pts = livePoints.value, kind = selected.value?.kind;
  if (t == null || pts.length === 0) return '';
  const last = pts[pts.length - 1];
  if (pts.length === 1) return `با مقدار کم شروع کنید (مثلاً ۱ ${unitShort.value}) و بعد از هم‌زدن pH را بخوانید.`;
  const over = kind === 'acid' ? last.ph < t - 0.05 : kind === 'base' ? last.ph > t + 0.05 : false;
  if (over) return 'pH از هدف رد شده؛ می‌توانید همین داده‌ها را محاسبه کنید (با میان‌یابی تخمین زده می‌شود) یا نمونهٔ تازه بیازمایید.';
  if (Math.abs(last.ph - t) <= 0.1) return 'به هدف رسیدید؛ «محاسبه مقدار برای مخزن» را بزنید.';
  const prev = pts[pts.length - 2];
  const slope = (last.ph - prev.ph) / (last.amount - prev.amount);
  if (!Number.isFinite(slope) || Math.abs(slope) < 1e-9) return '';
  const rem = (t - last.ph) / slope;
  return rem > 0 ? `مرحلهٔ بعد حدود ${fmt(Math.max(rem * (Math.abs(last.ph - t) > 0.4 ? 0.6 : 0.9), 0), 2)} ${unitShort.value} (تخمین محتاطانه از شیب قبلی).` : '';
});

const doseLabel = computed(() => (phStore.result ? fmtDose(phStore.result.dose_tank, phStore.result.dose_unit) : ''));
const canSave = computed(() => !!phStore.result && !stale.value && reportStore.hasActiveReport && !phStore.isSaving);

const step1Done = computed(() => !!form.fertilizerId && isPos(form.tankVolume) && isPos(form.sampleVolume) && phOk(form.initialPh) && phOk(form.targetPh) && !directionWarning.value);
const step2Done = computed(() => !!phStore.result && !stale.value);
const isStepDone = (id: StepId) => (id === 1 ? step1Done.value && currentStep.value > 1 : id === 2 ? step2Done.value && currentStep.value > 2 : step2Done.value && currentStep.value === 3);
const isStepReachable = (id: StepId) => (id === 1 ? true : id === 2 ? step1Done.value : !!phStore.result);
const stepCircleClass = (id: StepId) => (isStepDone(id) ? 'bg-emerald-500 text-white' : currentStep.value === id ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400');
const goToStep = (id: number) => { const t = id as StepId; if (!isStepReachable(t)) return; currentStep.value = t; nextTick(() => typeof window !== 'undefined' && window.scrollTo({ top: 0, behavior: 'smooth' })); };

const next1 = () => {
  touched1.value = true;
  phStore.errorMessage = !form.fertilizerId ? 'ابتدا اسید یا باز را انتخاب کنید.' : null;
  if (step1Done.value) goToStep(2);
};

function selectAdjuster(id: number) { form.fertilizerId = id; form.density = ''; phStore.errorMessage = null; }
function addStep() { if (form.steps.length < MAX_STEPS) form.steps.push(newStep()); }
function removeStep(id: number) { if (form.steps.length > 1) form.steps.splice(form.steps.findIndex((r) => r.id === id), 1); }

function buildPayload(): PhAdjustmentRequest | null {
  const tank = num(form.tankVolume), sample = num(form.sampleVolume), initial = num(form.initialPh), target = num(form.targetPh);
  if (!form.fertilizerId || !tank || !sample || initial == null || target == null) { phStore.errorMessage = 'اطلاعات مرحلهٔ ۱ را کامل کنید.'; return null; }
  const filled = form.steps.filter((r) => r.amount.trim() !== '' || r.ph.trim() !== '');
  if (filled.length === 0 || filled.some((r) => rowInvalid(r))) { touched3.value = true; phStore.errorMessage = 'هر مرحله باید هم مقدار (بزرگ‌تر از صفر) و هم pH معتبر داشته باشد.'; return null; }
  return { mode: 'trial', fertilizer_id: form.fertilizerId, tank_volume_l: tank, initial_ph: initial, target_ph: target, density_g_ml: num(form.density), sample_volume_l: sample,
    steps: filled.map((r) => ({ amount: parseNum(r.amount) as number, ph: parseNum(r.ph) as number })) };
}

async function calculate() {
  touched3.value = true; phStore.errorMessage = null;
  const payload = buildPayload();
  if (!payload) return;
  const ok = await phStore.calculate(payload);
  stale.value = false;
  currentStep.value = 3;
  await nextTick();
  if (!ok) errorRef.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  else if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function save() {
  saveError.value = '';
  const payload = buildPayload();
  if (!payload) return;
  const item = await phStore.save({ ...payload, note: saveForm.note.trim() || null, ec_before: num(saveForm.ecBefore), ec_after: num(saveForm.ecAfter), apply: true });
  if (item) { phStore.pendingRecalc = true; emit('applied', item.id); }
  else saveError.value = phStore.errorMessage || 'ثبت انجام نشد.';
}

async function toggleApply(id: number, applied: boolean) { await phStore.setApplied(id, applied); }
async function onUpdate(id: number, data: { note: string | null; ec_before: number | null; ec_after: number | null }) { await phStore.updateMeta(id, data); }
async function onDelete(id: number) { await phStore.remove(id); }

function reuse(item: PhAdjustmentItem) {
  if (item.mode !== 'trial') return;
  Object.assign(form, defaultForm());
  form.fertilizerId = item.fertilizer_id ?? null;
  form.tankVolume = String(item.tank_volume_l);
  form.sampleVolume = item.sample_volume_l != null ? String(item.sample_volume_l) : '5';
  form.initialPh = item.initial_ph != null ? String(item.initial_ph) : '';
  form.targetPh = item.target_ph != null ? String(item.target_ph) : '';
  form.steps = (item.trial_steps || []).map((s) => ({ id: ++rowSeq, amount: String(s.amount), ph: String(s.ph) }));
  if (form.steps.length === 0) form.steps = [newStep()];
  phStore.clearResult();
  currentStep.value = 2;
  if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetAll() {
  const keepTank = form.tankVolume;
  Object.assign(form, defaultForm());
  form.tankVolume = keepTank;
  form.targetPh = phStore.context ? String(phStore.context.suggested_target_ph) : '';
  saveForm.note = saveForm.ecBefore = saveForm.ecAfter = '';
  touched1.value = touched3.value = false; stale.value = false; saveError.value = '';
  phStore.clearResult();
  currentStep.value = 1;
}

watch(() => JSON.stringify(form), () => { if (phStore.result) stale.value = true; });

function prefillFromContext() {
  const ctx = phStore.context;
  if (!ctx) return;
  if (!form.tankVolume && ctx.tank_volume_l) form.tankVolume = String(ctx.tank_volume_l);
  if (!form.targetPh) form.targetPh = String(ctx.suggested_target_ph);
}
onMounted(async () => { phStore.clearResult(); await phStore.refreshAll(); prefillFromContext(); });
watch(() => reportStore.currentReportId, async () => { phStore.reset(); form.tankVolume = ''; form.targetPh = ''; currentStep.value = 1; await phStore.refreshAll(); prefillFromContext(); });
</script>

<style scoped>
.card { @apply bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5; }
.card-title { @apply text-base font-semibold text-gray-900 dark:text-white; }
.field-label { @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5; }
.field-input { @apply w-full px-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition; }
.field-invalid { @apply border-rose-400 dark:border-rose-500 bg-rose-50/60 dark:bg-rose-900/10; }
.chip { @apply h-[42px] px-3 rounded-lg border border-gray-200 dark:border-gray-600 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors; }
.chip-on { @apply border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300; }
.stat { @apply rounded-lg border border-gray-200 dark:border-gray-700 p-2; }
.stat p { @apply text-[11px] text-gray-500 dark:text-gray-400; }
.stat b { @apply block text-base font-bold tabular-nums text-gray-900 dark:text-white; }
.stat small { @apply text-[10px] font-normal text-gray-400; }
.primary-btn { @apply inline-flex items-center gap-2 px-4 sm:px-5 py-2.5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors; }
.tabular-nums { font-variant-numeric: tabular-nums; }
.step-enter-active, .step-leave-active { transition: opacity .18s ease, transform .18s ease; }
.step-enter-from { opacity: 0; transform: translateY(6px); }
.step-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
