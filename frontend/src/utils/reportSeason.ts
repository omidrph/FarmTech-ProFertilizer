// frontend/src/utils/reportSeason.ts
// فصل از روی تاریخ گزارش خوانده می‌شود (کاربر دستی وارد نمی‌کند)

const SEASONS = ['بهار', 'تابستان', 'پاییز', 'زمستان'];

const toLatinDigits = (s: string): string =>
  s.replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d))).replace(/[٠-٩]/g, (d) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(d)));

/** تاریخ شمسی (۱۴۰۵/۰۸/۰۱) یا میلادی (2026/10/23) → نام فصل؛ اگر قابل‌خواندن نبود رشتهٔ خالی */
export function seasonFromDate(date: string | null | undefined): string {
  const m = toLatinDigits(String(date || '')).match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/);
  if (!m) return '';
  const y = +m[1];
  let month = +m[2];
  const day = +m[3];
  if (y > 1700) {
    try {
      const jm = new Intl.DateTimeFormat('fa-IR-u-nu-latn', { month: 'numeric' }).format(new Date(y, month - 1, day));
      month = parseInt(jm, 10);
    } catch {
      return '';
    }
  }
  if (!(month >= 1 && month <= 12)) return '';
  return SEASONS[Math.floor((month - 1) / 3)];
}