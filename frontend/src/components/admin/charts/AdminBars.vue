<!-- نمودار ناحیه‌ای/خطی نرم با تولتیپ، شبکه و راهنما؛ زمان از راست به چپ (مناسب فارسی) -->
<template>
  <div ref="wrap" class="relative w-full select-none" :style="{ height: height + 'px' }">
    <svg v-if="w > 0" :width="w" :height="height" class="block overflow-visible"
         @mousemove="onMove" @mouseleave="hover = null" @touchstart.passive="onTouch" @touchmove.passive="onTouch">
      <defs>
        <linearGradient v-for="s in series" :key="'g' + s.key" :id="uid + s.key" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" :stop-color="s.color" stop-opacity="0.32" />
          <stop offset="100%" :stop-color="s.color" stop-opacity="0.02" />
        </linearGradient>
      </defs>

      <!-- شبکه + برچسب محور عمودی -->
      <g v-for="t in yTicks" :key="t.v">
        <line :x1="padL" :x2="w - padR" :y1="t.y" :y2="t.y" class="stroke-gray-200 dark:stroke-gray-700" stroke-dasharray="3 4" />
        <text :x="padL - 8" :y="t.y + 3.5" text-anchor="end" class="fill-gray-400" font-size="10">{{ faShort(t.v) }}</text>
      </g>

      <!-- محور افقی -->
      <text v-for="l in xLabels" :key="l.i" :x="l.x" :y="height - 6" text-anchor="middle" class="fill-gray-400" font-size="10">{{ l.text }}</text>

      <!-- ناحیه و خط -->
      <g v-for="s in series" :key="s.key" :style="{ opacity: hidden.has(s.key) ? 0 : 1, transition: 'opacity .25s' }">
        <path v-if="s.area !== false" :d="areaPath(s)" :fill="`url(#${uid}${s.key})`" />
        <path :d="linePath(s)" fill="none" :stroke="s.color" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"
              :stroke-dasharray="s.dashed ? '5 5' : undefined" />
      </g>

      <!-- نشانگر هاور -->
      <g v-if="hover !== null">
        <line :x1="xAt(hover)" :x2="xAt(hover)" :y1="padT" :y2="height - padB" class="stroke-gray-300 dark:stroke-gray-600" stroke-dasharray="3 3" />
        <template v-for="s in series" :key="'d' + s.key">
          <circle v-if="!hidden.has(s.key)" :cx="xAt(hover)" :cy="yAt(s.values[hover] ?? 0)" r="4.5" :fill="s.color" class="stroke-white dark:stroke-gray-800" stroke-width="2" />
        </template>
      </g>
    </svg>

    <!-- تولتیپ -->
    <div v-if="hover !== null && w > 0" class="pointer-events-none absolute z-10 min-w-[8.5rem] rounded-xl bg-gray-900/95 text-white text-xs px-3 py-2 shadow-xl"
         :style="{ left: tipLeft + 'px', top: '4px' }">
      <p class="text-[10px] text-gray-300 mb-1">{{ labels[hover] }}</p>
      <p v-for="s in series.filter((x) => !hidden.has(x.key))" :key="s.key" class="flex items-center justify-between gap-3">
        <span class="flex items-center gap-1.5"><i class="w-2 h-2 rounded-full inline-block" :style="{ background: s.color }"></i>{{ s.name }}</span>
        <b class="tabular-nums">{{ faNum(s.values[hover] ?? 0) }}</b>
      </p>
    </div>

    <!-- راهنما (کلیک = پنهان/نمایان) -->
    <div class="absolute -top-1 left-0 flex gap-1.5">
      <button v-for="s in series" :key="'l' + s.key" type="button" @click="toggle(s.key)"
        class="flex items-center gap-1.5 text-[11px] px-2 py-0.5 rounded-full border transition"
        :class="hidden.has(s.key) ? 'border-gray-200 dark:border-gray-700 text-gray-400' : 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200'">
        <i class="w-2 h-2 rounded-full" :style="{ background: hidden.has(s.key) ? '#cbd5e1' : s.color }"></i>{{ s.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue';
import { faNum, faShort, niceScale, smoothPath, type Pt } from './chartUtils';

export interface AreaSeries { key: string; name: string; color: string; values: number[]; area?: boolean; dashed?: boolean }
const props = withDefaults(defineProps<{ labels: string[]; series: AreaSeries[]; height?: number }>(), { height: 240 });

const uid = 'ac' + Math.random().toString(36).slice(2, 7);
const wrap = ref<HTMLElement | null>(null);
const w = ref(0);
const hover = ref<number | null>(null);
const hidden = reactive(new Set<string>());
const padL = 40, padR = 10, padT = 34, padB = 24;

let ro: ResizeObserver | null = null;
onMounted(() => {
  const measure = () => { w.value = wrap.value?.clientWidth || 0; };
  measure();
  ro = new ResizeObserver(measure);
  if (wrap.value) ro.observe(wrap.value);
});
onUnmounted(() => ro?.disconnect());

const n = computed(() => props.labels.length);
const visibleMax = computed(() => Math.max(1, ...props.series.filter((s) => !hidden.has(s.key)).flatMap((s) => s.values)));
const scale = computed(() => niceScale(visibleMax.value, 4));
const innerW = computed(() => Math.max(w.value - padL - padR, 1));
const innerH = computed(() => props.height - padT - padB);
// زمان از راست به چپ: نقطهٔ اول سمت راست است
const xAt = (i: number) => w.value - padR - (n.value <= 1 ? innerW.value / 2 : (i / (n.value - 1)) * innerW.value);
const yAt = (v: number) => padT + innerH.value - (v / scale.value.max) * innerH.value;

const yTicks = computed(() => Array.from({ length: 5 }, (_, i) => { const v = (scale.value.max / 4) * i; return { v, y: yAt(v) }; }));
const xLabels = computed(() => {
  const every = Math.max(1, Math.ceil(n.value / Math.max(Math.floor(innerW.value / 56), 1)));
  return props.labels.map((text, i) => ({ i, text, x: xAt(i) })).filter((l) => l.i % every === 0);
});
const pts = (s: AreaSeries): Pt[] => s.values.map((v, i) => ({ x: xAt(i), y: yAt(v) }));
const linePath = (s: AreaSeries) => smoothPath(pts(s), padT, padT + innerH.value);
const areaPath = (s: AreaSeries) => {
  const p = pts(s);
  if (!p.length) return '';
  return `${linePath(s)} L${p[p.length - 1].x.toFixed(1)},${padT + innerH.value} L${p[0].x.toFixed(1)},${padT + innerH.value} Z`;
};

function indexFromX(clientX: number) {
  const rect = wrap.value!.getBoundingClientRect();
  const x = clientX - rect.left;
  const frac = (w.value - padR - x) / innerW.value;
  return Math.min(Math.max(Math.round(frac * (n.value - 1)), 0), n.value - 1);
}
const onMove = (e: MouseEvent) => { if (n.value) hover.value = indexFromX(e.clientX); };
const onTouch = (e: TouchEvent) => { if (n.value && e.touches[0]) hover.value = indexFromX(e.touches[0].clientX); };
const tipLeft = computed(() => (hover.value === null ? 0 : Math.min(Math.max(xAt(hover.value) - 68, 0), Math.max(w.value - 140, 0))));
const toggle = (k: string) => { hidden.has(k) ? hidden.delete(k) : hidden.add(k); if (hidden.size >= props.series.length) hidden.clear(); };
</script>
