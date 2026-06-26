// frontend/src/store/modules/reportStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';
import { useWaterStore } from './waterStore';
import { useTargetStore } from './targetStore';
import { useCalcStore } from './calcStore';

interface ReportData {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  date: string;
}

interface Report {
  id: number;
  user_id: number;
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
  const reportData = ref<ReportData>({
    reportName: '',
    plantName: '',
    season: '',
    growthStage: '',
    date: getCurrentShamsiDate()
  });

  const currentReportId = ref<number | null>(null);
  const reports = ref<Report[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // ===== Getters =====
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

  const hasCurrentReport = computed(() => {
    return currentReportId.value !== null;
  });

  // ===== Actions =====
  function updateReportData(data: Partial<ReportData>) {
    reportData.value = {
      ...reportData.value,
      ...data
    };
  }

  function resetReportData() {
    reportData.value = {
      reportName: '',
      plantName: '',
      season: '',
      growthStage: '',
      date: getCurrentShamsiDate()
    };
    currentReportId.value = null;
  }

  function setDate(date: string) {
    reportData.value.date = date;
  }

  function setCurrentReportId(id: number | null) {
    currentReportId.value = id;
  }

  /**
   * 🆕 بارگذاری لیست گزارش‌های کاربر از API
   */
  async function loadReports(): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await apiService.getReports();
      if (data && Array.isArray(data)) {
        reports.value = data;
        return true;
      }
      return false;
    } catch (err: any) {
      error.value = err.message || 'خطا در بارگذاری گزارش‌ها';
      console.error('Error loading reports:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 🆕 ذخیره گزارش فعلی در دیتابیس
   * شامل تمام داده‌های مرتبط (آب، عناصر هدف، محاسبات)
   */
  async function saveCurrentReport(): Promise<boolean> {
    isLoading.value = true;
    error.value = null;

    try {
      const waterStore = useWaterStore();
      const targetStore = useTargetStore();
      const calcStore = useCalcStore();

      // 1. ذخیره یا به‌روزرسانی گزارش اصلی
      const reportPayload = {
        report_name: reportData.value.reportName || `گزارش ${reportData.value.date}`,
        plant_name: reportData.value.plantName,
        season: reportData.value.season,
        growth_stage: reportData.value.growthStage,
        report_date: reportData.value.date
      };

      let savedReport: any;

      if (currentReportId.value) {
        // به‌روزرسانی گزارش موجود
        savedReport = await apiService.updateReport(String(currentReportId.value), reportPayload);
      } else {
        // ایجاد گزارش جدید
        savedReport = await apiService.createReport(reportPayload);
        if (savedReport && savedReport.id) {
          currentReportId.value = savedReport.id;
        }
      }

      if (!savedReport || !savedReport.id) {
        throw new Error('خطا در ذخیره گزارش');
      }

      const reportId = String(savedReport.id);

      // 2. ذخیره آنالیز آب
      if (waterStore.waterMixData.waterSalinity > 0 || Object.keys(waterStore.waterValues).length > 0) {
        try {
          const existingWaterAnalysis = await apiService.getWaterAnalysis(reportId).catch(() => null);
          const waterPayload = {
            water_percentage: waterStore.waterMixData.waterPercentage,
            wastewater_percentage: waterStore.waterMixData.wastewaterPercentage,
            water_salinity: waterStore.waterMixData.waterSalinity,
            water_values: waterStore.waterValues,
            wastewater_values: waterStore.wastewaterValues
          };

          if (existingWaterAnalysis) {
            await apiService.updateWaterAnalysis(String(existingWaterAnalysis.id), waterPayload);
          } else {
            await apiService.createWaterAnalysis(reportId, waterPayload);
          }
        } catch (err) {
          console.warn('خطا در ذخیره آنالیز آب:', err);
        }
      }

      // 3. ذخیره محاسبات (عناصر هدف + نتایج)
      const targetKeys = Object.keys(targetStore.targetElements);
      const hasTargets = targetKeys.some(key => {
        const value = targetStore.targetElements[key as keyof typeof targetStore.targetElements];
        // اصلاح: بررسی نوع value قبل از مقایسه
        if (value === undefined || value === null) {
          return false;
        }
        if (typeof value === 'number') {
          return value > 0;
        }
        return false;
      });

      if (hasTargets || calcStore.calculationRows.length > 0) {
        try {
          // اطمینان از اینکه targetElements به درستی ذخیره می‌شود
          const targetValues: Record<string, number> = {};
          for (const [key, value] of Object.entries(targetStore.targetElements)) {
            // اصلاح: بررسی نوع value قبل از استفاده
            if (value === undefined || value === null) {
              continue;
            }
            if (typeof value === 'number' && value > 0) {
              targetValues[key] = value;
            }
          }

          const calcPayload = {
            target_values: targetValues,
            final_values: {},
            reservoir_data: calcStore.reservoirData,
            calc_rows: calcStore.calculationRows,
            interpretation: null
          };

          const existingCalc = await apiService.getCalculation(reportId).catch(() => null);
          if (existingCalc) {
            await apiService.updateCalculation(String(existingCalc.id), calcPayload);
          } else {
            await apiService.createCalculation(reportId, calcPayload);
          }
        } catch (err) {
          console.warn('خطا در ذخیره محاسبات:', err);
        }
      }

      // بارگذاری مجدد گزارش‌ها
      await loadReports();
      
      return true;
    } catch (err: any) {
      error.value = err.message || 'خطا در ذخیره گزارش';
      console.error('Error saving report:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 🆕 بارگذاری یک گزارش خاص و تمام داده‌های مرتبط آن
   */
  async function loadReport(reportId: number): Promise<boolean> {
    isLoading.value = true;
    error.value = null;

    try {
      const waterStore = useWaterStore();
      const targetStore = useTargetStore();
      const calcStore = useCalcStore();

      // 1. بارگذاری گزارش اصلی
      const report = await apiService.getReport(String(reportId));
      if (!report) {
        throw new Error('گزارش پیدا نشد');
      }

      // به‌روزرسانی reportData
      reportData.value = {
        reportName: report.report_name || '',
        plantName: report.plant_name || '',
        season: report.season || '',
        growthStage: report.growth_stage || '',
        date: report.report_date || getCurrentShamsiDate()
      };
      currentReportId.value = report.id;

      // 2. بارگذاری آنالیز آب
      try {
        const waterAnalysis = await apiService.getWaterAnalysis(String(reportId));
        if (waterAnalysis) {
          waterStore.setWaterMix({
            waterPercentage: waterAnalysis.water_percentage,
            wastewaterPercentage: waterAnalysis.wastewater_percentage,
            waterSalinity: waterAnalysis.water_salinity
          });
          if (waterAnalysis.water_values) {
            for (const [key, value] of Object.entries(waterAnalysis.water_values)) {
              waterStore.setWaterValue(key, value as number);
            }
          }
          if (waterAnalysis.wastewater_values) {
            for (const [key, value] of Object.entries(waterAnalysis.wastewater_values)) {
              waterStore.setWastewaterValue(key, value as number);
            }
          }
        }
      } catch (err) {
        console.warn('آنالیز آب برای این گزارش وجود ندارد');
      }

      // 3. بارگذاری محاسبات
      try {
        const calculation = await apiService.getCalculation(String(reportId));
        if (calculation) {
          // ===== اصلاح: اطمینان از اینکه target_values به درستی در targetStore قرار می‌گیرد =====
          if (calculation.target_values) {
            let targetValues = calculation.target_values;
            
            // اگر target_values رشته JSON است، آن را تبدیل کن
            if (typeof targetValues === 'string') {
              try {
                targetValues = JSON.parse(targetValues);
              } catch (e) {
                console.error('Error parsing target_values JSON:', e);
                targetValues = {};
              }
            }
            
            // اگر target_values دیکشنری است، آن را در targetStore قرار بده
            if (typeof targetValues === 'object' && targetValues !== null) {
              console.log('Loading target_values into store:', targetValues);
              for (const [key, value] of Object.entries(targetValues)) {
                // اصلاح: بررسی نوع value قبل از استفاده
                if (value === undefined || value === null) {
                  continue;
                }
                if (typeof value === 'number' && value > 0) {
                  targetStore.setTargetElement(key as any, value as number);
                }
              }
            } else {
              console.warn('target_values is not an object:', typeof targetValues);
            }
          } else {
            console.warn('calculation.target_values is null or undefined');
          }
          
          // بارگذاری calc_rows
          if (calculation.calc_rows && Array.isArray(calculation.calc_rows)) {
            calcStore.calculationRows = calculation.calc_rows;
          }
          
          // بارگذاری reservoir_data
          if (calculation.reservoir_data) {
            let reservoirData = calculation.reservoir_data;
            if (typeof reservoirData === 'string') {
              try {
                reservoirData = JSON.parse(reservoirData);
              } catch (e) {
                console.error('Error parsing reservoir_data JSON:', e);
                reservoirData = { A: [], B: [], C: [] };
              }
            }
            calcStore.reservoirData = reservoirData;
          }
        } else {
          console.warn('No calculation found for report:', reportId);
        }
      } catch (err) {
        console.warn('محاسبات برای این گزارش وجود ندارد:', err);
      }

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
   * 🆕 حذف گزارش فعلی
   */
  async function deleteCurrentReport(): Promise<boolean> {
    if (!currentReportId.value) {
      error.value = 'هیچ گزارشی برای حذف وجود ندارد';
      return false;
    }

    isLoading.value = true;
    error.value = null;

    try {
      await apiService.deleteReport(String(currentReportId.value));
      resetReportData();
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
   * 🆕 حذف یک گزارش خاص
   */
  async function deleteReport(reportId: number): Promise<boolean> {
    isLoading.value = true;
    error.value = null;

    try {
      await apiService.deleteReport(String(reportId));
      if (currentReportId.value === reportId) {
        resetReportData();
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

  function clearError() {
    error.value = null;
  }

  return {
    // State
    reportData,
    currentReportId,
    reports,
    isLoading,
    error,
    // Getters
    isReportComplete,
    reportSummary,
    hasCurrentReport,
    // Actions
    updateReportData,
    resetReportData,
    setDate,
    setCurrentReportId,
    loadReports,
    saveCurrentReport,
    loadReport,
    deleteCurrentReport,
    deleteReport,
    clearError
  };
});

export default useReportStore;