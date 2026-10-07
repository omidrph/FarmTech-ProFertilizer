// frontend/src/utils/fertilizerUnits.ts
// ============================================================
// واحدهای کود: جامد → گرم/کیلوگرم ، مایع → میلی‌لیتر/لیتر
// ------------------------------------------------------------
// بک‌اند و بهینه‌ساز همه‌چیز را «گرم محصول تجاری» نگه می‌دارند. کود مایع فقط در نمایش
// و ورودی کاربر به حجم تبدیل می‌شود: حجم(mL) = جرم(g) ÷ چگالی(g/mL).
// ============================================================

export type MassUnit = 'g' | 'kg';
export type VolumeUnit = 'ml' | 'l';
export type AmountUnit = MassUnit | VolumeUnit;

interface UnitInfo {
  form?: string | null;
  densityGMl?: number | null;
}

/** آیا این کود به‌صورت حجمی (لیتر) مصرف/نمایش داده شود؟ (مایع و چگالی معتبر) */
export function isLiquid(f: UnitInfo | null | undefined): boolean {
  return !!f && f.form === 'liquid';
}

export function canShowVolume(f: UnitInfo | null | undefined): boolean {
  return isLiquid(f) && !!f?.densityGMl && f.densityGMl > 0;
}

export function amountToGrams(amount: number, unit: AmountUnit, densityGMl?: number | null): number | null {
  if (!Number.isFinite(amount)) return null;
  if (unit === 'g') return amount;
  if (unit === 'kg') return amount * 1000;
  if (!densityGMl || densityGMl <= 0) return null;
  return (unit === 'l' ? amount * 1000 : amount) * densityGMl;
}

const fa = (n: number, d: number) =>
  new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d, minimumFractionDigits: 0 }).format(n);

export function formatMass(grams: number): string {
  if (!Number.isFinite(grams)) return '—';
  if (grams >= 1000) return `${fa(grams / 1000, 3)} کیلوگرم`;
  return `${fa(grams, grams < 10 ? 2 : 1)} گرم`;
}

export function formatVolumeMl(ml: number): string {
  if (!Number.isFinite(ml)) return '—';
  if (ml >= 1000) return `${fa(ml / 1000, 3)} لیتر`;
  return `${fa(ml, ml < 10 ? 2 : 1)} میلی‌لیتر`;
}

/**
 * مقدار قابل‌نمایش یک کود از روی جرم (گرم):
 *  - مایع با چگالی → «۲٫۵ لیتر» (و جرم معادل در پرانتز اگر خواسته شود)
 *  - غیر این صورت → «۱٫۲ کیلوگرم»
 */
export function formatFertilizerAmount(grams: number, f?: UnitInfo | null, withMass = false): string {
  if (canShowVolume(f)) {
    const ml = grams / (f!.densityGMl as number);
    const base = formatVolumeMl(ml);
    return withMass ? `${base} (${formatMass(grams)})` : base;
  }
  return formatMass(grams);
}

/** واحدهای قابل انتخاب برای ورود مقدار */
export function unitOptions(f: UnitInfo | null | undefined): Array<{ value: AmountUnit; label: string }> {
  if (canShowVolume(f)) {
    return [
      { value: 'ml', label: 'میلی‌لیتر' },
      { value: 'l', label: 'لیتر' },
      { value: 'g', label: 'گرم' },
      { value: 'kg', label: 'کیلوگرم' }
    ];
  }
  return [
    { value: 'g', label: 'گرم' },
    { value: 'kg', label: 'کیلوگرم' }
  ];
}

export function defaultUnit(f: UnitInfo | null | undefined): AmountUnit {
  return canShowVolume(f) ? 'ml' : 'g';
}

export function unitLabel(unit: AmountUnit): string {
  return { g: 'گرم', kg: 'کیلوگرم', ml: 'میلی‌لیتر', l: 'لیتر' }[unit];
}

/** قیمت: ذخیره همیشه به‌ازای کیلوگرم؛ ورودی/نمایش مایع به‌ازای لیتر */
export function pricePerLiter(pricePerKg: number, densityGMl?: number | null): number | null {
  return densityGMl && densityGMl > 0 ? pricePerKg * densityGMl : null;
}
export function pricePerKgFromLiter(pricePerLiter: number, densityGMl: number): number {
  return pricePerLiter / densityGMl;
}
