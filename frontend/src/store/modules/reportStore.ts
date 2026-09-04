// frontend/src/store/modules/reportStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';
import { useTargetStore } from './targetStore';
import { useWaterStore } from './waterStore';
import { useCalcStore } from './calcStore';

export interface ReportData {
  id: number | null;
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  date: string;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface ReportListItem {
  id: number;
  report_name: string | null;
  plant_name: string | null;
  season: string | null;
  growth_stage: string | null;
  report_date: string | null;
  created_at: string;
  updated_at: string | null;
}

const getCurrentShamsiDate = (): string => {
  const now = new Date();
  return now.toLocaleDateString('fa-IR');
};

export const useReportStore = defineStore('report', () => {
  // ===== State =====
  const currentReportId = ref<number | null>(null);
  const reportData = ref<ReportData>({
    id: null,
    reportName: '',
    plantName: '',
    season: '',
    growthStage: '',
    date: getCurrentShamsiDate(),
    createdAt: null,
    updatedAt: null
  });
  const reports = ref<ReportListItem[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const isSaving = ref(false);

  // ===== Getters =====
  const hasActiveReport = computed(() => currentReportId.value !== null);
  const isReportComplete = computed(() => {
    return !!(
      reportData.value.reportName &&
      reportData.value.plantName &&
      reportData.value.season &&
      reportData.value.growthStage
    );
  });
  const reportSummary = computed(() => {
    return `${reportData.value.reportName} - ${reportData.value.plantName} (${reportData.value.season})`;
  });

  // ===== Actions =====

  function createNewReport(): void {
    console.log('📄 Creating new empty report...');
    
    reportData.value = {
      id: null,
      reportName: '',
      plantName: '',
      season: '',
      growthStage: '',
      date: getCurrentShamsiDate(),
      createdAt: null,
      updatedAt: null
    };
    
    currentReportId.value = null;
    
    const targetStore = useTargetStore();
    const waterStore = useWaterStore();
    const calcStore = useCalcStore();
    
    targetStore.resetTargets();
    waterStore.resetWaterData();
    calcStore.resetCalculation();
    
    window.dispatchEvent(new CustomEvent('report-reset'));
    window.dispatchEvent(new CustomEvent('report-changed'));
    
    console.log('✅ New report created, all stores reset');
  }

  async function loadReport(reportId: number): Promise<boolean> {
    console.log(`📂 Loading report ${reportId}...`);
    
    isLoading.value = true;
    error.value = null;
    
    try {
      const targetStore = useTargetStore();
      const waterStore = useWaterStore();
      const calcStore = useCalcStore();
      
      targetStore.resetTargets();
      waterStore.resetWaterData();
      calcStore.resetCalculation();
      
      const report = await apiService.getReport(String(reportId));
      if (!report) {
        throw new Error('گزارش پیدا نشد');
      }
      
      reportData.value = {
        id: report.id,
        reportName: report.report_name || '',
        plantName: report.plant_name || '',
        season: report.season || '',
        growthStage: report.growth_stage || '',
        date: report.report_date || getCurrentShamsiDate(),
        createdAt: report.created_at || null,
        updatedAt: report.updated_at || null
      };
      
      currentReportId.value = report.id;
      
      // Water analysis
      try {
        const waterAnalysis = await apiService.getWaterAnalysis(String(reportId));
        if (waterAnalysis) {
          waterStore.loadFromAPI(waterAnalysis);
          console.log('💧 Water analysis loaded');
        }
      } catch (err) {
        console.log('ℹ️ No water analysis found');
      }
      
      // Calculation data
      try {
        const calculation = await apiService.getCalculation(String(reportId));
        if (calculation) {
          // Load targets
          if (calculation.target_values) {
            let targetValues = calculation.target_values;
            if (typeof targetValues === 'string') {
              try {
                targetValues = JSON.parse(targetValues);
              } catch (e) {
                targetValues = {};
              }
            }
            if (typeof targetValues === 'object' && targetValues !== null) {
              targetStore.loadTargetsFromObject(targetValues);
            }
          }
          
          // Load calc rows
          if (calculation.calc_rows && Array.isArray(calculation.calc_rows)) {
            calcStore.setCalculationRows(calculation.calc_rows);
          }
          
          // Load reservoir data
          if (calculation.reservoir_data) {
            let reservoirData = calculation.reservoir_data;
            if (typeof reservoirData === 'string') {
              try {
                reservoirData = JSON.parse(reservoirData);
              } catch (e) {
                reservoirData = { A: [], B: [], C: [] };
              }
            }
            calcStore.setReservoirData(reservoirData);

            // 🆕 رفع باگ «صفحه محاسبه کود ناقص برمی‌گردد»: تنظیمات استوک
            // (حجم مخزن اصلی، حجم سطل استوک، نسبت تزریق) قبلاً هیچ‌جا ذخیره
            // نمی‌شدند و با بازکردن گزارش قدیمی همیشه مقدار پیش‌فرض نشان
            // داده می‌شد. حالا این تنظیمات از داخل reservoir_data.settings
            // بازیابی می‌شوند.
            const savedSettings = (reservoirData as any)?.settings;
            if (savedSettings) {
              calcStore.setStockSettings({
                tankVolume: savedSettings.tank_volume,
                stockVolume: savedSettings.stock_volume,
                injectionRatio: savedSettings.injection_ratio
              });
            }
          }
          
          console.log('🧮 Calculation data loaded');
        }
      } catch (err) {
        console.log('ℹ️ No calculation found');
      }
      
      window.dispatchEvent(new CustomEvent('report-changed'));
      
      console.log(`✅ Report ${reportId} loaded successfully`);
      return true;
      
    } catch (err: any) {
      error.value = err.message || 'خطا در بارگذاری گزارش';
      console.error('Error loading report:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function saveCurrentReport(): Promise<boolean> {
    if (!hasActiveReport.value && !reportData.value.reportName) {
      error.value = 'لطفاً ابتدا اطلاعات گزارش را وارد کنید';
      return false;
    }
    
    isSaving.value = true;
    error.value = null;
    
    try {
      const targetStore = useTargetStore();
      const waterStore = useWaterStore();
      const calcStore = useCalcStore();
      
      const reportPayload = {
        report_name: reportData.value.reportName || `گزارش ${reportData.value.date}`,
        plant_name: reportData.value.plantName || '',
        season: reportData.value.season || '',
        growth_stage: reportData.value.growthStage || '',
        report_date: reportData.value.date || getCurrentShamsiDate()
      };
      
      let savedReport: any;
      
      if (currentReportId.value) {
        savedReport = await apiService.updateReport(String(currentReportId.value), reportPayload);
        console.log(`📝 Updating report ${currentReportId.value}`);
      } else {
        savedReport = await apiService.createReport(reportPayload);
        if (savedReport && savedReport.id) {
          currentReportId.value = savedReport.id;
          reportData.value.id = savedReport.id;
          console.log(`📝 Created new report with ID: ${currentReportId.value}`);
        }
      }
      
      if (!savedReport || !savedReport.id) {
        throw new Error('خطا در ذخیره گزارش');
      }
      
      const reportId = String(savedReport.id);
      
      // Water analysis
      if (waterStore.hasWaterData) {
        try {
          const waterPayload = {
            water_percentage: waterStore.waterMixData.waterPercentage,
            wastewater_percentage: waterStore.waterMixData.wastewaterPercentage,
            water_salinity: waterStore.waterMixData.waterSalinity,
            water_values: waterStore.waterValues,
            wastewater_values: waterStore.wastewaterValues
          };
          
          const existingWater = await apiService.getWaterAnalysis(reportId).catch(() => null);
          if (existingWater) {
            await apiService.updateWaterAnalysis(String(existingWater.id), waterPayload);
          } else {
            await apiService.createWaterAnalysis(reportId, waterPayload);
          }
        } catch (err) {
          console.warn('خطا در ذخیره آنالیز آب:', err);
        }
      }
      
      // Calculation data
      // 🆕 تنظیمات استوک (حجم مخزن اصلی، حجم سطل استوک، نسبت تزریق) داخل
      // reservoir_data ذخیره می‌شود تا این گزارش هنگام بازکردن مجدد کامل
      // برگردد (رفع باگ «این صفحه ناقص برمی‌گردد»).
      const reservoirDataWithSettings = {
        ...calcStore.reservoirData,
        settings: {
          tank_volume: calcStore.stockSettings.tankVolume,
          stock_volume: calcStore.stockSettings.stockVolume,
          injection_ratio: calcStore.stockSettings.injectionRatio
        }
      };

      const calcPayload = {
        target_values: targetStore.targetElements,
        final_values: calcStore.getFinalConcentrations(),
        reservoir_data: reservoirDataWithSettings,
        calc_rows: calcStore.calculationRows,
        interpretation: null
      };
      
      try {
        const existingCalc = await apiService.getCalculation(reportId).catch(() => null);
        if (existingCalc) {
          await apiService.updateCalculation(String(existingCalc.id), calcPayload);
        } else {
          await apiService.createCalculation(reportId, calcPayload);
        }
      } catch (err) {
        console.warn('خطا در ذخیره محاسبات:', err);
      }
      
      await loadReports();
      
      console.log('✅ Report saved successfully');
      return true;
      
    } catch (err: any) {
      error.value = err.message || 'خطا در ذخیره گزارش';
      console.error('Error saving report:', err);
      return false;
    } finally {
      isSaving.value = false;
    }
  }

  async function loadReports(): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await apiService.getReports();
      reports.value = Array.isArray(data) ? data : [];
      return true;
    } catch (err: any) {
      error.value = err.message || 'خطا در بارگذاری گزارش‌ها';
      console.error('Error loading reports:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteReport(reportId: number): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    try {
      await apiService.deleteReport(String(reportId));
      
      if (currentReportId.value === reportId) {
        createNewReport();
      }
      
      await loadReports();
      return true;
    } catch (err: any) {
      error.value = err.message || 'خطا در حذف گزارش';
      console.error('Error deleting report:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  function updateReportData(data: Partial<ReportData>) {
    reportData.value = {
      ...reportData.value,
      ...data
    };
  }

  function setCurrentReportId(id: number | null) {
    currentReportId.value = id;
    if (id === null) {
      reportData.value.id = null;
    }
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    currentReportId,
    reportData,
    reports,
    isLoading,
    error,
    isSaving,
    
    // Getters
    hasActiveReport,
    isReportComplete,
    reportSummary,
    
    // Actions
    createNewReport,
    loadReport,
    saveCurrentReport,
    loadReports,
    deleteReport,
    updateReportData,
    setCurrentReportId,
    clearError
  };
});

export default useReportStore;


