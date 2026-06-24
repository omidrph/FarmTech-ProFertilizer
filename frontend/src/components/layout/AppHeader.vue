<template>
  <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50 transition-colors duration-200">
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
      <div class="flex items-center justify-between h-16 sm:h-20 lg:h-24">
        
        <!-- Logo -->
        <div class="flex items-center gap-3 sm:gap-4 flex-shrink-0">
          <img
            src="/Logo.webp"
            alt="FarmTech"
            class="h-10 w-10 sm:h-14 sm:w-14 lg:h-16 lg:w-16 object-contain rounded-lg"
          />
          <div class="flex flex-col leading-tight">
            <h1 class="text-sm sm:text-base lg:text-xl font-bold text-gray-800 dark:text-white tracking-tight">
              FarmTech
            </h1>
            <p class="text-[10px] sm:text-xs text-gray-500 dark:text-gray-400 hidden sm:block">
              ProFertilizer
            </p>
          </div>
        </div>

        <!-- Mobile Menu Toggle -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          aria-label="منو"
        >
          <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Desktop Actions -->
        <div class="hidden lg:flex items-center gap-1 lg:gap-2">
          
          <!-- File Menu -->
          <div class="relative" ref="fileMenuRef">
            <button
              @click="toggleFileMenu"
              class="flex items-center gap-1 lg:gap-2 px-2 lg:px-3 py-1.5 lg:py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 transition-all duration-200 text-xs lg:text-sm"
            >
              <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span class="hidden sm:inline">فایل</span>
              <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>

            <!-- File Dropdown -->
            <div
              v-if="fileMenuOpen"
              class="absolute left-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 py-1 z-50 overflow-hidden"
            >
              <button
                @click="handleNewReport"
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                <span>جدید</span>
                <span class="mr-auto text-xs text-gray-400">Ctrl+N</span>
              </button>

              <button
                @click="handleOpenReport"
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"/>
                </svg>
                <span>بازکردن...</span>
                <span class="mr-auto text-xs text-gray-400">Ctrl+O</span>
              </button>

              <button
                @click="handleSaveReport"
                :disabled="isSaving"
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
              >
                <svg v-if="!isSaving" class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
                </svg>
                <svg v-else class="w-4 h-4 animate-spin text-gray-500" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <span>ذخیره</span>
                <span class="mr-auto text-xs text-gray-400">Ctrl+S</span>
              </button>

              <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>

              <button
                @click="handleDeleteReport"
                :disabled="!reportStore.hasCurrentReport"
                class="flex items-center gap-3 w-full text-right px-4 py-2.5 text-sm text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                <span>حذف گزارش فعلی</span>
              </button>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <button
            v-for="tab in navTabs"
            :key="tab.id"
            @click="setActiveTab(tab.id)"
            class="flex items-center gap-1 lg:gap-2 px-2 lg:px-3 py-1.5 lg:py-2 rounded-lg transition-all duration-200 text-xs lg:text-sm"
            :class="currentActiveTab === tab.id
              ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
          >
            <span v-html="tab.icon"></span>
            <span class="hidden sm:inline">{{ tab.label }}</span>
          </button>

          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-1.5 lg:p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-all duration-200"
          >
            <svg v-if="isDarkMode" class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="mobileMenuOpen"
      class="lg:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-2 px-3 shadow-lg"
    >
      <div class="flex flex-col gap-1">
        
        <!-- File Menu (Mobile) -->
        <button
          @click="toggleFileMenuMobile"
          class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 transition-colors text-sm"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <span>فایل</span>
          <svg class="w-4 h-4 ml-auto transition-transform" :class="{ 'rotate-180': fileMenuOpenMobile }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>

        <div v-if="fileMenuOpenMobile" class="mr-6 space-y-1">
          <button @click="handleNewReport" class="flex items-center gap-2 w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            <span>جدید</span>
          </button>
          <button @click="handleOpenReport" class="flex items-center gap-2 w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"/>
            </svg>
            <span>بازکردن...</span>
          </button>
          <button @click="handleSaveReport" :disabled="isSaving" class="flex items-center gap-2 w-full text-right px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
            </svg>
            <span>{{ isSaving ? 'در حال ذخیره...' : 'ذخیره' }}</span>
          </button>
          <button @click="handleDeleteReport" :disabled="!reportStore.hasCurrentReport" class="flex items-center gap-2 w-full text-right px-3 py-2 text-sm text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors disabled:opacity-50">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            <span>حذف گزارش فعلی</span>
          </button>
        </div>

        <!-- Navigation Buttons (Mobile) -->
        <button
          v-for="tab in navTabs"
          :key="tab.id"
          @click="setActiveTab(tab.id); mobileMenuOpen = false"
          class="flex items-center gap-2 px-3 py-2 rounded-lg transition-all duration-200 text-sm"
          :class="currentActiveTab === tab.id
            ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
        >
          <span v-html="tab.icon"></span>
          <span>{{ tab.label }}</span>
        </button>

        <!-- Theme Toggle (Mobile) -->
        <button
          @click="toggleTheme"
          class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors text-sm"
        >
          <svg v-if="isDarkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
          <span>تغییر تم</span>
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- 🆕 مودال بازکردن گزارش -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="showOpenModal"
          class="fixed inset-0 z-[100] overflow-y-auto"
          role="dialog"
          aria-modal="true"
        >
          <!-- Backdrop -->
          <div
            class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity"
            @click="closeOpenModal"
          ></div>

          <!-- Modal Container -->
          <div class="flex min-h-full items-center justify-center p-0 sm:p-4">
            <div class="relative w-full h-full sm:h-auto sm:max-w-2xl sm:my-8 bg-white dark:bg-gray-800 sm:rounded-2xl shadow-2xl overflow-hidden">
              
              <!-- Header -->
              <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-6 py-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">بازکردن گزارش</h3>
                    <p class="text-xs text-primary-100">یک گزارش از لیست زیر انتخاب کنید</p>
                  </div>
                </div>
                <button
                  @click="closeOpenModal"
                  class="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>

              <!-- Search Bar -->
              <div class="px-6 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
                <div class="relative">
                  <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="جستجو در گزارش‌ها..."
                    class="w-full pr-10 pl-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>
              </div>

              <!-- Reports List -->
              <div class="max-h-[500px] overflow-y-auto custom-scrollbar">
                
                <!-- Loading State -->
                <div v-if="reportStore.isLoading" class="flex items-center justify-center py-12">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                  <span class="mr-2 text-gray-600 dark:text-gray-400">در حال بارگذاری...</span>
                </div>

                <!-- Empty State -->
                <div v-else-if="filteredReports.length === 0" class="text-center py-12">
                  <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                    <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-gray-500 dark:text-gray-400 mb-2">
                    {{ searchQuery ? 'گزارشی با این مشخصات پیدا نشد' : 'هنوز گزارشی ذخیره نشده است' }}
                  </p>
                  <p class="text-xs text-gray-400 dark:text-gray-500">
                    {{ searchQuery ? 'عبارت جستجو را تغییر دهید' : 'ابتدا یک گزارش جدید ایجاد و ذخیره کنید' }}
                  </p>
                </div>

                <!-- Reports -->
                <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
                  <div
                    v-for="report in filteredReports"
                    :key="report.id"
                    class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                    :class="{ 'bg-primary-50 dark:bg-primary-900/10': report.id === reportStore.currentReportId }"
                  >
                    <div class="flex items-start justify-between gap-3">
                      <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2 mb-1">
                          <h4 class="font-semibold text-gray-900 dark:text-white truncate">
                            {{ report.report_name || 'بدون نام' }}
                          </h4>
                          <span v-if="report.id === reportStore.currentReportId" class="px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full text-xs font-medium">
                            فعال
                          </span>
                        </div>
                        <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-500 dark:text-gray-400">
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
                          @click="loadSelectedReport(report.id)"
                          :disabled="isLoadingReport"
                          class="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs flex items-center gap-1 disabled:opacity-50"
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
                        <button
                          @click="deleteSelectedReport(report.id)"
                          class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                          title="حذف"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Footer -->
              <div class="px-6 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex items-center justify-between">
                <span class="text-xs text-gray-500 dark:text-gray-400">
                  {{ filteredReports.length }} گزارش
                </span>
                <button
                  @click="closeOpenModal"
                  class="px-4 py-1.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm"
                >
                  بستن
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ============================================================ -->
    <!-- پیام موفقیت/خطا -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="toastMessage"
          class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-2"
          :class="toastType === 'success' 
            ? 'bg-success-600 text-white' 
            : 'bg-danger-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useCalcStore } from '@/store/modules/calcStore';

// ===== Props =====
interface Props {
  activeTab?: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'update:activeTab', value: string): void;
  (e: 'new-report'): void;
}>();

// ===== Stores =====
const reportStore = useReportStore();
const waterStore = useWaterStore();
const targetStore = useTargetStore();
const calcStore = useCalcStore();

// ===== State =====
const isDarkMode = ref(false);
const fileMenuOpen = ref(false);
const fileMenuOpenMobile = ref(false);
const mobileMenuOpen = ref(false);
const fileMenuRef = ref<HTMLElement | null>(null);

const showOpenModal = ref(false);
const searchQuery = ref('');
const isLoadingReport = ref(false);
const loadingReportId = ref<number | null>(null);

const isSaving = ref(false);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

// ===== Computed =====
const currentActiveTab = computed(() => props.activeTab || 'home');

const filteredReports = computed(() => {
  if (!searchQuery.value.trim()) {
    return reportStore.reports;
  }
  const query = searchQuery.value.trim().toLowerCase();
  return reportStore.reports.filter(report =>
    (report.report_name?.toLowerCase().includes(query)) ||
    (report.plant_name?.toLowerCase().includes(query)) ||
    (report.season?.toLowerCase().includes(query)) ||
    (report.growth_stage?.toLowerCase().includes(query))
  );
});

// ===== Navigation Tabs =====
const navTabs = [
  {
    id: 'home',
    label: 'صفحه اصلی',
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
    </svg>`
  },
  {
    id: 'education',
    label: 'آموزش',
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
    </svg>`
  },
  {
    id: 'contact',
    label: 'ارتباط با ما',
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
    </svg>`
  },
  {
    id: 'about',
    label: 'درباره',
    icon: `<svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>`
  }
];

// ===== Methods =====
const setActiveTab = (tabId: string) => {
  emit('update:activeTab', tabId);
};

const toggleFileMenu = () => {
  fileMenuOpen.value = !fileMenuOpen.value;
  if (fileMenuOpen.value) {
    fileMenuOpenMobile.value = false;
  }
};

const toggleFileMenuMobile = () => {
  fileMenuOpenMobile.value = !fileMenuOpenMobile.value;
  if (fileMenuOpenMobile.value) {
    fileMenuOpen.value = false;
  }
};

const closeFileMenu = () => {
  fileMenuOpen.value = false;
  fileMenuOpenMobile.value = false;
};

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
};

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('fa-IR');
  } catch {
    return 'نامشخص';
  }
};

// ===== File Menu Actions =====
const handleNewReport = async () => {
  closeFileMenu();
  
  if (reportStore.hasCurrentReport) {
    if (!confirm('گزارش فعلی ذخیره نشده است. آیا مطمئن هستید که می‌خواهید گزارش جدید ایجاد کنید؟')) {
      return;
    }
  }
  
  // پاک کردن همه داده‌ها
  reportStore.resetReportData();
  waterStore.resetWaterData();
  targetStore.resetTargets();
  calcStore.resetCalculation();
  
  emit('new-report');
  showToast('گزارش جدید ایجاد شد', 'success');
};

const handleOpenReport = async () => {
  closeFileMenu();
  showOpenModal.value = true;
  searchQuery.value = '';
  await reportStore.loadReports();
};

const handleSaveReport = async () => {
  closeFileMenu();
  
  if (!reportStore.reportData.reportName && !reportStore.reportData.plantName) {
    showToast('لطفاً ابتدا اطلاعات گزارش را وارد کنید', 'error');
    return;
  }
  
  isSaving.value = true;
  const success = await reportStore.saveCurrentReport();
  isSaving.value = false;
  
  if (success) {
    showToast('گزارش با موفقیت ذخیره شد', 'success');
    await reportStore.loadReports();
  } else {
    showToast(reportStore.error || 'خطا در ذخیره گزارش', 'error');
  }
};

const handleDeleteReport = async () => {
  closeFileMenu();
  
  if (!reportStore.hasCurrentReport) {
    showToast('هیچ گزارشی برای حذف وجود ندارد', 'error');
    return;
  }
  
  if (!confirm('آیا از حذف گزارش فعلی اطمینان دارید؟ این عملیات غیرقابل بازگشت است.')) {
    return;
  }
  
  const success = await reportStore.deleteCurrentReport();
  if (success) {
    showToast('گزارش با موفقیت حذف شد', 'success');
    // پاک کردن داده‌های فعلی
    waterStore.resetWaterData();
    targetStore.resetTargets();
    calcStore.resetCalculation();
  } else {
    showToast(reportStore.error || 'خطا در حذف گزارش', 'error');
  }
};

const closeOpenModal = () => {
  showOpenModal.value = false;
  searchQuery.value = '';
};

const loadSelectedReport = async (reportId: number) => {
  if (reportStore.hasCurrentReport && reportStore.currentReportId !== reportId) {
    if (!confirm('گزارش فعلی ذخیره نشده است. آیا می‌خواهید گزارش دیگری را بارگذاری کنید؟')) {
      return;
    }
  }
  
  isLoadingReport.value = true;
  loadingReportId.value = reportId;
  
  const success = await reportStore.loadReport(reportId);
  
  isLoadingReport.value = false;
  loadingReportId.value = null;
  
  if (success) {
    showToast('گزارش با موفقیت بارگذاری شد', 'success');
    closeOpenModal();
  } else {
    showToast(reportStore.error || 'خطا در بارگذاری گزارش', 'error');
  }
};

const deleteSelectedReport = async (reportId: number) => {
  if (!confirm('آیا از حذف این گزارش اطمینان دارید؟')) {
    return;
  }
  
  const success = await reportStore.deleteReport(reportId);
  if (success) {
    showToast('گزارش با موفقیت حذف شد', 'success');
    if (reportStore.currentReportId === reportId) {
      waterStore.resetWaterData();
      targetStore.resetTargets();
      calcStore.resetCalculation();
    }
  } else {
    showToast(reportStore.error || 'خطا در حذف گزارش', 'error');
  }
};

// ===== Keyboard Shortcuts =====
const handleKeyboard = (event: KeyboardEvent) => {
  if (event.ctrlKey || event.metaKey) {
    switch (event.key.toLowerCase()) {
      case 'n':
        event.preventDefault();
        handleNewReport();
        break;
      case 'o':
        event.preventDefault();
        handleOpenReport();
        break;
      case 's':
        event.preventDefault();
        handleSaveReport();
        break;
    }
  }
};

// ===== Click Outside Handler =====
const handleClickOutside = (event: MouseEvent) => {
  if (fileMenuRef.value && !fileMenuRef.value.contains(event.target as Node)) {
    fileMenuOpen.value = false;
  }
};

// ===== Lifecycle =====
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  }
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleKeyboard);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleKeyboard);
});

// ===== Watch for mobile menu close on resize =====
watch(mobileMenuOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
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
  transform: translate(-50%, 10px);
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

/* Spin Animation */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>