// frontend/src/components/features/widgets/ph/phFormat.ts
// ابزارهای ورودی/خروجی عددی (پشتیبانی از ارقام فارسی و عربی)

const PERSIAN = '۰۱۲۳۴۵۶۷۸۹';
const ARABIC = '٠١٢٣٤٥٦٧٨٩';

/** رشته‌ی عددی (حتی با ارقام فارسی، ۳٫۵ یا ۳،۵) را به عدد تبدیل می‌کند؛ نامعتبر = null */
export function parseNum(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined) return null;
  if (typeof value === 'number') return Number.isFinite(value) ? value : null;

  let s = String(value).trim();
  if (!s) return null;

  s = s
    .replace(/[۰-۹]/g, d => String(PERSIAN.indexOf(d)))
    .replace(/[٠-٩]/g, d => String(ARABIC.indexOf(d)))
    .replace(/[٫،,]/g, '.')
    .replace(/\s+/g, '');

  if (!/^[-+]?\d*\.?\d+$|^[-+]?\d+\.$/.test(s)) return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** نمایش عدد با ارقام فارسی و تعداد اعشار مناسب */
export function fmt(value: number, maxDecimals = 2): string {
  if (!Number.isFinite(value)) return '—';
  return value.toLocaleString('fa-IR', { maximumFractionDigits: maxDecimals });
}

/** مقدار حجم (لیتر) را به‌صورت «میلی‌لیتر» یا «لیتر» خوانا نشان می‌دهد */
export function fmtVolumeL(liters: number): string {
  if (!Number.isFinite(liters)) return '—';
  if (liters < 1) return `${fmt(liters * 1000, liters * 1000 < 10 ? 1 : 0)} میلی‌لیتر`;
  return `${fmt(liters, liters < 10 ? 2 : 1)} لیتر`;
}

/** مقدار جرم (گرم) را به‌صورت «گرم» یا «کیلوگرم» نشان می‌دهد */
export function fmtMassG(grams: number): string {
  if (!Number.isFinite(grams)) return '—';
  if (grams >= 1000) return `${fmt(grams / 1000, 2)} کیلوگرم`;
  return `${fmt(grams, grams < 10 ? 2 : 1)} گرم`;
}
