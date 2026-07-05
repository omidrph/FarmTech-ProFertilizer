<!-- frontend/src/components/features/home/HomeRecommendations.vue -->
<template>
  <div v-if="recommendations.length > 0" class="card border-l-4 border-l-primary-500">
    <div class="flex items-center gap-3 mb-4">
      <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
      </div>
      <div>
        <h3 class="text-base font-bold text-gray-900 dark:text-white">
          توصیه‌های هوشمند
        </h3>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          بر اساس تحلیل داده‌های فعلی
        </p>
      </div>
      <span class="mr-auto px-2.5 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full text-xs font-medium">
        {{ recommendations.length }} مورد
      </span>
    </div>

    <div class="space-y-2.5">
      <div
        v-for="(rec, idx) in recommendations"
        :key="idx"
        class="flex items-start gap-3 p-3.5 rounded-lg transition-all hover:shadow-sm"
        :class="getRecommendationBgClass(rec.type)"
      >
        <div class="flex-shrink-0 mt-0.5">
          <div class="w-7 h-7 rounded-full flex items-center justify-center" :class="getRecommendationIconBgClass(rec.type)">
            <svg class="w-4 h-4" :class="getRecommendationIconClass(rec.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="rec.type === 'warning'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              <path v-else-if="rec.type === 'danger'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold" :class="getRecommendationTextClass(rec.type)">
            {{ rec.title }}
          </p>
          <p class="text-xs mt-0.5 leading-relaxed" :class="getRecommendationDescClass(rec.type)">
            {{ rec.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ============================================================
// Types
// ============================================================
interface Recommendation {
  type: 'success' | 'warning' | 'danger';
  title: string;
  description: string;
}

// ============================================================
// Props
// ============================================================
interface Props {
  recommendations: Recommendation[];
}

defineProps<Props>();

// ============================================================
// Helper Functions
// ============================================================
const getRecommendationBgClass = (type: string): string => {
  if (type === 'danger') return 'bg-danger-50 dark:bg-danger-900/20';
  if (type === 'warning') return 'bg-warning-50 dark:bg-warning-900/20';
  return 'bg-success-50 dark:bg-success-900/20';
};

const getRecommendationIconBgClass = (type: string): string => {
  if (type === 'danger') return 'bg-danger-100 dark:bg-danger-900/50';
  if (type === 'warning') return 'bg-warning-100 dark:bg-warning-900/50';
  return 'bg-success-100 dark:bg-success-900/50';
};

const getRecommendationIconClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-600 dark:text-danger-400';
  if (type === 'warning') return 'text-warning-600 dark:text-warning-400';
  return 'text-success-600 dark:text-success-400';
};

const getRecommendationTextClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-700 dark:text-danger-400';
  if (type === 'warning') return 'text-warning-700 dark:text-warning-400';
  return 'text-success-700 dark:text-success-400';
};

const getRecommendationDescClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-600 dark:text-danger-500';
  if (type === 'warning') return 'text-warning-600 dark:text-warning-500';
  return 'text-success-600 dark:text-success-500';
};
</script>