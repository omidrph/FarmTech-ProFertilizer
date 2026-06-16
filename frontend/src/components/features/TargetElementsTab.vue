<template>
  <div class="space-y-6">
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
              <td v-for="element in elements" :key="'value-'+element" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="targetValues[element]" 
                  @input="updateTargetValue(element, $event)"
                  step="0.001"
                  class="w-full max-w-[70px] px-1 py-1 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded transition-all duration-200"
                />
              </td>
            </tr>
          </tbody>
        </table>
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
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">جدول توازن عناصر (تبدیل واحدها)</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[70px]">واحد</th>
              <th v-for="element in elements" :key="element" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[60px]">
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">PPM/L</td>
              <td v-for="element in elements" :key="'ppm-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center">
                {{ getConvertedValue(element, 'ppm') }}
              </td>
            </tr>
            <tr>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">MEQ/L</td>
              <td v-for="element in elements" :key="'meq-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center">
                {{ getConvertedValue(element, 'meq') }}
              </td>
            </tr>
            <tr>
              <td class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">MMOLS/L</td>
              <td v-for="element in elements" :key="'mmol-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center">
                {{ getConvertedValue(element, 'mmol') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-wrap gap-3">
      <button @click="calculateTargets" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        اعمال تغییرات
      </button>
      <button @click="resetTargets" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
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
  targetUnit: string;
  targetValues: Record<string, number>;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:targetUnit', value: string): void;
  (e: 'update:targetValues', value: Record<string, number>): void;
}>();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const ionBalance = computed(() => {
  let cation = 0;
  let anion = 0;
  const cations = ['K', 'Ca', 'Mg', 'Na'];
  const anions = ['N-NO3', 'P', 'S', 'N-NH4', 'Cl'];
  
  for (const [key, val] of Object.entries(props.targetValues)) {
    if (cations.includes(key)) cation += val || 0;
    else if (anions.includes(key)) anion += val || 0;
  }
  
  return { cation, anion, isBalanced: Math.abs(cation - anion) < 0.5 };
});

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

const getConvertedValue = (element: string, unit: string) => {
  const val = props.targetValues[element] || 0;
  if (unit === 'ppm') return val.toFixed(2);
  if (unit === 'meq') return (val * 0.02).toFixed(3);
  return (val * 0.01).toFixed(3);
};

const calculateTargets = () => {
  // Just update - reactive will handle it
};

const resetTargets = () => {
  const emptyValues: Record<string, number> = {};
  elements.forEach(el => emptyValues[el] = 0);
  emit('update:targetValues', emptyValues);
};

const printReport = () => {
  window.print();
};
</script>