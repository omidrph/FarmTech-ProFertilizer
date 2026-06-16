// frontend/src/utils/helpers.ts
import { ElementName, Unit, type IonBalance } from '@/types';

// ============================================================
// NUMBER FORMATTERS
// ============================================================

export const formatNumber = (value: number, decimals: number = 2): string => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0.00';
  }
  return value.toFixed(decimals);
};

export const parseNumber = (value: string): number => {
  const parsed = parseFloat(value);
  return isNaN(parsed) ? 0 : parsed;
};

export const clamp = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max);
};

// ============================================================
// UNIT CONVERTERS
// ============================================================

export const convertPpmToMeq = (ppm: number, molecularWeight: number, valence: number): number => {
  if (molecularWeight === 0 || valence === 0) return 0;
  return (ppm * valence) / molecularWeight;
};

export const convertMeqToPpm = (meq: number, molecularWeight: number, valence: number): number => {
  if (valence === 0) return 0;
  return (meq * molecularWeight) / valence;
};

export const convertPpmToMmol = (ppm: number, molecularWeight: number): number => {
  if (molecularWeight === 0) return 0;
  return ppm / molecularWeight;
};

export const convertMmolToPpm = (mmol: number, molecularWeight: number): number => {
  return mmol * molecularWeight;
};

// ============================================================
// ELEMENT HELPERS
// ============================================================

export const getElementMolecularWeight = (element: ElementName): number => {
  const weights: Record<ElementName, number> = {
    [ElementName.N_NO3]: 62.0049,
    [ElementName.P]: 30.9738,
    [ElementName.S]: 32.065,
    [ElementName.N_NH4]: 18.0385,
    [ElementName.K]: 39.0983,
    [ElementName.Ca]: 40.078,
    [ElementName.Mg]: 24.305,
    [ElementName.Na]: 22.9898,
    [ElementName.Cl]: 35.453,
    [ElementName.Fe]: 55.845,
    [ElementName.Mn]: 54.938,
    [ElementName.Zn]: 65.38,
    [ElementName.B]: 10.81,
    [ElementName.Cu]: 63.546,
    [ElementName.Mo]: 95.95
  };
  return weights[element] || 0;
};

export const getElementValence = (element: ElementName): number => {
  const valences: Record<ElementName, number> = {
    [ElementName.N_NO3]: 1,
    [ElementName.P]: 1,
    [ElementName.S]: 1,
    [ElementName.N_NH4]: 1,
    [ElementName.K]: 1,
    [ElementName.Ca]: 2,
    [ElementName.Mg]: 2,
    [ElementName.Na]: 1,
    [ElementName.Cl]: 1,
    [ElementName.Fe]: 2,
    [ElementName.Mn]: 2,
    [ElementName.Zn]: 2,
    [ElementName.B]: 1,
    [ElementName.Cu]: 2,
    [ElementName.Mo]: 2
  };
  return valences[element] || 0;
};

// ============================================================
// ION BALANCE
// ============================================================

export const calculateIonBalance = (
  elements: Record<ElementName, number>,
  unit: Unit = Unit.PPM
): IonBalance => {
  let cation = 0;
  let anion = 0;
  
  const cations: ElementName[] = [ElementName.K, ElementName.Ca, ElementName.Mg, ElementName.Na];
  const anions: ElementName[] = [ElementName.N_NO3, ElementName.P, ElementName.S, ElementName.N_NH4, ElementName.Cl];
  
  for (const [element, value] of Object.entries(elements)) {
    const elem = element as ElementName;
    const mw = getElementMolecularWeight(elem);
    const valence = getElementValence(elem);
    
    let meqValue = value;
    if (unit === Unit.PPM) {
      meqValue = convertPpmToMeq(value, mw, valence);
    } else if (unit === Unit.MMOL) {
      meqValue = value * valence;
    }
    
    if (cations.includes(elem)) {
      cation += meqValue;
    } else if (anions.includes(elem)) {
      anion += meqValue;
    }
  }
  
  const isBalanced = Math.abs(cation - anion) < 0.5;
  
  return {
    cation,
    anion,
    isBalanced
  };
};

// ============================================================
// VALIDATION HELPERS
// ============================================================

export const isValidNumber = (value: any): boolean => {
  if (value === undefined || value === null || value === '') return false;
  const num = parseNumber(value);
  return !isNaN(num) && isFinite(num);
};

export const isValidPercent = (value: number): boolean => {
  return value >= 0 && value <= 100;
};

export const isValidPositiveNumber = (value: number): boolean => {
  return value > 0;
};

// ============================================================
// DATE HELPERS
// ============================================================

export const getCurrentShamsiDate = (): string => {
  const now = new Date();
  return now.toLocaleDateString('fa-IR');
};

// ============================================================
// ARRAY HELPERS
// ============================================================

export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 9);
};

export const groupBy = <T>(array: T[], key: keyof T): Record<string, T[]> => {
  return array.reduce((result, item) => {
    const group = String(item[key]);
    if (!result[group]) {
      result[group] = [];
    }
    result[group].push(item);
    return result;
  }, {} as Record<string, T[]>);
};

export const sum = (numbers: number[]): number => {
  return numbers.reduce((acc, val) => acc + val, 0);
};

export const average = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  return sum(numbers) / numbers.length;
};