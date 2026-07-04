<!-- frontend/src/components/features/FertilizerCalcTab.vue -->
<template>
  <div class="space-y-6">
    <!-- هدر با توضیحات کامل -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <div class="space-y-2">
        <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed font-semibold">
          بهینه‌سازی خودکار ترکیب کودها
        </p>
        <ul class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed space-y-1 mr-4 list-disc">
          <li>کودهای مورد نظر خود را از لیست انتخاب کنید و روی دکمه <strong>بهینه‌سازی خودکار</strong> کلیک کنید.</li>
          <li>نرم‌افزار با استفاده از الگوریتم هوشمند NNLS، بهترین ترکیب کودها را برای دستیابی به عناصر هدف محاسبه می‌کند.</li>
          <li>گزینه <strong>تعادل یونی خودکار</strong> در صورت فعال بودن، به طور خودکار یون‌های پادبار (Na یا Cl) را برای برقراری تعادل یونی به ترکیب نهایی اضافه می‌کند.</li>
          <li>پس از بهینه‌سازی، می‌توانید نتیجه را در <strong>گزارش</strong> ذخیره کرده یا به صورت <strong>فایل CSV</strong> خروجی بگیرید.</li>
        </ul>
      </div>
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

    <!-- انتخاب کود -->
    <FertilizerSelector
      :fertilizers="fertilizers"
      :selected-fertilizers="localSelectedFertilizers"
      @update:selected-fertilizers="handleSelectionChange"
    />

    <!-- ============================================================ -->
    <!-- دکمه‌های اقدام - چیدمان جدید -->
    <!-- ============================================================ -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <!-- ردیف اول: دکمه بهینه‌سازی و تعادل یونی -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- دکمه بهینه‌سازی خودکار -->
        <button
          @click="handleAutoOptimize"
          :disabled="isOptimizing || localSelectedFertilizers.length === 0"
          class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors duration-200"
        >
          <svg v-if="!isOptimizing" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ isOptimizing ? 'در حال بهینه‌سازی...' : 'بهینه‌سازی خودکار' }}
        </button>

        <!-- گزینه تعادل یونی خودکار (بدون برچسب فعال/غیرفعال) -->
        <label class="inline-flex items-center gap-2 px-3 py-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600 cursor-pointer">
          <input
            type="checkbox"
            v-model="autoBalanceEnabled"
            class="w-4 h-4 rounded border-gray-300 dark:border-gray-600 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-0"
          />
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            تعادل یونی خودکار
          </span>
        </label>
      </div>

      <!-- ردیف دوم: دکمه‌های عملیاتی -->
      <div class="flex flex-wrap items-center gap-3 mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <!-- دکمه ذخیره در گزارش -->
        <button
          @click="saveToReport"
          :disabled="!hasOptimizationResult || isSaving"
          class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors duration-200"
        >
          <svg v-if="!isSaving" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ isSaving ? 'در حال ذخیره...' : 'ذخیره در گزارش' }}
        </button>

        <!-- دکمه خروجی CSV -->
        <button
          @click="exportCSV"
          :disabled="!hasOptimizationResult"
          class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors duration-200"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          خروجی CSV
        </button>

        <!-- دکمه بازنشانی -->
        <button
          @click="resetAll"
          class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 rounded-lg transition-colors duration-200"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          بازنشانی
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نمایش نتیجه بهینه‌سازی -->
    <!-- ============================================================ -->
    <OptimizationResult
      :result="calcStore.optimizationResult"
      :fertilizers="fertilizers"
      :target-values="targetStore.targetElements"
      @save="saveToReport"
      @export-csv="exportCSV"
    />

    <!-- ============================================================ -->
    <!-- خطاها -->
    <!-- ============================================================ -->
    <div v-if="calcErrors.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex-1 space-y-1">
          <div v-for="err in calcErrors" :key="err" class="text-danger-700 dark:text-danger-400 text-sm">
            {{ err }}
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام موفقیت/خطا (Toast) -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="toastMessage"
          class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-2"
          :class="toastType === 'success' 
            ? 'bg-emerald-600 text-white' 
            : 'bg-danger-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useReportStore } from '@/store/modules/reportStore';
import { useCalculations } from '@/composables/useCalculations';
import { useCSVExport } from '@/composables/useCSVExport';

import StockSettings from './calc/StockSettings.vue';
import FertilizerSelector from './calc/FertilizerSelector.vue';
import OptimizationResult from './calc/OptimizationResult.vue';

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

// ===== Stores =====
const calcStore = useCalcStore();
const targetStore = useTargetStore();
const waterStore = useWaterStore();
const reportStore = useReportStore();
const { optimizeFertilizers, isOptimizing } = useCalculations();
const { exportOptimizationResult } = useCSVExport();

// ===== State =====
const mainTankVolume = ref(5000);
const stockVolume = ref(25);
const injectionRatio = ref(100);
const localSelectedFertilizers = ref<string[]>([...props.selectedFertilizers]);
const isSaving = ref(false);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');
const autoBalanceEnabled = ref(true);

// ===== Computed =====
const hasOptimizationResult = computed(() => calcStore.optimizationResult !== null);

// ===== Watch =====
watch(() => props.selectedFertilizers, (newVal) => {
  localSelectedFertilizers.value = [...newVal];
}, { deep: true });

// ===== Methods =====

const handleSelectionChange = (selectedIds: string[]) => {
  localSelectedFertilizers.value = selectedIds;
  emit('update:selectedFertilizers', selectedIds);
};

const handleAutoOptimize = async () => {
  if (localSelectedFertilizers.value.length === 0) {
    showToast('لطفاً حداقل یک کود را انتخاب کنید', 'error');
    return;
  }

  const hasTargets = Object.values(targetStore.targetElements).some(v => v > 0);
  if (!hasTargets) {
    showToast('لطفاً ابتدا عناصر هدف را در بخش مربوطه وارد کنید', 'error');
    return;
  }

  const selectedFerts = props.fertilizers.filter(f => 
    localSelectedFertilizers.value.includes(f.id)
  );

  try {
    const options = {
      auto_balance: autoBalanceEnabled.value
    };

    const result = await optimizeFertilizers(
      selectedFerts,
      options,
      mainTankVolume.value,
      stockVolume.value,
      injectionRatio.value
    );

    if (result) {
      showToast('بهینه‌سازی با موفقیت انجام شد!', 'success');
    } else {
      showToast(calcStore.lastOptimizationError || 'خطا در بهینه‌سازی', 'error');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در بهینه‌سازی', 'error');
  }
};

const saveToReport = async () => {
  if (!calcStore.optimizationResult) {
    showToast('هیچ نتیجه بهینه‌سازی برای ذخیره وجود ندارد', 'error');
    return;
  }

  if (!reportStore.reportData.reportName) {
    reportStore.updateReportData({
      reportName: `گزارش ${new Date().toLocaleDateString('fa-IR')}`,
      date: new Date().toLocaleDateString('fa-IR')
    });
  }

  isSaving.value = true;
  try {
    const success = await reportStore.saveCurrentReport();
    if (success) {
      showToast('گزارش با موفقیت ذخیره شد', 'success');
    } else {
      showToast(reportStore.error || 'خطا در ذخیره گزارش', 'error');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در ذخیره گزارش', 'error');
  } finally {
    isSaving.value = false;
  }
};

const exportCSV = () => {
  if (!calcStore.optimizationResult) {
    showToast('هیچ نتیجه بهینه‌سازی برای خروجی وجود ندارد', 'error');
    return;
  }

  try {
    const result = calcStore.optimizationResult;
    const filename = `بهینه‌سازی_کود_${new Date().toLocaleDateString('fa-IR').replace(/\//g, '-')}`;
    exportOptimizationResult(result, props.fertilizers, targetStore.targetElements, filename);
    showToast('خروجی CSV با موفقیت ذخیره شد', 'success');
  } catch (error: any) {
    showToast(error.message || 'خطا در ایجاد خروجی CSV', 'error');
  }
};

const resetAll = () => {
  if (confirm('آیا از بازنشانی اطمینان دارید؟ تمام داده‌ها پاک خواهند شد.')) {
    emit('update:calcRows', []);
    emit('update:calcErrors', []);
    localSelectedFertilizers.value = [];
    emit('update:selectedFertilizers', []);
    mainTankVolume.value = 5000;
    stockVolume.value = 25;
    injectionRatio.value = 100;
    calcStore.clearOptimizationResult();
    showToast('همه داده‌ها پاک شدند', 'success');
  }
};

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}
</style>