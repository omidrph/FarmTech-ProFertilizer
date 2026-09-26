<!-- frontend/src/components/features/calc/PhCorrectionBanner.vue -->
<!--
  خلاصه‌ی آخرین «اصلاح pH» ثبت‌شده برای این گزارش (از تب PH).
  ------------------------------------------------------------
  عمداً به‌صورت یک بلوک کاملاً جدا از جدول مخزن‌های A/B/C نمایش داده
  می‌شود، نه به‌عنوان یک ردیف داخل آن جدول: مقادیر مخزن A/B/C برای
  «محلول استوکِ غلیظ» است، در حالی که این دوز اصلاحی برای «محلول
  نهاییِ رقیق‌شده‌ی داخل مخزن اصلی» محاسبه شده - قاطی‌کردنشان در یک
  جدول با یک واحد، گمراه‌کننده و از نظر غلظت/حجم اشتباه است.
  فقط خواندنی است؛ بهینه‌ساز را دوباره اجرا نمی‌کند.
-->
<template>
  <div class="rounded-xl border border-sky-200 dark:border-sky-800 bg-sky-50/60 dark:bg-sky-900/10 p-3 sm:p-4">
    <div class="flex items-start justify-between gap-3 flex-wrap">
      <div class="min-w-0">
        <p class="text-xs font-bold text-sky-800 dark:text-sky-300 flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          آخرین اصلاح pH ثبت‌شده (از تب PH)
        </p>
        <p class="mt-1 text-sm text-sky-900 dark:text-sky-100">
          {{ correction.chemical_name || 'ماده‌ی اصلاحی' }} -
          <span class="font-bold">{{ doseText }}</span>
          برای محلول نهایی {{ volumeText }}
        </p>
        <p class="mt-1 text-[11px] text-sky-800/70 dark:text-sky-300/70">
          {{ formatDate(correction.created_at) }}
          <span v-if="correction.inputs?.current_ph && correction.inputs?.target_ph">
            · pH {{ fmt(correction.inputs.current_ph) }} → {{ fmt(correction.inputs.target_ph) }}
          </span>
        </p>
      </div>
      <span class="flex-shrink-0 text-[10px] font-medium px-2 py-1 rounded-full bg-white dark:bg-gray-800 border border-sky-200 dark:border-sky-800 text-sky-700 dark:text-sky-300">
        برای مخزن نهایی - نه استوک
      </span>
    </div>

    <div v-if="elementEntries.length" class="mt-3 pt-3 border-t border-sky-200/60 dark:border-sky-800/60">
      <p class="text-[11px] text-sky-800/80 dark:text-sky-300/80 mb-1.5">
        این ماده به عناصر «تأمین‌شده» (بخش بالا) هم اضافه شده است:
      </p>
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="[el, val] in elementEntries"
          :key="el"
          class="text-[11px] px-2 py-1 rounded-lg bg-white dark:bg-gray-800 border border-sky-200 dark:border-sky-800 text-sky-800 dark:text-sky-200 tabular-nums"
        >
          {{ el }}: +{{ fmt(val, 1) }} mg/L
        </span>
      </div>
    </div>

    <p class="mt-3 text-[11px] text-sky-800/70 dark:text-sky-300/70 leading-5">
      این مقدار جزو فرمول رسمی مخزن‌های A/B/C (استوک) نیست؛ بعد از ساخت و رقیق‌سازی استوک، مستقیماً به مخزن نهایی اضافه می‌شود. برای بررسی یا ثبت اندازه‌گیری جدید به تب «PH» بروید.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PhHistoryItem } from '@/services/apiService';

const props = defineProps<{ correction: PhHistoryItem }>();

const fmt = (value: number, digits = 2): string => {
  if (!Number.isFinite(value)) return '—';
  return value.toLocaleString('fa-IR', { maximumFractionDigits: digits });
};

const doseText = computed(() => {
  const l = props.correction.outputs?.commercial_volume_l;
  if (!Number.isFinite(l)) return '—';
  return l < 1 ? `${fmt(l * 1000, 1)} میلی‌لیتر` : `${fmt(l, 2)} لیتر`;
});

const volumeText = computed(() => {
  const v = props.correction.inputs?.volume_l;
  return Number.isFinite(v) ? `${fmt(v, 0)} لیتری` : '';
});

const elementEntries = computed(() => {
  const contrib = props.correction.outputs?.element_contributions_mg_l as Record<string, number> | undefined;
  if (!contrib) return [] as Array<[string, number]>;
  return Object.entries(contrib).filter(([, v]) => Number.isFinite(v) && v > 0);
});

const formatDate = (iso: string): string => {
  try {
    return new Date(iso).toLocaleString('fa-IR', { dateStyle: 'medium', timeStyle: 'short' });
  } catch {
    return iso;
  }
};
</script>
