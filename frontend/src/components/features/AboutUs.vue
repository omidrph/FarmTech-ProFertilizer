<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
    <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-6 flex items-center gap-2">
      <svg class="w-6 h-6 sm:w-8 sm:h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      درباره ما
    </h2>
    
    <div class="space-y-6">
      <!-- معرفی -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">🌱 درباره FarmTech</h3>
        <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
          <strong>FarmTech - ProFertilizer</strong> یک نرم‌افزار تخصصی برای محاسبه، تحلیل و مدیریت فرمول‌های تغذیه گیاهان در سیستم‌های کشت بدون خاک، هیدروپونیک و گلخانه‌ای است.
        </p>
        <p class="text-gray-700 dark:text-gray-300 leading-relaxed mt-2">
          این نرم‌افزار با بهره‌گیری از الگوریتم‌های پیشرفته و دانش روز تغذیه گیاهان، به کشاورزان و متخصصان گلخانه‌ای کمک می‌کند تا فرمول‌های غذایی دقیق و متعادلی برای گیاهان خود طراحی کنند.
        </p>
      </div>

      <!-- ماموریت و چشم‌انداز -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <span class="text-lg">🎯</span>
            ماموریت
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            توانمندسازی کشاورزان و متخصصان گلخانه‌ای با ابزارهای هوشمند برای افزایش بهره‌وری و کیفیت محصولات کشاورزی.
          </p>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            <span class="text-lg">👁️</span>
            چشم‌انداز
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            تبدیل شدن به مرجع اصلی نرم‌افزارهای تخصصی تغذیه گیاهان در خاورمیانه و ارائه راهکارهای نوین در کشاورزی دقیق.
          </p>
        </div>
      </div>

      <!-- قابلیت‌ها -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">✨ قابلیت‌های کلیدی</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">🔐</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">احراز هویت امن</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">سیستم ورود با توکن تصادفی</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">💧</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">آنالیز آب و پساب</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">محاسبه مقادیر تامینی</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">🎯</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">عناصر هدف</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">تعیین مقادیر مورد نیاز</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">🧮</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">محاسبه خودکار کود</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">دقیق و سریع با فرمول‌های علمی</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">📚</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">پایگاه داده کودها</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">مدیریت کامل کودها و اسیدها</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">📊</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">تفسیر هوشمند</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">گزارش‌های جامع و توصیه‌های کودی</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">🌓</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">تم روشن/تاریک</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">راحتی در هر شرایط نوری</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">🖨️</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">چاپ گزارش</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">خروجی حرفه‌ای برای ارائه</p>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-start gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <span class="text-primary-600 text-lg">📱</span>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 text-sm">واکنش‌گرا</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">سازگار با همه دستگاه‌ها</p>
            </div>
          </div>
        </div>
      </div>

      <!-- تکنولوژی‌ها -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">🛠️ تکنولوژی‌های استفاده شده</h3>
        <div class="flex flex-wrap gap-2">
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">FastAPI</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Vue 3</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">TypeScript</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Tailwind CSS</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">SQLite</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Pinia</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Vite</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">SQLAlchemy</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Pydantic</span>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm border border-gray-200 dark:border-gray-600">Axios</span>
        </div>
      </div>

      <!-- تیم -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">👨‍💻 تیم توسعه</h3>
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center text-xl font-bold">
              OR
            </div>
            <div>
              <p class="font-semibold text-gray-900 dark:text-white text-lg">امید رحمانی</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">توسعه‌دهنده ارشد و طراح سیستم</p>
              <div class="flex items-center gap-3 mt-1">
                <a href="mailto:info@farmtech.ir" class="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
                  info@farmtech.ir
                </a>
                <span class="text-gray-300 dark:text-gray-600">|</span>
                <a href="https://github.com/omidrph" target="_blank" class="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
                  github.com/omidrph
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- اطلاعات نسخه -->
      <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9"/>
          </svg>
          <span>نسخه: {{ appVersion }}</span>
        </div>
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <span>آخرین به‌روزرسانی: {{ lastUpdate }}</span>
        </div>
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          <span>مجوز: اختصاصی (FarmTech)</span>
        </div>
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
          </svg>
          <span>ساخته شده با ❤️ توسط تیم FarmTech</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// ===== Constants =====
const appVersion = ref('0.1.0');
const lastUpdate = ref('۱۴۰۵/۰۴/۰۳');
</script>