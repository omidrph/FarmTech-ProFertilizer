<!-- frontend/src/components/features/home/HomeElementRings.vue -->
<!--
  «پوشش عناصر هدف» با حلقه‌های کوچک
  ------------------------------------------------------------
  - هر حلقه: درصد دستیابی به هدف
  - حلقه نازک بیرونی: بیش‌تأمین
  - رنگ: سبز (تا ۳٪)، کهربایی (تا ۱۰٪)، رز (بیشتر)
  - عناصر مشکل‌دار اول نمایش داده می‌شوند
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- هدر -->
    <header class="px-4 sm:px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="8" stroke-width="2" />
            <circle cx="12" cy="12" r="4" stroke-width="2" />
            <circle cx="12" cy="12" r="0.6" fill="currentColor" stroke="none" />
          </svg>
        </span>
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">پوشش عناصر هدف</h3>
      </div>
      <span class="text-[11px] text-gray-500 dark:text-gray-400 tabular-nums">
        {{ visibleRows.length.toLocaleString('fa-IR') }} از {{ rows.length.toLocaleString('fa-IR') }}
      </span>
    </header>

    <!-- حلقه‌ها -->
    <div class="p-4 sm:p-5">
      <div v-if="rows.length" class="grid grid-cols-3 sm:grid-cols-4 gap-3 sm:gap-4">
        <div
          v-for="row in visibleRows"
          :key="row.element"
          class="flex flex-col items-center gap-1"
        >
          <svg width="76" height="76" viewBox="0 0 76 76" role="img" :aria-label="`${row.element}: ${row.percentLabel}`">
            <!-- حلقه پایه -->
            <circle cx="38" cy="38" r="26" fill="none" stroke-width="7" class="stroke-gray-100 dark:stroke-gray-700/60" />
            <!-- حلقه اصلی: تا ۱۰۰٪ -->
            <circle
              cx="38" cy="38" r="26" fill="none" stroke-width="7" stroke-linecap="round"
              stroke="currentColor" :class="[row.ringClass, 'ring-progress']"
              :stroke-dasharray="RING_CIRC"
              :stroke-dashoffset="ready ? row.innerOffset : RING_CIRC"
              transform="rotate(-90 38 38)"
            />
            <!-- حلقه نازک بیرونی: بیش‌تأمین -->
            <circle
              v-if="row.overshootOffset !== null"
              cx="38" cy="38" r="33" fill="none" stroke-width="3" stroke-linecap="round"
              stroke="currentColor" class="text-rose-500 ring-progress"
              :stroke-dasharray="OUTER_CIRC"
              :stroke-dashoffset="ready ? row.overshootOffset : OUTER_CIRC"
              transform="rotate(-90 38 38)"
            />
            <text x="38" y="36" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:11px;font-weight:700">{{ row.element }}</text>
            <text x="38" y="49" text-anchor="middle" :class="row.textClass" style="font-size:11px;font-weight:600">{{ row.percentLabel }}</text>
          </svg>
        </div>
      </div>

      <p v-else class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
        عنصر هدفی ثبت نشده است.
      </p>

      <!-- پانوشت -->
      <div v-if="rows.length" class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3 flex-wrap">
        <div class="flex items-center gap-3 text-[11px] text-gray-400 dark:text-gray-500">
          <span class="flex items-center gap-1">
            <i class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></i>
            دقیق
          </span>
          <span class="flex items-center gap-1">
            <i class="w-2 h-2 rounded-full bg-amber-500 inline-block"></i>
            تا ۱۰٪
          </span>
          <span class="flex items-center gap-1">
            <i class="w-2 h-2 rounded-full bg-rose-500 inline-block"></i>
            بیشتر
          </span>
        </div>
        <button
          v-if="rows.length > LIMIT"
          type="button"
          @click="showAll = !showAll"
          class="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline"
        >
          {{ showAll ? 'نمایش کمتر' : `نمایش همه ${rows.length.toLocaleString('fa-IR')} عنصر` }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';

const props = defineProps<{
  targetValues: Record<string, number>;
  concentrations: Record<string, number>;
}>();

const LIMIT = 6;
const RING_CIRC = 2 * Math.PI * 26;
const OUTER_CIRC = 2 * Math.PI * 33;
const OVERSHOOT_FULL_AT = 0.5;

const showAll = ref(false);

const ready = ref(false);
onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true;
  });
});

type Level = 'ok' | 'warn' | 'bad';
const levelOrder: Record<Level, number> = { bad: 0, warn: 1, ok: 2 };

const rows = computed(() => {
  const entries = Object.entries(props.targetValues || {}).filter(([, target]) => Number(target) > 0);

  const list = entries.map(([element, targetRaw]) => {
    const target = Number(targetRaw);
    const actual = Number(props.concentrations?.[element] || 0);
    const ratio = target > 0 ? actual / target : 0;
    const absDeviation = Math.abs((ratio - 1) * 100);

    const level: Level = absDeviation <= 3 ? 'ok' : absDeviation <= 10 ? 'warn' : 'bad';
    const ringClass =
      level === 'ok' ? 'text-emerald-500 dark:text-emerald-400'
        : level === 'warn' ? 'text-amber-500 dark:text-amber-400'
          : 'text-rose-500 dark:text-rose-400';
    const textClass =
      level === 'ok' ? 'fill-emerald-600 dark:fill-emerald-400'
        : level === 'warn' ? 'fill-amber-600 dark:fill-amber-400'
          : 'fill-rose-600 dark:fill-rose-400';

    const innerOffset = RING_CIRC * (1 - Math.min(ratio, 1));

    let overshootOffset: number | null = null;
    if (ratio > 1) {
      overshootOffset = OUTER_CIRC * (1 - Math.min((ratio - 1) / OVERSHOOT_FULL_AT, 1));
    }

    return {
      element,
      level,
      absDeviation,
      ringClass,
      textClass,
      innerOffset,
      overshootOffset,
      percentLabel: `${Math.round(ratio * 100).toLocaleString('fa-IR')}٪`
    };
  });

  return list.sort((a, b) => {
    if (a.level !== b.level) return levelOrder[a.level] - levelOrder[b.level];
    return a.level === 'ok' ? 0 : b.absDeviation - a.absDeviation;
  });
});

const visibleRows = computed(() => (showAll.value ? rows.value : rows.value.slice(0, LIMIT)));
</script>

<style scoped>
.ring-progress {
  transition: stroke-dashoffset 0.9s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (prefers-reduced-motion: reduce) {
  .ring-progress {
    transition: none;
  }
}
</style>