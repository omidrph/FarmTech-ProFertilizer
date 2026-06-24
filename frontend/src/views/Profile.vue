<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200">
    <!-- هدر صفحه -->
    <div class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- دکمه بازگشت -->
          <button
            @click="goBack"
            class="flex items-center gap-2 px-3 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            <span class="text-sm font-medium">بازگشت</span>
          </button>

          <h1 class="text-lg font-bold text-gray-900 dark:text-white">پروفایل کاربری</h1>

          <!-- دکمه خروج -->
          <button
            @click="handleLogout"
            class="flex items-center gap-1.5 px-3 py-2 text-danger-600 hover:text-danger-700 dark:text-danger-400 dark:hover:text-danger-300 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span class="text-sm font-medium hidden sm:inline">خروج</span>
          </button>
        </div>
      </div>
    </div>

    <!-- محتوای صفحه -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      
      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-16">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">در حال بارگذاری اطلاعات...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
        <p class="text-danger-700 dark:text-danger-400">{{ error }}</p>
        <button @click="loadUserData" class="mt-2 px-4 py-2 bg-danger-600 text-white rounded-lg hover:bg-danger-700 transition-colors text-sm">
          تلاش مجدد
        </button>
      </div>

      <!-- User Data -->
      <div v-else-if="user" class="space-y-6">
        
        <!-- کارت اطلاعات کاربر -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          
          <!-- هدر کارت با گرادیانت -->
          <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-6 py-8">
            <div class="flex items-center gap-4">
              <!-- آواتار -->
              <div class="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-white/20 backdrop-blur-sm border-4 border-white/30 flex items-center justify-center text-white text-3xl sm:text-4xl font-bold shadow-lg">
                {{ userInitials }}
              </div>
              <div class="flex-1">
                <h2 class="text-xl sm:text-2xl font-bold text-white mb-1">
                  {{ user.full_name || `${user.first_name} ${user.last_name}` }}
                </h2>
                <p class="text-primary-100 text-sm flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  {{ user.phone_number }}
                </p>
                <div class="flex items-center gap-2 mt-2">
                  <span class="px-2 py-0.5 bg-white/20 backdrop-blur-sm rounded-full text-xs text-white">
                    {{ user.is_active ? '✅ فعال' : '❌ غیرفعال' }}
                  </span>
                  <span class="px-2 py-0.5 bg-white/20 backdrop-blur-sm rounded-full text-xs text-white">
                    📅 عضویت: {{ formatDate(user.created_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- بدنه کارت -->
          <div class="p-6">
            <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              اطلاعات شخصی
            </h3>

            <!-- فرم ویرایش -->
            <form @submit.prevent="handleUpdateProfile" class="space-y-4">
              
              <!-- نام و نام خانوادگی -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                    نام
                  </label>
                  <input
                    type="text"
                    v-model="editForm.first_name"
                    required
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                    نام خانوادگی
                  </label>
                  <input
                    type="text"
                    v-model="editForm.last_name"
                    required
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>
              </div>

              <!-- شماره تلفن (غیرقابل ویرایش) -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  شماره تلفن
                </label>
                <input
                  type="tel"
                  :value="user.phone_number"
                  disabled
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 cursor-not-allowed"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                  شماره تلفن قابل تغییر نیست
                </p>
              </div>

              <!-- دکمه ذخیره -->
              <div class="flex gap-3 pt-2">
                <button
                  type="submit"
                  :disabled="isSaving"
                  class="flex-1 px-4 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <svg v-if="!isSaving" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  <svg v-else class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  {{ isSaving ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}
                </button>
                <button
                  type="button"
                  @click="resetForm"
                  class="px-4 py-2.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                >
                  انصراف
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- کارت تغییر رمز عبور -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
            <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              تغییر رمز عبور
            </h3>
          </div>

          <div class="p-6">
            <form @submit.prevent="handleChangePassword" class="space-y-4">
              
              <!-- رمز عبور فعلی -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  رمز عبور فعلی
                </label>
                <input
                  type="password"
                  v-model="passwordForm.current_password"
                  required
                  minlength="6"
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>

              <!-- رمز عبور جدید -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  رمز عبور جدید
                </label>
                <input
                  type="password"
                  v-model="passwordForm.new_password"
                  required
                  minlength="6"
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">حداقل ۶ کاراکتر</p>
              </div>

              <!-- تکرار رمز عبور جدید -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  تکرار رمز عبور جدید
                </label>
                <input
                  type="password"
                  v-model="passwordForm.confirm_password"
                  required
                  minlength="6"
                  class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>

              <!-- دکمه تغییر رمز -->
              <button
                type="submit"
                :disabled="isChangingPassword"
                class="w-full px-4 py-2.5 bg-warning-600 text-white rounded-lg hover:bg-warning-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <svg v-if="!isChangingPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                <svg v-else class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ isChangingPassword ? 'در حال تغییر...' : 'تغییر رمز عبور' }}
              </button>
            </form>
          </div>
        </div>

        <!-- کارت آمار فعالیت -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
            <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              آمار فعالیت
            </h3>
          </div>

          <div class="p-6">
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="text-2xl font-bold text-primary-600 dark:text-primary-400 tabular-nums">
                  {{ stats.reports }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">گزارش‌ها</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="text-2xl font-bold text-success-600 dark:text-success-400 tabular-nums">
                  {{ stats.fertilizers }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">کودهای شخصی</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="text-2xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">
                  {{ stats.calculations }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">محاسبات</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div class="text-2xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">
                  {{ stats.days }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">روز عضویت</div>
              </div>
            </div>
          </div>
        </div>

        <!-- پیام موفقیت -->
        <Transition name="fade">
          <div v-if="successMessage" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-4">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <p class="text-success-700 dark:text-success-400 text-sm">{{ successMessage }}</p>
            </div>
          </div>
        </Transition>

        <!-- پیام خطا -->
        <Transition name="fade">
          <div v-if="errorMessage" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <div class="flex-1">
                <p class="text-danger-700 dark:text-danger-400 text-sm">{{ errorMessage }}</p>
                <button @click="errorMessage = null" class="text-xs text-danger-600 hover:text-danger-800 dark:hover:text-danger-300 mt-1 underline">
                  بستن
                </button>
              </div>
            </div>
          </div>
        </Transition>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { apiService } from '@/services/apiService';

const router = useRouter();
const { user, logout, checkAuth } = useAuth();

// ===== State =====
const isLoading = ref(true);
const isSaving = ref(false);
const isChangingPassword = ref(false);
const error = ref<string | null>(null);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

const stats = reactive({
  reports: 0,
  fertilizers: 0,
  calculations: 0,
  days: 0
});

const editForm = reactive({
  first_name: '',
  last_name: ''
});

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
});

// ===== Computed =====
const userInitials = computed(() => {
  if (user.value) {
    const first = user.value.first_name?.charAt(0) || '';
    const last = user.value.last_name?.charAt(0) || '';
    return (first + last).toUpperCase();
  }
  return '👤';
});

// ===== Methods =====
const goBack = () => {
  router.push('/');
};

const handleLogout = async () => {
  if (confirm('آیا از خروج از حساب خود اطمینان دارید؟')) {
    logout();
    await router.push('/login');
  }
};

const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('fa-IR');
  } catch {
    return 'نامشخص';
  }
};

const resetForm = () => {
  if (user.value) {
    editForm.first_name = user.value.first_name;
    editForm.last_name = user.value.last_name;
  }
};

const loadUserData = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    await checkAuth();
    
    if (user.value) {
      resetForm();
      
      // بارگذاری آمار
      try {
        const [reports, fertilizers] = await Promise.all([
          apiService.getReports().catch(() => []),
          apiService.getFertilizers().catch(() => [])
        ]);
        
        stats.reports = Array.isArray(reports) ? reports.length : 0;
        stats.fertilizers = Array.isArray(fertilizers) 
          ? fertilizers.filter((f: any) => !f.is_system_default).length 
          : 0;
        stats.calculations = 0; // TODO: از API بگیر
        
        // محاسبه روزهای عضویت
        const createdDate = new Date(user.value.created_at);
        const today = new Date();
        const diffTime = Math.abs(today.getTime() - createdDate.getTime());
        stats.days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
      } catch (err) {
        console.warn('خطا در بارگذاری آمار:', err);
      }
    }
  } catch (err: any) {
    error.value = err.message || 'خطا در بارگذاری اطلاعات کاربر';
  } finally {
    isLoading.value = false;
  }
};

const handleUpdateProfile = async () => {
  isSaving.value = true;
  errorMessage.value = null;
  successMessage.value = null;
  
  try {
    const result = await apiService.put('/users/me', {
      first_name: editForm.first_name,
      last_name: editForm.last_name
    });
    
    if (result) {
      successMessage.value = '✅ اطلاعات با موفقیت به‌روزرسانی شد';
      await checkAuth(); // به‌روزرسانی اطلاعات کاربر
      
      setTimeout(() => {
        successMessage.value = null;
      }, 3000);
    }
  } catch (err: any) {
    errorMessage.value = err.response?.data?.detail || 'خطا در به‌روزرسانی اطلاعات';
  } finally {
    isSaving.value = false;
  }
};

const handleChangePassword = async () => {
  // بررسی تطابق رمزهای جدید
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    errorMessage.value = 'رمز عبور جدید و تکرار آن مطابقت ندارند';
    return;
  }
  
  if (passwordForm.new_password.length < 6) {
    errorMessage.value = 'رمز عبور جدید باید حداقل ۶ کاراکتر باشد';
    return;
  }
  
  isChangingPassword.value = true;
  errorMessage.value = null;
  successMessage.value = null;
  
  try {
    // TODO: این endpoint باید در بک‌اند پیاده‌سازی شود
    // فعلاً فقط یک پیام نمایش می‌دهیم
    alert('قابلیت تغییر رمز عبور به زودی اضافه خواهد شد');
    
    // پاک کردن فرم
    passwordForm.current_password = '';
    passwordForm.new_password = '';
    passwordForm.confirm_password = '';
    
  } catch (err: any) {
    errorMessage.value = err.response?.data?.detail || 'خطا در تغییر رمز عبور';
  } finally {
    isChangingPassword.value = false;
  }
};

// ===== Lifecycle =====
onMounted(() => {
  loadUserData();
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

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>