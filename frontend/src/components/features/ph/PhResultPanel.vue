<!-- frontend/src/components/features/ph/PhResultPanel.vue -->
<!-- نتیجهٔ محاسبه: مقدار برای کل مخزن + دستور مرحله‌ای + سهم عناصر + اثر بر EC -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- مقدار اصلی -->
    <div class="p-4 sm:p-5 border-b border-gray-100 dark:border-gray-700 bg-gradient-to-l from-primary-50/70 to-transparent dark:from-primary-900/20">
      <div class="flex items-center justify-between gap-2 flex-wrap">
        <p class="text-xs text-gray-500 dark:text-gray-400">{{ result.kind === 'acid' ? 'اسید' : 'باز' }} لازم برای {{ fmt(result.tank_volume_l, 0) }} لیتر</p>
        <span v-if="result.initial_ph != null && result.final_ph != null" class="inline-flex items-center gap-1.5 rounded-full bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2.5 py-0.5 text-xs font-semibold text-gray-700 dark:text-gray-200 tabular-nums">
          <span>pH</span><span>{{ fmt(result.initial_ph, 2) }}</span>
          <svg class="w-3 h-3 text-primary-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
          <span>{{ fmt(result.final_ph, 2) }}</span>
        </span>
      </div>
      <p class="mt-1 text-2xl sm:text-3xl font-bold text-primary-700 dark:text-primary-300 tabular-nums">{{ fmtDose(result.dose_tank, result.dose_unit) }}</p>
      <p class="text-sm text-gray-600 dark:text-gray-300 mt-0.5">{{ result.chemical.name }}</p>

      <div class="mt-3 grid grid-cols-3 gap-2 text-center">
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">هر ۱۰۰۰ لیتر</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.dose_per_1000l, result.dose_unit) }}</p>
        </div>
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">مرحلهٔ ۱ (۷۰٪)</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.stage_first, result.dose_unit) }}</p>
        </div>
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">مرحلهٔ ۲ (مابقی)</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.stage_rest, result.dose_unit) }}</p>
        </div>
      </div>
    </div>

    <!-- عناصر + EC -->
    <div class="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <p class="text-sm font-bold text-gray-900 dark:text-white mb-2">عناصر واردشده به محلول</p>
        <ul v-if="elementRows.length" class="space-y-1.5">
          <li v-for="row in elementRows" :key="row.key" class="flex items-center justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-300">{{ row.label }}</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">{{ fmt(row.value, 2) }} <span class="text-[11px] font-normal text-gray-400">ppm</span></span>
          </li>
        </ul>
        <p v-else class="text-xs text-gray-500">عنصری برای این ماده ثبت نشده است.</p>
      </div>
      <div>
        <p class="text-sm font-bold text-gray-900 dark:text-white mb-2">اثر بر EC</p>
        <ul class="space-y-1.5 text-sm">
          <li class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">افزایش EC</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">+{{ fmt(result.ec_delta, 2) }} <span class="text-[11px] font-normal text-gray-400">dS/m</span></span>
          </li>
          <li v-if="result.predicted_ec != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">EC پیش‌بینی‌شده</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">{{ fmt(result.predicted_ec, 2) }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- هشدارها -->
    <div v-if="result.warnings.length" class="px-4 sm:px-5 pb-4 space-y-2">
      <div v-for="(w, i) in result.warnings" :key="i" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">{{ w }}</div>
    </div>

    <!-- جزئیات و توضیحات (آکاردئونی) -->
    <details class="group border-t border-gray-100 dark:border-gray-700">
      <summary class="flex items-center justify-between cursor-pointer select-none px-4 sm:px-5 py-3 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors list-none">
        جزئیات و توضیحات
        <svg class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
      </summary>
      <div class="px-4 sm:px-5 pb-4 space-y-3">
        <ul class="space-y-1.5 text-sm">
          <li class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">قدرت {{ result.kind === 'acid' ? 'اسید' : 'باز' }}</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">{{ fmt(result.strength_meq_l, 2) }} <span class="text-[11px] font-normal text-gray-400">meq/L</span></span>
          </li>
          <li v-if="result.water_alkalinity_meq_l != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">آلکالینیتی آب</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">{{ fmt(result.water_alkalinity_meq_l, 2) }} <span class="text-[11px] font-normal text-gray-400">meq/L</span></span>
          </li>
          <li v-if="result.base_ec != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">EC آخرین محاسبهٔ گزارش</span>
            <span class="font-bold text-gray-900 dark:text-white tabular-nums">{{ fmt(result.base_ec, 2) }}</span>
          </li>
        </ul>

        <p v-if="result.mode === 'trial' && result.scale_factor" class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">
          نمونهٔ {{ fmt(result.sample_volume_l || 0, 2) }} لیتری {{ fmtDose(result.sample_dose || 0, result.dose_unit) }} مصرف کرد
          ({{ result.trial_method === 'interpolated' ? 'میان‌یابی روی منحنی' : 'قرائت مستقیم' }})؛ ضریب مقیاس‌دهی به مخزن ×{{ fmt(result.scale_factor, 0) }}.
        </p>
        <p v-else-if="result.dose_basis_volume_l" class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">رسپی برای {{ fmt(result.dose_basis_volume_l, 0) }} لیتر به حجم مخزن مقیاس داده شد.</p>

        <p class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">
          جرم محصول تجاری ≈ {{ fmtMassG(result.commercial_mass_g) }} · ماده خالص ≈ {{ fmtMassG(result.pure_mass_g) }}
          <span v-if="result.chemical.density_g_ml"> · چگالی {{ fmt(result.chemical.density_g_ml, 3) }} g/mL</span>
        </p>

        <ul class="space-y-1 text-[11px] leading-5 text-gray-500 dark:text-gray-400 list-disc pr-4">
          <li>مرحلهٔ ۱ را اضافه کنید، خوب هم بزنید و pH را بخوانید؛ سپس مابقی را با تنظیم نهایی اضافه کنید.</li>
          <li>پس از «اعمال در محاسبهٔ کود»، این مقادیر مثل آب یک منبع پایه لحاظ می‌شوند و سهم کودهای دیگر کم می‌شود.</li>
          <li>اگر EC را قبل و بعد از اصلاح با دستگاه خواندید، در بخش «ثبت» وارد کنید تا در تاریخچه بماند.</li>
        </ul>
      </div>
    </details>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PhAdjustmentResult } from '@/services/apiService';
import { fmt, fmtDose, fmtMassG, ELEMENT_LABELS } from './phFormat';

const props = defineProps<{ result: PhAdjustmentResult }>();

const elementRows = computed(() =>
  Object.entries(props.result.element_contributions || {})
    .filter(([, v]) => Number(v) > 0)
    .map(([key, value]) => ({ key, label: ELEMENT_LABELS[key] || key, value: Number(value) }))
);
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>