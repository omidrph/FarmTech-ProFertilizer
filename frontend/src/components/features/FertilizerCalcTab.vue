<template>
  <div class="space-y-6">
    <!-- هدر با توضیحات -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        کود مورد نظر خود را جهت افزودن و محاسبه انتخاب کرده و دکمه افزودن را بزنید.
      </p>
    </div>

    <!-- کنترل‌ها -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 space-y-4">
      <div class="flex flex-wrap gap-4 items-end">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">انتخاب کود</label>
          <select 
            :value="selectedFertilizers" 
            @change="updateSelectedFertilizers($event)"
            multiple 
            class="w-full min-h-[80px] px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          >
            <option v-for="f in fertilizers" :key="f.id" :value="f.id">
              {{ f.name }} {{ f.isAcid ? '(اسید)' : '' }}
            </option>
          </select>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">برای انتخاب چند کود، کلید Ctrl را نگه دارید</p>
        </div>
        <button 
          @click="addFertilizersToCalc" 
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors h-[42px] flex items-center gap-2"
          :disabled="selectedFertilizers.length === 0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          افزودن به جدول
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">حجم مخزن (لیتر)</label>
          <input 
            type="number" 
            :value="tankVolume" 
            @input="updateTankVolume($event)"
            min="1" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" 
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">ضریب رقیق‌سازی</label>
          <input 
            type="number" 
            :value="dilutionFactor" 
            @input="updateDilutionFactor($event)"
            step="0.1" 
            min="0.1" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" 
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">مجموع (لیتر)</label>
          <input 
            type="text" 
            :value="totalLiter" 
            disabled 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed" 
          />
        </div>
      </div>
    </div>

    <!-- جدول محاسبه -->
    <div v-if="calcRows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">جدول محاسبه کود</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-xs border-collapse">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[100px]">ماده</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">وزن (گرم)</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">خلوص (%)</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[90px]">هزینه (تومان)</th>
              <th v-for="el in elements" :key="el" class="px-1 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[50px]">
                {{ el }}
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[60px]">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in calcRows" :key="row.id" :class="{ 'bg-gray-50 dark:bg-gray-700/50': row.isFixedRow }">
              <td class="px-2 py-1 border border-gray-100 dark:border-gray-700 text-center font-medium">
                {{ row.materialName }}
                <span v-if="row.isFixedRow" class="text-xs text-gray-400 dark:text-gray-500 block">(ثابت)</span>
              </td>
              <td class="px-2 py-1 border border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="row.weight" 
                  @input="updateRowWeight(row.id, $event)"
                  step="0.001" 
                  min="0"
                  class="w-full max-w-[70px] px-1 py-0.5 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200" 
                />
              </td>
              <td class="px-2 py-1 border border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="row.purity" 
                  @input="updateRowPurity(row.id, $event)"
                  step="0.1" 
                  min="0" 
                  max="100" 
                  class="w-full max-w-[70px] px-1 py-0.5 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200" 
                />
              </td>
              <td class="px-2 py-1 border border-gray-100 dark:border-gray-700 text-center font-mono">
                {{ row.cost ? Number(row.cost).toLocaleString() : '0' }}
              </td>
              <td v-for="el in elements" :key="el" class="px-1 py-1 border border-gray-100 dark:border-gray-700 text-center text-xs font-mono">
                {{ row.elements && row.elements[el] ? Number(row.elements[el]).toFixed(3) : '0.000' }}
              </td>
              <td class="px-2 py-1 border border-gray-100 dark:border-gray-700 text-center">
                <button 
                  v-if="!row.isFixedRow" 
                  @click="removeCalcRow(row.id)" 
                  class="text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors text-sm"
                  title="حذف"
                >
                  ✕
                </button>
                <span v-else class="text-gray-300 dark:text-gray-600">-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- خطاها -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm flex items-center gap-2">
        <span>⚠️</span>
        <span>{{ err }}</span>
      </div>
    </div>

    <!-- دکمه‌های اقدام -->
    <div class="flex flex-wrap gap-3">
      <button 
        @click="calculateFertilizer" 
        class="px-4 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors flex items-center gap-2"
        :disabled="calcRows.length === 0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
        </svg>
        محاسبه
      </button>
      <button 
        @click="resetFertilizerCalc" 
        class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        بازنشانی
      </button>
      <button 
        @click="printReport" 
        class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors"
      >
        🖨️ چاپ
      </button>
    </div>

    <!-- خلاصه محاسبات -->
    <div v-if="calcRows.length > 0 && totalCost > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap gap-6 text-sm">
        <div>
          <span class="text-gray-500 dark:text-gray-400">تعداد مواد:</span>
          <span class="font-bold text-gray-900 dark:text-white mr-1">{{ calcRows.length }}</span>
        </div>
        <div>
          <span class="text-gray-500 dark:text-gray-400">مجموع هزینه:</span>
          <span class="font-bold text-primary-600 dark:text-primary-400 mr-1">{{ Number(totalCost).toLocaleString() }} تومان</span>
        </div>
        <div>
          <span class="text-gray-500 dark:text-gray-400">حجم کل:</span>
          <span class="font-bold text-gray-900 dark:text-white mr-1">{{ totalLiter }} لیتر</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';

// ===== Props =====
const props = defineProps<{
  fertilizers: any[];
  selectedFertilizers: string[];
  tankVolume: number;
  dilutionFactor: number;
  calcRows: any[];
  calcErrors: string[];
}>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:tankVolume', value: number): void;
  (e: 'update:dilutionFactor', value: number): void;
  (e: 'update:calcRows', value: any[]): void;
  (e: 'update:calcErrors', value: string[]): void;
}>();

// ===== Store =====
const calcStore = useCalcStore();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const totalLiter = computed(() => props.tankVolume * props.dilutionFactor);

const totalCost = computed(() => {
  return props.calcRows.reduce((sum: number, row: any) => sum + (row.cost || 0), 0);
});

// ===== Methods =====
const updateSelectedFertilizers = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  const values = Array.from(target.selectedOptions).map(opt => opt.value);
  emit('update:selectedFertilizers', values);
};

const updateTankVolume = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:tankVolume', parseFloat(target.value) || 0);
};

const updateDilutionFactor = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:dilutionFactor', parseFloat(target.value) || 0);
};

const updateRowWeight = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, weight: value };
      // محاسبه مجدد سهم عناصر
      if (updatedRow.elements) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (value * (pct as number / 100) * (updatedRow.purity / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      // محاسبه هزینه
      const fertilizer = props.fertilizers.find((f: any) => f.name === updatedRow.materialName);
      if (fertilizer) {
        updatedRow.cost = (value / 1000) * fertilizer.pricePerKg;
      }
      return updatedRow;
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
};

const updateRowPurity = (id: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value) || 0;
  
  const newRows = props.calcRows.map((row: any) => {
    if (row.id === id) {
      const updatedRow = { ...row, purity: value };
      // محاسبه مجدد سهم عناصر
      if (updatedRow.elements && updatedRow.weight) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(updatedRow.elements)) {
          if (pct) {
            newElements[el] = (updatedRow.weight * (pct as number / 100) * (value / 100));
          }
        }
        updatedRow.elements = newElements;
      }
      return updatedRow;
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
};

const addFertilizersToCalc = () => {
  const selected = props.fertilizers.filter((f: any) => props.selectedFertilizers.includes(f.id));
  
  const newRows = selected.map((f: any) => ({
    id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
    materialName: f.name,
    weight: 0,
    purity: f.isAcid ? (f.acidType === 'H3PO4' ? 85 : f.acidType === 'HNO3' ? 65 : 98) : 100,
    cost: 0,
    elements: { ...f.elements },
    isAcid: f.isAcid || false,
    acidType: f.acidType || null,
    isFixedRow: false,
    fertilizerId: f.id
  }));
  
  emit('update:calcRows', [...props.calcRows, ...newRows]);
  emit('update:selectedFertilizers', []);
};

const removeCalcRow = (id: string) => {
  emit('update:calcRows', props.calcRows.filter((r: any) => r.id !== id));
};

const calculateFertilizer = () => {
  const errors: string[] = [];
  const newRows = props.calcRows.map((row: any) => {
    if (!row.isFixedRow) {
      if (!row.weight || row.weight <= 0) {
        errors.push(`وزن کود "${row.materialName}" را وارد کنید`);
      }
      if (!row.purity || row.purity <= 0 || row.purity > 100) {
        errors.push(`خلوص کود "${row.materialName}" باید بین 1 تا 100 باشد`);
      }
      
      // محاسبه هزینه
      if (row.weight && row.weight > 0) {
        const fertilizer = props.fertilizers.find((f: any) => f.name === row.materialName);
        if (fertilizer) {
          row.cost = (row.weight / 1000) * fertilizer.pricePerKg;
        }
      }
      
      // محاسبه سهم عناصر
      if (row.elements && row.weight && row.purity) {
        const newElements: Record<string, number> = {};
        for (const [el, pct] of Object.entries(row.elements)) {
          if (pct) {
            newElements[el] = (row.weight * (pct as number / 100) * (row.purity / 100));
          }
        }
        row.elements = newElements;
      }
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
  emit('update:calcErrors', errors);
  
  if (errors.length === 0) {
    // ذخیره در calcStore
    calcStore.calculationRows = newRows;
    calcStore.calculateReservoirData();
  }
};

const resetFertilizerCalc = () => {
  const fixedRows = [
    { 
      id: 'fixed-h3po4', 
      materialName: 'H3PO4', 
      weight: 0, 
      purity: 85, 
      cost: 0, 
      elements: {}, 
      isAcid: true, 
      acidType: 'H3PO4', 
      isFixedRow: true 
    },
    { 
      id: 'fixed-hno3', 
      materialName: 'HNO3', 
      weight: 0, 
      purity: 65, 
      cost: 0, 
      elements: {}, 
      isAcid: true, 
      acidType: 'HNO3', 
      isFixedRow: true 
    },
    { 
      id: 'fixed-h2so4', 
      materialName: 'H2SO4', 
      weight: 0, 
      purity: 98, 
      cost: 0, 
      elements: {}, 
      isAcid: true, 
      acidType: 'H2SO4', 
      isFixedRow: true 
    }
  ];
  
  emit('update:calcRows', fixedRows);
  emit('update:calcErrors', []);
  emit('update:tankVolume', 1000);
  emit('update:dilutionFactor', 1);
  emit('update:selectedFertilizers', []);
};

const printReport = () => {
  window.print();
};
</script>