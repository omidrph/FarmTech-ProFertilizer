<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات (آیکون حذف شد) -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
        اطلاعات مربوط به کودها در جدول زیر قابل مشاهده و ویرایش است. با فشردن دکمه "افزودن" می‌توانید کود جدید اضافه کنید.
        همچنین می‌توانید از دکمه "بارگذاری کودهای سیستمی" برای شروع سریع‌تر استفاده نمایید.
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- نوار ابزار (جستجو + دکمه‌ها) -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
        
        <!-- بخش راست: جستجو و فیلتر -->
        <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
          <!-- جستجو -->
          <div class="relative flex-1 min-w-[200px] max-w-md">
            <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="جستجوی نام کود یا برند..."
              class="w-full pr-10 pl-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
          
          <!-- فیلتر نوع -->
          <select
            v-model="filterType"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          >
            <option value="all">همه انواع</option>
            <option value="fertilizer">فقط کودها</option>
            <option value="acid">فقط اسیدها</option>
            <option value="system">کودهای سیستمی</option>
          </select>
        </div>

        <!-- بخش چپ: دکمه‌های عملیاتی -->
        <div class="flex flex-wrap gap-2 w-full lg:w-auto justify-end">
          <!-- 🆕 دکمه بارگذاری کودهای سیستمی -->
          <button
            @click="loadSystemFertilizers"
            :disabled="isLoading || hasSystemFertilizers"
            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2 shadow-sm hover:shadow-md"
            :title="hasSystemFertilizers ? 'کودهای سیستمی قبلاً بارگذاری شده‌اند' : 'بارگذاری ۴۲ کود پرکاربرد سیستمی برای شروع سریع'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
            {{ hasSystemFertilizers ? 'کودهای سیستمی موجود است' : 'بارگذاری کودهای سیستمی' }}
          </button>

          <!-- دکمه افزودن دستی -->
          <button
            @click="openAddModal"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            افزودن کود جدید
          </button>

          <!-- دکمه بروزرسانی -->
          <button
            @click="refreshFertilizers"
            :disabled="isLoading"
            class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <svg v-if="!isLoading" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            بروزرسانی
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- کارت‌های آماری -->
    <!-- ============================================================ -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کل کودها</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ fertilizers.length }}</p>
        </div>
      </div>
      
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کودهای معمولی</p>
          <p class="text-xl font-bold text-success-600 dark:text-success-400 tabular-nums">{{ normalFertilizersCount }}</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">اسیدها</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ acidFertilizersCount }}</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">سیستمی</p>
          <p class="text-xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">{{ systemFertilizersCount }}</p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام خالی بودن دیتابیس -->
    <!-- ============================================================ -->
    <div v-if="filteredFertilizers.length === 0 && !isLoading" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
        <svg class="w-10 h-10 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
      </div>
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {{ searchQuery || filterType !== 'all' ? 'نتیجه‌ای یافت نشد' : 'هیچ کودی در دیتابیس وجود ندارد' }}
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        {{ searchQuery || filterType !== 'all' ? 'لطفاً عبارت جستجو یا فیلتر را تغییر دهید.' : 'برای شروع، روی دکمه "بارگذاری کودهای سیستمی" کلیک کنید یا اولین کود خود را اضافه نمایید.' }}
      </p>
      <div class="mt-6 flex justify-center gap-3 flex-wrap">
        <button
          v-if="!searchQuery && filterType === 'all'"
          @click="loadSystemFertilizers"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
          بارگذاری سیستمی
        </button>
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          افزودن دستی
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول کودها -->
    <!-- ============================================================ -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- هدر جدول -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gray-50 dark:bg-gray-700/50">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">
            لیست کودها
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mr-2">({{ filteredFertilizers.length }} مورد)</span>
          </h3>
        </div>
      </div>
      
      <!-- جدول با اسکرول افقی -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700/50">
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[200px]">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                  نام کود / برند
                </div>
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
                <div class="flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  قیمت (تومان)
                </div>
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px]">
                <div class="flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
                  </svg>
                  نوع
                </div>
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[250px]">
                <div class="flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                  </svg>
                  عناصر تشکیل‌دهنده
                </div>
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px]">
                عملیات
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="fertilizer in filteredFertilizers"
              :key="fertilizer.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group"
            >
              <!-- نام کود -->
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-3 text-right">
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="fertilizer.isAcid ? 'bg-warning-50 dark:bg-warning-900/30' : fertilizer.isSystemDefault ? 'bg-indigo-50 dark:bg-indigo-900/30' : 'bg-primary-50 dark:bg-primary-900/30'"
                  >
                    <svg
                      class="w-5 h-5"
                      :class="fertilizer.isAcid ? 'text-warning-600 dark:text-warning-400' : fertilizer.isSystemDefault ? 'text-indigo-600 dark:text-indigo-400' : 'text-primary-600 dark:text-primary-400'"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path v-if="fertilizer.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                    <div class="flex items-center gap-2 mt-0.5 flex-wrap">
                      <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
                        {{ fertilizer.brand }}
                      </span>
                      <span v-if="fertilizer.isSystemDefault" class="text-[10px] text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 px-1.5 py-0.5 rounded border border-indigo-100 dark:border-indigo-800">
                        سیستمی
                      </span>
                    </div>
                  </div>
                </div>
              </td>
              
              <!-- قیمت -->
              <td class="px-4 py-3 text-center">
                <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                  {{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }}
                </span>
              </td>
              
              <!-- نوع -->
              <td class="px-4 py-3 text-center">
                <span
                  class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="fertilizer.isAcid
                    ? 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400'
                    : 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400'"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="fertilizer.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  {{ fertilizer.isAcid ? 'اسید' : 'کود' }}
                </span>
              </td>
              
              <!-- عناصر -->
              <td class="px-4 py-3">
                <div class="flex flex-wrap gap-1 justify-center">
                  <template v-if="hasElements(fertilizer)">
                    <span
                      v-for="(percentage, element) in getActiveElements(fertilizer)"
                      :key="element"
                      class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-600"
                      :title="`${element}: ${percentage}%`"
                    >
                      <span class="font-bold text-primary-600 dark:text-primary-400">{{ element }}</span>
                      <span class="mx-1 text-gray-400">|</span>
                      <span>{{ percentage }}%</span>
                    </span>
                  </template>
                  <span v-else class="text-xs text-gray-400 dark:text-gray-500 italic">بدون عنصر ثبت شده</span>
                </div>
              </td>
              
              <!-- عملیات -->
              <td class="px-4 py-3 text-center">
                <div class="flex items-center justify-center gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                  <button
                    @click="editFertilizer(fertilizer)"
                    class="p-1.5 rounded-lg text-primary-600 hover:text-primary-800 hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
                    title="ویرایش"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button
                    @click="deleteFertilizer(fertilizer.id, fertilizer.isSystemDefault)"
                    class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                    title="حذف"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مودال افزودن/ویرایش کود (بهبود یافته - بدون خطا) -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <div 
        v-if="showModal" 
        class="fixed inset-0 z-[100] overflow-y-auto"
        aria-labelledby="modal-title" 
        role="dialog" 
        aria-modal="true"
      >
        <!-- پس‌زمینه تاریک -->
        <div 
          class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity" 
          @click="closeModal"
        ></div>

        <!-- کانتینر مودال - دسکتاپ: وسط‌چین، موبایل: تمام صفحه -->
        <div class="flex min-h-full items-center justify-center p-0 sm:p-4 text-center sm:text-left">
          <div 
            class="relative transform overflow-hidden bg-white dark:bg-gray-800 text-right shadow-2xl transition-all w-full h-full sm:h-auto sm:my-8 sm:max-w-5xl sm:rounded-2xl"
          >
            <!-- هدر مودال -->
            <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-4 sm:px-6 py-4 flex items-center justify-between sticky top-0 z-10">
              <h3 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                {{ isEditing ? 'ویرایش کود' : 'افزودن کود جدید' }}
              </h3>
              <button 
                @click="closeModal" 
                class="text-white/80 hover:text-white transition-colors p-1 rounded-full hover:bg-white/10"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- بدنه مودال -->
            <div class="px-4 sm:px-6 py-5 max-h-[calc(100vh-140px)] sm:max-h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
                <!-- ستون راست: اطلاعات اصلی -->
                <div class="space-y-4">
                  <!-- نام کود -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      نام کود <span class="text-danger-500">*</span>
                    </label>
                    <input 
                      type="text" 
                      v-model="formData.name" 
                      placeholder="مثال: نیترات پتاسیم گرین استار" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>

                  <!-- برند و دسته‌بندی -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        برند / شرکت
                      </label>
                      <input 
                        type="text" 
                        list="brand-list"
                        v-model="formData.brand" 
                        placeholder="مثال: رازاک شیمی" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                      <datalist id="brand-list">
                        <option value="عمومی"></option>
                        <option value="رازاک شیمی"></option>
                        <option value="گل سم گرگان"></option>
                        <option value="اطلس"></option>
                        <option value="ردسا"></option>
                        <option value="کوالی مکس"></option>
                      </datalist>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        دسته‌بندی
                      </label>
                      <input 
                        type="text" 
                        list="category-list"
                        v-model="formData.category" 
                        placeholder="مثال: NPK کامل" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                      <datalist id="category-list">
                        <option value="NPK کامل"></option>
                        <option value="NPK پتاسیم بالا"></option>
                        <option value="NPK فسفر بالا"></option>
                        <option value="NPK نیتروژن بالا"></option>
                        <option value="نیترات"></option>
                        <option value="سولفات"></option>
                        <option value="فسفات"></option>
                        <option value="کلات EDTA"></option>
                        <option value="کلات EDDHA"></option>
                        <option value="کلات آمینو اسیدی"></option>
                        <option value="ریزمغذی"></option>
                        <option value="ریزمغذی کامل"></option>
                        <option value="اسید"></option>
                        <option value="محرک رشد"></option>
                        <option value="کلسیم-بور"></option>
                        <option value="پتاسیم مایع"></option>
                        <option value="روی-نیتروژن"></option>
                      </datalist>
                    </div>
                  </div>

                  <!-- قیمت -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      قیمت هر کیلوگرم (تومان) <span class="text-danger-500">*</span>
                    </label>
                    <div class="relative">
                      <input 
                        type="number" 
                        v-model.number="formData.price_per_kg" 
                        placeholder="مثال: ۸۵۰۰۰" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all pl-16"
                      />
                      <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-sm">تومان</span>
                    </div>
                  </div>

                  <!-- فرم فیزیکی و حلالیت -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        فرم فیزیکی
                      </label>
                      <select 
                        v-model="formData.form" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      >
                        <option value="">انتخاب کنید...</option>
                        <option value="powder">پودری (Powder)</option>
                        <option value="crystal">کریستالی (Crystal)</option>
                        <option value="liquid">مایع (Liquid)</option>
                        <option value="granular">گرانول (Granular)</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        حلالیت
                      </label>
                      <input 
                        type="text" 
                        v-model="formData.solubility" 
                        placeholder="مثال: 250 g/L" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                    </div>
                  </div>

                  <!-- نسبت NPK و pH -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        نسبت NPK
                      </label>
                      <input 
                        type="text" 
                        v-model="formData.npk_ratio" 
                        placeholder="مثال: 20-20-20" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        pH محلول
                      </label>
                      <input 
                        type="text" 
                        v-model="formData.ph_level" 
                        placeholder="مثال: 6.5" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                    </div>
                  </div>

                  <!-- توضیحات -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      توضیحات تکمیلی
                    </label>
                    <textarea 
                      v-model="formData.description" 
                      rows="3" 
                      placeholder="توضیحات درباره کاربرد، ویژگی‌ها یا نحوه مصرف..." 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                    ></textarea>
                  </div>
                </div>

                <!-- ستون چپ: عناصر و تنظیمات خاص -->
                <div class="space-y-4">
                  
                  <!-- بخش اسید -->
                  <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-4 border border-gray-200 dark:border-gray-600">
                    <div class="flex items-center justify-between mb-3">
                      <label class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer">
                        <input 
                          type="checkbox" 
                          v-model="formData.is_acid" 
                          class="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                        />
                        این ماده یک اسید است
                      </label>
                      <span v-if="formData.is_acid" class="text-xs bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 px-2 py-0.5 rounded-full">
                        تنظیم pH
                      </span>
                    </div>
                    
                    <div v-if="formData.is_acid" class="animate-fade-in">
                      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نوع اسید</label>
                      <select 
                        v-model="formData.acid_type" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      >
                        <option value="">انتخاب نوع اسید...</option>
                        <option value="H3PO4">اسید فسفریک (H3PO4)</option>
                        <option value="HNO3">اسید نیتریک (HNO3)</option>
                        <option value="H2SO4">اسید سولفوریک (H2SO4)</option>
                        <option value="Other">سایر اسیدها</option>
                      </select>
                    </div>
                  </div>

                  <!-- بخش عناصر -->
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        درصد عناصر تشکیل‌دهنده (%)
                      </label>
                      <button 
                        @click="clearElements" 
                        type="button"
                        class="text-xs text-danger-600 hover:text-danger-800 dark:hover:text-danger-400 transition-colors"
                      >
                        پاک کردن همه
                      </button>
                    </div>
                    
                    <div class="grid grid-cols-3 sm:grid-cols-4 gap-2 max-h-[280px] overflow-y-auto p-2 bg-gray-50 dark:bg-gray-700/20 rounded-lg custom-scrollbar">
                      <div v-for="el in elementsList" :key="el" class="flex flex-col gap-1">
                        <label class="text-xs font-medium text-gray-600 dark:text-gray-400 text-center bg-white dark:bg-gray-700 rounded py-1 border border-gray-200 dark:border-gray-600">
                          {{ el }}
                        </label>
                        <input 
                          type="number" 
                          v-model.number="formData.elements[el]" 
                          step="0.01" 
                          min="0" 
                          max="100"
                          placeholder="۰" 
                          class="w-full px-2 py-1.5 text-center border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-1 focus:ring-primary-500 focus:border-primary-500 transition-all"
                        />
                      </div>
                    </div>
                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 text-center">
                      مقادیر را بر اساس درصد وزنی وارد کنید (مثلاً ۲۰ برای ۲۰٪)
                    </p>
                  </div>

                  <!-- فیلدهای اضافی -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                    <div>
                      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">بسته‌بندی</label>
                      <input 
                        type="text" 
                        list="packaging-list"
                        v-model="formData.packaging" 
                        placeholder="مثال: 1 کیلویی" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                      <datalist id="packaging-list">
                        <option value="1 کیلویی"></option>
                        <option value="5 کیلویی"></option>
                        <option value="10 کیلویی"></option>
                        <option value="25 کیلویی"></option>
                        <option value="1 لیتری"></option>
                        <option value="5 لیتری"></option>
                        <option value="20 لیتری"></option>
                      </datalist>
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">کد ثبت</label>
                      <input 
                        type="text" 
                        v-model="formData.registration_code" 
                        placeholder="مثال: IR-12345" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- فوتر مودال -->
            <div class="bg-gray-50 dark:bg-gray-700/30 px-4 sm:px-6 py-4 border-t border-gray-200 dark:border-gray-600 flex flex-col-reverse sm:flex-row gap-3 justify-end sticky bottom-0">
              <button 
                @click="closeModal" 
                class="w-full sm:w-auto px-6 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors font-medium"
              >
                انصراف
              </button>
              <button 
                @click="saveFertilizer" 
                :disabled="isSaving || !formData.name"
                class="w-full sm:w-auto px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2 shadow-lg shadow-primary-500/30"
              >
                <svg v-if="isSaving" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره تغییرات' : 'افزودن کود') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';
import { apiService } from '@/services/apiService';

// ===== Props & Emits =====
const props = defineProps<{
  fertilizers: any[];
}>();

const emit = defineEmits<{
  (e: 'update:fertilizers', value: any[]): void;
}>();

// ===== Store =====
const fertilizerStore = useFertilizerStore();

// ===== State =====
const isLoading = ref(false);
const isSaving = ref(false);
const searchQuery = ref('');
const filterType = ref<'all' | 'fertilizer' | 'acid' | 'system'>('all');
const showModal = ref(false);
const isEditing = ref(false);

// لیست عناصر برای فرم
const elementsList = [
  'N-NO3', 'N-NH4', 'P', 'K', 'Ca', 'Mg', 'S', 
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Na', 'Cl'
];

// داده‌های فرم
const initialFormData = {
  id: null as string | null,
  name: '',
  brand: '',
  category: '',
  form: '',
  price_per_kg: 0,
  elements: {} as Record<string, number>,
  is_acid: false,
  acid_type: '',
  description: '',
  solubility: '',
  ph_level: '',
  npk_ratio: '',
  packaging: '',
  registration_code: '',
  is_system_default: false
};

const formData = reactive({ ...initialFormData });

// ===== Computed =====
const normalFertilizersCount = computed(() => {
  return props.fertilizers.filter((f: any) => !f.isAcid && !f.isSystemDefault).length;
});

const acidFertilizersCount = computed(() => {
  return props.fertilizers.filter((f: any) => f.isAcid).length;
});

const systemFertilizersCount = computed(() => {
  return props.fertilizers.filter((f: any) => f.isSystemDefault).length;
});

const hasSystemFertilizers = computed(() => {
  return systemFertilizersCount.value > 0;
});

const filteredFertilizers = computed(() => {
  let result = props.fertilizers;
  
  // فیلتر بر اساس نوع
  if (filterType.value === 'fertilizer') {
    result = result.filter((f: any) => !f.isAcid);
  } else if (filterType.value === 'acid') {
    result = result.filter((f: any) => f.isAcid);
  } else if (filterType.value === 'system') {
    result = result.filter((f: any) => f.isSystemDefault);
  }
  
  // فیلتر بر اساس جستجو
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase();
    result = result.filter((f: any) =>
      f.name.toLowerCase().includes(query) ||
      (f.brand && f.brand.toLowerCase().includes(query)) ||
      (f.acidType && f.acidType.toLowerCase().includes(query)) ||
      (f.category && f.category.toLowerCase().includes(query))
    );
  }
  
  return result;
});

// ===== Methods =====

/**
 * بارگذاری کودهای سیستمی از بک‌اند
 */
const loadSystemFertilizers = async () => {
  if (!confirm('آیا می‌خواهید ۴۲ کود پرکاربرد سیستمی را بارگذاری کنید؟\n\nاین کار باعث می‌شود شروع کار با برنامه راحت‌تر شود و نیازی به ورود دستی همه کودها نداشته باشید.')) {
    return;
  }
  
  isLoading.value = true;
  try {
    const result = await apiService.loadSystemFertilizers();
    
    if (result.success) {
      if (result.already_loaded) {
        alert(`✅ ${result.message}`);
      } else {
        alert(`🎉 ${result.message}\n\nتعداد کودهای اضافه شده: ${result.stats?.added || 0}`);
      }
      // رفرش لیست
      await refreshFertilizers();
    }
  } catch (error: any) {
    console.error(error);
    const errorMsg = error.response?.data?.detail || error.message || 'خطا در بارگذاری کودهای سیستمی';
    alert(`❌ ${errorMsg}`);
  } finally {
    isLoading.value = false;
  }
};

const refreshFertilizers = async () => {
  isLoading.value = true;
  try {
    await fertilizerStore.loadFertilizers();
    emit('update:fertilizers', fertilizerStore.fertilizers);
  } catch (error) {
    console.error('Error refreshing fertilizers:', error);
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  Object.assign(formData, { ...initialFormData, elements: {} });
  showModal.value = true;
};

const editFertilizer = (fertilizer: any) => {
  isEditing.value = true;
  Object.assign(formData, {
    id: fertilizer.id,
    name: fertilizer.name || '',
    brand: fertilizer.brand || '',
    category: fertilizer.category || '',
    form: fertilizer.form || '',
    price_per_kg: fertilizer.pricePerKg || fertilizer.price_per_kg || 0,
    elements: { ...(fertilizer.elements || {}) },
    is_acid: fertilizer.isAcid || fertilizer.is_acid || false,
    acid_type: fertilizer.acidType || fertilizer.acid_type || '',
    description: fertilizer.description || '',
    solubility: fertilizer.solubility || '',
    ph_level: fertilizer.phLevel || fertilizer.ph_level || '',
    npk_ratio: fertilizer.npkRatio || fertilizer.npk_ratio || '',
    packaging: fertilizer.packaging || '',
    registration_code: fertilizer.registrationCode || fertilizer.registration_code || '',
    is_system_default: fertilizer.isSystemDefault || fertilizer.is_system_default || false
  });
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const clearElements = () => {
  if (confirm('آیا از پاک کردن تمام عناصر اطمینان دارید؟')) {
    formData.elements = {};
  }
};

const saveFertilizer = async () => {
  if (!formData.name) {
    alert('لطفاً نام کود را وارد کنید.');
    return;
  }

  if (Number(formData.price_per_kg) < 0) {
    alert('قیمت نمی‌تواند منفی باشد.');
    return;
  }

  isSaving.value = true;
  try {
    // پاک کردن مقادیر خالی از elements
    const cleanElements: Record<string, number> = {};
for (const [key, value] of Object.entries(formData.elements)) {
  const numValue = Number(value);
  if (!isNaN(numValue) && numValue > 0) {
    cleanElements[key] = numValue;
  }
}

    const payload = {
      name: formData.name,
      brand: formData.brand || null,
      category: formData.category || null,
      form: formData.form || null,
      pricePerKg: Number(formData.price_per_kg),
      elements: cleanElements,
      isAcid: formData.is_acid,
      acidType: formData.acid_type || null,
      description: formData.description || null,
      solubility: formData.solubility || null,
      phLevel: formData.ph_level || null,
      npkRatio: formData.npk_ratio || null,
      packaging: formData.packaging || null,
      registrationCode: formData.registration_code || null
    };

    if (isEditing.value && formData.id) {
      await fertilizerStore.updateFertilizer(String(formData.id), payload);
    } else {
      await fertilizerStore.addFertilizer(payload);
    }

    closeModal();
    await refreshFertilizers();
    
  } catch (error: any) {
    console.error('Error saving fertilizer:', error);
    const errorMsg = error.response?.data?.detail || error.message || 'خطا در ذخیره‌سازی. لطفاً دوباره تلاش کنید.';
    alert(`❌ ${errorMsg}`);
  } finally {
    isSaving.value = false;
  }
};

const deleteFertilizer = async (id: string, isSystemDefault: boolean = false) => {
  let message = 'آیا از حذف این کود اطمینان دارید؟ این عملیات غیرقابل بازگشت است.';
  
  if (isSystemDefault) {
    message = '⚠️ این یک کود سیستمی است و قابل حذف نیست.\n\nاگر می‌خواهید تغییراتی روی آن اعمال کنید، از دکمه ویرایش استفاده کنید تا یک کپی شخصی برای شما ساخته شود.';
    alert(message);
    return;
  }
  
  if (confirm(message)) {
    try {
      await fertilizerStore.deleteFertilizer(id);
      await refreshFertilizers();
    } catch (error: any) {
      console.error('Error deleting fertilizer:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'خطا در حذف کود.';
      alert(`❌ ${errorMsg}`);
    }
  }
};

const hasElements = (fertilizer: any): boolean => {
  if (!fertilizer.elements) return false;
  return Object.values(fertilizer.elements).some((v: any) => v && v > 0);
};

const getActiveElements = (fertilizer: any): Record<string, number> => {
  if (!fertilizer.elements) return {};
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(fertilizer.elements)) {
    if (value && (value as number) > 0) {
      result[key] = value as number;
    }
  }
  return result;
};

// ===== Lifecycle =====
onMounted(() => {
  // بارگذاری اولیه کودها در صورت خالی بودن
  if (props.fertilizers.length === 0) {
    refreshFertilizers();
  }
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* Custom Scrollbar for Modal */
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

/* Animation for Acid Section */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* حذف اسپینر input number */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

/* استایل datalist */
input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 1rem;
  padding-left: 2.5rem;
}

.dark input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}
</style>