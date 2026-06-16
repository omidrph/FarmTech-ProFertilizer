// frontend/src/store/modules/calcStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { CalculationRow, CalculationInputs, ElementName } from '@/types';
import { ELEMENTS } from '@/utils/constants';
import { generateId } from '@/utils/helpers';

export const useCalcStore = defineStore('calc', () => {
  // ===== State =====
  const calculationRows = ref<CalculationRow[]>([]);
  const calculationInputs = ref<CalculationInputs>({
    tankVolume: 1000,
    dilutionFactor: 1,
    totalLiter: 1000
  });
  const errorMessages = ref<string[]>([]);

  // ===== Getters =====
  const totalCost = computed(() => {
    return calculationRows.value.reduce((sum: number, row: CalculationRow) => sum + (row.cost || 0), 0);
  });

  const elementTotals = computed(() => {
    const totals: Partial<Record<ElementName, number>> = {};
    for (const element of ELEMENTS) {
      totals[element] = calculationRows.value.reduce((sum: number, row: CalculationRow) => {
        return sum + (row.elements[element] || 0);
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
  function initializeFixedRows() {
    const fixedRows: CalculationRow[] = [
      {
        id: generateId(),
        materialName: 'H3PO4',
        weight: 0,
        purity: 0,
        cost: 0,
        elements: {},
        isAcid: true,
        acidType: 'H3PO4',
        isFixedRow: true
      },
      {
        id: generateId(),
        materialName: 'HNO3',
        weight: 0,
        purity: 0,
        cost: 0,
        elements: {},
        isAcid: true,
        acidType: 'HNO3',
        isFixedRow: true
      },
      {
        id: generateId(),
        materialName: 'H2SO4',
        weight: 0,
        purity: 0,
        cost: 0,
        elements: {},
        isAcid: true,
        acidType: 'H2SO4',
        isFixedRow: true
      }
    ];
    calculationRows.value = [...fixedRows];
  }

  function addCalculationRow(_fertilizerName: string, elements: Partial<Record<ElementName, number>>) {
    const newRow: CalculationRow = {
      id: generateId(),
      materialName: _fertilizerName,
      weight: 0,
      purity: 0,
      cost: 0,
      elements: elements || {},
      isAcid: false,
      isFixedRow: false
    };
    calculationRows.value.push(newRow);
  }

  function updateCalculationRow(id: string, data: Partial<Omit<CalculationRow, 'id' | 'isFixedRow'>>) {
    const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
    if (index !== -1) {
      calculationRows.value[index] = {
        ...calculationRows.value[index],
        ...data
      };
      return true;
    }
    return false;
  }

  function removeCalculationRow(id: string) {
    const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
    if (index !== -1 && !calculationRows.value[index].isFixedRow) {
      calculationRows.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function updateCalculationInputs(inputs: Partial<CalculationInputs>) {
    calculationInputs.value = {
      ...calculationInputs.value,
      ...inputs
    };
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

  function resetCalculation() {
    calculationRows.value = [];
    errorMessages.value = [];
    calculationInputs.value = {
      tankVolume: 1000,
      dilutionFactor: 1,
      totalLiter: 1000
    };
    initializeFixedRows();
  }

  function calculateElementContribution(
    _fertilizerName: string,
    elements: Partial<Record<ElementName, number>>,
    weight: number,
    purity: number
  ): Partial<Record<ElementName, number>> {
    const result: Partial<Record<ElementName, number>> = {};
    for (const [element, percentage] of Object.entries(elements)) {
      if (percentage && percentage > 0) {
        result[element as ElementName] = (weight * (percentage / 100) * (purity / 100));
      }
    }
    return result;
  }

  // ===== Initialize =====
  initializeFixedRows();

  return {
    // State
    calculationRows,
    calculationInputs,
    errorMessages,
    
    // Getters
    totalCost,
    elementTotals,
    hasErrors,
    fixedRows,
    dynamicRows,
    
    // Actions
    initializeFixedRows,
    addCalculationRow,
    updateCalculationRow,
    removeCalculationRow,
    updateCalculationInputs,
    addError,
    removeError,
    clearErrors,
    resetCalculation,
    calculateElementContribution
  };
});