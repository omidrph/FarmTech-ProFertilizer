<template>
  <div class="space-y-6">
    <!-- Info Box -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        کود مورد نظر خود را جهت افزودن و محاسبه انتخاب کرده و دکمه افزودن را بزنید.
      </p>
    </div>

    <!-- Controls -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 space-y-4">
      <div class="flex flex-wrap gap-4 items-end">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">انتخاب کود</label>
          <select 
            :value="selectedFertilizers" 
            @change="updateSelectedFertilizers($event)"
            multiple 
            class="w-full min-h-[80px] px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500"
          >
            <option v-for="f in fertilizers" :key="f.id" :value="f.id">
              {{ f.name }}
            </option>
          </select>
        </div>
        <button @click="addFertilizersToCalc" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors h-[42px]">
          ➕ افزودن
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
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500" 
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
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500" 
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

    <!-- Table -->
    <div v-if="calcRows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">جدول محاسبه کود</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[80px]">ماده</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[70px]">وزن (گرم)</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[70px]">خلوص (%)</th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[80px]">هزینه (تومان)</th>
              <th v-for="el in elements" :key="el" class="px-1 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[45px]">
                {{ el }}
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[50px]">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in calcRows" :key="row.id" :class="{ 'bg-gray-50 dark:bg-gray-700/50': row.isFixed }">
              <td class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center font-medium">{{ row.materialName }}</td>
              <td class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="row.weight" 
                  @input="updateRowWeight(row.id, $event)"
                  step="0.001" 
                  class="w-full max-w-[60px] px-1 py-0.5 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded" 
                />
              </td>
              <td class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <input 
                  type="number" 
                  :value="row.purity" 
                  @input="updateRowPurity(row.id, $event)"
                  step="0.1" 
                  min="0" 
                  max="100" 
                  class="w-full max-w-[60px] px-1 py-0.5 text-center bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 rounded" 
                />
              </td>
              <td class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">{{ row.cost ? row.cost.toFixed(0) : '0' }}</td>
              <td v-for="el in elements" :key="el" class="px-1 py-1 border-b border-gray-100 dark:border-gray-700 text-center text-xs">
                {{ row.elements && row.elements[el] ? row.elements[el].toFixed(3) : '0.000' }}
              </td>
              <td class="px-2 py-1 border-b border-gray-100 dark:border-gray-700 text-center">
                <button v-if="!row.isFixed" @click="removeCalcRow(row.id)" class="text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors text-sm">
                  ✕
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Errors -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm flex items-center gap-2">
        <span>⚠️</span>
        <span>{{ err }}</span>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-wrap gap-3">
      <button @click="calculateFertilizer" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        🧮 محاسبه
      </button>
      <button @click="resetFertilizerCalc" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
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
  fertilizers: any[];
  selectedFertilizers: string[];
  tankVolume: number;
  dilutionFactor: number;
  calcRows: any[];
  calcErrors: string[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:tankVolume', value: number): void;
  (e: 'update:dilutionFactor', value: number): void;
  (e: 'update:calcRows', value: any[]): void;
  (e: 'update:calcErrors', value: string[]): void;
}>();

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const totalLiter = computed(() => props.tankVolume * props.dilutionFactor);

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

const updateRowWeight = (id: number, event: Event) => {
  const target = event.target as HTMLInputElement;
  const newRows = props.calcRows.map(row => {
    if (row.id === id) {
      return { ...row, weight: parseFloat(target.value) || 0 };
    }
    return row;
  });
  emit('update:calcRows', newRows);
};

const updateRowPurity = (id: number, event: Event) => {
  const target = event.target as HTMLInputElement;
  const newRows = props.calcRows.map(row => {
    if (row.id === id) {
      return { ...row, purity: parseFloat(target.value) || 0 };
    }
    return row;
  });
  emit('update:calcRows', newRows);
};

const addFertilizersToCalc = () => {
  const selected = props.fertilizers.filter(f => props.selectedFertilizers.includes(f.id));
  const newRows = selected.map(f => ({
    id: Date.now() + Math.random(),
    materialName: f.name,
    weight: 0,
    purity: 100,
    cost: 0,
    elements: { ...f.elements },
    isFixed: false
  }));
  emit('update:calcRows', [...props.calcRows, ...newRows]);
  emit('update:selectedFertilizers', []);
};

const removeCalcRow = (id: number) => {
  emit('update:calcRows', props.calcRows.filter(r => r.id !== id));
};

const calculateFertilizer = () => {
  const errors: string[] = [];
  let hasError = false;
  const newRows = props.calcRows.map(row => {
    if (!row.isFixed && (!row.weight || row.weight <= 0)) {
      errors.push(`وزن کود "${row.materialName}" را وارد کنید`);
      hasError = true;
    }
    if (!row.isFixed && (!row.purity || row.purity <= 0 || row.purity > 100)) {
      errors.push(`خلوص کود "${row.materialName}" باید بین 1 تا 100 باشد`);
      hasError = true;
    }
    // Calculate cost
    if (!hasError && row.weight && row.purity) {
      const fertilizer = props.fertilizers.find(f => f.name === row.materialName);
      if (fertilizer) {
        row.cost = (row.weight / 1000) * fertilizer.pricePerKg;
      }
      // Calculate element contributions
      if (row.elements) {
        for (const [el, pct] of Object.entries(row.elements)) {
          if (pct) {
            row.elements[el] = (row.weight * (pct as number / 100) * (row.purity / 100));
          }
        }
      }
    }
    return row;
  });
  
  emit('update:calcRows', newRows);
  emit('update:calcErrors', errors);
};

const resetFertilizerCalc = () => {
  const fixedRows = [
    { id: 'fixed1', materialName: 'H3PO4', weight: 0, purity: 0, cost: 0, elements: {}, isFixed: true },
    { id: 'fixed2', materialName: 'HNO3', weight: 0, purity: 0, cost: 0, elements: {}, isFixed: true },
    { id: 'fixed3', materialName: 'H2SO4', weight: 0, purity: 0, cost: 0, elements: {}, isFixed: true }
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