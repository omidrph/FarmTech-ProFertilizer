<!-- frontend/src/components/features/ph/PhSchematic.vue -->
<!--
  شماتیک حرفه‌ای کار در گلخانه: مخزن اصلی (با نردبان و لوله) → سطل نمونه (با درجه‌بندی، حباب و pH‌متر) → اسید/باز.
  رنگ مایع مثل کاغذ تورنسل از روی pH (قرمز اسیدی ← سبز ≈۶ ← آبی قلیایی) و روی نوار رنگ پایین نشانگر pH دارد.
  همهٔ رنگ‌ها با CSS variable (سازگار با حالت تاریک).
-->
<template>
  <figure class="ph-fig rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden bg-gradient-to-b from-sky-50 via-white to-emerald-50/40 dark:from-gray-800 dark:via-gray-800 dark:to-gray-900/60">
    <svg viewBox="0 0 440 270" class="w-full h-auto select-none" role="img" :aria-label="ariaLabel">
      <defs>
        <linearGradient id="phLiqT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="tankColor" stop-opacity=".78"/><stop offset="1" :stop-color="tankColor" stop-opacity=".98"/></linearGradient>
        <linearGradient id="phLiqB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="bucketColor" stop-opacity=".78"/><stop offset="1" :stop-color="bucketColor" stop-opacity="1"/></linearGradient>
        <linearGradient id="phGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".25" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient>
        <linearGradient id="phScale" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="hsl(5 75% 52%)"/><stop offset=".25" stop-color="hsl(40 85% 52%)"/><stop offset=".5" stop-color="hsl(120 60% 48%)"/><stop offset=".75" stop-color="hsl(190 70% 50%)"/><stop offset="1" stop-color="hsl(225 70% 55%)"/>
        </linearGradient>
        <clipPath id="phTankClip"><rect x="296" y="62" width="112" height="136" rx="14"/></clipPath>
        <clipPath id="phBucketClip"><path d="M58 112 H170 L158 198 Q157 206 149 206 H79 Q71 206 70 198 Z"/></clipPath>
        <filter id="phShadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-opacity=".18"/></filter>
      </defs>

      <!-- زمین -->
      <ellipse cx="220" cy="236" rx="190" ry="8" fill="currentColor" class="text-gray-300/50 dark:text-black/40"/>

      <!-- ================= مخزن اصلی ================= -->
      <g filter="url(#phShadow)">
        <rect x="296" y="62" width="112" height="136" rx="14" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#phTankClip)">
          <rect x="296" :y="tankY" width="112" :height="198 - tankY" fill="url(#phLiqT)" class="ph-liq"/>
          <path :d="wave(296, tankY, 112, 5, 2)" :fill="tankColor" opacity=".55" class="ph-wave"/>
          <circle v-for="b in tankBubbles" :key="b.i" :cx="b.x" cy="190" :r="b.r" fill="#fff" opacity=".5" class="ph-bub" :style="{animationDelay: b.d + 's', animationDuration: b.t + 's'}"/>
          <rect x="296" y="62" width="112" height="136" fill="url(#phGlass)"/>
        </g>
        <rect x="296" y="62" width="112" height="136" rx="14" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3"/>
        <!-- حلقه‌های تقویتی -->
        <g class="stroke-gray-300 dark:stroke-gray-600" stroke-width="2"><line x1="296" y1="96" x2="408" y2="96"/><line x1="296" y1="164" x2="408" y2="164"/></g>
        <!-- نردبان -->
        <g class="stroke-gray-400 dark:stroke-gray-500" stroke-width="2.4" stroke-linecap="round"><line x1="420" y1="78" x2="420" y2="198"/><line x1="432" y1="78" x2="432" y2="198"/><line x1="420" y1="96" x2="432" y2="96"/><line x1="420" y1="122" x2="432" y2="122"/><line x1="420" y1="148" x2="432" y2="148"/><line x1="420" y1="174" x2="432" y2="174"/></g>
        <!-- درب و لوله -->
        <rect x="334" y="54" width="36" height="9" rx="4" class="fill-gray-400 dark:fill-gray-500"/>
        <path d="M296 182 H278 V212 H252" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="278" cy="182" r="5" class="fill-gray-400 dark:fill-gray-500"/>
      </g>
      <text x="352" y="40" text-anchor="middle" class="fill-gray-800 dark:fill-gray-100" style="font-size:14px;font-weight:700">مخزن اصلی</text>
      <g>
        <rect x="312" y="206" width="80" height="22" rx="11" class="fill-gray-100 dark:fill-gray-700"/>
        <text x="352" y="221" text-anchor="middle" class="fill-gray-700 dark:fill-gray-200" style="font-size:12px;font-weight:600">{{ tankText }}</text>
      </g>

      <!-- ================= فلش مقیاس ================= -->
      <g v-if="scale">
        <path d="M284 120 C258 120 236 128 196 128" fill="none" class="stroke-primary-500" stroke-width="3" stroke-dasharray="6 6" stroke-linecap="round" :class="'ph-flow'"/>
        <path d="M206 120 L192 128 L206 136" fill="none" class="stroke-primary-500" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="216" y="92" width="62" height="24" rx="12" class="fill-primary-600"/>
        <text x="247" y="109" text-anchor="middle" fill="#fff" style="font-size:12.5px;font-weight:700">×{{ scaleText }}</text>
      </g>

      <!-- ================= سطل نمونه ================= -->
      <g filter="url(#phShadow)">
        <path d="M58 112 H170 L158 198 Q157 206 149 206 H79 Q71 206 70 198 Z" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#phBucketClip)">
          <rect x="54" :y="bucketY" width="120" :height="212 - bucketY" fill="url(#phLiqB)" class="ph-liq"/>
          <path :d="wave(54, bucketY, 120, 4, 3)" :fill="bucketColor" opacity=".55" class="ph-wave"/>
          <circle v-for="b in bucketBubbles" :key="b.i" :cx="b.x" cy="200" :r="b.r" fill="#fff" opacity=".55" class="ph-bub" :style="{animationDelay: b.d + 's', animationDuration: b.t + 's'}"/>
          <!-- درجه‌بندی داخل سطل -->
          <g stroke="#fff" stroke-opacity=".55" stroke-width="1.6" stroke-linecap="round"><line x1="70" y1="136" x2="86" y2="136"/><line x1="70" y1="156" x2="80" y2="156"/><line x1="70" y1="176" x2="86" y2="176"/></g>
          <path d="M58 112 H170 L158 198 Q157 206 149 206 H79 Q71 206 70 198 Z" fill="url(#phGlass)"/>
        </g>
        <path d="M58 112 H170 L158 198 Q157 206 149 206 H79 Q71 206 70 198 Z" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3" stroke-linejoin="round"/>
        <rect x="54" y="108" width="120" height="8" rx="4" class="fill-gray-400 dark:fill-gray-500"/>
        <path d="M66 110 Q114 66 162 110" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3" stroke-linecap="round"/>
      </g>
      <text x="114" y="236" text-anchor="middle" class="fill-gray-600 dark:fill-gray-300" style="font-size:12px;font-weight:600">{{ sampleText }}</text>

      <!-- pH‌متر داخل سطل -->
      <g v-if="ph != null" class="ph-probe">
        <rect x="120" y="58" width="16" height="64" rx="6" class="fill-gray-700 dark:fill-gray-300"/>
        <rect x="123" y="62" width="10" height="16" rx="3" class="fill-emerald-400"/>
        <rect x="126" y="122" width="4" height="40" rx="2" class="fill-gray-500"/>
        <g>
          <rect x="146" y="64" width="64" height="30" rx="15" class="fill-white dark:fill-gray-900 stroke-gray-300 dark:stroke-gray-600" stroke-width="1.6"/>
          <text x="178" y="84.5" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:15px;font-weight:800">pH {{ phText }}</text>
        </g>
      </g>

      <!-- ================= بطری و قطره ================= -->
      <g v-if="showDropper" class="ph-bob">
        <g transform="translate(70 4)">
          <rect x="4" y="20" width="30" height="46" rx="8" :fill="kind === 'base' ? '#0ea5e9' : '#f59e0b'"/>
          <rect x="8" y="24" width="6" height="36" rx="3" fill="#fff" opacity=".35"/>
          <rect x="11" y="8" width="16" height="14" rx="3" class="fill-gray-500 dark:fill-gray-400"/>
          <path d="M19 66 V82" :stroke="kind === 'base' ? '#0ea5e9' : '#f59e0b'" stroke-width="3.5" stroke-linecap="round"/>
          <text x="19" y="48" text-anchor="middle" fill="#fff" style="font-size:12px;font-weight:800">{{ kind === 'base' ? 'باز' : 'اسید' }}</text>
        </g>
        <circle cx="89" cy="94" r="3.6" :fill="kind === 'base' ? '#0ea5e9' : '#f59e0b'" class="ph-drop"/>
        <circle cx="89" cy="94" r="3.6" :fill="kind === 'base' ? '#0ea5e9' : '#f59e0b'" class="ph-drop ph-drop-2"/>
      </g>

      <!-- برچسب دوز -->
      <g v-if="doseLabel">
        <rect x="150" y="196" width="118" height="30" rx="15" class="fill-emerald-600"/>
        <text x="209" y="216" text-anchor="middle" fill="#fff" style="font-size:13px;font-weight:800">{{ doseLabel }}</text>
      </g>
    </svg>

    <!-- نوار رنگ pH + نشانگرها -->
    <div class="px-5 pb-4 pt-1">
      <div class="relative h-3 rounded-full" style="background:linear-gradient(90deg,hsl(5 75% 52%),hsl(40 85% 52%),hsl(120 60% 48%),hsl(190 70% 50%),hsl(225 70% 55%))">
        <span v-if="markerPos(ph) != null" class="ph-mark ph-mark-now" :style="{ insetInlineStart: markerPos(ph) + '%' }"><i>{{ phText }}</i></span>
        <span v-if="markerPos(targetPh) != null" class="ph-mark ph-mark-target" :style="{ insetInlineStart: markerPos(targetPh) + '%' }"><i>هدف {{ fa(targetPh as number, 1) }}</i></span>
      </div>
      <div class="flex justify-between mt-5 text-[10px] text-gray-400 tabular-nums"><span>{{ fa(3) }}</span><span>{{ fa(5) }}</span><span>{{ fa(7) }}</span><span>{{ fa(9) }}</span><span>{{ fa(11) }}</span></div>
    </div>
    <figcaption v-if="caption" class="px-4 pb-3 -mt-1 text-center text-[11px] sm:text-xs text-gray-500 dark:text-gray-400 leading-5">{{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  tankVolume?: number | null; sampleVolume?: number | null; scale?: number | null;
  ph?: number | null; targetPh?: number | null; kind?: 'acid' | 'base' | null;
  showDropper?: boolean; doseLabel?: string; caption?: string;
}>(), { tankVolume: null, sampleVolume: null, scale: null, ph: null, targetPh: null, kind: null, showDropper: false, doseLabel: '', caption: '' });

const fa = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d }).format(n);

/** رنگ مایع از pH (۳ قرمز ← ۶ سبز ← ۹ آبی) */
function phColor(v: number | null | undefined): string {
  if (v == null || !Number.isFinite(v)) return '#7dd3fc';
  const x = Math.max(3, Math.min(10, v));
  const hue = x <= 6 ? 5 + ((x - 3) / 3) * 115 : 120 + ((Math.min(x, 9) - 6) / 3) * 95;
  return `hsl(${hue.toFixed(0)} 72% 52%)`;
}
const bucketColor = computed(() => phColor(props.ph));
const tankColor = computed(() => phColor(props.ph != null ? props.ph : props.targetPh));
const tankY = computed(() => 92);
const bucketY = computed(() => (props.sampleVolume ? 128 : 160));

// موج ساده
const wave = (x: number, y: number, w: number, a: number, n: number) => {
  const seg = w / (n * 2);
  let d = `M${x} ${y}`;
  for (let i = 0; i < n * 2; i++) d += ` q${seg / 2} ${i % 2 ? a : -a} ${seg} 0`;
  return d + ` V${y + 12} H${x} Z`;
};
const mkBubbles = (n: number, x0: number, x1: number) =>
  Array.from({ length: n }, (_, i) => ({ i, x: x0 + ((i * 37) % (x1 - x0)), r: 1.6 + ((i * 7) % 3), d: (i % 5) * 0.7, t: 3.2 + (i % 4) * 0.8 }));
const tankBubbles = computed(() => mkBubbles(6, 310, 396));
const bucketBubbles = computed(() => mkBubbles(5, 84, 150));

const tankText = computed(() => (props.tankVolume ? `${fa(props.tankVolume)} لیتر` : 'حجم مخزن؟'));
const sampleText = computed(() => (props.sampleVolume ? `نمونه ${fa(props.sampleVolume, 2)} لیتر` : 'نمونه'));
const scaleText = computed(() => (props.scale ? fa(props.scale, props.scale < 10 ? 1 : 0) : ''));
const phText = computed(() => (props.ph != null ? fa(props.ph, 2) : ''));
const markerPos = (v: number | null | undefined) => (v == null || !Number.isFinite(v) ? null : Math.max(0, Math.min(100, ((v - 3) / 8) * 100)));
const ariaLabel = computed(() => `شماتیک مخزن اصلی ${tankText.value} و ${sampleText.value}`);
</script>

<style scoped>
.ph-liq { transition: fill .4s; }
.ph-wave { animation: ph-wave 3.2s ease-in-out infinite alternate; transform-box: fill-box; }
@keyframes ph-wave { from { transform: translateX(-6px); } to { transform: translateX(6px); } }
.ph-bub { animation: ph-rise 4s ease-in infinite; }
@keyframes ph-rise { 0% { transform: translateY(0); opacity: 0; } 15% { opacity: .6; } 100% { transform: translateY(-70px); opacity: 0; } }
.ph-flow { stroke-dashoffset: 0; animation: ph-dash 1.2s linear infinite; }
@keyframes ph-dash { to { stroke-dashoffset: -24; } }
.ph-bob { animation: ph-bob 2.4s ease-in-out infinite; }
@keyframes ph-bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(3px); } }
.ph-drop { animation: ph-drip 1.5s ease-in infinite; }
.ph-drop-2 { animation-delay: .75s; }
@keyframes ph-drip { 0% { transform: translateY(-4px); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(32px); opacity: 0; } }
.ph-probe { animation: ph-probe 3s ease-in-out infinite; transform-box: fill-box; }
@keyframes ph-probe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(2px); } }
.ph-mark { position: absolute; top: -4px; width: 4px; height: 20px; border-radius: 2px; transform: translateX(50%); }
.ph-mark i { position: absolute; top: 22px; left: 50%; transform: translateX(-50%); font-style: normal; font-size: 10px; font-weight: 700; white-space: nowrap; padding: 1px 6px; border-radius: 8px; color: #fff; }
.ph-mark-now { background: #111827; } .ph-mark-now i { background: #111827; }
.ph-mark-target { background: #059669; } .ph-mark-target i { background: #059669; }
:global(.dark) .ph-mark-now, :global(.dark) .ph-mark-now i { background: #f9fafb; color: #111827; }
@media (prefers-reduced-motion: reduce) { .ph-wave, .ph-bub, .ph-flow, .ph-bob, .ph-drop, .ph-probe { animation: none; } }
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
