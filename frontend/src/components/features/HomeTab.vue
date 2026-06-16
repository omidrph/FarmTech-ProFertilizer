<template>
  <div class="space-y-6">
    <!-- جدول هدف و محلول نهایی -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">جدول هدف و محلول نهایی</h3>
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
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th v-for="element in elements" :key="element" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[60px]">
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td v-for="element in elements" :key="'label-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center text-xs font-medium text-gray-500 dark:text-gray-400">
                {{ element }}
              </td>
            </tr>
            <tr>
              <td v-for="element in elements" :key="'target-'+element" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="targetValues[element]" 
                  @input="updateTargetValue(element, $event)"
                  step="0.01"
                  class="w-full max-w-[70px] px-1 py-1 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded transition-all duration-200"
                />
              </td>
            </tr>
            <tr class="bg-primary-50 dark:bg-primary-900/10">
              <td v-for="element in elements" :key="'final-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-semibold text-primary-600 dark:text-primary-400">
                {{ finalValues[element] ? finalValues[element].toFixed(2) : '0.00' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- اطلاعات مخازن -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">اطلاعات مخازن</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="reservoir in ['A', 'B', 'C']" :key="reservoir" class="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
          <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-2 text-center">مخزن {{ reservoir }}</h4>
          <table class="w-full text-sm">
            <thead>
              <tr>
                <th class="text-right text-gray-600 dark:text-gray-400 font-medium text-xs">نام ماده</th>
                <th class="text-left text-gray-600 dark:text-gray-400 font-medium text-xs">مقدار (گرم)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in getReservoirItems(reservoir)" :key="idx">
                <td class="text-right text-gray-700 dark:text-gray-300 text-xs py-1">{{ item.name }}</td>
                <td class="text-left text-gray-700 dark:text-gray-300 text-xs py-1 font-mono">{{ item.amount.toFixed(3) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Props =====
interface Props {
  targetUnit: string;
  targetValues: Record<string, number>;
  finalValues: Record<string, number>;
  reservoirData?: any;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:targetUnit', value: string): void;
  (e: 'update:targetValues', value: Record<string, number>): void;
  (e: 'update:finalValues', value: Record<string, number>): void;
}>();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Methods =====
const updateTargetUnit = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:targetUnit', target.value);
};

const updateTargetValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const newValues = { ...props.targetValues };
  newValues[element] = parseFloat(target.value) || 0;
  emit('update:targetValues', newValues);
};

const getReservoirItems = (reservoir: string) => {
  // داده‌های نمونه برای مخازن
  const items: Record<string, Array<{name: string, amount: number}>> = {
    'A': [
      { name: 'Ca(NO3)2+NH4', amount: 25.015 },
      { name: 'KNO3', amount: 15.032 }
    ],
    'B': [
      { name: 'KH2PO4', amount: 8.245 },
      { name: 'MgSO4', amount: 12.500 }
    ],
    'C': [
      { name: 'Fe-EDTA', amount: 2.015 },
      { name: 'Micronutrients', amount: 1.500 }
    ]
  };
  return items[reservoir] || [];
};
</script>