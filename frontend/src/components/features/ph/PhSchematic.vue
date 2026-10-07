<!-- frontend/src/components/features/ph/PhSchematic.vue -->
<!--
  شماتیک کار در گلخانه: مخزن اصلی → نمونه (سطل) → قطره‌چکان اسید/باز.
  رنگ مایع بر اساس pH (مثل کاغذ تورنسل): قرمز/نارنجی اسیدی ← سبز نزدیک ۶ ← آبی قلیایی.
  چون صفحه راست‌به‌چپ است، مخزن سمت راست و سطل سمت چپ قرار می‌گیرد (جهت خواندن).
-->
<template>
  <figure class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-gradient-to-b from-sky-50/60 to-white dark:from-gray-800 dark:to-gray-800/60 p-3 sm:p-4">
    <svg viewBox="0 0 400 210" class="w-full h-auto select-none" role="img" :aria-label="ariaLabel">
      <defs>
        <clipPath id="ph-tank-clip"><rect x="262" y="52" width="108" height="118" rx="12" /></clipPath>
        <clipPath id="ph-bucket-clip"><path d="M64 96 H156 L146 170 Q145 176 139 176 H81 Q75 176 74 170 Z" /></clipPath>
      </defs>

      <!-- ===== مخزن اصلی (راست) ===== -->
      <g>
        <rect x="262" y="52" width="108" height="118" rx="12" class="fill-white dark:fill-gray-900/40 stroke-gray-300 dark:stroke-gray-600" stroke-width="2.5" />
        <g clip-path="url(#ph-tank-clip)">
          <rect x="262" :y="tankLiquidY" width="108" :height="170 - tankLiquidY" :fill="tankColor" opacity="0.85" class="transition-all duration-500" />
          <path :d="`M262 ${tankLiquidY} q13.5 -6 27 0 t27 0 t27 0 t27 0 V${tankLiquidY + 8} H262 Z`" :fill="tankColor" opacity="0.5" />
        </g>
        <rect x="262" y="52" width="108" height="118" rx="12" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="2.5" />
        <!-- خطوط درجه -->
        <g class="stroke-gray-300 dark:stroke-gray-600" stroke-width="1.5">
          <line x1="262" y1="82" x2="276" y2="82" /><line x1="262" y1="111" x2="272" y2="111" /><line x1="262" y1="140" x2="276" y2="140" />
        </g>
        <text x="316" y="40" text-anchor="middle" class="fill-gray-700 dark:fill-gray-200" style="font-size:12px;font-weight:700">مخزن اصلی</text>
        <text x="316" y="190" text-anchor="middle" class="fill-gray-500 dark:fill-gray-400" style="font-size:11px">{{ tankText }}</text>
        <!-- لوله ورودی -->
        <path d="M370 70 h14 v-20" fill="none" class="stroke-gray-300 dark:stroke-gray-600" stroke-width="3" stroke-linecap="round" />
      </g>

      <!-- ===== فلش مقیاس‌دهی ===== -->
      <g v-if="scale">
        <path d="M252 112 H170" class="stroke-primary-500" stroke-width="2.5" stroke-dasharray="5 5" fill="none" />
        <path d="M178 106 L168 112 L178 118" class="stroke-primary-500" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
        <rect x="186" y="88" width="56" height="20" rx="10" class="fill-primary-600" />
        <text x="214" y="102" text-anchor="middle" fill="#fff" style="font-size:11px;font-weight:700">×{{ scaleText }}</text>
      </g>

      <!-- ===== سطل نمونه (چپ) ===== -->
      <g>
        <path d="M64 96 H156 L146 170 Q145 176 139 176 H81 Q75 176 74 170 Z" class="fill-white dark:fill-gray-900/40" />
        <g clip-path="url(#ph-bucket-clip)">
          <rect x="60" :y="bucketLiquidY" width="100" :height="180 - bucketLiquidY" :fill="bucketColor" opacity="0.9" class="transition-all duration-500" />
          <path :d="`M60 ${bucketLiquidY} q12.5 -5 25 0 t25 0 t25 0 t25 0 V${bucketLiquidY + 8} H60 Z`" :fill="bucketColor" opacity="0.5" />
        </g>
        <path d="M64 96 H156 L146 170 Q145 176 139 176 H81 Q75 176 74 170 Z" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="2.5" stroke-linejoin="round" />
        <!-- دستهٔ سطل -->
        <path d="M70 96 Q110 62 150 96" fill="none" class="stroke-gray-400 dark:stroke-gray-500" stroke-width="2.5" stroke-linecap="round" />
        <text x="110" y="198" text-anchor="middle" class="fill-gray-500 dark:fill-gray-400" style="font-size:11px">{{ sampleText }}</text>

        <!-- pH روی سطل -->
        <g v-if="ph != null">
          <rect x="84" y="124" width="52" height="24" rx="12" class="fill-white/90 dark:fill-gray-900/80 stroke-gray-300 dark:stroke-gray-600" stroke-width="1.5" />
          <text x="110" y="140.5" text-anchor="middle" class="fill-gray-800 dark:fill-gray-100" style="font-size:13px;font-weight:700">pH {{ phText }}</text>
        </g>
      </g>

      <!-- ===== قطره‌چکان / بطری اسید ===== -->
      <g v-if="showDropper" class="ph-bob">
        <g :transform="`translate(${kind === 'base' ? 96 : 96} 10)`">
          <rect x="6" y="0" width="28" height="46" rx="7" :fill="kind === 'base' ? '#38bdf8' : '#f59e0b'" opacity="0.95" />
          <rect x="12" y="-8" width="16" height="10" rx="3" class="fill-gray-500 dark:fill-gray-400" />
          <path d="M20 46 v14" :stroke="kind === 'base' ? '#38bdf8' : '#f59e0b'" stroke-width="3" stroke-linecap="round" />
          <text x="20" y="28" text-anchor="middle" fill="#fff" style="font-size:12px;font-weight:700">{{ kind === 'base' ? 'باز' : 'اسید' }}</text>
        </g>
        <circle cx="116" cy="76" r="3.2" :fill="kind === 'base' ? '#38bdf8' : '#f59e0b'" class="ph-drop" />
        <circle cx="116" cy="76" r="3.2" :fill="kind === 'base' ? '#38bdf8' : '#f59e0b'" class="ph-drop ph-drop-2" />
      </g>

      <!-- ===== نتیجه: برچسب دوز مخزن ===== -->
      <g v-if="doseLabel">
        <rect x="150" y="150" width="104" height="28" rx="14" class="fill-emerald-600" />
        <text x="202" y="168.5" text-anchor="middle" fill="#fff" style="font-size:12px;font-weight:700">{{ doseLabel }}</text>
      </g>
    </svg>
    <figcaption v-if="caption" class="mt-1.5 text-center text-[11px] sm:text-xs text-gray-500 dark:text-gray-400 leading-5">{{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  tankVolume?: number | null;
  sampleVolume?: number | null;
  scale?: number | null;
  ph?: number | null;
  targetPh?: number | null;
  kind?: 'acid' | 'base' | null;
  showDropper?: boolean;
  doseLabel?: string;
  caption?: string;
}>(), { tankVolume: null, sampleVolume: null, scale: null, ph: null, targetPh: null, kind: null, showDropper: false, doseLabel: '', caption: '' });

const fa = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d }).format(n);

/** رنگ مایع از روی pH (۴ قرمز ← ۶ سبز ← ۹ آبی) */
function phColor(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return '#7dd3fc';
  const v = Math.max(3, Math.min(10, value));
  // hue: 5 (قرمز) در pH 3 ، 120 (سبز) در pH 6 ، 215 (آبی) در pH 9 به بعد
  let hue: number;
  if (v <= 6) hue = 5 + ((v - 3) / 3) * 115;
  else hue = 120 + ((Math.min(v, 9) - 6) / 3) * 95;
  return `hsl(${hue.toFixed(0)} 72% 55%)`;
}

const bucketColor = computed(() => phColor(props.ph));
const tankColor = computed(() => phColor(props.ph != null ? props.ph : props.targetPh));
const tankLiquidY = computed(() => 82);
const bucketLiquidY = computed(() => (props.sampleVolume ? 118 : 150));

const tankText = computed(() => (props.tankVolume ? `${fa(props.tankVolume)} لیتر` : 'حجم مخزن؟'));
const sampleText = computed(() => (props.sampleVolume ? `نمونه ${fa(props.sampleVolume, 2)} لیتر` : 'نمونه'));
const scaleText = computed(() => (props.scale ? fa(props.scale, props.scale < 10 ? 1 : 0) : ''));
const phText = computed(() => (props.ph != null ? fa(props.ph, 2) : ''));
const ariaLabel = computed(() => `شماتیک مخزن اصلی ${tankText.value} و نمونه ${sampleText.value}`);
</script>

<style scoped>
.ph-bob { animation: ph-bob 2.4s ease-in-out infinite; }
@keyframes ph-bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(3px); } }
.ph-drop { animation: ph-drip 1.4s ease-in infinite; }
.ph-drop-2 { animation-delay: .7s; }
@keyframes ph-drip { 0% { transform: translateY(-4px); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(30px); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .ph-bob, .ph-drop { animation: none; } }
</style>
