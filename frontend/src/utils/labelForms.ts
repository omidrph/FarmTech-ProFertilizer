// frontend/src/utils/labelForms.ts
// تبدیل مقادیر «روی برچسب کود» (اکسید، یون، ...) به «عنصر خالص» برای محاسبات برنامه
// ضریب = (جرم اتمی عنصر × تعداد اتم) ÷ جرم مولی فرم

export interface LabelForm {
  key: string;        // کلید ذخیره (مثلاً K2O)
  label: string;      // نمایش (K₂O)
  hint: string;       // توضیح فارسی کوتاه
  factor: number;     // ضریب تبدیل به عنصر
}

export interface ElementDef {
  key: string;        // کلید عنصر در برنامه (N-NO3, K, ...)
  symbol: string;     // نماد نمایشی
  name: string;       // نام فارسی
  type: 'cation' | 'anion' | 'neutral';
  defaultForm: string;
  forms: LabelForm[];
}

const f = (key: string, label: string, hint: string, factor: number): LabelForm => ({ key, label, hint, factor });

export const ELEMENT_DEFS: ElementDef[] = [
  { key: 'N-NO3', symbol: 'N', name: 'نیتروژن نیتراتی', type: 'anion', defaultForm: 'N',
    forms: [f('N', 'N', 'نیتروژن (روی برچسب: N نیتراتی)', 1), f('NO3', 'NO₃⁻', 'یون نیترات', 14.007 / 62.005)] },
  { key: 'N-NH4', symbol: 'N', name: 'نیتروژن آمونیومی', type: 'cation', defaultForm: 'N',
    forms: [f('N', 'N', 'نیتروژن (روی برچسب: N آمونیومی)', 1), f('NH4', 'NH₄⁺', 'یون آمونیوم', 14.007 / 18.039), f('NH3', 'NH₃', 'آمونیاک', 14.007 / 17.031)] },
  { key: 'P', symbol: 'P', name: 'فسفر', type: 'anion', defaultForm: 'P2O5',
    forms: [f('P2O5', 'P₂O₅', 'پنتااکسید فسفر (رایج روی برچسب)', (2 * 30.974) / 141.945), f('P', 'P', 'فسفر خالص', 1), f('PO4', 'PO₄³⁻', 'یون فسفات', 30.974 / 94.971)] },
  { key: 'K', symbol: 'K', name: 'پتاسیم', type: 'cation', defaultForm: 'K2O',
    forms: [f('K2O', 'K₂O', 'اکسید پتاسیم (رایج روی برچسب)', (2 * 39.098) / 94.196), f('K', 'K', 'پتاسیم خالص', 1)] },
  { key: 'Ca', symbol: 'Ca', name: 'کلسیم', type: 'cation', defaultForm: 'CaO',
    forms: [f('CaO', 'CaO', 'اکسید کلسیم (رایج روی برچسب)', 40.078 / 56.077), f('Ca', 'Ca', 'کلسیم خالص', 1), f('CaCO3', 'CaCO₃', 'کربنات کلسیم', 40.078 / 100.087)] },
  { key: 'Mg', symbol: 'Mg', name: 'منیزیم', type: 'cation', defaultForm: 'MgO',
    forms: [f('MgO', 'MgO', 'اکسید منیزیم (رایج روی برچسب)', 24.305 / 40.304), f('Mg', 'Mg', 'منیزیم خالص', 1)] },
  { key: 'S', symbol: 'S', name: 'گوگرد', type: 'anion', defaultForm: 'SO3',
    forms: [f('SO3', 'SO₃', 'تری‌اکسید گوگرد (رایج روی برچسب)', 32.06 / 80.06), f('S', 'S', 'گوگرد خالص', 1), f('SO4', 'SO₄²⁻', 'یون سولفات', 32.06 / 96.06)] },
  { key: 'Fe', symbol: 'Fe', name: 'آهن', type: 'cation', defaultForm: 'Fe',
    forms: [f('Fe', 'Fe', 'آهن خالص (کلات‌ها)', 1), f('Fe2O3', 'Fe₂O₃', 'اکسید آهن III', (2 * 55.845) / 159.688), f('FeO', 'FeO', 'اکسید آهن II', 55.845 / 71.844)] },
  { key: 'Mn', symbol: 'Mn', name: 'منگنز', type: 'cation', defaultForm: 'Mn',
    forms: [f('Mn', 'Mn', 'منگنز خالص', 1), f('MnO', 'MnO', 'اکسید منگنز II', 54.938 / 70.937), f('MnO2', 'MnO₂', 'اکسید منگنز IV', 54.938 / 86.937)] },
  { key: 'Zn', symbol: 'Zn', name: 'روی', type: 'cation', defaultForm: 'Zn',
    forms: [f('Zn', 'Zn', 'روی خالص', 1), f('ZnO', 'ZnO', 'اکسید روی', 65.38 / 81.38)] },
  { key: 'B', symbol: 'B', name: 'بور', type: 'anion', defaultForm: 'B',
    forms: [f('B', 'B', 'بور خالص', 1), f('B2O3', 'B₂O₃', 'اکسید بور', (2 * 10.811) / 69.62), f('H3BO3', 'H₃BO₃', 'اسید بوریک', 10.811 / 61.83)] },
  { key: 'Cu', symbol: 'Cu', name: 'مس', type: 'cation', defaultForm: 'Cu',
    forms: [f('Cu', 'Cu', 'مس خالص', 1), f('CuO', 'CuO', 'اکسید مس II', 63.546 / 79.545), f('Cu2O', 'Cu₂O', 'اکسید مس I', (2 * 63.546) / 143.091)] },
  { key: 'Mo', symbol: 'Mo', name: 'مولیبدن', type: 'anion', defaultForm: 'Mo',
    forms: [f('Mo', 'Mo', 'مولیبدن خالص', 1), f('MoO3', 'MoO₃', 'اکسید مولیبدن', 95.95 / 143.95)] },
  { key: 'Na', symbol: 'Na', name: 'سدیم', type: 'cation', defaultForm: 'Na2O',
    forms: [f('Na2O', 'Na₂O', 'اکسید سدیم (رایج روی برچسب)', (2 * 22.99) / 61.979), f('Na', 'Na', 'سدیم خالص', 1)] },
  { key: 'Cl', symbol: 'Cl', name: 'کلر', type: 'anion', defaultForm: 'Cl',
    forms: [f('Cl', 'Cl', 'کلر / کلرید', 1)] },
];

export const ELEMENT_KEYS = ELEMENT_DEFS.map((e) => e.key);

/** نام‌های فارسی/انگلیسی برای جستجوی کود بر اساس عنصر */
export const ELEMENT_SEARCH_ALIASES: Record<string, string[]> = {
  'N-NO3': ['n', 'no3', 'نیتروژن', 'ازت', 'نیترات', 'نیتراتی'],
  'N-NH4': ['n', 'nh4', 'نیتروژن', 'ازت', 'آمونیوم', 'آمونیومی'],
  P: ['p', 'p2o5', 'فسفر', 'فسفات', 'فسفره'],
  K: ['k', 'k2o', 'پتاسیم', 'پتاس'],
  Ca: ['ca', 'cao', 'کلسیم'],
  Mg: ['mg', 'mgo', 'منیزیم'],
  S: ['s', 'so3', 'so4', 'گوگرد', 'سولفات'],
  Fe: ['fe', 'آهن'],
  Mn: ['mn', 'mno', 'منگنز'],
  Zn: ['zn', 'zno', 'روی'],
  B: ['b', 'b2o3', 'بور'],
  Cu: ['cu', 'cuo', 'مس'],
  Mo: ['mo', 'moo3', 'مولیبدن'],
  Na: ['na', 'na2o', 'سدیم'],
  Cl: ['cl', 'کلر', 'کلرید'],
};

export const getElementDef = (key: string): ElementDef | undefined => ELEMENT_DEFS.find((e) => e.key === key);

export const getFactor = (elementKey: string, formKey: string): number => {
  const def = getElementDef(elementKey);
  return def?.forms.find((x) => x.key === formKey)?.factor ?? 1;
};

/** مقدار برچسب → درصد عنصر (۴ رقم اعشار) */
export const toElementPct = (elementKey: string, formKey: string, value: number): number =>
  Math.round((Number(value) || 0) * getFactor(elementKey, formKey) * 10000) / 10000;

/** کلید ذخیرهٔ مقدار برچسب: «عنصر|فرم» مثل K|K2O */
export const labelKey = (elementKey: string, formKey: string) => `${elementKey}|${formKey}`;

/** تبدیل زیرنویس‌های عددی فرمول: KNO3 → KNO₃ */
export const prettyFormula = (s: string): string =>
  s.replace(/([A-Za-z)\]])(\d+)/g, (_m, a: string, d: string) => a + d.replace(/\d/g, (x) => '₀₁₂₃₄₅₆₇₈₉'[Number(x)]));

/** آیا عبارت جستجو با عناصر این کود می‌خورد؟ (K، پتاسیم، K2O، ...) */
export const matchesElementQuery = (fert: any, query: string): boolean => {
  const q = (query || '').trim().toLowerCase();
  if (!q) return false;
  const els: Record<string, number> = fert.elements || {};
  for (const [k, v] of Object.entries(els)) {
    if (!(Number(v) > 0)) continue;
    const aliases = ELEMENT_SEARCH_ALIASES[k] || [k.toLowerCase()];
    if (k.toLowerCase() === q || aliases.some((a) => a === q || (q.length >= 3 && a.includes(q)))) return true;
  }
  const lv: Record<string, number> = fert.labelValues || {};
  return Object.keys(lv).some((k) => (k.split('|')[1] || '').toLowerCase() === q);
};
