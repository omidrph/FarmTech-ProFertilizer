<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-950 dark:via-gray-900 dark:to-primary-950 flex relative overflow-hidden">
    
    <!-- دکمه تغییر تم -->
    <button
      @click="toggleTheme"
      class="absolute top-4 left-4 z-50 p-2.5 rounded-xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm"
      :title="isDarkMode ? 'حالت روشن' : 'حالت تاریک'"
    >
      <svg v-if="isDarkMode" class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
      </svg>
      <svg v-else class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
      </svg>
    </button>

    <!-- ============================================================ -->
    <!-- بخش سمت راست - توضیحات برنامه (فقط دسکتاپ) -->
    <!-- ============================================================ -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-bl from-primary-600 via-primary-700 to-primary-900 dark:from-primary-900 dark:via-primary-950 dark:to-gray-900">
      
      <!-- پس‌زمینه تزئینی -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-20 -right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-20 -left-20 w-96 h-96 bg-primary-400/20 rounded-full blur-3xl"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary-500/10 rounded-full blur-3xl"></div>
      </div>

      <!-- محتوای اسلایدر -->
      <div class="relative z-10 flex flex-col justify-center items-center w-full px-12 py-12">
        
        <!-- لوگو بزرگ -->
        <div class="mb-6">
          <div class="relative">
            <div class="absolute inset-0 bg-white/20 rounded-full blur-2xl"></div>
            <img src="/Logo.webp" alt="سهند کود" class="relative h-28 w-28 object-contain drop-shadow-2xl" />
          </div>
        </div>

        <!-- عنوان اصلی -->
        <h1 class="text-4xl font-bold text-white text-center mb-2">
          سهند کود
        </h1>
        <p class="text-primary-100 text-center text-base mb-10">
          سیستم هوشمند نسخه‌نویسی کود
        </p>

        <!-- اسلایدر توضیحات -->
        <div class="relative w-full max-w-md min-h-[200px]">
          <div class="absolute inset-0 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-2xl"></div>
          
          <TransitionGroup name="slide-fade" tag="div" class="relative">
            <div
              v-for="(slide, index) in slides"
              :key="slide.id"
              v-show="currentSlide === index"
              class="absolute inset-0 p-5"
            >
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
                  <div v-html="slide.icon" class="w-6 h-6 text-white"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-white font-bold text-base mb-1.5">{{ slide.title }}</h3>
                  <p class="text-primary-100 text-sm leading-relaxed">{{ slide.description }}</p>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>

        <!-- نقاط اسلایدر -->
        <div class="flex items-center gap-2 mt-6">
          <button
            v-for="(slide, index) in slides"
            :key="index"
            @click="currentSlide = index"
            class="transition-all duration-300 rounded-full"
            :class="currentSlide === index 
              ? 'w-8 h-2 bg-white' 
              : 'w-2 h-2 bg-white/40 hover:bg-white/60'"
          ></button>
        </div>

        <!-- ویژگی‌های پایین -->
        <div class="mt-10 grid grid-cols-3 gap-4 w-full max-w-md">
          <div class="text-center">
            <div class="text-2xl font-bold text-white">۱۵</div>
            <div class="text-xs text-primary-200 mt-1">عنصر غذایی</div>
          </div>
          <div class="text-center border-x border-white/20">
            <div class="text-2xl font-bold text-white">۳</div>
            <div class="text-xs text-primary-200 mt-1">مخزن A,B,C</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-white">۴۲+</div>
            <div class="text-xs text-primary-200 mt-1">کود ایرانی</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش سمت چپ - فرم فراموشی رمز عبور -->
    <!-- ============================================================ -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-8">
      <div class="w-full max-w-md">
        
        <!-- لوگو موبایل -->
        <div class="lg:hidden text-center mb-6">
          <div class="relative inline-block">
            <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-xl"></div>
            <img src="/Logo.webp" alt="سهند کود" class="relative h-20 w-20 object-contain" />
          </div>
        </div>

        <!-- عنوان -->
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            فراموشی رمز عبور
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            کد تأیید به شماره تلفن شما ارسال خواهد شد
          </p>
        </div>

        <!-- پیام خطای اتصال -->
        <Transition name="fade">
          <div v-if="connectionStatus === 'disconnected'" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-3 mb-4">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <div class="flex-1">
                <p class="text-danger-700 dark:text-danger-400 text-sm font-medium">اتصال به سرور برقرار نیست</p>
                <p class="text-danger-600 dark:text-danger-500 text-xs mt-1">لطفاً مطمئن شوید بک‌اند در حال اجراست</p>
              </div>
              <button @click="retryConnection" class="text-danger-600 hover:text-danger-800 dark:hover:text-danger-300">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </button>
            </div>
          </div>
        </Transition>

        <!-- ===== پیام‌های خطا و موفقیت ===== -->
        <Transition name="fade">
          <div v-if="errorMessage" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-3 mb-4">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              <p class="text-danger-700 dark:text-danger-400 text-sm">{{ errorMessage }}</p>
            </div>
          </div>
        </Transition>

        <Transition name="fade">
          <div v-if="successMessage" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-3 mb-4">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-success-600 dark:text-success-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <p class="text-success-700 dark:text-success-400 text-sm">{{ successMessage }}</p>
            </div>
          </div>
        </Transition>

        <!-- ===== مرحله ۱: وارد کردن شماره تلفن ===== -->
        <div v-if="step === 1">
          <form @submit.prevent="handleSendCode" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                شماره تلفن
              </label>
              <div class="relative group">
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                </div>
                <input
                  type="tel"
                  v-model="phoneNumber"
                  placeholder="مثال: 09121234567"
                  required
                  pattern="09[0-9]{9}"
                  class="w-full pr-10 pl-4 py-3 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-primary-500 dark:focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all duration-200"
                />
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                شماره تلفن باید با 09 شروع شود و 11 رقم باشد
              </p>
            </div>

            <button
              type="submit"
              :disabled="isLoading || connectionStatus === 'disconnected'"
              class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30 hover:shadow-primary-500/50 transition-shadow"
            >
              <span v-if="!isLoading" class="flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                ارسال کد تأیید
              </span>
              <span v-else class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                در حال ارسال...
              </span>
            </button>
          </form>

          <div class="mt-6 text-center">
            <router-link to="/login" class="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors flex items-center justify-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              بازگشت به ورود
            </router-link>
          </div>
        </div>

        <!-- ===== مرحله ۲: وارد کردن کد و رمز جدید ===== -->
        <div v-else-if="step === 2">
          <form @submit.prevent="handleResetPassword" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                کد تأیید ۶ رقمی
              </label>
              <div class="relative group">
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                  </svg>
                </div>
                <input
                  type="text"
                  v-model="verificationCode"
                  placeholder="مثال: 123456"
                  required
                  minlength="6"
                  maxlength="6"
                  class="w-full pr-10 pl-4 py-3 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-primary-500 dark:focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all duration-200 text-center text-2xl tracking-widest"
                  autocomplete="off"
                />
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                کد ۶ رقمی ارسال شده به تلفن همراه را وارد کنید
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                رمز عبور جدید
              </label>
              <div class="relative group">
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                </div>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="newPassword"
                  placeholder="رمز عبور خود را وارد کنید"
                  required
                  minlength="8"
                  class="w-full pr-10 pl-12 py-3 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-primary-500 dark:focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all duration-200"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                >
                  <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                  </svg>
                </button>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1.5 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                حداقل ۸ کاراکتر با حروف بزرگ، کوچک، عدد و کاراکتر خاص
              </p>
            </div>

            <button
              type="submit"
              :disabled="isLoading || !isPasswordValid || connectionStatus === 'disconnected'"
              class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30 hover:shadow-primary-500/50 transition-shadow"
            >
              <span v-if="!isLoading" class="flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                بازنشانی رمز عبور
              </span>
              <span v-else class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                در حال بازنشانی...
              </span>
            </button>

            <button
              type="button"
              @click="step = 1"
              class="w-full py-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors flex items-center justify-center gap-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              بازگشت و ارسال مجدد کد
            </button>
          </form>
        </div>

        <!-- لینک ثبت‌نام (برای کاربرانی که حساب ندارند) -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            حساب کاربری ندارید؟
            <router-link 
              to="/register" 
              class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors"
            >
              ثبت‌نام کنید
            </router-link>
          </p>
        </div>

        <!-- فوتر -->
        <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <p class="text-xs text-center text-gray-500 dark:text-gray-400">
            © ۱۴۰۵ سهند کود - سیستم هوشمند نسخه‌نویسی کود
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import axios from 'axios';

const router = useRouter();
const { forgotPassword, resetPassword, isLoading } = useAuth();

const step = ref(1);
const phoneNumber = ref('');
const verificationCode = ref('');
const newPassword = ref('');
const showPassword = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const isDarkMode = ref(false);
const currentSlide = ref(0);

const connectionStatus = ref<'checking' | 'connected' | 'disconnected'>('checking');

const slides = [
  {
    id: 1,
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>`,
    title: 'محاسبه دقیق فرمول غذایی',
    description: 'با الگوریتم علمی، مقدار دقیق هر کود را برای رسیدن به ۱۵ عنصر هدف محاسبه کنید. از نیتروژن تا مولیبدن، همه چیز خودکار است.'
  },
  {
    id: 2,
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>`,
    title: 'مدیریت هوشمند مخازن A,B,C',
    description: 'تقسیم خودکار کودها در سه مخزن بر اساس سازگاری شیمیایی. جلوگیری از رسوب کلسیم-فسفات و تداخلات یونی.'
  },
  {
    id: 3,
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>`,
    title: 'آنالیز جامع آب و پساب',
    description: 'بررسی شوری EC، مقادیر عناصر و محاسبه خودکار مقادیر تامینی. تبدیل واحد بین PPM، MEQ و MMOL.'
  },
  {
    id: 4,
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`,
    title: 'پایش تعادل یونی',
    description: 'محاسبه خودکار کاتیون و آنیون با تلرانس ۰.۵ meq/L. هشدار فوری در صورت عدم تعادل محلول غذایی.'
  },
  {
    id: 5,
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>`,
    title: 'پایگاه داده ۴۲+ کود ایرانی',
    description: 'از برندهای معتبر اطلس، رازاک شیمی، ردسا و گل سم گرگان. شامل NPK، کلات EDTA/EDDHA، سولفات و اسیدها.'
  }
];

let slideInterval: number | null = null;

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
};

const checkConnection = async (): Promise<boolean> => {
  connectionStatus.value = 'checking';
  try {
    // 🔧 قبلاً آدرس مطلق "http://localhost:8000/health" هاردکد بود که
    // در پروڈاکشن همیشه fail می‌شد. اکنون مسیر نسبی است و nginx آن را
    // به بک‌اند پروکسی می‌کند.
    const response = await axios.get('/health', {
      timeout: 3000,
    });
    connectionStatus.value = response.status === 200 ? 'connected' : 'disconnected';
    return connectionStatus.value === 'connected';
  } catch {
    connectionStatus.value = 'disconnected';
    return false;
  }
};

const retryConnection = async () => {
  await checkConnection();
};

// ===== اعتبارسنجی رمز عبور =====
const passwordRequirements = computed(() => {
  const p = newPassword.value || '';
  return {
    hasMinLength: p.length >= 8,
    hasUpperCase: /[A-Z]/.test(p),
    hasLowerCase: /[a-z]/.test(p),
    hasNumber: /[0-9]/.test(p),
    hasSpecialChar: /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]/.test(p)
  };
});

const isPasswordValid = computed(() => {
  const req = passwordRequirements.value;
  return req.hasMinLength && req.hasUpperCase && req.hasLowerCase && 
         req.hasNumber && req.hasSpecialChar;
});

// ===== ارسال کد =====
const handleSendCode = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  
  if (connectionStatus.value !== 'connected') {
    const connected = await checkConnection();
    if (!connected) {
      return;
    }
  }
  
  if (!phoneNumber.value || !/^09[0-9]{9}$/.test(phoneNumber.value)) {
    errorMessage.value = 'لطفاً شماره تلفن معتبر وارد کنید';
    return;
  }
  
  const result = await forgotPassword(phoneNumber.value);
  
  if (result.success) {
    successMessage.value = result.message;
    step.value = 2;
  } else {
    errorMessage.value = result.message;
  }
};

// ===== بازنشانی رمز =====
const handleResetPassword = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  
  if (!isPasswordValid.value) {
    errorMessage.value = 'لطفاً رمز عبور معتبر وارد کنید (حداقل ۸ کاراکتر با حروف بزرگ، کوچک، عدد و کاراکتر خاص)';
    return;
  }
  
  if (!verificationCode.value || verificationCode.value.length !== 6) {
    errorMessage.value = 'لطفاً کد تأیید ۶ رقمی را وارد کنید';
    return;
  }
  
  const result = await resetPassword(
    phoneNumber.value,
    verificationCode.value,
    newPassword.value
  );
  
  if (result.success) {
    successMessage.value = result.message;
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } else {
    errorMessage.value = result.message;
  }
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length;
};

onMounted(async () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  }
  
  await checkConnection();
  slideInterval = window.setInterval(nextSlide, 4000);
});

onUnmounted(() => {
  if (slideInterval) {
    clearInterval(slideInterval);
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-enter-active {
  transition: all 0.6s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.4s ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-fade-move {
  transition: transform 0.5s;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>