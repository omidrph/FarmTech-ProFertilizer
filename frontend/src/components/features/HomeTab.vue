<!-- frontend/src/components/features/HomeTab.vue -->
<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- Loading State -->
    <!-- ============================================================ -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-16">
      <div class="relative">
        <div class="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 dark:border-primary-900"></div>
        <div class="animate-spin rounded-full h-16 w-16 border-4 border-primary-600 border-t-transparent absolute top-0"></div>
      </div>
      <p class="mt-4 text-gray-600 dark:text-gray-400 text-sm">در حال بارگذاری داده‌ها...</p>
    </div>

    <!-- ============================================================ -->
    <!-- Error State -->
    <!-- ============================================================ -->
    <div v-else-if="error" class="card border-r-4 border-r-danger-500">
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-danger-100 dark:bg-danger-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-danger-600 dark:text-danger-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-danger-700 dark:text-danger-400">خطا در دریافت داده‌ها</h4>
          <p class="text-sm text-danger-600 dark:text-danger-500 mt-1">{{ error }}</p>
          <button
            @click="loadDashboardData"
            class="mt-3 px-4 py-1.5 bg-danger-600 hover:bg-danger-700 text-white text-sm rounded-lg transition-colors"
          >
            تلاش مجدد
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- ✅ Empty State - وقتی هیچ گزارشی وجود ندارد -->
    <!-- ============================================================ -->
    <div v-else-if="!hasActiveReport" class="card text-center py-16">
      <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center">
        <svg class="w-12 h-12 text-primary-500 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">
        هیچ گزارشی وجود ندارد
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto leading-relaxed">
        برای شروع، یک گزارش جدید ایجاد کنید یا یک گزارش موجود را باز کنید.
      </p>
      <div class="mt-6 flex flex-wrap justify-center gap-2">
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs">
          فایل → جدید
        </span>
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs">
          فایل → بازکردن
        </span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- ✅ نمایش داده‌های واقعی از storeها -->
    <!-- ============================================================ -->
    <template v-else>
      <!-- بخش 1: کارت‌های خلاصه داشبورد -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <!-- کارت 1: وضعیت تعادل یونی -->
        <div class="card border-l-4" :class="ionBalanceStatus.borderClass">
          <div class="flex items-start justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center" :class="ionBalanceStatus.bgClass">
              <svg class="w-5 h-5 sm:w-6 sm:h-6" :class="ionBalanceStatus.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <span class="px-2 py-0.5 rounded-full text-xs font-semibold" :class="ionBalanceStatus.badgeClass">
              {{ ionBalance.isBalanced ? 'متعادل' : 'نامتعادل' }}
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">تعادل یونی</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ ionBalance.cation.toFixed(2) }}
            </span>
            <span class="text-xs text-gray-400">/ {{ ionBalance.anion.toFixed(2) }}</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">کاتیون / آنیون (meq/L)</p>
        </div>

        <!-- کارت 2: تعداد عناصر فعال -->
        <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-primary-500">
          <div class="flex items-start justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              </svg>
            </div>
            <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400">
              {{ activeElementsCount }}/15
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">عناصر فعال</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ activeElementsCount }}
            </span>
            <span class="text-xs text-gray-400">عنصر</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">دارای مقدار هدف</p>
        </div>

        <!-- کارت 3: تعداد مخازن فعال -->
        <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-success-500">
          <div class="flex items-start justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
              </svg>
            </div>
            <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-success-50 dark:bg-success-900/30 text-success-700 dark:text-success-400">
              {{ activeReservoirsCount }}/3
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">مخازن فعال</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ activeReservoirsCount }}
            </span>
            <span class="text-xs text-gray-400">مخزن</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">A, B, C</p>
        </div>

        <!-- کارت 4: مجموع هزینه -->
        <div class="card group hover:scale-[1.02] transition-all duration-300 border-l-4 border-l-warning-500">
          <div class="flex items-start justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-warning-50 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400">
              تومان
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">هزینه کل</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ totalCost.toLocaleString('fa-IR') }}
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">مجموع هزینه کودها</p>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 2: جدول مقایسه عناصر -->
      <!-- ============================================================ -->
      <div class="card">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">
                مقایسه هدف و محلول نهایی
              </h3>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                بررسی دقیق مقادیر هدف در برابر مقادیر تامین شده
              </p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500 dark:text-gray-400">واحد:</span>
            <span class="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-lg text-xs font-semibold text-gray-700 dark:text-gray-300">
              PPM
            </span>
          </div>
        </div>

        <!-- جدول -->
        <div class="overflow-x-auto -mx-4 sm:mx-0">
          <div class="inline-block min-w-full align-middle px-4 sm:px-0">
            <table class="min-w-full border-collapse">
              <thead>
                <tr>
                  <th class="sticky left-0 z-10 bg-gray-50 dark:bg-gray-700 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                    عنصر
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                    هدف
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                    تامین شده
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[120px]">
                    وضعیت
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                    اختلاف
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                <tr
                  v-for="item in elementComparisonData"
                  :key="item.element"
                  class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <td class="sticky left-0 z-10 bg-white dark:bg-gray-800 px-3 py-3 text-right">
                    <div class="flex items-center gap-2">
                      <span
                        class="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold"
                        :class="getElementBadgeClass(item.element)"
                      >
                        {{ getElementSymbol(item.element) }}
                      </span>
                      <span class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ item.element }}
                      </span>
                    </div>
                  </td>
                  <td class="px-3 py-3 text-center">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 tabular-nums">
                      {{ item.target.toFixed(2) }}
                    </span>
                  </td>
                  <td class="px-3 py-3 text-center">
                    <span class="text-sm font-semibold tabular-nums" :class="getActualValueClass(item.progressPercent)">
                      {{ item.actual.toFixed(2) }}
                    </span>
                  </td>
                  <td class="px-3 py-3">
                    <div class="flex items-center gap-2">
                      <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div
                          class="h-full rounded-full transition-all duration-500"
                          :class="getProgressClass(item.progressPercent)"
                          :style="{ width: Math.min(item.progressPercent, 100) + '%' }"
                        ></div>
                      </div>
                      <span class="text-xs font-semibold min-w-[35px] text-right tabular-nums" :class="getProgressTextClass(item.progressPercent)">
                        {{ Math.round(item.progressPercent) }}%
                      </span>
                    </div>
                  </td>
                  <td class="px-3 py-3 text-center">
                    <div
                      v-if="item.difference !== 0"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold"
                      :class="getDiffClass(item.difference, item.target)"
                    >
                      <svg v-if="item.difference > 0" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                      </svg>
                      <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
                      </svg>
                      {{ Math.abs(item.difference).toFixed(2) }}
                    </div>
                    <span v-else class="text-xs text-success-600 dark:text-success-400 font-semibold">
                      ✓ کامل
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- راهنمای رنگ‌ها -->
        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-wrap items-center gap-3 text-xs">
            <span class="text-gray-500 dark:text-gray-400">راهنما:</span>
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-success-500"></span>
              <span class="text-gray-600 dark:text-gray-400">مطلوب (90-110%)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-warning-500"></span>
              <span class="text-gray-600 dark:text-gray-400">نیاز به تنظیم (70-90%)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-danger-500"></span>
              <span class="text-gray-600 dark:text-gray-400">بحرانی (&lt;70% یا &gt;110%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 3: اطلاعات مخازن -->
      <!-- ============================================================ -->
      <div class="card">
        <div class="flex items-center gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
            <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div>
            <h3 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">
              توزیع مواد در مخازن
            </h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              تقسیم‌بندی کودها بر اساس سازگاری شیمیایی
            </p>
          </div>
        </div>

        <!-- کارت‌های مخازن -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            v-for="(reservoir, key) in reservoirData"
            :key="key"
            class="relative overflow-hidden rounded-xl border-2 p-4 transition-all hover:shadow-lg"
            :class="getReservoirBorderClass(key)"
          >
            <div class="absolute top-0 right-0 w-20 h-20 rounded-full -mr-10 -mt-10 opacity-50" :class="getReservoirBgClass(key)"></div>
            <div class="relative">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 rounded-lg text-white flex items-center justify-center font-bold text-lg shadow-md" :class="getReservoirColorClass(key)">
                    {{ key }}
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-900 dark:text-white text-sm">{{ getReservoirName(key) }}</h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">{{ getReservoirDesc(key) }}</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-white rounded-lg text-xs font-bold tabular-nums" :class="getReservoirColorClass(key)">
                  {{ getReservoirTotal(key).toFixed(2) }}g
                </span>
              </div>
              <div v-if="reservoir.length > 0" class="space-y-2">
                <div
                  v-for="(item, idx) in reservoir"
                  :key="idx"
                  class="flex items-center justify-between bg-white dark:bg-gray-700/50 rounded-lg px-3 py-2 border"
                  :class="getReservoirItemBorderClass(key)"
                >
                  <span class="text-xs font-medium text-gray-700 dark:text-gray-300 truncate max-w-[120px]">
                    {{ item.name }}
                  </span>
                  <span class="text-xs font-bold tabular-nums" :class="getReservoirItemTextClass(key)">
                    {{ item.amount?.toFixed(3) || '0.000' }}g
                  </span>
                </div>
              </div>
              <div v-else class="text-center py-4 text-xs text-gray-400 dark:text-gray-500">
                خالی
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-4 text-sm">
              <div class="flex items-center gap-2">
                <span class="text-gray-500 dark:text-gray-400">مجموع کل:</span>
                <span class="font-bold text-gray-900 dark:text-white tabular-nums">
                  {{ totalReservoirWeight.toFixed(2) }} گرم
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span>مخازن بر اساس سازگاری شیمیایی تقسیم شده‌اند</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 4: توصیه‌ها -->
      <!-- ============================================================ -->
      <div v-if="recommendations.length > 0" class="card border-l-4 border-l-primary-500">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-gray-900 dark:text-white">
              توصیه‌های هوشمند
            </h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              بر اساس تحلیل داده‌های فعلی
            </p>
          </div>
        </div>
        <div class="space-y-2">
          <div
            v-for="(rec, idx) in recommendations"
            :key="idx"
            class="flex items-start gap-3 p-3 rounded-lg"
            :class="getRecommendationBgClass(rec.type)"
          >
            <div class="flex-shrink-0 mt-0.5">
              <div class="w-6 h-6 rounded-full flex items-center justify-center" :class="getRecommendationIconBgClass(rec.type)">
                <svg class="w-3.5 h-3.5" :class="getRecommendationIconClass(rec.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="rec.type === 'warning'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                  <path v-else-if="rec.type === 'danger'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium" :class="getRecommendationTextClass(rec.type)">
                {{ rec.title }}
              </p>
              <p class="text-xs mt-0.5" :class="getRecommendationDescClass(rec.type)">
                {{ rec.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { apiService } from '@/services/apiService';

// ============================================================
// Props
// ============================================================
interface Props {
  targetUnit?: string;
}

const props = defineProps<Props>();

// ============================================================
// Stores
// ============================================================
const reportStore = useReportStore();
const targetStore = useTargetStore();
const waterStore = useWaterStore();
const calcStore = useCalcStore();

// ============================================================
// State
// ============================================================
const isLoading = ref(false);
const error = ref<string | null>(null);

// لیست عناصر
const ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ============================================================
// Computed - داده‌ها از storeها
// ============================================================

/** آیا گزارشی فعال است؟ */
const hasActiveReport = computed(() => reportStore.hasActiveReport);

/** تعادل یونی از targetStore */
const ionBalance = computed(() => targetStore.ionBalance);

/** عناصر هدف از targetStore */
const targetElements = computed(() => targetStore.targetElements);

/** عناصر تامین شده از calcStore (concentrations) */
const actualElements = computed(() => {
  if (calcStore.optimizationResult?.concentrations) {
    return calcStore.optimizationResult.concentrations;
  }
  // اگر نتیجه بهینه‌سازی وجود ندارد، از finalValues استفاده کن
  return calcStore.elementTotals || {};
});

/** تعداد عناصر فعال */
const activeElementsCount = computed(() => {
  return Object.values(targetElements.value).filter(v => v && v > 0).length;
});

/** داده‌های مخازن */
const reservoirData = computed(() => calcStore.reservoirData);

/** تعداد مخازن فعال */
const activeReservoirsCount = computed(() => {
  let count = 0;
  if (reservoirData.value.A?.length > 0) count++;
  if (reservoirData.value.B?.length > 0) count++;
  if (reservoirData.value.C?.length > 0) count++;
  return count;
});

/** مجموع وزن مخازن */
const totalReservoirWeight = computed(() => {
  let total = 0;
  for (const key of ['A', 'B', 'C'] as const) {
    for (const item of (reservoirData.value[key] || [])) {
      total += item.amount || 0;
    }
  }
  return total;
});

/** هزینه کل */
const totalCost = computed(() => calcStore.totalCost || 0);

/** داده‌های مقایسه عناصر */
const elementComparisonData = computed(() => {
  return ELEMENTS.map(element => {
    const target = (targetElements.value as any)[element] || 0;
    const actual = (actualElements.value as any)[element] || 0;
    const difference = actual - target;
    const progressPercent = target > 0 ? Math.min((actual / target) * 100, 150) : 0;
    
    return {
      element,
      target,
      actual,
      difference,
      progressPercent
    };
  });
});

/** وضعیت تعادل یونی برای کارت */
const ionBalanceStatus = computed(() => {
  if (!ionBalance.value) {
    return {
      borderClass: 'border-l-gray-300 dark:border-l-gray-600',
      bgClass: 'bg-gray-100 dark:bg-gray-700',
      iconClass: 'text-gray-500 dark:text-gray-400',
      badgeClass: 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
    };
  }
  if (ionBalance.value.isBalanced) {
    return {
      borderClass: 'border-l-success-500',
      bgClass: 'bg-success-50 dark:bg-success-900/30',
      iconClass: 'text-success-600 dark:text-success-400',
      badgeClass: 'bg-success-100 dark:bg-success-900/50 text-success-700 dark:text-success-400'
    };
  } else {
    return {
      borderClass: 'border-l-danger-500',
      bgClass: 'bg-danger-50 dark:bg-danger-900/30',
      iconClass: 'text-danger-600 dark:text-danger-400',
      badgeClass: 'bg-danger-100 dark:bg-danger-900/50 text-danger-700 dark:text-danger-400'
    };
  }
});

/** تولید توصیه‌ها */
const recommendations = computed(() => {
  const recs: Array<{ type: 'success' | 'warning' | 'danger'; title: string; description: string }> = [];
  
  // 1. تعادل یونی
  if (!ionBalance.value.isBalanced) {
    const diff = Math.abs(ionBalance.value.cation - ionBalance.value.anion);
    recs.push({
      type: 'danger',
      title: 'عدم تعادل یونی',
      description: `اختلاف کاتیون و آنیون ${diff.toFixed(2)} meq/L است.`
    });
  }
  
  // 2. بررسی عناصر کمبود/بیش‌بود
  const deficient: string[] = [];
  const excessive: string[] = [];
  
  for (const item of elementComparisonData.value) {
    if (item.target === 0) continue;
    if (item.progressPercent < 70) {
      deficient.push(item.element);
    } else if (item.progressPercent > 130) {
      excessive.push(item.element);
    }
  }
  
  if (deficient.length > 0) {
    recs.push({
      type: 'warning',
      title: `${deficient.length} عنصر با کمبود شدید`,
      description: `عناصر ${deficient.slice(0, 3).join(', ')}${deficient.length > 3 ? ' و...' : ''} کمتر از 70% مقدار هدف هستند.`
    });
  }
  
  if (excessive.length > 0) {
    recs.push({
      type: 'warning',
      title: `${excessive.length} عنصر با بیش‌بود`,
      description: `عناصر ${excessive.slice(0, 3).join(', ')}${excessive.length > 3 ? ' و...' : ''} بیشتر از 130% مقدار هدف هستند.`
    });
  }
  
  // 3. EC
  if (calcStore.optimizationResult?.ec !== undefined) {
    const ec = calcStore.optimizationResult.ec;
    if (ec < 0.8) {
      recs.push({
        type: 'warning',
        title: 'EC کم',
        description: `EC پایین است (${ec.toFixed(2)} dS/m). ممکن است نیاز به افزایش غلظت کودها باشد.`
      });
    } else if (ec > 3.5) {
      recs.push({
        type: 'danger',
        title: 'EC بحرانی',
        description: `EC بسیار بالا است (${ec.toFixed(2)} dS/m). خطر شوری جدی است!`
      });
    }
  }
  
  // 4. pH
  if (calcStore.optimizationResult?.ph !== undefined) {
    const ph = calcStore.optimizationResult.ph;
    if (ph < 5.5) {
      recs.push({
        type: 'warning',
        title: 'pH اسیدی',
        description: `pH پایین است (${ph.toFixed(2)}). ممکن است جذب برخی عناصر کاهش یابد.`
      });
    } else if (ph > 7.0) {
      recs.push({
        type: 'warning',
        title: 'pH قلیایی',
        description: `pH بالا است (${ph.toFixed(2)}). ممکن است جذب ریزمغذی‌ها کاهش یابد.`
      });
    }
  }
  
  if (recs.length === 0) {
    recs.push({
      type: 'success',
      title: 'وضعیت مطلوب',
      description: 'تمام پارامترها در محدوده مناسب قرار دارند.'
    });
  }
  
  return recs;
});

// ============================================================
// Helper Functions - مخازن
// ============================================================

const getReservoirColorClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'bg-primary-500',
    'B': 'bg-success-500',
    'C': 'bg-warning-500'
  };
  return classes[key] || 'bg-gray-500';
};

const getReservoirBorderClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'border-primary-200 dark:border-primary-800',
    'B': 'border-success-200 dark:border-success-800',
    'C': 'border-warning-200 dark:border-warning-800'
  };
  return classes[key] || 'border-gray-200 dark:border-gray-700';
};

const getReservoirBgClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'bg-primary-100 dark:bg-primary-900/30',
    'B': 'bg-success-100 dark:bg-success-900/30',
    'C': 'bg-warning-100 dark:bg-warning-900/30'
  };
  return classes[key] || 'bg-gray-100 dark:bg-gray-700/30';
};

const getReservoirName = (key: string): string => {
  const names: Record<string, string> = {
    'A': 'مخزن کلسیم',
    'B': 'مخزن اصلی',
    'C': 'مخزن اسید'
  };
  return names[key] || key;
};

const getReservoirDesc = (key: string): string => {
  const descs: Record<string, string> = {
    'A': 'کودهای کلسیمی',
    'B': 'سایر کودها',
    'C': 'تنظیم pH'
  };
  return descs[key] || '';
};

const getReservoirItemBorderClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'border-primary-100 dark:border-primary-900/50',
    'B': 'border-success-100 dark:border-success-900/50',
    'C': 'border-warning-100 dark:border-warning-900/50'
  };
  return classes[key] || 'border-gray-100 dark:border-gray-700';
};

const getReservoirItemTextClass = (key: string): string => {
  const classes: Record<string, string> = {
    'A': 'text-primary-600 dark:text-primary-400',
    'B': 'text-success-600 dark:text-success-400',
    'C': 'text-warning-600 dark:text-warning-400'
  };
  return classes[key] || 'text-gray-600 dark:text-gray-400';
};

const getReservoirTotal = (key: string): number => {
  const data = reservoirData.value?.[key as keyof typeof reservoirData.value] || [];
  return data.reduce((sum: number, item: any) => sum + (item.amount || 0), 0);
};

// ============================================================
// Helper Functions - عناصر
// ============================================================

const getElementSymbol = (element: string): string => {
  const symbols: Record<string, string> = {
    'N-NO3': 'N', 'P': 'P', 'S': 'S', 'N-NH4': 'N', 'K': 'K',
    'Ca': 'Ca', 'Mg': 'Mg', 'Na': 'Na', 'Cl': 'Cl', 'Fe': 'Fe',
    'Mn': 'Mn', 'Zn': 'Zn', 'B': 'B', 'Cu': 'Cu', 'Mo': 'Mo'
  };
  return symbols[element] || element.substring(0, 2);
};

const getElementBadgeClass = (element: string): string => {
  const macroElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg'];
  const microElements = ['Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];
  
  if (macroElements.includes(element)) {
    return 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400';
  } else if (microElements.includes(element)) {
    return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400';
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400';
};

const getProgressClass = (percent: number): string => {
  if (percent >= 90 && percent <= 110) return 'bg-success-500';
  if (percent >= 70 && percent < 90) return 'bg-warning-500';
  if (percent > 110 && percent <= 130) return 'bg-warning-500';
  return 'bg-danger-500';
};

const getProgressTextClass = (percent: number): string => {
  if (percent >= 90 && percent <= 110) return 'text-success-600 dark:text-success-400';
  if ((percent >= 70 && percent < 90) || (percent > 110 && percent <= 130)) return 'text-warning-600 dark:text-warning-400';
  return 'text-danger-600 dark:text-danger-400';
};

const getActualValueClass = (percent: number): string => {
  if (percent >= 90 && percent <= 110) return 'text-success-600 dark:text-success-400';
  if ((percent >= 70 && percent < 90) || (percent > 110 && percent <= 130)) return 'text-warning-600 dark:text-warning-400';
  return 'text-danger-600 dark:text-danger-400';
};

const getDiffClass = (diff: number, target: number): string => {
  if (target === 0) return '';
  const percent = Math.abs((diff / target) * 100);
  if (percent <= 10) return 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400';
  if (percent <= 30) return 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400';
  return 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400';
};

// ============================================================
// Helper Functions - توصیه‌ها
// ============================================================

const getRecommendationBgClass = (type: string): string => {
  if (type === 'danger') return 'bg-danger-50 dark:bg-danger-900/20';
  if (type === 'warning') return 'bg-warning-50 dark:bg-warning-900/20';
  return 'bg-success-50 dark:bg-success-900/20';
};

const getRecommendationIconBgClass = (type: string): string => {
  if (type === 'danger') return 'bg-danger-100 dark:bg-danger-900/50';
  if (type === 'warning') return 'bg-warning-100 dark:bg-warning-900/50';
  return 'bg-success-100 dark:bg-success-900/50';
};

const getRecommendationIconClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-600 dark:text-danger-400';
  if (type === 'warning') return 'text-warning-600 dark:text-warning-400';
  return 'text-success-600 dark:text-success-400';
};

const getRecommendationTextClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-700 dark:text-danger-400';
  if (type === 'warning') return 'text-warning-700 dark:text-warning-400';
  return 'text-success-700 dark:text-success-400';
};

const getRecommendationDescClass = (type: string): string => {
  if (type === 'danger') return 'text-danger-600 dark:text-danger-500';
  if (type === 'warning') return 'text-warning-600 dark:text-warning-500';
  return 'text-success-600 dark:text-success-500';
};

// ============================================================
// Load Dashboard Data
// ============================================================
const loadDashboardData = async () => {
  // اگر هیچ گزارشی فعال نیست، کاری نکن
  if (!hasActiveReport.value) {
    isLoading.value = false;
    return;
  }
  
  isLoading.value = true;
  error.value = null;
  
  try {
    // محاسبه تعادل یونی
    await targetStore.calculateIonBalanceFromAPI();
    
    // اگر نتیجه بهینه‌سازی وجود ندارد، از calcStore استفاده کن
    if (!calcStore.optimizationResult) {
      // محاسبات ساده از روی calcRows
      calcStore.calculateTotals();
    }
    
    // بارگذاری آنالیز آب (اگر قبلاً بارگذاری نشده)
    if (Object.keys(waterStore.waterValues).length === 0 && hasActiveReport.value) {
      try {
        const waterData = await apiService.getWaterAnalysis(String(reportStore.currentReportId));
        if (waterData) {
          waterStore.loadFromAPI(waterData);
        }
      } catch (e) {
        // آنالیز آب وجود ندارد - اشکالی ندارد
      }
    }
    
  } catch (err: any) {
    error.value = err.message || 'خطا در بارگذاری داده‌ها';
    console.error('Error loading dashboard data:', err);
  } finally {
    isLoading.value = false;
  }
};

// ============================================================
// Watch برای تغییرات
// ============================================================
watch(
  () => reportStore.currentReportId,
  (newId, oldId) => {
    console.log(`🔄 Report ID changed: ${oldId} → ${newId}`);
    if (newId === null) {
      // ریست کردن داده‌ها
      isLoading.value = false;
      error.value = null;
    } else {
      // بارگذاری داده‌های جدید
      loadDashboardData();
    }
  },
  { immediate: true }
);

// ============================================================
// Event Listeners
// ============================================================
const handleReportChanged = () => {
  console.log('📊 Report changed event received');
  loadDashboardData();
};

const handleReportReset = () => {
  console.log('🔄 Report reset event received');
  isLoading.value = false;
  error.value = null;
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(() => {
  console.log('🏠 HomeTab mounted');
  loadDashboardData();
  window.addEventListener('report-changed', handleReportChanged);
  window.addEventListener('report-reset', handleReportReset);
});

onUnmounted(() => {
  console.log('🏠 HomeTab unmounted');
  window.removeEventListener('report-changed', handleReportChanged);
  window.removeEventListener('report-reset', handleReportReset);
});
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .overflow-x-auto::-webkit-scrollbar-track {
  background: #374151;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>