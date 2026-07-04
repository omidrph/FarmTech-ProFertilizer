// frontend/src/composables/useCSVExport.ts
import type { OptimizationResponse } from '@/types';

export function useCSVExport() {
  
  const escapeCSV = (value: string | number | null | undefined): string => {
    if (value === null || value === undefined) return '';
    const stringValue = String(value);
    if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
      return `"${stringValue.replace(/"/g, '""')}"`;
    }
    return stringValue;
  };

  const generateCSVContent = (
    result: OptimizationResponse,
    fertilizers: any[],
    targetValues: Record<string, number>
  ): string => {
    const lines: string[] = [];

    // ================================================================
    // 1. هدر گزارش
    // ================================================================
    lines.push('"گزارش بهینه‌سازی ترکیب کود"');
    lines.push(`"تاریخ",${escapeCSV(new Date().toLocaleDateString('fa-IR'))}`);
    lines.push(`"زمان",${escapeCSV(new Date().toLocaleTimeString('fa-IR'))}`);
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 2. خلاصه بهینه‌سازی
    // ================================================================
    lines.push('"خلاصه بهینه‌سازی"');
    lines.push(`"خطای کل",${escapeCSV((result.residual_error * 100).toFixed(2))}%`);
    lines.push(`"وضعیت همگرایی",${escapeCSV(result.is_converged ? 'موفق' : 'ناموفق')}`);
    lines.push(`"تعداد تکرار",${escapeCSV(result.iterations)}`);
    lines.push(`"زمان محاسبه",${escapeCSV(result.convergence_time_ms.toFixed(0))}ms`);
    lines.push(`"مجموع هزینه",${escapeCSV(result.cost_total?.toFixed(0) || '0')} تومان`);
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 3. پارامترهای محلول نهایی
    // ================================================================
    lines.push('"پارامترهای محلول نهایی"');
    if (result.ec !== undefined) {
      lines.push(`"EC نهایی",${escapeCSV(result.ec.toFixed(2))},dS/m,${escapeCSV(result.ec_status || 'نامشخص')}`);
    }
    if (result.ph !== undefined) {
      lines.push(`"pH نهایی",${escapeCSV(result.ph.toFixed(2))},pH,${escapeCSV(result.ph_status || 'نامشخص')}`);
    }
    if (result.ec_ph_status?.message) {
      lines.push(`"وضعیت ترکیبی",${escapeCSV(result.ec_ph_status.message)}`);
      if (result.ec_ph_status.recommendations?.length > 0) {
        lines.push(`"توصیه‌ها",${escapeCSV(result.ec_ph_status.recommendations.join('; '))}`);
      }
    }
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 4. جدول وزن کودها
    // ================================================================
    lines.push('"مقدار کودها برای ساخت استوک"');
    lines.push('"شناسه کود","نام کود","وزن (گرم)","هزینه (تومان)","عناصر تشکیل‌دهنده"');

    const weights = result.weights || {};
    for (const [id, weight] of Object.entries(weights)) {
      if (weight !== undefined && weight !== null && typeof weight === 'number' && weight > 0) {
        const fert = fertilizers.find(f => f.id === id);
        const name = fert?.name || id;
        const cost = fert ? (weight / 1000) * (fert.pricePerKg || 0) : 0;
        
        // جمع‌آوری عناصر
        const elements: string[] = [];
        if (fert?.elements) {
          for (const [element, pct] of Object.entries(fert.elements)) {
            if (pct !== undefined && pct !== null && typeof pct === 'number' && pct > 0) {
              elements.push(`${element}: ${pct}%`);
            }
          }
        }
        
        lines.push([
          escapeCSV(id),
          escapeCSV(name),
          escapeCSV(weight.toFixed(3)),
          escapeCSV(cost.toFixed(0)),
          escapeCSV(elements.join(' | '))
        ].join(','));
      }
    }

    // اضافه کردن جمع کل
    lines.push(`"مجموع هزینه",,,,,${escapeCSV(result.cost_total?.toFixed(0) || '0')}`);
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 5. جدول مقایسه عناصر
    // ================================================================
    lines.push('"مقایسه عناصر هدف و تامین شده"');
    lines.push('"عنصر","هدف (PPM)","تامین (PPM)","درصد تامین","خطا (%)"');

    if (result.target_achievement) {
      for (const [element, pct] of Object.entries(result.target_achievement)) {
        const target = targetValues[element] || 0;
        const actual = result.concentrations[element] || 0;
        const error = target > 0 ? ((Math.abs(actual - target) / target) * 100) : 0;
        
        lines.push([
          escapeCSV(element),
          escapeCSV(target.toFixed(1)),
          escapeCSV(actual.toFixed(1)),
          escapeCSV(pct.toFixed(1)),
          escapeCSV(error.toFixed(2))
        ].join(','));
      }
    }
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 6. تعادل یونی
    // ================================================================
    lines.push('"تعادل یونی"');
    lines.push(`"کاتیون",${escapeCSV(result.ion_balance.cation.toFixed(2))},meq/L`);
    lines.push(`"آنیون",${escapeCSV(result.ion_balance.anion.toFixed(2))},meq/L`);
    lines.push(`"وضعیت",${escapeCSV(result.ion_balance.isBalanced ? 'متعادل' : 'نامتعادل')}`);
    if (!result.ion_balance.isBalanced) {
      const diff = Math.abs(result.ion_balance.cation - result.ion_balance.anion);
      lines.push(`"اختلاف",${escapeCSV(diff.toFixed(2))},meq/L`);
    }
    lines.push('');
    lines.push('"================================================"');
    lines.push('');

    // ================================================================
    // 7. هشدارها و پیشنهادات
    // ================================================================
    if (result.warnings.length > 0) {
      lines.push('"هشدارها"');
      for (const warning of result.warnings) {
        lines.push(`"${escapeCSV(warning)}"`);
      }
      lines.push('');
    }

    if (result.suggestions.length > 0) {
      lines.push('"پیشنهادات"');
      for (const suggestion of result.suggestions) {
        lines.push(`"${escapeCSV(suggestion)}"`);
      }
      lines.push('');
    }

    // ================================================================
    // 8. اطلاعات تکمیلی (کودهای استفاده نشده)
    // ================================================================
    const unusedFertilizers: string[] = [];
    for (const [id, weight] of Object.entries(weights)) {
      if (weight !== undefined && weight !== null && typeof weight === 'number' && weight === 0) {
        const fert = fertilizers.find(f => f.id === id);
        unusedFertilizers.push(fert?.name || id);
      }
    }
    
    if (unusedFertilizers.length > 0) {
      lines.push('"کودهای استفاده نشده"');
      lines.push(`"تعداد",${escapeCSV(unusedFertilizers.length)}`);
      lines.push(`"لیست",${escapeCSV(unusedFertilizers.join('; '))}`);
    }

    lines.push('');
    lines.push('"پایان گزارش"');

    return lines.join('\n');
  };

  const downloadCSV = (content: string, filename: string): void => {
    const BOM = '\uFEFF'; // برای پشتیبانی از UTF-8 در اکسل
    const blob = new Blob([BOM + content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const exportOptimizationResult = (
    result: OptimizationResponse,
    fertilizers: any[],
    targetValues: Record<string, number>,
    filename: string = 'بهینه‌سازی_کود'
  ): void => {
    const content = generateCSVContent(result, fertilizers, targetValues);
    downloadCSV(content, filename);
  };

  return {
    generateCSVContent,
    downloadCSV,
    exportOptimizationResult
  };
}