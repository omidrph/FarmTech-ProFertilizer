// frontend/src/utils/waterForms.ts
// فرم‌ها و واحدهای ورود آنالیز آب (مثل برگهٔ آزمایشگاه) و تبدیل آن‌ها به مقدار «عنصری» محاسبات
//
// مبنای ذخیره‌سازی (همان چیزی که بک‌اند انتظار دارد):
//   • عناصر: mg/L بر مبنای عنصر (N-NO3 و N-NH4 بر مبنای N خالص، P و S بر مبنای P و S)
//   • Alkalinity: mg/L بر مبنای CaCO3

export type WaterUnit = 'ppm' | 'meq' | 'mmol' | 'umol';

export interface WaterForm {
  key: string;     // کلید فرم (NO3, N, ...)
  label: string;   // نمایش (NO₃⁻)
  hint: string;    // نام فارسی
  factor: number;  // mg «فرم» → مقدار ذخیره‌شده (عنصر یا CaCO3)
  mw: number;      // جرم مولی فرم (g/mol)
  z: number;       // بار/ظرفیت برای meq
}

export interface WaterRow {
  key: string;     // کلید ذخیره (N-NO3, K, Alkalinity, ...)
  name: string;    // نام فارسی
  symbol: string;
  type: 'cation' | 'anion' | 'neutral';
  defaultForm: string;
  forms: WaterForm[];
}

const f = (key: string, label: string, hint: string, factor: number, mw: number, z: number): WaterForm => ({ key, label, hint, factor, mw, z });

export const WATER_MACRO: WaterRow[] = [
  { key: 'N-NO3', name: 'نیترات', symbol: 'N', type: 'anion', defaultForm: 'N',
    forms: [f('NO3', 'NO₃⁻', 'یون نیترات', 14.007 / 62.005, 62.005, 1), f('N', 'N', 'نیتروژن نیتراتی', 1, 14.007, 1)] },
  { key: 'N-NH4', name: 'آمونیوم', symbol: 'N', type: 'cation', defaultForm: 'N',
    forms: [f('NH4', 'NH₄⁺', 'یون آمونیوم', 14.007 / 18.039, 18.039, 1), f('N', 'N', 'نیتروژن آمونیومی', 1, 14.007, 1)] },
  { key: 'P', name: 'فسفر', symbol: 'P', type: 'anion', defaultForm: 'P',
    forms: [f('PO4', 'PO₄³⁻', 'یون فسفات', 30.974 / 94.971, 94.971, 3), f('P', 'P', 'فسفر', 1, 30.974, 1)] },
  { key: 'K', name: 'پتاسیم', symbol: 'K', type: 'cation', defaultForm: 'K',
    forms: [f('K', 'K⁺', 'پتاسیم', 1, 39.098, 1), f('K2O', 'K₂O', 'اکسید پتاسیم', (2 * 39.098) / 94.196, 94.196, 2)] },
  { key: 'Ca', name: 'کلسیم', symbol: 'Ca', type: 'cation', defaultForm: 'Ca',
    forms: [f('Ca', 'Ca²⁺', 'کلسیم', 1, 40.078, 2), f('CaO', 'CaO', 'اکسید کلسیم', 40.078 / 56.077, 56.077, 2), f('CaCO3', 'CaCO₃', 'سختی کلسیم (CaCO₃)', 40.078 / 100.087, 100.087, 2)] },
  { key: 'Mg', name: 'منیزیم', symbol: 'Mg', type: 'cation', defaultForm: 'Mg',
    forms: [f('Mg', 'Mg²⁺', 'منیزیم', 1, 24.305, 2), f('MgO', 'MgO', 'اکسید منیزیم', 24.305 / 40.304, 40.304, 2)] },
  { key: 'S', name: 'گوگرد (سولفات)', symbol: 'S', type: 'anion', defaultForm: 'S',
    forms: [f('SO4', 'SO₄²⁻', 'یون سولفات', 32.065 / 96.06, 96.06, 2), f('S', 'S', 'گوگرد سولفاتی', 1, 32.065, 2)] },
  { key: 'Na', name: 'سدیم', symbol: 'Na', type: 'cation', defaultForm: 'Na',
    forms: [f('Na', 'Na⁺', 'سدیم', 1, 22.99, 1), f('Na2O', 'Na₂O', 'اکسید سدیم', (2 * 22.99) / 61.979, 61.979, 2)] },
  { key: 'Cl', name: 'کلرید', symbol: 'Cl', type: 'anion', defaultForm: 'Cl',
    forms: [f('Cl', 'Cl⁻', 'کلرید', 1, 35.453, 1)] },
];

export const WATER_MICRO: WaterRow[] = [
  { key: 'Fe', name: 'آهن', symbol: 'Fe', type: 'cation', defaultForm: 'Fe', forms: [f('Fe', 'Fe', 'آهن', 1, 55.845, 2)] },
  { key: 'Mn', name: 'منگنز', symbol: 'Mn', type: 'cation', defaultForm: 'Mn', forms: [f('Mn', 'Mn', 'منگنز', 1, 54.938, 2)] },
  { key: 'Zn', name: 'روی', symbol: 'Zn', type: 'cation', defaultForm: 'Zn', forms: [f('Zn', 'Zn', 'روی', 1, 65.38, 2)] },
  { key: 'B', name: 'بور', symbol: 'B', type: 'anion', defaultForm: 'B',
    forms: [f('B', 'B', 'بور', 1, 10.81, 1), f('H3BO3', 'H₃BO₃', 'اسید بوریک', 10.81 / 61.83, 61.83, 1)] },
  { key: 'Cu', name: 'مس', symbol: 'Cu', type: 'cation', defaultForm: 'Cu', forms: [f('Cu', 'Cu', 'مس', 1, 63.546, 2)] },
  { key: 'Mo', name: 'مولیبدن', symbol: 'Mo', type: 'anion', defaultForm: 'Mo', forms: [f('Mo', 'Mo', 'مولیبدن', 1, 95.95, 2)] },
];

// قلیائیت: مقدار ذخیره‌شده mg/L بر مبنای CaCO3 (وزن هم‌ارز ۵۰٫۰۴) — برای تب pH
const EQ_CACO3 = 50.04;
export const WATER_ALK: WaterRow[] = [
  { key: 'Alkalinity', name: 'قلیائیت (بی‌کربنات)', symbol: 'HCO₃', type: 'anion', defaultForm: 'HCO3',
    forms: [
      f('HCO3', 'HCO₃⁻', 'بی‌کربنات', EQ_CACO3 / 61.017, 61.017, 1),
      f('CaCO3', 'CaCO₃', 'قلیائیت کل (CaCO₃)', 1, 100.087, 2),
      f('CO3', 'CO₃²⁻', 'کربنات', (EQ_CACO3 * 2) / 60.009, 60.009, 2),
    ] },
];

export const WATER_GROUPS: Array<{ title: string; rows: WaterRow[] }> = [
  { title: 'عناصر اصلی', rows: WATER_MACRO },
  { title: 'ریزمغذی‌ها', rows: WATER_MICRO },
  { title: 'قلیائیت', rows: WATER_ALK },
];

export const WATER_ELEMENT_KEYS = [...WATER_MACRO, ...WATER_MICRO].map((r) => r.key);

/** مقدار واردشده (در فرم و واحد انتخابی) → مقدار ذخیره‌شده */
export function toStored(form: WaterForm, unit: WaterUnit, value: number): number {
  let mgForm = value;
  if (unit === 'mmol') mgForm = value * form.mw;
  else if (unit === 'umol') mgForm = (value * form.mw) / 1000;
  else if (unit === 'meq') mgForm = (value / form.z) * form.mw;
  return mgForm * form.factor;
}

/** مقدار ذخیره‌شده → نمایش در فرم و واحد انتخابی */
export function fromStored(form: WaterForm, unit: WaterUnit, stored: number): number {
  const mgForm = stored / form.factor;
  if (unit === 'mmol') return mgForm / form.mw;
  if (unit === 'umol') return (mgForm / form.mw) * 1000;
  if (unit === 'meq') return (mgForm / form.mw) * form.z;
  return mgForm;
}

const PERSIAN = '۰۱۲۳۴۵۶۷۸۹';
const ARABIC = '٠١٢٣٤٥٦٧٨٩';
/** ارقام فارسی/عربی و جداکننده‌ها را استاندارد می‌کند */
export const normalizeNumberText = (s: string): string =>
  s.replace(/[۰-۹٠-٩]/g, (d) => String(PERSIAN.indexOf(d) >= 0 ? PERSIAN.indexOf(d) : ARABIC.indexOf(d)))
    .replace(/[٫,]/g, '.').replace(/[٬\s]/g, '');

/** نمایش عدد بدون صفرهای اضافه */
export const fmtPlain = (n: number): string => (Number.isFinite(n) ? String(parseFloat(n.toFixed(4))) : '');