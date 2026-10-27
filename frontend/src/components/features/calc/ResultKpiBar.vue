
<!-- frontend/src/components/features/calc/ResultKpiBar.vue -->
<!--
  نوار خلاصه نتیجه. «دقت رسیدن به هدف» چون ذاتاً یک درصد است، به‌شکل
  نمودار دایره‌ای (همان زبان تصویری بخش عناصر) نمایش داده می‌شود؛ بقیه
  شاخص‌ها (EC، هزینه، تعداد کود) چون عدد مطلق‌اند، کارت آیکون‌دار ساده
  می‌مانند.
-->
<template>
  <div class="grid grid-cols-2 lg:grid-cols-5 gap-2 sm:gap-3">

    <!-- خطای ماکرو و میکرو (جدا): تا ۵٪ سبز، ۵ تا ۱۰٪ زرد، بالای ۱۰٪ قرمز -->
    <article
      v-for="g in errorCards"
      :key="g.group"
      class="rounded-xl border bg-white dark:bg-gray-800 p-3 flex items-center gap-3"
      :class="LEVEL_CLASS[g.level].border"
    >
      <div class="relative w-14 h-14 flex-shrink-0">
        <svg viewBox="0 0 56 56" class="w-full h-full">
          <circle cx="28" cy="28" r="21" fill="none" class="stroke-gray-100 dark:stroke-gray-700" stroke-width="5" />
          <circle
            cx="28" cy="28" r="21" fill="none" stroke-width="5" stroke-linecap="round"
            :class="LEVEL_CLASS[g.level].ring"
            :stroke-dasharray="RING_CIRC"
            :stroke-dashoffset="RING_CIRC * (1 - g.coverage / 100)"
            transform="rotate(-90 28 28)"
            style="transition: stroke-dashoffset 0.6s ease"
          />
          <!-- حلقهٔ بیرونی قرمز: بیش‌تأمین (مثل پوشش عناصر هدف) -->
          <circle
            v-if="g.over > 0.5"
            cx="28" cy="28" r="26" fill="none" stroke-width="2" stroke-linecap="round"
            class="stroke-rose-500"
            :stroke-dasharray="OUTER_CIRC"
            :stroke-dashoffset="OUTER_CIRC * (1 - Math.min(g.over / 50, 1))"
            transform="rotate(-90 28 28)"
          />
        </svg>
      </div>
      <div class="min-w-0">
        <p class="text-[11px] text-gray-500 dark:text-gray-400">{{ g.group === 'macro' ? 'پوشش ماکرو' : 'پوشش میکرو' }}</p>
        <p v-if="g.count" class="text-lg font-bold tabular-nums" :class="LEVEL_CLASS[g.level].text">
          {{ faNum(g.coverage, 1) }}<span class="text-xs font-normal text-gray-400">٪</span>
        </p>
        <p v-else class="text-lg font-bold text-gray-400">—</p>
        <p class="text-[10px] truncate" :class="g.count ? LEVEL_CLASS[g.level].text : 'text-gray-400'">
          {{ g.count ? LEVEL_LABEL[g.level] : 'هدفی ثبت نشده' }}
        </p>
      </div>
    </article>

    <!-- بقیه شاخص‌ها -->
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
          <template v-if="item.key === 'ec'">
            <input
              type="text" inputmode="decimal" dir="ltr"
              v-model="ecDraft"
              @keyup.enter="commitEc"
              @blur="commitEc"
              class="w-20 text-lg sm:text-xl font-bold tabular-nums bg-transparent border-b border-dashed border-gray-300 dark:border-gray-600 focus:border-primary-500 outline-none text-gray-900 dark:text-white"
            />
          </template>
          <span v-else class="text-lg sm:text-xl font-bold tabular-nums" :class="item.color">{{ item.value }}</span>
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
import { computed, ref, watch } from 'vue';
import type { OptimizationResponse } from '@/types';

import { computeGroupErrors, faNum, LEVEL_CLASS, LEVEL_LABEL } from '@/utils/errorLevels';

const props = defineProps<{
  result: OptimizationResponse;
  usedCount: number;
  targetValues?: Record<string, number>;
}>();

const format = (value: unknown, digits = 2): string => {
  const parsed = Number(value);
  return isFinite(parsed) ? parsed.toFixed(digits) : '—';
};

const emit = defineEmits<{ (e: 'set-ec', value: number): void }>();

// EC قابل ویرایش: با Enter یا خروج از فیلد، فقط اگر مقدار واقعاً عوض شده باشد اعمال می‌شود
const ecDraft = ref<string>(format(props.result.ec, 2));
watch(() => props.result.ec, (v) => { ecDraft.value = format(v, 2); });
const commitEc = () => {
  const v = parseFloat(String(ecDraft.value).replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d))).replace(/٫/g, '.').replace(',', '.'));
  if (!isFinite(v)) { ecDraft.value = format(props.result.ec, 2); return; }
  if (Math.abs(v - Number(props.result.ec)) < 0.015) return;
  emit('set-ec', v);
};

const RING_CIRC = 2 * Math.PI * 21;
const OUTER_CIRC = 2 * Math.PI * 26;

// خطای ماکرو و میکرو جدا (میانگین خطای مطلق هر گروه؛ رنگ بر پایهٔ بدترین عنصر گروه)
// پوشش = ۱۰۰٪ منهای میانگین خطا (بدون مشکل → ۱۰۰٪)؛ over = میانگین بیش‌تأمین
const errorCards = computed(() => {
  const g = computeGroupErrors(props.targetValues || {}, props.result.concentrations || {});
  return [g.macro, g.micro].map((x) => ({
    ...x,
    coverage: Math.max(0, 100 - x.meanAbs),
    over: x.count ? x.rows.reduce((a, r) => a + Math.max(r.deviationPct, 0), 0) / x.count : 0
  }));
});

const statusColor = (status?: string): string => {
  if (!status) return 'text-gray-500 dark:text-gray-400';
  if (status.includes('مطلوب')) return 'text-emerald-600 dark:text-emerald-400';
  if (status.includes('بسیار') || status.includes('بحرانی')) return 'text-rose-600 dark:text-rose-400';
  return 'text-amber-600 dark:text-amber-400';
};

const ICONS = {
  pulse: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-7 4 14 2-7h6"/></svg>`,
  wallet: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7.5A1.5 1.5 0 014.5 6h13A1.5 1.5 0 0119 7.5V9H4.5A1.5 1.5 0 013 7.5z"/><path d="M3 9h16.5A1.5 1.5 0 0121 10.5v7a1.5 1.5 0 01-1.5 1.5H4.5A1.5 1.5 0 013 17.5V9z"/><circle cx="16.5" cy="14" r="1.1" fill="currentColor" stroke="none"/></svg>`,
  layers: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4.5-8 4.5-8-4.5L12 3z"/><path d="M4 12l8 4.5 8-4.5"/><path d="M4 16.5l8 4.5 8-4.5"/></svg>`
};

const items = computed(() => {
  const result = props.result;

  return [
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
