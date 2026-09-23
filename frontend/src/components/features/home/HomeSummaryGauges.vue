<!-- frontend/src/components/features/home/HomeSummaryGauges.vue -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3 mb-4">
      <div>
        <h2 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">خلاصه نتیجه</h2>
        <p class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400 mt-1">مهم‌ترین شاخص‌های همین محاسبه</p>
      </div>
      <span class="text-[11px] px-2.5 py-1 rounded-full font-medium" :class="accuracy >= 95 ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400' : accuracy >= 85 ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400' : 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400'">
        {{ accuracy >= 95 ? 'نتیجه مطلوب' : accuracy >= 85 ? 'نیازمند بررسی' : 'نیازمند اصلاح' }}
      </span>
    </div>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-3">
      <article class="rounded-xl bg-gray-50 dark:bg-gray-700/30 p-3 sm:p-4 flex flex-col items-center text-center">
        <div class="relative w-[82px] h-[82px] sm:w-[92px] sm:h-[92px]">
          <svg class="w-full h-full -rotate-90" viewBox="0 0 92 92">
            <circle cx="46" cy="46" r="36" fill="none" class="stroke-gray-200 dark:stroke-gray-600" stroke-width="7" />
            <circle cx="46" cy="46" r="36" fill="none" stroke-width="7" stroke-linecap="round" :class="accuracyRing" :stroke-dasharray="RING_CIRC" :stroke-dashoffset="accuracyOffset" class="transition-all duration-700" />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-base sm:text-lg font-bold tabular-nums" :class="accuracyText">{{ accuracy.toFixed(1) }}٪</span>
          </div>
        </div>
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-100 mt-2">دقت رسیدن به هدف</p>
        <p class="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">میانگین تحقق اهداف</p>
      </article>

      <article class="rounded-xl bg-gray-50 dark:bg-gray-700/30 p-3 sm:p-4 flex flex-col items-center text-center">
        <div class="relative w-[82px] h-[82px] sm:w-[92px] sm:h-[92px]">
          <svg class="w-full h-full -rotate-90" viewBox="0 0 92 92">
            <circle cx="46" cy="46" r="36" fill="none" class="stroke-gray-200 dark:stroke-gray-600" stroke-width="7" />
            <circle cx="46" cy="46" r="36" fill="none" stroke-width="7" stroke-linecap="round" class="text-blue-500 transition-all duration-700" stroke="currentColor" :stroke-dasharray="RING_CIRC" :stroke-dashoffset="ecOffset" />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span class="text-base sm:text-lg font-bold text-blue-600 dark:text-blue-400 tabular-nums">{{ ec.toFixed(2) }}</span>
            <span class="text-[9px] text-gray-400">dS/m</span>
          </div>
        </div>
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-100 mt-2">EC نهایی</p>
        <p class="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">مقیاس نمایشی تا ۳.۵</p>
      </article>

      <article class="rounded-xl bg-gray-50 dark:bg-gray-700/30 p-3 sm:p-4 flex flex-col items-center text-center">
        <div class="relative w-[82px] h-[82px] sm:w-[92px] sm:h-[92px]">
          <svg class="w-full h-full -rotate-90" viewBox="0 0 92 92">
            <circle cx="46" cy="46" r="36" fill="none" class="stroke-gray-200 dark:stroke-gray-600" stroke-width="7" />
            <circle cx="46" cy="46" r="36" fill="none" stroke-width="7" stroke-linecap="round" :class="balanceRing" :stroke-dasharray="RING_CIRC" :stroke-dashoffset="balanceOffset" class="transition-all duration-700" />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-sm font-bold" :class="balanceText">{{ isBalanced ? 'مطلوب' : 'بررسی' }}</span>
          </div>
        </div>
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-100 mt-2">تعادل یونی</p>
        <p class="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">وضعیت کاتیون و آنیون</p>
      </article>

      <article class="rounded-xl bg-gray-50 dark:bg-gray-700/30 p-3 sm:p-4 flex flex-col items-center justify-center text-center">
        <div class="text-2xl sm:text-3xl font-bold text-emerald-600 dark:text-emerald-400 tabular-nums">{{ costDisplay }}</div>
        <div class="text-[10px] text-gray-400 mt-1">تومان</div>
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-100 mt-3">هزینه کل</p>
        <p class="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">مجموع کودهای پیشنهادی</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  targetAchievement: Record<string, number>;
  ec: number;
  totalCost: number;
  ionBalanced?: boolean;
}>();

const RING_CIRC = 2 * Math.PI * 36;

const accuracy = computed(() => {
  const values = Object.values(props.targetAchievement || {});
  if (!values.length) return 0;
  return Math.max(0, Math.min(100, values.reduce((sum, value) => sum + (Number(value) || 0), 0) / values.length));
});

const accuracyOffset = computed(() => RING_CIRC * (1 - accuracy.value / 100));
const accuracyRing = computed(() => accuracy.value >= 95 ? 'text-emerald-500' : accuracy.value >= 85 ? 'text-amber-500' : 'text-rose-500');
const accuracyText = computed(() => accuracy.value >= 95 ? 'text-emerald-600 dark:text-emerald-400' : accuracy.value >= 85 ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400');

const ec = computed(() => Math.max(0, Number(props.ec) || 0));
const ecOffset = computed(() => RING_CIRC * (1 - Math.min(ec.value / 3.5, 1)));

const isBalanced = computed(() => props.ionBalanced !== false);
const balanceOffset = computed(() => RING_CIRC * (isBalanced.value ? 0 : 0.58));
const balanceRing = computed(() => isBalanced.value ? 'text-emerald-500' : 'text-amber-500');
const balanceText = computed(() => isBalanced.value ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400');

const costDisplay = computed(() => Math.round(props.totalCost || 0).toLocaleString('fa-IR'));
</script>

<style scoped>
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
