// frontend/src/composables/useCalculations.ts
import { ref } from 'vue';
import { apiService } from '@/services/apiService';
import type { InterpretationResult } from '@/types';

/**
 * 🎯 Composable برای محاسبات
 * تمام منطق محاسباتی در بک‌اند انجام می‌شود
 * این فایل فقط یک wrapper برای API است
 */
export function useCalculations() {
  const isCalculating = ref(false);

  /**
   * 🆕 تولید تفسیر از طریق API
   * تمام منطق محاسباتی در بک‌اند انجام می‌شود
   */
  async function generateInterpretation(reportId: string): Promise<InterpretationResult | null> {
    isCalculating.value = true;
    try {
      const result = await apiService.calculateInterpretation(reportId);

      if (result) {
        return {
          ionBalance: {
            cation: result.ion_balance.cation,
            anion: result.ion_balance.anion,
            isBalanced: result.ion_balance.is_balanced,
            message: result.ion_balance.message
          },
          elementStatus: result.element_status,
          waterQuality: result.water_quality,
          fertilizerRecommendation: result.fertilizer_recommendation,
          summary: result.summary
        };
      }
      return null;
    } catch (error) {
      console.error('Error generating interpretation:', error);
      return null;
    } finally {
      isCalculating.value = false;
    }
  }

  /**
   * 🆕 تبدیل واحد از طریق API
   */
  async function convertUnits(
    value: number,
    fromUnit: string,
    toUnit: string,
    element: string
  ): Promise<number | null> {
    try {
      const result = await apiService.convertUnit({
        value,
        from_unit: fromUnit,
        to_unit: toUnit,
        element
      });
      return result.converted_value;
    } catch (error) {
      console.error('Error converting units:', error);
      return null;
    }
  }

  /**
   * 🆕 محاسبه تعادل یونی از طریق API
   */
  async function calculateIonBalance(
    elements: Record<string, number>,
    unit: 'ppm' | 'meq' | 'mmol' = 'ppm'
  ) {
    try {
      const result = await apiService.calculateIonBalance({ elements, unit });
      return {
        cation: result.cation,
        anion: result.anion,
        isBalanced: result.is_balanced,
        message: result.message
      };
    } catch (error) {
      console.error('Error calculating ion balance:', error);
      return null;
    }
  }

  /**
   * 🆕 محاسبه مخازن از طریق API
   */
  async function calculateReservoir(fertilizers: any[]) {
    try {
      const result = await apiService.calculateReservoir({ fertilizers });
      return result;
    } catch (error) {
      console.error('Error calculating reservoir:', error);
      return null;
    }
  }

  /**
   * 🆕 محاسبه محلول نهایی از طریق API
   */
  async function calculateFinalSolution(
    targetValues: Record<string, number>,
    waterValues: Record<string, number>,
    fertilizerContributions: Record<string, number>
  ) {
    try {
      const result = await apiService.calculateFinalSolution({
        target_values: targetValues,
        water_values: waterValues,
        fertilizer_contributions: fertilizerContributions
      });
      return result;
    } catch (error) {
      console.error('Error calculating final solution:', error);
      return null;
    }
  }

  return {
    isCalculating,
    generateInterpretation,
    convertUnits,
    calculateIonBalance,
    calculateReservoir,
    calculateFinalSolution
  };
}