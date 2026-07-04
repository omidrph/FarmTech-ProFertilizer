<!-- frontend/src/components/features/calc/OptimizationResult.vue -->
<template>
  <div v-if="result" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    
    <!-- ============================================================ -->
    <!-- هدر نتیجه -->
    <!-- ============================================================ -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-l from-primary-50 to-indigo-50 dark:from-primary-900/20 dark:to-indigo-900/20">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">
            نتیجه بهینه‌سازی
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mr-2">
              (خطای کل: {{ (result.residual_error * 100).toFixed(2) }}%)
            </span>
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <span v-if="result.is_converged" class="text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              همگرایی موفق
            </span>
            <span v-else class="text-warning-600 dark:text-warning-400 flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              همگرایی کامل نشد
            </span>
            <span class="text-gray-400">•</span>
            <span>{{ result.iterations }} تکرار</span>
            <span class="text-gray-400">•</span>
            <span>{{ result.convergence_time_ms.toFixed(0) }}ms</span>
          </p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بدنه نتیجه -->
    <!-- ============================================================ -->
    <div class="p-4 space-y-4">
      
      <!-- ============================================================ -->
      <!-- بخش EC و pH نهایی -->
      <!-- ============================================================ -->
      <div v-if="result.ec !== undefined || result.ph !== undefined">
        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          پارامترهای محلول نهایی
        </h4>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <!-- EC -->
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 border border-blue-200 dark:border-blue-800">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">EC نهایی</p>
                <p class="text-xl font-bold text-blue-600 dark:text-blue-400 tabular-nums" style="font-family: 'Vazirmatn', sans-serif;">
                  {{ result.ec.toFixed(2) }}
                </p>
                <p class="text-[10px] text-gray-400">dS/m</p>
              </div>
              <div class="flex flex-col items-end">
                <span 
                  class="px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="getEcStatusClass(result.ec_status)"
                >
                  {{ result.ec_status || 'نامشخص' }}
                </span>
                <span class="text-[10px] text-gray-400 mt-1">
                  محدوده: 0.8 - 2.5
                </span>
              </div>
            </div>
          </div>
          
          <!-- pH -->
          <div class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3 border border-purple-200 dark:border-purple-800">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">pH نهایی</p>
                <p class="text-xl font-bold text-purple-600 dark:text-purple-400 tabular-nums" style="font-family: 'Vazirmatn', sans-serif;">
                  {{ result.ph.toFixed(2) }}
                </p>
                <p class="text-[10px] text-gray-400">pH</p>
              </div>
              <div class="flex flex-col items-end">
                <span 
                  class="px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="getPhStatusClass(result.ph_status)"
                >
                  {{ result.ph_status || 'نامشخص' }}
                </span>
                <span class="text-[10px] text-gray-400 mt-1">
                  محدوده: 5.5 - 6.5
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- وضعیت ترکیبی -->
        <div 
          v-if="result.ec_ph_status && result.ec_ph_status.message"
          class="mt-2 p-2 rounded-lg text-sm"
          :class="getEcPhStatusClass(result.ec_ph_status.color)"
        >
          <div class="flex items-start gap-2">
            <span v-html="getEcPhStatusIcon(result.ec_ph_status.color)"></span>
            <div>
              <p class="font-medium">{{ result.ec_ph_status.message }}</p>
              <div v-if="result.ec_ph_status.recommendations && result.ec_ph_status.recommendations.length > 0" class="mt-1">
                <p class="text-xs opacity-80">توصیه‌ها:</p>
                <ul class="text-xs opacity-80 list-disc list-inside mr-4">
                  <li v-for="rec in result.ec_ph_status.recommendations" :key="rec">{{ rec }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- ============================================================ -->
      <!-- بخش 1: جدول مقدار کودها برای ساخت استوک -->
      <!-- ============================================================ -->
      <div>
        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          مقدار کودها برای ساخت استوک
          <span class="text-xs font-normal text-gray-400 mr-2">
            ({{ usedFertilizersCount }} کود استفاده شده)
          </span>
        </h4>
        
        <div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-50 dark:bg-gray-700/50">
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
                  <div class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                    نام کود
                  </div>
                </th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
                  <div class="flex items-center justify-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                    </svg>
                    وزن (گرم)
                  </div>
                </th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
                  <div class="flex items-center justify-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    هزینه (تومان)
                  </div>
                </th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
                  <div class="flex items-center justify-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    مخزن
                  </div>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
              <tr 
                v-for="(weight, fertilizerId) in filteredWeights" 
                :key="fertilizerId"
                class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors"
              >
                <td class="px-4 py-2.5 text-right">
                  <div class="flex items-center gap-2">
                    <span 
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :class="getFertilizerAcid(fertilizerId) ? 'bg-warning-500' : 'bg-primary-500'"
                    ></span>
                    <span class="font-medium text-gray-900 dark:text-white">{{ getFertilizerName(fertilizerId) }}</span>
                    <span 
                      v-if="getFertilizerAcid(fertilizerId)" 
                      class="text-[9px] px-1.5 py-0.5 bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 rounded-full"
                    >
                      اسید
                    </span>
                  </div>
                </td>
                <td class="px-4 py-2.5 text-center font-mono tabular-nums font-semibold text-gray-900 dark:text-white" style="font-family: 'Vazirmatn', sans-serif;">
                  {{ weight.toFixed(3) }}
                </td>
                <td class="px-4 py-2.5 text-center font-mono tabular-nums font-semibold text-gray-900 dark:text-white" style="font-family: 'Vazirmatn', sans-serif;">
                  {{ formatCurrency(getFertilizerCost(fertilizerId, weight)) }}
                </td>
                <td class="px-4 py-2.5 text-center">
                  <span 
                    class="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium"
                    :class="getFertilizerTankClass(fertilizerId)"
                  >
                    {{ getFertilizerTankName(fertilizerId) }}
                  </span>
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="bg-gray-50 dark:bg-gray-700/50 border-t-2 border-gray-200 dark:border-gray-600">
                <td colspan="2" class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300">
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    مجموع هزینه
                  </div>
                </td>
                <td colspan="2" class="px-4 py-3 text-center font-bold text-emerald-600 dark:text-emerald-400 tabular-nums text-base" style="font-family: 'Vazirmatn', sans-serif;">
                  {{ formatCurrency(result.cost_total) }} تومان
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
        
        <!-- نمایش تعداد کودهای استفاده نشده -->
        <div v-if="unusedFertilizersCount > 0" class="mt-2 text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
          <svg class="w-4 h-4 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ unusedFertilizersCount }} کود انتخاب شده اما در ترکیب نهایی استفاده نشدند</span>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 2: مقایسه عناصر هدف و تامین شده (طراحی جدید با نمایش خطا) -->
      <!-- ============================================================ -->
      <div>
        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          مقایسه عناصر هدف و تامین شده
          <span class="text-xs font-normal text-gray-400 mr-2">
            (واحد: PPM)
          </span>
        </h4>

        <!-- گرید نمایش عناصر با طراحی جدید -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-3">
          <div
            v-for="(error, element) in elementErrors"
            :key="element"
            class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-3 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-shadow"
          >
            <!-- سطر اول: نام عنصر و درصد خطا -->
            <div class="flex items-center justify-between mb-1">
              <span class="text-sm font-bold text-gray-800 dark:text-gray-200">{{ element }}</span>
              <span 
                class="text-sm font-bold tabular-nums"
                :class="getErrorTextClass(error)"
                style="font-family: 'Vazirmatn', sans-serif;"
              >
                {{ getErrorDisplay(error) }}
              </span>
            </div>

            <!-- نوار پیشرفت نمایش خطا (با جهت‌دار بودن) -->
            <div class="relative w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
              <div
                class="absolute top-0 h-full rounded-full transition-all duration-700 ease-out"
                :class="getErrorBarClass(error)"
                :style="getErrorBarStyle(error)"
              ></div>
              <!-- خط وسط برای نشان دادن مرز صفر -->
              <div class="absolute top-0 left-1/2 w-0.5 h-full bg-gray-400/50 dark:bg-gray-500/50 z-10"></div>
            </div>

            <!-- مقادیر عددی هدف و تامین -->
            <div class="flex justify-between mt-1.5 text-[10px]">
              <span class="text-blue-600 dark:text-blue-400 font-medium">
                هدف: {{ getTargetValue(element) }}
              </span>
              <span 
                class="font-medium"
                :class="getActualValueClass(element)"
              >
                تامین: {{ getActualValue(element) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 3: تعادل یونی -->
      <!-- ============================================================ -->
      <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">تعادل یونی</span>
          </div>
          <div class="flex items-center gap-4 text-sm flex-wrap">
            <span class="text-gray-600 dark:text-gray-400">
              کاتیون: <strong class="text-blue-600 dark:text-blue-400 tabular-nums" style="font-family: 'Vazirmatn', sans-serif;">{{ result.ion_balance.cation.toFixed(2) }}</strong> meq/L
            </span>
            <span class="text-gray-600 dark:text-gray-400">
              آنیون: <strong class="text-purple-600 dark:text-purple-400 tabular-nums" style="font-family: 'Vazirmatn', sans-serif;">{{ result.ion_balance.anion.toFixed(2) }}</strong> meq/L
            </span>
            <span
              class="px-2 py-0.5 rounded-full text-xs font-medium flex items-center gap-1"
              :class="result.ion_balance.isBalanced
                ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
                : 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400'"
            >
              <svg v-if="result.ion_balance.isBalanced" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              {{ result.ion_balance.isBalanced ? 'متعادل' : 'نامتعادل' }}
              <span v-if="!result.ion_balance.isBalanced" class="text-[10px]">
                (اختلاف: {{ Math.abs(result.ion_balance.cation - result.ion_balance.anion).toFixed(2) }} meq/L)
              </span>
            </span>
          </div>
        </div>
        
        <div class="mt-2">
          <div class="relative w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
            <div class="absolute inset-0 flex">
              <div 
                class="h-full bg-blue-500 rounded-l-full transition-all duration-500"
                :style="{ width: getIonBalancePercent('cation') + '%' }"
              ></div>
              <div 
                class="h-full bg-purple-500 rounded-r-full transition-all duration-500"
                :style="{ width: getIonBalancePercent('anion') + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- ============================================================ -->
      <!-- بخش 4: هشدارها و پیشنهادات -->
      <!-- ============================================================ -->
      <div v-if="result.warnings.length > 0 || result.suggestions.length > 0" class="space-y-2">
        
        <div v-if="result.warnings.length > 0" class="bg-warning-50 dark:bg-warning-900/20 border-r-4 border-warning-500 rounded-lg p-3">
          <div class="flex items-start gap-2">
            <svg class="w-5 h-5 text-warning-600 dark:text-warning-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-warning-700 dark:text-warning-400 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                هشدارها
              </p>
              <ul class="text-sm text-warning-600 dark:text-warning-300 space-y-0.5 mr-4 list-disc list-inside">
                <li v-for="warning in result.warnings" :key="warning">{{ warning }}</li>
              </ul>
            </div>
          </div>
        </div>

        <div v-if="result.suggestions.length > 0" class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-3">
          <div class="flex items-start gap-2">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-primary-700 dark:text-primary-400 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                پیشنهادات
              </p>
              <ul class="text-sm text-primary-600 dark:text-primary-300 space-y-0.5 mr-4 list-disc list-inside">
                <li v-for="suggestion in result.suggestions" :key="suggestion">{{ suggestion }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OptimizationResponse } from '@/types';

// ===== Props =====
interface Props {
  result: OptimizationResponse | null;
  fertilizers: any[];
  targetValues: Record<string, number>;
}

const props = defineProps<Props>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'save'): void;
  (e: 'export-csv'): void;
}>();

// ===== Computed =====
const result = computed(() => props.result);

const filteredWeights = computed(() => {
  if (!result.value) return {};
  const weights = result.value.weights || {};
  const filtered: Record<string, number> = {};
  for (const [key, value] of Object.entries(weights)) {
    if (value !== undefined && value !== null && typeof value === 'number' && value > 0) {
      filtered[key] = value;
    }
  }
  return filtered;
});

const usedFertilizersCount = computed(() => {
  return Object.keys(filteredWeights.value).length;
});

const unusedFertilizersCount = computed(() => {
  if (!result.value) return 0;
  const weights = result.value.weights || {};
  let total = 0;
  for (const [, value] of Object.entries(weights)) {
    if (value !== undefined && value !== null && typeof value === 'number') {
      total++;
    }
  }
  return total - usedFertilizersCount.value;
});

// محاسبه خطا برای هر عنصر
const elementErrors = computed(() => {
  const errors: Record<string, number> = {};
  if (!result.value || !props.targetValues) return errors;
  
  for (const [element, target] of Object.entries(props.targetValues)) {
    const actual = result.value.concentrations[element] || 0;
    if (target > 0) {
      errors[element] = ((actual - target) / target) * 100;
    } else {
      errors[element] = 0;
    }
  }
  return errors;
});

// ===== Methods =====

// توابع مربوط به کودها
const getFertilizerName = (fertilizerId: string): string => {
  const fert = props.fertilizers.find(f => f.id === fertilizerId);
  return fert?.name || fertilizerId;
};

const getFertilizerAcid = (fertilizerId: string): boolean => {
  const fert = props.fertilizers.find(f => f.id === fertilizerId);
  return fert?.isAcid || false;
};

const getFertilizerCost = (fertilizerId: string, weight: number): number => {
  const fert = props.fertilizers.find(f => f.id === fertilizerId);
  if (!fert) return 0;
  return (weight / 1000) * (fert.pricePerKg || 0);
};

const getFertilizerTankName = (fertilizerId: string): string => {
  const fert = props.fertilizers.find(f => f.id === fertilizerId);
  return fert?.tankName || 'مخزن A';
};

const getFertilizerTankClass = (fertilizerId: string): string => {
  const fert = props.fertilizers.find(f => f.id === fertilizerId);
  const tank = fert?.tankName || 'مخزن A';
  const classes: Record<string, string> = {
    'مخزن A': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    'مخزن B': 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    'مخزن C': 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
    'مخزن D': 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
  };
  return classes[tank] || 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
};

// توابع مربوط به عناصر
const getTargetValue = (element: string): string => {
  if (!props.targetValues) return '0';
  const value = props.targetValues[element];
  if (value === undefined || value === null || typeof value !== 'number') return '0';
  return value.toFixed(1);
};

const getActualValue = (element: string): string => {
  if (!result.value) return '0';
  const value = result.value.concentrations[element];
  if (value === undefined || value === null || typeof value !== 'number') return '0';
  return value.toFixed(1);
};

// ============================================================
// توابع جدید برای نمایش زیبای خطا
// ============================================================

// ۱. نمایش عدد خطا با علامت مثبت/منفی
const getErrorDisplay = (error: number): string => {
  if (Math.abs(error) < 0.01) return '۰%';
  if (error > 0) return `+${error.toFixed(1)}%`;
  return `${error.toFixed(1)}%`;
};

// ۲. رنگ متن خطا بر اساس شدت
const getErrorTextClass = (error: number): string => {
  const absError = Math.abs(error);
  if (absError <= 0.5) return 'text-emerald-600 dark:text-emerald-400';
  if (absError <= 3) return 'text-emerald-500 dark:text-emerald-300';
  if (absError <= 7) return 'text-amber-500 dark:text-amber-400';
  if (absError <= 12) return 'text-orange-500 dark:text-orange-400';
  return 'text-rose-600 dark:text-rose-400';
};

// ۳. کلاس نوار بر اساس نوع خطا (مثبت/منفی/صفر)
const getErrorBarClass = (error: number): string => {
  const absError = Math.abs(error);
  if (absError <= 0.5) return 'bg-emerald-500';
  if (error > 0) return 'bg-rose-500';
  return 'bg-amber-500';
};

// ۴. استایل نوار (موقعیت و اندازه)
const getErrorBarStyle = (error: number): Record<string, string> => {
  const absError = Math.min(Math.abs(error), 20);
  const percentage = (absError / 20) * 50;

  if (Math.abs(error) < 0.01) {
    return { width: '100%', left: '0%' };
  }

  if (error > 0) {
    return { 
      width: `${percentage}%`, 
      left: '50%',
      borderRadius: '0 999px 999px 0'
    };
  } else {
    return { 
      width: `${percentage}%`, 
      left: `${50 - percentage}%`,
      borderRadius: '999px 0 0 999px'
    };
  }
};

// ۵. رنگ متن مقدار تامین شده (سبز اگر دقیق، نارنجی اگر خطا دارد)
const getActualValueClass = (element: string): string => {
  const error = elementErrors.value[element] || 0;
  if (Math.abs(error) <= 0.5) return 'text-emerald-600 dark:text-emerald-400';
  return 'text-amber-600 dark:text-amber-400';
};

// توابع مربوط به EC و pH
const getEcStatusClass = (status: string): string => {
  const classes: Record<string, string> = {
    'مطلوب': 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400',
    'کم': 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400',
    'بالا': 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400',
    'بحرانی': 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400'
  };
  return classes[status] || 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
};

const getPhStatusClass = (status: string): string => {
  const classes: Record<string, string> = {
    'مطلوب': 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400',
    'اسیدی': 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400',
    'قلیایی': 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400',
    'بسیار اسیدی': 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400',
    'بسیار قلیایی': 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400'
  };
  return classes[status] || 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
};

const getEcPhStatusClass = (color: string): string => {
  const classes: Record<string, string> = {
    'success': 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-500',
    'warning': 'bg-warning-50 dark:bg-warning-900/20 border-warning-500',
    'danger': 'bg-danger-50 dark:bg-danger-900/20 border-danger-500'
  };
  return classes[color] || 'bg-gray-50 dark:bg-gray-800 border-gray-400';
};

const getEcPhStatusIcon = (color: string): string => {
  const icons: Record<string, string> = {
    'success': `<svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`,
    'warning': `<svg class="w-5 h-5 text-warning-600 dark:text-warning-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
    'danger': `<svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
  };
  return icons[color] || '';
};

const getIonBalancePercent = (type: 'cation' | 'anion'): number => {
  if (!result.value) return 50;
  const cation = result.value.ion_balance.cation || 0;
  const anion = result.value.ion_balance.anion || 0;
  const total = cation + anion;
  if (total === 0) return 50;
  if (type === 'cation') {
    return (cation / total) * 100;
  } else {
    return (anion / total) * 100;
  }
};

const formatCurrency = (value: number): string => {
  if (value === undefined || value === null || isNaN(value)) return '۰';
  return Math.round(value).toLocaleString('fa-IR');
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