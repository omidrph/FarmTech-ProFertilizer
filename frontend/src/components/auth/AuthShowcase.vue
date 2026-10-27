
<template>
  <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-bl from-primary-600 via-primary-700 to-primary-900 dark:from-primary-900 dark:via-primary-950 dark:to-gray-900">
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-20 -right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -left-20 w-96 h-96 bg-primary-400/20 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative z-10 flex flex-col justify-center items-center w-full px-12 py-12">
      <div class="mb-6 relative">
        <div class="absolute inset-0 bg-white/20 rounded-full blur-2xl"></div>
        <img src="/Logo.webp" alt="سهند کود" class="relative h-28 w-28 object-contain drop-shadow-2xl" />
      </div>
      <h1 class="text-4xl font-bold text-white text-center mb-2">سهند کود</h1>
      <p class="text-primary-100 text-center text-base mb-10">سیستم هوشمند نسخه‌نویسی کود</p>

      <div class="relative w-full max-w-md min-h-[150px]">
        <div class="absolute inset-0 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-2xl"></div>
        <Transition name="slide-fade" mode="out-in">
          <div :key="slides[current].title" class="relative p-5 flex items-start gap-4">
            <div class="flex-shrink-0 w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="slides[current].icon" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-white font-bold text-base mb-1.5">{{ slides[current].title }}</h3>
              <p class="text-primary-100 text-sm leading-relaxed">{{ slides[current].text }}</p>
            </div>
          </div>
        </Transition>
      </div>

      <div class="flex items-center gap-2 mt-6">
        <button v-for="(s, i) in slides" :key="s.title" type="button" @click="go(i)" :aria-label="s.title"
          class="transition-all duration-300 rounded-full h-2"
          :class="current === i ? 'w-8 bg-white' : 'w-2 bg-white/40 hover:bg-white/60'"></button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const slides = [
  { title: 'فرمول غذایی دقیق، در چند دقیقه',
    text: 'کودها را با حالت دقیق‌ترین یا کم‌هزینه‌ترین محاسبه کنید؛ یا با محاسبهٔ دستی، مقدار دلخواه خودتان را وارد کنید.',
    icon: 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z' },
  { title: 'تنظیم pH با اسید و باز',
    text: 'از محلول نمونه بردارید و اسید یا باز را مرحله‌به‌مرحله اضافه کنید؛ مقدار لازم برای مخزن حساب می‌شود و مستقیم در فرمول لحاظ می‌گردد.',
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z' },
  { title: 'مخازن بدون رسوب',
    text: 'کودها بر اساس سازگاری شیمیایی بین مخازن تقسیم می‌شوند و خطر رسوب کلسیم، فسفات و سولفات همان لحظه هشدار می‌گیرد.',
    icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' },
  { title: 'تعادل یونی و EC همیشه زیر نظر',
    text: 'بعد از هر تغییر، کاتیون، آنیون و EC دوباره محاسبه می‌شود و خطاها و هشدارها همراه راهنمای اصلاح نمایش داده می‌شوند.',
    icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
  { title: 'کودهای شرکتی و مایع، آماده',
    text: 'کودهای پایه و شرکتی با مقادیر برگهٔ آزمایش در دسترس‌اند و کودهای مایع را هم می‌توانید با لیتر و میلی‌لیتر وارد کنید.',
    icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { title: 'آنالیز آب و گزارش‌ها',
    text: 'آنالیز آب را با قالب‌های ذخیره‌شده وارد کنید، گزارش‌ها را نگه دارید و هر زمان خروجی PDF بگیرید.',
    icon: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
];

const current = ref(0);
let timer: number | null = null;
const start = () => { stop(); timer = window.setInterval(() => (current.value = (current.value + 1) % slides.length), 5000); };
const stop = () => { if (timer) clearInterval(timer); timer = null; };
const go = (i: number) => { current.value = i; start(); };

onMounted(start);
onUnmounted(stop);
</script>

<style scoped>
.slide-fade-enter-active { transition: all .45s ease-out; }
.slide-fade-leave-active { transition: all .25s ease-in; }
.slide-fade-enter-from { opacity: 0; transform: translateX(24px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-24px); }
</style>
