// src/utils/constants.ts

import { ElementName, Unit, type ElementList } from '@/types';

// ============================================================
// ELEMENTS
// ============================================================

export const ELEMENTS: ElementList = [
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

export const ELEMENT_DISPLAY_NAMES: Record<ElementName, string> = {
  [ElementName.N_NO3]: 'N-NO₃',
  [ElementName.P]: 'P',
  [ElementName.S]: 'S',
  [ElementName.N_NH4]: 'N-NH₄',
  [ElementName.K]: 'K',
  [ElementName.Ca]: 'Ca',
  [ElementName.Mg]: 'Mg',
  [ElementName.Na]: 'Na',
  [ElementName.Cl]: 'Cl',
  [ElementName.Fe]: 'Fe',
  [ElementName.Mn]: 'Mn',
  [ElementName.Zn]: 'Zn',
  [ElementName.B]: 'B',
  [ElementName.Cu]: 'Cu',
  [ElementName.Mo]: 'Mo'
};

export const WATER_ELEMENTS = [
  'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'
];

// ============================================================
// UNITS
// ============================================================

export const UNITS = [
  { value: Unit.PPM, label: 'PPM/L' },
  { value: Unit.MEQ, label: 'MEQ/L' },
  { value: Unit.MMOL, label: 'MMOLS/L' }
];

export const DEFAULT_UNIT = Unit.PPM;

// ============================================================
// TABS
// ============================================================

export const TABS = [
  { id: 'home', label: 'خانه', icon: '🏠' },
  { id: 'water-analysis', label: 'آنالیز آب', icon: '💧' },
  { id: 'target-elements', label: 'عناصر هدف', icon: '🎯' },
  { id: 'fertilizer-calc', label: 'محاسبه خودکار مقدار کود', icon: '🧮' },
  { id: 'fertilizer-db', label: 'اطلاعات پایه کودها', icon: '📚' },
  { id: 'interpretation', label: 'تفسیر داده‌ها', icon: '📊' }
];

// ============================================================
// RESERVOIRS
// ============================================================

export const RESERVOIRS = ['A', 'B', 'C'];

// ============================================================
// MESSAGES
// ============================================================

export const ERROR_MESSAGES = {
  REQUIRED: 'این فیلد اجباری است',
  INVALID_NUMBER: 'لطفاً یک عدد معتبر وارد کنید',
  INVALID_PERCENT: 'لطفاً عددی بین 0 تا 100 وارد کنید',
  IMBALANCE: 'تعادل کاتیون و آنیون برقرار نیست',
  NO_FERTILIZER_SELECTED: 'لطفاً حداقل یک کود انتخاب کنید',
  CALCULATION_ERROR: 'خطا در محاسبات، لطفاً مقادیر را بررسی کنید'
};

export const SUCCESS_MESSAGES = {
  SAVED: 'اطلاعات با موفقیت ذخیره شد',
  ADDED: 'با موفقیت اضافه شد',
  DELETED: 'با موفقیت حذف شد',
  UPDATED: 'با موفقیت به‌روزرسانی شد',
  PRINTED: 'گزارش در حال چاپ...'
};