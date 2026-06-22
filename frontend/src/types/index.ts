// src/types/index.ts

// ============================================================
// ENUMS
// ============================================================

export enum Unit {
  PPM = 'ppm',
  MEQ = 'meq',
  MMOL = 'mmol'
}

export enum ElementName {
  N_NO3 = 'N-NO3',
  P = 'P',
  S = 'S',
  N_NH4 = 'N-NH4',
  K = 'K',
  Ca = 'Ca',
  Mg = 'Mg',
  Na = 'Na',
  Cl = 'Cl',
  Fe = 'Fe',
  Mn = 'Mn',
  Zn = 'Zn',
  B = 'B',
  Cu = 'Cu',
  Mo = 'Mo'
}

export enum ReservoirType {
  A = 'A',
  B = 'B',
  C = 'C'
}

export enum TabType {
  HOME = 'home',
  WATER_ANALYSIS = 'water-analysis',
  TARGET_ELEMENTS = 'target-elements',
  FERTILIZER_CALC = 'fertilizer-calc',
  FERTILIZER_DB = 'fertilizer-db',
  INTERPRETATION = 'interpretation'
}

// ============================================================
// INTERFACES - بخش قبلی
// ============================================================

export interface ElementRow {
  name: ElementName | string;
  targetValue: number;
  finalValue: number;
}

export interface WaterAnalysisRow {
  element: ElementName | string;
  wastewater: number;
  water: number;
  finalValue: number;
}

export interface Fertilizer {
  id: string;
  name: string;
  pricePerKg: number;
  elements: {
    [key in ElementName]?: number;
  };
  createdAt: Date;
  updatedAt: Date;
}

export interface ReservoirItem {
  name: string;
  amount: number;
}

export interface ReservoirData {
  type: ReservoirType;
  items: ReservoirItem[];
}

export interface CalculationRow {
  id: string;
  materialName: string;
  weight: number;
  purity: number;
  cost: number;
  elements: {
    [key in ElementName]?: number;
  };
  isAcid?: boolean;
  acidType?: 'H3PO4' | 'HNO3' | 'H2SO4';
  isFixedRow?: boolean;
}

export interface CalculationInputs {
  tankVolume: number;
  dilutionFactor: number;
  totalLiter: number;
}

export interface IonBalance {
  cation: number;
  anion: number;
  isBalanced: boolean;
}

export interface ReportData {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  date: string;
}

export interface WaterMixData {
  waterPercentage: number;
  wastewaterPercentage: number;
  waterSalinity: number;
}

export interface TargetElementData {
  elements: {
    [key in ElementName]?: number;
  };
  unit: Unit;
}

export interface InterpretationResult {
  ionBalance: {
    cation: number;
    anion: number;
    isBalanced: boolean;
    message: string;
  };
  elementStatus: {
    element: ElementName;
    target: number;
    actual: number;
    difference: number;
    status: 'deficient' | 'sufficient' | 'excessive' | 'toxic';
    message: string;
  }[];
  waterQuality: {
    salinity: number;
    impact: string;
    recommendation: string;
  };
  fertilizerRecommendation: {
    issue: string;
    suggestion: string;
    priority: 'low' | 'medium' | 'high';
  }[];
  summary: string;
}

// ============================================================
// TYPE ALIASES - بخش قبلی
// ============================================================

export type ElementValues = {
  [key in ElementName]?: number;
};

export type ElementList = ElementName[];

export type UnitType = Unit.PPM | Unit.MEQ | Unit.MMOL;

export type ThemeType = 'light' | 'dark';

export type LanguageType = 'fa' | 'en';

// ============================================================
// CONSTANTS AS TYPES - بخش قبلی
// ============================================================

export const ELEMENTS_LIST: ElementName[] = [
  ElementName.N_NO3,
  ElementName.P,
  ElementName.S,
  ElementName.N_NH4,
  ElementName.K,
  ElementName.Ca,
  ElementName.Mg,
  ElementName.Na,
  ElementName.Cl,
  ElementName.Fe,
  ElementName.Mn,
  ElementName.Zn,
  ElementName.B,
  ElementName.Cu,
  ElementName.Mo
];

export const WATER_ELEMENTS_LIST: string[] = [
  'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'
];

export const UNIT_OPTIONS: Unit[] = [Unit.PPM, Unit.MEQ, Unit.MMOL];

export const RESERVOIR_TYPES: ReservoirType[] = [
  ReservoirType.A,
  ReservoirType.B,
  ReservoirType.C
];

// ============================================================
// ✅ بخش جدید: نوع‌های مربوط به احراز هویت (Auth)
// ============================================================

export interface LoginCredentials {
  phone_number: string;
  password: string;
}

export interface RegisterData {
  first_name: string;
  last_name: string;
  phone_number: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: number;
  first_name: string;
  last_name: string;
  phone_number: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  full_name: string;
}