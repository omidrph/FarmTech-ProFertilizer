<template>
  <AuthLayout title="ساخت حساب کاربری" subtitle="در چند ثانیه حساب بسازید و اولین فرمول کود خود را محاسبه کنید">
    <AuthAlert v-if="isDown" title="ارتباط با سرور برقرار نشد" hint="اینترنت خود را بررسی کنید و دوباره تلاش کنید." action-label="تلاش مجدد" @action="check" />
    <AuthAlert v-if="alertData" :title="alertData.title" :hint="alertData.hint" dismissible @close="clearError" />
    <AuthAlert v-if="registerSuccess" type="success" title="حساب شما ساخته شد! در حال ورود…" />

    <form @submit.prevent="handleRegister" class="space-y-5" novalidate>
      <div class="grid grid-cols-2 gap-3">
        <AuthField id="first" v-model="firstName" label="نام" placeholder="علی" icon="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" autocomplete="given-name" />
        <AuthField id="last" v-model="lastName" label="نام خانوادگی" placeholder="محمدی" autocomplete="family-name" />
      </div>

      <AuthField id="phone" v-model="phoneNumber" label="شمارهٔ موبایل" type="tel" inputmode="tel" autocomplete="tel"
        placeholder="۰۹۱۲۳۴۵۶۷۸۹" :maxlength="11" icon="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" :error="phoneError" @blur="phoneTouched = true" />

      <AuthField id="password" v-model="password" label="رمز عبور" type="password" autocomplete="new-password"
        placeholder="رمز عبور" icon="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
        <PasswordChecklist :rules="rules" />
      </AuthField>

      <div>
        <div class="flex items-start gap-2.5">
          <input id="accept-terms" type="checkbox" v-model="acceptedTerms" class="mt-1 w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
          <label for="accept-terms" class="text-sm text-gray-600 dark:text-gray-400 cursor-pointer select-none leading-relaxed">
            <router-link to="/terms" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors" @click.stop>قوانین و شرایط استفاده</router-link>
            را خوانده‌ام و می‌پذیرم.
          </label>
        </div>
        <p v-if="submitted && !acceptedTerms" class="text-xs text-danger-600 dark:text-danger-400 mt-1.5">برای ادامه، پذیرش قوانین و شرایط لازم است.</p>
      </div>

      <button type="submit" :disabled="isLoading || isDown" class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30">
        <span v-if="!isLoading">ساخت حساب</span>
        <span v-else class="flex items-center justify-center gap-2"><svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> در حال ساخت حساب…</span>
      </button>
    </form>

    <p class="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
      قبلاً ثبت‌نام کرده‌اید؟
      <router-link to="/login" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors">وارد شوید</router-link>
    </p>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { useConnection } from '@/composables/useConnection';
import { usePasswordRules } from '@/composables/usePasswordRules';
import { friendlyAuthError, normalizeDigits, isValidPhone } from '@/utils/authMessages';
import AuthLayout from '@/components/auth/AuthLayout.vue';
import AuthAlert from '@/components/auth/AuthAlert.vue';
import AuthField from '@/components/auth/AuthField.vue';
import PasswordChecklist from '@/components/auth/PasswordChecklist.vue';

const router = useRouter();
const { register, isLoading, error: authError } = useAuth();
const { isDown, check } = useConnection();

const firstName = ref('');
const lastName = ref('');
const phoneNumber = ref('');
const password = ref('');
const acceptedTerms = ref(false);
const submitted = ref(false);
const phoneTouched = ref(false);
const registerSuccess = ref(false);
const localError = ref('');

const { rules, isValid: isPasswordValid } = usePasswordRules(password);

watch(phoneNumber, (v) => { const n = normalizeDigits(v).replace(/\D/g, ''); if (n !== v) phoneNumber.value = n; });

const phoneError = computed(() =>
  phoneTouched.value && phoneNumber.value && !isValidPhone(phoneNumber.value)
    ? 'شمارهٔ موبایل باید ۱۱ رقم باشد و با ۰۹ شروع شود' : '');

const alertData = computed(() => {
  const raw = localError.value || authError.value;
  return raw ? friendlyAuthError(raw, 'register') : null;
});

const clearError = () => { localError.value = ''; authError.value = null; };

const handleRegister = async () => {
  submitted.value = true;
  clearError();
  phoneTouched.value = true;

  if (!firstName.value.trim() || !lastName.value.trim()) { localError.value = 'نام و نام خانوادگی را وارد کنید.'; return; }
  if (!isValidPhone(phoneNumber.value)) return;
  if (!isPasswordValid.value) { localError.value = 'رمز عبور هنوز همهٔ شرایط زیر فیلد را ندارد.'; return; }
  if (!acceptedTerms.value) return;
  if (isDown.value && !(await check())) return;

  const ok = await register({
    first_name: firstName.value.trim(),
    last_name: lastName.value.trim(),
    phone_number: phoneNumber.value,
    password: password.value,
  });
  if (ok) {
    registerSuccess.value = true;
    setTimeout(() => router.push('/'), 800);
  }
};

onMounted(check);
</script>
