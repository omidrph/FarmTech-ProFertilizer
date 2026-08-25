<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-950 dark:via-gray-900 dark:to-primary-950 py-4 sm:py-6 px-3 sm:px-4">
    <div class="w-full max-w-5xl mx-auto">

      <!-- کارت اصلی -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden">

        <!-- هدر -->
        <div class="bg-gradient-to-l from-primary-600 via-primary-700 to-primary-800 dark:from-primary-900 dark:via-primary-950 dark:to-gray-900 px-4 sm:px-8 py-6 sm:py-8 relative overflow-hidden">
          <div class="absolute -top-10 -left-10 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
          <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-primary-400/20 rounded-full blur-3xl"></div>
          <div class="relative z-10 flex flex-col sm:flex-row items-center sm:items-start gap-4">
            <!-- لوگو با پس‌زمینه سفید -->
            <div class="bg-white p-2 rounded-xl shadow-md flex-shrink-0">
              <img src="/Logo.webp" alt="سهند کود" class="h-12 w-12 sm:h-14 sm:w-14 object-contain" />
            </div>
            <div class="text-center sm:text-right">
              <h1 class="text-xl sm:text-3xl font-bold text-white">قوانین و شرایط استفاده</h1>
              <p class="text-primary-100 text-xs sm:text-sm mt-1">سامانه سهند کود — سیستم هوشمند نسخه‌نویسی کود</p>
            </div>
          </div>
        </div>

        <!-- بدنه متن قوانین -->
        <div class="px-4 sm:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8 text-gray-700 dark:text-gray-300 leading-7 sm:leading-8 text-justify" dir="rtl">

          <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">
            آخرین به‌روزرسانی: {{ lastUpdated }}
          </p>

          <p class="text-sm sm:text-base">
            پیش از استفاده از سامانه «سهند کود» (که در این سند به‌اختصار «سامانه» یا «ما» نامیده می‌شود)، لطفاً این قوانین و شرایط استفاده را با دقت مطالعه فرمایید. با ثبت‌نام، ورود، یا هرگونه استفاده از سامانه، شما این قوانین را به‌طور کامل مطالعه کرده، پذیرفته و متعهد به رعایت آن‌ها هستید. در صورت عدم موافقت با هر بخش از این شرایط، خواهشمندیم از ثبت‌نام و استفاده از سامانه خودداری فرمایید.
          </p>

          <!-- ۱ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۱</span>
              ماهیت و هدف سامانه
            </h2>
            <p class="text-sm sm:text-base">
              سامانه سهند کود یک ابزار نرم‌افزاری کمک‌محاسباتی است که با هدف تسهیل محاسبات تغذیه‌ای، تعادل یونی، ترکیب کودها و تهیه محلول‌های غذایی برای کشاورزی طراحی شده است. خروجی سامانه بر پایه فرمول‌ها، الگوریتم‌ها و اطلاعات ورودی کاربر (از جمله آنالیز آب، هدف تغذیه‌ای و کودهای انتخابی) تولید می‌شود و صرفاً جنبه راهنما و کمک‌تصمیم‌گیری دارد.
            </p>
          </section>

          <!-- ۲ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۲</span>
              عدم ارائه مشاوره تخصصی و ماهیت اطلاعاتی خروجی‌ها
            </h2>
            <p class="text-sm sm:text-base">
              استفاده از سامانه و خروجی‌های آن، جایگزین نظر کارشناس کشاورزی، خاک‌شناس، یا مشاور فنی مجرب نیست. نتایج محاسبات (از جمله میزان کود، ترکیب مخازن، تعادل یونی و EC/pH پیشنهادی) بر اساس داده‌های واردشده توسط کاربر و مدل‌های محاسباتی عمومی تولید می‌شوند و ممکن است به دلیل تفاوت در شرایط اقلیمی، نوع خاک، رقم گیاهی، کیفیت واقعی کودها، خطای اندازه‌گیری آب یا سایر عوامل محلی، با نیاز واقعی مزرعه یا گلخانه مطابقت کامل نداشته باشند. مسئولیت راستی‌آزمایی نهایی، آزمایش میدانی و تطبیق نتایج با شرایط واقعی، به‌طور کامل بر عهده کاربر یا کارشناس ناظر بر عملیات کشت است.
            </p>
          </section>

          <!-- ۳ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۳</span>
              سلب مسئولیت و محدودیت مسئولیت
            </h2>
            <p class="text-sm sm:text-base">
              سامانه سهند کود به‌صورت «همان‌گونه که هست» (As-Is) و «همان‌گونه که در دسترس است» (As-Available) ارائه می‌شود، بدون هیچ‌گونه ضمانت صریح یا ضمنی نسبت به دقت، صحت، به‌روز بودن، کامل بودن یا مناسب بودن نتایج برای هدف خاص کاربر. در حداکثر میزان مجاز طبق قوانین، تیم توسعه و مالکان سامانه هیچ‌گونه مسئولیتی در قبال موارد زیر نمی‌پذیرند:
            </p>
            <ul class="list-disc pr-6 mt-2 sm:mt-3 space-y-1 sm:space-y-2 text-sm sm:text-base">
              <li>هرگونه خسارت مستقیم یا غیرمستقیم، مالی، تولیدی یا محصولی ناشی از استفاده یا اتکا به نتایج محاسبات سامانه؛</li>
              <li>آسیب به محصول، خاک، تجهیزات آبیاری یا هر بخش دیگر از سامانه کشت، در نتیجه اجرای مستقیم پیشنهادهای سامانه بدون بازبینی کارشناسی؛</li>
              <li>خطاهای ناشی از ورود نادرست اطلاعات توسط کاربر (مانند آنالیز آب اشتباه، غلظت نادرست کود، یا انتخاب نامناسب کود)؛</li>
              <li>هرگونه وقفه، خطا، اختلال فنی، از دست رفتن داده یا عدم دسترسی موقت یا دائم به سامانه؛</li>
              <li>تصمیماتی که کاربر بر پایه اطلاعات یا محتوای آموزشی موجود در سامانه اتخاذ می‌کند.</li>
            </ul>
            <p class="mt-2 sm:mt-3 text-sm sm:text-base">
              استفاده از هرگونه خروجی سامانه در مقیاس واقعی (به‌ویژه در مقیاس تجاری و وسیع) باید پس از آزمایش در مقیاس کوچک و تأیید کارشناس ذی‌صلاح انجام شود.
            </p>
          </section>

          <!-- ۴ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۴</span>
              تعهدات کاربر
            </h2>
            <p class="text-sm sm:text-base">با ثبت‌نام در سامانه، کاربر متعهد می‌شود که:</p>
            <ul class="list-disc pr-6 mt-2 sm:mt-3 space-y-1 sm:space-y-2 text-sm sm:text-base">
              <li>اطلاعات ثبت‌نامی (نام، شماره تلفن و سایر مشخصات) را به‌درستی و با صحت کامل وارد کند؛</li>
              <li>مسئولیت حفظ محرمانگی رمز عبور و اطلاعات حساب کاربری خود را بر عهده بگیرد و از افشای آن به اشخاص ثالث خودداری کند؛</li>
              <li>از سامانه صرفاً برای اهداف مشروع و مرتبط با فعالیت کشاورزی استفاده کند؛</li>
              <li>پیش از اجرای عملی هر نسخه یا فرمول پیشنهادی، صحت آن را با دانش فنی خود یا مشورت کارشناس بررسی کند؛</li>
              <li>هیچ‌گونه اقدامی جهت آسیب‌رساندن به زیرساخت، امنیت یا عملکرد سامانه (مانند تلاش برای نفوذ، استخراج غیرمجاز داده یا اضافه‌بار عمدی) انجام ندهد.</li>
            </ul>
          </section>

          <!-- ۵ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۵</span>
              حریم خصوصی و داده‌های کاربر
            </h2>
            <p class="text-sm sm:text-base">
              اطلاعاتی که کاربر هنگام ثبت‌نام و استفاده از سامانه وارد می‌کند (شامل مشخصات هویتی، آنالیز آب، فرمول‌ها و گزارش‌های ذخیره‌شده) صرفاً برای ارائه خدمات سامانه، بهبود کیفیت محاسبات و پشتیبانی فنی مورد استفاده قرار می‌گیرد. این اطلاعات بدون رضایت کاربر در اختیار اشخاص ثالث قرار نخواهد گرفت، مگر در مواردی که طبق قانون یا دستور مراجع ذی‌صلاح الزامی باشد. کاربر می‌تواند نسبت به حذف حساب کاربری و اطلاعات مرتبط با آن، از طریق پشتیبانی سامانه اقدام کند.
            </p>
          </section>

          <!-- ۶ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۶</span>
              مالکیت فکری
            </h2>
            <p class="text-sm sm:text-base">
              کلیه حقوق مربوط به طراحی، منطق محاسباتی، پایگاه داده کودها و رسپی‌های سیستمی، نام تجاری و محتوای سامانه سهند کود متعلق به تیم توسعه‌دهنده و <strong>شرکت ستاره سهیل</strong> است. هرگونه کپی‌برداری، بازتولید تجاری، مهندسی معکوس یا استفاده غیرمجاز از بخش‌های اختصاصی سامانه بدون اجازه کتبی ممنوع است. اطلاعاتی که کاربر شخصاً وارد یا تولید می‌کند (مانند گزارش‌های اختصاصی و فرمول‌های شخصی‌سازی‌شده) متعلق به همان کاربر باقی می‌ماند.
            </p>
          </section>

          <!-- ۷ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۷</span>
              تعلیق یا لغو حساب کاربری
            </h2>
            <p class="text-sm sm:text-base">
              سامانه این حق را برای خود محفوظ می‌دارد که در صورت مشاهده سوءاستفاده، نقض این قوانین، فعالیت مشکوک یا مخاطره‌آمیز برای امنیت سایر کاربران، نسبت به محدودسازی، تعلیق موقت یا لغو دائم دسترسی هر حساب کاربری، بدون نیاز به اطلاع قبلی اقدام کند.
            </p>
          </section>

          <!-- ۸ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۸</span>
              تغییرات در قوانین
            </h2>
            <p class="text-sm sm:text-base">
              این قوانین ممکن است در آینده به‌روزرسانی شود. در صورت اعمال تغییرات اساسی، تلاش می‌شود از طریق سامانه به کاربران اطلاع‌رسانی شود. ادامه استفاده از سامانه پس از اعمال تغییرات، به‌منزله پذیرش قوانین جدید تلقی می‌شود.
            </p>
          </section>

          <!-- ۹ -->
          <section class="hover:bg-primary-50/30 dark:hover:bg-primary-900/10 p-3 sm:p-4 rounded-xl transition-colors duration-200">
            <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 flex items-center gap-2">
              <span class="flex items-center justify-center w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs sm:text-sm font-bold">۹</span>
              قانون حاکم
            </h2>
            <p class="text-sm sm:text-base">
              این قوانین تابع مقررات جمهوری اسلامی ایران است و هرگونه اختلاف احتمالی، در صورت عدم امکان حل‌وفصل دوستانه، مطابق قوانین و مراجع صالح داخلی رسیدگی خواهد شد.
            </p>
          </section>

          <!-- جمع‌بندی مسئولیت -->
          <div class="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 rounded-xl p-4 sm:p-5 flex gap-3">
            <svg class="w-5 h-5 sm:w-6 sm:h-6 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <p class="text-xs sm:text-sm text-amber-800 dark:text-amber-300 leading-6 sm:leading-7">
              با تأیید این قوانین، کاربر آگاهانه می‌پذیرد که سامانه سهند کود صرفاً یک ابزار کمک‌محاسباتی است، خروجی‌های آن جایگزین قضاوت کارشناسی نیست، و مسئولیت هرگونه بهره‌برداری عملی از نتایج، به‌طور کامل بر عهده کاربر می‌باشد.
            </p>
          </div>

          <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 pt-2">
            در صورت هرگونه پرسش درباره این قوانین، می‌توانید از طریق راه‌های ارتباطی موجود در سامانه با تیم پشتیبانی سهند کود در تماس باشید.
          </p>
        </div>

        <!-- فوتر با دکمه بازگشت -->
        <div class="px-4 sm:px-8 py-4 sm:py-6 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p class="text-xs text-gray-500 dark:text-gray-400 order-2 sm:order-1">
            © ۱۴۰۵ سهند کود - سیستم هوشمند نسخه‌نویسی کود
          </p>
          <button
            @click="goBack"
            class="w-full sm:w-auto px-5 py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-semibold rounded-xl transition-colors shadow-sm order-1 sm:order-2"
          >
            بازگشت به ثبت‌نام
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isDarkMode = ref(false);

// تاریخ آخرین به‌روزرسانی این متن قوانین - در صورت ویرایش محتوا، این مقدار را تغییر دهید
const lastUpdated = '۱۴۰۵/۰۶/۰۲';

// تابع تغییر تم حذف شد ولی متغیر isDarkMode و تنظیمات دارک ثابت موند

const goBack = () => {
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/register');
  }
};

onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>