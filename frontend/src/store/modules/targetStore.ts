// frontend/src/store/modules/targetStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';
import { useReportStore } from './reportStore';

type Unit = 'ppm' | 'meq' | 'mmol';

const ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'] as const;
type ElementName = typeof ELEMENTS[number];

const DEFAULT_UNIT: Unit = 'ppm';

export const useTargetStore = defineStore('target', () => {
  // ===== State =====
  const targetElements = ref<Partial<Record<ElementName, number>>>({});
  const targetUnit = ref<Unit>(DEFAULT_UNIT);
  const ionBalance = ref({ cation: 0, anion: 0, isBalanced: false });
  const isCalculatingBalance = ref(false);
  let saveTimeout: ReturnType<typeof setTimeout> | null = null;

  // ===== Getters =====
  const isBalanced = computed(() => ionBalance.value.isBalanced);

  const targetRows = computed(() => {
    return ELEMENTS.map(element => ({
      name: element,
      value: targetElements.value[element] || 0
    }));
  });

  // ===== Actions =====

  /**
   * 🆕 ذخیره عناصر هدف در سرور
   */
  async function saveTargetsToServer(reportId?: string): Promise<boolean> {
    const reportStore = useReportStore();
    const targetId = reportId || String(reportStore.currentReportId);
    
    if (!targetId || targetId === 'null') {
      console.warn('⚠️ No report ID available for saving targets');
      return false;
    }

    // فیلتر کردن عناصر با مقدار مثبت
    const targetValues: Record<string, number> = {};
    for (const [key, value] of Object.entries(targetElements.value)) {
      if (value !== undefined && value !== null && typeof value === 'number' && value > 0) {
        targetValues[key] = value;
      }
    }

    // اگر هیچ عنصری وجود نداشته باشد، ذخیره نکن
    if (Object.keys(targetValues).length === 0) {
      console.log('ℹ️ No target values to save');
      return true;
    }

    try {
      console.log('💾 Saving targets to server:', targetValues);
      
      // دریافت محاسبات موجود
      let existingCalc = null;
      try {
        existingCalc = await apiService.getCalculation(targetId);
      } catch (e) {
        console.log('ℹ️ No existing calculation found, creating new one');
      }

      const calcPayload = {
        target_values: targetValues,
        final_values: existingCalc?.final_values || {},
        reservoir_data: existingCalc?.reservoir_data || { A: [], B: [], C: [] },
        calc_rows: existingCalc?.calc_rows || [],
        interpretation: existingCalc?.interpretation || null
      };

      if (existingCalc) {
        await apiService.updateCalculation(String(existingCalc.id), calcPayload);
        console.log('✅ Targets updated successfully');
      } else {
        await apiService.createCalculation(targetId, calcPayload);
        console.log('✅ Targets created successfully');
      }

      return true;
    } catch (error) {
      console.error('❌ Error saving targets to server:', error);
      return false;
    }
  }

  /**
   * 🎯 محاسبه تعادل یونی از طریق API بک‌اند
   */
  async function calculateIonBalanceFromAPI(): Promise<void> {
    isCalculatingBalance.value = true;
    try {
      const fullElements: Record<string, number> = {};
      for (const element of ELEMENTS) {
        fullElements[element] = targetElements.value[element] || 0;
      }

      const result = await apiService.calculateIonBalance({
        elements: fullElements,
        unit: targetUnit.value
      });

      ionBalance.value = {
        cation: result.cation,
        anion: result.anion,
        isBalanced: result.is_balanced
      };
    } catch (error) {
      console.error('Error calculating ion balance:', error);
      ionBalance.value = { cation: 0, anion: 0, isBalanced: false };
    } finally {
      isCalculatingBalance.value = false;
    }
  }

  /**
   * تنظیم مقدار یک عنصر هدف
   */
  function setTargetElement(element: ElementName, value: number) {
    console.log(`🎯 Setting target element: ${element} = ${value}`);
    targetElements.value[element] = value;
    
    // محاسبه تعادل یونی
    debounceCalculateBalance();
    
    // 🆕 ذخیره خودکار در سرور (با تأخیر)
    debounceSaveToServer();
  }

  /**
   * ذخیره با تأخیر (Debounce)
   */
  function debounceSaveToServer() {
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
    saveTimeout = setTimeout(async () => {
      const reportStore = useReportStore();
      if (reportStore.currentReportId) {
        await saveTargetsToServer();
      }
    }, 500);
  }

  function setTargetUnit(unit: Unit) {
    targetUnit.value = unit;
    calculateIonBalanceFromAPI();
  }

  function resetTargets() {
    targetElements.value = {};
    ionBalance.value = { cation: 0, anion: 0, isBalanced: false };
  }

  function getTargetElement(element: ElementName): number {
    return targetElements.value[element] || 0;
  }

  /**
   * بارگذاری عناصر هدف از یک شیء
   */
  function loadTargetsFromObject(data: Record<string, number>) {
    console.log('📥 Loading targets from object:', data);
    if (data && typeof data === 'object') {
      for (const [key, value] of Object.entries(data)) {
        if (ELEMENTS.includes(key as any) && value !== undefined && value !== null && value > 0) {
          targetElements.value[key as ElementName] = value;
        }
      }
      // محاسبه تعادل یونی پس از بارگذاری
      calculateIonBalanceFromAPI();
    } else {
      console.warn('⚠️ Invalid data for loadTargetsFromObject:', data);
    }
  }

  // ===== Debounce =====
  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

  function debounceCalculateBalance() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    debounceTimer = setTimeout(() => {
      calculateIonBalanceFromAPI();
    }, 500);
  }

  return {
    targetElements,
    targetUnit,
    ionBalance,
    isCalculatingBalance,
    isBalanced,
    targetRows,
    setTargetElement,
    setTargetUnit,
    resetTargets,
    getTargetElement,
    calculateIonBalanceFromAPI,
    loadTargetsFromObject,
    saveTargetsToServer // 🆕 تابع جدید برای ذخیره‌سازی
  };
});

export default useTargetStore;