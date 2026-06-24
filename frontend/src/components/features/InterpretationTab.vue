<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات (بدون آیکون - هم‌سبک با بقیه تب‌ها) -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        با کلیک روی دکمه "تولید تفسیر"، گزارش کاملی از وضعیت تغذیه گیاه و توصیه‌های کودی دریافت کنید.
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- دکمه‌های اقدام -->
    <!-- ============================================================ -->
    <div class="flex flex-wrap gap-3">
      <button
        @click="generateInterpretation"
        class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        تولید تفسیر
      </button>
      <button
        @click="printReport"
        class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
        </svg>
        چاپ گزارش
      </button>
    </div>

    <!-- ============================================================ -->
    <!-- نتیجه تفسیر -->
    <!-- ============================================================ -->
    <div v-if="interpretationResult" class="space-y-4">
      <!-- خلاصه گزارش -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2 bg-primary-50 dark:bg-primary-900/20">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">خلاصه گزارش</h3>
        </div>
        <div class="p-4">
          <pre class="whitespace-pre-wrap font-sans text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-600 leading-relaxed">{{ interpretationResult.summary }}</pre>
        </div>
      </div>

      <!-- کارت‌های اطلاعات -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- تعادل یونی -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
              <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h4 class="font-semibold text-gray-900 dark:text-white">تعادل یونی</h4>
          </div>
          <div class="p-4 space-y-3">
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ interpretationResult.ionBalance.message }}</p>
            <div class="flex gap-4 text-sm">
              <span class="text-gray-600 dark:text-gray-400">کاتیون: <strong class="text-gray-900 dark:text-white tabular-nums">{{ interpretationResult.ionBalance.cation.toFixed(2) }}</strong></span>
              <span class="text-gray-600 dark:text-gray-400">آنیون: <strong class="text-gray-900 dark:text-white tabular-nums">{{ interpretationResult.ionBalance.anion.toFixed(2) }}</strong></span>
            </div>
            <div
              class="flex items-center gap-2 p-2 rounded-lg"
              :class="interpretationResult.ionBalance.isBalanced
                ? 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400'
                : 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400'"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="interpretationResult.ionBalance.isBalanced" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span class="text-sm font-medium">
                {{ interpretationResult.ionBalance.isBalanced ? 'تعادل برقرار است' : 'تعادل برقرار نیست' }}
              </span>
            </div>
          </div>
        </div>

        <!-- کیفیت آب -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
              <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              </svg>
            </div>
            <h4 class="font-semibold text-gray-900 dark:text-white">کیفیت آب</h4>
          </div>
          <div class="p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600 dark:text-gray-400">شوری:</span>
              <span class="text-sm font-semibold text-gray-900 dark:text-white tabular-nums">
                {{ interpretationResult.waterQuality.salinity }} dS/m
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600 dark:text-gray-400">وضعیت:</span>
              <span
                class="px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="{
                  'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400': interpretationResult.waterQuality.impact === 'مناسب',
                  'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400': interpretationResult.waterQuality.impact === 'متوسط',
                  'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400': interpretationResult.waterQuality.impact === 'بالا'
                }"
              >
                {{ interpretationResult.waterQuality.impact }}
              </span>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
              <div class="flex items-start gap-2">
                <svg class="w-4 h-4 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-sm text-primary-700 dark:text-primary-300">
                  {{ interpretationResult.waterQuality.recommendation }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- وضعیت عناصر -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white">وضعیت عناصر</h4>
        </div>
        <div class="p-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            <div
              v-for="item in interpretationResult.elementStatus"
              :key="item.element"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
            >
              <span class="font-medium text-sm text-gray-700 dark:text-gray-300">{{ item.element }}</span>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-500 dark:text-gray-400 tabular-nums">{{ item.target.toFixed(2) }}</span>
                <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                </svg>
                <span class="text-xs text-gray-500 dark:text-gray-400 tabular-nums">{{ item.actual.toFixed(2) }}</span>
                <span
                  :class="{
                    'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400': item.status === 'sufficient',
                    'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400': item.status === 'deficient' || item.status === 'excessive',
                    'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400': item.status === 'toxic'
                  }"
                  class="px-2 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ item.message }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- توصیه‌های کودی -->
      <div v-if="interpretationResult.fertilizerRecommendation.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white">توصیه‌های کودی</h4>
          <span class="mr-auto px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full text-xs font-medium">
            {{ interpretationResult.fertilizerRecommendation.length }} مورد
          </span>
        </div>
        <div class="p-4 space-y-2">
          <div
            v-for="rec in interpretationResult.fertilizerRecommendation"
            :key="rec.issue"
            class="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
          >
            <span
              :class="{
                'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400': rec.priority === 'high',
                'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400': rec.priority === 'medium',
                'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400': rec.priority === 'low'
              }"
              class="flex-shrink-0 px-2 py-0.5 rounded-full text-xs font-bold"
            >
              {{ rec.priority === 'high' ? 'فوری' : rec.priority === 'medium' ? 'مهم' : 'عادی' }}
            </span>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ rec.issue }}</p>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1 flex items-start gap-1.5">
                <svg class="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
                {{ rec.suggestion }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- حالت خالی -->
    <!-- ============================================================ -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
        <svg class="w-10 h-10 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        هنوز تفسیری تولید نشده است
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        برای مشاهده تفسیر، ابتدا داده‌های آنالیز آب، عناصر هدف و محاسبات کود را وارد کنید، سپس روی دکمه "تولید تفسیر" کلیک کنید.
      </p>
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

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>