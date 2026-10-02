<!-- frontend/src/components/features/calc/PhAdjustmentBanner.vue -->
<!--
  اصلاح pH اعمال‌شده در این محاسبه (از تب PH).
  عناصر اسید/باز مثل آب یک منبع پایه‌اند و از قبل در «عناصر تأمین‌شده»، تعادل یونی و EC
  لحاظ شده‌اند؛ این کارت فقط نشان می‌دهد چه چیزی اعمال شده است.
-->
<template>
  <div class="rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50/70 dark:bg-emerald-900/10 px-3.5 py-3">
    <div class="flex items-start justify-between gap-3 flex-wrap">
      <div class="min-w-0">
        <p class="text-sm font-bold text-emerald-800 dark:text-emerald-200">
          {{ adjustment.kind === 'acid' ? 'اسید' : 'باز' }} تنظیم pH: {{ adjustment.chemical_name }}
        </p>
        <p class="text-xs text-emerald-900/80 dark:text-emerald-100/80 mt-1 leading-6">
          {{ fmtDose(adjustment.dose_tank, adjustment.dose_unit) }} برای {{ fmt(adjustment.tank_volume_l, 0) }} لیتر
          ({{ fmtDose(adjustment.dose_per_1000l, adjustment.dose_unit) }} در هر ۱۰۰۰ لیتر)
          <template v-if="adjustment.initial_ph != null && adjustment.final_ph != null">
            · pH {{ fmt(adjustment.initial_ph, 2) }} ← {{ fmt(adjustment.final_ph, 2) }}
          </template>
        </p>
        <p class="text-xs text-emerald-900/80 dark:text-emerald-100/80 leading-6">
          عناصر واردشده: {{ contribText }}
          <template v-if="adjustment.ec_delta"> · EC حدود +{{ fmt(adjustment.ec_delta, 2) }}</template>
        </p>
      </div>
    </div>
    <p class="mt-1.5 text-[11px] text-emerald-800/70 dark:text-emerald-200/70 leading-5">
      این عناصر در سهم کودها کسر شده‌اند؛ اسید را همراه کودها در مخزن (مرحلهٔ pH) اضافه کنید.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OptimizationResponse } from '@/types';
import { fmt, fmtDose } from '../ph/phFormat';

type Adjustment = NonNullable<OptimizationResponse['ph_adjustment']>;
const props = defineProps<{ adjustment: Adjustment }>();

const contribText = computed(() =>
  Object.entries(props.adjustment.element_contributions || {})
    .filter(([, v]) => Number(v) > 0)
    .map(([k, v]) => `${k} ${fmt(Number(v), 1)} ppm`)
    .join('، ') || '—'
);
</script>
