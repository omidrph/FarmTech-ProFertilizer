<!-- frontend/src/components/features/home/HomeIonBalance.vue -->
<!--
  کارت تعادل یونی: دو نوار افقی کاتیون و آنیون
  ------------------------------------------------------------
  - رنگ آبی برای کاتیون و رز برای آنیون
  - خلاصه اختلاف با رنگ‌بندی وضعیتی
  - کنتراست بالا در dark mode
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- هدر -->
    <header class="px-4 sm:px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v3m0 0l-6 12a5 5 0 0010 0L12 6zm0 0l6 12a5 5 0 01-10 0M4 9h4m8 0h4" />
          </svg>
        </span>
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">تعادل یونی</h3>
      </div>

      <span
        class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1"
        :class="balanced
          ? 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300'
          : 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-300'"
      >
        <svg v-if="balanced" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01" />
        </svg>
        {{ balanced ? 'متعادل' : 'نامتعادل' }}
      </span>
    </header>

    <!-- محتوا -->
    <div class="p-4 sm:p-5">
      <template v-if="hasData">
        <div class="space-y-4">
          <!-- کاتیون -->
          <div>
            <div class="flex justify-between items-center text-xs mb-1.5">
              <span class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                کاتیون
              </span>
              <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">
                {{ fmt(cation) }} <span class="text-[10px] text-gray-400">meq/L</span>
              </span>
            </div>
            <div class="relative h-2.5 rounded-full bg-gray-100 dark:bg-gray-700/60 overflow-hidden">
              <div
                class="absolute top-0 right-0 h-full rounded-full bg-gradient-to-l from-blue-500 to-blue-400 transition-all duration-700"
                :style="{ width: cationWidth }"
              ></div>
            </div>
          </div>

          <!-- آنیون -->
          <div>
            <div class="flex justify-between items-center text-xs mb-1.5">
              <span class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                آنیون
              </span>
              <span class="tabular-nums font-medium text-gray-700 dark:text-gray-200">
                {{ fmt(anion) }} <span class="text-[10px] text-gray-400">meq/L</span>
              </span>
            </div>
            <div class="relative h-2.5 rounded-full bg-gray-100 dark:bg-gray-700/60 overflow-hidden">
              <div
                class="absolute top-0 right-0 h-full rounded-full bg-gradient-to-l from-rose-500 to-rose-400 transition-all duration-700"
                :style="{ width: anionWidth }"
              ></div>
            </div>
          </div>
        </div>

        <!-- خلاصه اختلاف -->
        <div class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between text-xs">
          <span class="text-gray-500 dark:text-gray-400">اختلاف</span>
          <span
            class="tabular-nums font-bold"
            :class="balanced ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'"
          >
            {{ fmt(Math.abs(cation - anion)) }} <span class="text-[10px] font-normal text-gray-400">meq/L</span>
          </span>
        </div>
      </template>

      <p v-else class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
        داده‌ای برای نمایش نیست.
      </p>
    </div>
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
  Number(value || 0).toLocaleString('fa-IR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

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