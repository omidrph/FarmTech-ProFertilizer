// frontend/src/utils/chemFormula.ts
// تحلیلگر فرمول شیمیایی برای «حالت پیشرفتهٔ» ساخت کود
// ------------------------------------------------------------
// ورودی: هر فرمولی مثل KNO3 ، Ca(NO3)2·4H2O ، (NH4)2SO4 ، P2O5 ، K2O ، 5Ca(NO3)2·NH4NO3·10H2O
// خروجی: جرم مولی + کسر جرمی هر «عنصر قابل‌استفادهٔ برنامه» (N-NO3, N-NH4, P, K, Ca, Mg, S, Na, Cl, Fe, Mn, Zn, B, Cu, Mo, Si)
// نیتروژن بر اساس گروه نیترات (NO3) یا آمونیوم (NH4) جدا می‌شود؛ بقیه (مثل اوره) «نیتروژن سایر» است.

export const ATOMIC_WEIGHTS: Record<string, number> = {
  H: 1.008, Li: 6.94, Be: 9.012, B: 10.811, C: 12.011, N: 14.007, O: 15.999, F: 18.998, Na: 22.99, Mg: 24.305,
  Al: 26.982, Si: 28.086, P: 30.974, S: 32.06, Cl: 35.45, K: 39.098, Ca: 40.078, Ti: 47.867, V: 50.942, Cr: 51.996,
  Mn: 54.938, Fe: 55.845, Co: 58.933, Ni: 58.693, Cu: 63.546, Zn: 65.38, Ga: 69.723, As: 74.922, Se: 78.971, Br: 79.904,
  Rb: 85.468, Sr: 87.62, Mo: 95.95, Ag: 107.868, Cd: 112.414, Sn: 118.71, I: 126.904, Ba: 137.327, W: 183.84,
  Pb: 207.2, Hg: 200.59, Ce: 140.116, La: 138.905, Zr: 91.224, Ru: 101.07
};

/** عنصرهایی که برنامه در محاسبات دنبال می‌کند (کلید برنامه ← نماد شیمیایی) */
export const TRACKED: Record<string, string> = {
  P: 'P', K: 'K', Ca: 'Ca', Mg: 'Mg', S: 'S', Na: 'Na', Cl: 'Cl', Fe: 'Fe', Mn: 'Mn', Zn: 'Zn', B: 'B', Cu: 'Cu', Mo: 'Mo', Si: 'Si'
};
/** عنصرهای سبک که به‌عنوان «ثبت‌نشده» نمایش داده نمی‌شوند */
const SILENT = new Set(['H', 'O', 'C']);

export class FormulaError extends Error {}

export interface ParsedFormula {
  formula: string;
  mass: number;
  counts: Record<string, number>;
  nitrate: number;   // تعداد اتم N در گروه NO3
  ammonium: number;  // تعداد اتم N در گروه NH4
}

const SUB = '₀₁₂₃₄₅₆₇₈₉';
const normalize = (s: string): string =>
  s
    .replace(/[₀-₉]/g, (c) => String(SUB.indexOf(c)))
    .replace(/[۰-۹]/g, (c) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(c)))
    .replace(/[٠-٩]/g, (c) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(c)))
    .replace(/[−–—]/g, '-')
    .replace(/\s+/g, '');

/** فرمول را به عنصرها می‌شکند؛ در صورت خطا پیام فارسی قابل‌فهم می‌دهد */
export function parseFormula(input: string): ParsedFormula {
  let src = normalize(input || '');
  if (!src) throw new FormulaError('فرمول را بنویسید');
  if (/(EDTA|DTPA|EDDHA|HEDTA|EDDS|IDHA)/i.test(src)) {
    throw new FormulaError('کلات‌ها فرمول عنصری ندارند؛ از دکمهٔ «کلات‌ها» استفاده کنید');
  }
  // حذف بار یونی انتهایی: NO3- ، NH4+ ، SO4^2- ، SO4(2-)  (رقم زیرنویس هرگز حذف نمی‌شود)
  src = src.replace(/(?:\^\d*|\(\d+)?[+-]+\)?$/, '');
  if (!src) throw new FormulaError('فرمول معتبر نیست');

  const parts = src.split(/[·•∙*.]/).filter((p) => p.length > 0);
  if (!parts.length) throw new FormulaError('فرمول معتبر نیست');

  const total: Record<string, number> = {};
  let nitrate = 0, ammonium = 0;
  const add = (k: string, v: number) => { total[k] = (total[k] || 0) + v; };

  for (const part of parts) {
    const m = part.match(/^(\d+(?:\.\d+)?)?(.*)$/);
    const coef = m && m[1] ? parseFloat(m[1]) : 1;
    const body = m ? m[2] : part;
    if (!body) throw new FormulaError('بعد از ضریب، فرمول لازم است');
    const g = parseGroup(body);
    for (const [k, v] of Object.entries(g.counts)) add(k, v * coef);
    nitrate += g.nitrate * coef;
    ammonium += g.ammonium * coef;
  }

  let mass = 0;
  for (const [el, n] of Object.entries(total)) mass += n * ATOMIC_WEIGHTS[el];
  if (!(mass > 0)) throw new FormulaError('جرم مولی صفر شد؛ فرمول را بررسی کنید');
  return { formula: input.trim(), mass, counts: total, nitrate, ammonium };
}

interface Group { counts: Record<string, number>; nitrate: number; ammonium: number }

function parseGroup(s: string): Group {
  let i = 0;
  const readNum = (): number | null => {
    const st = i;
    while (i < s.length && /\d/.test(s[i])) i++;
    return i > st ? parseInt(s.slice(st, i), 10) : null;
  };

  const parseSeq = (closing: string | null): Group => {
    const out: Group = { counts: {}, nitrate: 0, ammonium: 0 };
    const merge = (g: Group, mul: number) => {
      for (const [k, v] of Object.entries(g.counts)) out.counts[k] = (out.counts[k] || 0) + v * mul;
      out.nitrate += g.nitrate * mul;
      out.ammonium += g.ammonium * mul;
    };
    while (i < s.length) {
      const ch = s[i];
      if (ch === ')' || ch === ']' || ch === '}') {
        if (closing === null) throw new FormulaError('پرانتز بسته اضافه است');
        return out;
      }
      if (ch === '(' || ch === '[' || ch === '{') {
        i++;
        const inner = parseSeq(ch);
        if (i >= s.length) throw new FormulaError('پرانتز باز بسته نشده است');
        i++; // بستن
        merge(inner, readNum() ?? 1);
        continue;
      }
      const em = s.slice(i).match(/^[A-Z][a-z]?/);
      if (!em) {
        if (/[a-z]/.test(ch)) throw new FormulaError('نماد عناصر باید با حرف بزرگ شروع شود (مثل KNO3 یا Ca(NO3)2)');
        throw new FormulaError(`نویسهٔ نامعتبر «${ch}» در فرمول`);
      }
      let sym = em[0];
      // «Co» یا «Cu» دو حرفی؛ اگر دو حرفی ناشناخته بود، تک‌حرفی را امتحان کن (مثلاً «Nb» → N + b ✗)
      if (!(sym in ATOMIC_WEIGHTS) && sym.length === 2 && sym[0] in ATOMIC_WEIGHTS) sym = sym[0];
      if (!(sym in ATOMIC_WEIGHTS)) throw new FormulaError(`عنصر «${sym}» ناشناخته است`);
      i += sym.length;
      const n = readNum();

      // گروه‌های نیتروژن: NO3 (نیترات) و NH4 (آمونیوم)
      if (sym === 'N' && (n === null || n === 1)) {
        const rest = s.slice(i);
        if (/^O3(?!\d)/.test(rest)) {
          i += 2;
          out.counts.N = (out.counts.N || 0) + 1;
          out.counts.O = (out.counts.O || 0) + 3;
          out.nitrate += 1;
          continue;
        }
        if (/^H4(?!\d)/.test(rest)) {
          i += 2;
          out.counts.N = (out.counts.N || 0) + 1;
          out.counts.H = (out.counts.H || 0) + 4;
          out.ammonium += 1;
          continue;
        }
      }
      out.counts[sym] = (out.counts[sym] || 0) + (n ?? 1);
    }
    if (closing !== null) throw new FormulaError('پرانتز باز بسته نشده است');
    return out;
  };

  const g = parseSeq(null);
  return g;
}

export interface Analysis {
  mass: number;
  /** کسر جرمی (۰ تا ۱) هر عنصر برنامه */
  elements: Record<string, number>;
  /** عنصرهایی که برنامه دنبال نمی‌کند (مثل Co) با کسر جرمی */
  untracked: Record<string, number>;
  /** آیا نیتروژنِ «نه نیترات نه آمونیوم» (مثل اوره) وجود داشت؟ */
  genericN: boolean;
}

/** genericN: نیتروژن اوره/آمید به کدام ستون برود (پیش‌فرض آمونیومی؛ اوره در خاک/محلول به آمونیوم تبدیل می‌شود) */
export function analyse(p: ParsedFormula, genericTo: 'N-NH4' | 'N-NO3' = 'N-NH4'): Analysis {
  const frac = (el: string, n: number) => (n * ATOMIC_WEIGHTS[el]) / p.mass;
  const elements: Record<string, number> = {};
  const untracked: Record<string, number> = {};
  const nTotal = p.counts.N || 0;
  const generic = Math.max(nTotal - p.nitrate - p.ammonium, 0);
  if (p.nitrate) elements['N-NO3'] = (elements['N-NO3'] || 0) + frac('N', p.nitrate);
  if (p.ammonium) elements['N-NH4'] = (elements['N-NH4'] || 0) + frac('N', p.ammonium);
  if (generic) elements[genericTo] = (elements[genericTo] || 0) + frac('N', generic);
  for (const [el, n] of Object.entries(p.counts)) {
    if (el === 'N') continue;
    const key = Object.keys(TRACKED).find((k) => TRACKED[k] === el);
    if (key) elements[key] = (elements[key] || 0) + frac(el, n);
    else if (!SILENT.has(el)) untracked[el] = (untracked[el] || 0) + frac(el, n);
  }
  return { mass: p.mass, elements, untracked, genericN: generic > 0 };
}

/** کسر جرمی یک عنصر از یک فرمول (برای ساخت ضریب‌ها): ۰ اگر عنصر وجود نداشت */
export function factorOf(formula: string, elementKey: string, genericTo: 'N-NH4' | 'N-NO3' = 'N-NH4'): number {
  const a = analyse(parseFormula(formula), genericTo);
  return Math.round((a.elements[elementKey] || 0) * 10000) / 10000;
}
