// frontend/src/store/modules/targetStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';

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

  function setTargetElement(element: ElementName, value: number) {
    targetElements.value[element] = value;
    debounceCalculateBalance();
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
    calculateIonBalanceFromAPI
  };
});

// ✅ اضافه کردن export default
export default useTargetStore;