// ابزارهای مشترک نمودارهای پنل مدیریت (SVG خالص، بدون کتابخانه)

export const faNum = (v: number, digits = 0): string =>
  isFinite(v) ? v.toLocaleString('fa-IR', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : '—';

/** عدد کوتاه: ۱٫۲ هزار */
export const faShort = (v: number): string => {
  const a = Math.abs(v);
  if (a >= 1_000_000) return faNum(v / 1_000_000, 1) + ' م';
  if (a >= 10_000) return faNum(v / 1000, 0) + ' هزار';
  if (a >= 1_000) return faNum(v / 1000, 1) + ' هزار';
  return faNum(v, Number.isInteger(v) ? 0 : 1);
};

/** تاریخ کوتاه شمسی از رشتهٔ YYYY-MM-DD */
export const faDay = (iso: string, withMonthName = false): string => {
  const d = new Date(iso + 'T12:00:00');
  if (isNaN(d.getTime())) return iso;
  return withMonthName
    ? d.toLocaleDateString('fa-IR', { month: 'long', day: 'numeric' })
    : d.toLocaleDateString('fa-IR', { month: '2-digit', day: '2-digit' });
};

/** بیشینهٔ «گرد» محور عمودی + تعداد خطوط شبکه */
export function niceScale(max: number, ticks = 4): { max: number; step: number } {
  if (max <= 0) return { max: ticks, step: 1 };
  const raw = max / ticks;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const norm = raw / mag;
  const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10) * mag;
  return { max: step * ticks, step };
}

export interface Pt { x: number; y: number }

/** منحنی نرم (Catmull-Rom → Bézier) با جلوگیری از فراتر رفتن از دامنه */
export function smoothPath(pts: Pt[], minY: number, maxY: number): string {
  if (!pts.length) return '';
  if (pts.length === 1) return `M${pts[0].x},${pts[0].y}`;
  const clamp = (y: number) => Math.min(Math.max(y, minY), maxY);
  let d = `M${pts[0].x.toFixed(1)},${pts[0].y.toFixed(1)}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    const t = 0.18;
    const c1 = { x: p1.x + (p2.x - p0.x) * t, y: clamp(p1.y + (p2.y - p0.y) * t) };
    const c2 = { x: p2.x - (p3.x - p1.x) * t, y: clamp(p2.y - (p3.y - p1.y) * t) };
    d += ` C${c1.x.toFixed(1)},${c1.y.toFixed(1)} ${c2.x.toFixed(1)},${c2.y.toFixed(1)} ${p2.x.toFixed(1)},${p2.y.toFixed(1)}`;
  }
  return d;
}

/** پالت یکپارچه با رنگ‌های برنامه */
export const PALETTE = {
  primary: '#2563eb', sky: '#0ea5e9', emerald: '#10b981', amber: '#f59e0b',
  rose: '#f43f5e', purple: '#8b5cf6', gray: '#94a3b8', orange: '#fb923c'
};
