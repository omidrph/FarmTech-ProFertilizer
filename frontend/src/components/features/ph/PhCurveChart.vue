<!-- frontend/src/components/features/ph/PhCurveChart.vue -->
<!--
  منحنی pH نمونه نسبت به مقدار تجمعی اسید/باز (آزمون و خطا).
  خط افقی خط‌چین = pH هدف. نقطه‌ها = قرائت‌های واقعی کاربر.
-->
<template>
  <div v-if="points.length >= 2" class="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/60 dark:bg-gray-900/30 p-3">
    <svg :viewBox="`0 0 ${W} ${H}`" class="w-full h-auto" role="img" aria-label="منحنی pH نمونه">
      <!-- شبکه -->
      <g class="stroke-gray-200 dark:stroke-gray-700" stroke-width="1">
        <line v-for="t in yTicks" :key="'y' + t" :x1="PAD_L" :x2="W - PAD_R" :y1="y(t)" :y2="y(t)" />
      </g>
      <g class="fill-gray-400" style="font-size:9px">
        <text v-for="t in yTicks" :key="'yt' + t" :x="PAD_L - 5" :y="y(t) + 3" text-anchor="end">{{ t.toFixed(1) }}</text>
        <text :x="W - PAD_R" :y="H - 4" text-anchor="end">{{ unitLabel }} (تجمعی)</text>
      </g>

      <!-- خط هدف -->
      <line :x1="PAD_L" :x2="W - PAD_R" :y1="y(targetPh)" :y2="y(targetPh)" class="stroke-emerald-500" stroke-width="1.5" stroke-dasharray="5 4" />
      <text :x="PAD_L + 4" :y="y(targetPh) - 4" class="fill-emerald-600" style="font-size:9px;font-weight:600">هدف {{ targetPh.toFixed(2) }}</text>

      <!-- منحنی -->
      <polyline :points="polyline" fill="none" class="stroke-primary-500" stroke-width="2" stroke-linejoin="round" />
      <g>
        <circle v-for="(p, i) in points" :key="i" :cx="x(p.amount)" :cy="y(p.ph)" r="3.5" class="fill-white stroke-primary-600" stroke-width="2" />
      </g>
      <g class="fill-gray-600 dark:fill-gray-300" style="font-size:9px">
        <text v-for="(p, i) in points" :key="'l' + i" :x="x(p.amount)" :y="y(p.ph) - 8" text-anchor="middle">{{ p.ph.toFixed(2) }}</text>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  points: Array<{ amount: number; ph: number }>;
  targetPh: number;
  unitLabel: string;
}>();

const W = 340;
const H = 170;
const PAD_L = 30;
const PAD_R = 12;
const PAD_T = 16;
const PAD_B = 18;

const maxX = computed(() => Math.max(...props.points.map((p) => p.amount), 0.0001));
const yRange = computed(() => {
  const all = [...props.points.map((p) => p.ph), props.targetPh];
  const lo = Math.floor(Math.min(...all) * 2) / 2 - 0.5;
  const hi = Math.ceil(Math.max(...all) * 2) / 2 + 0.5;
  return { lo, hi };
});
const yTicks = computed(() => {
  const { lo, hi } = yRange.value;
  const out: number[] = [];
  for (let v = lo; v <= hi + 1e-9; v += 0.5) out.push(v);
  return out;
});

const x = (v: number) => PAD_L + (v / maxX.value) * (W - PAD_L - PAD_R);
const y = (v: number) => {
  const { lo, hi } = yRange.value;
  return PAD_T + (1 - (v - lo) / (hi - lo)) * (H - PAD_T - PAD_B);
};
const polyline = computed(() => props.points.map((p) => `${x(p.amount)},${y(p.ph)}`).join(' '));
</script>
