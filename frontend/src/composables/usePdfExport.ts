// frontend/src/composables/usePdfExport.ts
// ============================================================
// خروجی PDF حرفه‌ای (طراحی مجدد از صفر)
// ------------------------------------------------------------
// سند HTML مستقل A4 / RTL داخل iframe مخفی ساخته و چاپ می‌شود (Save as PDF).
// - سربرگ برند + مشخصات گزارش + تاریخ
// - خلاصه: EC، هزینه، خطای ماکرو، خطای میکرو (سه‌رنگ: ۵٪ / ۱۰٪)
// - جدول کودها با ستون فرمول + مقدار در استوک و در ۱۰۰۰ لیتر + هزینه
// - کارت مخازن A/B/C، عناصر ماکرو/میکرو با نوار انحراف، تعادل یونی، هشدار رسوب
// - نام فایل از مشخصات گزارش + تاریخ (کوتاه)
// ============================================================
import { ref } from 'vue';
import type { OptimizationResponse } from '@/types';
import { computeGroupErrors, errorLevel, LEVEL_LABEL, type ErrorLevel } from '@/utils/errorLevels';

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

const COLORS: Record<ErrorLevel, { fg: string; bg: string; bar: string }> = {
    ok: { fg: '#047857', bg: '#ecfdf5', bar: '#10b981' },
    warn: { fg: '#b45309', bg: '#fffbeb', bar: '#f59e0b' },
    bad: { fg: '#be123c', bg: '#fff1f2', bar: '#f43f5e' }
};

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
    if (name.length > room) name = name.slice(0, room).trim();
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

    // ---------- سربرگ ----------
    function buildHeader(meta: PdfReportMeta): string {
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
<header class="hero">
  <div class="hero-brand">
    <div class="logo">سک</div>
    <div>
      <h1>گزارش فرمول تغذیه</h1>
      <p>سهند کود · سیستم هوشمند نسخه‌نویسی کود</p>
    </div>
  </div>
  <div class="hero-date"><span>تاریخ گزارش</span><strong>${esc(meta.date || todayFa())}</strong></div>
</header>
${rows.length ? `<section class="meta">${rows.map(([l, v]) => `<div><span>${esc(l)}</span><b>${esc(v)}</b></div>`).join('')}</section>` : ''}`;
    }

    // ---------- خلاصه ----------
    function buildKpis(payload: PdfExportPayload): string {
        const { result, targetValues } = payload;
        const g = computeGroupErrors(targetValues, result.concentrations || {});
        const errCard = (title: string, grp: typeof g.macro) => {
            if (!grp.count) return `<div class="kpi"><span>${title}</span><b class="muted">—</b><small>هدفی ثبت نشده</small></div>`;
            const c = COLORS[grp.level];
            return `<div class="kpi" style="border-color:${c.bar};background:${c.bg}">
  <span>${title}</span>
  <b style="color:${c.fg}">${fa(grp.meanAbs, 1)}٪</b>
  <small style="color:${c.fg}">${LEVEL_LABEL[grp.level]} · بیشترین ${esc(grp.worst)} ${fa(grp.maxAbs, 1)}٪</small>
</div>`;
        };
        return `
<section class="kpis">
  <div class="kpi"><span>EC نهایی</span><b>${fa(result.ec, 2)}</b><small>dS/m ${result.ec_status ? '· ' + esc(result.ec_status) : ''}</small></div>
  <div class="kpi"><span>هزینه کل</span><b>${money(result.cost_total)}</b><small>تومان</small></div>
  ${errCard('خطای ماکرو', g.macro)}
  ${errCard('خطای میکرو', g.micro)}
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

    // ---------- عناصر (ماکرو / میکرو) ----------
    function buildElements(payload: PdfExportPayload): string {
        const g = computeGroupErrors(payload.targetValues, payload.result.concentrations || {});
        if (!g.all.length) return '';
        const section = (title: string, grp: typeof g.macro) => {
            if (!grp.count) return '';
            const c = COLORS[grp.level];
            const rows = grp.rows
                .map((r) => {
                    const col = COLORS[r.level];
                    const w = Math.min(100, (r.actual / r.target) * 100);
                    const sign = r.deviationPct > 0 ? '+' : r.deviationPct < 0 ? '−' : '';
                    return `<tr>
  <td class="r"><b>${esc(r.element)}</b></td>
  <td class="m">${fa(r.target, 1)}</td>
  <td class="m">${fa(r.actual, 1)}</td>
  <td class="barcell"><div class="bar"><i style="width:${w.toFixed(0)}%;background:${col.bar}"></i></div></td>
  <td class="m" style="color:${col.fg}"><b>${sign}${fa(r.absPct, 1)}٪</b></td>
  <td><span class="pill" style="background:${col.bg};color:${col.fg}">${LEVEL_LABEL[r.level]}</span></td>
</tr>`;
                })
                .join('');
            return `
<div class="grp">
  <div class="grp-h" style="background:${c.bg};border-color:${c.bar}">
    <b>${title}</b>
    <span style="color:${c.fg}">میانگین خطا ${fa(grp.meanAbs, 1)}٪ · ${LEVEL_LABEL[grp.level]}</span>
  </div>
  <table class="tbl">
    <thead><tr><th class="r">عنصر</th><th>هدف (ppm)</th><th>تأمین‌شده</th><th>پوشش</th><th>انحراف</th><th>وضعیت</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>
</div>`;
        };
        return `
<section class="block">
  <h2>عناصر هدف در برابر عناصر تأمین‌شده</h2>
  ${section('عناصر ماکرو (پرمصرف)', g.macro)}
  ${section('عناصر میکرو (کم‌مصرف)', g.micro)}
  <p class="legend"><i style="background:${COLORS.ok.bar}"></i>تا ۵٪ قابل قبول <i style="background:${COLORS.warn.bar}"></i>۵ تا ۱۰٪ هشدار <i style="background:${COLORS.bad.bar}"></i>بالای ۱۰٪ عدم اعتماد</p>
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
@page{size:A4;margin:12mm 11mm 16mm}
*{box-sizing:border-box}
body{font-family:'Vazirmatn',Tahoma,sans-serif;margin:0;color:#1f2937;font-size:10.5px;line-height:1.75;direction:rtl;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.hero{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-radius:14px;color:#fff;background:linear-gradient(135deg,#047857 0%,#10b981 60%,#34d399 100%)}
.hero-brand{display:flex;align-items:center;gap:12px}
.logo{width:42px;height:42px;border-radius:12px;background:rgba(255,255,255,.2);border:1.5px solid rgba(255,255,255,.55);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.hero h1{margin:0;font-size:17px}.hero p{margin:0;font-size:10px;opacity:.9}
.hero-date{text-align:left}.hero-date span{display:block;font-size:9.5px;opacity:.85}.hero-date strong{font-size:13px}
.meta{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0 4px}
.meta div{background:#f8fafc;border:1px solid #e5e7eb;border-radius:9px;padding:5px 9px}
.meta span{display:block;font-size:9px;color:#6b7280}.meta b{font-size:11px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0 6px}
.kpi{border:1.5px solid #e5e7eb;border-radius:12px;padding:8px 11px;background:#fff;break-inside:avoid}
.kpi span{display:block;font-size:9.5px;color:#6b7280}.kpi b{display:block;font-size:19px;line-height:1.3}.kpi small{font-size:9px;color:#6b7280}.muted{color:#9ca3af}
.block{margin-top:13px}.avoid{break-inside:avoid}
h2{font-size:12.5px;margin:0 0 7px;padding-right:9px;border-right:4px solid #10b981;color:#064e3b}
.tbl{width:100%;border-collapse:collapse;font-size:10px}
.tbl th{background:#064e3b;color:#fff;padding:6px 6px;font-weight:700;text-align:center;font-size:9.5px}
.tbl th:first-child{border-radius:0 8px 0 0}.tbl th:last-child{border-radius:8px 0 0 0}
.tbl td{padding:5px 6px;text-align:center;border-bottom:1px solid #eef2f7}
.tbl tbody tr:nth-child(even){background:#f8fafc}
.tbl tr{break-inside:avoid}
.tbl tfoot td{background:#ecfdf5;border-top:2px solid #10b981;font-size:11px}
.r{text-align:right!important}.n{color:#9ca3af;width:22px}.m{font-variant-numeric:tabular-nums;white-space:nowrap}.dim{color:#6b7280}
.ltr{direction:ltr}.f{font-family:'Times New Roman',serif;font-size:10.5px;color:#334155}
.tag{font-style:normal;font-size:8.5px;background:#fef3c7;color:#92400e;border-radius:5px;padding:0 5px;margin-right:4px}
.tag-ph{background:#d1fae5;color:#065f46}
.tank{display:inline-block;font-size:9px;border-radius:6px;padding:0 7px;background:#f3f4f6;color:#374151}
.t-A{background:#dbeafe;color:#1d4ed8}.t-B{background:#ede9fe;color:#6d28d9}.t-C{background:#fef3c7;color:#b45309}
.tanks{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.tankcard{border:1.5px solid #e5e7eb;border-radius:12px;padding:8px 10px;break-inside:avoid}
.tankcard h3{margin:0 0 5px;font-size:10.5px}
.tankcard.t-A{border-color:#93c5fd;background:#eff6ff}.tankcard.t-B{border-color:#c4b5fd;background:#f5f3ff}.tankcard.t-C{border-color:#fcd34d;background:#fffbeb}
.tankcard ul{list-style:none;margin:0;padding:0}.tankcard li{display:flex;justify-content:space-between;gap:6px;font-size:9.5px;border-bottom:1px dashed #d1d5db;padding:2px 0}
.tankcard em{font-style:normal;color:#374151;font-weight:700;white-space:nowrap}
.grp{margin-bottom:9px}.grp-h{display:flex;justify-content:space-between;align-items:center;border:1px solid;border-radius:9px;padding:4px 10px;margin-bottom:5px;font-size:10.5px}
.barcell{width:26%}.bar{height:7px;background:#e5e7eb;border-radius:6px;overflow:hidden}.bar i{display:block;height:100%;border-radius:6px}
.pill{display:inline-block;font-size:9px;border-radius:999px;padding:0 8px}
.legend{font-size:9px;color:#6b7280;margin:4px 0 0}.legend i{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 8px 0 3px;vertical-align:middle}
.ion-bar{display:flex;height:12px;border-radius:7px;overflow:hidden;background:#e5e7eb}.ion-bar .cat,.ion i.cat{background:#3b82f6}.ion-bar .ani,.ion i.ani{background:#ef4444}
.ion-l{display:flex;gap:18px;margin-top:6px;font-size:10px}.ion-l i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-left:5px}
.alert{border:1px solid #e5e7eb;border-right:4px solid;border-radius:9px;padding:6px 10px;margin-bottom:6px;break-inside:avoid;background:#fff}
.alert p{margin:2px 0;font-size:9.8px;color:#374151}.alert ul{margin:3px 0 0;padding-right:16px;font-size:9.8px}
.empty{color:#6b7280}
.foot{position:fixed;bottom:0;left:0;right:0;display:flex;justify-content:space-between;font-size:8.5px;color:#9ca3af;border-top:1px solid #e5e7eb;padding-top:4px}
.note{margin-top:12px;font-size:9px;color:#6b7280;line-height:1.8}
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
<div class="foot"><span>سهند کود — سیستم هوشمند نسخه‌نویسی کود</span><span>${esc(meta.date || todayFa())}</span></div>
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
