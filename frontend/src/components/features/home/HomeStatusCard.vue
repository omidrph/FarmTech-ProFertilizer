<!-- frontend/src/components/features/home/HomeStatusCard.vue -->
<!-- حالت ۳ صفحه خانه: کارت وضعیت کلی فرمول (دقت، EC، هزینه) بعد از محاسبه -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-2 min-w-0">
        <span
          class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-white"
          :class="badgeClass"
        >
          <svg v-if="tone === 'good'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01" />
          </svg>
        </span>
        <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white truncate">{{ title }}</h3>
      </div>
      <span
        class="flex-shrink-0 text-xs"
        :class="ionBalanced ? 'text-gray-500 dark:text-gray-400' : 'text-amber-600 dark:text-amber-400'"
      >
        {{ ionBalanced ? 'تعادل یونی مطلوب' : 'عدم تعادل یونی' }}
      </span>
    </div>

    <div class="grid grid-cols-3 gap-2 sm:gap-3 mt-4">
      <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 px-2 py-3 text-center">
        <p class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400">دقت رسیدن به هدف</p>
        <p class="mt-1 text-lg sm:text-2xl font-bold tabular-nums" :class="textClass">{{ accuracyText }}٪</p>
      </div>
      <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 px-2 py-3 text-center">
        <p class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400">EC نهایی</p>
        <p
          class="mt-1 text-lg sm:text-2xl font-bold tabular-nums"
          :class="ecOutOfRange ? 'text-amber-600 dark:text-amber-400' : 'text-gray-900 dark:text-white'"
        >{{ ecText }}</p>
        <p class="text-[10px] text-gray-400 dark:text-gray-500">dS/m</p>
      </div>
      <div class="rounded-xl bg-gray-50 dark:bg-gray-700/30 px-2 py-3 text-center">
        <p class="text-[11px] sm:text-xs text-gray-500 dark:text-gray-400">هزینه فرمول</p>
        <p class="mt-1 text-lg sm:text-2xl font-bold tabular-nums text-gray-900 dark:text-white">{{ costText }}</p>
        <p class="text-[10px] text-gray-400 dark:text-gray-500">تومان</p>
      </div>
    </div>

    <div class="mt-4 pt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between gap-3">
      <span class="text-xs text-gray-500 dark:text-gray-400">
        {{ elementsCount.toLocaleString('fa-IR') }} عنصر هدف
        · {{ reservoirsCount.toLocaleString('fa-IR') }} مخزن
        · {{ fertilizersCount.toLocaleString('fa-IR') }} کود
      </span>
      <button
        type="button"
        @click="emit('view-details')"
        class="flex-shrink-0 inline-flex items-center gap-1 text-sm font-medium text-primary-600 dark:text-primary-400 hover:underline"
      >
        مشاهده نتیجه کامل
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  tone: 'good' | 'warn' | 'bad';
  title: string;
  ionBalanced: boolean;
  accuracyText: string;
  ecText: string;
  ecOutOfRange: boolean;
  costText: string;
  elementsCount: number;
  reservoirsCount: number;
  fertilizersCount: number;
}>();

const emit = defineEmits<{
  (e: 'view-details'): void;
}>();

const badgeClass = computed(() =>
  props.tone === 'good' ? 'bg-emerald-500' : props.tone === 'warn' ? 'bg-amber-500' : 'bg-rose-500'
);

const textClass = computed(() =>
  props.tone === 'good'
    ? 'text-emerald-600 dark:text-emerald-400'
    : props.tone === 'warn'
      ? 'text-amber-600 dark:text-amber-400'
      : 'text-rose-600 dark:text-rose-400'
);
</script>
