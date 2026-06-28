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
      <p class="mt-4 text-gray-600 dark:text-gray-400 text-sm">در حال بارگذاری داده‌ها از سرور...</p>
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
            @click="loadData"
            class="mt-3 px-4 py-1.5 bg-danger-600 hover:bg-danger-700 text-white text-sm rounded-lg transition-colors"
          >
            تلاش مجدد
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- Empty State -->
    <!-- ============================================================ -->
    <div v-else-if="!summary?.has_data" class="card text-center py-16">
      <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center">
        <svg class="w-12 h-12 text-primary-500 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">
        هنوز داده‌ای برای نمایش وجود ندارد
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto leading-relaxed">
        {{ summary?.message || 'برای مشاهده داشبورد، ابتدا در بخش‌های مختلف داده‌ها را وارد کرده و محاسبات را انجام دهید.' }}
      </p>
      <div class="mt-6 flex flex-wrap justify-center gap-2">
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs">
          ۱. آنالیز آب
        </span>
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs">
          ۲. عناصر هدف
        </span>
        <span class="px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs">
          ۳. محاسبه کود
        </span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- Data Loaded - Full Dashboard -->
    <!-- ============================================================ -->
    <template v-else>
      <!-- بخش 1: کارت‌های خلاصه داشبورد -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <!-- کارت 1: وضعیت تعادل یونی -->
        <div
          class="card group hover:scale-[1.02] transition-all duration-300"
          :class="ionBalanceStatus.borderClass"
        >
          <div class="flex items-start justify-between mb-3">
            <div
              class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center transition-colors"
              :class="ionBalanceStatus.bgClass"
            >
              <svg class="w-5 h-5 sm:w-6 sm:h-6" :class="ionBalanceStatus.iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <span
              class="px-2 py-0.5 rounded-full text-xs font-semibold"
              :class="ionBalanceStatus.badgeClass"
            >
              {{ summary.ion_balance?.is_balanced ? 'متعادل' : 'نامتعادل' }}
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">تعادل یونی</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ formatNumber(summary.ion_balance?.cation) }}
            </span>
            <span class="text-xs text-gray-400">/ {{ formatNumber(summary.ion_balance?.anion) }}</span>
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
              {{ summary.active_elements_count }}/{{ summary.total_elements }}
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">عناصر فعال</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ summary.active_elements_count }}
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
              {{ summary.active_reservoirs_count }}/3
            </span>
          </div>
          <h3 class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-1">مخازن فعال</h3>
          <div class="flex items-baseline gap-2">
            <span class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white tabular-nums">
              {{ summary.active_reservoirs_count }}
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
              {{ formatCurrency(summary.total_cost) }}
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">مجموع هزینه کودها</p>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 2: جدول هدف و محلول نهایی -->
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

        <!-- جدول با اسکرول افقی برای موبایل -->
        <div class="overflow-x-auto -mx-4 sm:mx-0">
          <div class="inline-block min-w-full align-middle px-4 sm:px-0">
            <table class="min-w-full border-collapse">
              <thead>
                <tr>
                  <th class="sticky left-0 z-10 bg-gray-50 dark:bg-gray-700 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                    عنصر
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                    <div class="flex flex-col items-center gap-1">
                      <span>هدف</span>
                      <span class="text-[10px] text-gray-400 font-normal">Target</span>
                    </div>
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[90px]">
                    <div class="flex flex-col items-center gap-1">
                      <span>تامین شده</span>
                      <span class="text-[10px] text-gray-400 font-normal">Actual</span>
                    </div>
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[120px]">
                    <div class="flex flex-col items-center gap-1">
                      <span>وضعیت</span>
                      <span class="text-[10px] text-gray-400 font-normal">Progress</span>
                    </div>
                  </th>
                  <th class="bg-gray-50 dark:bg-gray-700 px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b-2 border-gray-200 dark:border-gray-600 min-w-[80px]">
                    <div class="flex flex-col items-center gap-1">
                      <span>اختلاف</span>
                      <span class="text-[10px] text-gray-400 font-normal">Diff</span>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                <tr
                  v-for="item in summary.elements_data"
                  :key="item.element"
                  class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <!-- نام عنصر -->
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
                  <!-- مقدار هدف -->
                  <td class="px-3 py-3 text-center">
                    <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 tabular-nums">
                      {{ item.target.toFixed(2) }}
                    </span>
                  </td>
                  <!-- مقدار تامین شده -->
                  <td class="px-3 py-3 text-center">
                    <span class="text-sm font-semibold tabular-nums" :class="getActualValueClass(item.progress_percent)">
                      {{ item.actual.toFixed(2) }}
                    </span>
                  </td>
                  <!-- نوار پیشرفت -->
                  <td class="px-3 py-3">
                    <div class="flex items-center gap-2">
                      <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div
                          class="h-full rounded-full transition-all duration-500"
                          :class="getProgressClass(item.progress_percent)"
                          :style="{ width: Math.min(item.progress_percent, 100) + '%' }"
                        ></div>
                      </div>
                      <span class="text-xs font-semibold min-w-[35px] text-right tabular-nums" :class="getProgressTextClass(item.progress_percent)">
                        {{ Math.round(item.progress_percent) }}%
                      </span>
                    </div>
                  </td>
                  <!-- اختلاف -->
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
        <div class="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center gap-3">
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
        </div>

        <!-- کارت‌های مخازن -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- مخزن A -->
          <div class="relative overflow-hidden rounded-xl border-2 border-primary-200 dark:border-primary-800 bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/20 dark:to-gray-800 p-4 transition-all hover:shadow-lg">
            <div class="absolute top-0 right-0 w-20 h-20 bg-primary-100 dark:bg-primary-900/30 rounded-full -mr-10 -mt-10 opacity-50"></div>
            <div class="relative">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 rounded-lg bg-primary-500 text-white flex items-center justify-center font-bold text-lg shadow-md">
                    A
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-900 dark:text-white text-sm">مخزن کلسیم</h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">کودهای کلسیمی</p>
                  </div>
                </div>
                <span class="px-2 py-1 bg-primary-500 text-white rounded-lg text-xs font-bold tabular-nums">
                  {{ getReservoirTotal('A').toFixed(2) }}g
                </span>
              </div>
              <div v-if="summary.reservoir_data?.A?.length > 0" class="space-y-2">
                <div
                  v-for="(item, idx) in summary.reservoir_data.A"
                  :key="idx"
                  class="flex items-center justify-between bg-white dark:bg-gray-700/50 rounded-lg px-3 py-2 border border-primary-100 dark:border-primary-900/50"
                >
                  <span class="text-xs font-medium text-gray-700 dark:text-gray-300 truncate max-w-[120px]">
                    {{ item.name }}
                  </span>
                  <span class="text-xs font-bold text-primary-600 dark:text-primary-400 tabular-nums">
                    {{ item.amount?.toFixed(3) || '0.000' }}g
                  </span>
                </div>
              </div>
              <div v-else class="text-center py-4 text-xs text-gray-400 dark:text-gray-500">
                خالی
              </div>
            </div>
          </div>

          <!-- مخزن B -->
          <div class="relative overflow-hidden rounded-xl border-2 border-success-200 dark:border-success-800 bg-gradient-to-br from-success-50 to-white dark:from-success-900/20 dark:to-gray-800 p-4 transition-all hover:shadow-lg">
            <div class="absolute top-0 right-0 w-20 h-20 bg-success-100 dark:bg-success-900/30 rounded-full -mr-10 -mt-10 opacity-50"></div>
            <div class="relative">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 rounded-lg bg-success-500 text-white flex items-center justify-center font-bold text-lg shadow-md">
                    B
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-900 dark:text-white text-sm">مخزن اصلی</h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">سایر کودها</p>
                  </div>
                </div>
                <span class="px-2 py-1 bg-success-500 text-white rounded-lg text-xs font-bold tabular-nums">
                  {{ getReservoirTotal('B').toFixed(2) }}g
                </span>
              </div>
              <div v-if="summary.reservoir_data?.B?.length > 0" class="space-y-2">
                <div
                  v-for="(item, idx) in summary.reservoir_data.B"
                  :key="idx"
                  class="flex items-center justify-between bg-white dark:bg-gray-700/50 rounded-lg px-3 py-2 border border-success-100 dark:border-success-900/50"
                >
                  <span class="text-xs font-medium text-gray-700 dark:text-gray-300 truncate max-w-[120px]">
                    {{ item.name }}
                  </span>
                  <span class="text-xs font-bold text-success-600 dark:text-success-400 tabular-nums">
                    {{ item.amount?.toFixed(3) || '0.000' }}g
                  </span>
                </div>
              </div>
              <div v-else class="text-center py-4 text-xs text-gray-400 dark:text-gray-500">
                خالی
              </div>
            </div>
          </div>

          <!-- مخزن C -->
          <div class="relative overflow-hidden rounded-xl border-2 border-warning-200 dark:border-warning-800 bg-gradient-to-br from-warning-50 to-white dark:from-warning-900/20 dark:to-gray-800 p-4 transition-all hover:shadow-lg">
            <div class="absolute top-0 right-0 w-20 h-20 bg-warning-100 dark:bg-warning-900/30 rounded-full -mr-10 -mt-10 opacity-50"></div>
            <div class="relative">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 rounded-lg bg-warning-500 text-white flex items-center justify-center font-bold text-lg shadow-md">
                    C
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-900 dark:text-white text-sm">مخزن اسید</h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400">تنظیم pH</p>
                  </div>
                </div>
                <span class="px-2 py-1 bg-warning-500 text-white rounded-lg text-xs font-bold tabular-nums">
                  {{ getReservoirTotal('C').toFixed(2) }}g
                </span>
              </div>
              <div v-if="summary.reservoir_data?.C?.length > 0" class="space-y-2">
                <div
                  v-for="(item, idx) in summary.reservoir_data.C"
                  :key="idx"
                  class="flex items-center justify-between bg-white dark:bg-gray-700/50 rounded-lg px-3 py-2 border border-warning-100 dark:border-warning-900/50"
                >
                  <span class="text-xs font-medium text-gray-700 dark:text-gray-300 truncate max-w-[120px]">
                    {{ item.name }}
                  </span>
                  <span class="text-xs font-bold text-warning-600 dark:text-warning-400 tabular-nums">
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

        <!-- جمع کل -->
        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-4 text-sm">
              <div class="flex items-center gap-2">
                <span class="text-gray-500 dark:text-gray-400">مجموع کل:</span>
                <span class="font-bold text-gray-900 dark:text-white tabular-nums">
                  {{ summary.total_reservoir_weight?.toFixed(2) }} گرم
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
      <!-- بخش 4: نکات و توصیه‌های سریع -->
      <!-- ============================================================ -->
      <div v-if="summary.recommendations?.length > 0" class="card border-l-4 border-l-primary-500">
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
            v-for="(rec, idx) in summary.recommendations"
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { apiService } from '@/services/apiService';

// ============================================================
// State - فقط داده‌های دریافتی از API
// ============================================================
const summary = ref<any>(null);
const isLoading = ref(true);
const error = ref<string | null>(null);

// ============================================================
// Computed - فقط برای نمایش (بدون محاسبه)
// ============================================================
const ionBalanceStatus = computed(() => {
  if (!summary.value?.ion_balance) {
    return {
      borderClass: 'border-l-4 border-l-gray-300 dark:border-l-gray-600',
      bgClass: 'bg-gray-100 dark:bg-gray-700',
      iconClass: 'text-gray-500 dark:text-gray-400',
      badgeClass: 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
    };
  }
  if (summary.value.ion_balance.is_balanced) {
    return {
      borderClass: 'border-l-4 border-l-success-500',
      bgClass: 'bg-success-50 dark:bg-success-900/30',
      iconClass: 'text-success-600 dark:text-success-400',
      badgeClass: 'bg-success-100 dark:bg-success-900/50 text-success-700 dark:text-success-400'
    };
  } else {
    return {
      borderClass: 'border-l-4 border-l-danger-500',
      bgClass: 'bg-danger-50 dark:bg-danger-900/30',
      iconClass: 'text-danger-600 dark:text-danger-400',
      badgeClass: 'bg-danger-100 dark:bg-danger-900/50 text-danger-700 dark:text-danger-400'
    };
  }
});

// ============================================================
// Methods - فقط برای نمایش و فرمت‌بندی
// ============================================================
const loadData = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const data = await apiService.getHomeSummary();
    summary.value = data;
  } catch (err: any) {
    error.value = err.message || 'خطا در بارگذاری داده‌ها از سرور';
    console.error('Error loading home summary:', err);
  } finally {
    isLoading.value = false;
  }
};

// 🆕 Event handler برای بارگذاری مجدد داده‌ها
// این handler زمانی فراخوانی می‌شود که گزارش جدید ایجاد شود یا گزارش موجود بارگذاری شود
const handleReportChanged = () => {
  console.log('📊 Report changed, reloading home summary...');
  loadData();
};

const getReservoirTotal = (reservoir: 'A' | 'B' | 'C'): number => {
  const data = summary.value?.reservoir_data?.[reservoir];
  if (!data || !Array.isArray(data) || data.length === 0) return 0;
  return data.reduce((sum: number, item: any) => sum + (item.amount || 0), 0);
};

const formatNumber = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '0.00';
  return Number(value).toFixed(2);
};

const formatCurrency = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '0';
  return Math.round(value).toLocaleString('fa-IR');
};

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
  const secondaryElements = ['Na', 'Cl'];
  const microElements = ['Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];
  
  if (macroElements.includes(element)) {
    return 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400';
  } else if (secondaryElements.includes(element)) {
    return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400';
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
// Lifecycle
// ============================================================
onMounted(() => {
  loadData();
  // 🆕 گوش دادن به رویداد تغییر گزارش
  // این رویداد از AppHeader ارسال می‌شود
  window.addEventListener('report-changed', handleReportChanged);
});

onUnmounted(() => {
  // 🆕 حذف event listener برای جلوگیری از memory leak
  window.removeEventListener('report-changed', handleReportChanged);
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