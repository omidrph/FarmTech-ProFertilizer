// frontend/src/composables/usePdfExport.ts
// ============================================================
// خروجی PDF حرفه‌ای از نتیجه بهینه‌سازی
// ------------------------------------------------------------
// جایگزین کامل خروجی CSV قدیمی.
// روش کار: یک سند HTML مستقل و کاملاً استایل‌دهی‌شده (A4 / RTL)
// داخل یک iframe مخفی ساخته می‌شود و سپس دیالوگ چاپ مرورگر باز
// می‌شود؛ کاربر می‌تواند «Save as PDF» را انتخاب کند.
// مزیت نسبت به کتابخانه‌های PDF: پشتیبانی کامل از فارسی/RTL،
// فونت Vazirmatn پروژه، بدون افزودن هیچ dependency جدید.
// ============================================================
import { ref } from 'vue';
import type { OptimizationResponse } from '@/types';

export interface PdfReportMeta {
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

export function usePdfExport() {
    const isExporting = ref(false);

    // ============================================================
    // ابزارهای کمکی
    // ============================================================
    const esc = (value: unknown): string => {
        if (value === null || value === undefined) return '';
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    };

    const num = (value: unknown, digits = 2): string => {
        const parsed = Number(value);
        if (!isFinite(parsed)) return '—';
        return parsed.toFixed(digits);
    };

    const money = (value: unknown): string => {
        const parsed = Number(value);
        if (!isFinite(parsed)) return '۰';
        return Math.round(parsed).toLocaleString('fa-IR');
    };

    const todayFa = (): string => {
        try {
            return new Date().toLocaleDateString('fa-IR');
        } catch {
            return new Date().toISOString().slice(0, 10);
        }
    };

    // ============================================================
    // بخش‌های گزارش
    // ============================================================

    function buildHeader(meta: PdfReportMeta): string {
        const rows = [
            meta.reportName ? ['عنوان گزارش', meta.reportName] : null,
            meta.plantName ? ['محصول', meta.plantName] : null,
            meta.season ? ['فصل / مرحله رشد', meta.season] : null,
            meta.tankVolume ? ['حجم مخزن اصلی', `${meta.tankVolume} لیتر`] : null,
            meta.stockVolume ? ['حجم سطل استوک', `${meta.stockVolume} لیتر`] : null,
            meta.injectionRatio ? ['نسبت تزریق', `۱ : ${meta.injectionRatio}`] : null
        ].filter(Boolean) as string[][];

        const cells = rows
            .map(
                ([label, value]) => `
                <div class="meta-item">
                    <span class="meta-label">${esc(label)}</span>
                    <span class="meta-value">${esc(value)}</span>
                </div>`
            )
            .join('');

        return `
        <header class="doc-header">
            <div class="brand">
                <div class="brand-mark">FT</div>
                <div class="brand-text">
                    <h1>گزارش فرمول تغذیه</h1>
                    <p>FarmTech &mdash; ProFertilizer</p>
                </div>
            </div>
            <div class="issued">
                <span>تاریخ صدور</span>
                <strong>${esc(meta.date || todayFa())}</strong>
            </div>
        </header>
        ${cells ? `<section class="meta-grid">${cells}</section>` : ''}`;
    }

    function buildKpis(result: OptimizationResponse): string {
        const accuracy = Math.max(0, 100 - (Number(result.residual_error) || 0) * 100);
        const items = [
            { label: 'EC نهایی', value: num(result.ec, 2), unit: 'dS/m', note: result.ec_status || '' },
            { label: 'pH تخمینی', value: num(result.ph, 2), unit: '', note: result.ph_status || '' },
            { label: 'دقت رسیدن به هدف', value: num(accuracy, 1), unit: '٪', note: result.is_converged ? 'همگرا' : 'همگرا نشد' },
            { label: 'هزینه کل', value: money(result.cost_total), unit: 'تومان', note: '' }
        ];

        return `
        <section class="kpi-row">
            ${items
                .map(
                    (item) => `
                <div class="kpi">
                    <span class="kpi-label">${esc(item.label)}</span>
                    <span class="kpi-value">${esc(item.value)}<em>${esc(item.unit)}</em></span>
                    ${item.note ? `<span class="kpi-note">${esc(item.note)}</span>` : ''}
                </div>`
                )
                .join('')}
        </section>`;
    }

    function buildFertilizerTable(payload: PdfExportPayload): string {
        const { result, fertilizers } = payload;
        const weights = result.weights || {};
        const tankMap = buildTankMap(result, fertilizers);

        const rows = Object.entries(weights)
            .filter(([, weight]) => typeof weight === 'number' && weight > 0)
            .sort((a, b) => (b[1] as number) - (a[1] as number));

        if (rows.length === 0) {
            return '<section class="block"><h2>مقادیر کود</h2><p class="empty">موردی ثبت نشده است.</p></section>';
        }

        const body = rows
            .map(([id, weight]) => {
                const fert = fertilizers.find((f) => f.id === id);
                const cost = fert ? ((weight as number) / 1000) * (fert.pricePerKg || 0) : 0;
                const tank = tankMap[id] || '—';
                return `
                <tr>
                    <td class="right">${esc(fert?.name || id)}${fert?.isAcid ? ' <span class="tag tag-acid">اسید</span>' : ''}</td>
                    <td><span class="tank tank-${esc(tank)}">${tank === '—' ? '—' : `مخزن ${esc(tank)}`}</span></td>
                    <td class="mono">${num(weight, 1)}</td>
                    <td class="mono">${money(cost)}</td>
                </tr>`;
            })
            .join('');

        return `
        <section class="block">
            <h2>مقادیر کود برای ساخت استوک</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th class="right">نام کود</th>
                        <th>مخزن</th>
                        <th>وزن (گرم)</th>
                        <th>هزینه (تومان)</th>
                    </tr>
                </thead>
                <tbody>${body}</tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="right">مجموع هزینه</td>
                        <td class="mono strong">${money(result.cost_total)}</td>
                    </tr>
                </tfoot>
            </table>
        </section>`;
    }

    function buildElementsTable(payload: PdfExportPayload): string {
        const { result, targetValues } = payload;
        const entries = Object.entries(targetValues || {}).filter(([, target]) => Number(target) > 0);

        if (entries.length === 0) return '';

        const body = entries
            .map(([element, target]) => {
                const actual = Number(result.concentrations?.[element] || 0);
                const deviation = ((actual - Number(target)) / Number(target)) * 100;
                const state = Math.abs(deviation) <= 3 ? 'ok' : Math.abs(deviation) <= 10 ? 'warn' : 'bad';
                const sign = deviation > 0 ? '+' : '';
                return `
                <tr>
                    <td class="right strong">${esc(element)}</td>
                    <td class="mono">${num(target, 1)}</td>
                    <td class="mono">${num(actual, 1)}</td>
                    <td class="mono state-${state}">${sign}${num(deviation, 1)}٪</td>
                </tr>`;
            })
            .join('');

        return `
        <section class="block">
            <h2>عناصر هدف در برابر عناصر تأمین‌شده <small>(واحد: ppm)</small></h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th class="right">عنصر</th>
                        <th>هدف</th>
                        <th>تأمین‌شده</th>
                        <th>انحراف</th>
                    </tr>
                </thead>
                <tbody>${body}</tbody>
            </table>
        </section>`;
    }

    function buildIonBalance(result: OptimizationResponse): string {
        const balance = result.ion_balance;
        if (!balance) return '';
        const diff = Math.abs((balance.cation || 0) - (balance.anion || 0));
        return `
        <section class="block">
            <h2>تعادل یونی</h2>
            <div class="inline-cards">
                <div class="inline-card"><span>کاتیون</span><strong>${num(balance.cation, 2)} meq/L</strong></div>
                <div class="inline-card"><span>آنیون</span><strong>${num(balance.anion, 2)} meq/L</strong></div>
                <div class="inline-card"><span>اختلاف</span><strong>${num(diff, 2)} meq/L</strong></div>
                <div class="inline-card ${balance.isBalanced ? 'ok' : 'bad'}">
                    <span>وضعیت</span><strong>${balance.isBalanced ? 'متعادل' : 'نامتعادل'}</strong>
                </div>
            </div>
        </section>`;
    }

    function buildNotes(result: OptimizationResponse): string {
        const warnings = result.warnings || [];
        const suggestions = result.suggestions || [];
        if (warnings.length === 0 && suggestions.length === 0) return '';

        const list = (items: string[]) => items.map((item) => `<li>${esc(item)}</li>`).join('');

        return `
        <section class="block avoid-break">
            <h2>نکات و توصیه‌ها</h2>
            ${warnings.length ? `<div class="note note-warn"><h3>هشدارها</h3><ul>${list(warnings)}</ul></div>` : ''}
            ${suggestions.length ? `<div class="note note-info"><h3>پیشنهادها</h3><ul>${list(suggestions)}</ul></div>` : ''}
        </section>`;
    }

    function buildInstructions(result: OptimizationResponse): string {
        const instructions = result.stock_instructions || [];
        if (instructions.length === 0) return '';

        const items = instructions
            .map(
                (inst: any, index: number) => `
            <li>
                <span class="step-index">${index + 1}</span>
                <div>
                    <strong>${esc(inst.fertilizer_name)}</strong>
                    <span class="tank tank-${esc(inst.reservoir)}">مخزن ${esc(inst.reservoir)}</span>
                    <span class="step-weight">${num(inst.weight_grams, 0)} گرم در ${esc(inst.recommended_bucket_liters)} لیتر آب</span>
                    ${inst.warning ? `<em class="step-warn">${esc(inst.warning)}</em>` : ''}
                </div>
            </li>`
            )
            .join('');

        return `
        <section class="block avoid-break">
            <h2>ترتیب ساخت استوک</h2>
            <ol class="steps">${items}</ol>
        </section>`;
    }

    function buildTankMap(result: OptimizationResponse, fertilizers: any[]): Record<string, string> {
        const map: Record<string, string> = {};
        const data: any = result.reservoir_data;
        if (!data) return map;

        (['A', 'B', 'C'] as const).forEach((tank) => {
            const list = data[tank];
            if (!Array.isArray(list)) return;
            for (const item of list) {
                if (item?.fertilizer_id) {
                    map[item.fertilizer_id] = tank;
                } else if (item?.name) {
                    const fert = fertilizers.find((f) => f.name === item.name);
                    if (fert) map[fert.id] = tank;
                }
            }
        });
        return map;
    }

    // ============================================================
    // سند نهایی
    // ============================================================
    function buildDocument(payload: PdfExportPayload): string {
        const meta = payload.meta || {};
        const origin = typeof window !== 'undefined' ? window.location.origin : '';

        return `<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8" />
<title>گزارش فرمول تغذیه</title>
<style>
@font-face {
    font-family: 'Vazirmatn';
    src: url('${origin}/fonts/Vazirmatn-Regular.woff2') format('woff2');
    font-weight: 400;
    font-display: block;
}
@font-face {
    font-family: 'Vazirmatn';
    src: url('${origin}/fonts/Vazirmatn-Bold.woff2') format('woff2');
    font-weight: 700;
    font-display: block;
}
@page { size: A4; margin: 14mm 12mm; }
* { box-sizing: border-box; }
body {
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    margin: 0;
    color: #1f2937;
    font-size: 11px;
    line-height: 1.8;
    direction: rtl;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}
.doc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 12px;
    border-bottom: 2px solid #2563eb;
    margin-bottom: 14px;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-mark {
    width: 38px; height: 38px; border-radius: 10px;
    background: #2563eb; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; letter-spacing: .5px;
}
.brand-text h1 { margin: 0; font-size: 16px; font-weight: 700; }
.brand-text p { margin: 0; font-size: 10px; color: #6b7280; }
.issued { text-align: left; font-size: 10px; color: #6b7280; }
.issued strong { display: block; font-size: 12px; color: #111827; }

.meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    margin-bottom: 14px;
}
.meta-item {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 6px 8px;
    display: flex;
    justify-content: space-between;
    gap: 6px;
}
.meta-label { color: #6b7280; font-size: 10px; }
.meta-value { font-weight: 700; font-size: 10px; }

.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 16px; }
.kpi {
    border: 1px solid #e5e7eb;
    border-top: 3px solid #2563eb;
    border-radius: 8px;
    padding: 8px 10px;
    background: #fff;
}
.kpi-label { display: block; font-size: 10px; color: #6b7280; }
.kpi-value { display: block; font-size: 18px; font-weight: 700; color: #111827; }
.kpi-value em { font-size: 10px; font-style: normal; color: #6b7280; margin-right: 3px; }
.kpi-note { display: block; font-size: 9px; color: #2563eb; }

.block { margin-bottom: 16px; page-break-inside: auto; }
.avoid-break { page-break-inside: avoid; }
.block h2 {
    font-size: 12px;
    font-weight: 700;
    margin: 0 0 8px;
    padding-right: 8px;
    border-right: 3px solid #2563eb;
}
.block h2 small { font-weight: 400; color: #6b7280; font-size: 10px; }
.empty { color: #9ca3af; font-size: 10px; }

.data-table { width: 100%; border-collapse: collapse; font-size: 10px; }
.data-table th {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 6px 8px;
    text-align: center;
    font-weight: 700;
    color: #334155;
}
.data-table td { border: 1px solid #e5e7eb; padding: 5px 8px; text-align: center; }
.data-table tbody tr:nth-child(even) td { background: #fafafa; }
.data-table tfoot td { background: #f1f5f9; font-weight: 700; }
.right { text-align: right !important; }
.mono { font-variant-numeric: tabular-nums; }
.strong { font-weight: 700; }
.state-ok { color: #15803d; font-weight: 700; }
.state-warn { color: #b45309; font-weight: 700; }
.state-bad { color: #b91c1c; font-weight: 700; }

.tag { font-size: 8px; padding: 1px 4px; border-radius: 4px; }
.tag-acid { background: #fef3c7; color: #92400e; }
.tank { display: inline-block; font-size: 9px; padding: 1px 6px; border-radius: 10px; background: #e5e7eb; color: #374151; }
.tank-A { background: #dbeafe; color: #1d4ed8; }
.tank-B { background: #ede9fe; color: #6d28d9; }
.tank-C { background: #d1fae5; color: #047857; }

.inline-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.inline-card { border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px 8px; text-align: center; }
.inline-card span { display: block; font-size: 9px; color: #6b7280; }
.inline-card strong { font-size: 12px; }
.inline-card.ok { background: #f0fdf4; border-color: #86efac; color: #15803d; }
.inline-card.bad { background: #fef2f2; border-color: #fca5a5; color: #b91c1c; }

.note { border-radius: 6px; padding: 8px 10px; margin-bottom: 8px; }
.note h3 { margin: 0 0 4px; font-size: 10px; }
.note ul { margin: 0; padding-right: 16px; font-size: 10px; }
.note-warn { background: #fffbeb; border-right: 3px solid #f59e0b; color: #92400e; }
.note-info { background: #eff6ff; border-right: 3px solid #2563eb; color: #1e40af; }

.steps { list-style: none; margin: 0; padding: 0; }
.steps li { display: flex; gap: 8px; align-items: flex-start; padding: 6px 0; border-bottom: 1px dashed #e5e7eb; }
.step-index {
    flex: 0 0 auto;
    width: 18px; height: 18px; border-radius: 50%;
    background: #2563eb; color: #fff;
    font-size: 9px; display: flex; align-items: center; justify-content: center;
}
.step-weight { display: block; font-size: 10px; color: #374151; }
.step-warn { display: block; font-size: 9px; color: #b45309; }

.doc-footer {
    margin-top: 18px;
    padding-top: 8px;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    font-size: 9px;
    color: #9ca3af;
}
</style>
</head>
<body>
${buildHeader(meta)}
${buildKpis(payload.result)}
${buildFertilizerTable(payload)}
${buildInstructions(payload.result)}
${buildElementsTable(payload)}
${buildIonBalance(payload.result)}
${buildNotes(payload.result)}
<footer class="doc-footer">
    <span>تولیدشده توسط FarmTech &mdash; ProFertilizer</span>
    <span>${esc(todayFa())}</span>
</footer>
</body>
</html>`;
    }

    // ============================================================
    // اجرا
    // ============================================================
    async function exportOptimizationPdf(payload: PdfExportPayload): Promise<void> {
        if (!payload?.result) {
            throw new Error('نتیجه‌ای برای خروجی گرفتن وجود ندارد');
        }

        isExporting.value = true;

        try {
            const html = buildDocument(payload);

            // حذف iframe قبلی (در صورت وجود)
            const previous = document.getElementById('farmtech-pdf-frame');
            if (previous) previous.remove();

            const frame = document.createElement('iframe');
            frame.id = 'farmtech-pdf-frame';
            frame.setAttribute('aria-hidden', 'true');
            frame.style.position = 'fixed';
            frame.style.right = '-10000px';
            frame.style.bottom = '0';
            frame.style.width = '210mm';
            frame.style.height = '297mm';
            frame.style.border = '0';
            document.body.appendChild(frame);

            await new Promise<void>((resolve, reject) => {
                const doc = frame.contentDocument || frame.contentWindow?.document;
                if (!doc) {
                    reject(new Error('امکان ساخت سند چاپ وجود ندارد'));
                    return;
                }

                doc.open();
                doc.write(html);
                doc.close();

                const start = () => {
                    const win = frame.contentWindow;
                    if (!win) {
                        reject(new Error('امکان باز کردن پنجره چاپ وجود ندارد'));
                        return;
                    }
                    // اطمینان از لود شدن فونت پیش از چاپ
                    const fonts = (doc as any).fonts;
                    const ready = fonts?.ready ? fonts.ready : Promise.resolve();
                    ready
                        .catch(() => undefined)
                        .then(() => {
                            setTimeout(() => {
                                win.focus();
                                win.print();
                                resolve();
                            }, 120);
                        });
                };

                if (doc.readyState === 'complete') {
                    start();
                } else {
                    frame.onload = start;
                    // فالبک در صورت اجرا نشدن onload
                    setTimeout(start, 800);
                }
            });

            // پاک‌سازی با تأخیر تا دیالوگ چاپ بسته شود
            setTimeout(() => {
                document.getElementById('farmtech-pdf-frame')?.remove();
            }, 3000);
        } finally {
            isExporting.value = false;
        }
    }

    return {
        isExporting,
        exportOptimizationPdf
    };
}
