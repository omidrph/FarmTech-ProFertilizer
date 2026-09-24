<!-- frontend/src/components/features/home/HomeHeroCard.vue -->
<!--
  کارت اصلی صفحه خانه بعد از محاسبه:
  نمودار دایره‌ای بزرگ «دقت رسیدن به هدف» + وضعیت فرمول + شاخص‌های کلیدی + دکمه‌های اصلی
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
    <div class="flex flex-col sm:flex-row items-center gap-4 sm:gap-8">

      <!-- نمودار دایره‌ای بزرگ (روی موبایل کمی کوچک‌تر) -->
      <div class="relative w-[128px] h-[128px] sm:w-[150px] sm:h-[150px] flex-shrink-0">
        <svg viewBox="0 0 150 150" class="w-full h-full" role="img" :aria-label="`دقت ${accuracyText} درصد`">
          <circle cx="75" cy="75" r="62" fill="none" stroke-width="12" class="stroke-gray-100 dark:stroke-gray-700" />
          <circle
            cx="75" cy="75" r="62" fill="none" stroke-width="12" stroke-linecap="round"
            stroke="currentColor"
            :class="[ringColor, 'ring-progress']"
            :stroke-dasharray="CIRC"
            :stroke-dashoffset="offset"
            transform="rotate(-90 75 75)"
          />
        </svg>
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-[26px] sm:text-3xl font-bold tabular-nums leading-tight" :class="ringColor">{{ accuracyText }}٪</span>
          <span class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400">دقت هدف</span>
        </div>
      </div>

      <!-- وضعیت و شاخص‌ها -->
      <div class="flex-1 min-w-0 w-full">
        <div class="flex items-start justify-center sm:justify-start gap-2">
          <span class="w-6 h-6 sm:w-7 sm:h-7 mt-0.5 rounded-full flex items-center justify-center flex-shrink-0 text-white" :class="badgeClass">
            <svg v-if="tone === 'good'" class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01" />
            </svg>
          </span>
          <h3 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white leading-7 text-center sm:text-right">{{ title }}</h3>
        </div>
        <p class="mt-1 text-xs sm:text-sm text-gray-500 dark:text-gray-400 text-center sm:text-right leading-5">{{ subtitle }}</p>

        <!-- شاخص‌ها: موبایل = لیست ردیفی، دسکتاپ = سه ستون -->
        <dl class="mt-4 rounded-xl bg-gray-50 dark:bg-gray-700/30 divide-y divide-gray-200/70 dark:divide-gray-600/50 sm:bg-transparent sm:dark:bg-transparent sm:divide-y-0 sm:rounded-none sm:grid sm:grid-cols-3 sm:gap-4">
          <div class="flex items-baseline justify-between gap-3 px-3 py-2.5 sm:block sm:px-0 sm:py-0">
            <dt class="text-xs text-gray-500 dark:text-gray-400">EC نهایی</dt>
            <dd class="sm:mt-0.5 text-base sm:text-lg font-bold tabular-nums whitespace-nowrap" :class="ecOutOfRange ? 'text-amber-600 dark:text-amber-400' : 'text-gray-900 dark:text-white'">
              {{ ecText }} <span class="text-[11px] font-normal text-gray-400">dS/m</span>
            </dd>
          </div>
          <div class="flex items-baseline justify-between gap-3 px-3 py-2.5 sm:block sm:px-0 sm:py-0">
            <dt class="text-xs text-gray-500 dark:text-gray-400">هزینه فرمول</dt>
            <dd class="sm:mt-0.5 text-base sm:text-lg font-bold tabular-nums whitespace-nowrap text-gray-900 dark:text-white">
              {{ costText }} <span class="text-[11px] font-normal text-gray-400">تومان</span>
            </dd>
          </div>
          <div class="flex items-baseline justify-between gap-3 px-3 py-2.5 sm:block sm:px-0 sm:py-0">
            <dt class="text-xs text-gray-500 dark:text-gray-400">کودهای فرمول</dt>
            <dd class="sm:mt-0.5 text-base sm:text-lg font-bold tabular-nums whitespace-nowrap text-gray-900 dark:text-white">
              {{ fertilizersCount.toLocaleString('fa-IR') }} <span class="text-[11px] font-normal text-gray-400">کود</span>
            </dd>
          </div>
        </dl>

        <!-- دکمه‌ها: موبایل = زیر هم و تمام‌عرض، دسکتاپ = کنار هم -->
        <div class="mt-4 sm:mt-5 flex flex-col sm:flex-row sm:flex-wrap gap-2">
          <button
            type="button"
            @click="emit('view-details')"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-3 sm:py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors"
          >
            مشاهده نتیجه کامل
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            type="button"
            @click="emit('export-pdf')"
            :disabled="isExporting"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-3 sm:py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17v3a1 1 0 001 1h16a1 1 0 001-1v-3M12 3v7" />
            </svg>
            {{ isExporting ? 'در حال آماده‌سازی...' : 'خروجی PDF' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';

const props = defineProps<{
  tone: 'good' | 'warn' | 'bad';
  title: string;
  subtitle: string;
  accuracy: number;
  accuracyText: string;
  ecText: string;
  ecOutOfRange: boolean;
  costText: string;
  fertilizersCount: number;
  isExporting: boolean;
}>();

const emit = defineEmits<{
  (e: 'view-details'): void;
  (e: 'export-pdf'): void;
}>();

const CIRC = 2 * Math.PI * 62;

// حلقه از صفر شروع می‌شود و بعد از نمایش، به مقدار واقعی پر می‌شود
const ready = ref(false);
onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true;
  });
});

const offset = computed(() => CIRC * (1 - (ready.value ? Math.max(0, Math.min(100, props.accuracy)) : 0) / 100));

const ringColor = computed(() =>
  props.tone === 'good'
    ? 'text-emerald-500'
    : props.tone === 'warn'
      ? 'text-amber-500'
      : 'text-rose-500'
);

const badgeClass = computed(() =>
  props.tone === 'good' ? 'bg-emerald-500' : props.tone === 'warn' ? 'bg-amber-500' : 'bg-rose-500'
);
</script>

<style scoped>
.ring-progress {
  transition: stroke-dashoffset 1s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (prefers-reduced-motion: reduce) {
  .ring-progress {
    transition: none;
  }
}
</style>