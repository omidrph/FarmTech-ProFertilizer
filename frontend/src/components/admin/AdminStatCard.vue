<!-- کارت شاخص: آیکون رنگی، عدد بزرگ، روند نسبت به دورهٔ قبل و خط روند کوچک -->
<template>
  <div class="ad-card ad-hover p-4 relative overflow-hidden">
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0">
        <p class="text-[11px] font-medium text-gray-500 dark:text-gray-400">{{ title }}</p>
        <p class="mt-1.5 text-[1.7rem] leading-none font-extrabold tabular-nums text-gray-900 dark:text-white">
          {{ value }}<span v-if="unit" class="text-xs font-medium text-gray-400 mr-1">{{ unit }}</span>
        </p>
      </div>
      <span class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0" :style="{ background: color + '1a', color }">
        <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" :d="icon" /></svg>
      </span>
    </div>
    <div class="mt-3 flex items-end justify-between gap-2">
      <div class="min-w-0">
        <span v-if="trend !== null && trend !== undefined" class="inline-flex items-center gap-0.5 text-[11px] font-semibold px-1.5 py-0.5 rounded-md tabular-nums"
          :class="good ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-rose-50 text-rose-700 dark:bg-rose-900/30 dark:text-rose-300'">
          <svg class="w-3 h-3" :class="trend < 0 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.4"><path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7" /></svg>
          {{ faNum(Math.abs(trend), 0) }}٪
        </span>
        <span v-else-if="sub" class="text-[11px] text-gray-400">{{ sub }}</span>
        <p v-if="trend !== null && trend !== undefined && sub" class="text-[10px] text-gray-400 mt-1 truncate">{{ sub }}</p>
      </div>
      <AdminSparkline v-if="spark && spark.length > 1" :values="spark" :color="color" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import AdminSparkline from './charts/AdminSparkline.vue';
import { faNum } from './charts/chartUtils';
const props = withDefaults(defineProps<{
  title: string; value: string; unit?: string; trend?: number | null; sub?: string; spark?: number[];
  color?: string; icon: string; invert?: boolean;
}>(), { color: '#2563eb' });
// «invert»: برای شاخص‌هایی که کاهششان خوب است (مثل خطا)
const good = computed(() => (props.trend ?? 0) >= 0 !== !!props.invert);
</script>
