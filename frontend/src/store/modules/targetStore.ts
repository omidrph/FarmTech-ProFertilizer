import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

type Unit = 'ppm' | 'meq' | 'mmol';

interface IonBalance {
  cation: number;
  anion: number;
  isBalanced: boolean;
}

const ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'] as const;
type ElementName = typeof ELEMENTS[number];
const DEFAULT_UNIT: Unit = 'ppm';

// Helper function for ion balance calculation
const calculateIonBalance = (
  elements: Record<ElementName, number>
): IonBalance => {
  let cation = 0;
  let anion = 0;
  
  const cations: ElementName[] = ['K', 'Ca', 'Mg', 'Na'];
  const anions: ElementName[] = ['N-NO3', 'P', 'S', 'N-NH4', 'Cl'];
  
  for (const [element, value] of Object.entries(elements)) {
    const elem = element as ElementName;
    if (cations.includes(elem)) {
      cation += value;
    } else if (anions.includes(elem)) {
      anion += value;
    }
  }
  
  const isBalanced = Math.abs(cation - anion) < 0.5;
  
  return { cation, anion, isBalanced };
};

export const useTargetStore = defineStore('target', () => {
  // ===== State =====
  const targetElements = ref<Partial<Record<ElementName, number>>>({});
  const targetUnit = ref<Unit>(DEFAULT_UNIT);

  // ===== Getters =====
  const ionBalance = computed<IonBalance>(() => {
    const fullElements: Record<ElementName, number> = {} as Record<ElementName, number>;
    for (const element of ELEMENTS) {
      fullElements[element] = targetElements.value[element] || 0;
    }
    return calculateIonBalance(fullElements);
  });

  const isBalanced = computed(() => ionBalance.value.isBalanced);

  const targetRows = computed(() => {
    return ELEMENTS.map(element => ({
      name: element,
      value: targetElements.value[element] || 0
    }));
  });

  const convertedValues = computed(() => {
    return ELEMENTS.map(element => ({
      element,
      ppm: targetElements.value[element] || 0,
      meq: 0,
      mmol: 0
    }));
  });

  // ===== Actions =====
  function setTargetElement(element: ElementName, value: number) {
    targetElements.value[element] = value;
  }

  function setTargetUnit(unit: Unit) {
    targetUnit.value = unit;
  }

  function resetTargets() {
    targetElements.value = {};
  }

  function getTargetElement(element: ElementName): number {
    return targetElements.value[element] || 0;
  }

  return {
    targetElements,
    targetUnit,
    ionBalance,
    isBalanced,
    targetRows,
    convertedValues,
    setTargetElement,
    setTargetUnit,
    resetTargets,
    getTargetElement
  };
});