<!-- frontend/src/components/features/FertilizerCalcTab.vue -->
<template>
  <div class="space-y-6">
    <!-- هدر -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
        کودهای مورد نظر خود را انتخاب کنید. با کلیک روی هر کود، آن را به جدول استوک اضافه یا از آن حذف کنید.
      </p>
    </div>

    <!-- تنظیمات استوک -->
    <StockSettings
      :main-tank-volume="mainTankVolume"
      :stock-volume="stockVolume"
      :injection-ratio="injectionRatio"
      @update:main-tank-volume="mainTankVolume = $event"
      @update:stock-volume="stockVolume = $event"
      @update:injection-ratio="injectionRatio = $event"
    />

    <!-- انتخاب کود (بدون دکمه افزودن) -->
    <FertilizerSelector
      :fertilizers="fertilizers"
      :selected-fertilizers="localSelectedFertilizers"
      @update:selected-fertilizers="handleSelectionChange"
    />

    <!-- جدول محاسبه -->
    <CalcTable
      :rows="calcRows"
      :elements="elements"
      :fertilizers="fertilizers"
      @update:rows="calcRows = $event"
      @remove-row="removeCalcRow"
      @clear-all="clearAllRows"
    />

    <!-- خطاها -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <div class="flex-1 space-y-1">
          <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm">
            {{ err }}
          </div>
        </div>
      </div>
    </div>

    <!-- دکمه‌های اقدام -->
    <div v-if="calcRows.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap gap-3">
        <button
          @click="calculateFertilizer"
          :disabled="isCalculating || calcRows.length === 0"
          class="px-4 py-2 bg-success-600 text-white rounded-lg hover:bg-success-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="!isCalculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ isCalculating ? 'در حال محاسبه...' : 'محاسبه استوک' }}
        </button>

        <button
          @click="resetAll"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          شروع مجدد
        </button>

        <button
          @click="printReport"
          class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
          </svg>
          چاپ
        </button>
      </div>

      <!-- خلاصه -->
      <div v-if="totalCost > 0" class="grid grid-cols-1 sm:grid-cols-4 gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">تعداد مواد</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ calcRows.length }}</p>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">مجموع هزینه</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ Number(totalCost).toLocaleString('fa-IR') }} <span class="text-xs font-normal">تومان</span></p>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">حجم استوک</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ stockVolume }} <span class="text-xs font-normal">لیتر</span></p>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">نسبت تزریق</p>
          <p class="text-xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">1 : {{ injectionRatio }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';
import { useCalculations } from '@/composables/useCalculations';

import StockSettings from './calc/StockSettings.vue';
import FertilizerSelector from './calc/FertilizerSelector.vue';
import CalcTable from './calc/CalcTable.vue';

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
const { calculateReservoir, isCalculating } = useCalculations();

// ===== State =====
const mainTankVolume = ref(5000);
const stockVolume = ref(25);
const injectionRatio = ref(100);

// ===== Local State برای مدیریت انتخاب کودها =====
const localSelectedFertilizers = ref<string[]>([...props.selectedFertilizers]);

// ===== Watch برای همگام‌سازی با props =====
watch(() => props.selectedFertilizers, (newVal) => {
  localSelectedFertilizers.value = [...newVal];
}, { deep: true });

// ===== Data =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const totalCost = computed(() => {
  return props.calcRows.reduce((sum: number, row: any) => sum + (row.cost || 0), 0);
});

// ===== Methods =====

/**
 * 🆕 مدیریت تغییرات انتخاب کودها - به صورت Real-time
 * وقتی کاربر یک کود را انتخاب یا لغو انتخاب می‌کند، این تابع فراخوانی می‌شود
 */
const handleSelectionChange = (selectedIds: string[]) => {
  // به‌روزرسانی local state
  localSelectedFertilizers.value = selectedIds;
  
  // به‌روزرسانی props والد
  emit('update:selectedFertilizers', selectedIds);
  
  // 🆕 سینک کردن با جدول استوک
  syncTableWithSelection(selectedIds);
};

/**
 * 🆕 همگام‌سازی جدول استوک با انتخاب‌های کاربر
 * - اگر کودی انتخاب شده و در جدول نیست → اضافه کن
 * - اگر کودی لغو انتخاب شده و در جدول است → حذف کن
 */
const syncTableWithSelection = (selectedIds: string[]) => {
  // ۱. پیدا کردن کودهایی که تازه انتخاب شده‌اند (در جدول نیستند)
  const currentRowIds = props.calcRows.map(row => row.fertilizerId).filter(id => id);
  const newSelectedIds = selectedIds.filter(id => !currentRowIds.includes(id));
  
  // ۲. پیدا کردن کودهایی که لغو انتخاب شده‌اند (در جدول هستند ولی در لیست انتخاب نیستند)
  const removedIds = currentRowIds.filter(id => !selectedIds.includes(id));
  
  // ۳. اضافه کردن کودهای جدید به جدول
  if (newSelectedIds.length > 0) {
    const newFertilizers = props.fertilizers.filter((f: any) => 
      newSelectedIds.includes(f.id) && !f.isSystemDefault
    );
    
    const newRows = newFertilizers.map((f: any) => ({
      id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
      materialName: f.name,
      weight: 0,
      purity: f.concentration || 100,
      cost: 0,
      elements: { ...f.elements },
      isAcid: f.isAcid || false,
      acidType: f.acidType || null,
      fertilizerId: f.id
    }));
    
    emit('update:calcRows', [...props.calcRows, ...newRows]);
  }
  
  // ۴. حذف کودهای لغو شده از جدول
  if (removedIds.length > 0) {
    const filteredRows = props.calcRows.filter(row => 
      !removedIds.includes(row.fertilizerId)
    );
    emit('update:calcRows', filteredRows);
  }
};

const removeCalcRow = (id: string) => {
  // پیدا کردن کودی که حذف می‌شود
  const row = props.calcRows.find(r => r.id === id);
  if (row && row.fertilizerId) {
    // حذف از لیست انتخاب‌ها
    const newSelected = localSelectedFertilizers.value.filter(id => id !== row.fertilizerId);
    localSelectedFertilizers.value = newSelected;
    emit('update:selectedFertilizers', newSelected);
  }
  
  emit('update:calcRows', props.calcRows.filter((r: any) => r.id !== id));
};

const clearAllRows = () => {
  if (confirm('آیا از حذف همه ردیف‌ها اطمینان دارید؟')) {
    emit('update:calcRows', []);
    emit('update:calcErrors', []);
    localSelectedFertilizers.value = [];
    emit('update:selectedFertilizers', []);
  }
};

const calculateFertilizer = async () => {
  const errors: string[] = [];
  
  if (mainTankVolume.value <= 0) {
    errors.push('حجم مخزن اصلی باید بزرگتر از صفر باشد');
  }
  if (stockVolume.value <= 0) {
    errors.push('حجم سطل استوک باید بزرگتر از صفر باشد');
  }
  if (injectionRatio.value <= 0) {
    errors.push('نسبت تزریق باید بزرگتر از صفر باشد');
  }
  
  const rowsWithWeight = props.calcRows.filter(row => row.weight > 0);
  
  if (rowsWithWeight.length === 0) {
    errors.push('حداقل یک کود باید وزن داشته باشد');
  }
  
  for (const row of rowsWithWeight) {
    if (!row.purity || row.purity <= 0 || row.purity > 100) {
      errors.push(`خلوص کود "${row.materialName}" باید بین 1 تا 100 باشد`);
    }
  }
  
  emit('update:calcErrors', errors);
  
  if (errors.length === 0) {
    calcStore.calculationRows = props.calcRows;
    
    const fertilizers = rowsWithWeight.map(row => ({
      fertilizer: {
        name: row.materialName,
        is_acid: row.isAcid || false
      },
      weight: row.weight,
      purity: row.purity
    }));
    
    const reservoirResult = await calculateReservoir(fertilizers);
    if (reservoirResult) {
      calcStore.reservoirData = reservoirResult.reservoir_data;
    }
    
    alert('✅ محاسبات با موفقیت انجام شد!');
  }
};

const resetAll = () => {
  if (confirm('آیا از شروع مجدد اطمینان دارید؟ تمام داده‌ها پاک خواهند شد.')) {
    emit('update:calcRows', []);
    emit('update:calcErrors', []);
    localSelectedFertilizers.value = [];
    emit('update:selectedFertilizers', []);
    mainTankVolume.value = 5000;
    stockVolume.value = 25;
    injectionRatio.value = 100;
  }
};

const printReport = () => {
  window.print();
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>