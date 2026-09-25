<!-- frontend/src/components/features/ph/PhResultPanel.vue -->
<!-- نمایش نتیجه‌ی ماشین‌حساب pH (پاسخ backend: DoseResponse) -->
<template>
  <div class="space-y-3 sm:space-y-4" :class="stale ? 'opacity-60' : ''">

    <p v-if="stale" class="text-xs text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg px-3 py-2">
      ورودی‌ها تغییر کرده‌اند؛ برای نتیجه‌ی به‌روز دوباره «محاسبه دوز» را بزنید.
    </p>

    <!-- بدون نیاز به اصلاح -->
    <div
      v-if="result.method === 'no-adjustment'"
      class="rounded-2xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 p-4 sm:p-5 text-center"
    >
      <p class="text-base font-bold text-emerald-700 dark:text-emerald-300">نیازی به اصلاح نیست</p>
      <p class="text-sm text-emerald-700/80 dark:text-emerald-300/80 mt-1">pH فعلی با pH هدف یکسان است.</p>
    </div>

    <template v-else>
      <!-- مقدار پیشنهادی -->
      <section class="rounded-2xl border border-primary-200 dark:border-primary-800 bg-primary-50/60 dark:bg-primary-900/15 p-4 sm:p-5">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">
              مقدار پیشنهادی {{ result.chemical.name }} ({{ fmt(result.chemical.purity_pct, 1) }}٪)
            </p>
            <p class="mt-1 text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtVolumeL(result.commercial_volume_l) }}</p>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 tabular-nums">
              ≈ {{ fmtVolumeL(perThousand) }} به ازای هر ۱٬۰۰۰ لیتر
            </p>
          </div>
          <span class="flex-shrink-0 text-[11px] font-medium px-2 py-1 rounded-full bg-white dark:bg-gray-800 border border-primary-200 dark:border-primary-800 text-primary-700 dark:text-primary-300">
            {{ result.method === 'titration' ? 'تیتراسیون واقعی' : 'مدل تئوریک' }}
          </span>
        </div>

        <p v-if="result.chemical.source === 'fertilizer_db'" class="mt-2 text-[11px] text-primary-700/80 dark:text-primary-300/80">
          از پایگاه‌داده‌ی کود شما (کود اسیدیِ واقعی) خوانده شده است.
        </p>
        <p v-if="result.chemical.density_is_reference" class="mt-1 text-[11px] text-amber-700/90 dark:text-amber-300/80">
          چگالی از جدول مرجع صنعتی تخمین زده شده{{ result.chemical.density_extrapolated ? ' (برون‌یابی‌شده - با احتیاط بیشتر استفاده کنید)' : '' }}؛
          برای دقت بالاتر، چگالی واقعی محصول را از برگه‌ی مشخصات (SDS) وارد کنید.
        </p>

        <p
          v-if="result.sensitivity"
          class="mt-3 text-xs text-gray-600 dark:text-gray-300 bg-white/70 dark:bg-gray-800/60 rounded-lg px-3 py-2 leading-6"
        >
          بازه‌ی حساسیت (خطای اندازه‌گیری آلکالینیتی ±۱۰٪ و pH ±۰٫۱):
          <span class="font-semibold tabular-nums">{{ fmtVolumeL(result.sensitivity.min_l) }}</span>
          تا
          <span class="font-semibold tabular-nums">{{ fmtVolumeL(result.sensitivity.max_l) }}</span>
        </p>

        <p class="mt-3 text-xs text-primary-800 dark:text-primary-200 leading-6">
          این عدد یک <strong>تخمین</strong> است، نه مقدار قطعی تزریق. دقت واقعی فقط پس از اعتبارسنجی با نمونه‌ی خودتان مشخص می‌شود.
        </p>
      </section>

      <!-- برنامه‌ی تزریق مرحله‌ای -->
      <section class="rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-3">برنامه‌ی پیشنهادی تزریق مرحله‌ای</h4>
        <ol class="space-y-2.5">
          <li v-for="(step, i) in stagedPlan" :key="i" class="flex items-start gap-3">
            <span class="w-6 h-6 rounded-full bg-primary-600 text-white text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">{{ (i + 1).toLocaleString('fa-IR') }}</span>
            <span class="text-sm text-gray-700 dark:text-gray-200 leading-6">{{ step }}</span>
          </li>
        </ol>
      </section>

      <!-- جزئیات محاسبه -->
      <section class="rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-3">جزئیات محاسبه</h4>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 divide-y sm:divide-y-0 divide-gray-100 dark:divide-gray-700">
          <div v-for="row in detailRows" :key="row.label" class="flex items-baseline justify-between gap-3 py-2 sm:border-b sm:border-gray-100 sm:dark:border-gray-700">
            <dt class="text-xs text-gray-500 dark:text-gray-400">{{ row.label }}</dt>
            <dd class="text-sm font-semibold text-gray-900 dark:text-white tabular-nums text-left">{{ row.value }}</dd>
          </div>
        </dl>
      </section>

      <!-- هشدارها -->
      <ul
        v-if="result.warnings.length"
        class="rounded-2xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3 space-y-1.5"
      >
        <li v-for="w in result.warnings" :key="w" class="flex items-start gap-2 text-sm text-amber-900 dark:text-amber-200 leading-6">
          <svg class="w-4 h-4 mt-1 flex-shrink-0 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span>{{ w }}</span>
        </li>
      </ul>

      <!-- فرض‌های مدل -->
      <details v-if="result.method === 'theoretical'" class="rounded-2xl border border-gray-200 dark:border-gray-700 px-4 py-3 group">
        <summary class="text-sm font-medium text-gray-700 dark:text-gray-200 cursor-pointer select-none">فرض‌های مدل تئوریک</summary>
        <ul class="mt-2 space-y-1 text-xs text-gray-600 dark:text-gray-400 leading-6 list-disc pr-4">
          <li>سیستم بسته است؛ CO₂ با هوا تبادل نمی‌کند و مجموع کربن معدنی (C<sub>T</sub>) ثابت می‌ماند.</li>
          <li>آلکالینیتی فقط از کربنات، بی‌کربنات و هیدروکسید می‌آید (فسفات، آمونیوم و اسیدهای آلی نادیده‌اند).</li>
          <li>ضریب فعالیت ۱ فرض شده و از قدرت یونی صرف‌نظر شده است.</li>
          <li>ثابت‌های تعادل بر اساس دمای واردشده محاسبه می‌شوند.</li>
        </ul>
      </details>

      <!-- ایمنی -->
      <section class="rounded-2xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 p-4 sm:p-5">
        <h4 class="text-sm font-bold text-rose-800 dark:text-rose-300 mb-2">ایمنی</h4>
        <p class="text-xs text-rose-800/90 dark:text-rose-200/90 leading-6 mb-2">
          این محاسبه جایگزین برگه‌ی ایمنی ماده (SDS)، تجهیزات حفاظت فردی و دستورالعمل اجرایی محل کار نیست.
        </p>
        <ul class="space-y-1 text-xs text-rose-800/90 dark:text-rose-200/90 leading-6 list-disc pr-4">
          <li>برای اسیدها و بازهای غلیظ از تجهیزات حفاظت فردی مناسب استفاده کنید.</li>
          <li>در رقیق‌سازی، اسید را به آب اضافه کنید، نه آب را به اسید.</li>
          <li>تزریق را با اختلاط مناسب و کنترل pH انجام دهید و از تجهیزات سازگار با ماده‌ی خورنده استفاده کنید.</li>
          <li>هرگز کل دوز محاسبه‌شده را بدون اعتبارسنجی عملی یک‌باره تزریق نکنید.</li>
        </ul>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PhDoseResponse } from '@/services/apiService';
import { fmt, fmtVolumeL, fmtMassG } from './phFormat';

const props = defineProps<{
  result: PhDoseResponse;
  volumeL: number;
  targetPH: number;
  stale: boolean;
}>();

const perThousand = computed(() => (props.result.commercial_volume_l / props.volumeL) * 1000);

const stagedPlan = computed(() => {
  const half = props.result.commercial_volume_l * 0.5;
  const rest = props.result.commercial_volume_l - half;
  return [
    `ابتدا حدود ۵۰٪ دوز (${fmtVolumeL(half)}) را با اختلاط مناسب و به‌تدریج تزریق کنید.`,
    'پس از ۵ تا ۱۰ دقیقه اختلاط، pH را با pH متر کالیبره اندازه بگیرید.',
    `بر اساس pH اندازه‌گیری‌شده، مقدار باقی‌مانده (حداکثر حدود ${fmtVolumeL(rest)}) را در یک یا دو مرحله‌ی کوچک اصلاح کنید.`,
    `تا رسیدن به pH ${fmt(props.targetPH, 2)} اندازه‌گیری و اصلاح را تکرار کنید و مقدار نهایی مصرف‌شده را برای کالیبراسیون ثبت کنید.`
  ];
});

const detailRows = computed(() => {
  const r = props.result;
  const rows: Array<{ label: string; value: string }> = [
    { label: 'معادل شیمیایی کل', value: `${fmt(r.total_meq, 0)} meq` },
    {
      label: 'ظرفیت مؤثر (z)',
      value: r.chemical.z === 'phosphoric' ? `${fmt(r.effective_z, 2)} (وابسته به pH)` : fmt(r.effective_z, 2)
    },
    { label: 'جرم ماده‌ی خالص', value: fmtMassG(r.pure_mass_g) },
    { label: 'جرم ماده‌ی تجاری', value: fmtMassG(r.commercial_mass_g) }
  ];

  if (r.theoretical) {
    rows.push(
      { label: 'آلکالینیتی اولیه', value: `${fmt(r.theoretical.initial_alk_mg_l, 1)} mg/L as CaCO₃` },
      { label: 'آلکالینیتی در pH هدف', value: `${fmt(r.theoretical.target_alk_mg_l, 1)} mg/L as CaCO₃` },
      { label: 'اختلاف آلکالینیتی', value: `${fmt(r.theoretical.delta_meq_l, 3)} meq/L` },
      { label: 'کربن معدنی کل (C_T)', value: `${fmt(r.theoretical.ct_mmol_l, 3)} mmol/L` }
    );
  }

  if (r.titration) {
    rows.push(
      { label: 'بازه‌ی میان‌یابی', value: `${fmt(r.titration.from_volume_ml, 2)} تا ${fmt(r.titration.to_volume_ml, 2)} mL` },
      { label: 'تیترانت در pH هدف', value: `${fmt(r.titration.dose_ml, 3)} mL` },
      { label: 'معادل در هر لیتر نمونه', value: `${fmt(r.titration.meq_per_l, 3)} meq/L` }
    );
  }

  return rows;
});
</script>
