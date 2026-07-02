<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات و وضعیت ذخیره‌سازی -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4 flex justify-between items-start">
      <div>
        <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
          مقادیر مورد نظر خود را برای هر عنصر در جدول زیر وارد کنید. نرم‌افزار به صورت خودکار تعادل یونی را بررسی می‌کند.
          <br>
          <span class="text-xs text-primary-600 dark:text-primary-400 font-medium mt-1 inline-block">
            تغییرات شما به صورت خودکار و لحظه‌ای ذخیره می‌شوند.
          </span>
        </p>
      </div>
      <!-- نشانگر وضعیت ذخیره‌سازی -->
      <div v-if="isSaving || saveStatus === 'success'" class="flex items-center gap-2 text-xs animate-fade-in flex-shrink-0">
        <span v-if="isSaving" class="flex items-center gap-1 text-gray-500 dark:text-gray-400">
          <svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          در حال ذخیره...
        </span>
        <span v-else-if="saveStatus === 'success'" class="flex items-center gap-1 text-success-600 dark:text-success-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          ذخیره شد
        </span>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نوار ابزار (واحد + دکمه بازنشانی) -->
    <!-- ============================================================ -->
    <div class="flex flex-wrap items-center gap-3 bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
      <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[200px]">
        <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2 whitespace-nowrap">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
            <circle cx="12" cy="12" r="6"/>
            <circle cx="12" cy="12" r="2"/>
          </svg>
          <span class="hidden xs:inline">عناصر هدف</span>
          <span class="xs:hidden">اهداف</span>
        </h3>
        
        <div class="flex items-center gap-1.5 mr-1 sm:mr-0">
          <label class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">واحد:</label>
          <select
            v-model="targetUnit"
            @change="handleUnitChange"
            class="px-1.5 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 transition-all"
          >
            <option value="ppm">PPM</option>
            <option value="meq">MEQ/L</option>
            <option value="mmol">MMOL/L</option>
          </select>
        </div>
      </div>

      <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap w-full sm:w-auto justify-end">
        <button
          @click="resetTargets"
          class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 min-w-[60px] sm:min-w-0"
          title="بازنشانی تمام مقادیر"
        >
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <span class="hidden xs:inline">بازنشانی همه</span>
          <span class="xs:hidden">بازنشانی</span>
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول عناصر هدف با رنگ‌آمیزی کاتیون و آنیون -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-sm border-collapse min-w-[700px]">
          <thead>
            <tr>
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px] shadow-sm">
                عنصر
              </th>
              <th 
                v-for="element in elements" 
                :key="element" 
                class="px-3 py-3 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[90px] transition-colors"
                :class="getElementHeaderClass(element)"
              >
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-primary-500"></span>
                  مقدار هدف
                </div>
              </td>
              <td 
                v-for="element in elements" 
                :key="'value-'+element" 
                class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center transition-colors"
                :class="getElementCellClass(element)"
              >
                <input
                  type="number"
                  :value="getDisplayValue(element)"
                  @input="updateElementValue(element, $event)"
                  step="0.001"
                  min="0"
                  class="w-full max-w-[80px] mx-auto px-2 py-1.5 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300"
                  placeholder="۰"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- ============================================================ -->
      <!-- راهنمای رنگ‌ها (بدون ایموجی و بدون توضیح اضافی) -->
      <!-- ============================================================ -->
      <div class="px-4 py-3 bg-gray-50 dark:bg-gray-700/30 border-t border-gray-200 dark:border-gray-600 flex flex-wrap items-center gap-4 text-xs">
        <span class="text-gray-600 dark:text-gray-400 font-medium">راهنما:</span>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-blue-500"></span>
          <span class="text-gray-600 dark:text-gray-400">کاتیون</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-red-500"></span>
          <span class="text-gray-600 dark:text-gray-400">آنیون</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-gray-400"></span>
          <span class="text-gray-600 dark:text-gray-400">خنثی</span>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- تعادل کاتیون و آنیون -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-4 sm:p-5">
        <div v-if="targetStore.isCalculatingBalance" class="flex items-center justify-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="mr-3 text-gray-600 dark:text-gray-400 text-sm">در حال محاسبه تعادل یونی...</span>
        </div>

        <div v-else>
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
                    {{ ionBalance.isBalanced ? 'متعادل' : 'نامتعادل' }}
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
    <!-- بخش مدیریت رسپی‌ها -->
    <!-- ============================================================ -->
    <RecipeManager @recipe-applied="handleRecipeApplied" />

    <!-- ============================================================ -->
    <!-- جدول توازن عناصر -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-4 sm:p-5">
        <div class="flex flex-wrap justify-between items-center mb-4 gap-3">
          <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            جدول توازن عناصر
          </h3>
          <button
            @click="loadConvertedValues"
            :disabled="isConverting"
            class="px-3 sm:px-4 py-1.5 sm:py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs sm:text-sm flex items-center gap-1.5 disabled:opacity-50 shadow-sm hover:shadow-md"
          >
            <svg v-if="!isConverting" class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <svg v-else class="animate-spin h-3.5 w-3.5 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <span class="hidden xs:inline">{{ isConverting ? 'در حال تبدیل...' : 'به‌روزرسانی' }}</span>
            <span class="xs:hidden">{{ isConverting ? '...' : 'بروزرسانی' }}</span>
          </button>
        </div>

        <div v-if="isConverting && !convertedValues" class="flex items-center justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <span class="mr-2 text-gray-600 dark:text-gray-400 text-sm">در حال تبدیل واحدها...</span>
        </div>

        <div v-else class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-sm border-collapse min-w-[600px]">
            <thead>
              <tr>
                <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px] shadow-sm">
                  واحد
                </th>
                <th v-for="element in elements" :key="element" class="px-3 py-3 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[70px]">
                  {{ element }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                  PPM/L
                </td>
                <td v-for="element in elements" :key="'ppm-'+element" class="px-3 py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300">
                  {{ getConvertedValue(element, 'ppm') }}
                </td>
              </tr>
              <tr>
                <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                  MEQ/L
                </td>
                <td v-for="element in elements" :key="'meq-'+element" class="px-3 py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300">
                  {{ getConvertedValue(element, 'meq') }}
                </td>
              </tr>
              <tr>
                <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                  MMOLS/L
                </td>
                <td v-for="element in elements" :key="'mmol-'+element" class="px-3 py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300">
                  {{ getConvertedValue(element, 'mmol') }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام Toast -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="toastMessage" class="fixed bottom-4 sm:bottom-6 left-1/2 -translate-x-1/2 z-[200] px-4 sm:px-6 py-2.5 sm:py-3 rounded-xl shadow-2xl flex items-center gap-2 sm:gap-3 text-xs sm:text-sm font-medium max-w-[90vw] sm:max-w-none"
          :class="toastType === 'success' ? 'bg-success-600 text-white' : 'bg-danger-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span class="text-center">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
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
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// Auto-save State
const isSaving = ref(false);
const saveStatus = ref<'idle' | 'saving' | 'success'>('idle');
let saveTimeout: ReturnType<typeof setTimeout> | null = null;

// Toast State
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

// Convert State
const isConverting = ref(false);
const convertedValues = ref<Record<string, Record<string, number>> | null>(null);

// ============================================================
// ✅ تعریف کاتیون‌ها و آنیون‌ها برای رنگ‌آمیزی
// ============================================================
const CATION_ELEMENTS = ['N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Fe', 'Mn', 'Zn', 'Cu'];
const ANION_ELEMENTS = ['N-NO3', 'P', 'S', 'Cl', 'B', 'Mo'];

// ===== Computed =====
const targetUnit = computed({
  get: () => targetStore.targetUnit,
  set: (val: any) => targetStore.setTargetUnit(val)
});

const targetValues = computed(() => targetStore.targetElements);
const ionBalance = computed(() => targetStore.ionBalance);

// ============================================================
// ✅ توابع رنگ‌آمیزی (بدون ایموجی)
// ============================================================

/**
 * تعیین نوع عنصر: cation, anion, neutral
 */
const getElementType = (element: string): 'cation' | 'anion' | 'neutral' => {
  if (CATION_ELEMENTS.includes(element)) return 'cation';
  if (ANION_ELEMENTS.includes(element)) return 'anion';
  return 'neutral';
};

/**
 * کلاس CSS برای هدر ستون
 */
const getElementHeaderClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300';
    case 'anion':
      return 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300';
    default:
      return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
  }
};

/**
 * کلاس CSS برای سلول جدول
 */
const getElementCellClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-50/30 dark:bg-blue-900/5';
    case 'anion':
      return 'bg-red-50/30 dark:bg-red-900/5';
    default:
      return '';
  }
};

// ============================================================
// توابع تبدیل واحد
// ============================================================

const ELEMENT_DATA: Record<string, { mw: number; valence: number }> = {
  'N-NO3': { mw: 62.0049, valence: 1 },
  'P': { mw: 30.9738, valence: 1 },
  'S': { mw: 32.065, valence: 1 },
  'N-NH4': { mw: 18.0385, valence: 1 },
  'K': { mw: 39.0983, valence: 1 },
  'Ca': { mw: 40.078, valence: 2 },
  'Mg': { mw: 24.305, valence: 2 },
  'Na': { mw: 22.9898, valence: 1 },
  'Cl': { mw: 35.453, valence: 1 },
  'Fe': { mw: 55.845, valence: 2 },
  'Mn': { mw: 54.938, valence: 2 },
  'Zn': { mw: 65.38, valence: 2 },
  'B': { mw: 10.81, valence: 1 },
  'Cu': { mw: 63.546, valence: 2 },
  'Mo': { mw: 95.95, valence: 2 }
};

function convertToDisplay(value: number, element: string, unit: string): number {
  if (!ELEMENT_DATA[element]) return value;
  const { mw, valence } = ELEMENT_DATA[element];

  if (unit === 'ppm') return value;
  if (unit === 'meq') return (value * valence) / mw;
  if (unit === 'mmol') return value / mw;
  return value;
}

function convertFromDisplay(displayValue: number, element: string, unit: string): number {
  if (!ELEMENT_DATA[element]) return displayValue;
  const { mw, valence } = ELEMENT_DATA[element];

  if (unit === 'ppm') return displayValue;
  if (unit === 'meq') return (displayValue * mw) / valence;
  if (unit === 'mmol') return displayValue * mw;
  return displayValue;
}

// ===== Methods =====

const getDisplayValue = (element: string): number => {
  const rawValue = (targetValues.value as any)[element] || 0;
  return parseFloat(convertToDisplay(rawValue, element, targetUnit.value).toFixed(3));
};

const updateElementValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const displayValue = parseFloat(target.value) || 0;
  const realValue = convertFromDisplay(displayValue, element, targetUnit.value);
  targetStore.setTargetElement(element as any, realValue);
  triggerAutoSave();
};

const handleUnitChange = () => {
  loadConvertedValues();
  triggerAutoSave();
};

const resetTargets = () => {
  targetStore.resetTargets();
  convertedValues.value = null;
  showToast('همه مقادیر بازنشانی شدند', 'success');
  triggerAutoSave();
};

// ===== Auto-save Logic =====
const triggerAutoSave = () => {
  if (saveTimeout) clearTimeout(saveTimeout);
  saveStatus.value = 'saving';
  saveTimeout = setTimeout(async () => {
    await performSave();
  }, 1000);
};

const performSave = async () => {
  if (!reportStore.currentReportId) {
    saveStatus.value = 'idle';
    return;
  }
  isSaving.value = true;
  try {
    const targetValuesForSave: Record<string, number> = {};
    for (const [key, value] of Object.entries(targetValues.value)) {
      if (value !== undefined && value !== null && typeof value === 'number' && value > 0) {
        targetValuesForSave[key] = value;
      }
    }

    const calcPayload = {
      target_values: targetValuesForSave,
      final_values: {},
      reservoir_data: {},
      calc_rows: [],
      interpretation: null
    };

    let existingCalc = null;
    try {
      existingCalc = await apiService.getCalculation(String(reportStore.currentReportId));
    } catch (e) {}

    if (existingCalc) {
      await apiService.updateCalculation(String(existingCalc.id), calcPayload);
    } else {
      await apiService.createCalculation(String(reportStore.currentReportId), calcPayload);
    }

    saveStatus.value = 'success';
    setTimeout(() => { saveStatus.value = 'idle'; }, 2000);
  } catch (error: any) {
    console.error('Auto-save error:', error);
    saveStatus.value = 'idle';
  } finally {
    isSaving.value = false;
  }
};

// ===== Toast =====
const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

// ===== Convert Values =====
const loadConvertedValues = async () => {
  isConverting.value = true;
  try {
    const result: Record<string, Record<string, number>> = {};

    for (const element of elements) {
      const value = getDisplayValue(element);
      if (value === 0) {
        result[element] = { ppm: 0, meq: 0, mmol: 0 };
        continue;
      }

      const ppmResult = await apiService.convertUnit({
        value,
        from_unit: targetUnit.value,
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
    showToast('خطا در تبدیل واحدها', 'error');
  } finally {
    isConverting.value = false;
  }
};

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

const handleRecipeApplied = () => {
  loadConvertedValues();
  triggerAutoSave();
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
/* ===== Animations ===== */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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

/* ===== Scrollbar ===== */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
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

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

/* ===== Utilities ===== */
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* ===== Responsive ===== */
@media (max-width: 480px) {
  .xs\:inline {
    display: inline !important;
  }
  .xs\:hidden {
    display: none !important;
  }
}

@media (min-width: 481px) {
  .xs\:inline {
    display: none !important;
  }
  .xs\:hidden {
    display: inline !important;
  }
}
</style>