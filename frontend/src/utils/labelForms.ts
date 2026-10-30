
// frontend/src/utils/labelForms.ts
// تبدیل مقادیر «روی برچسب کود» (اکسید، یون، ...) به «عنصر خالص» برای محاسبات برنامه
// ضریب = (جرم اتمی عنصر × تعداد اتم) ÷ جرم مولی فرم
import { factorOf } from './chemFormula';

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
/** فرم رایج با ضریبِ محاسبه‌شده از خودِ فرمول (بدون خطای دستی): fx('N-NO3','Mg(NO3)2·6H2O', ...) */
const fx = (el: string, formula: string, key: string, label: string, hint: string): LabelForm =>
  ({ key, label, hint, factor: factorOf(formula, el) });

export const ELEMENT_DEFS: ElementDef[] = [
  { key: 'N-NO3', symbol: 'N', name: 'نیتروژن نیتراتی', type: 'anion', defaultForm: 'N',
    forms: [
      f('N', 'N', 'نیتروژن', 1),
      f('NO3', 'NO₃⁻', 'یون نیترات', 14.007 / 62.005),
      f('KNO3', 'KNO₃', 'نیترات پتاسیم', 0.1385),
      f('CaNO32', 'Ca(NO₃)₂', 'نیترات کلسیم', 0.1707),
      f('NH4NO3', 'NH₄NO₃', 'نیترات آمونیوم (نیمهٔ نیتراتی)', 0.175),
      fx('N-NO3', 'Ca(NO3)2·4H2O', 'CaNO324H2O', 'Ca(NO₃)₂·4H₂O', 'نیترات کلسیم چهار آبه (رایج گلخانه)'),
      fx('N-NO3', 'Mg(NO3)2·6H2O', 'MgNO32', 'Mg(NO₃)₂·6H₂O', 'نیترات منیزیم'),
      fx('N-NO3', 'NaNO3', 'NaNO3', 'NaNO₃', 'نیترات سدیم'),
      fx('N-NO3', 'HNO3', 'HNO3', 'HNO₃', 'اسید نیتریک'),
      fx('N-NO3', '5Ca(NO3)2·NH4NO3·10H2O', 'CAN155', '5Ca(NO₃)₂·NH₄NO₃·10H₂O', 'نیترات کلسیم آمونیوم (CAN ۱۵٫۵٪)'),
    ] },
  { key: 'N-NH4', symbol: 'N', name: 'نیتروژن آمونیومی', type: 'cation', defaultForm: 'N',
    forms: [
      f('N', 'N', 'نیتروژن', 1),
      f('NH4', 'NH₄⁺', 'یون آمونیوم', 14.007 / 18.039),
      f('NH3', 'NH₃', 'آمونیاک', 14.007 / 17.031),
      f('NH42SO4', '(NH₄)₂SO₄', 'سولفات آمونیوم', 0.212),
      f('NH4NO3', 'NH₄NO₃', 'نیترات آمونیوم (نیمهٔ آمونیومی)', 0.175),
      f('DAP', '(NH₄)₂HPO₄', 'دی‌آمونیوم فسفات', 0.2121),
      fx('N-NH4', 'NH4H2PO4', 'MAP', 'NH₄H₂PO₄', 'مونوآمونیوم فسفات (MAP)'),
      fx('N-NH4', 'NH4Cl', 'NH4Cl', 'NH₄Cl', 'کلرید آمونیوم'),
      fx('N-NH4', 'CO(NH2)2', 'Urea', 'CO(NH₂)₂', 'اوره (نیتروژن آمیدی؛ آمونیومی ثبت می‌شود)'),
      fx('N-NH4', '5Ca(NO3)2·NH4NO3·10H2O', 'CAN155', '5Ca(NO₃)₂·NH₄NO₃·10H₂O', 'نیترات کلسیم آمونیوم (CAN)'),
    ] },
  { key: 'P', symbol: 'P', name: 'فسفر', type: 'anion', defaultForm: 'P2O5',
    forms: [
      f('P2O5', 'P₂O₅', 'انیدرید فسفریک', (2 * 30.974) / 141.945),
      f('P', 'P', 'فسفر', 1),
      f('PO4', 'PO₄³⁻', 'یون فسفات', 30.974 / 94.971),
      f('MKP', 'KH₂PO₄', 'مونوپتاسیم فسفات', 0.2276),
      f('DAP', '(NH₄)₂HPO₄', 'دی‌آمونیوم فسفات', 0.2346),
      f('H3PO4', 'H₃PO₄', 'اسید فسفریک', 0.3161),
      fx('P', 'NH4H2PO4', 'MAP', 'NH₄H₂PO₄', 'مونوآمونیوم فسفات (MAP)'),
      fx('P', 'K2HPO4', 'K2HPO4', 'K₂HPO₄', 'دی‌پتاسیم فسفات'),
      fx('P', 'Ca(H2PO4)2·H2O', 'MCP', 'Ca(H₂PO₄)₂·H₂O', 'مونوکلسیم فسفات'),
    ] },
  { key: 'K', symbol: 'K', name: 'پتاسیم', type: 'cation', defaultForm: 'K2O',
    forms: [
      f('K2O', 'K₂O', 'پتاس (اکسید پتاسیم)', (2 * 39.098) / 94.196),
      f('K', 'K', 'پتاسیم', 1),
      f('KNO3', 'KNO₃', 'نیترات پتاسیم', 0.3867),
      f('MKP', 'KH₂PO₄', 'مونوپتاسیم فسفات', 0.2873),
      f('KCl', 'KCl', 'کلرید پتاسیم', 0.5244),
      f('K2SO4', 'K₂SO₄', 'سولفات پتاسیم', 0.4487),
      fx('K', 'K2HPO4', 'K2HPO4', 'K₂HPO₄', 'دی‌پتاسیم فسفات'),
      fx('K', 'KHCO3', 'KHCO3', 'KHCO₃', 'بی‌کربنات پتاسیم'),
      fx('K', 'K2CO3', 'K2CO3', 'K₂CO₃', 'کربنات پتاسیم'),
      fx('K', 'KOH', 'KOH', 'KOH', 'هیدروکسید پتاسیم'),
    ] },
  { key: 'Ca', symbol: 'Ca', name: 'کلسیم', type: 'cation', defaultForm: 'CaO',
    forms: [
      f('CaO', 'CaO', 'اکسید کلسیم', 40.078 / 56.077),
      f('Ca', 'Ca', 'کلسیم', 1),
      f('CaNO32', 'Ca(NO₃)₂', 'نیترات کلسیم', 0.2442),
      f('CaCl2', 'CaCl₂·6H₂O', 'کلرید کلسیم', 0.1829),
      f('CaSO4', 'CaSO₄·2H₂O', 'سولفات کلسیم (گچ)', 0.2328),
      f('CaCO3', 'CaCO₃', 'کربنات کلسیم', 40.078 / 100.087),
      fx('Ca', 'Ca(NO3)2·4H2O', 'CaNO324H2O', 'Ca(NO₃)₂·4H₂O', 'نیترات کلسیم چهار آبه (رایج گلخانه)'),
      fx('Ca', 'Ca(OH)2', 'CaOH2', 'Ca(OH)₂', 'هیدروکسید کلسیم'),
      fx('Ca', '5Ca(NO3)2·NH4NO3·10H2O', 'CAN155', '5Ca(NO₃)₂·NH₄NO₃·10H₂O', 'نیترات کلسیم آمونیوم (CAN)'),
    ] },
  { key: 'Mg', symbol: 'Mg', name: 'منیزیم', type: 'cation', defaultForm: 'MgO',
    forms: [
      f('MgO', 'MgO', 'اکسید منیزیم', 24.305 / 40.304),
      f('Mg', 'Mg', 'منیزیم', 1),
      f('MgSO4', 'MgSO₄·7H₂O', 'سولفات منیزیم', 0.0986),
      fx('Mg', 'MgSO4', 'MgSO4anh', 'MgSO₄', 'سولفات منیزیم بی‌آب'),
      fx('Mg', 'Mg(NO3)2·6H2O', 'MgNO32', 'Mg(NO₃)₂·6H₂O', 'نیترات منیزیم'),
      fx('Mg', 'MgCl2·6H2O', 'MgCl2', 'MgCl₂·6H₂O', 'کلرید منیزیم'),
      fx('Mg', 'Mg(OH)2', 'MgOH2', 'Mg(OH)₂', 'هیدروکسید منیزیم'),
      fx('Mg', 'MgCO3', 'MgCO3', 'MgCO₃', 'کربنات منیزیم'),
    ] },
  { key: 'S', symbol: 'S', name: 'گوگرد', type: 'anion', defaultForm: 'SO3',
    forms: [
      f('SO3', 'SO₃', 'تری‌اکسید گوگرد', 32.06 / 80.06),
      f('S', 'S', 'گوگرد', 1),
      f('SO4', 'SO₄²⁻', 'یون سولفات', 32.06 / 96.06),
      f('H2SO4', 'H₂SO₄', 'اسید سولفوریک', 0.3269),
      f('NH42SO4', '(NH₄)₂SO₄', 'سولفات آمونیوم', 0.2427),
      f('K2SO4', 'K₂SO₄', 'سولفات پتاسیم', 0.184),
      f('MgSO4', 'MgSO₄·7H₂O', 'سولفات منیزیم', 0.1301),
      f('CaSO4', 'CaSO₄·2H₂O', 'سولفات کلسیم (گچ)', 0.1862),
      fx('S', 'MgSO4', 'MgSO4anh', 'MgSO₄', 'سولفات منیزیم بی‌آب'),
      fx('S', 'Na2SO4', 'Na2SO4', 'Na₂SO₄', 'سولفات سدیم'),
    ] },
  { key: 'Fe', symbol: 'Fe', name: 'آهن', type: 'cation', defaultForm: 'Fe',
    forms: [
      f('Fe', 'Fe', 'آهن', 1),
      f('FeSO4', 'FeSO₄·7H₂O', 'سولفات آهن', 0.2009),
      fx('Fe', 'FeCl3', 'FeCl3', 'FeCl₃', 'کلرید آهن ۳'),
      f('Fe2O3', 'Fe₂O₃', 'اکسید آهن ۳', (2 * 55.845) / 159.688),
      f('FeO', 'FeO', 'اکسید آهن ۲', 55.845 / 71.844),
    ] },
  { key: 'Mn', symbol: 'Mn', name: 'منگنز', type: 'cation', defaultForm: 'Mn',
    forms: [
      f('Mn', 'Mn', 'منگنز', 1),
      f('MnSO4', 'MnSO₄·4H₂O', 'سولفات منگنز', 0.2463),
      f('MnCl2', 'MnCl₂·4H₂O', 'کلرید منگنز', 0.2776),
      fx('Mn', 'MnSO4·H2O', 'MnSO4H2O', 'MnSO₄·H₂O', 'سولفات منگنز یک آبه'),
      f('MnO', 'MnO', 'اکسید منگنز ۲', 54.938 / 70.937),
      f('MnO2', 'MnO₂', 'اکسید منگنز ۴', 54.938 / 86.937),
    ] },
  { key: 'Zn', symbol: 'Zn', name: 'روی', type: 'cation', defaultForm: 'Zn',
    forms: [
      f('Zn', 'Zn', 'روی', 1),
      f('ZnSO4', 'ZnSO₄·7H₂O', 'سولفات روی', 0.2274),
      f('ZnCl2', 'ZnCl₂', 'کلرید روی', 0.4797),
      fx('Zn', 'ZnSO4·H2O', 'ZnSO4H2O', 'ZnSO₄·H₂O', 'سولفات روی یک آبه'),
      f('ZnO', 'ZnO', 'اکسید روی', 65.38 / 81.38),
    ] },
  { key: 'B', symbol: 'B', name: 'بور', type: 'anion', defaultForm: 'B',
    forms: [
      f('B', 'B', 'بور', 1),
      f('H3BO3', 'H₃BO₃', 'اسید بوریک', 0.1748),
      f('Borax', 'Na₂B₄O₇·10H₂O', 'تترا بورات سدیم (بوراکس)', 0.1134),
      f('B2O3', 'B₂O₃', 'اکسید بور', (2 * 10.811) / 69.62),
      fx('B', 'Na2B8O13·4H2O', 'Solubor', 'Na₂B₈O₁₃·4H₂O', 'سولوبور (بورات سدیم محلول)'),
    ] },
  { key: 'Cu', symbol: 'Cu', name: 'مس', type: 'cation', defaultForm: 'Cu',
    forms: [
      f('Cu', 'Cu', 'مس', 1),
      f('CuSO4', 'CuSO₄·5H₂O', 'سولفات مس', 0.2545),
      f('CuO', 'CuO', 'اکسید مس ۲', 63.546 / 79.545),
      f('Cu2O', 'Cu₂O', 'اکسید مس ۱', (2 * 63.546) / 143.091),
      fx('Cu', 'CuCl2·2H2O', 'CuCl2', 'CuCl₂·2H₂O', 'کلرید مس'),
    ] },
  { key: 'Mo', symbol: 'Mo', name: 'مولیبدن', type: 'anion', defaultForm: 'Mo',
    forms: [
      f('Mo', 'Mo', 'مولیبدن', 1),
      f('AHM', '(NH₄)₆Mo₇O₂₄', 'مولیبدات آمونیوم', 0.5771),
      f('NaMo', 'Na₆Mo₇O₂₄', 'مولیبدات سدیم', 0.5627),
      f('MoO3', 'MoO₃', 'اکسید مولیبدن', 95.95 / 143.95),
      fx('Mo', 'Na2MoO4·2H2O', 'Na2MoO4', 'Na₂MoO₄·2H₂O', 'مولیبدات سدیم دو آبه'),
    ] },
  { key: 'Si', symbol: 'Si', name: 'سیلیسیم', type: 'neutral', defaultForm: 'Si',
    forms: [
      f('Si', 'Si', 'سیلیسیم', 1),
      f('SiO2', 'SiO₂', 'سیلیس', 28.086 / 60.084),
      f('K2SiO3', 'K₂SiO₃', 'سیلیکات پتاسیم', 0.182),
      f('Na2SiO3', 'Na₂SiO₃', 'سیلیکات سدیم', 0.2301),
      f('H4SiO4', 'H₄SiO₄', 'اسید سیلیسیک', 28.086 / 96.115),
    ] },
  { key: 'Na', symbol: 'Na', name: 'سدیم', type: 'cation', defaultForm: 'Na2O',
    forms: [
      f('Na2O', 'Na₂O', 'اکسید سدیم', (2 * 22.99) / 61.979),
      f('Na', 'Na', 'سدیم', 1),
      fx('Na', 'NaCl', 'NaCl', 'NaCl', 'نمک خوراکی (کلرید سدیم)'),
      fx('Na', 'NaNO3', 'NaNO3', 'NaNO₃', 'نیترات سدیم'),
      fx('Na', 'Na2SO4', 'Na2SO4', 'Na₂SO₄', 'سولفات سدیم'),
      fx('Na', 'NaOH', 'NaOH', 'NaOH', 'هیدروکسید سدیم (سودسوزآور)'),
      fx('Na', 'NaHCO3', 'NaHCO3', 'NaHCO₃', 'بی‌کربنات سدیم'),
    ] },
  { key: 'Cl', symbol: 'Cl', name: 'کلر', type: 'anion', defaultForm: 'Cl',
    forms: [
      f('Cl', 'Cl', 'کلر', 1),
      fx('Cl', 'KCl', 'KCl', 'KCl', 'کلرید پتاسیم'),
      fx('Cl', 'NaCl', 'NaCl', 'NaCl', 'کلرید سدیم'),
      fx('Cl', 'CaCl2·6H2O', 'CaCl2', 'CaCl₂·6H₂O', 'کلرید کلسیم'),
      fx('Cl', 'MgCl2·6H2O', 'MgCl2', 'MgCl₂·6H₂O', 'کلرید منیزیم'),
      fx('Cl', 'NH4Cl', 'NH4Cl', 'NH₄Cl', 'کلرید آمونیوم'),
      fx('Cl', 'HCl', 'HCl', 'HCl', 'اسید کلریدریک'),
    ] },
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
  Si: ['si', 'sio2', 'سیلیسیم', 'سیلیس', 'سیلیکات'],
};

export const getElementDef = (key: string): ElementDef | undefined => ELEMENT_DEFS.find((e) => e.key === key);

// ============================================================
// 🧪 کلات‌ها (بخش جداگانه)
// مقدار واردشده = «درصد فلز» همان‌طور که روی برچسب محصول نوشته شده (مثلاً Fe ۶٪)،
// بنابراین ضریب همیشه ۱ است و هر درصدی (۶، ۷٫۵، ۱۰، ۱۳، ...) مجاز است.
// ============================================================
export interface ChelateAgent { key: string; label: string; stability?: string }
export const CHELATE_AGENTS: ChelateAgent[] = [
  { key: 'EDTA', label: 'EDTA', stability: 'پایدار تا pH حدود ۶٫۵' },
  { key: 'DTPA', label: 'DTPA', stability: 'پایدار تا pH حدود ۷٫۵' },
  { key: 'HEDTA', label: 'HEDTA', stability: 'پایدار تا pH حدود ۷' },
  { key: 'EDDHA', label: 'EDDHA', stability: 'پایدار تا pH حدود ۹ (مناسب آب قلیایی)' },
  { key: 'EDDS', label: 'EDDS', stability: 'پایدار تا pH حدود ۸' },
  { key: 'IDHA', label: 'IDHA', stability: 'پایدار تا pH حدود ۹' },
  { key: 'GLUCO', label: 'گلوکوهپتونات' },
  { key: 'AMINO', label: 'اسید آمینه (آمینوکلات)' },
  { key: 'LIGNO', label: 'لیگنوسولفونات' },
  { key: 'CITRATE', label: 'سیترات' },
  { key: 'OTHER', label: 'سایر / نامشخص' },
];
/** فلزهایی که کلات آن‌ها در بازار وجود دارد */
export const CHELATE_METALS = ['Fe', 'Mn', 'Zn', 'Cu', 'Mg', 'Ca'];
/** مقدار رایج فلز در محصول (فقط پیشنهاد سریع؛ مقدار واقعی را از برچسب محصول وارد کنید) */
export const CHELATE_PRESETS: Record<string, Record<string, number>> = {
  Fe: { EDTA: 13, DTPA: 11, EDDHA: 6, HEDTA: 5 },
  Mn: { EDTA: 13 },
  Zn: { EDTA: 15 },
  Cu: { EDTA: 15 },
  Mg: { EDTA: 6 },
  Ca: { EDTA: 10 },
};
export const CHELATE_PREFIX = 'chelate-';
export const chelateFormKey = (agent: string) => CHELATE_PREFIX + agent;
export const isChelateForm = (formKey: string) => formKey.startsWith(CHELATE_PREFIX);
export const chelateAgentOf = (formKey: string) => formKey.slice(CHELATE_PREFIX.length);
export const chelateAgentLabel = (formKey: string) =>
  CHELATE_AGENTS.find((a) => a.key === chelateAgentOf(formKey))?.label || chelateAgentOf(formKey);

/** فرم‌های قدیمیِ کلات که دیگر در منو نیستند؛ برای خواندن کودهای ذخیره‌شدهٔ قبلی نگه داشته شده‌اند */
export const LEGACY_CHELATES: Record<string, { agent: string; factor: number }> = {
  FeEDTA: { agent: 'EDTA', factor: 0.1 },
  MnEDTA: { agent: 'EDTA', factor: 0.05 },
  ZnEDTA14: { agent: 'EDTA', factor: 0.14 },
  ZnChel9: { agent: 'OTHER', factor: 0.09 },
};

export const getFactor = (elementKey: string, formKey: string): number => {
  if (isChelateForm(formKey)) return 1;
  if (LEGACY_CHELATES[formKey]) return LEGACY_CHELATES[formKey].factor;
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
  return Object.keys(lv).some((k) => {
    const form = (k.split('|')[1] || '').toLowerCase();
    if (form === q) return true;
    // جستجوی «کلات» یا نام عامل کلات‌ساز (eddha، edta، ...)
    if (form.startsWith(CHELATE_PREFIX)) return q === 'کلات' || q === 'chelate' || form.slice(CHELATE_PREFIX.length) === q;
    return false;
  });
};
