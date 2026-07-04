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
import { useTargetStore } from './targetStore';
import { useReportStore } from './reportStore'; // ✅ اضافه کردن import

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
    
    // ===== State برای بهینه‌سازی =====
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

    const hasOptimizationResult = computed(() => optimizationResult.value !== null);
    const optimizationCost = computed(() => optimizationResult.value?.cost_total || 0);
    const optimizationError = computed(() => optimizationResult.value?.residual_error || 0);
    const isOptimizationConverged = computed(() => optimizationResult.value?.is_converged || false);

    // ===== Actions =====

    function initializeFixedRows() {
        calculationRows.value = [];
    }

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

    function removeCalculationRow(id: string) {
        const index = calculationRows.value.findIndex((row: CalculationRow) => row.id === id);
        if (index !== -1 && !calculationRows.value[index].isFixedRow) {
            calculationRows.value.splice(index, 1);
            return true;
        }
        return false;
    }

    function clearAllRows() {
        calculationRows.value = [];
        optimizationResult.value = null;
    }

    function updateCalculationInputs(inputs: Partial<CalculationInputs>) {
        const newTankVolume = inputs.tankVolume !== undefined ? inputs.tankVolume : calculationInputs.value.tankVolume;
        const newDilutionFactor = inputs.dilutionFactor !== undefined ? inputs.dilutionFactor : calculationInputs.value.dilutionFactor;
        calculationInputs.value = {
            tankVolume: newTankVolume,
            dilutionFactor: newDilutionFactor,
            totalLiter: newTankVolume * newDilutionFactor
        };
    }

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

    async function calculateAndSave(reportId: string): Promise<any> {
        isLoading.value = true;
        errorMessages.value = [];
        try {
            const reservoir = await calculateReservoirDataFromAPI();
            if (!reservoir) {
                throw new Error('خطا در محاسبه مخازن');
            }

            totalCost.value = calculationRows.value.reduce((sum, row) => sum + (row.cost || 0), 0);

            const finalValues: Record<string, number> = {};
            for (const row of calculationRows.value) {
                if (row.elements) {
                    for (const [element, percentage] of Object.entries(row.elements)) {
                        if (percentage && percentage > 0 && row.weight && row.weight > 0) {
                            const contribution = (percentage / 100) * row.weight * (row.purity / 100);
                            finalValues[element] = (finalValues[element] || 0) + contribution;
                        }
                    }
                }
            }

            const calcData = {
                target_values: {},
                final_values: finalValues,
                reservoir_data: reservoir,
                calc_rows: calculationRows.value.map((row: CalculationRow) => ({
                    material_name: row.materialName,
                    weight: row.weight,
                    purity: row.purity,
                    cost: row.cost,
                    elements: row.elements,
                    is_acid: row.isAcid || false,
                    acid_type: row.acidType || null,
                    is_fixed: row.isFixedRow || false,
                    fertilizer_id: row.fertilizerId || null
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
                        fertilizerId: row.fertilizer_id || row.fertilizerId || null,
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
    // توابع بهینه‌سازی خودکار
    // ============================================================

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

            const result = await apiService.optimizeFertilizers(requestData);
            
            if (result) {
                optimizationResult.value = result;
                
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
                
                calculationRows.value = newRows;
                totalCost.value = totalCostValue;
                
                if (result.reservoir_data) {
                    reservoirData.value = result.reservoir_data;
                }
                
                optimizationHistory.value.unshift(result);
                if (optimizationHistory.value.length > 50) {
                    optimizationHistory.value.pop();
                }
                
                // ✅ اصلاح: استفاده صحیح از useReportStore
                const reportStore = useReportStore();
                if (reportStore.currentReportId) {
                    await reportStore.saveCurrentReport();
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

    async function loadOptimizationHistory(
        skip: number = 0, 
        limit: number = 50, 
        reportId?: number
    ): Promise<OptimizationResponse[]> {
        try {
            const history = await apiService.getOptimizationHistory(skip, limit, reportId);
            // ✅ اصلاح: اضافه کردن فیلدهای مورد نیاز OptimizationResponse
            const formattedHistory: OptimizationResponse[] = history.map((item: any) => ({
                weights: item.optimized_weights || {},
                concentrations: item.final_concentrations || {},
                residual_error: item.residual_error || 0,
                cost_total: item.cost_total || 0,
                ion_balance: {
                    cation: item.ion_balance?.cation || 0,
                    anion: item.ion_balance?.anion || 0,
                    isBalanced: item.ion_balance?.isBalanced || false,
                    message: item.ion_balance?.message || ''
                },
                target_achievement: {},
                warnings: item.warnings || [],
                suggestions: item.suggestions || [],
                reservoir_data: { A: [], B: [], C: [] },
                iterations: item.iterations || 0,
                convergence_time_ms: item.convergence_time_ms || 0,
                is_converged: item.is_successful || false,
                summary: '',
                // ✅ اضافه کردن فیلدهای جدید
                ec: 0,
                ph: 7.0,
                ec_status: '',
                ph_status: '',
                ec_ph_status: {
                    status: 'optimal',
                    status_label: 'مطلوب',
                    color: 'success',
                    message: '',
                    issues: [],
                    recommendations: [],
                    ec: 0,
                    ph: 7.0,
                    ec_status: '',
                    ec_label: '',
                    ph_status: '',
                    ph_label: ''
                }
            }));
            
            optimizationHistory.value = formattedHistory;
            return formattedHistory;
        } catch (error) {
            console.error('Error loading optimization history:', error);
            return [];
        }
    }

    function clearOptimizationResult() {
        optimizationResult.value = null;
        lastOptimizationError.value = null;
    }

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
        
        const targetStore = useTargetStore();
        targetStore.resetTargets();
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
        
        optimizationResult,
        optimizationHistory,
        lastOptimizationError,
        
        // Getters
        elementTotals,
        hasErrors,
        fixedRows,
        dynamicRows,
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
        optimizeFertilizers,
        saveOptimizationToReport,
        loadOptimizationHistory,
        clearOptimizationResult
    };
});

export default useCalcStore;