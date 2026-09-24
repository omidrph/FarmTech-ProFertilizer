<!-- frontend/src/components/features/home/HomeElementRings.vue -->
<!--
  «پوشش عناصر هدف» — بازطراحی حرفه‌ای
  ------------------------------------------------------------
  - هر عنصر در یک کارت با حلقه دایره‌ای
  - نوار پیشرفت خطی زیر هر حلقه برای خوانایی بیشتر
  - حلقه نازک بیرونی برای بیش‌تأمین
  - چیدمان شبکه‌ای مرتب با راهنمای رنگ
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

    <div class="p-4 sm:p-5">
      <!-- شبکه کارت‌ها -->
      <div
        v-if="rows.length"
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5 sm:gap-3"
      >
        <article
          v-for="row in visibleRows"
          :key="row.element"
          class="rounded-xl border p-3 transition-colors"
          :class="row.cardClass"
        >
          <div class="flex items-center justify-between gap-2">
            <!-- حلقه دایره‌ای کوچک -->
            <div class="relative w-12 h-12 flex-shrink-0">
              <svg viewBox="0 0 48 48" class="w-full h-full">
                <circle cx="24" cy="24" r="18" fill="none" stroke-width="4" class="stroke-gray-200 dark:stroke-gray-700/70" />
                <circle
                  cx="24" cy="24" r="18" fill="none" stroke-width="4" stroke-linecap="round"
                  stroke="currentColor" :class="[row.ringClass, 'ring-progress']"
                  :stroke-dasharray="RING_CIRC"
                  :stroke-dashoffset="ready ? row.innerOffset : RING_CIRC"
                  transform="rotate(-90 24 24)"
                />
                <!-- حلقه نازک بیرونی: بیش‌تأمین -->
                <circle
                  v-if="row.overshootOffset !== null"
                  cx="24" cy="24" r="22" fill="none" stroke-width="2" stroke-linecap="round"
                  stroke="currentColor" class="text-rose-500 ring-progress"
                  :stroke-dasharray="OUTER_CIRC"
                  :stroke-dashoffset="ready ? row.overshootOffset : OUTER_CIRC"
                  transform="rotate(-90 24 24)"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-[10px] font-bold tabular-nums" :class="row.textClass">
                  {{ row.percentShort }}
                </span>
              </div>
            </div>

            <!-- نام و وضعیت -->
            <div class="min-w-0 flex-1">
              <p class="text-sm font-bold text-gray-900 dark:text-white truncate">{{ row.element }}</p>
              <p class="text-[11px] mt-0.5 flex items-center gap-1" :class="row.textClass">
                <span class="w-1.5 h-1.5 rounded-full inline-block" :class="row.dotClass"></span>
                {{ row.statusLabel }}
              </p>
            </div>
          </div>

          <!-- مقادیر -->
          <div class="mt-2.5 pt-2.5 border-t border-gray-200/60 dark:border-gray-700/60 flex items-baseline justify-between text-[11px]">
            <span class="text-gray-500 dark:text-gray-400">هدف</span>
            <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">
              {{ row.targetDisplay }}
            </span>
          </div>
          <div class="mt-1 flex items-baseline justify-between text-[11px]">
            <span class="text-gray-500 dark:text-gray-400">فعلی</span>
            <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">
              {{ row.actualDisplay }}
            </span>
          </div>
        </article>
      </div>

      <p v-else class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
        عنصر هدفی ثبت نشده است.
      </p>

      <!-- راهنمای رنگ -->
      <div
        v-if="rows.length"
        class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3 flex-wrap"
      >
        <div class="flex items-center gap-3 text-[11px] text-gray-500 dark:text-gray-400">
          <span class="flex items-center gap-1.5">
            <i class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></i>
            دقیق (تا ۳٪)
          </span>
          <span class="flex items-center gap-1.5">
            <i class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></i>
            تا ۱۰٪
          </span>
          <span class="flex items-center gap-1.5">
            <i class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></i>
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

const LIMIT = 8;
const RING_CIRC = 2 * Math.PI * 18;
const OUTER_CIRC = 2 * Math.PI * 22;
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

const levelLabels: Record<Level, string> = {
  ok: 'دقیق',
  warn: 'نزدیک هدف',
  bad: 'دور از هدف'
};

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
      level === 'ok' ? 'text-emerald-600 dark:text-emerald-400'
        : level === 'warn' ? 'text-amber-600 dark:text-amber-400'
          : 'text-rose-600 dark:text-rose-400';
    const dotClass =
      level === 'ok' ? 'bg-emerald-500'
        : level === 'warn' ? 'bg-amber-500'
          : 'bg-rose-500';
    const cardClass =
      level === 'ok' ? 'bg-emerald-50/40 dark:bg-emerald-950/20 border-emerald-100 dark:border-emerald-900/40'
        : level === 'warn' ? 'bg-amber-50/40 dark:bg-amber-950/20 border-amber-100 dark:border-amber-900/40'
          : 'bg-rose-50/40 dark:bg-rose-950/20 border-rose-100 dark:border-rose-900/40';

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
      dotClass,
      cardClass,
      innerOffset,
      overshootOffset,
      statusLabel: levelLabels[level],
      percentShort: `${Math.round(ratio * 100).toLocaleString('fa-IR')}٪`,
      targetDisplay: target.toLocaleString('fa-IR', { maximumFractionDigits: 2 }),
      actualDisplay: actual.toLocaleString('fa-IR', { maximumFractionDigits: 2 })
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