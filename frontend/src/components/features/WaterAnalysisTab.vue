<template>
  <div class="space-y-6">
    <!-- هدر با توضیحات -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        مقادیر آب تامینی خود را به صورت درصد وارد کنید و سپس مقادیر عناصر را در جدول وارد نمایید.
      </p>
    </div>

    <!-- ورودی‌های درصد -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            استفاده از آب (درصد) <span class="text-danger-500">*</span>
          </label>
          <div class="relative">
            <input 
              type="number" 
              :value="waterPercentage" 
              @input="updateWaterPercentage($event)"
              min="0" 
              max="100" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 text-sm">%</span>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            استفاده از پساب (درصد) <span class="text-danger-500">*</span>
          </label>
          <div class="relative">
            <input 
              type="number" 
              :value="wastewaterPercentage" 
              @input="updateWastewaterPercentage($event)"
              min="0" 
              max="100" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 text-sm">%</span>
          </div>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">مجموع آب و پساب باید ۱۰۰٪ باشد</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            شوری آب (EC)
          </label>
          <input 
            type="number" 
            :value="waterSalinity" 
            @input="updateWaterSalinity($event)"
            step="0.01" 
            min="0"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          />
        </div>
      </div>
      
      <!-- هشدار مجموع درصد -->
      <div v-if="totalPercentage !== 100" class="mt-3 bg-yellow-50 dark:bg-yellow-900/20 border-r-4 border-yellow-500 rounded-lg p-3">
        <p class="text-yellow-700 dark:text-yellow-400 text-sm flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          مجموع درصد آب و پساب باید برابر ۱۰۰ باشد. (فعلاً {{ totalPercentage }}٪)
        </p>
      </div>
    </div>

    <!-- جدول آنالیز آب -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">مقادیر آنالیز آب و پساب</h3>
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 dark:text-gray-400">واحد:</label>
          <select 
            :value="analysisUnit" 
            @change="updateAnalysisUnit($event)"
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
              <th v-for="el in waterElements" :key="el" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[70px]">
                {{ el }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">
                پساب
              </td>
              <td v-for="el in waterElements" :key="'waste-'+el" class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center">
                <input 
                  type="number" 
                  :value="getWastewaterValue(el)"
                  @input="updateWastewaterValue(el, $event)"
                  step="0.01" 
                  min="0"
                  class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                  placeholder="۰"
                />
              </td>
            </tr>
            <tr>
              <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">
                آب
              </td>
              <td v-for="el in waterElements" :key="'water-'+el" class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center">
                <input 
                  type="number" 
                  :value="getWaterValue(el)"
                  @input="updateWaterValue(el, $event)"
                  step="0.01" 
                  min="0"
                  class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                  placeholder="۰"
                />
              </td>
            </tr>
            <tr class="bg-primary-50 dark:bg-primary-900/10">
              <td class="px-3 py-2 bg-primary-50 dark:bg-primary-900/10 border border-gray-200 dark:border-gray-600 text-center font-semibold text-primary-600 dark:text-primary-400">
                مقادیر تامینی
              </td>
              <td v-for="el in waterElements" :key="'final-'+el" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center font-semibold text-primary-600 dark:text-primary-400">
                {{ getFinalValue(el) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- دکمه‌های اقدام -->
      <div class="flex flex-wrap gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <button 
          @click="saveWaterAnalysis" 
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
          :disabled="totalPercentage !== 100"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          ذخیره آنالیز آب
        </button>
        <button 
          @click="resetWaterAnalysis" 
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          بازنشانی
        </button>
        <button 
          @click="loadSampleWaterAnalysis" 
          class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors"
        >
          📥 بارگذاری نمونه
        </button>
      </div>
    </div>

    <!-- پیام موفقیت -->
    <div v-if="saveSuccess" class="bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-4 animate-fade-in">
      <p class="text-success-700 dark:text-success-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        آنالیز آب با موفقیت ذخیره شد!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useWaterStore } from '@/store/modules/waterStore';

// ===== Store =====
const waterStore = useWaterStore();

// ===== State =====
const saveSuccess = ref(false);
const waterElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'];

// ===== Computed =====
const waterPercentage = computed({
  get: () => waterStore.waterMixData.waterPercentage,
  set: (val: number) => waterStore.setWaterMix({ waterPercentage: val })
});

const wastewaterPercentage = computed({
  get: () => waterStore.waterMixData.wastewaterPercentage,
  set: (val: number) => waterStore.setWaterMix({ wastewaterPercentage: val })
});

const waterSalinity = computed({
  get: () => waterStore.waterMixData.waterSalinity,
  set: (val: number) => waterStore.setWaterMix({ waterSalinity: val })
});

const analysisUnit = ref('ppm');

const totalPercentage = computed(() => {
  return (waterPercentage.value || 0) + (wastewaterPercentage.value || 0);
});

// ===== Methods =====
const getWastewaterValue = (element: string): number => {
  return (waterStore.wastewaterValues as any)[element] || 0;
};

const getWaterValue = (element: string): number => {
  return (waterStore.waterValues as any)[element] || 0;
};

const getFinalValue = (element: string): string => {
  if (element === 'EC' || element === 'pH') return '-';
  const waterPct = (waterPercentage.value || 0) / 100;
  const wastePct = (wastewaterPercentage.value || 0) / 100;
  const waterVal = getWaterValue(element);
  const wasteVal = getWastewaterValue(element);
  const val = (waterVal * waterPct) + (wasteVal * wastePct);
  return val.toFixed(2);
};

const updateWaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  waterPercentage.value = parseFloat(target.value) || 0;
};

const updateWastewaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  wastewaterPercentage.value = parseFloat(target.value) || 0;
};

const updateWaterSalinity = (event: Event) => {
  const target = event.target as HTMLInputElement;
  waterSalinity.value = parseFloat(target.value) || 0;
};

const updateAnalysisUnit = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  analysisUnit.value = target.value;
};

const updateWastewaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  waterStore.setWastewaterValue(element, value);
};

const updateWaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  waterStore.setWaterValue(element, value);
};

const saveWaterAnalysis = () => {
  if (totalPercentage.value !== 100) {
    alert('مجموع درصد آب و پساب باید برابر ۱۰۰ باشد.');
    return;
  }
  
  saveSuccess.value = true;
  setTimeout(() => {
    saveSuccess.value = false;
  }, 3000);
  
  console.log('آنالیز آب ذخیره شد:', {
    waterPercentage: waterPercentage.value,
    wastewaterPercentage: wastewaterPercentage.value,
    waterSalinity: waterSalinity.value,
    wastewaterValues: waterStore.wastewaterValues,
    waterValues: waterStore.waterValues
  });
};

const resetWaterAnalysis = () => {
  waterStore.resetWaterData();
};

const loadSampleWaterAnalysis = () => {
  waterPercentage.value = 80;
  wastewaterPercentage.value = 20;
  waterSalinity.value = 1.2;
  
  const sampleWastewater: Record<string, number> = {
    'N-NO3': 20,
    'P': 5,
    'S': 10,
    'N-NH4': 2,
    'K': 15,
    'Ca': 30,
    'Fe': 0.5,
    'Mn': 0.1,
    'Zn': 0.05,
    'B': 0.02,
    'Cu': 0.01,
    'Mo': 0.005
  };
  
  const sampleWater: Record<string, number> = {
    'N-NO3': 10,
    'P': 2,
    'S': 5,
    'N-NH4': 1,
    'K': 8,
    'Ca': 20,
    'Fe': 0.2,
    'Mn': 0.05,
    'Zn': 0.02,
    'B': 0.01,
    'Cu': 0.005,
    'Mo': 0.002
  };
  
  for (const [key, value] of Object.entries(sampleWastewater)) {
    waterStore.setWastewaterValue(key, value);
  }
  
  for (const [key, value] of Object.entries(sampleWater)) {
    waterStore.setWaterValue(key, value);
  }
  
  saveSuccess.value = true;
  setTimeout(() => {
    saveSuccess.value = false;
  }, 3000);
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