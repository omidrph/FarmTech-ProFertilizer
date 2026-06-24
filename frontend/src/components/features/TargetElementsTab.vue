<template>
  <div class="space-y-6">
    <!-- هدر با توضیحات -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        مقادیر مورد نظر خود را برای هر عنصر در جدول زیر وارد کنید. نرم‌افزار به صورت خودکار تعادل یونی را بررسی می‌کند.
      </p>
    </div>

    <!-- جدول عناصر هدف -->
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
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          ذخیره عناصر هدف
        </button>
        <button 
          @click="resetTargets" 
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          بازنشانی همه
        </button>
        <button 
          @click="loadSampleTargets" 
          class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors"
        >
          📥 بارگذاری نمونه
        </button>
      </div>
    </div>

    <!-- تعادل کاتیون و آنیون -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4 mb-4">
        <p class="text-gray-700 dark:text-gray-300 text-sm">
          کاتیون و آنیون نشان‌دهنده مجموع بار الکتریکی عناصر بر اساس میلی‌اکی والان می‌باشد که باید برابر شوند.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-6 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">کاتیون:</span>
          <span class="text-lg font-bold text-primary-600 dark:text-primary-400">{{ ionBalance.cation.toFixed(2) }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">آنیون:</span>
          <span class="text-lg font-bold text-primary-600 dark:text-primary-400">{{ ionBalance.anion.toFixed(2) }}</span>
        </div>
        <div :class="ionBalance.isBalanced ? 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400' : 'bg-danger-100 dark:bg-danger-900/30 text-danger-700 dark:text-danger-400'" class="px-3 py-1 rounded-full text-sm font-medium">
          {{ ionBalance.isBalanced ? '✅ تعادل برقرار' : '❌ تعادل برقرار نیست' }}
        </div>
      </div>
    </div>

    <!-- جدول توازن عناصر -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">جدول توازن عناصر</h3>
      <div class="overflow-x-auto">
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
              <td v-for="element in elements" :key="'ppm-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center">
                {{ getConvertedValue(element, 'ppm') }}
              </td>
            </tr>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">MEQ/L</td>
              <td v-for="element in elements" :key="'meq-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center">
                {{ getConvertedValue(element, 'meq') }}
              </td>
            </tr>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">MMOLS/L</td>
              <td v-for="element in elements" :key="'mmol-'+element" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center">
                {{ getConvertedValue(element, 'mmol') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- پیام موفقیت -->
    <div v-if="saveSuccess" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-4 animate-fade-in">
      <p class="text-success-700 dark:text-success-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        عناصر هدف با موفقیت ذخیره شدند!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useReportStore } from '@/store/modules/reportStore';
import { apiService } from '@/services/apiService';

// ===== Stores =====
const targetStore = useTargetStore();
const reportStore = useReportStore();

// ===== State =====
const saveSuccess = ref(false);
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const targetUnit = computed({
  get: () => targetStore.targetUnit,
  set: (val: any) => targetStore.setTargetUnit(val)
});

const targetValues = computed(() => targetStore.targetElements);

const ionBalance = computed(() => targetStore.ionBalance);

// ===== Methods =====
const getElementValue = (element: string): number => {
  return (targetValues.value as any)[element] || 0;
};

const updateElementValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  targetStore.setTargetElement(element as any, value);
};

const updateTargetUnit = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  targetStore.setTargetUnit(target.value as any);
};

const saveTargets = async () => {
  saveSuccess.value = false;
  
  try {
    // اگر گزارش وجود ندارد، یک گزارش جدید ایجاد کن
    if (!reportStore.reportData.reportName) {
      reportStore.updateReportData({
        reportName: `گزارش ${new Date().toLocaleDateString('fa-IR')}`,
        date: new Date().toLocaleDateString('fa-IR')
      });
    }
    
    // ذخیره در دیتابیس از طریق API
    // ابتدا یک گزارش ایجاد کن
    const reportData = {
      report_name: reportStore.reportData.reportName || `گزارش ${new Date().toLocaleDateString('fa-IR')}`,
      plant_name: reportStore.reportData.plantName || 'نامشخص',
      season: reportStore.reportData.season || 'بهار',
      growth_stage: reportStore.reportData.growthStage || 'رشد رویشی',
      report_date: reportStore.reportData.date || new Date().toLocaleDateString('fa-IR')
    };
    
    // اینجا باید گزارش را ایجاد کنید و سپس عناصر هدف را ذخیره کنید
    // فعلاً فقط در store ذخیره می‌شود
    
    saveSuccess.value = true;
    setTimeout(() => {
      saveSuccess.value = false;
    }, 3000);
    
    console.log('عناصر هدف ذخیره شد:', targetValues.value);
  } catch (error) {
    console.error('خطا در ذخیره عناصر هدف:', error);
    alert('خطا در ذخیره عناصر هدف. لطفاً دوباره تلاش کنید.');
  }
};

const resetTargets = () => {
  targetStore.resetTargets();
};

const loadSampleTargets = () => {
  const samples: Record<string, number> = {
    'N-NO3': 150,
    'P': 40,
    'S': 60,
    'N-NH4': 10,
    'K': 200,
    'Ca': 180,
    'Mg': 50,
    'Na': 0,
    'Cl': 0,
    'Fe': 2.5,
    'Mn': 0.5,
    'Zn': 0.3,
    'B': 0.2,
    'Cu': 0.05,
    'Mo': 0.02
  };
  
  for (const [element, value] of Object.entries(samples)) {
    targetStore.setTargetElement(element as any, value);
  }
  
  saveSuccess.value = true;
  setTimeout(() => {
    saveSuccess.value = false;
  }, 3000);
};

const getConvertedValue = (element: string, unit: string): string => {
  const val = getElementValue(element);
  if (!val) return '0.00';
  
  if (unit === 'ppm') return val.toFixed(2);
  if (unit === 'meq') return (val * 0.02).toFixed(3);
  return (val * 0.01).toFixed(3);
};
</script>

<style scoped>
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
</style>