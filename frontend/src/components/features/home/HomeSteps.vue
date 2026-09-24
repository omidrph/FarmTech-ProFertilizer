<!-- frontend/src/components/features/home/HomeSteps.vue -->
<!--
  «مراحل محاسبه کود» (حالت ۲ صفحه خانه: گزارش باز است ولی هنوز محاسبه‌ای انجام نشده)
  کاربر را مرحله‌به‌مرحله جلو می‌برد: مرحله‌ی جاری برجسته است و دکمه‌ی اقدام دارد؛
  مراحل اختیاری را می‌شود رد کرد؛ مراحل انجام‌شده سبز می‌شوند.
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3">
      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">مراحل محاسبه کود</h3>
      <span class="text-xs text-gray-500 dark:text-gray-400 tabular-nums">
        {{ completedCount.toLocaleString('fa-IR') }} از {{ steps.length.toLocaleString('fa-IR') }} مرحله
      </span>
    </div>

    <div
      class="mt-3 h-1.5 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden"
      role="progressbar"
      :aria-valuenow="completedCount"
      aria-valuemin="0"
      :aria-valuemax="steps.length"
    >
      <div
        class="h-full rounded-full bg-emerald-500 transition-all duration-500"
        :style="{ width: progressPercent + '%' }"
      ></div>
    </div>

    <ol class="mt-4">
      <li
        v-for="(step, index) in steps"
        :key="step.key"
        class="relative flex gap-3"
        :class="index < steps.length - 1 ? 'pb-3' : ''"
      >
        <!-- خط اتصال مراحل -->
        <span
          v-if="index < steps.length - 1"
          class="absolute top-9 bottom-0 right-[15px] w-0.5 rounded-full"
          :class="step.status === 'done' ? 'bg-emerald-300 dark:bg-emerald-700' : 'bg-gray-200 dark:bg-gray-700'"
        ></span>

        <!-- دایره‌ی وضعیت -->
        <span
          class="relative z-10 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold transition-colors"
          :class="circleClass(step)"
        >
          <svg v-if="step.status === 'done'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="step.status === 'skipped'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 12h12" />
          </svg>
          <template v-else>{{ (index + 1).toLocaleString('fa-IR') }}</template>
        </span>

        <!-- محتوای مرحله -->
        <div
          class="flex-1 min-w-0 rounded-xl px-3 py-2 transition-colors"
          :class="step.key === currentKey
            ? 'bg-primary-50/70 dark:bg-primary-900/15 border border-primary-200 dark:border-primary-800'
            : 'border border-transparent'"
        >
          <div class="flex items-start justify-between gap-2">
            <div class="min-w-0">
              <p class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-1.5 flex-wrap">
                {{ step.title }}
                <span
                  v-if="step.optional"
                  class="text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                >اختیاری</span>
              </p>
              <p
                class="text-xs mt-0.5 leading-5"
                :class="step.status === 'done'
                  ? 'text-emerald-600 dark:text-emerald-400'
                  : 'text-gray-500 dark:text-gray-400'"
              >{{ step.hint }}</p>
            </div>

            <!-- لینک کوچک برای مراحلی که مرحله‌ی جاری نیستند -->
            <button
              v-if="step.key !== currentKey"
              type="button"
              @click="emit('go', step.key)"
              class="flex-shrink-0 text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline mt-0.5"
            >
              {{ step.status === 'done' ? 'ویرایش' : 'رفتن' }}
            </button>
          </div>

          <!-- دکمه‌های مرحله‌ی جاری -->
          <div v-if="step.key === currentKey" class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2">
            <button
              type="button"
              @click="emit('go', step.key)"
              class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors"
            >
              {{ step.actionLabel }}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              v-if="step.optional"
              type="button"
              @click="emit('skip', step.key)"
              class="text-xs font-medium text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:underline"
            >
              فعلاً رد کن
            </button>
          </div>
        </div>
      </li>
    </ol>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

export interface HomeStepItem {
  key: string;
  title: string;
  hint: string;
  actionLabel: string;
  status: 'done' | 'skipped' | 'pending';
  optional?: boolean;
}

const props = defineProps<{
  steps: HomeStepItem[];
  currentKey: string | null;
}>();

const emit = defineEmits<{
  (e: 'go', key: string): void;
  (e: 'skip', key: string): void;
}>();

const completedCount = computed(() => props.steps.filter(s => s.status === 'done').length);

const progressPercent = computed(() =>
  props.steps.length ? Math.round((completedCount.value / props.steps.length) * 100) : 0
);

const circleClass = (step: HomeStepItem) => {
  if (step.status === 'done') return 'bg-emerald-500 text-white';
  if (step.key === props.currentKey) return 'bg-primary-600 text-white ring-4 ring-primary-100 dark:ring-primary-900/40';
  if (step.status === 'skipped') return 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-300';
  return 'bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-600 text-gray-400 dark:text-gray-500';
};
</script>
