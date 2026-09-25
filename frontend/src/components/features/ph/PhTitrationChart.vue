<!-- frontend/src/components/features/ph/PhTitrationChart.vue -->
<!-- منحنی تیتراسیون: حجم تجمعی تیترانت (محور افقی) در برابر pH (محور عمودی) -->
<template>
  <div class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-3">
    <div class="flex items-center justify-between gap-2 mb-2">
      <span class="text-xs font-medium text-gray-700 dark:text-gray-300">منحنی تیتراسیون</span>
      <span class="text-[11px] text-gray-400 dark:text-gray-500">محور افقی: mL تیترانت · محور عمودی: pH</span>
    </div>

    <div dir="ltr" class="w-full">
      <svg :viewBox="`0 0 ${W} ${H}`" class="w-full h-auto" role="img" aria-label="منحنی تیتراسیون pH بر حسب حجم تیترانت">
        <!-- شبکه و برچسب محور عمودی -->
        <g v-for="t in yTicks" :key="`y${t}`">
          <line :x1="PAD_L" :x2="W - PAD_R" :y1="y(t)" :y2="y(t)" class="stroke-gray-100 dark:stroke-gray-700" stroke-width="1" />
          <text :x="PAD_L - 6" :y="y(t) + 3" text-anchor="end" class="fill-gray-400 dark:fill-gray-500" style="font-size:10px">{{ t.toFixed(1) }}</text>
        </g>
        <!-- برچسب محور افقی -->
        <g v-for="t in xTicks" :key="`x${t}`">
          <text :x="x(t)" :y="H - PAD_B + 14" text-anchor="middle" class="fill-gray-400 dark:fill-gray-500" style="font-size:10px">{{ formatTick(t) }}</text>
        </g>
        <line :x1="PAD_L" :x2="W - PAD_R" :y1="H - PAD_B" :y2="H - PAD_B" class="stroke-gray-300 dark:stroke-gray-600" stroke-width="1" />
        <line :x1="PAD_L" :x2="PAD_L" :y1="PAD_T" :y2="H - PAD_B" class="stroke-gray-300 dark:stroke-gray-600" stroke-width="1" />

        <!-- خط pH هدف -->
        <template v-if="targetPH !== null">
          <line :x1="PAD_L" :x2="W - PAD_R" :y1="y(targetPH)" :y2="y(targetPH)" stroke="currentColor" class="text-amber-500" stroke-width="1.5" stroke-dasharray="5 4" />
          <text :x="W - PAD_R" :y="y(targetPH) - 4" text-anchor="end" class="fill-amber-600 dark:fill-amber-400" style="font-size:10px;font-weight:600">هدف {{ targetPH.toFixed(2) }}</text>
        </template>

        <!-- نقطه‌ی دوز -->
        <template v-if="doseMl !== null && targetPH !== null">
          <line :x1="x(doseMl)" :x2="x(doseMl)" :y1="y(targetPH)" :y2="H - PAD_B" stroke="currentColor" class="text-emerald-500" stroke-width="1.5" stroke-dasharray="3 3" />
          <circle :cx="x(doseMl)" :cy="y(targetPH)" r="5" class="fill-emerald-500 stroke-white dark:stroke-gray-800" stroke-width="2" />
          <text :x="x(doseMl)" :y="H - PAD_B - 6" text-anchor="middle" class="fill-emerald-600 dark:fill-emerald-400" style="font-size:10px;font-weight:600">{{ doseMl.toFixed(2) }} mL</text>
        </template>

        <!-- منحنی و نقاط -->
        <polyline :points="polyline" fill="none" stroke="currentColor" class="text-primary-500" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
        <circle v-for="(p, i) in sorted" :key="i" :cx="x(p.volumeMl)" :cy="y(p.pH)" r="3.5" class="fill-white dark:fill-gray-800 stroke-primary-500" stroke-width="2" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Point {
  volumeMl: number;
  pH: number;
}

const props = defineProps<{
  points: Point[];
  targetPH: number | null;
  doseMl: number | null;
}>();

const W = 360;
const H = 190;
const PAD_L = 34;
const PAD_R = 12;
const PAD_T = 14;
const PAD_B = 26;

const sorted = computed(() => [...props.points].sort((a, b) => a.volumeMl - b.volumeMl));

const xMax = computed(() => {
  const maxV = Math.max(...sorted.value.map(p => p.volumeMl), props.doseMl ?? 0, 0.1);
  return maxV * 1.05;
});

const yRange = computed(() => {
  const values = sorted.value.map(p => p.pH);
  if (props.targetPH !== null) values.push(props.targetPH);
  const lo = Math.floor((Math.min(...values) - 0.2) * 2) / 2;
  const hi = Math.ceil((Math.max(...values) + 0.2) * 2) / 2;
  return { lo, hi: hi === lo ? lo + 1 : hi };
});

const x = (v: number) => PAD_L + (v / xMax.value) * (W - PAD_L - PAD_R);
const y = (ph: number) =>
  PAD_T + (1 - (ph - yRange.value.lo) / (yRange.value.hi - yRange.value.lo)) * (H - PAD_T - PAD_B);

const polyline = computed(() => sorted.value.map(p => `${x(p.volumeMl)},${y(p.pH)}`).join(' '));

const yTicks = computed(() => {
  const { lo, hi } = yRange.value;
  const step = hi - lo > 3 ? 1 : 0.5;
  const ticks: number[] = [];
  for (let t = lo; t <= hi + 1e-9; t += step) ticks.push(Number(t.toFixed(2)));
  return ticks;
});

const xTicks = computed(() => {
  const n = 4;
  return Array.from({ length: n + 1 }, (_, i) => (xMax.value / n) * i);
});

const formatTick = (t: number) => (t >= 10 ? t.toFixed(0) : t.toFixed(1));
</script>



