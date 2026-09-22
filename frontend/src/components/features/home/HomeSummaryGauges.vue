<!-- frontend/src/components/features/home/HomeSummaryGauges.vue -->
<!-- 🆕 خلاصه دایره‌ای صفحه خانه: دقت هدف، EC، هزینه -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="grid grid-cols-3 gap-3">
      <div class="flex flex-col items-center text-center">
        <svg width="76" height="76" viewBox="0 0 76 76">
          <circle cx="38" cy="38" r="30" fill="none" stroke="currentColor" class="text-gray-100 dark:text-gray-700" stroke-width="6" />
          <circle
            cx="38" cy="38" r="30" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"
            :class="accuracyRing" transform="rotate(-90 38 38)"
            :stroke-dasharray="RING_CIRC" :stroke-dashoffset="accuracyOffset"
          />
          <text x="38" y="42" text-anchor="middle" class="text-[13px] font-bold" :class="accuracyText">{{ accuracy.toFixed(1) }}٪</text>
        </svg>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">دقت هدف</p>
      </div>

      <div class="flex flex-col items-center text-center">
        <svg width="76" height="76" viewBox="0 0 76 76">
          <circle cx="38" cy="38" r="30" fill="none" stroke="currentColor" class="text-gray-100 dark:text-gray-700" stroke-width="6" />
          <circle
            cx="38" cy="38" r="30" fill="none" stroke-width="6" stroke-linecap="round"
            class="text-blue-500" stroke="currentColor" transform="rotate(-90 38 38)"
            :stroke-dasharray="RING_CIRC" :stroke-dashoffset="ecOffset"
          />
          <text x="38" y="42" text-anchor="middle" class="text-[13px] font-bold fill-blue-600 dark:fill-blue-400">{{ ec.toFixed(2) }}</text>
        </svg>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">EC (dS/m)</p>
      </div>

      <div class="flex flex-col items-center justify-center text-center">
        <p class="text-lg font-bold text-emerald-600 dark:text-emerald-400 tabular-nums">{{ costDisplay }}</p>
        <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">هزینه کل (تومان)</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  targetAchievement: Record<string, number>;
  ec: number;
  totalCost: number;
}>();

const RING_CIRC = 2 * Math.PI * 30;

const accuracy = computed(() => {
  const values = Object.values(props.targetAchievement || {});
  if (values.length === 0) return 0;
  const sum = values.reduce((total, value) => total + (Number(value) || 0), 0);
  return Math.max(0, Math.min(100, sum / values.length));
});

const accuracyOffset = computed(() => RING_CIRC * (1 - Math.min(accuracy.value, 100) / 100));
const accuracyRing = computed(() =>
  accuracy.value >= 95 ? 'text-emerald-500' : accuracy.value >= 85 ? 'text-amber-500' : 'text-rose-500'
);
const accuracyText = computed(() =>
  accuracy.value >= 95 ? 'fill-emerald-600 dark:fill-emerald-400' : accuracy.value >= 85 ? 'fill-amber-600 dark:fill-amber-400' : 'fill-rose-600 dark:fill-rose-400'
);

// EC مطلوب معمولاً حدود ۰.۸ تا ۲.۵ است؛ برای نمایش حلقه، نسبت به سقف ۳.۵ مقیاس می‌شود
const ec = computed(() => Number(props.ec) || 0);
const ecOffset = computed(() => RING_CIRC * (1 - Math.min(ec.value / 3.5, 1)));

const costDisplay = computed(() => Math.round(props.totalCost || 0).toLocaleString('fa-IR'));
</script>
