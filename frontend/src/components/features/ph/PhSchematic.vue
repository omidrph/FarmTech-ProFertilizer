<!-- frontend/src/components/features/ph/PhSchematic.vue -->
<!--
  شماتیک حرفه‌ای کار در گلخانه: مخزن اصلی (با نردبان و لوله) → سطل نمونه (با درجه‌بندی، حباب و pH‌متر) → اسید/باز.
  رنگ مایع مثل کاغذ تورنسل از روی pH (قرمز اسیدی ← سبز ≈۶ ← آبی قلیایی) و روی نوار رنگ پایین نشانگر pH دارد.
  همهٔ رنگ‌ها با CSS variable (سازگار با حالت تاریک).
-->
<template>
  <figure class="ph-fig rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden bg-gradient-to-b from-sky-50 via-white to-emerald-50/40 dark:from-gray-800 dark:via-gray-800 dark:to-gray-900/60">
    <svg viewBox="0 0 460 300" class="w-full h-auto select-none" role="img" :aria-label="ariaLabel">
      <defs>
        <linearGradient id="phSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0f2fe"/><stop offset="1" stop-color="#f0fdf4"/></linearGradient>
        <linearGradient id="phSkyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#14231b"/></linearGradient>
        <linearGradient id="phLiqT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="tankColor" stop-opacity=".78"/><stop offset="1" :stop-color="tankColor" stop-opacity=".98"/></linearGradient>
        <linearGradient id="phLiqB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="bucketColor" stop-opacity=".78"/><stop offset="1" :stop-color="bucketColor" stop-opacity="1"/></linearGradient>
        <linearGradient id="phGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".6"/><stop offset=".22" stop-color="#fff" stop-opacity=".06"/><stop offset=".85" stop-color="#fff" stop-opacity=".02"/><stop offset="1" stop-color="#fff" stop-opacity=".3"/></linearGradient>
        <linearGradient id="phMetal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9ca3af"/><stop offset=".5" stop-color="#e5e7eb"/><stop offset="1" stop-color="#9ca3af"/></linearGradient>
        <clipPath id="phTankClip"><rect x="300" y="72" width="116" height="140" rx="16"/></clipPath>
        <clipPath id="phBucketClip"><path d="M60 142 H176 L164 228 Q163 236 155 236 H81 Q73 236 72 228 Z"/></clipPath>
        <filter id="phShadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="3.5" flood-opacity=".2"/></filter>
      </defs>

      <!-- ===== پس‌زمینه: گلخانه ===== -->
      <rect x="0" y="0" width="460" height="300" fill="url(#phSky)" class="ph-sky-l"/>
      <rect x="0" y="0" width="460" height="300" fill="url(#phSkyD)" class="ph-sky-d"/>
      <g class="stroke-sky-200 dark:stroke-gray-700" fill="none" stroke-width="2" opacity=".9">
        <path d="M-10 120 Q230 -50 470 120"/><path d="M-10 160 Q230 -10 470 160" opacity=".6"/>
        <line x1="230" y1="12" x2="230" y2="260"/><line x1="130" y1="30" x2="110" y2="260"/><line x1="330" y1="30" x2="350" y2="260"/><line x1="40" y1="78" x2="20" y2="260"/><line x1="420" y1="78" x2="440" y2="260"/>
      </g>
      <!-- گیاهان پس‌زمینه -->
      <g opacity=".85">
        <g v-for="x in [18, 52, 380, 430]" :key="x" :transform="`translate(${x} 246)`">
          <path d="M0 0 C-12 -16 -10 -34 0 -46 C10 -34 12 -16 0 0Z" fill="#4ade80"/><path d="M0 0 C-22 -6 -28 -22 -22 -34 C-8 -28 -2 -14 0 0Z" fill="#22c55e"/><path d="M0 0 C22 -6 28 -22 22 -34 C8 -28 2 -14 0 0Z" fill="#16a34a"/>
        </g>
      </g>
      <rect x="0" y="252" width="460" height="48" class="fill-emerald-100/70 dark:fill-gray-900/70"/>
      <rect x="0" y="252" width="460" height="3" class="fill-emerald-200 dark:fill-gray-700"/>

      <!-- ===== مخزن اصلی ===== -->
      <g filter="url(#phShadow)">
        <!-- پایه‌ها -->
        <g class="fill-gray-400 dark:fill-gray-500"><rect x="312" y="210" width="10" height="42" rx="2"/><rect x="394" y="210" width="10" height="42" rx="2"/><rect x="306" y="248" width="22" height="5" rx="2"/><rect x="388" y="248" width="22" height="5" rx="2"/></g>
        <rect x="300" y="72" width="116" height="140" rx="16" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#phTankClip)">
          <rect x="300" :y="tankY" width="116" :height="212 - tankY" fill="url(#phLiqT)" class="ph-liq"/>
          <path :d="wave(296, tankY, 124, 5, 3)" :fill="tankColor" opacity=".55" class="ph-wave"/>
          <circle v-for="b in tankBubbles" :key="b.i" :cx="b.x" cy="204" :r="b.r" fill="#fff" opacity=".5" class="ph-bub" :style="{animationDelay: b.d + 's', animationDuration: b.t + 's'}"/>
          <rect x="300" y="72" width="116" height="140" fill="url(#phGlass)"/>
        </g>
        <rect x="300" y="72" width="116" height="140" rx="16" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3.2"/>
        <g class="stroke-gray-300 dark:stroke-gray-600" stroke-width="2"><line x1="300" y1="108" x2="416" y2="108"/><line x1="300" y1="176" x2="416" y2="176"/></g>
        <!-- درب -->
        <rect x="338" y="62" width="40" height="11" rx="5" fill="url(#phMetal)"/><rect x="352" y="56" width="12" height="7" rx="2" class="fill-gray-500"/>
        <!-- شیر خروجی و لوله -->
        <path d="M300 196 H282 V232 H244" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="282" cy="196" r="7" class="fill-primary-500"/><rect x="278" y="188" width="8" height="5" rx="2" class="fill-gray-600"/>
        <!-- نشانگر سطح (روی بدنه) -->
        <g class="fill-gray-500 dark:fill-gray-300" style="font-size:8.5px"><text x="296" y="112" text-anchor="end">¾</text><text x="296" y="143" text-anchor="end">½</text><text x="296" y="180" text-anchor="end">¼</text></g>
        <!-- نردبان -->
        <g class="stroke-gray-400 dark:stroke-gray-500" stroke-width="2.4" stroke-linecap="round"><line x1="430" y1="88" x2="430" y2="212"/><line x1="442" y1="88" x2="442" y2="212"/><line x1="430" y1="108" x2="442" y2="108"/><line x1="430" y1="134" x2="442" y2="134"/><line x1="430" y1="160" x2="442" y2="160"/><line x1="430" y1="186" x2="442" y2="186"/></g>
      </g>
      <text x="358" y="38" text-anchor="middle" class="fill-gray-800 dark:fill-gray-100" style="font-size:14.5px;font-weight:800">مخزن اصلی</text>
      <g><rect x="318" y="262" width="80" height="22" rx="11" class="fill-gray-800 dark:fill-gray-100"/><text x="358" y="277" text-anchor="middle" class="fill-white dark:fill-gray-900" style="font-size:12px;font-weight:700">{{ tankText }}</text></g>

      <!-- ===== فلش مقیاس‌دهی ===== -->
      <g v-if="scale">
        <path d="M292 140 C268 140 246 150 200 150" fill="none" class="stroke-primary-500 ph-flow" stroke-width="3.2" stroke-dasharray="7 6" stroke-linecap="round"/>
        <path d="M212 142 L196 150 L212 158" fill="none" class="stroke-primary-500" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="222" y="112" width="66" height="26" rx="13" class="fill-primary-600"/>
        <text x="255" y="130" text-anchor="middle" fill="#fff" style="font-size:13px;font-weight:800">×{{ scaleText }}</text>
      </g>

      <!-- ===== میز + سطل نمونه ===== -->
      <g class="fill-amber-700/80 dark:fill-amber-900"><rect x="40" y="236" width="160" height="9" rx="3"/><rect x="52" y="245" width="9" height="9"/><rect x="179" y="245" width="9" height="9"/></g>
      <g filter="url(#phShadow)">
        <path d="M60 142 H176 L164 228 Q163 236 155 236 H81 Q73 236 72 228 Z" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#phBucketClip)">
          <rect x="56" :y="bucketY" width="124" :height="242 - bucketY" fill="url(#phLiqB)" class="ph-liq"/>
          <path :d="wave(52, bucketY, 132, 4, 3)" :fill="bucketColor" opacity=".55" class="ph-wave"/>
          <circle v-for="b in bucketBubbles" :key="b.i" :cx="b.x" cy="228" :r="b.r" fill="#fff" opacity=".55" class="ph-bub" :style="{animationDelay: b.d + 's', animationDuration: b.t + 's'}"/>
          <g stroke="#fff" stroke-opacity=".6" stroke-width="1.8" stroke-linecap="round"><line x1="76" y1="168" x2="94" y2="168"/><line x1="76" y1="188" x2="86" y2="188"/><line x1="76" y1="208" x2="94" y2="208"/></g>
          <path d="M60 142 H176 L164 228 Q163 236 155 236 H81 Q73 236 72 228 Z" fill="url(#phGlass)"/>
        </g>
        <path d="M60 142 H176 L164 228 Q163 236 155 236 H81 Q73 236 72 228 Z" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3.2" stroke-linejoin="round"/>
        <rect x="56" y="138" width="124" height="9" rx="4.5" class="fill-gray-400 dark:fill-gray-500"/>
        <path d="M68 140 Q118 92 168 140" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="3.2" stroke-linecap="round"/>
      </g>
      <text x="118" y="272" text-anchor="middle" class="fill-gray-700 dark:fill-gray-200" style="font-size:12px;font-weight:700">{{ sampleText }}</text>

      <!-- ===== pH‌متر ===== -->
      <g v-if="ph != null" class="ph-probe">
        <rect x="126" y="84" width="20" height="74" rx="7" class="fill-gray-700 dark:fill-gray-300"/>
        <rect x="130" y="90" width="12" height="20" rx="3" class="fill-emerald-400"/><rect x="132" y="94" width="8" height="3" rx="1.5" fill="#064e3b"/>
        <rect x="132" y="158" width="4" height="46" rx="2" class="fill-gray-500"/><circle cx="134" cy="206" r="4" class="fill-emerald-500"/>
        <rect x="152" y="86" width="72" height="32" rx="16" class="fill-white dark:fill-gray-900 stroke-gray-300 dark:stroke-gray-600" stroke-width="1.8"/>
        <text x="188" y="108" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:16px;font-weight:800">pH {{ phText }}</text>
      </g>

      <!-- ===== سرنگ اسید/باز ===== -->
      <g v-if="showDropper" class="ph-bob">
        <g transform="translate(84 6)">
          <rect x="6" y="30" width="30" height="62" rx="6" class="fill-white dark:fill-gray-900 stroke-gray-400 dark:stroke-gray-500" stroke-width="2.2"/>
          <rect x="9" y="52" width="24" height="38" rx="4" :fill="kind === 'base' ? '#38bdf8' : '#f59e0b'" opacity=".85"/>
          <g stroke="#6b7280" stroke-width="1.4"><line x1="9" y1="44" x2="17" y2="44"/><line x1="9" y1="56" x2="14" y2="56"/><line x1="9" y1="68" x2="17" y2="68"/><line x1="9" y1="80" x2="14" y2="80"/></g>
          <rect x="19" y="4" width="4" height="30" class="fill-gray-500"/><rect x="10" y="0" width="22" height="6" rx="3" class="fill-gray-600"/>
          <path d="M21 92 V112" :stroke="kind === 'base' ? '#0284c7' : '#d97706'" stroke-width="3" stroke-linecap="round"/>
          <text x="21" y="76" text-anchor="middle" fill="#fff" style="font-size:11px;font-weight:800">{{ kind === 'base' ? 'باز' : 'اسید' }}</text>
        </g>
        <circle cx="105" cy="128" r="3.8" :fill="kind === 'base' ? '#0ea5e9' : '#f59e0b'" class="ph-drop"/>
        <circle cx="105" cy="128" r="3.8" :fill="kind === 'base' ? '#0ea5e9' : '#f59e0b'" class="ph-drop ph-drop-2"/>
      </g>

      <!-- برچسب دوز -->
      <g v-if="doseLabel">
        <rect x="150" y="212" width="124" height="32" rx="16" class="fill-primary-600"/>
        <text x="212" y="233" text-anchor="middle" fill="#fff" style="font-size:13.5px;font-weight:800">{{ doseLabel }}</text>
      </g>
    </svg>

    <!-- نوار رنگ pH + نشانگرها -->
    <div class="px-5 pb-4 pt-1" dir="ltr">
      <div class="relative h-3 rounded-full" style="background:linear-gradient(90deg,hsl(5 75% 52%),hsl(40 85% 52%),hsl(120 60% 48%),hsl(190 70% 50%),hsl(225 70% 55%))">
        <span v-if="markerPos(ph) != null" class="ph-mark ph-mark-now" :style="{ left: markerPos(ph) + '%' }"><i>{{ phText }}</i></span>
        <span v-if="markerPos(targetPh) != null" class="ph-mark ph-mark-target" :style="{ left: markerPos(targetPh) + '%' }"><i>هدف {{ fa(targetPh as number, 1) }}</i></span>
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
const tankY = computed(() => 104);
const bucketY = computed(() => (props.sampleVolume ? 166 : 190));

// موج ساده
const wave = (x: number, y: number, w: number, a: number, n: number) => {
  const seg = w / (n * 2);
  let d = `M${x} ${y}`;
  for (let i = 0; i < n * 2; i++) d += ` q${seg / 2} ${i % 2 ? a : -a} ${seg} 0`;
  return d + ` V${y + 12} H${x} Z`;
};
const mkBubbles = (n: number, x0: number, x1: number) =>
  Array.from({ length: n }, (_, i) => ({ i, x: x0 + ((i * 37) % (x1 - x0)), r: 1.6 + ((i * 7) % 3), d: (i % 5) * 0.7, t: 3.2 + (i % 4) * 0.8 }));
const tankBubbles = computed(() => mkBubbles(7, 312, 404));
const bucketBubbles = computed(() => mkBubbles(5, 86, 156));

const tankText = computed(() => (props.tankVolume ? `${fa(props.tankVolume)} لیتر` : 'حجم مخزن؟'));
const sampleText = computed(() => (props.sampleVolume ? `نمونه ${fa(props.sampleVolume, 2)} لیتر` : 'نمونه'));
const scaleText = computed(() => (props.scale ? fa(props.scale, props.scale < 10 ? 1 : 0) : ''));
const phText = computed(() => (props.ph != null ? fa(props.ph, 2) : ''));
const markerPos = (v: number | null | undefined) => (v == null || !Number.isFinite(v) ? null : Math.max(0, Math.min(100, ((v - 3) / 8) * 100)));
const ariaLabel = computed(() => `شماتیک مخزن اصلی ${tankText.value} و ${sampleText.value}`);
</script>

<style scoped>
.ph-liq { transition: fill .4s; }
.ph-sky-d { opacity: 0; }
:global(.dark) .ph-sky-d { opacity: 1; }
:global(.dark) .ph-sky-l { opacity: 0; }
.ph-wave { animation: ph-wave 3.2s ease-in-out infinite alternate; transform-box: fill-box; }
@keyframes ph-wave { from { transform: translateX(-6px); } to { transform: translateX(6px); } }
.ph-bub { animation: ph-rise 4s ease-in infinite; }
@keyframes ph-rise { 0% { transform: translateY(0); opacity: 0; } 15% { opacity: .6; } 100% { transform: translateY(-80px); opacity: 0; } }
.ph-flow { stroke-dashoffset: 0; animation: ph-dash 1.2s linear infinite; }
@keyframes ph-dash { to { stroke-dashoffset: -24; } }
.ph-bob { animation: ph-bob 2.4s ease-in-out infinite; }
@keyframes ph-bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(3px); } }
.ph-drop { animation: ph-drip 1.5s ease-in infinite; }
.ph-drop-2 { animation-delay: .75s; }
@keyframes ph-drip { 0% { transform: translateY(-4px); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(32px); opacity: 0; } }
.ph-probe { animation: ph-probe 3s ease-in-out infinite; transform-box: fill-box; }
@keyframes ph-probe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(2px); } }
.ph-mark { position: absolute; top: -4px; width: 4px; height: 20px; border-radius: 2px; transform: translateX(-50%); }
.ph-mark i { position: absolute; top: 22px; left: 50%; transform: translateX(-50%); font-style: normal; font-size: 10px; font-weight: 700; white-space: nowrap; padding: 1px 6px; border-radius: 8px; color: #fff; }
.ph-mark-now { background: #111827; } .ph-mark-now i { background: #111827; }
.ph-mark-target { background: #059669; } .ph-mark-target i { background: #059669; }
:global(.dark) .ph-mark-now, :global(.dark) .ph-mark-now i { background: #f9fafb; color: #111827; }
@media (prefers-reduced-motion: reduce) { .ph-wave, .ph-bub, .ph-flow, .ph-bob, .ph-drop, .ph-probe { animation: none; } }
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
