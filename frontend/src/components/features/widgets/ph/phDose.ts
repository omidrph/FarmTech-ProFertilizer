// frontend/src/components/features/widgets/ph/phDose.ts
// ============================================================
// محاسبه‌ی دوز اصلاح pH (توابع خالص)
//   مسیر ۱) مدل تئوریک سیستم کربنات (فقط آب ساده)
//   مسیر ۲) تیتراسیون واقعی نمونه (روش پیشنهادی برای محلول‌های غذایی/ترکیبی)
// مرجع: گزارش فنی اصلاح‌شده – سیستم اصلاح pH (نسخه ۳٫۰)
//
// اصل مهم: هیچ جدول عمومی «pH هدف → آلکالینیتی» استفاده نمی‌شود.
// ============================================================
import {
  carbonateConstants,
  alkalinityFromCT,
  totalCarbonFromAlkalinity,
  phosphoricEffectiveZ
} from './phChemistry';

export type ChemicalKind = 'acid' | 'base';

export interface Chemical {
  id: string;
  name: string;
  formula: string;
  kind: ChemicalKind;
  /** جرم مولی (g/mol) */
  mw: number;
  /** ظرفیت مؤثر واکنش؛ برای اسید فسفریک وابسته به pH است و محاسبه می‌شود */
  z: number | 'phosphoric';
  /** خلوص تجاری (٪ وزنی) */
  purityPct: number;
  /** چگالی محصول تجاری (g/mL) */
  densityGmL: number;
  custom?: boolean;
}

/** مقادیر تجاری نمونه؛ برای محاسبه‌ی واقعی باید از برگه‌ی مشخصات محصول اصلاح شوند */
export const CHEMICALS: Chemical[] = [
  { id: 'hcl', name: 'اسید کلریدریک', formula: 'HCl', kind: 'acid', mw: 36.46, z: 1, purityPct: 37, densityGmL: 1.19 },
  { id: 'h2so4', name: 'اسید سولفوریک', formula: 'H₂SO₄', kind: 'acid', mw: 98.08, z: 2, purityPct: 98, densityGmL: 1.84 },
  { id: 'hno3', name: 'اسید نیتریک', formula: 'HNO₃', kind: 'acid', mw: 63.01, z: 1, purityPct: 65, densityGmL: 1.4 },
  { id: 'h3po4', name: 'اسید فسفریک', formula: 'H₃PO₄', kind: 'acid', mw: 97.99, z: 'phosphoric', purityPct: 85, densityGmL: 1.7 },
  { id: 'naoh', name: 'سدیم هیدروکسید', formula: 'NaOH', kind: 'base', mw: 40.0, z: 1, purityPct: 10, densityGmL: 1.11 },
  { id: 'custom-acid', name: 'اسید دلخواه', formula: '—', kind: 'acid', mw: 36.46, z: 1, purityPct: 100, densityGmL: 1.0, custom: true },
  { id: 'custom-base', name: 'باز دلخواه', formula: '—', kind: 'base', mw: 40.0, z: 1, purityPct: 100, densityGmL: 1.0, custom: true }
];

export interface DoseInputBase {
  volumeL: number;
  currentPH: number;
  targetPH: number;
  temperatureC: number;
  chemical: Chemical;
}

export interface TheoreticalInput extends DoseInputBase {
  /** آلکالینیتی نمونه (mg/L as CaCO₃) */
  alkalinityMgL: number;
  sampleType: 'simple' | 'complex';
}

export interface TitrationPoint {
  /** حجم تجمعی تیترانت افزوده‌شده (mL) */
  volumeMl: number;
  pH: number;
}

export interface TitrationInput extends DoseInputBase {
  /** نقاط پس از نقطه‌ی اولیه (حجم > ۰)؛ نقطه‌ی اولیه = (۰، pH فعلی) خودکار افزوده می‌شود */
  points: TitrationPoint[];
  /** نرمالیته‌ی تیترانت استاندارد (eq/L) */
  normality: number;
  /** حجم نمونه‌ی تیتراسیون (mL) */
  sampleVolumeMl: number;
}

export interface DoseSuccess {
  ok: true;
  method: 'theoretical' | 'titration' | 'no-adjustment';
  direction: 'acid' | 'base' | 'none';
  /** معادل شیمیایی کل (meq) */
  totalMeq: number;
  /** ظرفیت مؤثر به‌کاررفته در تبدیل */
  effectiveZ: number;
  pureMassG: number;
  commercialMassG: number;
  commercialVolumeL: number;
  /** بازه‌ی حساسیت به خطای اندازه‌گیری (فقط مدل تئوریک) */
  sensitivity?: { minL: number; maxL: number };
  theoretical?: {
    ctMmolL: number;
    initialAlkMgL: number;
    targetAlkMgL: number;
    deltaMeqL: number;
    pK1: number;
    pK2: number;
  };
  titration?: {
    fromVolumeMl: number;
    toVolumeMl: number;
    doseMl: number;
    meqPerL: number;
  };
  warnings: string[];
}

export interface DoseFailure {
  ok: false;
  error: string;
  /** وقتی true باشد، رابط کاربری کاربر را به مسیر تیتراسیون هدایت می‌کند */
  needTitration?: boolean;
}

export type DoseResult = DoseSuccess | DoseFailure;

const PH_TOLERANCE = 0.005;
const PH_MIN = 3;
const PH_MAX = 11;

// ------------------------------------------------------------
// اعتبارسنجی مشترک
// ------------------------------------------------------------
export function validateBase(input: DoseInputBase): string | null {
  const { volumeL, currentPH, targetPH, temperatureC, chemical } = input;

  if (!(volumeL > 0)) return 'حجم محلول باید بزرگ‌تر از صفر باشد.';
  if (!(currentPH >= PH_MIN && currentPH <= PH_MAX)) return `pH فعلی باید بین ${PH_MIN} تا ${PH_MAX} باشد.`;
  if (!(targetPH >= PH_MIN && targetPH <= PH_MAX)) return `pH هدف باید بین ${PH_MIN} تا ${PH_MAX} باشد.`;
  if (!(temperatureC >= 0 && temperatureC <= 60)) return 'دما باید بین ۰ تا ۶۰ درجه‌ی سانتی‌گراد باشد.';

  if (!(chemical.mw > 0)) return 'جرم مولی ماده شیمیایی نامعتبر است.';
  if (chemical.z !== 'phosphoric' && !(chemical.z > 0)) return 'ظرفیت مؤثر ماده شیمیایی نامعتبر است.';
  if (!(chemical.purityPct > 0 && chemical.purityPct <= 100)) return 'خلوص باید بین ۰ تا ۱۰۰ درصد باشد.';
  if (!(chemical.densityGmL > 0)) return 'چگالی ماده شیمیایی نامعتبر است.';

  if (Math.abs(currentPH - targetPH) >= PH_TOLERANCE) {
    const needed: ChemicalKind = targetPH < currentPH ? 'acid' : 'base';
    if (chemical.kind !== needed) {
      return needed === 'acid'
        ? 'برای کاهش pH باید یک «اسید» انتخاب کنید.'
        : 'برای افزایش pH باید یک «باز» انتخاب کنید.';
    }
  }
  return null;
}

const zeroResult = (): DoseSuccess => ({
  ok: true,
  method: 'no-adjustment',
  direction: 'none',
  totalMeq: 0,
  effectiveZ: 1,
  pureMassG: 0,
  commercialMassG: 0,
  commercialVolumeL: 0,
  warnings: []
});

// ------------------------------------------------------------
// تبدیل معادل شیمیایی به ماده‌ی خالص و ماده‌ی تجاری (بخش ۷ گزارش)
//   جرم خالص (g)   = meq × (MW / z) ÷ 1000
//   حجم تجاری (L)  = جرم خالص ÷ (خلوص × چگالی × 1000)
// ------------------------------------------------------------
export function equivalentsToCommercial(totalMeq: number, chemical: Chemical, targetPH: number) {
  const z = chemical.z === 'phosphoric' ? phosphoricEffectiveZ(targetPH) : chemical.z;
  const pureMassG = (totalMeq * (chemical.mw / z)) / 1000;
  const purity = chemical.purityPct / 100;
  const commercialMassG = pureMassG / purity;
  const commercialVolumeL = commercialMassG / chemical.densityGmL / 1000;
  return { effectiveZ: z, pureMassG, commercialMassG, commercialVolumeL };
}

const directionOf = (currentPH: number, targetPH: number): 'acid' | 'base' =>
  targetPH < currentPH ? 'acid' : 'base';

const commonWarnings = (input: DoseInputBase): string[] => {
  const list: string[] = [];
  if (input.chemical.z === 'phosphoric') {
    list.push(
      'برای اسید فسفریک ظرفیت ثابت ۳ استفاده نشده است؛ ظرفیت مؤثر بر اساس گونه‌بندی فسفات در pH هدف محاسبه شد.'
    );
  }
  if (input.chemical.kind === 'base') {
    list.push('در افزایش pH، خروج CO₂ و ترکیب محلول می‌تواند دوز واقعی را تغییر دهد؛ حتماً مرحله‌ای تزریق و اندازه‌گیری کنید.');
  }
  return list;
};

// ------------------------------------------------------------
// مسیر ۱: مدل تئوریک کربنات
// ------------------------------------------------------------

/** معادل کل (meq) در مدل کربناتی؛ null یعنی مدل برای این ورودی معتبر نیست */
function theoreticalTotalMeq(
  alkMgL: number,
  currentPH: number,
  targetPH: number,
  temperatureC: number,
  volumeL: number
) {
  const c = carbonateConstants(temperatureC);
  const alkEqL = alkMgL / 50000;
  const CT = totalCarbonFromAlkalinity(currentPH, alkEqL, c);
  if (!(CT > 0)) return null;

  const targetAlkEqL = alkalinityFromCT(targetPH, CT, c);
  const acid = targetPH < currentPH;
  const deltaEqL = acid ? alkEqL - targetAlkEqL : targetAlkEqL - alkEqL;
  if (!(deltaEqL > 0)) return null;

  return {
    totalMeq: deltaEqL * 1000 * volumeL,
    deltaMeqL: deltaEqL * 1000,
    ctMmolL: CT * 1000,
    targetAlkMgL: targetAlkEqL * 50000,
    pK1: c.pK1,
    pK2: c.pK2
  };
}

export function calculateTheoretical(input: TheoreticalInput): DoseResult {
  const baseError = validateBase(input);
  if (baseError) return { ok: false, error: baseError };

  if (Math.abs(input.currentPH - input.targetPH) < PH_TOLERANCE) return zeroResult();

  if (input.sampleType === 'complex') {
    return {
      ok: false,
      needTitration: true,
      error:
        'برای محلول غذایی یا ترکیبی، مدل عمومی کربناتی قابل اتکا نیست (فسفات، آمونیوم و اسیدهای آلی بر ظرفیت اسیدی/بازی اثر دارند). لطفاً از روش «تیتراسیون واقعی» استفاده کنید.'
    };
  }

  if (!(input.alkalinityMgL > 0)) {
    return {
      ok: false,
      needTitration: true,
      error: 'آلکالینیتی باید بزرگ‌تر از صفر باشد. اگر آلکالینیتی نمونه بسیار کم است، مدل کربناتی مناسب نیست و تیتراسیون واقعی لازم است.'
    };
  }

  const core = theoreticalTotalMeq(
    input.alkalinityMgL,
    input.currentPH,
    input.targetPH,
    input.temperatureC,
    input.volumeL
  );
  if (!core) {
    return {
      ok: false,
      needTitration: true,
      error: 'با این ورودی‌ها مدل کربناتی نتیجه‌ی معتبری نمی‌دهد (آلکالینیتی و pH با هم سازگار نیستند). مقادیر را بررسی کنید یا از تیتراسیون واقعی استفاده کنید.'
    };
  }

  const conv = equivalentsToCommercial(core.totalMeq, input.chemical, input.targetPH);

  // حساسیت به خطای اندازه‌گیری: آلکالینیتی ±۱۰٪ و pH فعلی ±۰٫۱
  const volumes: number[] = [];
  for (const alkFactor of [0.9, 1, 1.1]) {
    for (const phShift of [-0.1, 0, 0.1]) {
      const r = theoreticalTotalMeq(
        input.alkalinityMgL * alkFactor,
        input.currentPH + phShift,
        input.targetPH,
        input.temperatureC,
        input.volumeL
      );
      if (r) volumes.push(equivalentsToCommercial(r.totalMeq, input.chemical, input.targetPH).commercialVolumeL);
    }
  }

  const warnings = commonWarnings(input);
  if (input.currentPH < 6 || input.currentPH > 9.5) {
    warnings.push('pH فعلی خارج از محدوده‌ی معمول آب‌های کربناتی (۶ تا ۹٫۵) است؛ دقت مدل کمتر می‌شود.');
  }
  if (input.targetPH < 5 || input.targetPH > 9.5) {
    warnings.push('pH هدف در ناحیه‌ای است که فرض‌های مدل کربناتی ضعیف‌تر می‌شوند.');
  }

  return {
    ok: true,
    method: 'theoretical',
    direction: directionOf(input.currentPH, input.targetPH),
    totalMeq: core.totalMeq,
    ...conv,
    sensitivity: volumes.length ? { minL: Math.min(...volumes), maxL: Math.max(...volumes) } : undefined,
    theoretical: {
      ctMmolL: core.ctMmolL,
      initialAlkMgL: input.alkalinityMgL,
      targetAlkMgL: core.targetAlkMgL,
      deltaMeqL: core.deltaMeqL,
      pK1: core.pK1,
      pK2: core.pK2
    },
    warnings
  };
}

// ------------------------------------------------------------
// مسیر ۲: تیتراسیون واقعی (میان‌یابی خطی روی منحنی pH–حجم)
// ------------------------------------------------------------
export function calculateTitration(input: TitrationInput): DoseResult {
  const baseError = validateBase(input);
  if (baseError) return { ok: false, error: baseError };

  if (Math.abs(input.currentPH - input.targetPH) < PH_TOLERANCE) return zeroResult();

  if (!(input.normality > 0)) return { ok: false, error: 'نرمالیته‌ی تیترانت باید بزرگ‌تر از صفر باشد.' };
  if (!(input.sampleVolumeMl > 0)) return { ok: false, error: 'حجم نمونه‌ی تیتراسیون باید بزرگ‌تر از صفر باشد.' };
  if (!input.points.length) return { ok: false, error: 'حداقل یک نقطه‌ی تیتراسیون (حجم و pH) وارد کنید.' };

  for (const p of input.points) {
    if (!(p.volumeMl > 0)) return { ok: false, error: 'حجم تیترانت در هر نقطه باید بزرگ‌تر از صفر باشد.' };
    if (!(p.pH >= 0 && p.pH <= 14)) return { ok: false, error: 'pH هر نقطه باید بین ۰ تا ۱۴ باشد.' };
  }

  const curve: TitrationPoint[] = [{ volumeMl: 0, pH: input.currentPH }, ...input.points].sort(
    (a, b) => a.volumeMl - b.volumeMl
  );
  for (let i = 1; i < curve.length; i++) {
    if (curve[i].volumeMl === curve[i - 1].volumeMl) {
      return { ok: false, error: 'حجم‌های تیترانت باید متفاوت باشند (حجم تکراری وجود دارد).' };
    }
  }

  const direction = directionOf(input.currentPH, input.targetPH);
  const warnings = commonWarnings(input);

  // اولین بازه‌ای که pH هدف را قطع می‌کند
  let found: { i: number; volumeMl: number } | null = null;
  for (let i = 0; i < curve.length - 1; i++) {
    const a = curve[i];
    const b = curve[i + 1];
    if ((a.pH - input.targetPH) * (b.pH - input.targetPH) <= 0 && a.pH !== b.pH) {
      const fraction = (input.targetPH - a.pH) / (b.pH - a.pH);
      found = { i, volumeMl: a.volumeMl + fraction * (b.volumeMl - a.volumeMl) };
      break;
    }
  }

  if (!found) {
    const phs = curve.map(p => p.pH);
    const lo = Math.min(...phs).toFixed(2);
    const hi = Math.max(...phs).toFixed(2);
    return {
      ok: false,
      error: `pH هدف خارج از محدوده‌ی داده‌های تیتراسیون شما (${lo} تا ${hi}) است. برای پرهیز از برون‌یابی، تیتراسیون را تا رسیدن به pH هدف ادامه دهید و نقطه‌های بیشتری ثبت کنید.`
    };
  }

  const movesTowardTarget = direction === 'acid' ? curve[1].pH < curve[0].pH : curve[1].pH > curve[0].pH;
  if (!movesTowardTarget) {
    return {
      ok: false,
      error:
        direction === 'acid'
          ? 'با افزودن تیترانت، pH باید کاهش یابد؛ داده‌ها با تیتراسیون «اسیدی» سازگار نیستند.'
          : 'با افزودن تیترانت، pH باید افزایش یابد؛ داده‌ها با تیتراسیون «بازی» سازگار نیستند.'
    };
  }

  // اگر منحنی در جهت هدف یکنواخت نباشد، هشدار
  for (let i = 0; i < curve.length - 1; i++) {
    const step = curve[i + 1].pH - curve[i].pH;
    if ((direction === 'acid' && step > 0) || (direction === 'base' && step < 0)) {
      warnings.push('منحنی تیتراسیون یکنواخت نیست (در برخی نقاط pH خلاف جهت انتظار حرکت کرده)؛ اختلاط و قرائت‌ها را بررسی کنید.');
      break;
    }
  }

  const meqPerL = (found.volumeMl * input.normality) / (input.sampleVolumeMl / 1000);
  const totalMeq = meqPerL * input.volumeL;
  const conv = equivalentsToCommercial(totalMeq, input.chemical, input.targetPH);

  if (curve.length < 4) {
    warnings.push('تعداد نقاط کم است؛ با نقاط بیشتر، میان‌یابی دقیق‌تر می‌شود.');
  }

  return {
    ok: true,
    method: 'titration',
    direction,
    totalMeq,
    ...conv,
    titration: {
      fromVolumeMl: curve[found.i].volumeMl,
      toVolumeMl: curve[found.i + 1].volumeMl,
      doseMl: found.volumeMl,
      meqPerL
    },
    warnings
  };
}
