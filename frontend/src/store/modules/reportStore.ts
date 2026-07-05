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

// ============================================================
// 🆕 ReportStore - بازطراحی کامل با معماری جدید
// ============================================================
export const useReportStore = defineStore('report', () => {
  // ===== State =====
  
  /** شناسه گزارش فعلی (null یعنی هیچ گزارشی فعال نیست) */
  const currentReportId = ref<number | null>(null);
  
  /** داده‌های گزارش فعلی */
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
  
  /** لیست همه گزارش‌های کاربر */
  const reports = ref<ReportListItem[]>([]);
  
  /** وضعیت بارگذاری */
  const isLoading = ref(false);
  
  /** خطا */
  const error = ref<string | null>(null);

  /** آیا در حال ذخیره‌سازی هستیم؟ */
  const isSaving = ref(false);

  // ===== Getters =====
  
  /** آیا گزارشی فعال است؟ */
  const hasActiveReport = computed(() => currentReportId.value !== null);
  
  /** آیا گزارش کامل است؟ */
  const isReportComplete = computed(() => {
    return !!(
      reportData.value.reportName &&
      reportData.value.plantName &&
      reportData.value.season &&
      reportData.value.growthStage
    );
  });
  
  /** خلاصه گزارش */
  const reportSummary = computed(() => {
    return `${reportData.value.reportName} - ${reportData.value.plantName} (${reportData.value.season})`;
  });

  // ===== Actions =====

  /**
   * 🆕 ایجاد یک گزارش جدید (خالی)
   * این تابع همه داده‌ها را ریست می‌کند و حالت جدید ایجاد می‌کند
   */
  function createNewReport(): void {
    console.log('📄 Creating new empty report...');
    
    // 1. Reset report data
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
    
    // 2. Clear current report ID
    currentReportId.value = null;
    
    // 3. Reset all dependent stores
    const targetStore = useTargetStore();
    const waterStore = useWaterStore();
    const calcStore = useCalcStore();
    
    targetStore.resetTargets();
    waterStore.resetWaterData();
    calcStore.resetCalculation();
    
    // 4. Dispatch event for UI update
    window.dispatchEvent(new CustomEvent('report-reset'));
    window.dispatchEvent(new CustomEvent('report-changed'));
    
    console.log('✅ New report created, all stores reset');
  }

  /**
   * 🆕 بارگذاری یک گزارش موجود
   */
  async function loadReport(reportId: number): Promise<boolean> {
    console.log(`📂 Loading report ${reportId}...`);
    
    isLoading.value = true;
    error.value = null;
    
    try {
      // 1. Reset all stores first (clean state)
      const targetStore = useTargetStore();
      const waterStore = useWaterStore();
      const calcStore = useCalcStore();
      
      targetStore.resetTargets();
      waterStore.resetWaterData();
      calcStore.resetCalculation();
      
      // 2. Fetch report data
      const report = await apiService.getReport(String(reportId));
      if (!report) {
        throw new Error('گزارش پیدا نشد');
      }
      
      // 3. Update report data
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
      
      // 4. Load water analysis
      try {
        const waterAnalysis = await apiService.getWaterAnalysis(String(reportId));
        if (waterAnalysis) {
          waterStore.loadFromAPI(waterAnalysis);
          console.log('💧 Water analysis loaded');
        }
      } catch (err) {
        console.log('ℹ️ No water analysis found for this report');
      }
      
      // 5. Load calculation data
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
          }
          
          console.log('🧮 Calculation data loaded');
        }
      } catch (err) {
        console.log('ℹ️ No calculation found for this report');
      }
      
      // 6. Dispatch event for UI update
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

  /**
   * 🆕 ذخیره گزارش فعلی
   */
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
      
      // 1. Prepare report payload
      const reportPayload = {
        report_name: reportData.value.reportName || `گزارش ${reportData.value.date}`,
        plant_name: reportData.value.plantName || '',
        season: reportData.value.season || '',
        growth_stage: reportData.value.growthStage || '',
        report_date: reportData.value.date || getCurrentShamsiDate()
      };
      
      let savedReport: any;
      
      // 2. Create or update report
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
      
      // 3. Save water analysis
      if (waterStore.hasWaterData.value) {
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
      
      // 4. Save calculation data
      const calcPayload = {
        target_values: targetStore.targetElements,
        final_values: calcStore.getFinalConcentrations(),
        reservoir_data: calcStore.reservoirData,
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
      
      // 5. Refresh reports list
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

  /**
   * بارگذاری لیست گزارش‌ها
   */
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

  /**
   * حذف یک گزارش
   */
  async function deleteReport(reportId: number): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    try {
      await apiService.deleteReport(String(reportId));
      
      // If current report was deleted, reset state
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

  /**
   * به‌روزرسانی داده‌های گزارش
   */
  function updateReportData(data: Partial<ReportData>) {
    reportData.value = {
      ...reportData.value,
      ...data
    };
  }

  /**
   * تنظیم شناسه گزارش فعلی
   */
  function setCurrentReportId(id: number | null) {
    currentReportId.value = id;
    if (id === null) {
      reportData.value.id = null;
    }
  }

  /**
   * پاک کردن خطا
   */
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