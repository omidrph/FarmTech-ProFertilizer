<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">

    <!-- ============================================================ -->
    <!-- بخش درباره سامانه فارم‌تک -->
    <!-- ============================================================ -->
    <div class="mb-10">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-3">
        <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        درباره سامانه فارم‌تک
      </h2>

      <div class="space-y-4 text-gray-600 dark:text-gray-300 leading-relaxed text-justify">
        <p>
          سامانه هوشمند نسخه‌نویسی کود فارم‌تک، راهکاری جامع و تخصصی برای مدیریت دقیق تغذیه گیاه در گلخانه‌هاست. 
          این نرم‌افزار با بهره‌گیری از الگوریتم‌های علمی معتبر و پایگاه داده‌ای از بیش از ۴۲ کود ایرانی، 
          امکان محاسبه دقیق فرمول غذایی، تحلیل آب و پساب، و تعادل یونی را فراهم می‌کند.
        </p>
        <p>
          فارم‌تک با هدف افزایش بهره‌وری و کاهش هزینه‌های تولید، ابزاری هوشمند در اختیار گلخانه‌داران، 
          مشاوران و کارشناسان کشاورزی قرار می‌دهد تا بتوانند بهترین تصمیم‌های تغذیه‌ای را برای محصول خود اتخاذ کنند. 
          این نرم‌افزار با ساده‌سازی دانش پیچیده تغذیه گیاه، امکان مدیریت حرفه‌ای تغذیه را در هر زمان و مکان فراهم می‌کند.
        </p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش قابلیت‌های کلیدی -->
    <!-- ============================================================ -->
    <div class="mb-12">
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
        <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        قابلیت‌های کلیدی
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- 1. محاسبه فرمول غذایی -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">محاسبه دقیق فرمول غذایی</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">با الگوریتم علمی، مقدار دقیق هر کود را برای ۱۵ عنصر هدف محاسبه کنید</p>
            </div>
          </div>
        </div>

        <!-- 2. آنالیز آب و پساب -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">آنالیز جامع آب و پساب</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">بررسی EC، عناصر و تبدیل واحد بین PPM، MEQ و MMOL</p>
            </div>
          </div>
        </div>

        <!-- 3. مدیریت مخازن -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">مدیریت هوشمند مخازن A,B,C</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">تقسیم خودکار کودها بر اساس سازگاری شیمیایی برای جلوگیری از رسوب</p>
            </div>
          </div>
        </div>

        <!-- 4. پایش تعادل یونی -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">پایش تعادل یونی</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">محاسبه کاتیون و آنیون با تلرانس ۰.۵ meq/L و هشدار فوری</p>
            </div>
          </div>
        </div>

        <!-- 5. پایگاه داده کودها -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4zm0 5c0 2.21 3.582 4 8 4s8-1.79 8-4"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">پایگاه داده ۴۲+ کود ایرانی</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">از برندهای اطلس، رازاک شیمی، ردسا و گل سم گرگان</p>
            </div>
          </div>
        </div>

        <!-- 6. تفسیر هوشمند و گزارش‌گیری -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">تفسیر هوشمند و گزارش‌گیری</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">گزارش‌های جامع با قابلیت چاپ برای ارائه به بهره‌بردار</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش تیم توسعه -->
    <!-- ============================================================ -->
    <div class="border-t border-gray-200 dark:border-gray-700 pt-6 mt-6">
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
        </svg>
        تیم توسعه
      </h3>

      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl">
        <!-- آواتار -->
        <div class="flex-shrink-0">
          <div class="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400 text-2xl font-bold">
            O
          </div>
        </div>

        <!-- اطلاعات -->
        <div class="flex-1">
          <h4 class="text-lg font-bold text-gray-900 dark:text-white">امید رحمانی</h4>
          <p class="text-sm text-gray-500 dark:text-gray-400">توسعه‌دهنده ارشد و طراح سیستم</p>
          <div class="flex flex-wrap items-center gap-3 mt-2 text-sm">
            <a href="mailto:omidrpe@gmail.com" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              omidrpe@gmail.com
            </a>
            <span class="text-gray-300 dark:text-gray-600">|</span>
            <a href="https://github.com/omidrph" target="_blank" class="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 transition-colors flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.15 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.62.24 2.85.12 3.15.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
              </svg>
              github.com/omidrph
            </a>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
// این صفحه درباره ما است و نیازی به state خاصی ندارد
</script>

<style scoped>
/* استایل‌های مورد نیاز */
</style>