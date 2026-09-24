<!-- frontend/src/components/features/home/HomeReservoirs.vue -->
<!-- خلاصه‌ی مخازن A / B / C: فقط تعداد کود هر مخزن -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white mb-3">مخازن</h3>
    <div class="grid grid-cols-3 gap-2">
      <div
        v-for="tank in tanks"
        :key="tank.key"
        class="rounded-xl bg-gray-50 dark:bg-gray-700/30 px-2 py-2.5 text-center"
      >
        <p class="text-xs text-gray-500 dark:text-gray-400">مخزن {{ tank.key }}</p>
        <p class="mt-0.5 text-sm font-bold" :class="tank.count ? 'text-gray-900 dark:text-white' : 'text-gray-300 dark:text-gray-600'">
          {{ tank.count ? `${tank.count.toLocaleString('fa-IR')} کود` : '—' }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  counts: { A: number; B: number; C: number };
}>();

const tanks = computed(() => [
  { key: 'A', count: props.counts.A },
  { key: 'B', count: props.counts.B },
  { key: 'C', count: props.counts.C }
]);
</script>
