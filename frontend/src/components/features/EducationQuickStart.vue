<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- گام‌ها -->
    <div class="space-y-3 sm:space-y-4">
      <!-- گام ۱ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[0] }"
        @click="toggleStep(0)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۱
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">ثبت‌نام و ورود به سیستم</h4>
              <span class="text-xs px-2 py-0.5 bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400 rounded-full">ضروری</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              برای استفاده از نرم‌افزار ابتدا باید ثبت‌نام کنید. پس از ثبت‌نام، با شماره تلفن و رمز عبور وارد شوید.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <router-link to="/register" class="text-xs sm:text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium flex items-center gap-1">
                <span>صفحه ثبت‌نام</span>
                <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </router-link>
              <router-link to="/login" class="text-xs sm:text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium flex items-center gap-1">
                <span>صفحه ورود</span>
                <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </router-link>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[0] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <!-- توضیحات کامل (قابل باز/بسته شدن) -->
        <div v-show="openSteps[0]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل ثبت‌نام:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>روی دکمه "ثبت‌نام" در صفحه ورود کلیک کنید</li>
            <li>نام، نام خانوادگی، شماره تلفن و رمز عبور خود را وارد کنید</li>
            <li>شماره تلفن باید با <code class="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-xs">09</code> شروع شود</li>
            <li>رمز عبور باید حداقل ۶ کاراکتر باشد</li>
          </ul>
          <p class="mt-2">✅ <strong>مراحل ورود:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>شماره تلفن و رمز عبور خود را وارد کنید</li>
            <li>پس از ورود، به صفحه اصلی هدایت می‌شوید</li>
          </ul>
          <div class="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3 mt-2 text-primary-700 dark:text-primary-300 text-xs sm:text-sm">
            💡 <strong>نکته:</strong> پس از ورود، توکن احراز هویت به صورت خودکار در مرورگر ذخیره می‌شود و تا ۲۴ ساعت معتبر است.
          </div>
        </div>
      </div>

      <!-- گام ۲ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[1] }"
        @click="toggleStep(1)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۲
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">تعریف کودها در پایگاه داده</h4>
              <span class="text-xs px-2 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded-full">پیش‌نیاز</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              قبل از محاسبه کود، باید کودهای مورد نظر خود را در پایگاه داده تعریف کنید.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">📍 مسیر: تب <strong class="text-gray-700 dark:text-gray-300">خانه</strong> → <strong class="text-gray-700 dark:text-gray-300">پایگاه داده کودها</strong></span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[1] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <div v-show="openSteps[1]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل تعریف کود:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>به تب <strong>"پایگاه داده کودها"</strong> بروید</li>
            <li>روی دکمه <strong>"افزودن کود جدید"</strong> کلیک کنید</li>
            <li>نام کود، قیمت هر کیلوگرم و درصد عناصر موجود در آن را وارد کنید</li>
            <li>برای بارگذاری نمونه‌های آماده، روی <strong>"بارگذاری نمونه"</strong> کلیک کنید</li>
          </ul>
          <div class="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-3 mt-2 text-yellow-700 dark:text-yellow-300 text-xs sm:text-sm">
            ⚠️ <strong>توجه:</strong> درصد عناصر باید بین ۰ تا ۱۰۰ باشد و مجموع آنها نباید از ۱۰۰ بیشتر شود.
          </div>
          <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mt-2 text-green-700 dark:text-green-300 text-xs sm:text-sm">
            ✅ <strong>نکته:</strong> می‌توانید کودهای اسیدی مانند H3PO4، HNO3 و H2SO4 را نیز تعریف کنید.
          </div>
        </div>
      </div>

      <!-- گام ۳ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[2] }"
        @click="toggleStep(2)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۳
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">وارد کردن آنالیز آب</h4>
              <span class="text-xs px-2 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded-full">پیش‌نیاز</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              اطلاعات آنالیز آب و پساب خود را وارد کنید تا نرم‌افزار بتواند محاسبات دقیق انجام دهد.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">📍 مسیر: تب <strong class="text-gray-700 dark:text-gray-300">خانه</strong> → <strong class="text-gray-700 dark:text-gray-300">آنالیز آب</strong></span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[2] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <div v-show="openSteps[2]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل وارد کردن آنالیز آب:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>درصد آب و پساب را در بخش بالایی وارد کنید (مثلاً ۸۰٪ آب و ۲۰٪ پساب)</li>
            <li>مقدار شوری آب را وارد کنید</li>
            <li>در جدول، مقادیر هر عنصر را برای آب و پساب به صورت مجزا وارد کنید</li>
            <li>ستون <strong>"مقادیر تامینی"</strong> به صورت خودکار محاسبه می‌شود</li>
          </ul>
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mt-2 text-blue-700 dark:text-blue-300 text-xs sm:text-sm">
            💡 <strong>نکته:</strong> واحدهای قابل انتخاب شامل PPM/L، MEQ/L و MMOLS/L هستند. واحد پیش‌فرض PPM/L است.
          </div>
        </div>
      </div>

      <!-- گام ۴ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[3] }"
        @click="toggleStep(3)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۴
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">تعیین عناصر هدف</h4>
              <span class="text-xs px-2 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded-full">پیش‌نیاز</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              مقدار مورد نظر خود را برای هر عنصر غذایی تعیین کنید. نرم‌افزار تعادل یونی را به صورت خودکار بررسی می‌کند.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">📍 مسیر: تب <strong class="text-gray-700 dark:text-gray-300">خانه</strong> → <strong class="text-gray-700 dark:text-gray-300">عناصر هدف</strong></span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[3] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <div v-show="openSteps[3]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل تعیین عناصر هدف:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>مقادیر مورد نظر خود را برای هر عنصر در جدول وارد کنید</li>
            <li>نرم‌افزار به صورت خودکار <strong>تعادل کاتیون و آنیون</strong> را محاسبه می‌کند</li>
            <li>اگر تعادل برقرار نباشد، پیام هشدار نمایش داده می‌شود</li>
            <li>با کلیک روی <strong>"اعمال تغییرات"</strong> مقادیر ذخیره می‌شوند</li>
          </ul>
          <div class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3 mt-2 text-purple-700 dark:text-purple-300 text-xs sm:text-sm">
            🔬 <strong>عناصر قابل تنظیم:</strong> N-NO3، P، S، N-NH4، K، Ca، Mg، Na، Cl، Fe، Mn، Zn، B، Cu، Mo
          </div>
          <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 mt-2 text-red-700 dark:text-red-300 text-xs sm:text-sm">
            ⚠️ <strong>توجه:</strong> اختلاف کاتیون و آنیون باید کمتر از ۰.۵ باشد تا تعادل برقرار شود.
          </div>
        </div>
      </div>

      <!-- گام ۵ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[4] }"
        @click="toggleStep(4)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۵
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">محاسبه خودکار مقدار کود</h4>
              <span class="text-xs px-2 py-0.5 bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400 rounded-full">اصلی</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              با انتخاب کودهای تعریف شده، نرم‌افزار به صورت خودکار مقدار دقیق هر کود را محاسبه می‌کند.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">📍 مسیر: تب <strong class="text-gray-700 dark:text-gray-300">خانه</strong> → <strong class="text-gray-700 dark:text-gray-300">محاسبه خودکار مقدار کود</strong></span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[4] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <div v-show="openSteps[4]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل محاسبه کود:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>از لیست، کودهای مورد نظر خود را انتخاب کنید (با نگه‌داشتن Ctrl می‌توانید چند کود انتخاب کنید)</li>
            <li>روی دکمه <strong>"افزودن"</strong> کلیک کنید تا کودها به جدول محاسبه اضافه شوند</li>
            <li>حجم مخزن (لیتر) و ضریب رقیق‌سازی را وارد کنید</li>
            <li>برای هر کود، وزن (گرم) و خلوص (درصد) را وارد کنید</li>
            <li>روی دکمه <strong>"محاسبه"</strong> کلیک کنید</li>
            <li>نرم‌افزار سهم هر عنصر، هزینه و مجموع را محاسبه می‌کند</li>
          </ul>
          <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mt-2 text-green-700 dark:text-green-300 text-xs sm:text-sm">
            ✅ <strong>نتیجه:</strong> پس از محاسبه، جدول کامل با وزن، خلوص، هزینه و سهم هر عنصر نمایش داده می‌شود.
          </div>
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mt-2 text-blue-700 dark:text-blue-300 text-xs sm:text-sm">
            💡 <strong>نکته:</strong> اسیدها (H3PO4، HNO3، H2SO4) به صورت پیش‌فرض در جدول وجود دارند و قابل حذف نیستند.
          </div>
        </div>
      </div>

      <!-- گام ۶ -->
      <div 
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-all duration-200 hover:shadow-md cursor-pointer"
        :class="{ 'border-primary-300 dark:border-primary-700': openSteps[5] }"
        @click="toggleStep(5)"
      >
        <div class="flex items-start gap-3 sm:gap-4">
          <div class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm sm:text-base">
            ۶
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h4 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">تفسیر داده‌ها و دریافت گزارش</h4>
              <span class="text-xs px-2 py-0.5 bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400 rounded-full">نهایی</span>
            </div>
            <p class="text-sm sm:text-base text-gray-600 dark:text-gray-400">
              پس از تکمیل محاسبات، نرم‌افزار یک تفسیر کامل از وضعیت تغذیه گیاه و توصیه‌های کودی ارائه می‌دهد.
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">📍 مسیر: تب <strong class="text-gray-700 dark:text-gray-300">خانه</strong> → <strong class="text-gray-700 dark:text-gray-300">تفسیر داده‌ها</strong></span>
            </div>
          </div>
          <div class="flex-shrink-0 mt-1">
            <svg 
              class="w-5 h-5 sm:w-6 sm:h-6 transition-transform duration-300 text-gray-400 dark:text-gray-500"
              :class="{ 'rotate-180': openSteps[5] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
        
        <div v-show="openSteps[5]" class="mt-3 sm:mt-4 mr-11 sm:mr-14 space-y-2 text-sm sm:text-base text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-700 pt-3 sm:pt-4">
          <p>✅ <strong>مراحل دریافت تفسیر:</strong></p>
          <ul class="list-disc list-inside space-y-1 mr-4">
            <li>اطمینان حاصل کنید که آنالیز آب و عناصر هدف را وارد کرده‌اید</li>
            <li>محاسبات کود را انجام داده باشید</li>
            <li>روی دکمه <strong>"تولید تفسیر"</strong> کلیک کنید</li>
            <li>گزارش کامل شامل موارد زیر نمایش داده می‌شود:</li>
          </ul>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
              <span class="font-semibold text-gray-700 dark:text-gray-300">🔬 تعادل یونی</span>
              <p class="text-xs text-gray-500 dark:text-gray-400">بررسی تعادل کاتیون و آنیون</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
              <span class="font-semibold text-gray-700 dark:text-gray-300">📊 وضعیت عناصر</span>
              <p class="text-xs text-gray-500 dark:text-gray-400">کمبود، بیش‌بود یا سمیت</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
              <span class="font-semibold text-gray-700 dark:text-gray-300">💧 کیفیت آب</span>
              <p class="text-xs text-gray-500 dark:text-gray-400">تأثیر شوری آب</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
              <span class="font-semibold text-gray-700 dark:text-gray-300">🧪 توصیه‌های کودی</span>
              <p class="text-xs text-gray-500 dark:text-gray-400">راهکارهای اصلاحی</p>
            </div>
          </div>
          <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mt-2 text-green-700 dark:text-green-300 text-xs sm:text-sm">
            🖨️ <strong>چاپ گزارش:</strong> با کلیک روی دکمه "چاپ گزارش" می‌توانید خروجی را پرینت بگیرید.
          </div>
        </div>
      </div>
    </div>

    <!-- دکمه ریست -->
    <div class="text-center">
      <button 
        @click="resetSteps" 
        class="text-xs text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-400 transition-colors"
      >
        ↺ بستن همه
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// ===== State =====
const openSteps = ref<boolean[]>([false, false, false, false, false, false]);

// ===== Methods =====
const toggleStep = (step: number) => {
  openSteps.value[step] = !openSteps.value[step];
};

const resetSteps = () => {
  openSteps.value = [false, false, false, false, false, false];
};
</script>

<style scoped>
code {
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  background-color: #f3f4f6;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
}

.dark code {
  background-color: #374151;
}

.list-disc {
  list-style-type: disc;
}

.list-inside {
  list-style-position: inside;
}

.cursor-pointer {
  cursor: pointer;
}
</style>