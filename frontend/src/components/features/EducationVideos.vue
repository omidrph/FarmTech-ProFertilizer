<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- ============================================================ -->
    <!-- هدر معرفی -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">فیلم‌های آموزشی</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">آموزش‌های تصویری استفاده از سامانه سهند کود</p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- حالت «به‌زودی» -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 sm:p-12 text-center">
      <!-- آیکون -->
      <div class="relative inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-primary-50 dark:bg-primary-900/20 mb-6">
        <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-xl animate-pulse"></div>
        <svg class="relative w-10 h-10 sm:w-12 sm:h-12 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
        </svg>
      </div>

      <h4 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2">به‌زودی در دسترس</h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-lg mx-auto leading-relaxed mb-4">
        تیم سهند کود در حال آماده‌سازی مجموعه‌ای از فیلم‌های آموزشی گام‌به‌گام برای استفاده هرچه راحت‌تر از سامانه است.
        این آموزش‌ها شامل موارد زیر خواهند بود:
      </p>

      <!-- لیست موضوعات آینده -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-2xl mx-auto mt-6 text-right">
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">معرفی کلی سامانه و رابط کاربری</span>
        </div>
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">مدیریت کودها و پایگاه داده</span>
        </div>
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">بهینه‌سازی خودکار فرمول کودی</span>
        </div>
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">استفاده از ابزارک محاسبه pH</span>
        </div>
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">چاپ و خروجی PDF گزارش‌ها</span>
        </div>
        <div class="flex items-center gap-2 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/30 border border-gray-100 dark:border-gray-700">
          <span class="w-6 h-6 rounded-md bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </span>
          <span class="text-xs text-gray-600 dark:text-gray-300">نکات تخصصی و پاسخ به سوالات</span>
        </div>
      </div>

      <!-- دکمه اطلاع‌رسانی -->
      <div class="mt-8 inline-flex items-center gap-2 px-4 py-2 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 rounded-lg text-sm font-medium">
        <svg class="w-4 h-4 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        در حال آماده‌سازی...
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام جایگزین -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800 p-4 sm:p-5 text-center">
      <p class="text-sm text-gray-700 dark:text-gray-300">
        تا زمان آماده شدن فیلم‌ها، می‌توانید از بخش
        <router-link to="/" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium mx-1">شروع سریع</router-link>
        و
        <router-link to="/" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium mx-1">سوالات متداول</router-link>
        استفاده کنید.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
// این کامپوننت در حال حاضر صرفاً یک placeholder حرفه‌ای است
</script>