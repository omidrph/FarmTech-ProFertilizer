// frontend/src/store/modules/calcStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { CalculationRow, CalculationInputs, ElementName, ReservoirData } from '@/types';
import { apiService } from '@/services/apiService';

const ELEMENTS: ElementName[] = [
  'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl',
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'
] as ElementName[];

export const useCalcStore = defineStore('calc', () => {
  // ===== State =====
  const calculationRows = ref<CalculationRow[]>([]);
  const calculationInputs = ref<CalculationInputs>({
    tankVolume: 1000,
    dilutionFactor: 1,
    totalLiter: 1000
  });
  const errorMessages = ref<string[]>([]);
  const isLoading = ref(false);
  const currentReportId = ref<string | null>(null);
  const reservoirData = ref<ReservoirData>({ A: [], B: [], C: [] });
  const totalCost = ref(0);

  // ===== Getters =====
  const elementTotals = computed(() => {
    const totals: Partial<Record<ElementName, number>> = {};
    for (const element of ELEMENTS) {
      totals[element] = calculationRows.value.reduce((sum: number, row: CalculationRow) => {
        return sum + (row.elements?.[element] || 0);
      }, 0);
    }
    return totals;
  });

  const hasErrors = computed(() => errorMessages.value.length > 0);

  const fixedRows = computed(() => {
    return calculationRows.value.filter((row: CalculationRow) => row.isFixedRow);
  });

  const dynamicRows = computed(() => {
    return calculationRows.value.filter((row: CalculationRow) => !row.isFixedRow);
  });

  // ===== Actions =====

  /**
   * 🆕 تابع مقداردهی اولیه ردیف‌های ثابت - دیگر استفاده نمی‌شود
   * این تابع برای backward compatibility نگه داشته شده اما کاربردی ندارد
   * @deprecated دیگر از این تابع استفاده نمی‌شود
   */
  function initializeFixedRows() {
    // ⚠️ این تابع دیگر ردیف‌های ثابت را ایجاد نمی‌کند
    // کاربر باید خودش کودهای مورد نظر را انتخاب کند
    calculationRows.value = [];
  }

  /**
   * 🆕 افزودن ردیف جدید به جدول محاسبه
   * این تابع توسط کامپوننت FertilizerCalcTab فراخوانی می‌شود
   */
  function addCalculationRow(fertilizerName: string, elements: Partial<Record<ElementName, number>>, fertilizerId?: string) {
    const newRow: CalculationRow = {
      id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
      materialName: fertilizerName,
      weight: 0,
      purity: 100,
      cost: 0,
      elements: elements || {},
      isAcid: false,
      isFixedRow: false,
      fertilizerId: fertilizerId
    };
    calculationRows.value.push(newRow);
    return newRow;
  }

  /**
   * به‌روزرسانی یک ردیف موجود
   */
  function updateCalculationRow(id: string, data: Partial<Omit<CalculationRow, 'id' | 'isFixedRow'>>) {
    const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
    if (index !== -1) {
      const row = calculationRows.value[index];
      if (data.weight !== undefined) row.weight = data.weight;
      if (data.purity !== undefined) row.purity = data.purity;
      if (data.materialName !== undefined) row.materialName = data.materialName;
      if (data.cost !== undefined) row.cost = data.cost;
      if (data.elements !== undefined) row.elements = data.elements;
      if (data.isAcid !== undefined) row.isAcid = data.isAcid;
      if (data.acidType !== undefined) row.acidType = data.acidType;
      calculationRows.value[index] = row;
      return true;
    }
    return false;
  }

  /**
   * حذف یک ردیف از جدول
   * فقط ردیف‌های غیرثابت (isFixedRow === false) قابل حذف هستند
   */
  function removeCalculationRow(id: string) {
    const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
    if (index !== -1 && !calculationRows.value[index].isFixedRow) {
      calculationRows.value.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * 🆕 حذف همه ردیف‌ها (به جز ردیف‌های ثابت - که الان وجود ندارند)
   */
  function clearAllRows() {
    calculationRows.value = [];
  }

  /**
   * به‌روزرسانی تنظیمات ورودی محاسبه
   */
  function updateCalculationInputs(inputs: Partial<CalculationInputs>) {
    const newTankVolume = inputs.tankVolume !== undefined ? inputs.tankVolume : calculationInputs.value.tankVolume;
    const newDilutionFactor = inputs.dilutionFactor !== undefined ? inputs.dilutionFactor : calculationInputs.value.dilutionFactor;
    calculationInputs.value = {
      tankVolume: newTankVolume,
      dilutionFactor: newDilutionFactor,
      totalLiter: newTankVolume * newDilutionFactor
    };
  }

  /**
   * 🎯 محاسبه مخازن از طریق API بک‌اند
   */
  async function calculateReservoirDataFromAPI(): Promise<ReservoirData | null> {
    isLoading.value = true;
    try {
      const fertilizers = calculationRows.value
        .filter(row => row.weight && row.weight > 0)
        .map(row => ({
          fertilizer: {
            name: row.materialName,
            is_acid: row.isAcid || false
          },
          weight: row.weight,
          purity: row.purity
        }));

      const result = await apiService.calculateReservoir({ fertilizers });
      reservoirData.value = result.reservoir_data;
      return result.reservoir_data;
    } catch (error) {
      console.error('Error calculating reservoir data:', error);
      errorMessages.value.push('خطا در محاسبه مخازن');
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 🎯 محاسبه کامل و ذخیره در دیتابیس
   */
  async function calculateAndSave(reportId: string): Promise<any> {
    isLoading.value = true;
    errorMessages.value = [];
    try {
      const reservoir = await calculateReservoirDataFromAPI();
      if (!reservoir) {
        throw new Error('خطا در محاسبه مخازن');
      }

      totalCost.value = calculationRows.value.reduce((sum, row) => sum + (row.cost || 0), 0);

      const calcData = {
        target_values: {},
        final_values: elementTotals.value,
        reservoir_data: reservoir,
        calc_rows: calculationRows.value.map((row: CalculationRow) => ({
          material_name: row.materialName,
          weight: row.weight,
          purity: row.purity,
          cost: row.cost,
          elements: row.elements,
          is_acid: row.isAcid || false,
          acid_type: row.acidType || null,
          is_fixed: row.isFixedRow || false
        }))
      };

      const result = await apiService.createCalculation(reportId, calcData);
      if (result) {
        currentReportId.value = reportId;
        return result;
      }
      errorMessages.value.push('خطا در ذخیره محاسبات');
      return null;
    } catch (err: any) {
      errorMessages.value.push(err.message || 'خطا در انجام محاسبات');
      console.error('Error in calculateAndSave:', err);
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * بارگذاری محاسبات از دیتابیس
   */
  async function loadCalculation(reportId: string): Promise<boolean> {
    isLoading.value = true;
    errorMessages.value = [];
    try {
      const data = await apiService.getCalculation(reportId);
      if (data) {
        if (data.calc_rows && Array.isArray(data.calc_rows)) {
          calculationRows.value = data.calc_rows.map((row: any) => ({
            id: row.id || `row-${Date.now()}-${Math.random()}`,
            materialName: row.material_name || row.materialName,
            weight: row.weight || 0,
            purity: row.purity || 100,
            cost: row.cost || 0,
            elements: row.elements || {},
            isAcid: row.is_acid || row.isAcid || false,
            acidType: row.acid_type || row.acidType || null,
            isFixedRow: row.is_fixed || row.isFixedRow || false
          }));
        }
        if (data.reservoir_data) {
          reservoirData.value = data.reservoir_data;
        }
        currentReportId.value = reportId;
        return true;
      }
      return false;
    } catch (err: any) {
      errorMessages.value.push(err.message || 'خطا در بارگذاری محاسبات');
      console.error('Error loading calculation:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 🆕 بازنشانی کامل - بدون ردیف‌های ثابت
   */
  function resetCalculation() {
    calculationRows.value = [];
    errorMessages.value = [];
    reservoirData.value = { A: [], B: [], C: [] };
    calculationInputs.value = {
      tankVolume: 1000,
      dilutionFactor: 1,
      totalLiter: 1000
    };
    currentReportId.value = null;
    totalCost.value = 0;
    // دیگر initializeFixedRows() اجرا نمی‌شود
  }

  function addError(message: string) {
    if (!errorMessages.value.includes(message)) {
      errorMessages.value.push(message);
    }
  }

  function removeError(message: string) {
    const index = errorMessages.value.indexOf(message);
    if (index !== -1) {
      errorMessages.value.splice(index, 1);
    }
  }

  function clearErrors() {
    errorMessages.value = [];
  }

  // ===== Initialize =====
  // ⚠️ دیگر initializeFixedRows() در ابتدا اجرا نمی‌شود
  // جدول محاسبه خالی شروع می‌شود و کاربر باید کودهای خود را انتخاب کند
  calculationRows.value = [];

  return {
    // State
    calculationRows,
    calculationInputs,
    errorMessages,
    isLoading,
    currentReportId,
    reservoirData,
    totalCost,
    
    // Getters
    elementTotals,
    hasErrors,
    fixedRows,
    dynamicRows,
    
    // Actions
    initializeFixedRows,      // نگه داشته شده برای backward compatibility
    addCalculationRow,
    updateCalculationRow,
    removeCalculationRow,
    clearAllRows,             // 🆕 تابع جدید
    updateCalculationInputs,
    calculateReservoirDataFromAPI,
    calculateAndSave,
    loadCalculation,
    resetCalculation,         // 🆕 تغییر داده شده
    addError,
    removeError,
    clearErrors
  };
});

// ✅ اضافه کردن export default
export default useCalcStore;