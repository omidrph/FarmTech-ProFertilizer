<!-- frontend/src/components/features/home/HomeHeroCard.vue -->
<!--
  کارت اصلی صفحه خانه: نمای کلی وضعیت فرمول
  ------------------------------------------------------------
  - نوار وضعیت بالای کارت با یک جمله خلاصه
  - نمودار دایره‌ای بزرگ «دقت رسیدن به هدف»
  - سه شاخص کلیدی (EC، هزینه، تعداد کود)
  - دو دکمه اصلی
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm">
    <!-- نوار وضعیت -->
    <div
      class="px-4 sm:px-6 py-3 border-b flex items-center justify-between gap-3"
      :class="statusBarClasses"
    >
      <div class="flex items-center gap-2.5 min-w-0">
        <span class="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center" :class="statusIconWrapClasses">
          <svg v-if="tone === 'good'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="tone === 'warn'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </span>
        <span class="text-sm font-medium truncate" :class="statusTextClasses">{{ statusBarText }}</span>
      </div>
      <span v-if="lastUpdatedText" class="text-[11px] flex-shrink-0 hidden sm:inline" :class="statusTextClasses">
        {{ lastUpdatedText }}
      </span>
    </div>

    <!-- بدنه اصلی -->
    <div class="p-4 sm:p-6">
      <div class="flex flex-col sm:flex-row items-center gap-4 sm:gap-8">

        <!-- نمودار دایره‌ای -->
        <div class="relative w-[132px] h-[132px] sm:w-[156px] sm:h-[156px] flex-shrink-0">
          <svg viewBox="0 0 150 150" class="w-full h-full" role="img" :aria-label="`دقت ${accuracyText} درصد`">
            <circle cx="75" cy="75" r="62" fill="none" stroke-width="10" class="stroke-gray-100 dark:stroke-gray-700/60" />
            <circle
              cx="75" cy="75" r="62" fill="none" stroke-width="10" stroke-linecap="round"
              stroke="currentColor"
              :class="[ringColor, 'ring-progress']"
              :stroke-dasharray="CIRC"
              :stroke-dashoffset="offset"
              transform="rotate(-90 75 75)"
            />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span class="text-[28px] sm:text-[34px] font-bold tabular-nums leading-none" :class="ringColor">
              {{ accuracyText }}<span class="text-lg">٪</span>
            </span>
            <span class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400 mt-1">دقت هدف</span>
          </div>
        </div>

        <!-- محتوا -->
        <div class="flex-1 min-w-0 w-full">
          <!-- خلاصه وضعیت عناصر: جایگزین متن تکراری -->
          <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700 px-3.5 py-3">
            <p class="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1 mb-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              خلاصه وضعیت عناصر
            </p>
            <p class="text-sm font-medium text-gray-800 dark:text-gray-100 leading-6">
              {{ summaryText }}
            </p>
          </div>

          <!-- شاخص‌ها -->
          <div class="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3">
            <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700 px-3 py-2.5">
              <p class="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                EC نهایی
              </p>
              <p class="mt-1 text-base sm:text-lg font-bold tabular-nums leading-tight"
                 :class="ecOutOfRange ? 'text-amber-600 dark:text-amber-400' : 'text-gray-900 dark:text-white'">
                {{ ecText }}<span class="text-[11px] font-normal text-gray-400 mr-1"> dS/m</span>
              </p>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700 px-3 py-2.5">
              <p class="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7.5A1.5 1.5 0 014.5 6h13A1.5 1.5 0 0119 7.5V9H4.5A1.5 1.5 0 013 7.5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9h16.5A1.5 1.5 0 0121 10.5v7a1.5 1.5 0 01-1.5 1.5H4.5A1.5 1.5 0 013 17.5V9z" />
                </svg>
                هزینه فرمول
              </p>
              <p class="mt-1 text-base sm:text-lg font-bold tabular-nums leading-tight text-gray-900 dark:text-white">
                {{ costText }}<span class="text-[11px] font-normal text-gray-400 mr-1"> تومان</span>
              </p>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700 px-3 py-2.5">
              <p class="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                کودهای فرمول
              </p>
              <p class="mt-1 text-base sm:text-lg font-bold tabular-nums leading-tight text-gray-900 dark:text-white">
                {{ fertilizersCount.toLocaleString('fa-IR') }}<span class="text-[11px] font-normal text-gray-400 mr-1"> کود</span>
              </p>
            </div>
          </div>

          <!-- دکمه‌ها -->
          <div class="mt-5 flex flex-col sm:flex-row gap-2">
            <button
              type="button"
              @click="emit('view-details')"
              class="inline-flex items-center justify-center gap-2 px-5 py-3 sm:py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors shadow-sm hover:shadow-md"
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
              class="inline-flex items-center justify-center gap-2 px-5 py-3 sm:py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <svg v-if="!isExporting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17v3a1 1 0 001 1h16a1 1 0 001-1v-3M12 3v7" />
              </svg>
              <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              {{ isExporting ? 'در حال آماده‌سازی...' : 'خروجی PDF' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';

const props = withDefaults(
  defineProps<{
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
    lastUpdatedText?: string;
    /** 🆕 متن خلاصه وضعیت عناصر برای جایگزینی متن تکراری قبلی */
    summaryText?: string;
  }>(),
  {
    lastUpdatedText: '',
    summaryText: ''
  }
);

const emit = defineEmits<{
  (e: 'view-details'): void;
  (e: 'export-pdf'): void;
}>();

const CIRC = 2 * Math.PI * 62;

const ready = ref(false);
onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true;
  });
});

const offset = computed(
  () => CIRC * (1 - (ready.value ? Math.max(0, Math.min(100, props.accuracy)) : 0) / 100)
);

const ringColor = computed(() =>
  props.tone === 'good'
    ? 'text-emerald-500'
    : props.tone === 'warn'
      ? 'text-amber-500'
      : 'text-rose-500'
);

const statusBarClasses = computed(() => {
  if (props.tone === 'good')
    return 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-100 dark:border-emerald-800/60';
  if (props.tone === 'warn')
    return 'bg-amber-50 dark:bg-amber-950/40 border-amber-100 dark:border-amber-800/60';
  return 'bg-rose-50 dark:bg-rose-950/40 border-rose-100 dark:border-rose-800/60';
});

const statusIconWrapClasses = computed(() => {
  if (props.tone === 'good')
    return 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400';
  if (props.tone === 'warn')
    return 'bg-amber-100 dark:bg-amber-900/50 text-amber-600 dark:text-amber-400';
  return 'bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400';
});

const statusTextClasses = computed(() => {
  if (props.tone === 'good') return 'text-emerald-700 dark:text-emerald-300';
  if (props.tone === 'warn') return 'text-amber-700 dark:text-amber-300';
  return 'text-rose-700 dark:text-rose-300';
});

const statusBarText = computed(() => {
  if (props.tone === 'good') return 'وضعیت فرمول: مطلوب و آماده استفاده';
  if (props.tone === 'warn') return 'وضعیت فرمول: نیازمند بررسی';
  return 'وضعیت فرمول: نیازمند اصلاح';
});
</script>

<style scoped>
.ring-progress {
  transition: stroke-dashoffset 1.1s cubic-bezier(0.22, 1, 0.36, 1);
}
@media (prefers-reduced-motion: reduce) {
  .ring-progress {
    transition: none;
  }
}
</style>