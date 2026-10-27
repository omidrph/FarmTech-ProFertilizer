<!-- frontend/src/components/features/home/HomeElementRings.vue -->
<!--
  «پوشش عناصر هدف» — با جداسازی ماکرو و میکرو و منطق سه‌رنگ خطا
  ------------------------------------------------------------
  - هر گروه (ماکرو / میکرو) هدر جدا با «میانگین خطا» و «بدترین عنصر» دارد
  - رنگ هر عنصر: تا ۵٪ سبز (قابل قبول) | ۵ تا ۱۰٪ زرد (هشدار) | بالای ۱۰٪ قرمز (عدم اعتماد)
  - رنگ سربرگ هر گروه بر پایهٔ بدترین عنصر همان گروه است (یک عنصر خراب پنهان نمی‌ماند)
  - عناصر مشکل‌دار هر گروه اول نمایش داده می‌شوند
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
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
        {{ total.toLocaleString('fa-IR') }} عنصر
      </span>
    </header>

    <div class="p-4 sm:p-5 space-y-5">
      <template v-for="g in sections" :key="g.group">
        <div v-if="g.shown.length">
          <!-- هدر گروه -->
          <div
            class="mb-3 flex items-center justify-between gap-2 flex-wrap rounded-xl border px-3 py-2"
            :class="[LEVEL_CLASS[g.level].bg, LEVEL_CLASS[g.level].border]"
          >
            <div class="flex items-center gap-2">
              <i class="w-2.5 h-2.5 rounded-full inline-block" :class="LEVEL_CLASS[g.level].dot"></i>
              <h4 class="text-sm font-bold text-gray-900 dark:text-white">{{ GROUP_TITLES[g.group] }}</h4>
              <span class="text-[11px] text-gray-500 dark:text-gray-400">{{ g.count.toLocaleString('fa-IR') }} عنصر</span>
            </div>
            <div class="flex items-center gap-3 text-[11px] tabular-nums">
              <span class="text-gray-600 dark:text-gray-300">
                میانگین خطا
                <b :class="LEVEL_CLASS[errorLevel(g.meanAbs)].text">{{ faNum(g.meanAbs, 1) }}٪</b>
              </span>
              <span class="font-semibold" :class="LEVEL_CLASS[g.level].text">{{ LEVEL_LABEL[g.level] }}</span>
            </div>
          </div>

          <!-- شبکه کارت‌ها -->
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5 sm:gap-3">
            <article
              v-for="row in g.shown"
              :key="row.element"
              class="rounded-xl border p-3 transition-colors"
              :class="[LEVEL_CLASS[row.level].bg, LEVEL_CLASS[row.level].border]"
            >
              <div class="flex items-center justify-between gap-2">
                <div class="relative w-12 h-12 flex-shrink-0">
                  <svg viewBox="0 0 48 48" class="w-full h-full">
                    <circle cx="24" cy="24" r="18" fill="none" stroke-width="4" class="stroke-gray-200 dark:stroke-gray-700/70" />
                    <circle
                      cx="24" cy="24" r="18" fill="none" stroke-width="4" stroke-linecap="round"
                      stroke="currentColor" :class="[ringText(row.level), 'ring-progress']"
                      :stroke-dasharray="RING_CIRC"
                      :stroke-dashoffset="ready ? innerOffset(row) : RING_CIRC"
                      transform="rotate(-90 24 24)"
                    />
                    <circle
                      v-if="row.actual > row.target"
                      cx="24" cy="24" r="22" fill="none" stroke-width="2" stroke-linecap="round"
                      stroke="currentColor" class="text-rose-500 ring-progress"
                      :stroke-dasharray="OUTER_CIRC"
                      :stroke-dashoffset="ready ? outerOffset(row) : OUTER_CIRC"
                      transform="rotate(-90 24 24)"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-[10px] font-bold tabular-nums" :class="LEVEL_CLASS[row.level].text">
                      {{ Math.round((row.actual / row.target) * 100).toLocaleString('fa-IR') }}٪
                    </span>
                  </div>
                </div>

                <div class="min-w-0 flex-1">
                  <p class="text-sm font-bold text-gray-900 dark:text-white truncate">{{ row.element }}</p>
                  <p class="text-[11px] mt-0.5 flex items-center gap-1" :class="LEVEL_CLASS[row.level].text">
                    <span class="w-1.5 h-1.5 rounded-full inline-block" :class="LEVEL_CLASS[row.level].dot"></span>
                    {{ faNum(row.absPct, 1) }}٪ {{ row.deviationPct >= 0 ? 'بیش' : 'کم' }}
                  </p>
                </div>
              </div>

              <div class="mt-2.5 pt-2.5 border-t border-gray-200/60 dark:border-gray-700/60 flex items-baseline justify-between text-[11px]">
                <span class="text-gray-500 dark:text-gray-400">هدف</span>
                <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">{{ fmt(row.target) }}</span>
              </div>
              <div class="mt-1 flex items-baseline justify-between text-[11px]">
                <span class="text-gray-500 dark:text-gray-400">فعلی</span>
                <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">{{ fmt(row.actual) }}</span>
              </div>
            </article>
          </div>
        </div>
      </template>

      <!-- بقیهٔ عناصر: آکاردئون -->
      <div v-if="hiddenCount > 0">
        <button
          type="button"
          @click="expanded = !expanded"
          :aria-expanded="expanded"
          class="w-full flex items-center justify-between gap-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/30 hover:bg-gray-100 dark:hover:bg-gray-700/60 px-3.5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 transition-colors"
        >
          <span>{{ expanded ? 'نمایش کمتر' : `نمایش ${hiddenCount.toLocaleString('fa-IR')} عنصر دیگر` }}</span>
          <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="expanded ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="acc-body" :class="expanded ? 'acc-open' : ''">
          <div class="overflow-hidden">
            <div class="pt-3 space-y-4">
              <template v-for="g in sections" :key="'h-' + g.group">
                <div v-if="g.hidden.length">
                  <p class="mb-2 text-[11px] font-semibold text-gray-500 dark:text-gray-400">{{ GROUP_TITLES[g.group] }}</p>
                  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5 sm:gap-3">
                    <article
                      v-for="row in g.hidden"
                      :key="row.element"
                      class="rounded-xl border p-3"
                      :class="[LEVEL_CLASS[row.level].bg, LEVEL_CLASS[row.level].border]"
                    >
                      <div class="flex items-center justify-between gap-2">
                        <div class="relative w-12 h-12 flex-shrink-0">
                          <svg viewBox="0 0 48 48" class="w-full h-full">
                            <circle cx="24" cy="24" r="18" fill="none" stroke-width="4" class="stroke-gray-200 dark:stroke-gray-700/70" />
                            <circle cx="24" cy="24" r="18" fill="none" stroke-width="4" stroke-linecap="round" stroke="currentColor" :class="ringText(row.level)" :stroke-dasharray="RING_CIRC" :stroke-dashoffset="innerOffset(row)" transform="rotate(-90 24 24)" />
                            <circle v-if="row.actual > row.target" cx="24" cy="24" r="22" fill="none" stroke-width="2" stroke-linecap="round" stroke="currentColor" class="text-rose-500" :stroke-dasharray="OUTER_CIRC" :stroke-dashoffset="outerOffset(row)" transform="rotate(-90 24 24)" />
                          </svg>
                          <div class="absolute inset-0 flex items-center justify-center">
                            <span class="text-[10px] font-bold tabular-nums" :class="LEVEL_CLASS[row.level].text">{{ Math.round((row.actual / row.target) * 100).toLocaleString('fa-IR') }}٪</span>
                          </div>
                        </div>
                        <div class="min-w-0 flex-1">
                          <p class="text-sm font-bold text-gray-900 dark:text-white truncate">{{ row.element }}</p>
                          <p class="text-[11px] mt-0.5 flex items-center gap-1" :class="LEVEL_CLASS[row.level].text">
                            <span class="w-1.5 h-1.5 rounded-full inline-block" :class="LEVEL_CLASS[row.level].dot"></span>
                            {{ faNum(row.absPct, 1) }}٪ {{ row.deviationPct >= 0 ? 'بیش' : 'کم' }}
                          </p>
                        </div>
                      </div>
                      <div class="mt-2.5 pt-2.5 border-t border-gray-200/60 dark:border-gray-700/60 flex items-baseline justify-between text-[11px]">
                        <span class="text-gray-500 dark:text-gray-400">هدف</span>
                        <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">{{ fmt(row.target) }}</span>
                      </div>
                      <div class="mt-1 flex items-baseline justify-between text-[11px]">
                        <span class="text-gray-500 dark:text-gray-400">فعلی</span>
                        <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">{{ fmt(row.actual) }}</span>
                      </div>
                    </article>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <p v-if="!total" class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">عنصر هدفی ثبت نشده است.</p>

      <!-- راهنمای رنگ -->
      <div v-if="total" class="pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center gap-4 flex-wrap text-[11px] text-gray-500 dark:text-gray-400">
        <span class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></i>تا ۵٪ — قابل قبول</span>
        <span class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></i>۵ تا ۱۰٪ — هشدار</span>
        <span class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></i>بالای ۱۰٪ — عدم اعتماد</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import {
  computeGroupErrors, errorLevel, faNum, GROUP_TITLES, LEVEL_CLASS, LEVEL_LABEL,
  type ElementError, type ErrorLevel
} from '@/utils/errorLevels';

const props = defineProps<{
  targetValues: Record<string, number>;
  concentrations: Record<string, number>;
}>();

const RING_CIRC = 2 * Math.PI * 18;
const OUTER_CIRC = 2 * Math.PI * 22;
const OVERSHOOT_FULL_AT = 0.5;

const ready = ref(false);
onMounted(() => requestAnimationFrame(() => { ready.value = true; }));

const order: Record<ErrorLevel, number> = { bad: 0, warn: 1, ok: 2 };
const ringText = (l: ErrorLevel) =>
  l === 'ok' ? 'text-emerald-500 dark:text-emerald-400' : l === 'warn' ? 'text-amber-500 dark:text-amber-400' : 'text-rose-500 dark:text-rose-400';

const innerOffset = (r: ElementError) => RING_CIRC * (1 - Math.min(r.actual / r.target, 1));
const outerOffset = (r: ElementError) => OUTER_CIRC * (1 - Math.min((r.actual / r.target - 1) / OVERSHOOT_FULL_AT, 1));
const fmt = (v: number) => v.toLocaleString('fa-IR', { maximumFractionDigits: 2 });

const groups = computed(() => computeGroupErrors(props.targetValues, props.concentrations));
// تعداد استاندارد نمایش: ۸ عنصر (اول ماکرو، بعد میکرو؛ مشکل‌دارها اول)؛ بقیه داخل آکاردئون
const LIMIT = 8;
const expanded = ref(false);
const sections = computed(() => {
  let left = LIMIT;
  return [groups.value.macro, groups.value.micro].map((g) => {
    const sorted = [...g.rows].sort((a, b) => (a.level !== b.level ? order[a.level] - order[b.level] : b.absPct - a.absPct));
    const shown = sorted.slice(0, Math.max(left, 0));
    left -= shown.length;
    return { ...g, shown, hidden: sorted.slice(shown.length) };
  });
});
const hiddenCount = computed(() => sections.value.reduce((n, g) => n + g.hidden.length, 0));
const total = computed(() => groups.value.all.length);
</script>

<style scoped>
.acc-body { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.25s ease; }
.acc-body.acc-open { grid-template-rows: 1fr; }
.ring-progress {
  transition: stroke-dashoffset 0.9s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (prefers-reduced-motion: reduce) {
  .acc-body { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.25s ease; }
.acc-body.acc-open { grid-template-rows: 1fr; }
.ring-progress { transition: none; }
}
</style>
