// frontend/src/store/modules/waterStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { WaterMixData } from '@/types';
import { WATER_ELEMENTS } from '@/utils/constants';

export const useWaterStore = defineStore('water', () => {
  // ===== State =====
  const waterMixData = ref<WaterMixData>({
    waterPercentage: 80,
    wastewaterPercentage: 20,
    waterSalinity: 0
  });

  const wastewaterValues = ref<Record<string, number>>({});
  const waterValues = ref<Record<string, number>>({});

  // ===== Getters =====
  const finalValues = computed(() => {
    const result: Record<string, number> = {};
    const waterPct = waterMixData.value.waterPercentage / 100;
    const wastePct = waterMixData.value.wastewaterPercentage / 100;

    for (const element of WATER_ELEMENTS) {
      const waterVal = waterValues.value[element] || 0;
      const wasteVal = wastewaterValues.value[element] || 0;
      result[element] = (waterVal * waterPct) + (wasteVal * wastePct);
    }

    return result;
  });

  const analysisRows = computed(() => {
    return WATER_ELEMENTS.map(element => ({
      element,
      wastewater: wastewaterValues.value[element] || 0,
      water: waterValues.value[element] || 0,
      finalValue: finalValues.value[element] || 0
    }));
  });

  // ===== Actions =====
  function setWaterMix(data: Partial<WaterMixData>) {
    waterMixData.value = {
      ...waterMixData.value,
      ...data
    };
  }

  function setWastewaterValue(element: string, value: number) {
    wastewaterValues.value[element] = value;
  }

  function setWaterValue(element: string, value: number) {
    waterValues.value[element] = value;
  }

  function resetWaterData() {
    wastewaterValues.value = {};
    waterValues.value = {};
    waterMixData.value = {
      waterPercentage: 80,
      wastewaterPercentage: 20,
      waterSalinity: 0
    };
  }

  function getElementFinalValue(element: string): number {
    return finalValues.value[element] || 0;
  }

  return {
    // State
    waterMixData,
    wastewaterValues,
    waterValues,
    
    // Getters
    finalValues,
    analysisRows,
    
    // Actions
    setWaterMix,
    setWastewaterValue,
    setWaterValue,
    resetWaterData,
    getElementFinalValue
  };
});