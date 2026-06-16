import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface ReportData {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  date: string;
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
  }

  function setDate(date: string) {
    reportData.value.date = date;
  }

  return {
    reportData,
    isReportComplete,
    reportSummary,
    updateReportData,
    resetReportData,
    setDate
  };
});