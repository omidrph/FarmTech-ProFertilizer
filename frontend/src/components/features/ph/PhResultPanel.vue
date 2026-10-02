<!-- frontend/src/components/features/ph/PhResultPanel.vue -->
<!-- نتیجهٔ محاسبه: مقدار برای کل مخزن + دستور مرحله‌ای + سهم عناصر + اثر بر EC -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- مقدار اصلی -->
    <div class="p-4 sm:p-5 border-b border-gray-100 dark:border-gray-700 bg-gradient-to-l from-primary-50/70 to-transparent dark:from-primary-900/20">
      <p class="text-xs text-gray-500 dark:text-gray-400">
        {{ result.kind === 'acid' ? 'اسید' : 'باز' }} لازم برای {{ fmt(result.tank_volume_l, 0) }} لیتر
        <span v-if="result.initial_ph != null && result.final_ph != null">
          · pH {{ fmt(result.initial_ph, 2) }} ← {{ fmt(result.final_ph, 2) }}
        </span>
      </p>
      <p class="mt-1 text-2xl sm:text-3xl font-bold text-primary-700 dark:text-primary-300 tabular-nums">
        {{ fmtDose(result.dose_tank, result.dose_unit) }}
      </p>
      <p class="text-sm text-gray-600 dark:text-gray-300 mt-0.5">{{ result.chemical.name }}</p>

      <div class="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-2 text-center">
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">به‌ازای هر ۱۰۰۰ لیتر (برای رسپی)</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.dose_per_1000l, result.dose_unit) }}</p>
        </div>
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">مرحلهٔ ۱ (۷۰٪) — بعد هم بزنید و pH بخوانید</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.stage_first, result.dose_unit) }}</p>
        </div>
        <div class="rounded-lg bg-white/80 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 px-2 py-2">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">مرحلهٔ ۲ (مابقی، با تنظیم نهایی)</p>
          <p class="text-sm font-bold text-gray-900 dark:text-white tabular-nums">{{ fmtDose(result.stage_rest, result.dose_unit) }}</p>
        </div>
      </div>

      <p v-if="result.mode === 'trial' && result.scale_factor" class="mt-3 text-xs text-gray-500 dark:text-gray-400 leading-6">
        نمونهٔ {{ fmt(result.sample_volume_l || 0, 2) }} لیتری
        {{ fmtDose(result.sample_dose || 0, result.dose_unit) }} مصرف کرد
        ({{ result.trial_method === 'interpolated' ? 'میان‌یابی روی منحنی' : 'قرائت مستقیم' }}) ؛
        ضریب مقیاس‌دهی به مخزن: ×{{ fmt(result.scale_factor, 0) }}
      </p>
      <p v-else-if="result.dose_basis_volume_l" class="mt-3 text-xs text-gray-500 dark:text-gray-400 leading-6">
        رسپی برای {{ fmt(result.dose_basis_volume_l, 0) }} لیتر به حجم مخزن مقیاس داده شد.
      </p>
    </div>

    <!-- سهم عناصر + EC -->
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
        <p class="mt-2 text-[11px] text-gray-500 dark:text-gray-400 leading-5">
          پس از «اعمال در محاسبهٔ کود»، این مقادیر مثل آب یک منبع پایه لحاظ می‌شوند و سهم کودهای دیگر به‌طور خودکار کم می‌شود.
        </p>
      </div>

      <div>
        <p class="text-sm font-bold text-gray-900 dark:text-white mb-2">اثر بر EC و تعادل یونی</p>
        <ul class="space-y-1.5 text-sm">
          <li class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">افزایش EC (تخمینی)</span>
            <span class="font-bold tabular-nums text-gray-900 dark:text-white">+{{ fmt(result.ec_delta, 2) }} <span class="text-[11px] font-normal text-gray-400">dS/m</span></span>
          </li>
          <li v-if="result.base_ec != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">EC آخرین محاسبهٔ گزارش</span>
            <span class="tabular-nums text-gray-900 dark:text-white">{{ fmt(result.base_ec, 2) }}</span>
          </li>
          <li v-if="result.predicted_ec != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">EC پیش‌بینی با این اصلاح</span>
            <span class="font-bold tabular-nums text-gray-900 dark:text-white">{{ fmt(result.predicted_ec, 2) }}</span>
          </li>
          <li class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">قدرت {{ result.kind === 'acid' ? 'اسید' : 'باز' }}</span>
            <span class="tabular-nums text-gray-900 dark:text-white">{{ fmt(result.strength_meq_l, 2) }} <span class="text-[11px] text-gray-400">meq/L</span></span>
          </li>
          <li v-if="result.water_alkalinity_meq_l != null" class="flex items-center justify-between">
            <span class="text-gray-600 dark:text-gray-300">آلکالینیتی آب</span>
            <span class="tabular-nums text-gray-900 dark:text-white">{{ fmt(result.water_alkalinity_meq_l, 2) }} <span class="text-[11px] text-gray-400">meq/L</span></span>
          </li>
        </ul>
        <p class="mt-2 text-[11px] text-gray-500 dark:text-gray-400 leading-5">
          اگر EC را قبل و بعد از اصلاح با دستگاه خواندید، در بخش «ثبت» وارد کنید تا در تاریخچه بماند.
        </p>
      </div>
    </div>

    <!-- جرم -->
    <div class="px-4 sm:px-5 pb-4 text-[11px] text-gray-500 dark:text-gray-400 leading-5">
      جرم محصول تجاری ≈ {{ fmtMassG(result.commercial_mass_g) }} · ماده خالص ≈ {{ fmtMassG(result.pure_mass_g) }}
      <span v-if="result.chemical.density_g_ml"> · چگالی {{ fmt(result.chemical.density_g_ml, 3) }} g/mL{{ result.chemical.density_is_reference ? ' (مرجع تقریبی)' : '' }}</span>
    </div>

    <!-- هشدارها -->
    <div v-if="result.warnings.length" class="px-4 sm:px-5 pb-4 space-y-2">
      <div v-for="(w, i) in result.warnings" :key="i" class="rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200">
        {{ w }}
      </div>
    </div>
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
