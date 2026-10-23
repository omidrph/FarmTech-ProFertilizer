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
  /** فقط ثبت و نمایش؛ در محاسبهٔ کود دخالت ندارد */
  info?: boolean;
}

const f = (key: string, label: string, hint: string, factor: number, mw: number, z: number): WaterForm => ({ key, label, hint, factor, mw, z });

export const WATER_MACRO: WaterRow[] = [
  { key: 'N-NO3', name: 'نیترات', symbol: 'N', type: 'anion', defaultForm: 'N',
    forms: [f('NO3', 'NO₃⁻', 'یون نیترات', 14.007 / 62.005, 62.005, 1), f('N', 'N', 'نیتروژن نیتراتی', 1, 14.007, 1)] },
  { key: 'N-NH4', name: 'آمونیوم', symbol: 'N', type: 'cation', defaultForm: 'N',
    forms: [f('NH4', 'NH₄⁺', 'یون آمونیوم', 14.007 / 18.039, 18.039, 1), f('N', 'N', 'نیتروژن آمونیومی', 1, 14.007, 1), f('NH3', 'NH₃', 'آمونیاک', 14.007 / 17.031, 17.031, 1)] },
  { key: 'P', name: 'فسفر', symbol: 'P', type: 'anion', defaultForm: 'P',
    forms: [f('PO4', 'PO₄³⁻', 'یون فسفات', 30.974 / 94.971, 94.971, 3), f('P', 'P', 'فسفر', 1, 30.974, 1),
      f('H2PO4', 'H₂PO₄⁻', 'یون دی‌هیدروژن فسفات', 30.974 / 96.987, 96.987, 1), f('P2O5', 'P₂O₅', 'انیدرید فسفریک', (2 * 30.974) / 141.945, 141.945, 2)] },
  { key: 'K', name: 'پتاسیم', symbol: 'K', type: 'cation', defaultForm: 'K',
    forms: [f('K', 'K⁺', 'پتاسیم', 1, 39.098, 1), f('K2O', 'K₂O', 'اکسید پتاسیم', (2 * 39.098) / 94.196, 94.196, 2)] },
  { key: 'Ca', name: 'کلسیم', symbol: 'Ca', type: 'cation', defaultForm: 'Ca',
    forms: [f('Ca', 'Ca²⁺', 'کلسیم', 1, 40.078, 2), f('CaO', 'CaO', 'اکسید کلسیم', 40.078 / 56.077, 56.077, 2), f('CaCO3', 'CaCO₃', 'سختی کلسیم (CaCO₃)', 40.078 / 100.087, 100.087, 2)] },
  { key: 'Mg', name: 'منیزیم', symbol: 'Mg', type: 'cation', defaultForm: 'Mg',
    forms: [f('Mg', 'Mg²⁺', 'منیزیم', 1, 24.305, 2), f('MgO', 'MgO', 'اکسید منیزیم', 24.305 / 40.304, 40.304, 2), f('CaCO3', 'CaCO₃', 'سختی منیزیم (CaCO₃)', 24.305 / 100.087, 100.087, 2)] },
  { key: 'S', name: 'گوگرد (سولفات)', symbol: 'S', type: 'anion', defaultForm: 'S',
    forms: [f('SO4', 'SO₄²⁻', 'یون سولفات', 32.065 / 96.06, 96.06, 2), f('S', 'S', 'گوگرد سولفاتی', 1, 32.065, 2), f('SO3', 'SO₃', 'تری‌اکسید گوگرد', 32.065 / 80.06, 80.06, 2)] },
  { key: 'Na', name: 'سدیم', symbol: 'Na', type: 'cation', defaultForm: 'Na',
    forms: [f('Na', 'Na⁺', 'سدیم', 1, 22.99, 1), f('Na2O', 'Na₂O', 'اکسید سدیم', (2 * 22.99) / 61.979, 61.979, 2), f('NaCl', 'NaCl', 'نمک (سدیم کلرید)', 22.99 / 58.443, 58.443, 1)] },
  { key: 'Cl', name: 'کلرید', symbol: 'Cl', type: 'anion', defaultForm: 'Cl',
    forms: [f('Cl', 'Cl⁻', 'کلرید', 1, 35.453, 1), f('NaCl', 'NaCl', 'نمک (سدیم کلرید)', 35.453 / 58.443, 58.443, 1)] },
];

export const WATER_MICRO: WaterRow[] = [
  { key: 'Fe', name: 'آهن', symbol: 'Fe', type: 'cation', defaultForm: 'Fe', forms: [f('Fe', 'Fe', 'آهن', 1, 55.845, 2)] },
  { key: 'Mn', name: 'منگنز', symbol: 'Mn', type: 'cation', defaultForm: 'Mn', forms: [f('Mn', 'Mn', 'منگنز', 1, 54.938, 2)] },
  { key: 'Zn', name: 'روی', symbol: 'Zn', type: 'cation', defaultForm: 'Zn', forms: [f('Zn', 'Zn', 'روی', 1, 65.38, 2)] },
  { key: 'B', name: 'بور', symbol: 'B', type: 'anion', defaultForm: 'B',
    forms: [f('B', 'B', 'بور', 1, 10.81, 1), f('H3BO3', 'H₃BO₃', 'اسید بوریک', 10.81 / 61.83, 61.83, 1), f('BO3', 'BO₃³⁻', 'یون بورات', 10.81 / 58.8, 58.8, 3)] },
  { key: 'Cu', name: 'مس', symbol: 'Cu', type: 'cation', defaultForm: 'Cu', forms: [f('Cu', 'Cu', 'مس', 1, 63.546, 2)] },
  { key: 'Mo', name: 'مولیبدن', symbol: 'Mo', type: 'anion', defaultForm: 'Mo',
    forms: [f('Mo', 'Mo', 'مولیبدن', 1, 95.95, 2), f('MoO4', 'MoO₄²⁻', 'یون مولیبدات', 95.95 / 159.95, 159.95, 2)] },
  { key: 'Si', name: 'سیلیسیم', symbol: 'Si', type: 'neutral', defaultForm: 'Si', info: true,
    forms: [f('Si', 'Si', 'سیلیسیم', 1, 28.086, 0), f('SiO2', 'SiO₂', 'سیلیس', 28.086 / 60.084, 60.084, 0), f('H4SiO4', 'H₄SiO₄', 'اسید سیلیسیک', 28.086 / 96.115, 96.115, 0)] },
];

// قلیائیت: مقدار ذخیره‌شده mg/L بر مبنای CaCO3 (وزن هم‌ارز ۵۰٫۰۴)؛ برای تب pH
const EQ_CACO3 = 50.04;
const alkForms = (): WaterForm[] => [
  f('HCO3', 'HCO₃⁻', 'بی‌کربنات', EQ_CACO3 / 61.017, 61.017, 1),
  f('CaCO3', 'CaCO₃', 'قلیائیت کل (CaCO₃)', 1, 100.087, 2),
];

// نیتروژن کل، بی‌کربنات در دو نقطهٔ پایانی و کربنات (مطابق برگهٔ آزمایشگاه)
export const WATER_OTHER: WaterRow[] = [
  { key: 'N-total', name: 'نیتروژن کل', symbol: 'N', type: 'neutral', defaultForm: 'N', info: true, forms: [f('N', 'N', 'نیتروژن کل', 1, 14.007, 1)] },
  { key: 'Alk55', name: 'بی‌کربنات (pH 5.5)', symbol: 'HCO₃', type: 'anion', defaultForm: 'HCO3', forms: alkForms() },
  { key: 'Alk45', name: 'بی‌کربنات (pH 4.5)', symbol: 'HCO₃', type: 'anion', defaultForm: 'HCO3', info: true, forms: alkForms() },
  { key: 'CO3', name: 'کربنات', symbol: 'CO₃', type: 'anion', defaultForm: 'CO3', info: true, forms: [f('CO3', 'CO₃²⁻', 'یون کربنات', 1, 60.009, 2)] },
];

export const WATER_GROUPS: Array<{ title: string; rows: WaterRow[] }> = [
  { title: 'عناصر اصلی', rows: WATER_MACRO },
  { title: 'ریزمغذی‌ها', rows: WATER_MICRO },
  { title: 'نیتروژن کل، بی‌کربنات و کربنات', rows: WATER_OTHER },
];

/** عناصری که در محاسبهٔ کود دخالت دارند */
export const WATER_ELEMENT_KEYS = [...WATER_MACRO, ...WATER_MICRO].filter((r) => !r.info).map((r) => r.key);

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