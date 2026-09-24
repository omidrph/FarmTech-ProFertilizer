<!-- frontend/src/components/features/home/HomeReservoirs.vue -->
<!--
  خلاصه مخازن A / B / C
  ------------------------------------------------------------
  - نمایش تعداد کود در هر مخزن
  - رنگ اختصاصی برای هر مخزن
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <header class="px-4 sm:px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
        <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </span>
      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">مخازن</h3>
    </header>

    <div class="p-4 sm:p-5 grid grid-cols-3 gap-2.5">
      <div
        v-for="tank in tanks"
        :key="tank.key"
        class="rounded-xl border px-3 py-3 text-center transition-colors"
        :class="tank.count
          ? tank.activeClass
          : 'bg-gray-50 dark:bg-gray-700/30 border-gray-100 dark:border-gray-700'"
      >
        <p class="text-[11px] font-medium" :class="tank.count ? tank.labelClass : 'text-gray-400 dark:text-gray-500'">
          مخزن {{ tank.key }}
        </p>
        <p class="mt-1 text-base font-bold tabular-nums"
           :class="tank.count ? tank.valueClass : 'text-gray-300 dark:text-gray-600'">
          {{ tank.count ? tank.count.toLocaleString('fa-IR') : '—' }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  counts: { A: number; B: number; C: number };
}>();

const tanks = computed(() => [
  {
    key: 'A',
    count: props.counts.A,
    activeClass: 'bg-blue-50 dark:bg-blue-950/40 border-blue-200 dark:border-blue-700/60',
    labelClass: 'text-blue-700 dark:text-blue-300',
    valueClass: 'text-blue-700 dark:text-blue-300',
  },
  {
    key: 'B',
    count: props.counts.B,
    activeClass: 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-700/60',
    labelClass: 'text-emerald-700 dark:text-emerald-300',
    valueClass: 'text-emerald-700 dark:text-emerald-300',
  },
  {
    key: 'C',
    count: props.counts.C,
    activeClass: 'bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-700/60',
    labelClass: 'text-amber-700 dark:text-amber-300',
    valueClass: 'text-amber-700 dark:text-amber-300',
  },
]);
</script>