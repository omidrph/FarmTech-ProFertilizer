// frontend/src/components/features/widgets/ph/phChemistry.ts
// ============================================================
// شیمی پایه‌ی ماشین‌حساب pH (توابع خالص، بدون وابستگی به Vue)
// مرجع: «گزارش فنی اصلاح‌شده – سیستم اصلاح pH» نسخه ۳٫۰
//
// فرض‌های مدل (به کاربر هم نمایش داده می‌شود):
//   • سیستم بسته است (CO₂ با هوا تبادل نمی‌کند؛ C_T ثابت می‌ماند)
//   • ضریب فعالیت = ۱ (از قدرت یونی صرف‌نظر شده است)
//   • آلکالینیتی فقط از کربنات/بی‌کربنات/هیدروکسید می‌آید
// ============================================================

export interface CarbonateConstants {
  K1: number;
  K2: number;
  Kw: number;
  pK1: number;
  pK2: number;
  pKw: number;
}

/**
 * ثابت‌های تعادل کربنات و آب بر حسب دما (°C)
 * pK1 و pK2: Plummer & Busenberg (1982)؛ pKw: رابطه‌ی Millero
 */
export function carbonateConstants(temperatureC: number): CarbonateConstants {
  const T = temperatureC + 273.15;
  const pK1 =
    356.3094 + 0.06091964 * T - 21834.37 / T - 126.8339 * Math.log10(T) + 1684915 / (T * T);
  const pK2 =
    107.8871 + 0.03252849 * T - 5151.79 / T - 38.92561 * Math.log10(T) + 563713.9 / (T * T);
  const pKw = 4470.99 / T - 6.0875 + 0.01706 * T;
  return { K1: 10 ** -pK1, K2: 10 ** -pK2, Kw: 10 ** -pKw, pK1, pK2, pKw };
}

/** کسرهای گونه‌ای کربنات: α₀ (H₂CO₃*)، α₁ (HCO₃⁻)، α₂ (CO₃²⁻) */
export function carbonateFractions(pH: number, c: CarbonateConstants) {
  const H = 10 ** -pH;
  const D = H * H + c.K1 * H + c.K1 * c.K2;
  return { a0: (H * H) / D, a1: (c.K1 * H) / D, a2: (c.K1 * c.K2) / D };
}

/** آلکالینیتی (eq/L) در مدل کربناتی: C_T(α₁+2α₂) + Kw/H − H */
export function alkalinityFromCT(pH: number, CT: number, c: CarbonateConstants): number {
  const H = 10 ** -pH;
  const { a1, a2 } = carbonateFractions(pH, c);
  return CT * (a1 + 2 * a2) + c.Kw / H - H;
}

/** تخمین C_T (mol/L) از آلکالینیتی و pH اولیه (وارونِ رابطه‌ی بالا) */
export function totalCarbonFromAlkalinity(pH: number, alkEqL: number, c: CarbonateConstants): number {
  const H = 10 ** -pH;
  const { a1, a2 } = carbonateFractions(pH, c);
  return (alkEqL - c.Kw / H + H) / (a1 + 2 * a2);
}

// pKa های اسید فسفریک در ۲۵°C
const PK_PHOSPHATE = [2.15, 7.2, 12.35] as const;

/** کسرهای گونه‌ای فسفات: H₃PO₄، H₂PO₄⁻، HPO₄²⁻، PO₄³⁻ */
export function phosphateFractions(pH: number) {
  const H = 10 ** -pH;
  const [k1, k2, k3] = PK_PHOSPHATE.map(pk => 10 ** -pk);
  const D = H ** 3 + k1 * H ** 2 + k1 * k2 * H + k1 * k2 * k3;
  return {
    f0: H ** 3 / D,
    f1: (k1 * H ** 2) / D,
    f2: (k1 * k2 * H) / D,
    f3: (k1 * k2 * k3) / D
  };
}

/**
 * ظرفیت مؤثر (meq بر mmol) اسید فسفریک در pH هدف.
 * با مرجع H₂PO₄⁻ برای آلکالینیتی، افزودن H₃PO₄ دقیقاً ۱ eq/mol آلکالینیتی می‌کاهد
 * و خودِ گونه‌های فسفات نیز در pH هدف سهم دارند:
 *   z_eff = 1 + (α HPO₄²⁻ + 2·α PO₄³⁻ − α H₃PO₄)
 * (در pH≈۷ حدود ۱٫۴ و در pH≈۶ حدود ۱٫۱؛ یعنی «۳» ثابت نیست.)
 */
export function phosphoricEffectiveZ(targetPH: number): number {
  const { f0, f2, f3 } = phosphateFractions(targetPH);
  return 1 + f2 + 2 * f3 - f0;
}

/** mg/L as CaCO₃ ↔ meq/L */
export const mgLCaCO3ToMeqL = (mgL: number) => mgL / 50;
export const meqLToMgLCaCO3 = (meqL: number) => meqL * 50;
