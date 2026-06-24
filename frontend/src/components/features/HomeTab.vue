<template>
  <div class="space-y-6">
    <!-- جدول هدف و محلول نهایی -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">جدول هدف و محلول نهایی</h3>
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 dark:text-gray-400">واحد:</label>
          <span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-lg text-sm text-gray-700 dark:text-gray-300">
            {{ targetUnit || 'ppm' }}
          </span>
        </div>
      </div>

      <div v-if="!hasData" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <p>هیچ داده‌ای وارد نشده است.</p>
        <p class="text-sm mt-1">لطفاً ابتدا در بخش‌های "عناصر هدف" و "محاسبه خودکار مقدار کود" داده‌ها را وارد کنید.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr>
              <th v-for="element in elements" :key="element" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[60px]">
                {{ element }}
              </th>
            </tr>
          </thead>
          <tbody>
            <!-- ردیف برچسب -->
            <tr>
              <td v-for="element in elements" :key="'label-'+element" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center text-xs font-medium text-gray-400 dark:text-gray-500">
                {{ element }}
              </td>
            </tr>
            <!-- ردیف هدف (از targetStore) -->
            <tr>
              <td v-for="element in elements" :key="'target-'+element" class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <span class="text-gray-700 dark:text-gray-300">{{ getTargetValue(element) }}</span>
              </td>
            </tr>
            <!-- ردیف محلول نهایی (از calcStore) -->
            <tr class="bg-primary-50 dark:bg-primary-900/10">
              <td v-for="element in elements" :key="'final-'+element" class="px-2 py-2 border-b border-gray-100 dark:border-gray-700 text-center font-semibold text-primary-600 dark:text-primary-400">
                {{ getFinalValue(element) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- اطلاعات مخازن (از calcStore) -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">اطلاعات مخازن</h3>
      
      <div v-if="!hasReservoirData" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <p>هنوز محاسبات مخازن انجام نشده است.</p>
        <p class="text-sm mt-1">لطفاً ابتدا در بخش "محاسبه خودکار مقدار کود" محاسبات را انجام دهید.</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="(items, reservoir) in reservoirData" :key="reservoir" class="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
          <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-2 text-center">مخزن {{ reservoir }}</h4>
          
          <div v-if="items && items.length > 0">
            <table class="w-full text-sm">
              <thead>
                <tr>
                  <th class="text-right text-gray-600 dark:text-gray-400 font-medium text-xs">نام ماده</th>
                  <th class="text-left text-gray-600 dark:text-gray-400 font-medium text-xs">مقدار (گرم)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in items" :key="idx">
                  <td class="text-right text-gray-700 dark:text-gray-300 text-xs py-1">{{ item.name }}</td>
                  <td class="text-left text-gray-700 dark:text-gray-300 text-xs py-1 font-mono">{{ item.amount ? item.amount.toFixed(3) : '0.000' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="text-center text-gray-400 dark:text-gray-500 text-sm py-2">خالی</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useCalcStore } from '@/store/modules/calcStore';

// ===== Stores =====
const targetStore = useTargetStore();
const calcStore = useCalcStore();

// ===== Props =====
const props = defineProps<{
  targetUnit?: string;
}>();

// ===== Elements =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const targetValues = computed(() => targetStore.targetElements);
const finalValues = computed(() => calcStore.elementTotals);
const reservoirData = computed(() => calcStore.reservoirData);

const hasData = computed(() => {
  return Object.values(targetValues.value).some(val => val && val > 0);
});

const hasReservoirData = computed(() => {
  const data = reservoirData.value;
  return !!(data.A && data.A.length > 0) || 
         !!(data.B && data.B.length > 0) || 
         !!(data.C && data.C.length > 0);
});

// ===== Methods =====
const getTargetValue = (element: string): string => {
  const val = (targetValues.value as any)[element];
  if (val === undefined || val === null) return '0.00';
  return val.toFixed(2);
};

const getFinalValue = (element: string): string => {
  const val = (finalValues.value as any)[element];
  if (val === undefined || val === null) return '0.00';
  return val.toFixed(2);
};

const formatNumber = (value: number | undefined): string => {
  if (value === undefined || value === null) return '0.00';
  return value.toFixed(2);
};
</script>