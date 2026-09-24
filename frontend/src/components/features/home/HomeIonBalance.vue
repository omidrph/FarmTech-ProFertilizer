<!-- frontend/src/components/features/home/HomeIonBalance.vue -->
<!-- تعادل یونی فرمول: دو نوار افقی کاتیون و آنیون -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3 mb-4">
      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">تعادل یونی</h3>
      <span
        class="text-[11px] font-medium px-2 py-0.5 rounded-full"
        :class="balanced
          ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400'
          : 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400'"
      >{{ balanced ? 'متعادل' : 'نامتعادل' }}</span>
    </div>

    <template v-if="hasData">
      <div class="space-y-3">
        <div>
          <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
            <span>کاتیون</span>
            <span class="tabular-nums">{{ fmt(cation) }} meq/L</span>
          </div>
          <div class="h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
            <div class="h-full rounded-full bg-primary-500 bar" :style="{ width: cationWidth }"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
            <span>آنیون</span>
            <span class="tabular-nums">{{ fmt(anion) }} meq/L</span>
          </div>
          <div class="h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
            <div class="h-full rounded-full bg-amber-500 bar" :style="{ width: anionWidth }"></div>
          </div>
        </div>
      </div>
      <p class="mt-3 text-[11px] text-gray-400 dark:text-gray-500">اختلاف: {{ fmt(Math.abs(cation - anion)) }} meq/L</p>
    </template>

    <p v-else class="py-3 text-center text-sm text-gray-500 dark:text-gray-400">داده‌ای برای نمایش نیست.</p>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';

const props = defineProps<{
  cation: number;
  anion: number;
  balanced: boolean;
}>();

const fmt = (value: number) =>
  Number(value || 0).toLocaleString('fa-IR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

const hasData = computed(() => props.cation > 0 || props.anion > 0);
const maxValue = computed(() => Math.max(props.cation, props.anion, 0.0001));

const ready = ref(false);
onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true;
  });
});

const cationWidth = computed(() => (ready.value ? `${(props.cation / maxValue.value) * 100}%` : '0%'));
const anionWidth = computed(() => (ready.value ? `${(props.anion / maxValue.value) * 100}%` : '0%'));
</script>

<style scoped>
.bar {
  transition: width 0.9s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (prefers-reduced-motion: reduce) {
  .bar {
    transition: none;
  }
}
</style>
