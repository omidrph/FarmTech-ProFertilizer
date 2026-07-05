<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-[100] overflow-y-auto"
        role="dialog"
        aria-modal="true"
      >
        <!-- Backdrop -->
        <div
          class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity"
          @click="closeModal"
        ></div>

        <!-- Modal Container -->
        <div
          class="flex min-h-full items-center justify-center p-0 sm:p-4"
        >
          <div
            class="relative w-full h-full sm:h-auto sm:max-w-3xl sm:my-8 bg-white dark:bg-gray-800 sm:rounded-2xl shadow-2xl overflow-hidden"
          >
            <!-- Loading State -->
            <div v-if="isLoadingUser" class="flex flex-col items-center justify-center py-20">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              <p class="mt-4 text-gray-600 dark:text-gray-400">در حال بارگذاری اطلاعات کاربر...</p>
            </div>

            <!-- User Data -->
            <template v-else-if="currentUser">
              <!-- Header -->
              <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-6 py-6">
                <div class="flex items-start justify-between">
                  <div class="flex items-center gap-4">
                    <!-- Avatar -->
                    <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-white/20 backdrop-blur-sm border-4 border-white/30 flex items-center justify-center text-white text-2xl sm:text-3xl font-bold shadow-lg">
                      {{ userInitials }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <h2 class="text-lg sm:text-xl font-bold text-white truncate">
                        {{ currentUser.full_name || `${currentUser.first_name} ${currentUser.last_name}` }}
                      </h2>
                      <p class="text-primary-100 text-sm flex items-center gap-2 mt-1">
                        <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                        </svg>
                        <span class="truncate">{{ currentUser.phone_number }}</span>
                      </p>
                      <div class="flex items-center gap-2 mt-2 flex-wrap">
                        <span class="px-2 py-0.5 bg-white/20 backdrop-blur-sm rounded-full text-xs text-white flex items-center gap-1">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                          </svg>
                          {{ currentUser.is_active ? 'فعال' : 'غیرفعال' }}
                        </span>
                        <span class="px-2 py-0.5 bg-white/20 backdrop-blur-sm rounded-full text-xs text-white flex items-center gap-1">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                          </svg>
                          عضویت: {{ formatDate(currentUser.created_at) }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <button
                    @click="closeModal"
                    class="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Tabs -->
              <div class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
                <div class="flex overflow-x-auto scrollbar-hide">
                  <button
                    v-for="tab in tabs"
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    class="flex items-center gap-2 px-4 sm:px-6 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors flex-shrink-0"
                    :class="activeTab === tab.id
                      ? 'border-primary-500 text-primary-600 dark:text-primary-400 bg-white dark:bg-gray-800'
                      : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
                  >
                    <div v-html="tab.icon" class="w-4 h-4"></div>
                    <span>{{ tab.label }}</span>
                  </button>
                </div>
              </div>

              <!-- Tab Content -->
              <div class="max-h-[calc(100vh-320px)] sm:max-h-[500px] overflow-y-auto custom-scrollbar">

                <!-- Profile Tab -->
                <div v-if="activeTab === 'profile'" class="p-6">
                  <form @submit.prevent="handleUpdateProfile" class="space-y-4">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                          </svg>
                          نام
                        </label>
                        <input
                          type="text"
                          v-model="profileForm.first_name"
                          required
                          class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                          </svg>
                          نام خانوادگی
                        </label>
                        <input
                          type="text"
                          v-model="profileForm.last_name"
                          required
                          class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        />
                      </div>
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                        </svg>
                        شماره تلفن
                      </label>
                      <input
                        type="tel"
                        :value="currentUser.phone_number"
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
                        @click="resetProfileForm"
                        class="px-4 py-2.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                      >
                        انصراف
                      </button>
                    </div>
                  </form>
                </div>

                <!-- Security Tab -->
                <div v-if="activeTab === 'security'" class="p-6">
                  <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-3 mb-4">
                    <div class="flex items-start gap-2">
                      <svg class="w-5 h-5 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <p class="text-sm text-primary-700 dark:text-primary-300">
                        برای تغییر رمز عبور، ابتدا رمز فعلی و سپس رمز جدید را وارد کنید. رمز عبور باید حداقل ۶ کاراکتر باشد.
                      </p>
                    </div>
                  </div>

                  <form @submit.prevent="handleChangePassword" class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                        </svg>
                        رمز عبور فعلی
                      </label>
                      <div class="relative">
                        <input
                          :type="showCurrentPassword ? 'text' : 'password'"
                          v-model="passwordForm.current_password"
                          required
                          minlength="6"
                          class="w-full px-4 py-2.5 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="رمز عبور فعلی را وارد کنید"
                        />
                        <button
                          type="button"
                          @click="showCurrentPassword = !showCurrentPassword"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                        >
                          <svg v-if="!showCurrentPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                          </svg>
                          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                          </svg>
                        </button>
                      </div>
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                        </svg>
                        رمز عبور جدید
                      </label>
                      <div class="relative">
                        <input
                          :type="showNewPassword ? 'text' : 'password'"
                          v-model="passwordForm.new_password"
                          required
                          minlength="6"
                          class="w-full px-4 py-2.5 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="حداقل ۶ کاراکتر"
                        />
                        <button
                          type="button"
                          @click="showNewPassword = !showNewPassword"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                        >
                          <svg v-if="!showNewPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                          </svg>
                          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                          </svg>
                        </button>
                      </div>
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5 flex items-center gap-1.5">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                        تکرار رمز عبور جدید
                      </label>
                      <input
                        type="password"
                        v-model="passwordForm.confirm_password"
                        required
                        minlength="6"
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        placeholder="رمز عبور جدید را دوباره وارد کنید"
                      />
                    </div>

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

                <!-- Stats Tab -->
                <div v-if="activeTab === 'stats'" class="p-6">
                  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 text-center border border-gray-200 dark:border-gray-600">
                      <div class="w-10 h-10 mx-auto mb-2 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                      </div>
                      <div class="text-2xl font-bold text-primary-600 dark:text-primary-400 tabular-nums">{{ stats.reports }}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">گزارش‌ها</div>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 text-center border border-gray-200 dark:border-gray-600">
                      <div class="w-10 h-10 mx-auto mb-2 rounded-lg bg-success-100 dark:bg-success-900/30 flex items-center justify-center">
                        <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                        </svg>
                      </div>
                      <div class="text-2xl font-bold text-success-600 dark:text-success-400 tabular-nums">{{ stats.fertilizers }}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">کودهای شخصی</div>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 text-center border border-gray-200 dark:border-gray-600">
                      <div class="w-10 h-10 mx-auto mb-2 rounded-lg bg-warning-100 dark:bg-warning-900/30 flex items-center justify-center">
                        <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                      </div>
                      <div class="text-2xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ stats.calculations }}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">محاسبات</div>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 text-center border border-gray-200 dark:border-gray-600">
                      <div class="w-10 h-10 mx-auto mb-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                        <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                      </div>
                      <div class="text-2xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">{{ stats.days }}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">روز عضویت</div>
                    </div>
                  </div>

                  <div class="mt-6 bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
                    <div class="flex items-start gap-3">
                      <svg class="w-5 h-5 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                      </svg>
                      <div class="text-sm text-primary-700 dark:text-primary-300">
                        <p class="font-medium mb-1">آمار فعالیت شما</p>
                        <p class="text-xs text-primary-600 dark:text-primary-400">
                          این آمار بر اساس داده‌های ذخیره شده در حساب کاربری شما محاسبه می‌شود.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Reports Tab -->
                <div v-if="activeTab === 'reports'" class="p-6">
                  <!-- Header -->
                  <div class="flex items-center gap-3 mb-4 pb-3 border-b border-gray-200 dark:border-gray-700">
                    <div class="w-9 h-9 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                      <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-base font-bold text-gray-900 dark:text-white">
                        گزارش‌های ذخیره شده
                      </h3>
                      <p class="text-xs text-gray-500 dark:text-gray-400">
                        لیست تمام گزارش‌های ذخیره شده شما
                      </p>
                    </div>
                    <button
                      @click="loadReports"
                      :disabled="isLoadingReports"
                      class="mr-auto p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      title="بروزرسانی"
                    >
                      <svg v-if="!isLoadingReports" class="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                      </svg>
                      <svg v-else class="w-4 h-4 animate-spin text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                    </button>
                  </div>

                  <!-- لیست گزارش‌ها -->
                  <div v-if="reports.length > 0" class="space-y-2">
                    <div
                      v-for="report in reports"
                      :key="report.id"
                      class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors group"
                    >
                      <div class="flex-1 min-w-0">
                        <p class="font-medium text-gray-900 dark:text-white truncate">{{ report.report_name || 'بدون نام' }}</p>
                        <div class="flex items-center gap-3 mt-1 text-xs text-gray-500 dark:text-gray-400 flex-wrap">
                          <span v-if="report.plant_name" class="flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                            </svg>
                            {{ report.plant_name }}
                          </span>
                          <span v-if="report.season" class="flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
                            </svg>
                            {{ report.season }}
                          </span>
                          <span v-if="report.growth_stage" class="flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                            </svg>
                            {{ report.growth_stage }}
                          </span>
                          <span class="flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                            </svg>
                            {{ formatDate(report.created_at) }}
                          </span>
                        </div>
                      </div>
                      <div class="flex items-center gap-2 flex-shrink-0">
                        <button
                          @click="loadReport(report.id)"
                          :disabled="isLoadingReport"
                          class="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs flex items-center gap-1 shadow-sm hover:shadow-md disabled:opacity-50"
                        >
                          <svg v-if="isLoadingReport && loadingReportId === report.id" class="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                          </svg>
                          <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                          </svg>
                          <span>بارگذاری</span>
                        </button>
                        <!-- ✅ فقط اینجا confirm دارد -->
                        <button
                          @click="deleteReport(report.id)"
                          class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors opacity-0 group-hover:opacity-100 sm:opacity-100"
                          title="حذف"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- حالت خالی -->
                  <div v-else class="text-center py-12">
                    <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                      <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <p class="text-gray-500 dark:text-gray-400 mb-2">هنوز گزارشی ذخیره نشده است</p>
                    <p class="text-xs text-gray-400 dark:text-gray-500">
                      برای ذخیره گزارش فعلی، از منوی <span class="font-medium text-primary-600 dark:text-primary-400">فایل → ذخیره</span> استفاده کنید
                    </p>
                  </div>
                </div>

              </div>

              <!-- Messages -->
              <Transition name="fade">
                <div v-if="successMessage" class="absolute bottom-4 left-4 right-4 bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-3 z-10">
                  <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-success-600 dark:text-success-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    <p class="text-success-700 dark:text-success-400 text-sm">{{ successMessage }}</p>
                  </div>
                </div>
              </Transition>

              <Transition name="fade">
                <div v-if="errorMessage" class="absolute bottom-4 left-4 right-4 bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-3 z-10">
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
            </template>

            <!-- Error State -->
            <div v-else class="flex flex-col items-center justify-center py-20">
              <svg class="w-16 h-16 text-danger-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <p class="text-danger-700 dark:text-danger-400 mb-4">خطا در بارگذاری اطلاعات کاربر</p>
              <button @click="loadUserData" class="px-4 py-2 bg-danger-600 text-white rounded-lg hover:bg-danger-700 transition-colors">
                تلاش مجدد
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useAuth } from '@/composables/useAuth';
import { apiService } from '@/services/apiService';
import { useReportStore } from '@/store/modules/reportStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useCalcStore } from '@/store/modules/calcStore';

// ===== Props & Emits =====
interface Props {
  isOpen: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
}>();

// ===== Stores =====
const reportStore = useReportStore();
const waterStore = useWaterStore();
const targetStore = useTargetStore();
const calcStore = useCalcStore();

// ===== State =====
const { user, checkAuth } = useAuth();

const currentUser = ref<any>(null);
const isLoadingUser = ref(false);
const activeTab = ref<'profile' | 'security' | 'stats' | 'reports'>('profile');
const isSaving = ref(false);
const isChangingPassword = ref(false);
const isLoadingReports = ref(false);
const isLoadingReport = ref(false);
const loadingReportId = ref<number | null>(null);
const successMessage = ref<string | null>(null);
const errorMessage = ref<string | null>(null);

const showCurrentPassword = ref(false);
const showNewPassword = ref(false);

const reports = ref<any[]>([]);

const stats = reactive({
  reports: 0,
  fertilizers: 0,
  calculations: 0,
  days: 0
});

const profileForm = reactive({
  first_name: '',
  last_name: ''
});

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
});

// ===== Tabs Definition =====
const tabs = [
  {
    id: 'profile' as const,
    label: 'اطلاعات کاربری',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`
  },
  {
    id: 'security' as const,
    label: 'امنیت',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>`
  },
  {
    id: 'stats' as const,
    label: 'آمار',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`
  },
  {
    id: 'reports' as const,
    label: 'گزارش‌ها',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>`
  }
];

// ===== Computed =====
const userInitials = computed(() => {
  if (currentUser.value) {
    const first = currentUser.value.first_name?.charAt(0) || '';
    const last = currentUser.value.last_name?.charAt(0) || '';
    return (first + last).toUpperCase();
  }
  return '?';
});

// ===== Methods =====
const closeModal = () => {
  emit('update:isOpen', false);
  setTimeout(() => {
    successMessage.value = null;
    errorMessage.value = null;
  }, 300);
};

const formatDate = (dateString: string | undefined): string => {
  if (!dateString) return 'نامشخص';
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('fa-IR');
  } catch {
    return 'نامشخص';
  }
};

const resetProfileForm = () => {
  if (currentUser.value) {
    profileForm.first_name = currentUser.value.first_name || '';
    profileForm.last_name = currentUser.value.last_name || '';
  }
};

const resetPasswordForm = () => {
  passwordForm.current_password = '';
  passwordForm.new_password = '';
  passwordForm.confirm_password = '';
};

const showSuccess = (message: string) => {
  successMessage.value = message;
  setTimeout(() => {
    successMessage.value = null;
  }, 3000);
};

const showError = (message: string) => {
  errorMessage.value = message;
};

const loadUserData = async () => {
  isLoadingUser.value = true;
  errorMessage.value = null;
  
  try {
    await checkAuth();
    
    if (user.value) {
      currentUser.value = user.value;
      resetProfileForm();
      await loadStats();
    } else {
      showError('اطلاعات کاربر در دسترس نیست');
    }
  } catch (err: any) {
    showError(err.message || 'خطا در بارگذاری اطلاعات کاربر');
    console.error('Error loading user data:', err);
  } finally {
    isLoadingUser.value = false;
  }
};

const loadStats = async () => {
  try {
    const [reportsData, fertilizers] = await Promise.all([
      apiService.getReports().catch(() => []),
      apiService.getFertilizers().catch(() => [])
    ]);

    reports.value = Array.isArray(reportsData) ? reportsData : [];
    stats.reports = reports.value.length;
    stats.fertilizers = Array.isArray(fertilizers)
      ? fertilizers.filter((f: any) => !f.is_system_default).length
      : 0;
    stats.calculations = 0;

    if (currentUser.value?.created_at) {
      const createdDate = new Date(currentUser.value.created_at);
      const today = new Date();
      const diffTime = Math.abs(today.getTime() - createdDate.getTime());
      stats.days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
  } catch (err) {
    console.warn('خطا در بارگذاری آمار:', err);
  }
};

const loadReports = async () => {
  isLoadingReports.value = true;
  try {
    const data = await apiService.getReports();
    reports.value = Array.isArray(data) ? data : [];
    stats.reports = reports.value.length;
  } catch (err) {
    console.error('خطا در بارگذاری گزارش‌ها:', err);
  } finally {
    isLoadingReports.value = false;
  }
};

const handleUpdateProfile = async () => {
  isSaving.value = true;
  errorMessage.value = null;
  successMessage.value = null;

  try {
    const result = await apiService.put('/users/me', {
      first_name: profileForm.first_name,
      last_name: profileForm.last_name
    });

    if (result) {
      currentUser.value = result;
      showSuccess('اطلاعات با موفقیت به‌روزرسانی شد');
      await checkAuth();
    }
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || err.message || 'خطا در به‌روزرسانی اطلاعات';
    showError(errorMsg);
    console.error('Error updating profile:', err);
  } finally {
    isSaving.value = false;
  }
};

const handleChangePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    showError('رمز عبور جدید و تکرار آن مطابقت ندارند');
    return;
  }

  if (passwordForm.new_password.length < 6) {
    showError('رمز عبور جدید باید حداقل ۶ کاراکتر باشد');
    return;
  }

  if (!passwordForm.current_password) {
    showError('لطفاً رمز عبور فعلی را وارد کنید');
    return;
  }

  isChangingPassword.value = true;
  errorMessage.value = null;
  successMessage.value = null;

  try {
    const result = await apiService.post('/auth/change-password', {
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    });

    if (result.success) {
      showSuccess('رمز عبور با موفقیت تغییر کرد');
      resetPasswordForm();
    }
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || err.message || 'خطا در تغییر رمز عبور';
    showError(errorMsg);
    console.error('Error changing password:', err);
  } finally {
    isChangingPassword.value = false;
  }
};

// ============================================================
// ✅ loadReport - بدون confirm (الگو گرفته از AppHeader)
// ============================================================
const loadReport = async (reportId: number) => {
  // ❌ حذف کامل confirm
  // if (reportStore.hasActiveReport && reportStore.currentReportId !== reportId) {
  //   if (!confirm('آیا می‌خواهید گزارش دیگری را بارگذاری کنید؟')) {
  //     return;
  //   }
  // }
  
  isLoadingReport.value = true;
  loadingReportId.value = reportId;
  
  try {
    const success = await reportStore.loadReport(reportId);
    if (success) {
      showSuccess('گزارش با موفقیت بارگذاری شد');
      setTimeout(() => {
        closeModal();
      }, 1000);
    } else {
      showError(reportStore.error || 'خطا در بارگذاری گزارش');
    }
  } catch (err: any) {
    showError(err.response?.data?.detail || 'خطا در بارگذاری گزارش');
    console.error('Error loading report:', err);
  } finally {
    isLoadingReport.value = false;
    loadingReportId.value = null;
  }
};

// ============================================================
// ✅ deleteReport - فقط اینجا confirm دارد
// ============================================================
const deleteReport = async (reportId: number) => {
  if (!confirm('آیا از حذف این گزارش اطمینان دارید؟ این عملیات غیرقابل بازگشت است.')) {
    return;
  }
  
  try {
    const success = await reportStore.deleteReport(reportId);
    if (success) {
      reports.value = reports.value.filter(r => r.id !== reportId);
      stats.reports = reports.value.length;
      showSuccess('گزارش با موفقیت حذف شد');
      
      if (reportStore.currentReportId === reportId) {
        waterStore.resetWaterData();
        targetStore.resetTargets();
        calcStore.resetCalculation();
        window.dispatchEvent(new CustomEvent('report-changed'));
        window.dispatchEvent(new CustomEvent('report-reset'));
      }
    } else {
      showError(reportStore.error || 'خطا در حذف گزارش');
    }
  } catch (err: any) {
    showError(err.response?.data?.detail || 'خطا در حذف گزارش');
    console.error('Error deleting report:', err);
  }
};

// ===== Watchers =====
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    loadUserData();
    activeTab.value = 'profile';
  }
});

// ===== Lifecycle =====
onMounted(() => {
  if (props.isOpen) {
    loadUserData();
  }
});
</script>

<style scoped>
/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(20px);
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

/* Scrollbar Hide */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Tabular Nums */
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* Spin Animation */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>