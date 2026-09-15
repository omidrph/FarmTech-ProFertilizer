<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- 🆕 حالت «به‌زودی»: بخش تفسیر موقتاً غیرفعال است -->
    <!-- این بخش قرار است بعداً با یک سرویس هوش مصنوعی از نو پیاده‌سازی -->
    <!-- شود؛ فعلاً فقط یک وضعیت خالیِ هم‌سبک با بقیه تب‌های برنامه -->
    <!-- نمایش داده می‌شود (بدون هیچ منطق یا فراخوانی API). -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary-50 dark:bg-primary-900/20 flex items-center justify-center">
        <svg class="w-10 h-10 text-primary-500 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        به‌زودی
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        بخش تفسیر هوشمند در حال بازطراحی است و به‌زودی در دسترس قرار می‌گیرد.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
// 🆕 این کامپوننت موقتاً به یک وضعیت «به‌زودی» ساده تبدیل شده است.
// منطق قبلی (تولید تفسیر مبتنی بر قوانین ثابت) و اتصال آن به بک‌اند
// به‌طور کامل حذف شده‌اند؛ این تب بعداً با یک سرویس هوش مصنوعی از نو
// پیاده‌سازی خواهد شد. فعلاً هیچ prop، event یا فراخوانی API لازم نیست.
</script>
