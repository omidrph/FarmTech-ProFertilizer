// frontend/src/utils/errorLevels.ts
// منطق یکپارچهٔ «خطای نسخه‌دهی»: جداسازی ماکرو/میکرو + سه‌رنگ
//   تا ۵٪ = سبز (قابل قبول) | ۵ تا ۱۰٪ = زرد (هشدار) | بالای ۱۰٪ = قرمز (عدم اعتماد)

export type ErrorLevel = 'ok' | 'warn' | 'bad';
export type ElementGroup = 'macro' | 'micro';

export const ERROR_OK_MAX = 5;
export const ERROR_WARN_MAX = 10;

// دسته‌بندی هم‌راستا با تب «عناصر هدف» (Na و Cl در گروه پرمصرف)
export const MACRO_ELEMENTS = ['N-NO3', 'N-NH4', 'P', 'K', 'Ca', 'Mg', 'S', 'Na', 'Cl'];
export const MICRO_ELEMENTS = ['Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Si'];

export const GROUP_TITLES: Record<ElementGroup, string> = {
  macro: 'عناصر ماکرو (پرمصرف)',
  micro: 'عناصر میکرو (کم‌مصرف)'
};

export function elementGroup(el: string): ElementGroup {
  return MICRO_ELEMENTS.includes(el) ? 'micro' : 'macro';
}

export function errorLevel(absPct: number): ErrorLevel {
  if (!isFinite(absPct)) return 'bad';
  // گرد کردن به یک رقم اعشار تا ۵٫۰۰۱ در برچسب «۵٫۰» زرد نشود
  const v = Math.round(absPct * 10) / 10;
  return v <= ERROR_OK_MAX ? 'ok' : v <= ERROR_WARN_MAX ? 'warn' : 'bad';
}

export const LEVEL_LABEL: Record<ErrorLevel, string> = {
  ok: 'قابل قبول',
  warn: 'هشدار',
  bad: 'عدم اعتماد'
};

export const LEVEL_CLASS: Record<ErrorLevel, { text: string; bg: string; border: string; dot: string; ring: string }> = {
  ok: { text: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800', dot: 'bg-emerald-500', ring: 'stroke-emerald-500' },
  warn: { text: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800', dot: 'bg-amber-500', ring: 'stroke-amber-500' },
  bad: { text: 'text-rose-600 dark:text-rose-400', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800', dot: 'bg-rose-500', ring: 'stroke-rose-500' }
};

export interface ElementError {
  element: string;
  group: ElementGroup;
  target: number;
  actual: number;
  deviationPct: number; // علامت‌دار: مثبت = بیش‌تأمین
  absPct: number;
  level: ErrorLevel;
}

export interface GroupError {
  group: ElementGroup;
  count: number;
  meanAbs: number; // میانگین خطای مطلق (٪)
  maxAbs: number;
  level: ErrorLevel; // بر پایهٔ میانگین خطای مطلق گروه
  worst: string | null;
  /** پوشش گروه (٪) دقیقاً مثل حلقه‌های عناصر: میانگین min(فعلی/هدف، ۱) */
  coverage: number;
  /** میانگین بیش‌تأمین (٪) برای حلقهٔ بیرونی قرمز */
  over: number;
  rows: ElementError[];
}

export function computeElementErrors(targets: Record<string, number>, actual: Record<string, number>): ElementError[] {
  return Object.entries(targets || {})
    .filter(([, t]) => Number(t) > 0)
    .map(([element, t]) => {
      const target = Number(t);
      const act = Number(actual?.[element] || 0);
      const deviationPct = (act / target - 1) * 100;
      const absPct = Math.abs(deviationPct);
      return { element, group: elementGroup(element), target, actual: act, deviationPct, absPct, level: errorLevel(absPct) };
    });
}

export function computeGroupErrors(targets: Record<string, number>, actual: Record<string, number>) {
  const rows = computeElementErrors(targets, actual);
  const build = (group: ElementGroup): GroupError => {
    const rs = rows.filter((r) => r.group === group);
    const meanAbs = rs.length ? rs.reduce((s, r) => s + r.absPct, 0) / rs.length : 0;
    const worstRow = rs.reduce<ElementError | null>((w, r) => (!w || r.absPct > w.absPct ? r : w), null);
    const maxAbs = worstRow ? worstRow.absPct : 0;
    const coverage = rs.length ? (rs.reduce((a, r) => a + Math.min(r.actual / r.target, 1), 0) / rs.length) * 100 : 0;
    const over = rs.length ? (rs.reduce((a, r) => a + Math.max(r.actual / r.target - 1, 0), 0) / rs.length) * 100 : 0;
    return { group, count: rs.length, meanAbs, maxAbs, level: errorLevel(meanAbs), worst: worstRow?.element ?? null, coverage, over, rows: rs };
  };
  return { macro: build('macro'), micro: build('micro'), all: rows };
}

export const faNum = (v: number, digits = 1): string =>
  isFinite(v) ? v.toLocaleString('fa-IR', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : '—';
