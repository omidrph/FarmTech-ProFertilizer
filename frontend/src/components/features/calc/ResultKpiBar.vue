<!-- frontend/src/components/features/calc/ResultKpiBar.vue -->
<!--
  نوار خلاصه نتیجه، با آیکون اختصاصی و معنادار برای هر شاخص
  (نسخه قبلی هیچ آیکونی نداشت؛ دکمه کوچک «i» هم به نظر شلخته می‌آمد
  و حذف شد — توضیح کوتاه زیر هر عدد به‌جای آن کافی است)
-->
<template>
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-3">
    <article
      v-for="item in items"
      :key="item.key"
      class="rounded-xl border bg-white dark:bg-gray-800 p-3 flex items-start gap-2.5"
      :class="item.border"
    >
      <span class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" :class="item.iconWrap">
        <span v-html="item.icon" class="w-4 h-4" :class="item.iconColor"></span>
      </span>

      <div class="min-w-0 flex-1">
        <p class="text-[11px] text-gray-500 dark:text-gray-400 truncate">{{ item.label }}</p>
        <p class="mt-0.5 flex items-baseline gap-1">
          <span class="text-lg sm:text-xl font-bold tabular-nums" :class="item.color">{{ item.value }}</span>
          <span v-if="item.unit" class="text-[10px] text-gray-400">{{ item.unit }}</span>
        </p>
        <p v-if="item.note" class="text-[10px] mt-0.5 truncate" :class="item.noteColor || 'text-gray-400'">
          {{ item.note }}
        </p>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OptimizationResponse } from '@/types';

const props = defineProps<{
  result: OptimizationResponse;
  usedCount: number;
}>();

const format = (value: unknown, digits = 2): string => {
  const parsed = Number(value);
  return isFinite(parsed) ? parsed.toFixed(digits) : '—';
};

const accuracy = computed(() => Math.max(0, 100 - (Number(props.result.residual_error) || 0) * 100));

const statusColor = (status?: string): string => {
  if (!status) return 'text-gray-500 dark:text-gray-400';
  if (status.includes('مطلوب')) return 'text-emerald-600 dark:text-emerald-400';
  if (status.includes('بسیار') || status.includes('بحرانی')) return 'text-rose-600 dark:text-rose-400';
  return 'text-amber-600 dark:text-amber-400';
};

// ===== آیکون‌های اختصاصی (svg خام، هر کدام متناظر با معنای کارت) =====
const ICONS = {
  target: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="0.6" fill="currentColor"/></svg>`,
  pulse: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-7 4 14 2-7h6"/></svg>`,
  wallet: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7.5A1.5 1.5 0 014.5 6h13A1.5 1.5 0 0119 7.5V9H4.5A1.5 1.5 0 013 7.5z"/><path d="M3 9h16.5A1.5 1.5 0 0121 10.5v7a1.5 1.5 0 01-1.5 1.5H4.5A1.5 1.5 0 013 17.5V9z"/><circle cx="16.5" cy="14" r="1.1" fill="currentColor" stroke="none"/></svg>`,
  layers: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4.5-8 4.5-8-4.5L12 3z"/><path d="M4 12l8 4.5 8-4.5"/><path d="M4 16.5l8 4.5 8-4.5"/></svg>`
};

const items = computed(() => {
  const result = props.result;

  return [
    {
      key: 'accuracy',
      label: 'دقت رسیدن به هدف',
      value: format(accuracy.value, 1),
      unit: '٪',
      icon: ICONS.target,
      iconWrap: 'bg-primary-50 dark:bg-primary-900/30',
      iconColor: 'text-primary-600 dark:text-primary-400',
      color: accuracy.value >= 95 ? 'text-emerald-600 dark:text-emerald-400' : accuracy.value >= 85 ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400',
      border: 'border-gray-200 dark:border-gray-700',
      note: result.is_converged ? 'محاسبه همگرا شد' : 'همگرایی کامل نشد',
      noteColor: result.is_converged ? 'text-emerald-500' : 'text-amber-500'
    },
    {
      key: 'ec',
      label: 'EC نهایی',
      value: format(result.ec, 2),
      unit: 'dS/m',
      icon: ICONS.pulse,
      iconWrap: 'bg-blue-50 dark:bg-blue-900/30',
      iconColor: 'text-blue-600 dark:text-blue-400',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: result.ec_status || 'محدوده مطلوب ۰٫۸ تا ۲٫۵',
      noteColor: statusColor(result.ec_status)
    },
    {
      key: 'cost',
      label: 'هزینه کل',
      value: Math.round(Number(result.cost_total) || 0).toLocaleString('fa-IR'),
      unit: 'تومان',
      icon: ICONS.wallet,
      iconWrap: 'bg-emerald-50 dark:bg-emerald-900/30',
      iconColor: 'text-emerald-600 dark:text-emerald-400',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: '',
      noteColor: ''
    },
    {
      key: 'count',
      label: 'کود مصرفی',
      value: String(props.usedCount),
      unit: 'قلم',
      icon: ICONS.layers,
      iconWrap: 'bg-amber-50 dark:bg-amber-900/30',
      iconColor: 'text-amber-600 dark:text-amber-400',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: '',
      noteColor: ''
    }
  ];
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
