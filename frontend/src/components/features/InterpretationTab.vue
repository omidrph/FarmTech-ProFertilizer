<template>
  <div class="space-y-6">
    <!-- Actions -->
    <div class="flex flex-wrap gap-3">
      <button @click="generateInterpretation" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        🚀 تولید تفسیر
      </button>
      <button @click="printReport" class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors">
        🖨️ چاپ گزارش
      </button>
    </div>

    <!-- Result -->
    <div v-if="interpretationResult" class="space-y-4">
      <!-- Summary -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">خلاصه گزارش</h3>
        <pre class="whitespace-pre-wrap font-sans text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-600">{{ interpretationResult.summary }}</pre>
      </div>

      <!-- Details Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Ion Balance -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">تعادل یونی</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">{{ interpretationResult.ionBalance.message }}</p>
          <div class="flex gap-4 text-sm">
            <span class="text-gray-600 dark:text-gray-400">کاتیون: <strong class="text-gray-900 dark:text-white">{{ interpretationResult.ionBalance.cation.toFixed(2) }}</strong></span>
            <span class="text-gray-600 dark:text-gray-400">آنیون: <strong class="text-gray-900 dark:text-white">{{ interpretationResult.ionBalance.anion.toFixed(2) }}</strong></span>
          </div>
        </div>

        <!-- Water Quality -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">کیفیت آب</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400">شوری: {{ interpretationResult.waterQuality.salinity }}</p>
          <p class="text-sm text-gray-600 dark:text-gray-400">وضعیت: {{ interpretationResult.waterQuality.impact }}</p>
          <p class="text-sm text-primary-600 dark:text-primary-400 mt-1">{{ interpretationResult.waterQuality.recommendation }}</p>
        </div>
      </div>

      <!-- Element Status -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
        <h4 class="font-semibold text-gray-900 dark:text-white mb-3">وضعیت عناصر</h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
          <div v-for="item in interpretationResult.elementStatus" :key="item.element" class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <span class="font-medium text-sm text-gray-700 dark:text-gray-300">{{ item.element }}</span>
            <div class="flex items-center gap-2">
              <span class="text-xs text-gray-500 dark:text-gray-400">{{ item.target.toFixed(2) }}</span>
              <span class="text-xs text-gray-400 dark:text-gray-500">→</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">{{ item.actual.toFixed(2) }}</span>
              <span :class="{
                'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400': item.status === 'sufficient',
                'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400': item.status === 'deficient' || item.status === 'excessive',
                'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400': item.status === 'toxic'
              }" class="px-2 py-0.5 rounded-full text-xs">
                {{ item.message }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div v-if="interpretationResult.fertilizerRecommendation.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
        <h4 class="font-semibold text-gray-900 dark:text-white mb-3">توصیه‌های کودی</h4>
        <div v-for="rec in interpretationResult.fertilizerRecommendation" :key="rec.issue" class="flex flex-wrap items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg mb-2">
          <span :class="{
            'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400': rec.priority === 'high',
            'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400': rec.priority === 'medium',
            'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400': rec.priority === 'low'
          }" class="px-2 py-0.5 rounded-full text-xs font-bold uppercase">
            {{ rec.priority }}
          </span>
          <span class="text-sm text-gray-700 dark:text-gray-300">{{ rec.issue }}</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">→ {{ rec.suggestion }}</span>
        </div>
      </div>
    </div>

    <!-- Placeholder -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <svg class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <p class="text-gray-500 dark:text-gray-400">برای مشاهده تفسیر، دکمه "تولید تفسیر" را کلیک کنید.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Props =====
interface Props {
  interpretationResult: any;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:interpretationResult', value: any): void;
  (e: 'generate'): void;
}>();

// ===== Methods =====
const generateInterpretation = () => {
  emit('generate');
};

const printReport = () => {
  window.print();
};
</script>