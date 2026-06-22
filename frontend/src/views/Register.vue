<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-950 dark:to-gray-900 flex items-center justify-center p-4">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full p-6 sm:p-8 border border-gray-200 dark:border-gray-700">
      <!-- Logo -->
      <div class="text-center mb-6">
        <img src="/Logo.webp" alt="FarmTech" class="h-12 w-auto mx-auto mb-3 object-contain" />
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">ثبت‌نام</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">ساخت حساب کاربری جدید</p>
      </div>

      <!-- Error Message -->
      <div v-if="authError" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-3 mb-4">
        <p class="text-danger-700 dark:text-danger-400 text-sm">{{ authError }}</p>
      </div>

      <!-- Success Message -->
      <div v-if="registerSuccess" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-3 mb-4">
        <p class="text-success-700 dark:text-success-400 text-sm">ثبت‌نام با موفقیت انجام شد!</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <!-- نام -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            نام
          </label>
          <input
            type="text"
            v-model="firstName"
            placeholder="مثال: علی"
            required
            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- نام خانوادگی -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            نام خانوادگی
          </label>
          <input
            type="text"
            v-model="lastName"
            placeholder="مثال: محمدی"
            required
            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- شماره تلفن -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            شماره تلفن
          </label>
          <div class="relative">
            <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
            </span>
            <input
              type="tel"
              v-model="phoneNumber"
              placeholder="مثال: 09121234567"
              required
              class="w-full pr-10 pl-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <!-- رمز عبور -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            رمز عبور
          </label>
          <div class="relative">
            <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </span>
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="حداقل ۶ کاراکتر"
              required
              minlength="6"
              class="w-full pr-10 pl-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
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
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">رمز عبور باید حداقل ۶ کاراکتر باشد</p>
        </div>

        <!-- دکمه ثبت‌نام -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-2"
        >
          <span v-if="!isLoading">ثبت‌نام</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            در حال ثبت‌نام...
          </span>
        </button>
      </form>

      <!-- لینک ورود -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          قبلاً ثبت‌نام کرده‌اید؟
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium transition-colors">
            وارد شوید
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const { register, isLoading, error: authError } = useAuth();

const firstName = ref('');
const lastName = ref('');
const phoneNumber = ref('');
const password = ref('');
const showPassword = ref(false);
const registerSuccess = ref(false);

const handleRegister = async () => {
  const success = await register({
    first_name: firstName.value,
    last_name: lastName.value,
    phone_number: phoneNumber.value,
    password: password.value
  });
  
  if (success) {
    registerSuccess.value = true;
    setTimeout(() => {
      router.push('/');
    }, 500);
  }
};
</script>