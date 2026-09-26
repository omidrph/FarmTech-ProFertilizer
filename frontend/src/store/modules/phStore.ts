// frontend/src/store/modules/phStore.ts
// ============================================================
// استور تب «PH» (ماشین‌حساب pH)
// ------------------------------------------------------------
// این تب عمداً خارج از چرخه‌ی رسمی محاسبه‌ی کود است (calcStore) اما
// از پایگاه‌داده‌ی کود واقعی (اسیدها) و به‌صورت اطلاعاتی از آنالیز آب
// و عناصر هدف گزارش جاری می‌خواند، و تاریخچه‌ی محاسبات خودش را
// جداگانه ذخیره می‌کند. تمام محاسبات شیمیایی در بک‌اند (پایتون) انجام
// می‌شود؛ این استور فقط state و فراخوانی API است.
// ============================================================
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';
import type {
  PhAcidOption,
  PhContextResponse,
  PhDoseResponse,
  PhHistoryItem,
  PhMonitoringRequest,
  PhTheoreticalRequest,
  PhTitrationRequest
} from '@/services/apiService';
import { useReportStore } from './reportStore';

export const usePhStore = defineStore('ph', () => {
  // ===== State =====
  const acidOptions = ref<PhAcidOption[]>([]);
  const context = ref<PhContextResponse | null>(null);
  const history = ref<PhHistoryItem[]>([]);
  const result = ref<PhDoseResponse | null>(null);

  const isLoadingAcids = ref(false);
  const isLoadingContext = ref(false);
  const isCalculating = ref(false);
  const isLoadingHistory = ref(false);

  const errorMessage = ref<string>('');
  const needTitrationHint = ref(false);

  // 🆕 پایش سریع (بدون محاسبه‌ی دوز) - برای سیستم‌های بازچرخشی
  const isLoggingMonitoring = ref(false);
  const monitoringError = ref<string>('');

  // ===== Getters =====
  const hasAcidOptions = computed(() => acidOptions.value.length > 0);

  // ===== Actions =====
  async function loadAcidOptions(): Promise<void> {
    isLoadingAcids.value = true;
    try {
      acidOptions.value = await apiService.getPhAcidOptions();
    } catch (e) {
      console.error('خطا در دریافت لیست اسیدها:', e);
      acidOptions.value = [];
    } finally {
      isLoadingAcids.value = false;
    }
  }

  async function loadContext(): Promise<void> {
    const reportStore = useReportStore();
    isLoadingContext.value = true;
    try {
      context.value = await apiService.getPhContext(reportStore.currentReportId ?? undefined);
    } catch (e) {
      console.error('خطا در دریافت داده‌ی زمینه:', e);
      context.value = null;
    } finally {
      isLoadingContext.value = false;
    }
  }

  function extractError(e: any): { message: string; needTitration: boolean } {
    const detail = e?.response?.data?.detail;
    if (detail && typeof detail === 'object' && 'error' in detail) {
      return { message: detail.error, needTitration: !!detail.need_titration };
    }
    if (typeof detail === 'string') return { message: detail, needTitration: false };
    return { message: 'خطا در محاسبه. ورودی‌ها را بررسی کنید.', needTitration: false };
  }

  async function calculateTheoretical(payload: PhTheoreticalRequest): Promise<boolean> {
    isCalculating.value = true;
    errorMessage.value = '';
    needTitrationHint.value = false;
    try {
      result.value = await apiService.calculatePhTheoretical(payload);
      if (payload.save) await loadHistory();
      return true;
    } catch (e) {
      const { message, needTitration } = extractError(e);
      errorMessage.value = message;
      needTitrationHint.value = needTitration;
      result.value = null;
      return false;
    } finally {
      isCalculating.value = false;
    }
  }

  async function calculateTitration(payload: PhTitrationRequest): Promise<boolean> {
    isCalculating.value = true;
    errorMessage.value = '';
    needTitrationHint.value = false;
    try {
      result.value = await apiService.calculatePhTitration(payload);
      if (payload.save) await loadHistory();
      return true;
    } catch (e) {
      const { message, needTitration } = extractError(e);
      errorMessage.value = message;
      needTitrationHint.value = needTitration;
      result.value = null;
      return false;
    } finally {
      isCalculating.value = false;
    }
  }

  async function loadHistory(): Promise<void> {
    const reportStore = useReportStore();
    isLoadingHistory.value = true;
    try {
      history.value = await apiService.getPhHistory(reportStore.currentReportId ?? undefined);
    } catch (e) {
      console.error('خطا در دریافت تاریخچه:', e);
    } finally {
      isLoadingHistory.value = false;
    }
  }

  // 🆕 ثبت سریع یک اندازه‌گیری (pH/EC) بدون محاسبه‌ی دوز - برای پایش روزانه‌ی سیستم بازچرخشی
  async function logMonitoring(ph: number, ecMsCm?: number | null, note?: string | null): Promise<boolean> {
    const reportStore = useReportStore();
    if (!reportStore.currentReportId) {
      monitoringError.value = 'برای ثبت پایش، ابتدا یک گزارش فعال لازم است.';
      return false;
    }
    isLoggingMonitoring.value = true;
    monitoringError.value = '';
    try {
      const payload: PhMonitoringRequest = {
        report_id: reportStore.currentReportId,
        ph,
        ec_ms_cm: ecMsCm ?? undefined,
        note: note ?? undefined
      };
      await apiService.savePhMonitoring(payload);
      await loadHistory();
      return true;
    } catch (e: any) {
      monitoringError.value = e?.response?.data?.detail || 'ثبت اندازه‌گیری با خطا مواجه شد.';
      return false;
    } finally {
      isLoggingMonitoring.value = false;
    }
  }

  async function deleteHistoryItem(id: number): Promise<void> {
    await apiService.deletePhHistoryItem(id);
    history.value = history.value.filter(h => h.id !== id);
  }

  function clearResult(): void {
    result.value = null;
    errorMessage.value = '';
    needTitrationHint.value = false;
  }

  return {
    // state
    acidOptions,
    context,
    history,
    result,
    isLoadingAcids,
    isLoadingContext,
    isCalculating,
    isLoadingHistory,
    errorMessage,
    needTitrationHint,
    isLoggingMonitoring,
    monitoringError,
    // getters
    hasAcidOptions,
    // actions
    loadAcidOptions,
    loadContext,
    calculateTheoretical,
    calculateTitration,
    loadHistory,
    logMonitoring,
    deleteHistoryItem,
    clearResult
  };
});
