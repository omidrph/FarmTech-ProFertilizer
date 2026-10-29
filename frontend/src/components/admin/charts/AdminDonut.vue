<!-- نمودار دونات با عدد مرکزی و راهنمای درصدی -->
<template>
  <div class="flex items-center gap-4">
    <div class="relative flex-shrink-0" :style="{ width: size + 'px', height: size + 'px' }">
      <svg :width="size" :height="size" viewBox="0 0 120 120" class="-rotate-90">
        <circle cx="60" cy="60" :r="R" fill="none" class="stroke-gray-100 dark:stroke-gray-700" stroke-width="14" />
        <circle v-for="(a, i) in arcs" :key="i" cx="60" cy="60" :r="R" fill="none" :stroke="a.color" stroke-width="14"
          stroke-linecap="butt" :stroke-dasharray="`${a.len} ${C - a.len}`" :stroke-dashoffset="-a.off"
          class="transition-all duration-700 cursor-default" :opacity="active === null || active === i ? 1 : 0.25"
          @mouseenter="active = i" @mouseleave="active = null" />
      </svg>
      <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span class="text-xl font-extrabold tabular-nums text-gray-900 dark:text-white leading-none">{{ centerValue }}</span>
        <span class="mt-1 text-[10px] text-gray-500 dark:text-gray-400">{{ active !== null ? segments[active].label : centerLabel }}</span>
      </div>
    </div>
    <ul class="flex-1 space-y-1.5 min-w-0">
      <li v-for="(s, i) in segments" :key="s.label" class="flex items-center justify-between gap-2 text-xs"
          @mouseenter="active = i" @mouseleave="active = null">
        <span class="flex items-center gap-2 min-w-0"><i class="w-2.5 h-2.5 rounded-full flex-shrink-0" :style="{ background: s.color }"></i><span class="truncate text-gray-600 dark:text-gray-300">{{ s.label }}</span></span>
        <span class="tabular-nums flex-shrink-0"><b class="text-gray-900 dark:text-white">{{ faNum(s.value) }}</b> <span class="text-gray-400">({{ pct(s.value) }}٪)</span></span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { faNum } from './chartUtils';

const props = withDefaults(defineProps<{ segments: { label: string; value: number; color: string }[]; centerLabel?: string; size?: number }>(), { centerLabel: 'کل', size: 128 });
const R = 46;
const C = 2 * Math.PI * R;
const active = ref<number | null>(null);
const total = computed(() => props.segments.reduce((a, s) => a + s.value, 0));
const centerValue = computed(() => faNum(active.value !== null ? props.segments[active.value].value : total.value));
const pct = (v: number) => (total.value ? Math.round((v / total.value) * 100).toLocaleString('fa-IR') : '۰');
const arcs = computed(() => {
  let off = 0;
  const gap = props.segments.filter((s) => s.value > 0).length > 1 ? 2 : 0;
  return props.segments.map((s) => {
    const len = total.value ? Math.max((s.value / total.value) * C - gap, 0) : 0;
    const a = { len, off, color: s.color };
    off += total.value ? (s.value / total.value) * C : 0;
    return a;
  });
});
</script>
