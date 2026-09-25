<!-- frontend/src/components/features/PhCalculatorTab.vue -->
<!--
  تب «PH» (بین «پایگاه‌داده کود» و «ابزارک‌ها»)
  ------------------------------------------------------------
  نسخه‌ی جدید: تمام محاسبات شیمیایی در بک‌اند (پایتون) انجام می‌شود
  (app/core/ph_calculator + app/routes/ph_calculator.py). این کامپوننت
  فقط UI است و از طریق store/modules/phStore.ts با API صحبت می‌کند.

  طبق تصمیم محصول این تب عمداً در چرخه‌ی رسمی محاسبه‌ی کود قرار ندارد؛
  اما به داده‌ی واقعی سیستم وصل است:
    • اسیدها: مستقیماً از پایگاه‌داده‌ی کود (is_acid=true) - نه لیست ثابت
    • زمینه: به‌صورت اطلاعاتی از آنالیز آب و عناصر هدف گزارش جاری
  و می‌تواند تاریخچه‌ی محاسبات خودش را (اختیاری) ذخیره کند.
-->
<template>
  <div class="space-y-5 sm:space-y-6">

    <!-- ===================== سربرگ ===================== -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <div class="min-w-0">
          <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">ماشین‌حساب PH</h2>
          <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
            محاسبه‌ی مقدار اسید یا باز لازم برای رساندن pH محلول به مقدار هدف - جدا از چرخه‌ی رسمی محاسبه‌ی کود
          </p>
        </div>
      </div>
    </section>

    <!-- ===================== راهنمای زمینه (از آنالیز آب/عناصر هدف) ===================== -->
    <div
      v-if="phStore.context?.is_likely_complex_solution"
      class="rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3 text-xs sm:text-sm text-amber-900 dark:text-amber-200 leading-6"
    >
      عناصر هدفِ گزارش جاری شامل {{ phStore.context.complex_indicator_elements.join('، ') }} است؛ یعنی این احتمالاً یک
      «محلول غذایی» است، نه آب ساده. برای این حالت روش «تیتراسیون واقعی» دقیق‌تر از مدل تئوریک کربناتی است.
      <button type="button" @click="method = 'titration'; sampleType = 'complex'" class="underline font-medium">رفتن به تیتراسیون واقعی</button>
    </div>

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
          <span v-if="m.badge" class="text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">{{ m.badge }}</span>
        </span>
        <span class="block mt-1 text-xs text-gray-500 dark:text-gray-400 leading-5">{{ m.subtitle }}</span>
      </button>
    </div>

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
          <select id="ph-sample-type" v-model="sampleType" class="field-input">
            <option value="simple">آب ساده (سیستم کربناتی غالب است)</option>
            <option value="complex">محلول غذایی یا ترکیبی</option>
          </select>
        </div>
        <div>
          <label for="ph-alk" class="field-label">
            آلکالینیتی
            <span class="font-normal text-gray-400">(فیلدی مستقل - در صفحه‌ی آنالیز آب ذخیره نمی‌شود)</span>
          </label>
          <div class="flex gap-2">
            <input id="ph-alk" v-model="form.alkalinity" type="text" inputmode="decimal" placeholder="مثلاً ۲۰۰" class="field-input flex-1 min-w-0" :class="sampleType === 'simple' && bad(form.alkalinity) && 'field-invalid'" />
            <select v-model="form.alkUnit" class="field-input !w-40 flex-shrink-0" aria-label="واحد آلکالینیتی">
              <option value="mg_l_caco3">mg/L as CaCO₃</option>
              <option value="meq_l">meq/L</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="sampleType === 'complex'" class="mt-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3">
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

        <div class="grid grid-cols-[1fr_1fr_2.25rem] gap-2 px-3 py-2 border-t border-gray-100 dark:border-gray-700 items-center">
          <span class="field-input !bg-gray-100 dark:!bg-gray-700 text-gray-500 dark:text-gray-400 tabular-nums">۰ (نقطه‌ی اولیه)</span>
          <span class="field-input !bg-gray-100 dark:!bg-gray-700 text-gray-500 dark:text-gray-400 tabular-nums">{{ form.currentPH || 'pH فعلی' }}</span>
          <span></span>
        </div>

        <div v-for="(row, i) in rows" :key="row.id" class="px-3 py-2 border-t border-gray-100 dark:border-gray-700">
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
        </div>

        <div class="px-3 py-2.5 border-t border-gray-100 dark:border-gray-700">
          <button type="button" @click="addRow" :disabled="rows.length >= MAX_ROWS" class="inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline disabled:opacity-40 disabled:no-underline">
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

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div class="sm:col-span-2">
          <label for="ph-chem" class="field-label">
            ماده
            <span class="font-normal text-gray-400">(از اسیدهای واقعی پایگاه‌داده‌ی کود شما)</span>
          </label>
          <select id="ph-chem" v-model="selectedAcidKey" class="field-input" :disabled="phStore.isLoadingAcids">
            <optgroup label="اسیدهای پایگاه‌داده کود" v-if="filteredAcidOptions.length">
              <option v-for="a in filteredAcidOptions" :key="a.fertilizer_id" :value="`fert-${a.fertilizer_id}`">
                {{ a.name }} ({{ fmt(a.concentration, 1) }}٪{{ a.is_system_default ? ' · سیستمی' : '' }})
              </option>
            </optgroup>
            <option value="custom">ماده‌ی سفارشی (وارد کردن دستی مشخصات)</option>
          </select>
          <p v-if="phStore.isLoadingAcids" class="mt-1 text-xs text-gray-400">در حال دریافت لیست اسیدها...</p>
          <p v-else-if="!filteredAcidOptions.length" class="mt-1 text-xs text-amber-600 dark:text-amber-400">
            هیچ کود اسیدی در پایگاه‌داده‌ی کود شما ثبت نشده؛ از «ماده‌ی سفارشی» استفاده کنید یا ابتدا یک اسید در تب «پایگاه‌داده کود» ثبت کنید.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mt-3">
        <div>
          <label for="ph-purity" class="field-label">خلوص تجاری (٪ وزنی)</label>
          <input id="ph-purity" v-model="chemFields.purity" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields.purity) && 'field-invalid'" />
        </div>
        <div>
          <label for="ph-density" class="field-label">
            چگالی (g/mL)
            <span v-if="isCustomAcid || selectedAcidRecognized" class="font-normal text-gray-400">{{ densityHint }}</span>
          </label>
          <input id="ph-density" v-model="chemFields.density" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields.density) && 'field-invalid'" />
        </div>
        <template v-if="isCustomAcid || !selectedAcidRecognized">
          <div>
            <label for="ph-mw" class="field-label">جرم مولی (g/mol)</label>
            <input id="ph-mw" v-model="chemFields.mw" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields.mw) && 'field-invalid'" />
          </div>
        </template>
      </div>
      <div v-if="isCustomAcid || !selectedAcidRecognized" class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mt-3">
        <div>
          <label for="ph-kind" class="field-label">نوع</label>
          <select id="ph-kind" v-model="chemFields.kind" class="field-input">
            <option value="acid">اسید</option>
            <option value="base">باز</option>
          </select>
        </div>
        <div>
          <label for="ph-z" class="field-label">ظرفیت مؤثر (z)</label>
          <input id="ph-z" v-model="chemFields.z" type="text" inputmode="decimal" class="field-input" :class="bad(chemFields.z) && 'field-invalid'" />
        </div>
        <div v-if="isCustomAcid">
          <label for="ph-name" class="field-label">نام</label>
          <input id="ph-name" v-model="chemFields.name" type="text" class="field-input" placeholder="مثلاً اسید سیتریک" />
        </div>
      </div>

      <p class="mt-2 text-xs text-gray-500 dark:text-gray-400 leading-6">
        مقادیر چگالی/خلوص پیش‌فرض تقریبی‌اند؛ مقدار واقعی محصول خود را از برگه‌ی مشخصات وارد کنید. تغییر این مقادیر در
        همین صفحه ذخیره می‌شود و پایگاه‌داده‌ی کود شما را تغییر نمی‌دهد.
      </p>
    </section>

    <!-- ===================== ذخیره‌سازی ===================== -->
    <section class="rounded-xl border border-gray-200 dark:border-gray-700 px-4 py-3">
      <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-200 cursor-pointer">
        <input type="checkbox" v-model="saveToHistory" class="rounded border-gray-300 text-primary-600 focus:ring-primary-500" :disabled="!reportStore.hasActiveReport" />
        این محاسبه در تاریخچه‌ی این گزارش ذخیره شود
      </label>
      <p v-if="!reportStore.hasActiveReport" class="mt-1 text-xs text-gray-400">برای ذخیره، ابتدا یک گزارش فعال انتخاب یا ایجاد کنید.</p>
      <input v-if="saveToHistory" v-model="noteText" type="text" placeholder="یادداشت اختیاری (مثلاً «استخر مادر - بعد از اختلاط استوک A و B»)" class="field-input mt-2" />
    </section>

    <!-- ===================== عملیات ===================== -->
    <div class="flex flex-col-reverse sm:flex-row sm:items-center gap-2 sm:gap-3">
      <button type="button" @click="reset" class="w-full sm:w-auto px-5 py-3 sm:py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
        پاک‌سازی
      </button>
      <button type="button" @click="calculate" :disabled="phStore.isCalculating" class="w-full sm:w-auto px-8 py-3 sm:py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 disabled:opacity-60 text-white text-sm font-medium transition-colors">
        {{ phStore.isCalculating ? 'در حال محاسبه...' : 'محاسبه دوز' }}
      </button>
    </div>

    <!-- ===================== خطا ===================== -->
    <div v-if="phStore.errorMessage" ref="errorRef" class="rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3" role="alert">
      <p class="text-sm text-rose-800 dark:text-rose-200 leading-6">{{ phStore.errorMessage }}</p>
      <button v-if="phStore.needTitrationHint && method === 'theoretical'" type="button" @click="method = 'titration'" class="mt-2 text-sm font-medium text-rose-800 dark:text-rose-200 underline">
        رفتن به تیتراسیون واقعی
      </button>
    </div>

    <!-- ===================== نتیجه ===================== -->
    <div v-if="phStore.result && phStore.result.ok" ref="resultRef">
      <PhResultPanel :result="phStore.result" :volume-l="lastVolumeL" :target-p-h="lastTargetPH" :stale="stale" />
    </div>

    <!-- ===================== تاریخچه ===================== -->
    <PhHistoryPanel v-if="reportStore.hasActiveReport" :items="phStore.history" @delete="onDeleteHistory" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';
import { usePhStore } from '@/store/modules/phStore';
import { useReportStore } from '@/store/modules/reportStore';
import type { PhChemicalInput, PhTheoreticalRequest, PhTitrationRequest } from '@/services/apiService';
import { parseNum, fmt } from './ph/phFormat';
import PhResultPanel from './ph/PhResultPanel.vue';
import PhTitrationChart from './ph/PhTitrationChart.vue';
import PhHistoryPanel from './ph/PhHistoryPanel.vue';

type Method = 'theoretical' | 'titration';

const MAX_ROWS = 20;

const phStore = usePhStore();
const reportStore = useReportStore();

const methods: Array<{ id: Method; title: string; subtitle: string; badge?: string }> = [
  { id: 'theoretical', title: 'مدل تئوریک', subtitle: 'برای آب ساده با غلبه‌ی سیستم کربنات؛ فقط با آلکالینیتی و pH' },
  { id: 'titration', title: 'تیتراسیون واقعی', subtitle: 'از نمونه‌ی واقعی؛ مناسب محلول‌های غذایی و ترکیبی', badge: 'دقیق‌تر' }
];

// ============================================================
// State
// ============================================================
const method = ref<Method>('theoretical');
const sampleType = ref<'simple' | 'complex'>('simple');

const defaultForm = () => ({
  volume: '',
  volumeUnit: 'L' as 'L' | 'm3',
  currentPH: '',
  targetPH: '',
  temperature: '25',
  alkalinity: '',
  alkUnit: 'mg_l_caco3' as 'mg_l_caco3' | 'meq_l',
  normality: '0.1',
  sampleVolumeMl: '100'
});
const form = reactive(defaultForm());

const selectedAcidKey = ref('custom');
const chemFields = reactive({
  name: '',
  kind: 'acid' as 'acid' | 'base',
  mw: '',
  z: '',
  purity: '',
  density: ''
});

let rowSeq = 0;
const newRow = () => ({ id: ++rowSeq, volume: '', pH: '' });
const rows = ref([newRow(), newRow(), newRow(), newRow()]);

const saveToHistory = ref(false);
const noteText = ref('');

const submitted = ref(false);
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

const filteredAcidOptions = computed(() => {
  // فقط اسیدها (این ماشین‌حساب فعلاً روی مسیر اسیدی/بازی محدود به اسیدهای واقعی پایگاه‌داده است)
  return phStore.acidOptions;
});

const isCustomAcid = computed(() => selectedAcidKey.value === 'custom');

const selectedAcidOption = computed(() => {
  if (isCustomAcid.value) return null;
  const id = Number(selectedAcidKey.value.replace('fert-', ''));
  return phStore.acidOptions.find(a => a.fertilizer_id === id) || null;
});

const selectedAcidRecognized = computed(() => !!selectedAcidOption.value?.recognized);

const densityHint = computed(() => {
  const a = selectedAcidOption.value;
  if (!a) return '';
  return a.density_extrapolated ? ' (تخمین برون‌یابی‌شده - مرجع نیست)' : ' (تخمین مرجع - در صورت وجود SDS جایگزین کنید)';
});

// نقاط معتبر برای نمودار
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
  const r = phStore.result;
  return r && r.ok && r.titration && !stale.value ? r.titration.dose_ml : null;
});

// ============================================================
// وقتی اسید انتخابی عوض می‌شود، فیلدهای خلوص/چگالی/mw/z را پرمی‌کنیم
// ============================================================
watch(selectedAcidKey, () => {
  const a = selectedAcidOption.value;
  if (!a) {
    chemFields.name = '';
    chemFields.kind = 'acid';
    chemFields.mw = '';
    chemFields.z = '';
    chemFields.purity = '';
    chemFields.density = '';
    return;
  }
  chemFields.purity = String(a.concentration);
  chemFields.density = a.suggested_density_g_ml !== null && a.suggested_density_g_ml !== undefined ? String(a.suggested_density_g_ml) : '';
  chemFields.mw = a.suggested_mw !== null && a.suggested_mw !== undefined ? String(a.suggested_mw) : '';
  chemFields.z = a.suggested_z && a.suggested_z !== 'phosphoric' ? a.suggested_z : '';
  chemFields.kind = 'acid';
}, { immediate: false });

watch(() => phStore.acidOptions, opts => {
  if (opts.length && selectedAcidKey.value === 'custom') {
    selectedAcidKey.value = `fert-${opts[0].fertilizer_id}`;
  }
}, { immediate: true });

// ============================================================
// اعتبارسنجی نمایشی
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
const addRow = () => { if (rows.value.length < MAX_ROWS) rows.value.push(newRow()); };
const removeRow = (id: number) => { if (rows.value.length > 1) rows.value = rows.value.filter(r => r.id !== id); };

// ============================================================
// ساخت payload ماده‌ی شیمیایی برای API
// ============================================================
function buildChemicalInput(): PhChemicalInput | null {
  const purity = parseNum(chemFields.purity);
  const density = parseNum(chemFields.density);
  if (purity === null) return null;

  if (!isCustomAcid.value && selectedAcidOption.value) {
    const payload: PhChemicalInput = {
      fertilizer_id: selectedAcidOption.value.fertilizer_id,
      purity_pct: purity,
      density_g_ml: density ?? undefined
    };
    if (!selectedAcidRecognized.value) {
      const mw = parseNum(chemFields.mw);
      const z = parseNum(chemFields.z);
      if (mw === null || z === null) return null;
      payload.mw = mw;
      payload.z = z;
    }
    return payload;
  }

  // ماده‌ی کاملاً سفارشی
  const mw = parseNum(chemFields.mw);
  const z = parseNum(chemFields.z);
  if (mw === null || z === null || density === null) return null;
  return {
    name: chemFields.name || undefined,
    kind: chemFields.kind,
    mw,
    z,
    purity_pct: purity,
    density_g_ml: density
  };
}

// ============================================================
// Actions
// ============================================================
async function calculate() {
  submitted.value = true;
  phStore.clearResult();
  stale.value = false;

  const volume = parseNum(form.volume);
  const currentPH = currentPHValue.value;
  const targetPH = targetPHValue.value;
  const temperatureC = parseNum(form.temperature);

  if (volume === null || currentPH === null || targetPH === null || temperatureC === null) {
    phStore.errorMessage = 'حجم، pH فعلی، pH هدف و دما را کامل و معتبر وارد کنید.';
    await nextTick();
    errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  const chemical = buildChemicalInput();
  if (!chemical) {
    phStore.errorMessage = 'مشخصات ماده‌ی شیمیایی (خلوص/چگالی/جرم مولی/ظرفیت) کامل نیست.';
    await nextTick();
    errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  const volumeL = form.volumeUnit === 'm3' ? volume * 1000 : volume;
  const reportId = reportStore.currentReportId ?? undefined;

  let ok = false;
  if (method.value === 'theoretical') {
    const alk = parseNum(form.alkalinity);
    if (alk === null && sampleType.value === 'simple') {
      phStore.errorMessage = 'آلکالینیتی نمونه را وارد کنید.';
      await nextTick();
      errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
      return;
    }
    const payload: PhTheoreticalRequest = {
      volume_l: volumeL,
      current_ph: currentPH,
      target_ph: targetPH,
      temperature_c: temperatureC,
      alkalinity_value: alk ?? 0,
      alkalinity_unit: form.alkUnit,
      sample_type: sampleType.value,
      chemical,
      report_id: saveToHistory.value ? reportId : undefined,
      save: saveToHistory.value && !!reportId,
      note: noteText.value || undefined
    };
    ok = await phStore.calculateTheoretical(payload);
  } else {
    const normality = parseNum(form.normality);
    const sampleVolumeMl = parseNum(form.sampleVolumeMl);
    if (normality === null || sampleVolumeMl === null) {
      phStore.errorMessage = 'نرمالیته و حجم نمونه‌ی تیتراسیون را وارد کنید.';
      await nextTick();
      errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
      return;
    }
    const points: Array<{ volume_ml: number; ph: number }> = [];
    for (const [i, row] of rows.value.entries()) {
      const empty = row.volume.trim() === '' && row.pH.trim() === '';
      if (empty) continue;
      const v = parseNum(row.volume);
      const p = parseNum(row.pH);
      if (v === null || p === null) {
        phStore.errorMessage = `نقطه‌ی ${(i + 1).toLocaleString('fa-IR')} کامل یا معتبر نیست (هم حجم و هم pH لازم است).`;
        await nextTick();
        errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
        return;
      }
      points.push({ volume_ml: v, ph: p });
    }
    const payload: PhTitrationRequest = {
      volume_l: volumeL,
      current_ph: currentPH,
      target_ph: targetPH,
      temperature_c: temperatureC,
      normality,
      sample_volume_ml: sampleVolumeMl,
      points,
      chemical,
      report_id: saveToHistory.value ? reportId : undefined,
      save: saveToHistory.value && !!reportId,
      note: noteText.value || undefined
    };
    ok = await phStore.calculateTitration(payload);
  }

  if (ok) {
    lastVolumeL.value = volumeL;
    lastTargetPH.value = targetPH;
    await nextTick();
    resultRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'start' });
  } else {
    await nextTick();
    errorRef.value?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
  }
}

const reset = () => {
  Object.assign(form, defaultForm());
  sampleType.value = 'simple';
  rows.value = [newRow(), newRow(), newRow(), newRow()];
  submitted.value = false;
  stale.value = false;
  saveToHistory.value = false;
  noteText.value = '';
  phStore.clearResult();
};

async function onDeleteHistory(id: number) {
  await phStore.deleteHistoryItem(id);
}

// اگر بعد از محاسبه ورودی‌ها عوض شدند، نتیجه «قدیمی» علامت می‌خورد
const signature = computed(() =>
  JSON.stringify([method.value, sampleType.value, form, selectedAcidKey.value, chemFields, rows.value])
);
watch(signature, () => {
  if (phStore.result) stale.value = true;
});

// ============================================================
// بارگذاری اولیه
// ============================================================
onMounted(async () => {
  await Promise.all([phStore.loadAcidOptions(), phStore.loadContext()]);
  if (reportStore.hasActiveReport) {
    await phStore.loadHistory();
  }
});

watch(() => reportStore.currentReportId, async () => {
  await phStore.loadContext();
  if (reportStore.hasActiveReport) {
    await phStore.loadHistory();
  } else {
    phStore.history.splice(0, phStore.history.length);
  }
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
