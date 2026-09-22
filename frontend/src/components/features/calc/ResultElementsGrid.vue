<!-- frontend/src/components/features/calc/ResultElementsGrid.vue -->
<!--
  بازطراحی «عناصر تأمین‌شده در برابر هدف» با نمودار دایره‌ای (رادیال).
  ------------------------------------------------------------
  منطق حلقه:
    • حلقه داخلی (ضخیم) = رسیدن به هدف، حداکثر تا ۱۰۰٪ پر می‌شود.
    • اگر غلظت واقعی از هدف بیشتر شود، حلقه داخلی کامل (سبز) می‌ماند و
      یک حلقه نازک بیرونی، فقط به‌اندازه مقدار «اضافه»، با رنگ هشدار
      دور آن کشیده می‌شود (شبیه دور دوم حلقه‌های فعالیت). این‌طوری
      حلقه هیچ‌وقت «می‌شکند» و شکل همیشه یک‌دست می‌ماند.
    • رنگ بر اساس فاصله از هدف: سبز (تا ۳٪)، کهربایی (تا ۱۰٪)، قرمز
      (بیشتر).
-->
<template>
  <div class="space-y-3">

    <!-- راهنمای رنگ -->
    <div class="flex items-center gap-3 flex-wrap text-[11px] text-gray-400">
      <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></i>دقیق</span>
      <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-amber-500 inline-block"></i>تا ۱۰٪ فاصله</span>
      <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-rose-500 inline-block"></i>بیشتر</span>
      <span class="flex items-center gap-1 mr-auto"><i class="w-2.5 h-0.5 rounded-full bg-rose-400 inline-block"></i>حلقه نازک = بیش‌تأمین</span>
    </div>

    <!-- شبکه حلقه‌ها -->
    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-2.5">
      <div
        v-for="row in rows"
        :key="row.element"
        class="flex flex-col items-center gap-1 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 py-2.5 px-1.5"
      >
        <svg width="66" height="66" viewBox="0 0 66 66">
          <!-- ریل خالی -->
          <circle cx="33" cy="33" r="24" fill="none" class="stroke-gray-100 dark:stroke-gray-700" stroke-width="6" />
          <!-- حلقه اصلی: تا ۱۰۰٪ هدف -->
          <circle
            cx="33" cy="33" r="24" fill="none" stroke-width="6" stroke-linecap="round"
            :class="row.ringClass"
            stroke="currentColor"
            :stroke-dasharray="RING_CIRC"
            :stroke-dashoffset="row.innerOffset"
            transform="rotate(-90 33 33)"
          />
          <!-- حلقه بیرونی نازک: فقط برای بیش‌تأمین -->
          <circle
            v-if="row.overshootOffset !== null"
            cx="33" cy="33" r="30" fill="none" stroke-width="3" stroke-linecap="round"
            class="stroke-rose-500"
            stroke="currentColor"
            :stroke-dasharray="OUTER_CIRC"
            :stroke-dashoffset="row.overshootOffset"
            transform="rotate(-90 33 33)"
          />
          <text x="33" y="31" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:9px;font-weight:700">{{ row.element }}</text>
          <text x="33" y="42" text-anchor="middle" :class="row.textClass" style="font-size:10px;font-weight:600">{{ row.percentLabel }}</text>
        </svg>
        <p class="text-[10px] text-gray-400 tabular-nums leading-tight text-center">
          {{ row.actualDisplay }} <span class="text-gray-300 dark:text-gray-600">/</span> {{ row.targetDisplay }}
        </p>
      </div>
    </div>

    <p v-if="rows.length === 0" class="text-sm text-gray-500 dark:text-gray-400 text-center py-6">
      عنصر هدفی ثبت نشده است.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  targetValues: Record<string, number>;
  concentrations: Record<string, number>;
}>();

// محیط دایره برای شعاع 24 (حلقه اصلی) و 30 (حلقه بیرونی اضافه)
const RING_CIRC = 2 * Math.PI * 24; // ≈ 150.8
const OUTER_CIRC = 2 * Math.PI * 30; // ≈ 188.5
// یک دور کامل حلقه بیرونی معادل «۵۰٪ اضافه بر هدف» در نظر گرفته می‌شود
// تا بیش‌تأمین‌های خیلی زیاد هم در یک دور قابل نمایش بمانند.
const OVERSHOOT_FULL_AT = 0.5;

const rows = computed(() => {
  const entries = Object.entries(props.targetValues || {}).filter(([, target]) => Number(target) > 0);

  return entries.map(([element, targetRaw]) => {
    const target = Number(targetRaw);
    const actual = Number(props.concentrations?.[element] || 0);
    const ratio = actual / target; // 1 = دقیقاً روی هدف
    const deviationPct = (ratio - 1) * 100;
    const absDeviation = Math.abs(deviationPct);

    const level = absDeviation <= 3 ? 'ok' : absDeviation <= 10 ? 'warn' : 'bad';
    const ringClass = level === 'ok' ? 'stroke-emerald-500' : level === 'warn' ? 'stroke-amber-500' : 'stroke-rose-500';
    const textClass =
      level === 'ok' ? 'fill-emerald-600' : level === 'warn' ? 'fill-amber-600' : 'fill-rose-600';

    const innerRatio = Math.min(ratio, 1);
    const innerOffset = RING_CIRC * (1 - innerRatio);

    let overshootOffset: number | null = null;
    if (ratio > 1) {
      const overshootFraction = Math.min((ratio - 1) / OVERSHOOT_FULL_AT, 1);
      overshootOffset = OUTER_CIRC * (1 - overshootFraction);
    }

    return {
      element,
      ringClass,
      textClass,
      innerOffset,
      overshootOffset,
      percentLabel: `${Math.round(ratio * 100)}٪`,
      targetDisplay: target.toFixed(0),
      actualDisplay: actual.toFixed(0)
    };
  });
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
circle {
  transition: stroke-dashoffset 0.6s ease;
}
</style>
