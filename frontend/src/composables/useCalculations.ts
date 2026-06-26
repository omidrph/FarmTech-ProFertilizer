// frontend/src/composables/useCalculations.ts
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';
import type { 
    InterpretationResult, 
    OptimizationResponse,
    OptimizationOptions,
    IonBalance
} from '@/types';
import { useCalcStore } from '@/store/modules/calcStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';

/**
 * 🎯 Composable برای محاسبات
 * تمام منطق محاسباتی در بک‌اند انجام می‌شود
 * این فایل یک wrapper برای API است
 */
export function useCalculations() {
    const isCalculating = ref(false);
    const isOptimizing = ref(false);
    const calcStore = useCalcStore();
    const targetStore = useTargetStore();
    const waterStore = useWaterStore();

    /**
     * 🆕 بهینه‌سازی خودکار فرمول کود
     * 
     * این تابع از الگوریتم NNLS برای محاسبه بهترین ترکیب کودها استفاده می‌کند.
     * کاربر فقط کودها را انتخاب می‌کند و نرم‌افزار بقیه کار را انجام می‌دهد.
     * 
     * @param fertilizers - لیست کودهای انتخاب شده
     * @param options - تنظیمات بهینه‌سازی (اختیاری)
     * @param tankVolume - حجم مخزن اصلی (لیتر)
     * @param stockVolume - حجم استوک (لیتر)
     * @param injectionRatio - نسبت تزریق
     */
    async function optimizeFertilizers(
        fertilizers: any[],
        options?: OptimizationOptions,
        tankVolume: number = 1000,
        stockVolume: number = 100,
        injectionRatio: number = 100
    ): Promise<OptimizationResponse | null> {
        isOptimizing.value = true;
        
        try {
            // دریافت داده‌ها از storeها
            const targetValues = targetStore.targetElements;
            const waterValues = waterStore.waterValues;
            
            // بررسی وجود عناصر هدف
            const hasTargets = Object.values(targetValues).some(v => v > 0);
            if (!hasTargets) {
                throw new Error('لطفاً ابتدا عناصر هدف را در بخش مربوطه وارد کنید');
            }
            
            // بررسی انتخاب کودها
            if (!fertilizers || fertilizers.length === 0) {
                throw new Error('لطفاً حداقل یک کود را انتخاب کنید');
            }
            
            // تبدیل داده‌ها به فرمت مورد نیاز
            const targetValuesRecord: Record<string, number> = {};
            for (const [key, value] of Object.entries(targetValues)) {
                if (value > 0) {
                    targetValuesRecord[key] = value;
                }
            }
            
            const waterValuesRecord: Record<string, number> = {};
            for (const [key, value] of Object.entries(waterValues)) {
                if (value > 0) {
                    waterValuesRecord[key] = value;
                }
            }
            
            // تنظیمات پیش‌فرض
            const defaultOptions: OptimizationOptions = {
                method: 'nnls',
                use_precipitation_check: true,
                use_ion_balance_check: true,
                reservoir_mode: 'auto',
                max_iterations: 1000,
                tolerance: 1e-6,
                cost_weight: 0.01,
                allow_zero_weights: true
            };
            
            const mergedOptions = { ...defaultOptions, ...options };
            
            // فراخوانی API
            const result = await calcStore.optimizeFertilizers(
                targetValuesRecord,
                waterValuesRecord,
                fertilizers,
                mergedOptions,
                tankVolume,
                stockVolume,
                injectionRatio
            );
            
            return result;
            
        } catch (error: any) {
            console.error('Error in optimizeFertilizers:', error);
            throw error;
        } finally {
            isOptimizing.value = false;
        }
    }

    /**
     * تولید تفسیر از طریق API
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
     * تبدیل واحد از طریق API
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
     * محاسبه تعادل یونی از طریق API
     */
    async function calculateIonBalance(
        elements: Record<string, number>,
        unit: 'ppm' | 'meq' | 'mmol' = 'ppm'
    ): Promise<IonBalance | null> {
        try {
            const result = await apiService.calculateIonBalance({ elements, unit });
            return {
                cation: result.cation,
                anion: result.anion,
                isBalanced: result.is_balanced
            };
        } catch (error) {
            console.error('Error calculating ion balance:', error);
            return null;
        }
    }

    /**
     * محاسبه مخازن از طریق API
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
     * محاسبه محلول نهایی از طریق API
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

    /**
     * بررسی رسوب احتمالی
     */
    async function checkPrecipitation(
        concentrations: Record<string, number>,
        temperature: number = 25
    ) {
        try {
            const result = await apiService.checkPrecipitation(concentrations, temperature);
            return result;
        } catch (error) {
            console.error('Error checking precipitation:', error);
            return null;
        }
    }

    /**
     * دریافت تاریخچه بهینه‌سازی
     */
    async function getOptimizationHistory(
        skip: number = 0,
        limit: number = 50,
        reportId?: number
    ) {
        try {
            return await apiService.getOptimizationHistory(skip, limit, reportId);
        } catch (error) {
            console.error('Error getting optimization history:', error);
            return [];
        }
    }

    return {
        isCalculating,
        isOptimizing,
        optimizeFertilizers,
        generateInterpretation,
        convertUnits,
        calculateIonBalance,
        calculateReservoir,
        calculateFinalSolution,
        checkPrecipitation,
        getOptimizationHistory
    };
}