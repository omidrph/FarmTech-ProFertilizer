<template>
  <AuthLayout title="ورود به سهند کود" subtitle="شمارهٔ موبایل و رمز عبور خود را وارد کنید">
    <AuthAlert v-if="isDown" title="ارتباط با سرور برقرار نشد" hint="اینترنت خود را بررسی کنید و دوباره تلاش کنید." action-label="تلاش مجدد" @action="check" />
    <AuthAlert v-if="alertData" :title="alertData.title" :hint="alertData.hint" dismissible @close="authError = null" />
    <AuthAlert v-if="loginSuccess" type="success" title="خوش آمدید! در حال انتقال…" />

    <form @submit.prevent="handleLogin" class="space-y-5" novalidate>
      <AuthField id="phone" v-model="phoneNumber" label="شمارهٔ موبایل" type="tel" inputmode="tel" autocomplete="tel"
        placeholder="۰۹۱۲۳۴۵۶۷۸۹" :maxlength="11" icon="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" :error="phoneError" @blur="phoneTouched = true" />

      <AuthField id="password" v-model="password" label="رمز عبور" type="password" autocomplete="current-password"
        placeholder="رمز عبور" icon="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
        <div class="mt-2 text-left">
          <router-link to="/forgot-password" class="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors">رمز عبور را فراموش کرده‌اید؟</router-link>
        </div>
      </AuthField>

      <button type="submit" :disabled="isLoading || isDown" class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30 mt-2">
        <span v-if="!isLoading">ورود به حساب</span>
        <span v-else class="flex items-center justify-center gap-2"><svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> در حال ورود…</span>
      </button>
    </form>

    <p class="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
      حساب ندارید؟
      <router-link to="/register" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors">ثبت‌نام کنید</router-link>
    </p>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { useConnection } from '@/composables/useConnection';
import { friendlyAuthError, normalizeDigits, isValidPhone } from '@/utils/authMessages';
import AuthLayout from '@/components/auth/AuthLayout.vue';
import AuthAlert from '@/components/auth/AuthAlert.vue';
import AuthField from '@/components/auth/AuthField.vue';

const router = useRouter();
const { login, isLoading, error: authError } = useAuth();
const { isDown, check } = useConnection();

const phoneNumber = ref('');
const password = ref('');
const phoneTouched = ref(false);
const loginSuccess = ref(false);

watch(phoneNumber, (v) => { const n = normalizeDigits(v).replace(/\D/g, ''); if (n !== v) phoneNumber.value = n; });

const phoneError = computed(() =>
  phoneTouched.value && phoneNumber.value && !isValidPhone(phoneNumber.value)
    ? 'شمارهٔ موبایل باید ۱۱ رقم باشد و با ۰۹ شروع شود' : '');

const alertData = computed(() => (authError.value ? friendlyAuthError(authError.value, 'login') : null));

const handleLogin = async () => {
  phoneTouched.value = true;
  if (!isValidPhone(phoneNumber.value) || !password.value) return;
  if (isDown.value && !(await check())) return;

  if (await login(phoneNumber.value, password.value)) {
    loginSuccess.value = true;
    setTimeout(() => router.push('/'), 800);
  }
};

onMounted(check);
</script>
