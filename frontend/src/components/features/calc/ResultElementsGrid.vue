<!-- frontend/src/components/features/calc/ResultElementsGrid.vue -->
<!--
  ریدیزاین نمایش عناصر.
  مدل قبلی (نوار دوطرفه از وسط) برای کاربر گمراه‌کننده بود.
  مدل جدید: «درصد تأمین نسبت به هدف» با نشانگر ثابت روی ۱۰۰٪.
  یعنی نوار هرچه به خط هدف نزدیک‌تر باشد بهتر است؛ عبور از خط یعنی بیش‌تأمین.
-->
<template>
  <div class="space-y-3">
    <!-- راهنمای رنگ -->
    <div class="flex items-center gap-3 flex-wrap text-[11px] text-gray-500 dark:text-gray-400">
      <span class="flex items-center gap-1"><i class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></i> اختلاف تا ۳٪</span>
      <span class="flex items-center gap-1"><i class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></i> ۳ تا ۱۰٪</span>
      <span class="flex items-center gap-1"><i class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></i> بیش از ۱۰٪</span>
      <span class="flex items-center gap-1 mr-auto">
        <i class="w-0.5 h-3 bg-gray-400 inline-block"></i> خط هدف (۱۰۰٪)
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-2.5">
      <article
        v-for="row in rows"
        :key="row.element"
        class="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-3"
      >
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-bold text-gray-900 dark:text-white">{{ row.element }}</span>
          <span class="text-xs font-semibold tabular-nums" :class="row.textClass">{{ row.deviationLabel }}</span>
        </div>

        <!-- نوار درصد تأمین -->
        <div class="relative h-2.5 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
          <div
            class="absolute top-0 right-0 h-full rounded-full transition-all duration-500"
            :class="row.barClass"
            :style="{ width: row.barWidth }"
          ></div>
          <!-- نشانگر هدف -->
          <div class="absolute top-0 h-full w-0.5 bg-gray-400 dark:bg-gray-400/80" style="right: 83.33%"></div>
        </div>

        <div class="flex items-center justify-between mt-1.5 text-[11px]">
          <span class="text-gray-500 dark:text-gray-400">
            هدف: <strong class="tabular-nums text-gray-700 dark:text-gray-200">{{ row.target }}</strong>
          </span>
          <span class="text-gray-500 dark:text-gray-400">
            تأمین: <strong class="tabular-nums" :class="row.textClass">{{ row.actual }}</strong>
          </span>
        </div>
      </article>
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

// نوار تا ۱۲۰٪ هدف را نشان می‌دهد؛ خط هدف روی ۱۰۰/۱۲۰ = ۸۳٫۳۳٪ عرض است.
const MAX_SCALE = 120;

const rows = computed(() => {
  const entries = Object.entries(props.targetValues || {}).filter(([, target]) => Number(target) > 0);

  return entries.map(([element, targetRaw]) => {
    const target = Number(targetRaw);
    const actual = Number(props.concentrations?.[element] || 0);
    const ratio = (actual / target) * 100;
    const deviation = ratio - 100;
    const absDeviation = Math.abs(deviation);

    const level = absDeviation <= 3 ? 'ok' : absDeviation <= 10 ? 'warn' : 'bad';

    const barClass =
      level === 'ok' ? 'bg-emerald-500' : level === 'warn' ? 'bg-amber-500' : 'bg-rose-500';

    const textClass =
      level === 'ok'
        ? 'text-emerald-600 dark:text-emerald-400'
        : level === 'warn'
          ? 'text-amber-600 dark:text-amber-400'
          : 'text-rose-600 dark:text-rose-400';

    const sign = deviation > 0 ? '+' : '';

    return {
      element,
      target: target.toFixed(1),
      actual: actual.toFixed(1),
      deviationLabel: absDeviation < 0.05 ? 'دقیق' : `${sign}${deviation.toFixed(1)}٪`,
      barWidth: `${Math.min(Math.max(ratio, 0), MAX_SCALE) / MAX_SCALE * 100}%`,
      barClass,
      textClass
    };
  });
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
