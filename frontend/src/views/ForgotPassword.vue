<template>
  <AuthLayout :title="step === 1 ? 'بازیابی رمز عبور' : 'کد پیامک‌شده را وارد کنید'"
    :subtitle="step === 1 ? 'شمارهٔ موبایل خود را وارد کنید تا کد ۶ رقمی را با پیامک برایتان بفرستیم.' : ''">
    <AuthAlert v-if="isDown" title="ارتباط با سرور برقرار نشد" hint="اینترنت خود را بررسی کنید و دوباره تلاش کنید." action-label="تلاش مجدد" @action="check" />
    <AuthAlert v-if="alertData" :title="alertData.title" :hint="alertData.hint" dismissible @close="errorMessage = ''" />
    <AuthAlert v-if="infoMessage" type="info" :title="infoMessage" />
    <AuthAlert v-if="done" type="success" title="رمز عبور تغییر کرد. اکنون وارد شوید." />

    <form v-if="step === 1" @submit.prevent="handleSendCode" class="space-y-5" novalidate>
      <AuthField id="phone" v-model="phoneNumber" label="شمارهٔ موبایل" type="tel" inputmode="tel" autocomplete="tel"
        placeholder="۰۹۱۲۳۴۵۶۷۸۹" :maxlength="11" icon="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" :error="phoneError" @blur="phoneTouched = true" />
      <button type="submit" :disabled="isLoading || isDown" class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30">
        <span v-if="!isLoading">ارسال کد</span>
        <span v-else class="flex items-center justify-center gap-2"><svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> در حال ارسال…</span>
      </button>
    </form>

    <form v-else @submit.prevent="handleReset" class="space-y-5" novalidate>
      <AuthField id="code" v-model="verificationCode" label="کد ۶ رقمی" inputmode="numeric" autocomplete="one-time-code"
        placeholder="۱۲۳۴۵۶" :maxlength="6" icon="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
      <AuthField id="new-password" v-model="newPassword" label="رمز عبور جدید" type="password" autocomplete="new-password"
        placeholder="رمز عبور جدید" icon="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
        <PasswordChecklist :rules="rules" />
      </AuthField>
      <button type="submit" :disabled="isLoading || isDown || done" class="w-full py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-500/30">
        <span v-if="!isLoading">تغییر رمز عبور</span>
        <span v-else class="flex items-center justify-center gap-2"><svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> در حال تغییر…</span>
      </button>
      <button type="button" @click="backToStep1" class="w-full text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors">ویرایش شماره یا ارسال مجدد کد</button>
    </form>

    <p class="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
      <router-link to="/login" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition-colors">بازگشت به ورود</router-link>
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
const { forgotPassword, resetPassword, isLoading } = useAuth();
const { isDown, check } = useConnection();

const step = ref(1);
const phoneNumber = ref('');
const verificationCode = ref('');
const newPassword = ref('');
const phoneTouched = ref(false);
const errorMessage = ref('');
const infoMessage = ref('');
const done = ref(false);

const { rules, isValid: isPasswordValid } = usePasswordRules(newPassword);

watch(phoneNumber, (v) => { const n = normalizeDigits(v).replace(/\D/g, ''); if (n !== v) phoneNumber.value = n; });
watch(verificationCode, (v) => { const n = normalizeDigits(v).replace(/\D/g, ''); if (n !== v) verificationCode.value = n; });

const phoneError = computed(() =>
  phoneTouched.value && phoneNumber.value && !isValidPhone(phoneNumber.value)
    ? 'شمارهٔ موبایل باید ۱۱ رقم باشد و با ۰۹ شروع شود' : '');

const alertData = computed(() => (errorMessage.value ? friendlyAuthError(errorMessage.value, 'reset') : null));

const backToStep1 = () => { step.value = 1; errorMessage.value = ''; infoMessage.value = ''; verificationCode.value = ''; newPassword.value = ''; };

const handleSendCode = async () => {
  errorMessage.value = '';
  phoneTouched.value = true;
  if (!isValidPhone(phoneNumber.value)) return;
  if (isDown.value && !(await check())) return;

  const r = await forgotPassword(phoneNumber.value);
  if (r.success) {
    infoMessage.value = 'کد ۶ رقمی برای شمارهٔ ' + phoneNumber.value + ' پیامک شد.';
    step.value = 2;
  } else {
    errorMessage.value = r.message;
  }
};

const handleReset = async () => {
  errorMessage.value = '';
  if (verificationCode.value.length !== 6) { errorMessage.value = 'کد ۶ رقمی پیامک‌شده را کامل وارد کنید.'; return; }
  if (!isPasswordValid.value) { errorMessage.value = 'رمز عبور جدید هنوز همهٔ شرایط زیر فیلد را ندارد.'; return; }

  const r = await resetPassword(phoneNumber.value, verificationCode.value, newPassword.value);
  if (r.success) {
    infoMessage.value = '';
    done.value = true;
    setTimeout(() => router.push('/login'), 2000);
  } else {
    errorMessage.value = r.message;
  }
};

onMounted(check);
</script>
