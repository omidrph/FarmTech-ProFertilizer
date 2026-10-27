// frontend/src/composables/usePdfExport.ts
// ============================================================
// خروجی PDF حرفه‌ای (طراحی مجدد از صفر)
// ------------------------------------------------------------
// سند HTML مستقل A4 / RTL داخل iframe مخفی ساخته و چاپ می‌شود (Save as PDF).
// - سربرگ با لوگوی برنامه + مشخصات گزارش + تاریخ (تم سفید/بنفش/خاکستری با لهجهٔ آبی)
// - خلاصه: EC، هزینه، ماکرو و میکرو (حلقه‌ای، دقیقاً مثل پوشش عناصر)
// - جدول کودها با ستون فرمول + مقدار در استوک و در ۱۰۰۰ لیتر + هزینه
// - کارت مخازن A/B/C، عناصر ماکرو/میکرو با نمودار دایره‌ای، تعادل یونی، هشدار رسوب
// - نام فایل از مشخصات گزارش + تاریخ (کوتاه)
// ============================================================
import { ref } from 'vue';
import type { OptimizationResponse } from '@/types';
import { computeElementErrors, computeGroupErrors, errorLevel, LEVEL_LABEL, type ErrorLevel } from '@/utils/errorLevels';

export interface PdfReportMeta {
    greenhouseName?: string;
    reportName?: string;
    plantName?: string;
    season?: string;
    date?: string;
    tankVolume?: number;
    stockVolume?: number;
    injectionRatio?: number;
}

export interface PdfExportPayload {
    result: OptimizationResponse;
    fertilizers: any[];
    targetValues: Record<string, number>;
    meta?: PdfReportMeta;
}

// وضعیت خطا (سه‌رنگ) فقط برای نشانگرها؛ تم کلی گزارش بنفش/خاکستری/آبی است
const COLORS: Record<ErrorLevel, { fg: string; bg: string; bar: string }> = {
    ok: { fg: '#059669', bg: '#f0fdf8', bar: '#10b981' },
    warn: { fg: '#b45309', bg: '#fffbeb', bar: '#f59e0b' },
    bad: { fg: '#be123c', bg: '#fff1f2', bar: '#f43f5e' }
};
const PURPLE = '#6d28d9';
const BLUE = '#2563eb';

const toLatin = (s: string): string =>
    s.replace(/[۰-۹]/g, (d) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d))).replace(/[٠-٩]/g, (d) => String('٠١٢٣٤٥٦٧٨٩'.indexOf(d)));

const todayFa = (): string => {
    try {
        return new Date().toLocaleDateString('fa-IR');
    } catch {
        return new Date().toISOString().slice(0, 10);
    }
};

/**
 * نام فایل PDF: «سهند کود - [گلخانه] - گزارش - محصول - ۱۴۰۵-۰۸-۰۵»
 * هر بخش حداکثر ۱۸ نویسه و کل نام حداکثر ~۶۰ نویسه؛ تاریخ همیشه هست.
 */
export function buildPdfFileName(meta: PdfReportMeta = {}): string {
    const clean = (v?: string, max = 18) =>
        (v || '')
            .replace(/[\\/:*?"<>|]+/g, ' ')
            .replace(/\s+/g, ' ')
            .trim()
            .slice(0, max)
            .trim();
    const dateRaw = (meta.date || todayFa()).trim();
    const date = toLatin(dateRaw).replace(/[^\d]+/g, '-').replace(/^-|-$/g, '') || toLatin(todayFa()).replace(/[^\d]+/g, '-');
    const parts = [clean(meta.greenhouseName), clean(meta.reportName, 22), clean(meta.plantName)].filter(Boolean);
    let name = ['سهند کود', ...parts].join(' - ');
    const room = 60 - date.length - 3;
    if (name.length > room) name = name.slice(0, room).replace(/[\s-]+$/, '');
    return `${name} - ${date}`;
}

export function usePdfExport() {
    const isExporting = ref(false);

    const esc = (value: unknown): string =>
        value === null || value === undefined
            ? ''
            : String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

    const fa = (value: unknown, digits = 2): string => {
        const n = Number(value);
        return isFinite(n) ? n.toLocaleString('fa-IR', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : '—';
    };
    const money = (value: unknown): string => {
        const n = Number(value);
        return isFinite(n) ? Math.round(n).toLocaleString('fa-IR') : '۰';
    };

    function amountText(grams: number, fert: { form?: string; densityGMl?: number } | null): string {
        if (fert?.form === 'liquid' && Number(fert.densityGMl) > 0) {
            const ml = grams / Number(fert.densityGMl);
            return ml >= 1000 ? `${fa(ml / 1000, 2)} لیتر` : `${fa(ml, 1)} میلی‌لیتر`;
        }
        return grams >= 1000 ? `${fa(grams / 1000, 3)} کیلوگرم` : `${fa(grams, 1)} گرم`;
    }

    function buildTankMap(result: OptimizationResponse, fertilizers: any[]): Record<string, string> {
        const map: Record<string, string> = {};
        const data: any = result.reservoir_data;
        if (!data) return map;
        (['A', 'B', 'C'] as const).forEach((tank) => {
            const list = data[tank];
            if (!Array.isArray(list)) return;
            for (const item of list) {
                if (item?.fertilizer_id) map[item.fertilizer_id] = tank;
                else if (item?.name) {
                    const f = fertilizers.find((x) => x.name === item.name);
                    if (f) map[f.id] = tank;
                }
            }
        });
        return map;
    }

    // ---------- حلقهٔ دایره‌ای (هم‌شکل پوشش عناصر در برنامه) ----------
    function ring(actual: number, target: number, level: ErrorLevel, size = 54): string {
        const C1 = 2 * Math.PI * 18;
        const C2 = 2 * Math.PI * 22;
        const ratio = target > 0 ? actual / target : 0;
        const inner = C1 * (1 - Math.min(ratio, 1));
        const outer = ratio > 1 ? C2 * (1 - Math.min((ratio - 1) / 0.5, 1)) : 0;
        const col = COLORS[level].bar;
        return `<svg width="${size}" height="${size}" viewBox="0 0 48 48">
  <circle cx="24" cy="24" r="18" fill="none" stroke="#e5e7eb" stroke-width="4"/>
  <circle cx="24" cy="24" r="18" fill="none" stroke="${col}" stroke-width="4" stroke-linecap="round" stroke-dasharray="${C1.toFixed(2)}" stroke-dashoffset="${inner.toFixed(2)}" transform="rotate(-90 24 24)"/>
  ${ratio > 1 ? `<circle cx="24" cy="24" r="22" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" stroke-dasharray="${C2.toFixed(2)}" stroke-dashoffset="${outer.toFixed(2)}" transform="rotate(-90 24 24)"/>` : ''}
  <text x="24" y="27" text-anchor="middle" font-size="10" font-weight="700" fill="${COLORS[level].fg}">${fa(ratio * 100, 0)}٪</text>
</svg>`;
    }

    // ---------- سربرگ ----------
    function buildHeader(meta: PdfReportMeta): string {
        const origin = typeof window !== 'undefined' ? window.location.origin : '';
        const rows = [
            meta.greenhouseName ? ['گلخانه', meta.greenhouseName] : null,
            meta.reportName ? ['گزارش', meta.reportName] : null,
            meta.plantName ? ['محصول', meta.plantName] : null,
            meta.season ? ['فصل', meta.season] : null,
            meta.tankVolume ? ['حجم مخزن اصلی', `${fa(meta.tankVolume, 0)} لیتر`] : null,
            meta.stockVolume ? ['حجم سطل استوک', `${fa(meta.stockVolume, 0)} لیتر`] : null,
            meta.injectionRatio ? ['نسبت تزریق', `۱ به ${fa(meta.injectionRatio, 0)}`] : null
        ].filter(Boolean) as string[][];
        return `
<header class="top">
  <div class="brand">
    <img src="${origin}/Logo.webp" alt="" onerror="this.style.display='none'" />
    <div><h1>گزارش فرمول تغذیه</h1><p>سهند کود · سیستم هوشمند نسخه‌نویسی کود</p></div>
  </div>
  <div class="date"><span>تاریخ گزارش</span><b>${esc(meta.date || todayFa())}</b></div>
</header>
${rows.length ? `<section class="meta">${rows.map(([l, v]) => `<div><span>${esc(l)}</span><b>${esc(v)}</b></div>`).join('')}</section>` : ''}`;
    }

    // ---------- خلاصه ----------
    function buildKpis(payload: PdfExportPayload): string {
        const { result, targetValues } = payload;
        const g = computeGroupErrors(targetValues, result.concentrations || {});
        const cov = (title: string, grp: typeof g.macro) => {
            if (!grp.count) return `<div class="kpi"><span>${title}</span><b class="muted">—</b></div>`;
            const C = 2 * Math.PI * 18;
            const col = COLORS[grp.level];
            return `<div class="kpi kpi-ring">
  <svg width="50" height="50" viewBox="0 0 48 48">
    <circle cx="24" cy="24" r="18" fill="none" stroke="#e5e7eb" stroke-width="4"/>
    <circle cx="24" cy="24" r="18" fill="none" stroke="${col.bar}" stroke-width="4" stroke-linecap="round" stroke-dasharray="${C.toFixed(2)}" stroke-dashoffset="${(C * (1 - grp.coverage / 100)).toFixed(2)}" transform="rotate(-90 24 24)"/>
    ${grp.over > 0.5 ? `<circle cx="24" cy="24" r="22" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" stroke-dasharray="${(2 * Math.PI * 22).toFixed(2)}" stroke-dashoffset="${(2 * Math.PI * 22 * (1 - Math.min(grp.over / 50, 1))).toFixed(2)}" transform="rotate(-90 24 24)"/>` : ''}
  </svg>
  <div><span>${title}</span><b style="color:${col.fg}">${fa(grp.coverage, 1)}٪</b><small style="color:${col.fg}">${LEVEL_LABEL[grp.level]}</small></div>
</div>`;
        };
        return `
<section class="kpis">
  <div class="kpi"><span>EC نهایی</span><b>${fa(result.ec, 2)}</b><small>dS/m${result.ec_status ? ' · ' + esc(result.ec_status) : ''}</small></div>
  <div class="kpi"><span>هزینه کل</span><b>${money(result.cost_total)}</b><small>تومان</small></div>
  ${cov('ماکرو', g.macro)}
  ${cov('میکرو', g.micro)}
</section>`;
    }

    // ---------- جدول کودها ----------
    function buildFertilizerTable(payload: PdfExportPayload): string {
        const { result, fertilizers, meta } = payload;
        const tankMap = buildTankMap(result, fertilizers);
        const vol = Number(meta?.tankVolume) || 0;

        const rows = Object.entries(result.weights || {})
            .filter(([, w]) => typeof w === 'number' && w > 0)
            .sort((a, b) => (b[1] as number) - (a[1] as number));

        const adj: any = result.ph_adjustment;
        if (rows.length === 0 && !adj) {
            return '<section class="block"><h2>مقادیر کود</h2><p class="empty">موردی ثبت نشده است.</p></section>';
        }

        const line = (name: string, formula: string, tag: string, tank: string, grams: number, fert: any, cost: number, i: number) => {
            const per1000 = vol > 0 ? (grams / vol) * 1000 : 0;
            return `<tr>
  <td class="n">${fa(i, 0)}</td>
  <td class="r"><b>${esc(name)}</b>${tag}</td>
  <td class="ltr f">${esc(formula) || '—'}</td>
  <td><span class="tank t-${esc(tank)}">${tank === '—' ? '—' : 'مخزن ' + esc(tank)}</span></td>
  <td class="m">${amountText(grams, fert)}</td>
  <td class="m dim">${vol > 0 ? amountText(per1000, fert) : '—'}</td>
  <td class="m">${money(cost)}</td>
</tr>`;
        };

        let i = 0;
        const body = rows
            .map(([id, w]) => {
                const f = fertilizers.find((x) => x.id === id) || null;
                const tag = f?.isAcid ? ' <i class="tag">اسید</i>' : f?.isBase ? ' <i class="tag">باز</i>' : '';
                return line(f?.name || id, f?.formula || '', tag, tankMap[id] || '—', w as number, f, f ? ((w as number) / 1000) * (f.pricePerKg || 0) : 0, ++i);
            })
            .join('');

        let phLine = '';
        if (adj && Number(adj.dose_total_g) > 0) {
            const f = fertilizers.find((x) => String(x.id) === String(adj.fertilizer_id)) || null;
            const dens = Number(adj.chemical?.density_g_ml) || 0;
            const asFert = adj.dose_unit === 'ml' && dens > 0 ? { form: 'liquid', densityGMl: dens } : null;
            phLine = line(adj.chemical_name, f?.formula || '', ' <i class="tag tag-ph">تنظیم pH</i>', 'C', Number(adj.dose_total_g), asFert, Number(adj.cost) || 0, ++i);
        }

        return `
<section class="block">
  <h2>مقادیر کود برای ساخت استوک</h2>
  <table class="tbl">
    <thead><tr>
      <th>#</th><th class="r">نام کود</th><th>فرمول</th><th>مخزن</th>
      <th>مقدار در استوک</th><th>در ۱۰۰۰ لیتر محلول</th><th>هزینه (تومان)</th>
    </tr></thead>
    <tbody>${body}${phLine}</tbody>
    <tfoot><tr><td colspan="6" class="r">مجموع هزینه ترکیب</td><td class="m"><b>${money(result.cost_total)}</b></td></tr></tfoot>
  </table>
</section>`;
    }

    // ---------- مخازن ----------
    function buildTanks(payload: PdfExportPayload): string {
        const { result, fertilizers } = payload;
        const data: any = result.reservoir_data || {};
        const titles: Record<string, string> = { A: 'مخزن A · کلسیمی', B: 'مخزن B · اصلی', C: 'مخزن C · اسید' };
        const cards = (['A', 'B', 'C'] as const)
            .map((t) => {
                const list: any[] = Array.isArray(data[t]) ? data[t] : [];
                const extra = t === 'C' && (result.ph_adjustment as any)?.chemical_name ? [(result.ph_adjustment as any).chemical_name] : [];
                if (!list.length && !extra.length) return '';
                const items = list
                    .map((it) => {
                        const f = fertilizers.find((x) => String(x.id) === String(it.fertilizer_id));
                        return `<li><span>${esc(it.name)}</span><em>${amountText(Number(it.amount) || 0, f || null)}</em></li>`;
                    })
                    .concat(extra.map((n) => `<li><span>${esc(n)}</span><em>تنظیم pH (از تب PH)</em></li>`))
                    .join('');
                return `<div class="tankcard t-${t}"><h3>${titles[t]}</h3><ul>${items}</ul></div>`;
            })
            .join('');
        return cards ? `<section class="block"><h2>چیدمان مخازن استوک</h2><div class="tanks">${cards}</div></section>` : '';
    }

    // ---------- عناصر هدف: یک فهرست یکپارچه با حلقه‌های دایره‌ای ----------
    function buildElements(payload: PdfExportPayload): string {
        const rows = computeElementErrors(payload.targetValues, payload.result.concentrations || {});
        if (!rows.length) return '';
        const order: Record<ErrorLevel, number> = { bad: 0, warn: 1, ok: 2 };
        const cells = rows
            .sort((a, b) => (a.level !== b.level ? order[a.level] - order[b.level] : b.absPct - a.absPct))
            .map(
                (r) => `<div class="el">
  ${ring(r.actual, r.target, r.level, 52)}
  <div class="el-t"><b>${esc(r.element)}</b><small>${r.group === 'micro' ? 'میکرو' : 'ماکرو'}</small></div>
  <div class="el-v"><span>هدف ${fa(r.target, 1)}</span><span>فعلی ${fa(r.actual, 1)}</span></div>
</div>`
            )
            .join('');
        return `
<section class="block">
  <h2>پوشش عناصر هدف <small>ppm</small></h2>
  <div class="els">${cells}</div>
  <p class="legend"><i style="background:${COLORS.ok.bar}"></i>تا ۵٪ قابل قبول <i style="background:${COLORS.warn.bar}"></i>۵ تا ۱۰٪ هشدار <i style="background:${COLORS.bad.bar}"></i>بالای ۱۰٪ عدم اعتماد <i style="background:#f43f5e;border-radius:2px;height:3px;width:12px"></i>حلقهٔ بیرونی: بیش‌تأمین</p>
</section>`;
    }

    // ---------- تعادل یونی ----------
    function buildIonBalance(result: OptimizationResponse): string {
        const b: any = result.ion_balance;
        if (!b) return '';
        const cat = Number(b.cation) || 0;
        const ani = Number(b.anion) || 0;
        const tot = cat + ani || 1;
        const diff = Math.abs(cat - ani);
        const pct = Math.max(cat, ani) > 0 ? (diff / Math.max(cat, ani)) * 100 : 0;
        const lvl = errorLevel(pct);
        return `
<section class="block avoid">
  <h2>تعادل یونی</h2>
  <div class="ion">
    <div class="ion-bar"><i class="cat" style="width:${((cat / tot) * 100).toFixed(1)}%"></i><i class="ani" style="width:${((ani / tot) * 100).toFixed(1)}%"></i></div>
    <div class="ion-l">
      <span><i class="cat"></i>کاتیون <b>${fa(cat, 2)}</b> meq/L</span>
      <span><i class="ani"></i>آنیون <b>${fa(ani, 2)}</b> meq/L</span>
      <span style="color:${COLORS[lvl].fg}">اختلاف <b>${fa(diff, 2)}</b> (${fa(pct, 1)}٪) · ${LEVEL_LABEL[lvl]}</span>
    </div>
  </div>
</section>`;
    }

    // ---------- هشدارها ----------
    function buildAlerts(result: OptimizationResponse): string {
        const alerts = (result.precipitation_alerts || []).filter((a) => a.severity !== 'info');
        const warnings = (result.warnings || []).filter((w) => !/^خطر رسوب/.test(w));
        if (!alerts.length && !warnings.length) return '';
        const sev: Record<string, { c: string; l: string }> = { danger: { c: '#be123c', l: 'خطر' }, warn: { c: '#b45309', l: 'هشدار' }, info: { c: '#0369a1', l: 'نکته' } };
        const a = alerts
            .map(
                (x) => `<div class="alert" style="border-right-color:${sev[x.severity].c}">
  <b style="color:${sev[x.severity].c}">${sev[x.severity].l} · ${esc(x.title)}</b>
  <p>${esc(x.detail)}</p><p><u>راه‌حل:</u> ${esc(x.solution)}</p></div>`
            )
            .join('');
        const w = warnings.length ? `<div class="alert" style="border-right-color:#b45309"><b style="color:#b45309">سایر هشدارها</b><ul>${warnings.map((t) => `<li>${esc(t)}</li>`).join('')}</ul></div>` : '';
        return `<section class="block"><h2>هشدارها و ترکیبات رسوب‌زا</h2>${a}${w}</section>`;
    }

    // ---------- سند ----------
    function buildDocument(payload: PdfExportPayload, title: string): string {
        const meta = payload.meta || {};
        const origin = typeof window !== 'undefined' ? window.location.origin : '';
        return `<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8" /><title>${esc(title)}</title>
<style>
@font-face{font-family:'Vazirmatn';src:url('${origin}/fonts/Vazirmatn-Regular.woff2') format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'Vazirmatn';src:url('${origin}/fonts/Vazirmatn-Bold.woff2') format('woff2');font-weight:700;font-display:block}
@page{size:A4;margin:12mm 12mm 16mm}
*{box-sizing:border-box}
body{font-family:'Vazirmatn',Tahoma,sans-serif;margin:0;color:#1f2937;font-size:10.5px;line-height:1.75;direction:rtl;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.top{display:flex;justify-content:space-between;align-items:center;padding:0 0 10px;border-bottom:2px solid ${PURPLE}}
.brand{display:flex;align-items:center;gap:11px}
.brand img{width:46px;height:46px;object-fit:contain;border-radius:10px}
.brand h1{margin:0;font-size:18px;color:#2e1065}.brand p{margin:0;font-size:9.5px;color:#6b7280}
.date{text-align:left}.date span{display:block;font-size:9px;color:#6b7280}.date b{font-size:12.5px;color:#374151}
.meta{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:10px 0 2px;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden}
.meta div{padding:5px 10px;border-left:1px solid #eef0f4;border-bottom:1px solid #eef0f4;background:#fff}
.meta span{display:block;font-size:8.8px;color:#9ca3af}.meta b{font-size:10.8px;color:#1f2937}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0 4px}
.kpi{border:1px solid #e5e7eb;border-radius:12px;padding:8px 12px;background:#faf9ff;break-inside:avoid}
.kpi span{display:block;font-size:9.5px;color:#6b7280}.kpi b{display:block;font-size:18px;line-height:1.3;color:${PURPLE}}.kpi small{font-size:9px;color:#9ca3af}.muted{color:#9ca3af!important}
.kpi-ring{display:flex;align-items:center;gap:9px}
.block{margin-top:14px}.avoid{break-inside:avoid}
h2{font-size:12.5px;margin:0 0 8px;color:#2e1065;display:flex;align-items:center;gap:8px}
h2::before{content:'';width:4px;height:14px;border-radius:3px;background:${PURPLE}}
h2 small{font-size:9px;color:#9ca3af;font-weight:400}
.tbl{width:100%;border-collapse:collapse;font-size:10px}
.tbl th{background:#f5f3ff;color:#4c1d95;padding:6px;font-weight:700;text-align:center;font-size:9.5px;border-bottom:1.5px solid #ddd6fe}
.tbl td{padding:5px 6px;text-align:center;border-bottom:1px solid #f1f2f6}
.tbl tr{break-inside:avoid}
.tbl tfoot td{background:#faf9ff;border-top:1.5px solid #ddd6fe;font-size:11px;color:#4c1d95}
.r{text-align:right!important}.n{color:#c4c7d0;width:22px}.m{font-variant-numeric:tabular-nums;white-space:nowrap}.dim{color:#9ca3af}
.ltr{direction:ltr}.f{font-family:'Times New Roman',serif;font-size:10.5px;color:#475569}
.tag{font-style:normal;font-size:8.5px;background:#ede9fe;color:#5b21b6;border-radius:5px;padding:0 5px;margin-right:4px}
.tag-ph{background:#dbeafe;color:#1d4ed8}
.tank{display:inline-block;font-size:9px;border-radius:6px;padding:0 7px;background:#f3f4f6;color:#4b5563}
.t-A{background:#dbeafe;color:#1d4ed8}.t-B{background:#ede9fe;color:#6d28d9}.t-C{background:#e5e7eb;color:#374151}
.tanks{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.tankcard{border:1px solid #e5e7eb;border-top:3px solid #9ca3af;border-radius:10px;padding:8px 10px;break-inside:avoid;background:#fff}
.tankcard h3{margin:0 0 5px;font-size:10.5px;color:#374151}
.tankcard.t-A{border-top-color:#3b82f6}.tankcard.t-B{border-top-color:#8b5cf6}.tankcard.t-C{border-top-color:#9ca3af}
.tankcard ul{list-style:none;margin:0;padding:0}.tankcard li{display:flex;justify-content:space-between;gap:6px;font-size:9.5px;border-bottom:1px dashed #e5e7eb;padding:2px 0}
.tankcard em{font-style:normal;color:#374151;font-weight:700;white-space:nowrap}
.grp{margin-bottom:10px}.grp-h{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e5e7eb;padding:0 2px 3px;margin-bottom:7px;font-size:10.5px}
.grp-h b{color:#4c1d95}
.els{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.el{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:8px;align-items:center;border:1px solid #eef0f4;border-radius:11px;padding:6px 8px;background:#fff;break-inside:avoid}
.el svg{grid-row:1 / span 2}
.el-t b{display:block;font-size:11px;color:#1f2937;line-height:1.3}.el-t small{font-size:8.5px;color:#7c7f8a;background:#f3f4f6;border-radius:5px;padding:0 6px}
.el-v{display:flex;flex-direction:column;font-size:8.6px;color:#9ca3af;line-height:1.5;font-variant-numeric:tabular-nums}
.legend{font-size:8.8px;color:#9ca3af;margin:4px 0 0}.legend i{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 8px 0 3px;vertical-align:middle}
.ion-bar{display:flex;height:11px;border-radius:7px;overflow:hidden;background:#e5e7eb}.ion-bar .cat,.ion i.cat{background:#3b82f6}.ion-bar .ani,.ion i.ani{background:#ef4444}
.ion-l{display:flex;gap:18px;margin-top:6px;font-size:10px}.ion-l i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-left:5px}
.alert{border:1px solid #e5e7eb;border-right:3px solid;border-radius:9px;padding:6px 10px;margin-bottom:6px;break-inside:avoid;background:#fff}
.alert p{margin:2px 0;font-size:9.8px;color:#4b5563}.alert ul{margin:3px 0 0;padding-right:16px;font-size:9.8px}
.empty{color:#6b7280}
.foot{position:fixed;bottom:0;left:0;right:0;display:flex;justify-content:space-between;font-size:8.5px;color:#9ca3af;border-top:1px solid #e5e7eb;padding-top:4px}
.note{margin-top:12px;font-size:9px;color:#9ca3af;line-height:1.8}
</style></head>
<body>
${buildHeader(meta)}
${buildKpis(payload)}
${buildFertilizerTable(payload)}
${buildTanks(payload)}
${buildElements(payload)}
${buildIonBalance(payload.result)}
${buildAlerts(payload.result)}
<p class="note">مقادیر بر پایهٔ ترکیب کودهای انتخابی و آنالیز آب واردشده محاسبه شده‌اند؛ پیش از مصرف، EC و pH محلول نهایی را با دستگاه اندازه‌گیری و در صورت نیاز تنظیم کنید.</p>
<div class="foot"><span>سهند کود · سیستم هوشمند نسخه‌نویسی کود</span><span>${esc(meta.date || todayFa())}</span></div>
</body></html>`;
    }

    async function exportOptimizationPdf(payload: PdfExportPayload): Promise<void> {
        if (!payload?.result) throw new Error('نتیجه‌ای برای خروجی گرفتن وجود ندارد');
        isExporting.value = true;
        const fileName = buildPdfFileName(payload.meta);
        const prevTitle = document.title;

        try {
            const html = buildDocument(payload, fileName);
            document.getElementById('farmtech-pdf-frame')?.remove();

            const frame = document.createElement('iframe');
            frame.id = 'farmtech-pdf-frame';
            frame.setAttribute('aria-hidden', 'true');
            Object.assign(frame.style, { position: 'fixed', right: '-10000px', bottom: '0', width: '210mm', height: '297mm', border: '0' });
            document.body.appendChild(frame);

            await new Promise<void>((resolve, reject) => {
                const doc = frame.contentDocument || frame.contentWindow?.document;
                if (!doc) return reject(new Error('امکان ساخت سند چاپ وجود ندارد'));
                doc.open();
                doc.write(html);
                doc.close();

                let started = false;
                const start = () => {
                    if (started) return;
                    started = true;
                    const win = frame.contentWindow;
                    if (!win) return reject(new Error('امکان باز کردن پنجره چاپ وجود ندارد'));
                    const fonts = (doc as any).fonts;
                    (fonts?.ready ? fonts.ready : Promise.resolve()).catch(() => undefined).then(() => {
                        setTimeout(() => {
                            // مرورگرها نام پیش‌فرض فایل را از عنوان صفحه می‌گیرند؛ موقتاً عنوان را روی نام فایل می‌گذاریم
                            document.title = fileName;
                            const restore = () => { document.title = prevTitle; };
                            win.addEventListener('afterprint', restore, { once: true });
                            setTimeout(restore, 60000);
                            win.focus();
                            win.print();
                            resolve();
                        }, 150);
                    });
                };
                if (doc.readyState === 'complete') start();
                else {
                    frame.onload = start;
                    setTimeout(start, 800);
                }
            });

            setTimeout(() => document.getElementById('farmtech-pdf-frame')?.remove(), 65000);
        } finally {
            isExporting.value = false;
        }
    }

    return { isExporting, exportOptimizationPdf };
}
