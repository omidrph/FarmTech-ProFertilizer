<!-- خط کوچک روند برای کارت‌های شاخص -->
<template>
  <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`" class="block overflow-visible">
    <defs><linearGradient :id="uid" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" :stop-color="color" stop-opacity="0.35" /><stop offset="100%" :stop-color="color" stop-opacity="0" /></linearGradient></defs>
    <path v-if="area" :d="area" :fill="`url(#${uid})`" />
    <path v-if="line" :d="line" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    <circle v-if="last" :cx="last.x" :cy="last.y" r="2.6" :fill="color" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { smoothPath, type Pt } from './chartUtils';
const props = withDefaults(defineProps<{ values: number[]; color?: string; width?: number; height?: number }>(), { color: '#2563eb', width: 96, height: 34 });
const uid = 'sp' + Math.random().toString(36).slice(2, 7);
// زمان از راست به چپ؛ نقطهٔ آخر (جدیدترین) سمت چپ
const pts = computed<Pt[]>(() => {
  const v = props.values, n = v.length;
  if (n < 2) return [];
  const max = Math.max(...v), min = Math.min(...v), span = max - min || 1;
  return v.map((val, i) => ({ x: props.width - 3 - (i / (n - 1)) * (props.width - 6), y: 4 + (props.height - 8) * (1 - (val - min) / span) }));
});
const line = computed(() => smoothPath(pts.value, 2, props.height - 2));
const area = computed(() => (pts.value.length ? `${line.value} L${pts.value[pts.value.length - 1].x},${props.height} L${pts.value[0].x},${props.height} Z` : ''));
const last = computed(() => pts.value[pts.value.length - 1]);
</script>
