<!-- frontend/src/components/features/calc/ResultAccordion.vue -->
<!--
  بخش تاشو (آکاردئون) برای نمایش نتیجه.
  هدف: جلوگیری از شلوغی صفحه؛ هر بخش فقط در صورت نیاز باز می‌شود.
-->
<template>
  <section class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden">
    <button
      type="button"
      @click="isOpen = !isOpen"
      class="w-full flex items-center justify-between gap-3 px-4 py-3 text-right hover:bg-gray-50 dark:hover:bg-gray-700/40 transition-colors"
      :aria-expanded="isOpen"
    >
      <span class="flex items-center gap-2 min-w-0">
        <span
          class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
          :class="toneClasses.icon"
        >
          <slot name="icon">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </slot>
        </span>
        <span class="min-w-0">
          <span class="block text-sm font-semibold text-gray-900 dark:text-white truncate">{{ title }}</span>
          <span v-if="subtitle" class="block text-xs text-gray-500 dark:text-gray-400 truncate">{{ subtitle }}</span>
        </span>
      </span>

      <span class="flex items-center gap-2 flex-shrink-0">
        <span
          v-if="badge"
          class="text-[11px] px-2 py-0.5 rounded-full font-medium"
          :class="toneClasses.badge"
        >{{ badge }}</span>
        <svg
          class="w-4 h-4 text-gray-400 transition-transform duration-200"
          :class="isOpen ? 'rotate-180' : ''"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </span>
    </button>

    <Transition name="accordion">
      <div v-show="isOpen" class="px-4 pb-4 pt-1 border-t border-gray-100 dark:border-gray-700/60">
        <slot />
      </div>
    </Transition>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = withDefaults(
  defineProps<{
    title: string;
    subtitle?: string;
    badge?: string;
    tone?: 'neutral' | 'primary' | 'success' | 'warning' | 'danger';
    defaultOpen?: boolean;
  }>(),
  {
    tone: 'neutral',
    defaultOpen: false
  }
);

const isOpen = ref(props.defaultOpen);

const toneClasses = computed(() => {
  const map: Record<string, { icon: string; badge: string }> = {
    neutral: {
      icon: 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300',
      badge: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
    },
    primary: {
      icon: 'bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400',
      badge: 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400'
    },
    success: {
      icon: 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
      badge: 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
    },
    warning: {
      icon: 'bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
      badge: 'bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
    },
    danger: {
      icon: 'bg-rose-50 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400',
      badge: 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-400'
    }
  };
  return map[props.tone] || map.neutral;
});
</script>

<style scoped>
.accordion-enter-active,
.accordion-leave-active {
  transition: opacity 0.18s ease;
}
.accordion-enter-from,
.accordion-leave-to {
  opacity: 0;
}
</style>
