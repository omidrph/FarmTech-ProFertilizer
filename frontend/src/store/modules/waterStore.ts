// frontend/src/store/modules/waterStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { WaterMixData } from '@/types';

const WATER_ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

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

export const PH_STANDARDS = {
  MIN_VALID_PH: 0,
  MAX_VALID_PH: 14,
  RANGES: [
    { min: 0, max: 5.5, level: 'acidic', label: 'اسیدی', color: 'warning', description: 'نیاز به تنظیم pH' },
    { min: 5.5, max: 6.5, level: 'slightly_acidic', label: 'کمی اسیدی', color: 'success', description: 'مناسب برای اکثر گیاهان' },
    { min: 6.5, max: 7.5, level: 'neutral', label: 'خنثی', color: 'success', description: 'ایده‌آل برای جذب عناصر' },
    { min: 7.5, max: 8.5, level: 'slightly_alkaline', label: 'کمی قلیایی', color: 'warning', description: 'نیاز به بررسی' },
    { min: 8.5, max: 14, level: 'alkaline', label: 'قلیایی', color: 'danger', description: 'نامناسب برای اکثر گیاهان' }
  ]
} as const;

export function convertECUnit(value: number, fromUnit: string, toUnit: string): number {
  if (fromUnit === toUnit) return value;

  let dsValue: number;
  if (fromUnit === 'dS/m') {
    dsValue = value;
  } else if (fromUnit === 'mS/cm') {
    dsValue = value;
  } else if (fromUnit === 'μS/cm') {
    dsValue = value / 1000;
  } else {
    return value;
  }

  if (toUnit === 'dS/m') {
    return dsValue;
  } else if (toUnit === 'mS/cm') {
    return dsValue;
  } else if (toUnit === 'μS/cm') {
    return dsValue * 1000;
  }

  return value;
}

export function calculateTDS(ecDS: number): number {
  return ecDS * 640;
}

export const useWaterStore = defineStore('water', () => {
  // ===== State =====
  const waterMixData = ref<WaterMixData>({
    waterPercentage: 100,
    wastewaterPercentage: 0,
    waterSalinity: EC_STANDARDS.DEFAULT_EC
  });

  const ecUnit = ref<'dS/m' | 'mS/cm' | 'μS/cm'>('dS/m');
  const wastewaterValues = ref<Record<string, number>>({});
  const waterValues = ref<Record<string, number>>({});

  // pH آب اختیاری است و در water_values['pH'] نگه داشته می‌شود (پیش‌فرض خالی)
  const waterPH = computed<number | null>({
    get: () => {
      const v = waterValues.value['pH'];
      return typeof v === 'number' && v > 0 ? v : null;
    },
    set: (v) => {
      if (v === null || !Number.isFinite(v)) delete waterValues.value['pH'];
      else waterValues.value['pH'] = v;
    }
  });

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

  // مقادیر آب برای محاسبه: ترکیب آب و پساب + قلیائیت + pH (در صورت وجود)
  const calcWaterValues = computed(() => {
    const out: Record<string, number> = {};
    const waterPct = waterMixData.value.waterPercentage / 100;
    const wastePct = waterMixData.value.wastewaterPercentage / 100;
    for (const key of [...WATER_ELEMENTS, 'Alkalinity']) {
      const v = (waterValues.value[key] || 0) * waterPct + (wastewaterValues.value[key] || 0) * wastePct;
      if (v > 0) out[key] = v;
    }
    const ph = waterValues.value['pH'];
    if (typeof ph === 'number' && ph > 0) out['pH'] = ph;
    return out;
  });

  const analysisRows = computed(() => {
    return WATER_ELEMENTS.map(element => ({
      element,
      wastewater: wastewaterValues.value[element] || 0,
      water: waterValues.value[element] || 0,
      finalValue: finalValues.value[element] || 0
    }));
  });

  const tds = computed(() => {
    const ecDS = convertECUnit(waterMixData.value.waterSalinity, ecUnit.value, 'dS/m');
    return calculateTDS(ecDS);
  });

  const phStatus = computed(() => {
    if (waterPH.value === null) return null;
    
    for (const range of PH_STANDARDS.RANGES) {
      if (waterPH.value >= range.min && waterPH.value < range.max) {
        return {
          level: range.level,
          label: range.label,
          color: range.color,
          description: range.description
        };
      }
    }
    return null;
  });

  // ===== Getters جدید =====
  const hasWaterData = computed(() => {
    return waterMixData.value.waterSalinity > 0 || 
           Object.keys(waterValues.value).some(k => waterValues.value[k] > 0) ||
           Object.keys(wastewaterValues.value).some(k => wastewaterValues.value[k] > 0);
  });

  // ===== Actions =====
  function setWaterMix(data: Partial<WaterMixData>) {
    waterMixData.value = {
      ...waterMixData.value,
      ...data
    };
  }

  function setECUnit(unit: 'dS/m' | 'mS/cm' | 'μS/cm') {
    const currentValue = waterMixData.value.waterSalinity;
    const newValue = convertECUnit(currentValue, ecUnit.value, unit);
    
    ecUnit.value = unit;
    waterMixData.value.waterSalinity = newValue;
  }

  function setWaterPH(ph: number | null) {
    waterPH.value = ph;
  }

  function removeWaterValue(element: string) {
    delete waterValues.value[element];
  }

  function removeWastewaterValue(element: string) {
    delete wastewaterValues.value[element];
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
  }

  function getElementFinalValue(element: string): number {
    return finalValues.value[element] || 0;
  }

  // ============================================================
  // 🆕 متد جدید برای بارگذاری از API
  // ============================================================
  function loadFromAPI(data: any) {
    if (!data) return;
    
    waterMixData.value = {
      waterPercentage: data.water_percentage || 100,
      wastewaterPercentage: data.wastewater_percentage || 0,
      waterSalinity: data.water_salinity || EC_STANDARDS.DEFAULT_EC
    };
    
    if (data.water_values) {
      for (const [key, value] of Object.entries(data.water_values)) {
        if (value && typeof value === 'number' && value > 0) {
          waterValues.value[key] = value;
        }
      }
    }
    
    if (data.wastewater_values) {
      for (const [key, value] of Object.entries(data.wastewater_values)) {
        if (value && typeof value === 'number' && value > 0) {
          wastewaterValues.value[key] = value;
        }
      }
    }
  }

  return {
    waterMixData,
    ecUnit,
    waterPH,
    wastewaterValues,
    waterValues,
    finalValues,
    calcWaterValues,
    analysisRows,
    tds,
    phStatus,
    hasWaterData,
    setWaterMix,
    setECUnit,
    setWaterPH,
    setWastewaterValue,
    setWaterValue,
    removeWaterValue,
    removeWastewaterValue,
    resetWaterData,
    getElementFinalValue,
    loadFromAPI
  };
});

export default useWaterStore;