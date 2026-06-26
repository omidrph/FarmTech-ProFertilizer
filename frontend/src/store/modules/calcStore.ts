// frontend/src/store/modules/calcStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { 
    CalculationRow, 
    CalculationInputs, 
    ElementName, 
    ReservoirData,
    OptimizationResponse,
    OptimizationRequest,
    OptimizationOptions
} from '@/types';
import { apiService } from '@/services/apiService';

const ELEMENTS: ElementName[] = [
    'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl',
    'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'
] as ElementName[];

export const useCalcStore = defineStore('calc', () => {
    // ===== State =====
    const calculationRows = ref<CalculationRow[]>([]);
    const calculationInputs = ref<CalculationInputs>({
        tankVolume: 1000,
        dilutionFactor: 1,
        totalLiter: 1000
    });
    const errorMessages = ref<string[]>([]);
    const isLoading = ref(false);
    const isOptimizing = ref(false);
    const currentReportId = ref<string | null>(null);
    const reservoirData = ref<ReservoirData>({ A: [], B: [], C: [] });
    const totalCost = ref(0);
    
    // ===== 🆕 State برای بهینه‌سازی =====
    const optimizationResult = ref<OptimizationResponse | null>(null);
    const optimizationHistory = ref<OptimizationResponse[]>([]);
    const lastOptimizationError = ref<string | null>(null);

    // ===== Getters =====
    const elementTotals = computed(() => {
        const totals: Partial<Record<ElementName, number>> = {};
        for (const element of ELEMENTS) {
            totals[element] = calculationRows.value.reduce((sum: number, row: CalculationRow) => {
                return sum + (row.elements?.[element] || 0);
            }, 0);
        }
        return totals;
    });

    const hasErrors = computed(() => errorMessages.value.length > 0);

    const fixedRows = computed(() => {
        return calculationRows.value.filter((row: CalculationRow) => row.isFixedRow);
    });

    const dynamicRows = computed(() => {
        return calculationRows.value.filter((row: CalculationRow) => !row.isFixedRow);
    });

    // ===== 🆕 Getters برای بهینه‌سازی =====
    const hasOptimizationResult = computed(() => optimizationResult.value !== null);
    const optimizationCost = computed(() => optimizationResult.value?.cost_total || 0);
    const optimizationError = computed(() => optimizationResult.value?.residual_error || 0);
    const isOptimizationConverged = computed(() => optimizationResult.value?.is_converged || false);

    // ===== Actions =====

    /**
     * 🆕 تابع مقداردهی اولیه ردیف‌های ثابت - دیگر استفاده نمی‌شود
     * این تابع برای backward compatibility نگه داشته شده اما کاربردی ندارد
     * @deprecated دیگر از این تابع استفاده نمی‌شود
     */
    function initializeFixedRows() {
        // ⚠️ این تابع دیگر ردیف‌های ثابت را ایجاد نمی‌کند
        // کاربر باید خودش کودهای مورد نظر را انتخاب کند
        calculationRows.value = [];
    }

    /**
     * 🆕 افزودن ردیف جدید به جدول محاسبه
     * این تابع توسط کامپوننت FertilizerCalcTab فراخوانی می‌شود
     */
    function addCalculationRow(
        fertilizerName: string, 
        elements: Partial<Record<ElementName, number>>, 
        fertilizerId?: string
    ) {
        const newRow: CalculationRow = {
            id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
            materialName: fertilizerName,
            weight: 0,
            purity: 100,
            cost: 0,
            elements: elements || {},
            isAcid: false,
            isFixedRow: false,
            fertilizerId: fertilizerId
        };
        calculationRows.value.push(newRow);
        return newRow;
    }

    /**
     * به‌روزرسانی یک ردیف موجود
     */
    function updateCalculationRow(id: string, data: Partial<Omit<CalculationRow, 'id' | 'isFixedRow'>>) {
        const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
        if (index !== -1) {
            const row = calculationRows.value[index];
            if (data.weight !== undefined) row.weight = data.weight;
            if (data.purity !== undefined) row.purity = data.purity;
            if (data.materialName !== undefined) row.materialName = data.materialName;
            if (data.cost !== undefined) row.cost = data.cost;
            if (data.elements !== undefined) row.elements = data.elements;
            if (data.isAcid !== undefined) row.isAcid = data.isAcid;
            if (data.acidType !== undefined) row.acidType = data.acidType;
            calculationRows.value[index] = row;
            return true;
        }
        return false;
    }

    /**
     * حذف یک ردیف از جدول
     * فقط ردیف‌های غیرثابت (isFixedRow === false) قابل حذف هستند
     */
    function removeCalculationRow(id: string) {
        const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
        if (index !== -1 && !calculationRows.value[index].isFixedRow) {
            calculationRows.value.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * حذف همه ردیف‌ها (به جز ردیف‌های ثابت - که الان وجود ندارند)
     */
    function clearAllRows() {
        calculationRows.value = [];
        optimizationResult.value = null;
    }

    /**
     * به‌روزرسانی تنظیمات ورودی محاسبه
     */
    function updateCalculationInputs(inputs: Partial<CalculationInputs>) {
        const newTankVolume = inputs.tankVolume !== undefined ? inputs.tankVolume : calculationInputs.value.tankVolume;
        const newDilutionFactor = inputs.dilutionFactor !== undefined ? inputs.dilutionFactor : calculationInputs.value.dilutionFactor;
        calculationInputs.value = {
            tankVolume: newTankVolume,
            dilutionFactor: newDilutionFactor,
            totalLiter: newTankVolume * newDilutionFactor
        };
    }

    /**
     * 🎯 محاسبه مخازن از طریق API بک‌اند
     */
    async function calculateReservoirDataFromAPI(): Promise<ReservoirData | null> {
        isLoading.value = true;
        try {
            const fertilizers = calculationRows.value
                .filter(row => row.weight && row.weight > 0)
                .map(row => ({
                    fertilizer: {
                        name: row.materialName,
                        is_acid: row.isAcid || false
                    },
                    weight: row.weight,
                    purity: row.purity
                }));

            const result = await apiService.calculateReservoir({ fertilizers });
            reservoirData.value = result.reservoir_data;
            return result.reservoir_data;
        } catch (error) {
            console.error('Error calculating reservoir data:', error);
            errorMessages.value.push('خطا در محاسبه مخازن');
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * 🎯 محاسبه کامل و ذخیره در دیتابیس
     */
    async function calculateAndSave(reportId: string): Promise<any> {
        isLoading.value = true;
        errorMessages.value = [];
        try {
            const reservoir = await calculateReservoirDataFromAPI();
            if (!reservoir) {
                throw new Error('خطا در محاسبه مخازن');
            }

            totalCost.value = calculationRows.value.reduce((sum, row) => sum + (row.cost || 0), 0);

            const calcData = {
                target_values: {},
                final_values: elementTotals.value,
                reservoir_data: reservoir,
                calc_rows: calculationRows.value.map((row: CalculationRow) => ({
                    material_name: row.materialName,
                    weight: row.weight,
                    purity: row.purity,
                    cost: row.cost,
                    elements: row.elements,
                    is_acid: row.isAcid || false,
                    acid_type: row.acidType || null,
                    is_fixed: row.isFixedRow || false
                }))
            };

            const result = await apiService.createCalculation(reportId, calcData);
            if (result) {
                currentReportId.value = reportId;
                return result;
            }
            errorMessages.value.push('خطا در ذخیره محاسبات');
            return null;
        } catch (err: any) {
            errorMessages.value.push(err.message || 'خطا در انجام محاسبات');
            console.error('Error in calculateAndSave:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * بارگذاری محاسبات از دیتابیس
     */
    async function loadCalculation(reportId: string): Promise<boolean> {
        isLoading.value = true;
        errorMessages.value = [];
        try {
            const data = await apiService.getCalculation(reportId);
            if (data) {
                if (data.calc_rows && Array.isArray(data.calc_rows)) {
                    calculationRows.value = data.calc_rows.map((row: any) => ({
                        id: row.id || `row-${Date.now()}-${Math.random()}`,
                        materialName: row.material_name || row.materialName,
                        weight: row.weight || 0,
                        purity: row.purity || 100,
                        cost: row.cost || 0,
                        elements: row.elements || {},
                        isAcid: row.is_acid || row.isAcid || false,
                        acidType: row.acid_type || row.acidType || null,
                        isFixedRow: row.is_fixed || row.isFixedRow || false
                    }));
                }
                if (data.reservoir_data) {
                    reservoirData.value = data.reservoir_data;
                }
                currentReportId.value = reportId;
                return true;
            }
            return false;
        } catch (err: any) {
            errorMessages.value.push(err.message || 'خطا در بارگذاری محاسبات');
            console.error('Error loading calculation:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    // ============================================================
    // 🆕 توابع بهینه‌سازی خودکار
    // ============================================================

    /**
     * 🚀 بهینه‌سازی خودکار فرمول کود
     * 
     * این تابع قلب تپنده جدید FarmTech است.
     * با استفاده از الگوریتم NNLS، بهترین ترکیب کودها را محاسبه می‌کند.
     * 
     * @param targetValues - عناصر هدف (ppm)
     * @param waterValues - عناصر موجود در آب (ppm)
     * @param fertilizers - لیست کودهای انتخاب شده
     * @param options - تنظیمات بهینه‌سازی
     * @param tankVolume - حجم مخزن (لیتر)
     * @param stockVolume - حجم استوک (لیتر)
     * @param injectionRatio - نسبت تزریق
     */
    async function optimizeFertilizers(
        targetValues: Record<string, number>,
        waterValues: Record<string, number>,
        fertilizers: any[],
        options?: OptimizationOptions,
        tankVolume: number = 1000,
        stockVolume: number = 100,
        injectionRatio: number = 100
    ): Promise<OptimizationResponse | null> {
        isOptimizing.value = true;
        lastOptimizationError.value = null;
        optimizationResult.value = null;

        try {
            // آماده‌سازی داده‌ها برای API
            const requestData: OptimizationRequest = {
                target_values: targetValues,
                water_values: waterValues,
                fertilizers: fertilizers.map(f => ({
                    id: f.id,
                    name: f.name,
                    elements: f.elements || {},
                    price_per_kg: f.pricePerKg || 0,
                    purity: f.concentration || 100,
                    is_acid: f.isAcid || false,
                    is_system_default: f.isSystemDefault || false
                })),
                options: options || {
                    method: 'nnls',
                    use_precipitation_check: true,
                    use_ion_balance_check: true,
                    reservoir_mode: 'auto'
                },
                tank_volume: tankVolume,
                stock_volume: stockVolume,
                injection_ratio: injectionRatio
            };

            // ارسال درخواست به API
            const result = await apiService.optimizeFertilizers(requestData);
            
            if (result) {
                optimizationResult.value = result;
                
                // تبدیل نتایج به ردیف‌های جدول (برای سازگاری با نسخه قبلی)
                const newRows: CalculationRow[] = [];
                let totalCostValue = 0;
                
                for (const [fertilizerId, weight] of Object.entries(result.weights)) {
                    const fert = fertilizers.find(f => f.id === fertilizerId);
                    if (fert && weight > 0) {
                        const cost = (weight / 1000) * (fert.pricePerKg || 0);
                        totalCostValue += cost;
                        
                        newRows.push({
                            id: `row-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
                            materialName: fert.name || 'نامشخص',
                            weight: weight,
                            purity: fert.concentration || 100,
                            cost: cost,
                            elements: fert.elements || {},
                            isAcid: fert.isAcid || false,
                            acidType: fert.acidType || null,
                            fertilizerId: fertilizerId,
                            isFixedRow: false
                        });
                    }
                }
                
                // به‌روزرسانی ردیف‌های جدول
                calculationRows.value = newRows;
                totalCost.value = totalCostValue;
                
                // به‌روزرسانی مخازن
                if (result.reservoir_data) {
                    reservoirData.value = result.reservoir_data;
                }
                
                // اضافه کردن به تاریخچه
                optimizationHistory.value.unshift(result);
                if (optimizationHistory.value.length > 50) {
                    optimizationHistory.value.pop();
                }
                
                return result;
            }
            
            const errorMsg = 'نتیجه‌ای از سرور دریافت نشد';
            lastOptimizationError.value = errorMsg;
            errorMessages.value.push(errorMsg);
            return null;
            
        } catch (error: any) {
            console.error('Error in optimizeFertilizers:', error);
            const errorMsg = error.message || 'خطا در بهینه‌سازی';
            lastOptimizationError.value = errorMsg;
            errorMessages.value.push(errorMsg);
            return null;
        } finally {
            isOptimizing.value = false;
        }
    }

    /**
     * ذخیره نتیجه بهینه‌سازی در گزارش
     */
    async function saveOptimizationToReport(reportId: string): Promise<boolean> {
        if (!optimizationResult.value) {
            errorMessages.value.push('هیچ نتیجه بهینه‌سازی برای ذخیره وجود ندارد');
            return false;
        }

        try {
            const result = await calculateAndSave(reportId);
            return !!result;
        } catch (error) {
            console.error('Error saving optimization to report:', error);
            return false;
        }
    }

    /**
     * بارگذاری تاریخچه بهینه‌سازی از سرور
     */
    async function loadOptimizationHistory(
        skip: number = 0, 
        limit: number = 50, 
        reportId?: number
    ): Promise<OptimizationResponse[]> {
        try {
            const history = await apiService.getOptimizationHistory(skip, limit, reportId);
            // تبدیل به فرمت مناسب
            const formattedHistory = history.map((item: any) => ({
                weights: item.optimized_weights || {},
                concentrations: item.final_concentrations || {},
                residual_error: item.residual_error || 0,
                cost_total: item.cost_total || 0,
                ion_balance: item.ion_balance || { cation: 0, anion: 0, isBalanced: true, message: '' },
                target_achievement: {},
                warnings: item.warnings || [],
                suggestions: item.suggestions || [],
                reservoir_data: { A: [], B: [], C: [] },
                iterations: item.iterations || 0,
                convergence_time_ms: item.convergence_time_ms || 0,
                is_converged: item.is_successful || false,
                summary: ''
            }));
            
            optimizationHistory.value = formattedHistory;
            return formattedHistory;
        } catch (error) {
            console.error('Error loading optimization history:', error);
            return [];
        }
    }

    /**
     * پاک کردن نتیجه بهینه‌سازی
     */
    function clearOptimizationResult() {
        optimizationResult.value = null;
        lastOptimizationError.value = null;
    }

    /**
     * بازنشانی کامل - بدون ردیف‌های ثابت
     */
    function resetCalculation() {
        calculationRows.value = [];
        errorMessages.value = [];
        reservoirData.value = { A: [], B: [], C: [] };
        calculationInputs.value = {
            tankVolume: 1000,
            dilutionFactor: 1,
            totalLiter: 1000
        };
        currentReportId.value = null;
        totalCost.value = 0;
        optimizationResult.value = null;
        lastOptimizationError.value = null;
    }

    function addError(message: string) {
        if (!errorMessages.value.includes(message)) {
            errorMessages.value.push(message);
        }
    }

    function removeError(message: string) {
        const index = errorMessages.value.indexOf(message);
        if (index !== -1) {
            errorMessages.value.splice(index, 1);
        }
    }

    function clearErrors() {
        errorMessages.value = [];
    }

    // ===== Initialize =====
    // ⚠️ دیگر initializeFixedRows() در ابتدا اجرا نمی‌شود
    // جدول محاسبه خالی شروع می‌شود و کاربر باید کودهای خود را انتخاب کند
    calculationRows.value = [];

    return {
        // State
        calculationRows,
        calculationInputs,
        errorMessages,
        isLoading,
        isOptimizing,
        currentReportId,
        reservoirData,
        totalCost,
        
        // 🆕 State بهینه‌سازی
        optimizationResult,
        optimizationHistory,
        lastOptimizationError,
        
        // Getters
        elementTotals,
        hasErrors,
        fixedRows,
        dynamicRows,
        
        // 🆕 Getters بهینه‌سازی
        hasOptimizationResult,
        optimizationCost,
        optimizationError,
        isOptimizationConverged,
        
        // Actions
        initializeFixedRows,
        addCalculationRow,
        updateCalculationRow,
        removeCalculationRow,
        clearAllRows,
        updateCalculationInputs,
        calculateReservoirDataFromAPI,
        calculateAndSave,
        loadCalculation,
        resetCalculation,
        addError,
        removeError,
        clearErrors,
        
        // 🆕 Actions بهینه‌سازی
        optimizeFertilizers,
        saveOptimizationToReport,
        loadOptimizationHistory,
        clearOptimizationResult
    };
});

// ✅ اضافه کردن export default
export default useCalcStore;