<!-- frontend/src/components/features/ph/PhVisual.vue -->
<!--
  نمای بصری اصلاح pH: گیج نیم‌دایره‌ای (عقربه، هدف و بازهٔ رنگی) + مسیر «نمونه ← مخزن» با ظرف‌های شیشه‌ای.
  رنگ مایع از روی pH. همهٔ رنگ‌ها سازگار با حالت تاریک؛ انیمیشن‌ها با prefers-reduced-motion خاموش می‌شوند.
-->
<template>
  <div class="pv rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden shadow-sm">
    <!-- ===== گیج pH ===== -->
    <div class="pv-top px-4 pt-4 pb-1">
      <svg viewBox="0 0 320 222" class="w-full h-auto" role="img" :aria-label="`pH ${phText || 'نامشخص'}`">
        <defs>
          <linearGradient id="pvArc" x1="40" y1="0" x2="280" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0" stop-color="#ef4444"/><stop offset=".18" stop-color="#f97316"/><stop offset=".36" stop-color="#eab308"/>
            <stop offset=".5" stop-color="#22c55e"/><stop offset=".68" stop-color="#14b8a6"/><stop offset=".85" stop-color="#3b82f6"/><stop offset="1" stop-color="#6366f1"/>
          </linearGradient>
          <filter id="pvGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <!-- ریل -->
        <path :d="arc(120)" fill="none" class="stroke-gray-100 dark:stroke-gray-700" stroke-width="22" stroke-linecap="round"/>
        <path :d="arc(120)" fill="none" stroke="url(#pvArc)" stroke-width="14" stroke-linecap="round" opacity=".95"/>
        <!-- درجه‌ها -->
        <g v-for="t in ticks" :key="t.v">
          <line :x1="t.x1" :y1="t.y1" :x2="t.x2" :y2="t.y2" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="1.6" stroke-linecap="round"/>
          <text :x="t.tx" :y="t.ty" text-anchor="middle" dominant-baseline="middle" class="fill-gray-500 dark:fill-gray-400" style="font-size:10px;font-weight:600">{{ fa(t.v) }}</text>
        </g>
        <!-- هدف -->
        <g v-if="targetPh != null">
          <circle :cx="pt(targetPh, 120).x" :cy="pt(targetPh, 120).y" r="11" class="fill-white dark:fill-gray-800 stroke-emerald-500" stroke-width="3.5"/>
          <circle :cx="pt(targetPh, 120).x" :cy="pt(targetPh, 120).y" r="3.5" class="fill-emerald-500"/>
        </g>
        <!-- عقربه -->
        <g :style="{ transform: `rotate(${rot}deg)`, transformOrigin: '160px 160px' }" class="pv-needle">
          <path d="M160 160 L74 160" stroke-width="3.4" stroke-linecap="round" style="stroke:currentColor" />
          <path d="M64 160 L96 155 L96 165 Z" fill="currentColor"/>
        </g>
        <circle cx="160" cy="160" r="11" fill="currentColor" class="text-gray-900 dark:text-white"/>
        <circle cx="160" cy="160" r="4.5" class="fill-white dark:fill-gray-900"/>
        <!-- عدد -->
        <text x="160" y="198" text-anchor="middle" class="fill-gray-900 dark:fill-white" style="font-size:34px;font-weight:800">{{ phText || '—' }}</text>
        <text x="160" y="216" text-anchor="middle" class="fill-gray-500 dark:fill-gray-400" style="font-size:11px">pH {{ live ? 'فعلی' : 'اولیه' }}</text>
      </svg>
      <div class="flex items-center justify-center gap-2 pb-3 text-[11px]">
        <span v-if="targetPh != null" class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 font-medium tabular-nums">هدف {{ fa(targetPh, 2) }}</span>
        <span v-if="gap != null" class="px-2.5 py-1 rounded-full tabular-nums font-medium" :class="Math.abs(gap) <= 0.1 ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300' : 'bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-300'">
          {{ Math.abs(gap) <= 0.1 ? 'روی هدف' : `فاصله ${fa(Math.abs(gap), 2)}` }}
        </span>
      </div>
    </div>

    <!-- ===== مسیر نمونه ← مخزن ===== -->
    <div class="px-3 pb-4 pt-2 bg-gradient-to-b from-gray-50/70 to-transparent dark:from-gray-900/30">
      <svg viewBox="0 0 320 150" class="w-full h-auto" role="img" aria-label="نمونه و مخزن اصلی">
        <defs>
          <linearGradient id="pvLiqS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="color" stop-opacity=".8"/><stop offset="1" :stop-color="color"/></linearGradient>
          <linearGradient id="pvLiqT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" :stop-color="tankColor" stop-opacity=".8"/><stop offset="1" :stop-color="tankColor"/></linearGradient>
          <linearGradient id="pvGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset=".3" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity=".3"/></linearGradient>
          <clipPath id="pvClipS"><path d="M28 34 H96 L90 104 Q89 112 81 112 H43 Q35 112 34 104 Z"/></clipPath>
          <clipPath id="pvClipT"><path d="M226 30 H298 V108 Q298 116 262 116 Q226 116 226 108 Z"/></clipPath>
        </defs>

        <!-- نمونه (بشر) -->
        <ellipse cx="62" cy="120" rx="40" ry="6" class="fill-gray-200/70 dark:fill-black/30"/>
        <path d="M28 34 H96 L90 104 Q89 112 81 112 H43 Q35 112 34 104 Z" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#pvClipS)">
          <rect x="24" :y="sampleY" width="76" height="90" fill="url(#pvLiqS)" class="pv-liq"/>
          <path :d="wave(24, sampleY, 76, 3.5, 3)" :fill="color" opacity=".5" class="pv-wave"/>
          <circle v-for="b in bubblesS" :key="b.i" :cx="b.x" cy="104" :r="b.r" fill="#fff" opacity=".6" class="pv-bub" :style="{ animationDelay: b.d + 's' }"/>
          <rect x="24" y="30" width="76" height="86" fill="url(#pvGlass)"/>
        </g>
        <path d="M28 34 H96 L90 104 Q89 112 81 112 H43 Q35 112 34 104 Z" fill="none" class="stroke-gray-300 dark:stroke-gray-500" stroke-width="2.4" stroke-linejoin="round"/>
        <g class="stroke-gray-300 dark:stroke-gray-500" stroke-width="1.4" stroke-linecap="round"><line x1="34" y1="58" x2="44" y2="58"/><line x1="35" y1="76" x2="41" y2="76"/><line x1="36" y1="94" x2="44" y2="94"/></g>
        <path d="M24 34 H100" class="stroke-gray-400 dark:stroke-gray-400" stroke-width="3.2" stroke-linecap="round"/>
        <!-- قطره -->
        <g v-if="dropper"><circle cx="62" cy="10" r="4" :fill="dropColor" class="pv-drop"/><circle cx="62" cy="10" r="4" :fill="dropColor" class="pv-drop pv-drop2"/></g>

        <!-- مخزن (استوانه) -->
        <ellipse cx="262" cy="124" rx="48" ry="6" class="fill-gray-200/70 dark:fill-black/30"/>
        <path d="M226 30 H298 V108 Q298 116 262 116 Q226 116 226 108 Z" class="fill-white dark:fill-gray-900"/>
        <g clip-path="url(#pvClipT)">
          <rect x="222" :y="tankY" width="80" height="100" fill="url(#pvLiqT)" class="pv-liq"/>
          <path :d="wave(222, tankY, 80, 3.5, 3)" :fill="tankColor" opacity=".5" class="pv-wave"/>
          <rect x="222" y="26" width="80" height="94" fill="url(#pvGlass)"/>
        </g>
        <path d="M226 30 H298 V108 Q298 116 262 116 Q226 116 226 108 Z" fill="none" class="stroke-gray-300 dark:stroke-gray-500" stroke-width="2.4" stroke-linejoin="round"/>
        <ellipse cx="262" cy="30" rx="36" ry="7" class="fill-gray-100 dark:fill-gray-700 stroke-gray-300 dark:stroke-gray-500" stroke-width="2"/>
        <g class="stroke-gray-200 dark:stroke-gray-600" stroke-width="1.6"><line x1="226" y1="58" x2="298" y2="58"/><line x1="226" y1="86" x2="298" y2="86"/></g>

        <!-- جریان و ضریب -->
        <path d="M110 74 C150 74 176 74 214 74" fill="none" class="stroke-primary-400 pv-flow" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 8"/>
        <path d="M206 66 L218 74 L206 82" fill="none" class="stroke-primary-500" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <g v-if="scale">
          <rect x="136" y="56" width="52" height="24" rx="12" class="fill-primary-600"/>
          <text x="162" y="72.5" text-anchor="middle" fill="#fff" style="font-size:12.5px;font-weight:800">×{{ scaleText }}</text>
        </g>

        <!-- برچسب‌ها -->
        <text x="62" y="141" text-anchor="middle" class="fill-gray-600 dark:fill-gray-300" style="font-size:11px;font-weight:600">{{ sampleText }}</text>
        <text x="262" y="141" text-anchor="middle" class="fill-gray-600 dark:fill-gray-300" style="font-size:11px;font-weight:600">{{ tankText }}</text>
      </svg>

      <!-- دوز نهایی -->
      <Transition name="pvfade">
        <div v-if="doseLabel" class="mx-1 mt-1 rounded-xl bg-gradient-to-l from-primary-600 to-primary-500 text-white px-4 py-3 flex items-center justify-between shadow">
          <div><p class="text-[11px] opacity-80">{{ kind === 'base' ? 'باز' : 'اسید' }} لازم برای کل مخزن</p><p class="text-xl font-extrabold tabular-nums leading-7">{{ doseLabel }}</p></div>
          <svg class="w-9 h-9 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4a2 2 0 001.8-3l-5-9V3M8 15h8" /></svg>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  ph?: number | null; targetPh?: number | null; kind?: 'acid' | 'base' | null;
  tankVolume?: number | null; sampleVolume?: number | null; scale?: number | null;
  doseLabel?: string; dropper?: boolean; live?: boolean;
}>(), { ph: null, targetPh: null, kind: null, tankVolume: null, sampleVolume: null, scale: null, doseLabel: '', dropper: false, live: false });

const fa = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);
const MIN = 3, MAX = 11, CX = 160, CY = 160;
const clamp = (v: number) => Math.max(MIN, Math.min(MAX, v));
const ang = (v: number) => Math.PI * (1 - (clamp(v) - MIN) / (MAX - MIN));
const pt = (v: number, r: number) => ({ x: CX + r * Math.cos(ang(v)), y: CY - r * Math.sin(ang(v)) });
const arc = (r: number) => { const a = pt(MIN, r), b = pt(MAX, r); return `M${a.x} ${a.y} A${r} ${r} 0 0 1 ${b.x} ${b.y}`; };
const ticks = Array.from({ length: MAX - MIN + 1 }, (_, i) => {
  const v = MIN + i; const a = pt(v, 106), b = pt(v, 96), t = pt(v, 80);
  return { v, x1: a.x, y1: a.y, x2: b.x, y2: b.y, tx: t.x, ty: t.y };
});
const rot = computed(() => ((clamp(props.ph ?? MIN) - MIN) / (MAX - MIN)) * 180);
const phText = computed(() => (props.ph != null ? fa(props.ph, 2) : ''));
const gap = computed(() => (props.ph != null && props.targetPh != null ? props.ph - props.targetPh : null));

function phColor(v: number | null | undefined): string {
  if (v == null || !Number.isFinite(v)) return '#7dd3fc';
  const x = Math.max(3, Math.min(10, v));
  const hue = x <= 6 ? 5 + ((x - 3) / 3) * 115 : 120 + ((Math.min(x, 9) - 6) / 3) * 95;
  return `hsl(${hue.toFixed(0)} 70% 52%)`;
}
const color = computed(() => phColor(props.ph));
const tankColor = computed(() => phColor(props.doseLabel ? props.targetPh : props.ph));
const dropColor = computed(() => (props.kind === 'base' ? '#0ea5e9' : '#f59e0b'));
const sampleY = computed(() => (props.sampleVolume ? 52 : 74));
const tankY = computed(() => 50);
const wave = (x: number, y: number, w: number, a: number, n: number) => {
  const seg = w / (n * 2); let d = `M${x} ${y}`;
  for (let i = 0; i < n * 2; i++) d += ` q${seg / 2} ${i % 2 ? a : -a} ${seg} 0`;
  return d + ` V${y + 10} H${x} Z`;
};
const bubblesS = [0, 1, 2, 3].map((i) => ({ i, x: 44 + i * 13, r: 1.6 + (i % 2), d: i * 0.6 }));
const sampleText = computed(() => (props.sampleVolume ? `نمونه ${fa(props.sampleVolume, 2)} لیتر` : 'نمونه'));
const tankText = computed(() => (props.tankVolume ? `مخزن ${fa(props.tankVolume)} لیتر` : 'مخزن اصلی'));
const scaleText = computed(() => (props.scale ? fa(props.scale, props.scale < 10 ? 1 : 0) : ''));
</script>

<style scoped>
.pv-needle { transition: transform .9s cubic-bezier(.2, 1.2, .3, 1); color: #111827; }
:global(.dark) .pv-needle { color: #f9fafb; }
.pv-liq { transition: fill .4s, y .4s; }
.pv-wave { animation: pv-wave 3s ease-in-out infinite alternate; }
@keyframes pv-wave { from { transform: translateX(-5px); } to { transform: translateX(5px); } }
.pv-bub { animation: pv-rise 3.4s ease-in infinite; }
@keyframes pv-rise { 0% { transform: translateY(0); opacity: 0; } 20% { opacity: .7; } 100% { transform: translateY(-46px); opacity: 0; } }
.pv-flow { animation: pv-dash 1s linear infinite; }
@keyframes pv-dash { to { stroke-dashoffset: -20; } }
.pv-drop { animation: pv-drip 1.3s ease-in infinite; }
.pv-drop2 { animation-delay: .65s; }
@keyframes pv-drip { 0% { transform: translateY(0); opacity: 0; } 25% { opacity: 1; } 100% { transform: translateY(34px); opacity: 0; } }
.pvfade-enter-active, .pvfade-leave-active { transition: opacity .3s, transform .3s; }
.pvfade-enter-from, .pvfade-leave-to { opacity: 0; transform: translateY(6px); }
.tabular-nums { font-variant-numeric: tabular-nums; }
@media (prefers-reduced-motion: reduce) { .pv-wave, .pv-bub, .pv-flow, .pv-drop, .pv-needle { animation: none; transition: none; } }
</style>
