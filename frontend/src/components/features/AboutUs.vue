<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">

    <!-- ============================================================ -->
    <!-- بخش درباره سامانه سهند کود -->
    <!-- ============================================================ -->
    <div class="mb-10">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <svg class="w-6 h-6 sm:w-8 sm:h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        درباره سهند کود
      </h2>

      <div class="space-y-4 text-gray-600 dark:text-gray-300 leading-relaxed text-justify text-sm sm:text-base">
        <p>
          سامانه هوشمند <strong class="text-gray-800 dark:text-gray-100">سهند کود</strong> یک پلتفرم جامع و پیشرفته برای مدیریت دقیق و علمی تغذیه گیاه در گلخانه‌ها و کشت‌های بدون خاک است. این نرم‌افزار با هدف ساده‌سازی پیچیدگی‌های محاسبات شیمیایی، به کشاورزان، گلخانه‌داران و کارشناسان کمک می‌کند تا با اطمینان کامل، بهترین فرمول کودی را برای محصول خود تهیه کنند.
        </p>
        <p>
          موتور محاسباتی سهند کود بر پایه <strong class="text-gray-800 dark:text-gray-100">الگوریتم بهینه‌سازی NNLS (کمترین مربعات نامنفی)</strong> بنا شده است که تضمین می‌کند هیچ‌گاه وزن منفی برای یک کود محاسبه نشود و همواره واقع‌بینانه‌ترین ترکیب ممکن را ارائه دهد. این سیستم نه‌تنها مقادیر کود را محاسبه می‌کند، بلکه تعادل یونی محلول، خطر رسوب‌های شیمیایی، و سازگاری کودها در مخازن مختلف را نیز به‌طور کامل بررسی می‌کند.
        </p>
        <p>
          ما در سهند کود، تجربه‌ای حرفه‌ای را با استفاده از جدیدترین تکنولوژی‌های وب و پایگاهی از <strong class="text-gray-800 dark:text-gray-100">کودهای ایرانی</strong> به همراه <strong class="text-gray-800 dark:text-gray-100">رسپی‌های آماده و تأییدشده</strong> برای محصولات پرمصرف، در اختیار شما قرار می‌دهیم. هدف ما، ارتقای بهره‌وری و کاهش هزینه‌های تولید، از طریق دقت علمی و اتوماسیون فرآیندها است.
        </p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش قابلیت‌های کلیدی -->
    <!-- ============================================================ -->
    <div class="mb-10">
      <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        قابلیت‌های کلیدی
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- 1. محاسبه و بهینه‌سازی هوشمند -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">محاسبه و بهینه‌سازی هوشمند</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                یافتن بهترین ترکیب از میان ده‌ها کود با الگوریتم NNLS برای رسیدن دقیق به عناصر هدف، با در نظر گرفتن قیمت و خلوص.
              </p>
            </div>
          </div>
        </div>

        <!-- 2. تحلیل جامع آب و محلول -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">تحلیل جامع آب و محلول</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                محاسبه دقیق EC بر اساس استاندارد، تخمین pH، بررسی خطر رسوب و محاسبه سهم هر عنصر از آب و کود.
              </p>
            </div>
          </div>
        </div>

        <!-- 3. مدیریت پیشرفته مخازن A, B, C -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">مدیریت پیشرفته مخازن A, B, C</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                توزیع خودکار و هوشمند کودها در مخازن بر اساس سازگاری شیمیایی برای جلوگیری از رسوب و افزایش کارایی.
              </p>
            </div>
          </div>
        </div>

        <!-- 4. پایگاه داده و رسپی‌های آماده -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">پایگاه داده و رسپی‌های آماده</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                دسترسی به کودهای استاندارد ایرانی و رسپی‌های آماده برای محصولات مختلف، همگی تأییدشده و متعادل.
              </p>
            </div>
          </div>
        </div>

        <!-- 5. تعادل یونی و ابزار pH -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">تعادل یونی و ابزار pH</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                تضمین تعادل بار و جلوگیری از مشکلات جذب، به همراه ابزارک تخصصی محاسبه دقیق دوز اسید/باز برای تنظیم pH.
              </p>
            </div>
          </div>
        </div>

        <!-- 6. طراحی مدرن و خروجی حرفه‌ای -->
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-5 border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">طراحی مدرن و خروجی حرفه‌ای</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
                رابط کاربری واکنش‌گرا و آسان برای موبایل و دسکتاپ، به همراه قابلیت چاپ گزارش‌های کامل و حرفه‌ای.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش تیم توسعه -->
    <!-- ============================================================ -->
    <div class="border-t border-gray-200 dark:border-gray-700 pt-6 mt-6">
      <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
        </svg>
        تیم توسعه
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- امید رحمانی -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl border border-gray-100 dark:border-gray-700">
          <div class="flex-shrink-0">
            <div class="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400 text-2xl font-bold">
              O
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-bold text-gray-900 dark:text-white">امید رحمانی</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">توسعه‌دهنده ارشد و طراح سیستم</p>
            <a href="mailto:omidrpe@gmail.com" class="mt-2 inline-flex items-center gap-1.5 text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <span class="truncate">omidrpe@gmail.com</span>
            </a>
          </div>
        </div>

        <!-- محسن نوذری -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl border border-gray-100 dark:border-gray-700">
          <div class="flex-shrink-0">
            <div class="w-16 h-16 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400 text-2xl font-bold">
              M
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-bold text-gray-900 dark:text-white">محسن نوذری</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">توسعه‌دهنده</p>
            <a href="mailto:mohsennozari13822003@gmail.com" class="mt-2 inline-flex items-center gap-1.5 text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <span class="truncate">mohsennozari13822003@gmail.com</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- فوتر -->
    <!-- ============================================================ -->
    <div class="border-t border-gray-200 dark:border-gray-700 pt-4 mt-6">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-500 dark:text-gray-400">
        <div class="flex items-center gap-2">
          <span class="inline-block px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded text-[10px] font-medium">
            محصول دانش‌بنیان
          </span>
        </div>
        <p class="text-center">
          © ۱۴۰۱ – ۱۴۰۵ محصولی دانش‌بنیان از شرکت توسعه فناوری ستاره سهیل، تمامی حقوق محفوظ است.
        </p>
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