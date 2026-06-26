<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات (ادغام شده) -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
        مقادیر مورد نظر خود را برای هر عنصر در جدول زیر وارد کنید. نرم‌افزار به صورت خودکار تعادل یونی را بررسی می‌کند.
        همچنین می‌توانید از رسپی‌های آماده (سیستمی) استفاده کنید یا رسپی‌های شخصی خود را بسازید، ویرایش و مدیریت کنید.
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- جدول عناصر هدف -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">ورود عناصر هدف</h3>
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 dark:text-gray-400">واحد:</label>
          <select
            :value="targetUnit"
            @change="updateTargetUnit($event)"
            class="px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
          >
            <option value="ppm">PPM/L</option>
            <option value="meq">MEQ/L</option>
            <option value="mmol">MMOLS/L</option>
          </select>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr>
              <th class="px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">
                عنصر
              </th>
              <th v-for="element in elements" :key="element" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[70px]">
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400 text-xs">
                مقدار هدف
              </td>
              <td v-for="element in elements" :key="'value-'+element" class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center">
                <input
                  type="number"
                  :value="getElementValue(element)"
                  @input="updateElementValue(element, $event)"
                  step="0.001"
                  min="0"
                  class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                  placeholder="۰"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- دکمه‌های اقدام -->
      <div class="flex flex-wrap gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <button
          @click="saveTargets"
          :disabled="isSaving"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="!isSaving" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isSaving ? 'در حال ذخیره...' : 'ذخیره عناصر هدف' }}
        </button>
        <button
          @click="resetTargets"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          بازنشانی همه
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- تعادل کاتیون و آنیون (مینیمال و حرفه‌ای) -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- محتوای بدون هدر -->
      <div class="p-5">
        <!-- Loading State -->
        <div v-if="targetStore.isCalculatingBalance" class="flex items-center justify-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="mr-3 text-gray-600 dark:text-gray-400 text-sm">در حال محاسبه تعادل یونی...</span>
        </div>

        <!-- Data Display -->
        <div v-else>
          <!-- کارت‌های آماری مینیمال -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <!-- کاتیون -->
            <div class="bg-blue-50/30 dark:bg-blue-900/10 rounded-lg p-3 border border-blue-100 dark:border-blue-800/20">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 font-medium">کاتیون</p>
                  <p class="text-xl font-bold text-blue-600 dark:text-blue-400 tabular-nums">
                    {{ ionBalance.cation.toFixed(2) }}
                  </p>
                </div>
                <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">meq/L</p>
            </div>

            <!-- آنیون -->
            <div class="bg-purple-50/30 dark:bg-purple-900/10 rounded-lg p-3 border border-purple-100 dark:border-purple-800/20">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 font-medium">آنیون</p>
                  <p class="text-xl font-bold text-purple-600 dark:text-purple-400 tabular-nums">
                    {{ ionBalance.anion.toFixed(2) }}
                  </p>
                </div>
                <div class="w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                  <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">meq/L</p>
            </div>

            <!-- وضعیت نهایی -->
            <div class="bg-gray-50/30 dark:bg-gray-800/30 rounded-lg p-3 border border-gray-100 dark:border-gray-700/30">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 font-medium">وضعیت</p>
                  <p class="text-sm font-bold" :class="ionBalance.isBalanced ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                    {{ ionBalance.isBalanced ? '✓ متعادل' : '✗ نامتعادل' }}
                  </p>
                </div>
                <div class="w-8 h-8 rounded-full flex items-center justify-center"
                  :class="ionBalance.isBalanced ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'"
                >
                  <svg class="w-4 h-4" :class="ionBalance.isBalanced ? 'text-green-500' : 'text-red-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="ionBalance.isBalanced" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                  </svg>
                </div>
              </div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-1">
                اختلاف: {{ Math.abs(ionBalance.cation - ionBalance.anion).toFixed(2) }} meq/L
              </p>
            </div>
          </div>

          <!-- نوار پیشرفت تعادل (مینیمال) -->
          <div class="mt-4">
            <div class="flex items-center justify-between text-xs text-gray-400 dark:text-gray-500 mb-1">
              <span class="text-blue-500">کاتیون</span>
              <span class="text-purple-500">آنیون</span>
            </div>
            <div class="relative w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
              <div class="absolute inset-0 flex items-center">
                <div 
                  class="h-full bg-blue-500 rounded-full transition-all duration-500"
                  :style="{ width: Math.min((ionBalance.cation / (ionBalance.cation + ionBalance.anion + 0.01)) * 100, 100) + '%' }"
                ></div>
                <div 
                  class="h-full bg-purple-500 rounded-full transition-all duration-500"
                  :style="{ width: Math.min((ionBalance.anion / (ionBalance.cation + ionBalance.anion + 0.01)) * 100, 100) + '%', marginLeft: 'auto' }"
                ></div>
              </div>
            </div>
            <div class="flex items-center justify-between text-[10px] text-gray-400 dark:text-gray-500 mt-1">
              <span>0</span>
              <span>تعادل</span>
              <span>{{ (ionBalance.cation + ionBalance.anion).toFixed(2) }} meq/L</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بخش مدیریت رسپی‌ها (بعد از کاتیون و آنیون) -->
    <!-- ============================================================ -->
    <RecipeManager @recipe-applied="loadConvertedValues" />

    <!-- ============================================================ -->
    <!-- جدول توازن عناصر (تبدیل واحدها از API) -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">جدول توازن عناصر</h3>
        <button
          @click="loadConvertedValues"
          :disabled="isConverting"
          class="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm flex items-center gap-2 disabled:opacity-50"
        >
          <svg v-if="!isConverting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isConverting ? 'در حال تبدیل...' : 'به‌روزرسانی' }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isConverting && !convertedValues" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span class="mr-2 text-gray-600 dark:text-gray-400">در حال تبدیل واحدها...</span>
      </div>

      <!-- Data Display -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr>
              <th class="px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">
                واحد
              </th>
              <th v-for="element in elements" :key="element" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[70px]">
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">PPM/L</td>
              <td v-for="element in elements" :key="'ppm-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center tabular-nums">
                {{ getConvertedValue(element, 'ppm') }}
              </td>
            </tr>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">MEQ/L</td>
              <td v-for="element in elements" :key="'meq-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center tabular-nums">
                {{ getConvertedValue(element, 'meq') }}
              </td>
            </tr>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">MMOLS/L</td>
              <td v-for="element in elements" :key="'mmol-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center tabular-nums">
                {{ getConvertedValue(element, 'mmol') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام موفقیت (Toast) -->
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

    <!-- ============================================================ -->
    <!-- پیام موفقیت (قدیمی - برای سازگاری) -->
    <!-- ============================================================ -->
    <div v-if="saveSuccess" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-4 animate-fade-in">
      <p class="text-success-700 dark:text-success-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        عناصر هدف با موفقیت ذخیره شدند!
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- پیام خطا -->
    <!-- ============================================================ -->
    <div v-if="errorMessage" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <p class="text-danger-700 dark:text-danger-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ errorMessage }}
      </p>
      <button @click="errorMessage = null" class="text-xs text-danger-600 hover:text-danger-800 mt-1">بستن</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useReportStore } from '@/store/modules/reportStore';
import { apiService } from '@/services/apiService';
import RecipeManager from './RecipeManager.vue';

// ===== Stores =====
const targetStore = useTargetStore();
const reportStore = useReportStore();

// ===== State =====
const saveSuccess = ref(false);
const isSaving = ref(false);
const isConverting = ref(false);
const errorMessage = ref<string | null>(null);
const convertedValues = ref<Record<string, Record<string, number>> | null>(null);

// ===== Toast State =====
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const targetUnit = computed({
  get: () => targetStore.targetUnit,
  set: (val: any) => targetStore.setTargetUnit(val)
});

const targetValues = computed(() => targetStore.targetElements);
const ionBalance = computed(() => targetStore.ionBalance);

// ===== Toast Functions =====
const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

// ===== Methods =====

/**
 * دریافت مقدار یک عنصر
 */
const getElementValue = (element: string): number => {
  return (targetValues.value as any)[element] || 0;
};

/**
 * به‌روزرسانی مقدار یک عنصر
 */
const updateElementValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  targetStore.setTargetElement(element as any, value);
};

/**
 * تغییر واحد
 */
const updateTargetUnit = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  targetStore.setTargetUnit(target.value as any);
  loadConvertedValues();
};

/**
 * ذخیره عناصر هدف
 */
const saveTargets = async () => {
  saveSuccess.value = false;
  errorMessage.value = null;
  isSaving.value = true;

  try {
    // بررسی اینکه آیا حداقل یک عنصر با مقدار مثبت وجود دارد
    const hasPositiveValue = Object.values(targetValues.value).some(v => v > 0);
    if (!hasPositiveValue) {
      showToast('لطفاً حداقل یک عنصر با مقدار مثبت وارد کنید', 'error');
      return;
    }

    // اگر گزارش وجود نداشت، یک گزارش جدید ایجاد کن
    if (!reportStore.reportData.reportName) {
      reportStore.updateReportData({
        reportName: `گزارش ${new Date().toLocaleDateString('fa-IR')}`,
        date: new Date().toLocaleDateString('fa-IR')
      });
    }

    // ذخیره گزارش
    const success = await reportStore.saveCurrentReport();
    
    if (success) {
      saveSuccess.value = true;
      showToast('✅ عناصر هدف با موفقیت ذخیره شدند!', 'success');
      
      // پس از 3 ثانیه پیام موفقیت را مخفی کن
      setTimeout(() => {
        saveSuccess.value = false;
      }, 3000);
    } else {
      showToast('❌ خطا در ذخیره عناصر هدف: ' + (reportStore.error || 'خطای ناشناخته'), 'error');
    }
  } catch (error: any) {
    console.error('خطا در ذخیره عناصر هدف:', error);
    errorMessage.value = 'خطا در ذخیره عناصر هدف. لطفاً دوباره تلاش کنید.';
    showToast('❌ خطا در ذخیره عناصر هدف', 'error');
  } finally {
    isSaving.value = false;
  }
};

/**
 * بازنشانی تمام مقادیر
 */
const resetTargets = () => {
  targetStore.resetTargets();
  convertedValues.value = null;
  showToast('همه مقادیر بازنشانی شدند', 'success');
};

/**
 * دریافت مقادیر تبدیل شده از API
 */
const loadConvertedValues = async () => {
  isConverting.value = true;
  errorMessage.value = null;

  try {
    const result: Record<string, Record<string, number>> = {};

    for (const element of elements) {
      const value = getElementValue(element);
      if (value === 0) {
        result[element] = {
          ppm: 0,
          meq: 0,
          mmol: 0
        };
        continue;
      }

      const ppmResult = await apiService.convertUnit({
        value,
        from_unit: targetStore.targetUnit,
        to_unit: 'ppm',
        element
      });

      const meqResult = await apiService.convertUnit({
        value: ppmResult.converted_value,
        from_unit: 'ppm',
        to_unit: 'meq',
        element
      });

      const mmolResult = await apiService.convertUnit({
        value: ppmResult.converted_value,
        from_unit: 'ppm',
        to_unit: 'mmol',
        element
      });

      result[element] = {
        ppm: ppmResult.converted_value,
        meq: meqResult.converted_value,
        mmol: mmolResult.converted_value
      };
    }

    convertedValues.value = result;
  } catch (error: any) {
    console.error('خطا در تبدیل واحدها:', error);
    errorMessage.value = 'خطا در تبدیل واحدها. لطفاً دوباره تلاش کنید.';
    showToast('❌ خطا در تبدیل واحدها', 'error');
  } finally {
    isConverting.value = false;
  }
};

/**
 * دریافت مقدار تبدیل شده برای یک عنصر و واحد خاص
 */
const getConvertedValue = (element: string, unit: string): string => {
  if (!convertedValues.value || !convertedValues.value[element]) {
    return '0.00';
  }

  const value = convertedValues.value[element][unit];
  if (value === undefined || value === null) {
    return '0.00';
  }

  return value.toFixed(3);
};

// ===== Watchers =====
watch(targetValues, () => {
  setTimeout(() => {
    if (convertedValues.value) {
      loadConvertedValues();
    }
  }, 500);
}, { deep: true });

// ===== Lifecycle =====
onMounted(() => {
  loadConvertedValues();
});
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}
</style>