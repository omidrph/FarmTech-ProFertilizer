<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
        </div>
        <div>
          <p class="text-gray-700 dark:text-gray-300 text-sm">
            کود مورد نظر خود را جهت افزودن و محاسبه انتخاب کرده و دکمه افزودن را بزنید.
          </p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- کنترل‌ها -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 space-y-4">
      <div class="flex items-center gap-2 mb-2">
        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
        </svg>
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">تنظیمات محاسبه</h3>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <!-- انتخاب کود -->
        <div class="lg:col-span-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
              </svg>
              انتخاب کود
            </div>
          </label>
          <select
            :value="selectedFertilizers"
            @change="updateSelectedFertilizers($event)"
            multiple
            class="w-full min-h-[100px] px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          >
            <option v-for="f in fertilizers" :key="f.id" :value="f.id">
              {{ f.name }} {{ f.isAcid ? '(اسید)' : '' }}
            </option>
          </select>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 flex items-center gap-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            برای انتخاب چند کود، کلید Ctrl را نگه دارید
          </p>
        </div>

        <!-- دکمه افزودن -->
        <div class="flex items-end">
          <button
            @click="addFertilizersToCalc"
            :disabled="selectedFertilizers.length === 0"
            class="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            افزودن به جدول
          </button>
        </div>
      </div>

      <!-- تنظیمات حجم مخزن -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
              </svg>
              حجم مخزن (لیتر)
            </div>
          </label>
          <input
            type="number"
            :value="tankVolume"
            @input="updateTankVolume($event)"
            min="1"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              ضریب رقیق‌سازی
            </div>
          </label>
          <input
            type="number"
            :value="dilutionFactor"
            @input="updateDilutionFactor($event)"
            step="0.1"
            min="0.1"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
              مجموع (لیتر)
            </div>
          </label>
          <input
            type="text"
            :value="totalLiter"
            disabled
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed"
          />
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول محاسبه -->
    <!-- ============================================================ -->
    <div v-if="calcRows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- هدر جدول -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">جدول محاسبه کود</h3>
        </div>
        <span class="text-sm text-gray-500 dark:text-gray-400">{{ calcRows.length }} ردیف</span>
      </div>

      <!-- جدول با اسکرول افقی -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700/50">
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[130px]">
                ماده
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px]">
                <div class="flex items-center justify-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                  </svg>
                  وزن (گرم)
                </div>
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[90px]">
                خلوص (%)
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[110px]">
                <div class="flex items-center justify-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  هزینه (تومان)
                </div>
              </th>
              <th
                v-for="el in elements"
                :key="el"
                class="px-2 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[60px]"
              >
                {{ el }}
              </th>
              <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[70px]">
                عملیات
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="row in calcRows"
              :key="row.id"
              :class="[
                'hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors',
                row.isFixedRow ? 'bg-gray-50/50 dark:bg-gray-700/20' : ''
              ]"
            >
              <!-- نام ماده -->
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-3 py-2 text-right">
                <div class="flex items-center gap-2">
                  <div
                    class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="row.isAcid ? 'bg-warning-50 dark:bg-warning-900/30' : 'bg-primary-50 dark:bg-primary-900/30'"
                  >
                    <svg
                      class="w-4 h-4"
                      :class="row.isAcid ? 'text-warning-600 dark:text-warning-400' : 'text-primary-600 dark:text-primary-400'"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path v-if="row.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 dark:text-white text-sm truncate">{{ row.materialName }}</p>
                    <p v-if="row.isFixedRow" class="text-[10px] text-gray-400 dark:text-gray-500">ثابت</p>
                  </div>
                </div>
              </td>

              <!-- وزن -->
              <td class="px-3 py-2 text-center">
                <input
                  type="number"
                  :value="row.weight"
                  @input="updateRowWeight(row.id, $event)"
                  step="0.001"
                  min="0"
                  class="w-full max-w-[80px] px-2 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200 tabular-nums"
                />
              </td>

              <!-- خلوص -->
              <td class="px-3 py-2 text-center">
                <input
                  type="number"
                  :value="row.purity"
                  @input="updateRowPurity(row.id, $event)"
                  step="0.1"
                  min="0"
                  max="100"
                  class="w-full max-w-[70px] px-2 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200 tabular-nums"
                />
              </td>

              <!-- هزینه -->
              <td class="px-3 py-2 text-center">
                <span class="font-semibold text-gray-900 dark:text-white tabular-nums text-sm">
                  {{ row.cost ? Number(row.cost).toLocaleString('fa-IR') : '0' }}
                </span>
              </td>

              <!-- عناصر -->
              <td
                v-for="el in elements"
                :key="el"
                class="px-2 py-2 text-center text-xs font-mono tabular-nums text-gray-700 dark:text-gray-300"
              >
                {{ row.elements && row.elements[el] ? Number(row.elements[el]).toFixed(3) : '0.000' }}
              </td>

              <!-- عملیات -->
              <td class="px-3 py-2 text-center">
                <button
                  v-if="!row.isFixedRow"
                  @click="removeCalcRow(row.id)"
                  class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                  title="حذف"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
                <span v-else class="text-gray-300 dark:text-gray-600 text-xs">-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- خطاها -->
    <!-- ============================================================ -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <div class="flex-1 space-y-1">
          <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm">
            {{ err }}
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- دکمه‌های اقدام -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap gap-3">
        <button
          @click="calculateFertilizer"
          :disabled="isCalculating || calcRows.length === 0"
          class="px-4 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="!isCalculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isCalculating ? 'در حال محاسبه...' : 'محاسبه' }}
        </button>
        <button
          @click="resetFertilizerCalc"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          بازنشانی
        </button>
        <button
          @click="printReport"
          class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
          </svg>
          چاپ
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- خلاصه محاسبات -->
    <!-- ============================================================ -->
    <div v-if="calcRows.length > 0 && totalCost > 0" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">تعداد مواد</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ calcRows.length }}</p>
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">مجموع هزینه</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ Number(totalCost).toLocaleString('fa-IR') }} <span class="text-xs font-normal">تومان</span></p>
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">حجم کل</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ totalLiter }} <span class="text-xs font-normal">لیتر</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';
import { useCalculations } from '@/composables/useCalculations';

// ===== Props =====
const props = defineProps<{
  fertilizers: any[];
  selectedFertilizers: string[];
  tankVolume: number;
  dilutionFactor: number;
  calcRows: any[];
  calcErrors: string[];
}>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:tankVolume', value: number): void;
  (e: 'update:dilutionFactor', value: number): void;
  (e: 'update:calcRows', value: any[]): void;
  (e: 'update:calcErrors', value: string[]): void;
}>();

// ===== Store & Composables =====
const calcStore = useCalcStore();
const { calculateReservoir, isCalculating } = useCalculations();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const totalLiter = computed(() => props.tankVolume * props.dilutionFactor);
const totalCost = computed(() => {
  return props.calcRows.reduce((sum: number, row: any) => sum + (row.cost || 0), 0);
});

// ===== Methods =====
const updateSelectedFertilizers = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  const values = Array.from(target.selectedOptions).map(opt => opt.value);
  emit('update:selectedFertilizers', values);
};

const updateTankVolume = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:tankVolume', parseFloat(target.value) || 0);
};

const updateDilutionFactor = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:dilutionFactor', parseFloat(target.value) || 0);
};

const updateRowWeight = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, weight: value };
      if (updatedRow.elements) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (value * (pct as number / 100) * (updatedRow.purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      const fertilizer = props.fertilizers.find((f: any) => f.name === updatedRow.materialName);
      if (fertilizer) {
        updatedRow.cost = (value / 1000) * fertilizer.pricePerKg;
      }
      return updatedRow;
    }
    return row;
  });
  emit('update:calcRows', newRows);
};

const updateRowPurity = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, purity: value };
      if (updatedRow.elements && updatedRow.weight) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (updatedRow.weight * (pct as number / 100) * (value / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      return updatedRow;
    }
    return row;
  });
  emit('update:calcRows', newRows);
};

const addFertilizersToCalc = () => {
  const selected = props.fertilizers.filter((f: any) => props.selectedFertilizers.includes(f.id));
  const newRows = selected.map((f: any) => ({
    id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
    materialName: f.name,
    weight: 0,
    purity: f.isAcid ? (f.acidType === 'H3PO4' ? 85 : f.acidType === 'HNO3' ? 65 : 98) : 100,
    cost: 0,
    elements: { ...f.elements },
    isAcid: f.isAcid || false,
    acidType: f.acidType || null,
    isFixedRow: false,
    fertilizerId: f.id
  }));
  emit('update:calcRows', [...props.calcRows, ...newRows]);
  emit('update:selectedFertilizers', []);
};

const removeCalcRow = (id: string) => {
  emit('update:calcRows', props.calcRows.filter((r: any) => r.id !== id));
};

const calculateFertilizer = async () => {
  const errors: string[] = [];
  const newRows = props.calcRows.map((row: any) => {
    if (!row.isFixedRow) {
      if (!row.weight || row.weight <= 0) {
        errors.push(`وزن کود "${row.materialName}" را وارد کنید`);
      }
      if (!row.purity || row.purity <= 0 || row.purity > 100) {
        errors.push(`خلوص کود "${row.materialName}" باید بین 1 تا 100 باشد`);
      }
      if (row.weight && row.weight > 0) {
        const fertilizer = props.fertilizers.find((f: any) => f.name === row.materialName);
        if (fertilizer) {
          row.cost = (row.weight / 1000) * fertilizer.pricePerKg;
        }
      }
      if (row.elements && row.weight && row.purity) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(row.elements)) {
          if (pct) {
            newElements[el] = (row.weight * (pct as number / 100) * (row.purity / 100));
          }
        }
        row.elements = newElements;
      }
    }
    return row;
  });

  emit('update:calcRows', newRows);
  emit('update:calcErrors', errors);

  if (errors.length === 0) {
    calcStore.calculationRows = newRows;
    const fertilizers = newRows
      .filter(row => row.weight && row.weight > 0)
      .map(row => ({
        fertilizer: {
          name: row.materialName,
          is_acid: row.isAcid || false
        },
        weight: row.weight,
        purity: row.purity
      }));

    const reservoirResult = await calculateReservoir(fertilizers);
    if (reservoirResult) {
      calcStore.reservoirData = reservoirResult.reservoir_data;
    }
  }
};

const resetFertilizerCalc = () => {
  const fixedRows = [
    {
      id: 'fixed-h3po4',
      materialName: 'H3PO4',
      weight: 0,
      purity: 85,
      cost: 0,
      elements: {},
      isAcid: true,
      acidType: 'H3PO4',
      isFixedRow: true
    },
    {
      id: 'fixed-hno3',
      materialName: 'HNO3',
      weight: 0,
      purity: 65,
      cost: 0,
      elements: {},
      isAcid: true,
      acidType: 'HNO3',
      isFixedRow: true
    },
    {
      id: 'fixed-h2so4',
      materialName: 'H2SO4',
      weight: 0,
      purity: 98,
      cost: 0,
      elements: {},
      isAcid: true,
      acidType: 'H2SO4',
      isFixedRow: true
    }
  ];
  emit('update:calcRows', fixedRows);
  emit('update:calcErrors', []);
  emit('update:tankVolume', 1000);
  emit('update:dilutionFactor', 1);
  emit('update:selectedFertilizers', []);
};

const printReport = () => {
  window.print();
};
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

.dark .overflow-x-auto::-webkit-scrollbar-track {
  background: #374151;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>