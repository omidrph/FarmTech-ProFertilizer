<!-- frontend/src/components/features/calc/CalcTable.vue -->
<template>
  <div v-if="rows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- هدر جدول -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gray-50 dark:bg-gray-700/50">
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
        </svg>
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">
          جدول محاسبه استوک
          <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mr-2">({{ rows.length }} ردیف)</span>
        </h3>
      </div>
      <button
        @click="clearAll"
        class="text-xs text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors flex items-center gap-1"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        حذف همه
      </button>
    </div>

    <!-- کارت‌های محاسبه (برای موبایل) -->
    <div class="block lg:hidden p-4 space-y-3">
      <div
        v-for="row in rows"
        :key="row.id"
        class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600"
      >
        <!-- نام ماده -->
        <div class="flex items-center justify-between mb-3">
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
            <div>
              <p class="font-medium text-sm text-gray-900 dark:text-white">{{ row.materialName }}</p>
              <p class="text-[10px] text-gray-400 dark:text-gray-500">
                {{ row.isAcid ? 'اسید' : 'کود' }}
              </p>
            </div>
          </div>
          <button
            @click="removeRow(row.id)"
            class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>

        <!-- فیلدها -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
              وزن در استوک (گرم)
              <span v-if="row.weight > 0" class="text-success-600">✓</span>
            </label>
            <input
              type="number"
              :value="row.weight"
              @input="updateWeight(row.id, $event)"
              step="0.001"
              min="0"
              :class="[
                'w-full px-2 py-1.5 text-center border rounded text-sm transition-all',
                row.weight > 0 
                  ? 'border-success-400 bg-success-50 dark:bg-success-900/20 text-success-700 dark:text-success-400' 
                  : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
              ]"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
              خلوص (%)
              <span v-if="row.purity > 0 && row.purity !== 100" class="text-warning-600">!</span>
            </label>
            <input
              type="number"
              :value="row.purity"
              @input="updatePurity(row.id, $event)"
              step="0.1"
              min="0"
              max="100"
              :class="[
                'w-full px-2 py-1.5 text-center border rounded text-sm transition-all',
                row.purity > 0 && row.purity !== 100
                  ? 'border-warning-400 bg-warning-50 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400'
                  : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
              ]"
            />
          </div>
        </div>

        <!-- هزینه -->
        <div class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600 flex items-center justify-between">
          <span class="text-xs text-gray-600 dark:text-gray-400">هزینه:</span>
          <span class="font-semibold text-sm text-gray-900 dark:text-white tabular-nums">
            {{ row.cost ? Number(row.cost).toLocaleString('fa-IR') : '0' }} تومان
          </span>
        </div>

        <!-- عناصر -->
        <div v-if="row.elements && Object.keys(row.elements).length > 0" class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
          <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">عناصر تامین شده در استوک:</p>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="(value, el) in row.elements"
              :key="el"
              class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
            >
              {{ el }}: {{ Number(value).toFixed(3) }}g
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- جدول دسکتاپ -->
    <div class="hidden lg:block overflow-x-auto">
      <table class="w-full text-sm border-collapse">
        <thead>
          <tr class="bg-gray-50 dark:bg-gray-700/50">
            <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-3 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[150px]">
              ماده
            </th>
            <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
              <div class="flex items-center justify-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                </svg>
                وزن در استوک (گرم)
              </div>
            </th>
            <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[90px]">
              خلوص (%)
            </th>
            <th class="px-3 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
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
              class="px-2 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[70px]"
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
            v-for="row in rows"
            :key="row.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors"
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
                  <p class="text-[10px] text-gray-400 dark:text-gray-500">
                    {{ row.isAcid ? 'اسید' : 'کود' }}
                  </p>
                </div>
              </div>
            </td>

            <!-- وزن -->
            <td class="px-3 py-2 text-center">
              <input
                type="number"
                :value="row.weight"
                @input="updateWeight(row.id, $event)"
                step="0.001"
                min="0"
                :class="[
                  'w-full max-w-[100px] px-2 py-1.5 text-center border-2 rounded transition-all duration-200 tabular-nums',
                  row.weight > 0
                    ? 'border-success-400 bg-success-50 dark:bg-success-900/20 text-success-700 dark:text-success-400 font-semibold'
                    : 'border-transparent bg-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500'
                ]"
              />
            </td>

            <!-- خلوص -->
            <td class="px-3 py-2 text-center">
              <input
                type="number"
                :value="row.purity"
                @input="updatePurity(row.id, $event)"
                step="0.1"
                min="0"
                max="100"
                :class="[
                  'w-full max-w-[80px] px-2 py-1.5 text-center border-2 rounded transition-all duration-200 tabular-nums',
                  row.purity > 0 && row.purity !== 100
                    ? 'border-warning-400 bg-warning-50 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400 font-semibold'
                    : 'border-transparent bg-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500'
                ]"
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
              class="px-2 py-2 text-center text-xs font-mono tabular-nums"
              :class="[
                row.elements && row.elements[el] && row.elements[el] > 0
                  ? 'text-primary-600 dark:text-primary-400 font-semibold bg-primary-50 dark:bg-primary-900/20'
                  : 'text-gray-700 dark:text-gray-300'
              ]"
            >
              {{ row.elements && row.elements[el] ? Number(row.elements[el]).toFixed(3) : '0.000' }}
            </td>

            <!-- عملیات -->
            <td class="px-3 py-2 text-center">
              <button
                @click="removeRow(row.id)"
                class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                title="حذف"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Types =====
interface CalculationRow {
  id: string;
  materialName: string;
  weight: number;
  purity: number;
  cost: number;
  elements: Record<string, number>;
  isAcid: boolean;
  acidType?: string;
  fertilizerId?: string;
}

// ===== Props =====
interface Props {
  rows: CalculationRow[];
  elements: string[];
  fertilizers: any[];
}

const props = defineProps<Props>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:rows', value: CalculationRow[]): void;
  (e: 'remove-row', id: string): void;
  (e: 'clear-all'): void;
}>();

// ===== Methods =====

/**
 * به‌روزرسانی وزن یک ردیف
 */
const updateWeight = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const weight = parseFloat(target.value) || 0;
  
  const newRows = props.rows.map((row: CalculationRow) => {
    if (row.id === id) {
      const updatedRow = { ...row, weight };
      
      // محاسبه عناصر تامین شده
      if (updatedRow.elements) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (weight * (pct / 100) * (updatedRow.purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      
      // محاسبه هزینه
      const fertilizer = props.fertilizers.find((f: any) => f.id === updatedRow.fertilizerId);
      if (fertilizer) {
        updatedRow.cost = (weight / 1000) * fertilizer.pricePerKg;
      }
      
      return updatedRow;
    }
    return row;
  });
  
  emit('update:rows', newRows);
};

/**
 * به‌روزرسانی خلوص یک ردیف
 */
const updatePurity = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const purity = parseFloat(target.value) || 0;
  
  const newRows = props.rows.map((row: CalculationRow) => {
    if (row.id === id) {
      const updatedRow = { ...row, purity };
      
      // محاسبه مجدد عناصر
      if (updatedRow.elements && updatedRow.weight) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (updatedRow.weight * (pct / 100) * (purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      
      return updatedRow;
    }
    return row;
  });
  
  emit('update:rows', newRows);
};

/**
 * حذف یک ردیف
 */
const removeRow = (id: string) => {
  emit('remove-row', id);
};

/**
 * حذف همه ردیف‌ها
 */
const clearAll = () => {
  if (confirm('آیا از حذف همه ردیف‌ها اطمینان دارید؟')) {
    emit('clear-all');
  }
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
</style>