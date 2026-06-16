import { computed, ref } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import type { ElementName, IonBalance, InterpretationResult, Unit } from '@/types';
import { ELEMENTS } from '@/utils/constants';
import {
  calculateIonBalance,
  formatNumber,
  getElementMolecularWeight,
  getElementValence
} from '@/utils/helpers';

export function useCalculations() {
  const targetStore = useTargetStore();
  const waterStore = useWaterStore();
  const calcStore = useCalcStore();

  const isCalculating = ref(false);

  // ===== محاسبه کمبود عناصر =====
  const elementDeficiency = computed(() => {
    const result: Record<ElementName, number> = {} as Record<ElementName, number>;
    
    for (const element of ELEMENTS) {
      const target = targetStore.getTargetElement(element);
      const waterValue = waterStore.getElementFinalValue(element);
      const fertilizerValue = calcStore.elementTotals[element] || 0;
      
      const deficiency = target - (waterValue + fertilizerValue);
      result[element] = deficiency;
    }
    
    return result;
  });

  // ===== محاسبه تعادل یونی نهایی =====
  const finalIonBalance = computed<IonBalance>(() => {
    const totalElements: Record<ElementName, number> = {} as Record<ElementName, number>;
    
    for (const element of ELEMENTS) {
      const waterValue = waterStore.getElementFinalValue(element);
      const fertilizerValue = calcStore.elementTotals[element] || 0;
      totalElements[element] = waterValue + fertilizerValue;
    }
    
    // اصلاح: ارسال یک شیء کامل
    return calculateIonBalance(totalElements);
  });

  // ===== محاسبه مقدار نهایی محلول =====
  function calculateFinalSolution() {
    isCalculating.value = true;
    
    try {
      const finalSolution: Record<ElementName, number> = {} as Record<ElementName, number>;
      
      for (const element of ELEMENTS) {
        const waterValue = waterStore.getElementFinalValue(element);
        const fertilizerValue = calcStore.elementTotals[element] || 0;
        finalSolution[element] = waterValue + fertilizerValue;
      }
      
      // اصلاح: ارسال یک شیء کامل
      const balance = calculateIonBalance(finalSolution);
      if (!balance.isBalanced) {
        calcStore.addError('تعادل کاتیون و آنیون برقرار نیست. لطفاً مقادیر را تنظیم کنید.');
      } else {
        calcStore.removeError('تعادل کاتیون و آنیون برقرار نیست. لطفاً مقادیر را تنظیم کنید.');
      }
      
      for (const element of ELEMENTS) {
        const target = targetStore.getTargetElement(element);
        const actual = finalSolution[element] || 0;
        const diff = target - actual;
        
        if (diff > 1) {
          calcStore.addError(`عنصر ${element}: کمبود ${formatNumber(diff)} ${targetStore.targetUnit}`);
        } else if (diff < -1) {
          calcStore.addError(`عنصر ${element}: بیش‌بود ${formatNumber(Math.abs(diff))} ${targetStore.targetUnit}`);
        }
      }
      
      return finalSolution;
    } catch (error) {
      calcStore.addError('خطا در محاسبات: ' + (error as Error).message);
      return null;
    } finally {
      isCalculating.value = false;
    }
  }

  // ===== تفسیر داده‌ها =====
  function generateInterpretation(): InterpretationResult | null {
    try {
      const finalSolution = calculateFinalSolution();
      if (!finalSolution) return null;

      const balance = finalIonBalance.value;

      const elementStatus = ELEMENTS.map(element => {
        const target = targetStore.getTargetElement(element);
        const actual = finalSolution[element] || 0;
        const diff = target - actual;
        
        let status: 'deficient' | 'sufficient' | 'excessive' | 'toxic' = 'sufficient';
        let message = 'وضعیت مطلوب';
        
        if (diff > 5) {
          status = 'deficient';
          message = `کمبود ${formatNumber(diff)} واحد`;
        } else if (diff < -5) {
          status = 'excessive';
          message = `بیش‌بود ${formatNumber(Math.abs(diff))} واحد`;
        } else if (diff < -15) {
          status = 'toxic';
          message = 'سمیت احتمالی';
        }
        
        return {
          element,
          target,
          actual,
          difference: diff,
          status,
          message
        };
      });

      const salinity = waterStore.waterMixData.waterSalinity;
      let salinityImpact = 'مناسب';
      let salinityRecommendation = 'نیازی به اقدام نیست';
      
      if (salinity > 2.5) {
        salinityImpact = 'بالا';
        salinityRecommendation = 'استفاده از آب با شوری کمتر توصیه می‌شود';
      } else if (salinity > 1.5) {
        salinityImpact = 'متوسط';
        salinityRecommendation = 'توجه به عناصر سمی در آب';
      }

      const recommendations: { issue: string; suggestion: string; priority: 'low' | 'medium' | 'high' }[] = [];
      
      if (!balance.isBalanced) {
        recommendations.push({
          issue: 'عدم تعادل یونی',
          suggestion: 'مقادیر کاتیون و آنیون را تنظیم کنید تا برابر شوند',
          priority: 'high'
        });
      }

      for (const status of elementStatus) {
        if (status.status === 'deficient' || status.status === 'toxic') {
          recommendations.push({
            issue: `عنصر ${status.element}: ${status.message}`,
            suggestion: status.status === 'deficient' 
              ? 'افزایش مقدار این عنصر در فرمول غذایی' 
              : 'کاهش مقدار این عنصر یا بررسی کیفیت آب',
            priority: status.status === 'toxic' ? 'high' : 'medium'
          });
        }
      }

      const summary = `
        گزارش تفسیر تغذیه گیاه:
        - تعادل یونی: ${balance.isBalanced ? 'برقرار ✅' : 'نامتعادل ⚠️'}
        - عناصر دارای مشکل: ${elementStatus.filter(e => e.status !== 'sufficient').map(e => e.element).join(', ') || 'هیچکدام'}
        - کیفیت آب: ${salinityImpact}
        - تعداد توصیه‌ها: ${recommendations.length}
      `;

      return {
        ionBalance: {
          cation: balance.cation,
          anion: balance.anion,
          isBalanced: balance.isBalanced,
          message: balance.isBalanced ? 'تعادل یونی برقرار است' : 'تعادل یونی برقرار نیست'
        },
        elementStatus,
        waterQuality: {
          salinity,
          impact: salinityImpact,
          recommendation: salinityRecommendation
        },
        fertilizerRecommendation: recommendations,
        summary
      };

    } catch (error) {
      calcStore.addError('خطا در تفسیر داده‌ها: ' + (error as Error).message);
      return null;
    }
  }

  // ===== تبدیل واحدها =====
  function convertUnits(value: number, fromUnit: string, toUnit: string, element: ElementName): number {
    const mw = getElementMolecularWeight(element);
    const valence = getElementValence(element);
    
    if (fromUnit === 'ppm' && toUnit === 'meq') {
      return (value * valence) / mw;
    } else if (fromUnit === 'ppm' && toUnit === 'mmol') {
      return value / mw;
    } else if (fromUnit === 'meq' && toUnit === 'ppm') {
      return (value * mw) / valence;
    } else if (fromUnit === 'meq' && toUnit === 'mmol') {
      return value / valence;
    } else if (fromUnit === 'mmol' && toUnit === 'ppm') {
      return value * mw;
    } else if (fromUnit === 'mmol' && toUnit === 'meq') {
      return value * valence;
    }
    
    return value;
  }

  return {
    isCalculating,
    elementDeficiency,
    finalIonBalance,
    calculateFinalSolution,
    generateInterpretation,
    convertUnits
  };
}