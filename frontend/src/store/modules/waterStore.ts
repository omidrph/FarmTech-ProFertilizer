// frontend/src/store/modules/waterStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { WaterMixData } from '@/types';

// عناصری که در جدول آنالیز آب نمایش داده می‌شوند
const WATER_ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ============================================================
// 🆕 ثابت‌های استاندارد EC
// ============================================================
export const EC_STANDARDS = {
  MIN_VALID_EC: 0.1,
  DEFAULT_EC: 0.8,
  RANGES: [
    { min: 0, max: 0.75, level: 'excellent', label: 'عالی', color: 'success', description: 'مناسب برای همه گیاهان' },
    { min: 0.75, max: 2.0, level: 'good', label: 'قابل قبول', color: 'warning', description: 'نیاز به بررسی نوع گیاه' },
    { min: 2.0, max: 3.0, level: 'moderate', label: 'نیاز به توجه', color: 'warning', description: 'فقط گیاهان مقاوم به شوری' },
    { min: 3.0, max: Infinity, level: 'critical', label: 'بحرانی', color: 'danger', description: 'نامناسب برای آبیاری' }
  ]
} as const;

// ============================================================
// 🆕 توابع تبدیل واحد EC
// ============================================================
export function convertECUnit(value: number, fromUnit: string, toUnit: string): number {
  if (fromUnit === toUnit) return value;
  
  // تبدیل به dS/m
  let dsValue: number;
  if (fromUnit === 'dS/m') {
    dsValue = value;
  } else if (fromUnit === 'mS/cm') {
    dsValue = value; // 1 mS/cm = 1 dS/m
  } else if (fromUnit === 'μS/cm') {
    dsValue = value / 1000;
  } else {
    return value;
  }
  
  // تبدیل از dS/m به واحد مقصد
  if (toUnit === 'dS/m') {
    return dsValue;
  } else if (toUnit === 'mS/cm') {
    return dsValue;
  } else if (toUnit === 'μS/cm') {
    return dsValue * 1000;
  }
  
  return value;
}

// ============================================================
// 🆕 محاسبه TDS از EC
// ============================================================
export function calculateTDS(ecDS: number): number {
  return ecDS * 640; // TDS (mg/L) ≈ EC (dS/m) × 640
}

export const useWaterStore = defineStore('water', () => {
  // ===== State =====
  const waterMixData = ref<WaterMixData>({
    waterPercentage: 100,
    wastewaterPercentage: 0,
    waterSalinity: EC_STANDARDS.DEFAULT_EC
  });
  
  // 🆕 واحد EC و pH
  const ecUnit = ref<'dS/m' | 'mS/cm' | 'μS/cm'>('dS/m');
  const waterPH = ref<number | null>(null);
  
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

  // 🆕 محاسبه TDS
  const tds = computed(() => {
    const ecDS = convertECUnit(waterMixData.value.waterSalinity, ecUnit.value, 'dS/m');
    return calculateTDS(ecDS);
  });

  // ===== Actions =====
  function setWaterMix(data: Partial<WaterMixData>) {
    waterMixData.value = {
      ...waterMixData.value,
      ...data
    };
  }

  function setECUnit(unit: 'dS/m' | 'mS/cm' | 'μS/cm') {
    // تبدیل مقدار EC به واحد جدید
    const currentValue = waterMixData.value.waterSalinity;
    const newValue = convertECUnit(currentValue, ecUnit.value, unit);
    ecUnit.value = unit;
    waterMixData.value.waterSalinity = newValue;
  }

  function setWaterPH(ph: number | null) {
    waterPH.value = ph;
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
      waterPercentage: 100,
      wastewaterPercentage: 0,
      waterSalinity: EC_STANDARDS.DEFAULT_EC
    };
    ecUnit.value = 'dS/m';
    waterPH.value = null;
  }

  function getElementFinalValue(element: string): number {
    return finalValues.value[element] || 0;
  }

  return {
    waterMixData,
    ecUnit,
    waterPH,
    wastewaterValues,
    waterValues,
    finalValues,
    analysisRows,
    tds,
    setWaterMix,
    setECUnit,
    setWaterPH,
    setWastewaterValue,
    setWaterValue,
    resetWaterData,
    getElementFinalValue
  };
});

export default useWaterStore;