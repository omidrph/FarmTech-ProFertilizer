<!-- frontend/src/components/features/calc/ResultElementsGrid.vue -->
<!--
  بازطراحی نمایش «عناصر تأمین‌شده در برابر هدف»
  ------------------------------------------------------------
  نسخه قبلی: هر عنصر یک کارت جدا و سه‌خطی بود → با ۸-۱۰ عنصر، این
  بخش به‌تنهایی صدها پیکسل فضا می‌گرفت.
  نسخه فعلی: هر عنصر فقط یک ردیف فشرده (~۳۶px)، در دو ستون روی
  دسکتاپ، همچنان با نوار بولت-چارت (خط ثابت = هدف) و رنگ وضعیت،
  بدون افت خوانایی.
-->
<template>
  <div class="space-y-2">

    <!-- سوییچ واحد + راهنمای رنگ (یک خط جمع‌وجور) -->
    <div class="flex items-center justify-between gap-2 flex-wrap">
      <div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden text-[11px]">
        <button
          v-for="mode in modes"
          :key="mode.key"
          type="button"
          @click="activeMode = mode.key"
          class="px-2.5 py-1 font-medium transition-colors"
          :class="activeMode === mode.key
            ? 'bg-primary-600 text-white'
            : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'"
        >{{ mode.label }}</button>
      </div>

      <div class="flex items-center gap-2 flex-wrap text-[10px] text-gray-400">
        <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></i>دقیق</span>
        <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-amber-500 inline-block"></i>تا ۱۰٪</span>
        <span class="flex items-center gap-1"><i class="w-2 h-2 rounded-full bg-rose-500 inline-block"></i>بیشتر</span>
      </div>
    </div>

    <!-- ردیف‌های فشرده، دو ستونه در دسکتاپ -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-1.5">
      <div
        v-for="row in rows"
        :key="row.element"
        class="flex items-center gap-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-2.5 py-1.5"
      >
        <span class="text-xs font-bold text-gray-700 dark:text-gray-200 w-12 flex-shrink-0 truncate" :title="row.element">
          {{ row.element }}
        </span>

        <div class="relative h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden flex-1 min-w-0">
          <div
            class="absolute top-0 right-0 h-full rounded-full transition-all duration-500"
            :class="row.barClass"
            :style="{ width: row.barWidth }"
          ></div>
          <div
            class="absolute top-[-1px] h-[calc(100%+2px)] w-[2px] rounded-full bg-gray-600 dark:bg-gray-300"
            :style="{ right: row.targetMarkerPosition }"
            :title="'هدف: ' + row.targetDisplay"
          ></div>
        </div>

        <span class="text-[10px] text-gray-400 tabular-nums flex-shrink-0 hidden sm:inline">
          {{ row.actualDisplay }}
        </span>
        <span class="text-[11px] font-semibold tabular-nums px-1.5 py-0.5 rounded flex-shrink-0 w-14 text-center" :class="row.chipClass">
          {{ row.deviationLabel }}
        </span>
      </div>
    </div>

    <p v-if="rows.length === 0" class="text-sm text-gray-500 dark:text-gray-400 text-center py-6">
      عنصر هدفی ثبت نشده است.
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps<{
  targetValues: Record<string, number>;
  concentrations: Record<string, number>;
}>();

// ===== واحد نمایش =====
type Mode = 'relative' | 'ppm';
const modes: Array<{ key: Mode; label: string }> = [
  { key: 'relative', label: 'نسبت به هدف (٪)' },
  { key: 'ppm', label: 'غلظت مطلق (ppm)' }
];
const activeMode = ref<Mode>('relative');

const rows = computed(() => {
  const entries = Object.entries(props.targetValues || {}).filter(([, target]) => Number(target) > 0);

  const ppmCeiling = entries.reduce((max, [element, targetRaw]) => {
    const target = Number(targetRaw);
    const actual = Number(props.concentrations?.[element] || 0);
    return Math.max(max, target, actual);
  }, 0) || 1;

  return entries.map(([element, targetRaw]) => {
    const target = Number(targetRaw);
    const actual = Number(props.concentrations?.[element] || 0);
    const ratio = (actual / target) * 100;
    const deviation = ratio - 100;
    const absDeviation = Math.abs(deviation);

    const level = absDeviation <= 3 ? 'ok' : absDeviation <= 10 ? 'warn' : 'bad';
    const barClass = level === 'ok' ? 'bg-emerald-500' : level === 'warn' ? 'bg-amber-500' : 'bg-rose-500';
    const chipClass =
      level === 'ok'
        ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
        : level === 'warn'
          ? 'bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
          : 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-400';

    const sign = deviation > 0 ? '+' : '';
    const deviationLabel = absDeviation < 0.5 ? 'دقیق' : `${sign}${deviation.toFixed(0)}٪`;

    let barWidth: string;
    let targetMarkerPosition: string;
    let targetDisplay: string;
    let actualDisplay: string;

    if (activeMode.value === 'relative') {
      const SCALE = 150;
      barWidth = `${Math.min(Math.max(ratio, 0), SCALE) / SCALE * 100}%`;
      targetMarkerPosition = `${100 - (100 / SCALE) * 100}%`;
      targetDisplay = '۱۰۰٪';
      actualDisplay = `${ratio.toFixed(0)}٪`;
    } else {
      const ceiling = ppmCeiling * 1.15;
      barWidth = `${Math.min(Math.max(actual, 0), ceiling) / ceiling * 100}%`;
      targetMarkerPosition = `${100 - Math.min(target, ceiling) / ceiling * 100}%`;
      targetDisplay = `${target.toFixed(1)} ppm`;
      actualDisplay = `${actual.toFixed(1)} ppm`;
    }

    return {
      element,
      targetDisplay,
      actualDisplay,
      deviationLabel,
      barWidth,
      targetMarkerPosition,
      barClass,
      chipClass
    };
  });
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
