<!-- frontend/src/components/features/home/HomeEmptyState.vue -->
<template>
  <div class="card text-center py-12 sm:py-16" :class="containerClass">
    
    <!-- ===== Loading ===== -->
    <div v-if="type === 'loading'" class="flex flex-col items-center justify-center">
      <div class="relative">
        <div class="animate-spin rounded-full h-14 w-14 sm:h-16 sm:w-16 border-4 border-primary-200 dark:border-primary-900"></div>
        <div class="animate-spin rounded-full h-14 w-14 sm:h-16 sm:w-16 border-4 border-primary-600 border-t-transparent absolute top-0"></div>
      </div>
      <p class="mt-4 text-gray-600 dark:text-gray-400 text-sm">در حال بارگذاری داده‌ها...</p>
    </div>

    <!-- ===== Error ===== -->
    <div v-else-if="type === 'error'" class="flex flex-col items-center">
      <div class="w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-4 rounded-full bg-danger-100 dark:bg-danger-900/30 flex items-center justify-center">
        <svg class="w-10 h-10 sm:w-12 sm:h-12 text-danger-600 dark:text-danger-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <h4 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2">خطا در دریافت داده‌ها</h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">{{ message || 'خطای ناشناخته رخ داده است.' }}</p>
      <button
        @click="$emit('retry')"
        class="mt-4 px-5 py-2 bg-danger-600 hover:bg-danger-700 text-white text-sm rounded-lg transition-colors shadow-sm hover:shadow-md"
      >
        تلاش مجدد
      </button>
    </div>

    <!-- ============================================================ -->
    <!-- ===== No Report ===== -->
    <!-- ============================================================ -->
    <div v-else-if="type === 'no-report'" class="flex flex-col items-center">
      <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center">
        <svg class="w-12 h-12 text-primary-500 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">
        هیچ گزارشی وجود ندارد
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto leading-relaxed">
        برای شروع، یک گزارش جدید ایجاد کنید یا یک گزارش موجود را باز کنید.
      </p>
      
      <!-- مراحل -->
      <div class="mt-6 flex flex-wrap items-center justify-center gap-2 text-sm">
        
        <!-- مرحله ۱ -->
        <div class="flex items-center gap-2 px-4 py-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
          <span class="w-6 h-6 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center font-bold">۱</span>
          <span>فایل → جدید</span>
          <svg class="w-4 h-4 text-gray-400 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
        
        <!-- مرحله ۲ -->
        <div class="flex items-center gap-2 px-4 py-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
          <span class="w-6 h-6 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center font-bold">۲</span>
          <span>اطلاعات گزارش (نام گزارش، مرحله رشد)</span>
          <svg class="w-4 h-4 text-gray-400 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
        
        <!-- مرحله ۳ -->
        <div class="flex items-center gap-2 px-4 py-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
          <span class="w-6 h-6 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center font-bold">۳</span>
          <span>فایل → ذخیره</span>
          <svg class="w-4 h-4 text-gray-400 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
        
      </div>
      
      <div class="mt-4 flex flex-wrap justify-center gap-2">
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs font-medium flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          پس از ذخیره، صفحه خانه فعال می‌شود
        </span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- ===== No Data ===== -->
    <!-- ============================================================ -->
    <div v-else-if="type === 'no-data'" class="flex flex-col items-center">
      <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center">
        <svg class="w-12 h-12 text-primary-500 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">
        هنوز داده‌ای برای نمایش وجود ندارد
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto leading-relaxed">
        برای مشاهده داشبورد، مراحل زیر را به ترتیب انجام دهید:
      </p>
      
      <!-- مراحل -->
      <div class="mt-5 w-full max-w-lg space-y-2 text-right">
        <div class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer" @click="$emit('navigate', 'water-analysis')">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-bold">۱</span>
          <span class="text-sm text-gray-700 dark:text-gray-300">آنالیز آب</span>
          <span class="text-xs text-gray-400 mr-auto">وارد کردن درصد آب، EC، pH و عناصر</span>
        </div>
        
        <div class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer" @click="$emit('navigate', 'target-elements')">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500 text-white text-xs flex items-center justify-center font-bold">۲</span>
          <span class="text-sm text-gray-700 dark:text-gray-300">عناصر هدف</span>
          <span class="text-xs text-gray-400 mr-auto">تعیین مقدار PPM مورد نظر برای هر عنصر</span>
        </div>
        
        <div class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer" @click="$emit('navigate', 'fertilizer-db')">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 text-white text-xs flex items-center justify-center font-bold">۳</span>
          <span class="text-sm text-gray-700 dark:text-gray-300">پایگاه داده کودها</span>
          <span class="text-xs text-gray-400 mr-auto">تعریف کودهای موجود یا کپی از کودهای سیستمی</span>
        </div>
        
        <div class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer" @click="$emit('navigate', 'fertilizer-calc')">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-amber-500 text-white text-xs flex items-center justify-center font-bold">۴</span>
          <span class="text-sm text-gray-700 dark:text-gray-300">محاسبه خودکار کود</span>
          <span class="text-xs text-gray-400 mr-auto">انتخاب کودها و کلیک روی بهینه‌سازی خودکار</span>
        </div>
      </div>
      
      <!-- راهنما -->
      <div class="mt-5 px-4 py-2.5 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-200 dark:border-primary-800 text-xs text-primary-700 dark:text-primary-300 flex items-center justify-center gap-2">
        <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span>پس از تکمیل مراحل، صفحه خانه به‌روزرسانی می‌شود</span>
        <span class="text-primary-400">|</span>
        <router-link to="/" class="font-medium hover:underline flex items-center gap-1">
          <span>آموزش بیشتر</span>
          <svg class="w-3.5 h-3.5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ============================================================
// Props
// ============================================================
interface Props {
  type: 'loading' | 'error' | 'no-report' | 'no-data';
  message?: string;
}

const props = defineProps<Props>();

// ============================================================
// Emits
// ============================================================
defineEmits<{
  (e: 'retry'): void;
  (e: 'navigate', tab: string): void;
}>();

// ============================================================
// Computed
// ============================================================
const containerClass = computed(() => {
  if (props.type === 'error') {
    return 'border-r-4 border-r-danger-500';
  }
  return '';
});
</script>