<!-- frontend/src/components/features/home/HomeElementRings.vue -->
<!--
  «پوشش عناصر هدف» با حلقه‌های کوچک (همان منطق صفحه‌ی نتیجه):
    • حلقه‌ی اصلی = رسیدن به هدف (حداکثر ۱۰۰٪)
    • حلقه‌ی نازک بیرونی = بیش‌تأمین
    • رنگ: سبز (تا ۳٪ فاصله)، کهربایی (تا ۱۰٪)، قرمز (بیشتر)
  عناصر مشکل‌دار اول نمایش داده می‌شوند؛ حداکثر ۶ عنصر، و دکمه‌ی «نمایش همه».
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3 mb-4">
      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">پوشش عناصر هدف</h3>
      <span class="text-xs text-gray-500 dark:text-gray-400 tabular-nums">
        {{ visibleRows.length.toLocaleString('fa-IR') }} از {{ rows.length.toLocaleString('fa-IR') }} عنصر
      </span>
    </div>

    <div v-if="rows.length" class="grid grid-cols-3 sm:grid-cols-4 gap-3">
      <div
        v-for="row in visibleRows"
        :key="row.element"
        class="flex flex-col items-center gap-1"
      >
        <svg width="72" height="72" viewBox="0 0 72 72" role="img" :aria-label="`${row.element}: ${row.percentLabel}`">
          <circle cx="36" cy="36" r="26" fill="none" stroke-width="7" class="stroke-gray-100 dark:stroke-gray-700" />
          <circle
            cx="36" cy="36" r="26" fill="none" stroke-width="7" stroke-linecap="round"
            stroke="currentColor" :class="[row.ringClass, 'ring-progress']"
            :stroke-dasharray="RING_CIRC"
            :stroke-dashoffset="ready ? row.innerOffset : RING_CIRC"
            transform="rotate(-90 36 36)"
          />
          <circle
            v-if="row.overshootOffset !== null"
            cx="36" cy="36" r="33" fill="none" stroke-width="3" stroke-linecap="round"
            stroke="currentColor" class="text-rose-500 ring-progress"
            :stroke-dasharray="OUTER_CIRC"
            :stroke-dashoffset="ready ? row.overshootOffset : OUTER_CIRC"
            transform="rotate(-90 36 36)"
          />
          <text x="36" y="34" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:11px;font-weight:700">{{ row.element }}</text>
          <text x="36" y="47" text-anchor="middle" :class="row.textClass" style="font-size:11px;font-weight:600">{{ row.percentLabel }}</text>
        </svg>
      </div>
    </div>

    <p v-else class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">عنصر هدفی ثبت نشده است.</p>

    <div v-if="rows.length" class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3">
      <span class="text-[11px] text-gray-400 dark:text-gray-500">حلقه‌ی نازک قرمز = بیش‌تأمین</span>
      <button
        v-if="rows.length > LIMIT"
        type="button"
        @click="showAll = !showAll"
        class="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline"
      >
        {{ showAll ? 'نمایش کمتر' : `نمایش همه ${rows.length.toLocaleString('fa-IR')} عنصر` }}
      </button>
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
// یک دور کامل حلقه‌ی بیرونی = ۵۰٪ اضافه بر هدف
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
    const ratio = actual / target;
    const absDeviation = Math.abs((ratio - 1) * 100);

    const level: Level = absDeviation <= 3 ? 'ok' : absDeviation <= 10 ? 'warn' : 'bad';
    const ringClass =
      level === 'ok' ? 'text-emerald-500' : level === 'warn' ? 'text-amber-500' : 'text-rose-500';
    const textClass =
      level === 'ok'
        ? 'fill-emerald-600 dark:fill-emerald-400'
        : level === 'warn'
          ? 'fill-amber-600 dark:fill-amber-400'
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

  // مشکل‌دارها اول (بدترین بالاتر)؛ عناصر سالم به ترتیب اصلی می‌مانند
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
