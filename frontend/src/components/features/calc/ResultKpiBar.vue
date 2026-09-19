<!-- frontend/src/components/features/calc/ResultKpiBar.vue -->
<!--
  نوار خلاصه نتیجه: مهم‌ترین اعدادی که کاربر بلافاصله بعد از محاسبه
  می‌خواهد ببیند. جایگزین کارت‌های پراکنده و بلند قبلی.
-->
<template>
  <div class="grid grid-cols-2 lg:grid-cols-5 gap-2 sm:gap-3">
    <article
      v-for="item in items"
      :key="item.key"
      class="rounded-xl border bg-white dark:bg-gray-800 p-3 flex flex-col justify-between"
      :class="item.border"
    >
      <p class="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1">
        {{ item.label }}
        <button
          v-if="item.hint"
          type="button"
          class="w-3.5 h-3.5 rounded-full border border-gray-300 dark:border-gray-600 text-[8px] leading-none text-gray-400 flex items-center justify-center"
          :title="item.hint"
          aria-label="راهنما"
        >i</button>
      </p>
      <p class="mt-1 flex items-baseline gap-1">
        <span class="text-lg sm:text-xl font-bold tabular-nums" :class="item.color">{{ item.value }}</span>
        <span v-if="item.unit" class="text-[10px] text-gray-400">{{ item.unit }}</span>
      </p>
      <p v-if="item.note" class="text-[10px] mt-0.5 truncate" :class="item.noteColor || 'text-gray-400'">
        {{ item.note }}
      </p>
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

const items = computed(() => {
  const result = props.result;
  const phNote =
    result.ph_min !== undefined && result.ph_max !== undefined
      ? `بازه محتمل ${format(result.ph_min)} تا ${format(result.ph_max)}`
      : result.ph_status || '';

  return [
    {
      key: 'accuracy',
      label: 'دقت رسیدن به هدف',
      value: format(accuracy.value, 1),
      unit: '٪',
      color: accuracy.value >= 95 ? 'text-emerald-600 dark:text-emerald-400' : accuracy.value >= 85 ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400',
      border: 'border-gray-200 dark:border-gray-700',
      note: result.is_converged ? 'محاسبه همگرا شد' : 'همگرایی کامل نشد',
      noteColor: result.is_converged ? 'text-emerald-500' : 'text-amber-500',
      hint: 'اختلاف کل بین عناصر هدف و عناصر تأمین‌شده'
    },
    {
      key: 'ec',
      label: 'EC نهایی',
      value: format(result.ec, 2),
      unit: 'dS/m',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: result.ec_status || 'محدوده مطلوب ۰٫۸ تا ۲٫۵',
      noteColor: statusColor(result.ec_status),
      hint: 'شوری محلول نهایی؛ محدوده متداول ۰٫۸ تا ۲٫۵'
    },
    {
      key: 'ph',
      label: 'pH تخمینی',
      value: format(result.ph, 2),
      unit: '',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: phNote,
      noteColor: statusColor(result.ph_status),
      hint: 'عدد تخمینی است و جایگزین اندازه‌گیری با pH‌متر نمی‌شود'
    },
    {
      key: 'cost',
      label: 'هزینه کل',
      value: Math.round(Number(result.cost_total) || 0).toLocaleString('fa-IR'),
      unit: 'تومان',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: '',
      noteColor: '',
      hint: 'بر اساس قیمت هر کیلو ثبت‌شده برای کودها'
    },
    {
      key: 'count',
      label: 'کود مصرفی',
      value: String(props.usedCount),
      unit: 'قلم',
      color: 'text-gray-900 dark:text-white',
      border: 'border-gray-200 dark:border-gray-700',
      note: '',
      noteColor: '',
      hint: 'تعداد کودهایی که در ترکیب نهایی وزن گرفته‌اند'
    }
  ];
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
