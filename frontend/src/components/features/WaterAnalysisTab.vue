<template>
  <div class="space-y-6">
    <!-- Info Box -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        مقادیر آب تامینی خود را به صورت درصد وارد کنید (برای مثال 80 درصد آب و 20 درصد پساب)
      </p>
    </div>

    <!-- Inputs -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">استفاده از آب (درصد)</label>
          <input 
            type="number" 
            :value="waterPercentage" 
            @input="updateWaterPercentage($event)"
            min="0" 
            max="100" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500" 
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">استفاده از پساب (درصد)</label>
          <input 
            type="number" 
            :value="wastewaterPercentage" 
            @input="updateWastewaterPercentage($event)"
            min="0" 
            max="100" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500" 
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">مقدار شوری آب</label>
          <input 
            type="number" 
            :value="waterSalinity" 
            @input="updateWaterSalinity($event)"
            step="0.1" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500" 
          />
        </div>
      </div>
    </div>

    <!-- Table -->
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
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[70px]">عنصر</th>
              <th v-for="el in waterElements" :key="el" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[60px]">
                {{ el }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">پساب</td>
              <td v-for="el in waterElements" :key="'waste-'+el" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="wastewaterValues[el]" 
                  @input="updateWastewaterValue(el, $event)"
                  step="0.01" 
                  class="w-full max-w-[60px] px-1 py-1 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded" 
                />
              </td>
            </tr>
            <tr>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">آب</td>
              <td v-for="el in waterElements" :key="'water-'+el" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="waterValues[el]" 
                  @input="updateWaterValue(el, $event)"
                  step="0.01" 
                  class="w-full max-w-[60px] px-1 py-1 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded" 
                />
              </td>
            </tr>
            <tr class="bg-primary-50 dark:bg-primary-900/10">
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-semibold text-primary-600 dark:text-primary-400">مقادیر تامینی</td>
              <td v-for="el in waterElements" :key="'final-'+el" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-semibold text-primary-600 dark:text-primary-400">
                {{ calculateFinalValue(el) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-wrap gap-3">
      <button @click="calculateWaterAnalysis" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        محاسبه
      </button>
      <button @click="resetWaterAnalysis" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
        بازنشانی
      </button>
      <button @click="printReport" class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors">
        🖨️ چاپ
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ===== Props =====
interface Props {
  waterPercentage: number;
  wastewaterPercentage: number;
  waterSalinity: number;
  analysisUnit: string;
  wastewaterValues: Record<string, number>;
  waterValues: Record<string, number>;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:waterPercentage', value: number): void;
  (e: 'update:wastewaterPercentage', value: number): void;
  (e: 'update:waterSalinity', value: number): void;
  (e: 'update:analysisUnit', value: string): void;
  (e: 'update:wastewaterValues', value: Record<string, number>): void;
  (e: 'update:waterValues', value: Record<string, number>): void;
}>();

// ===== Data =====
const waterElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'];

// ===== Methods =====
const updateWaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:waterPercentage', parseFloat(target.value) || 0);
};

const updateWastewaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:wastewaterPercentage', parseFloat(target.value) || 0);
};

const updateWaterSalinity = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:waterSalinity', parseFloat(target.value) || 0);
};

const updateAnalysisUnit = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:analysisUnit', target.value);
};

const updateWastewaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const newValues = { ...props.wastewaterValues };
  newValues[element] = parseFloat(target.value) || 0;
  emit('update:wastewaterValues', newValues);
};

const updateWaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const newValues = { ...props.waterValues };
  newValues[element] = parseFloat(target.value) || 0;
  emit('update:waterValues', newValues);
};

const calculateFinalValue = (element: string) => {
  if (element === 'EC' || element === 'pH') return '-';
  const waterPct = props.waterPercentage / 100;
  const wastePct = props.wastewaterPercentage / 100;
  const val = (props.waterValues[element] || 0) * waterPct + (props.wastewaterValues[element] || 0) * wastePct;
  return val.toFixed(2);
};

const calculateWaterAnalysis = () => {
  // Just recalculate - reactive will handle it
};

const resetWaterAnalysis = () => {
  emit('update:waterPercentage', 80);
  emit('update:wastewaterPercentage', 20);
  emit('update:waterSalinity', 0);
  const emptyValues: Record<string, number> = {};
  waterElements.forEach(el => emptyValues[el] = 0);
  emit('update:wastewaterValues', emptyValues);
  emit('update:waterValues', emptyValues);
};

const printReport = () => {
  window.print();
};
</script>