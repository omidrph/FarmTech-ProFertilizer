// frontend/src/store/modules/phStore.ts
// ============================================================
// استور تب «PH» (اصلاح pH با اسید/باز)
// ------------------------------------------------------------
// همهٔ محاسبات در بک‌اند انجام می‌شود؛ این استور فقط وضعیت UI و
// ارتباط با API را نگه می‌دارد:
//   • adjusters : اسید/بازهای پایگاه‌داده‌ی کود خود کاربر
//   • context   : حجم مخزن، pH/آلکالینیتی آب، EC پایه، اصلاح فعال گزارش
//   • result    : نتیجهٔ آخرین محاسبه (preview)
//   • history   : تاریخچهٔ اصلاح‌های ثبت‌شدهٔ گزارش
// ============================================================
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {
  apiService,
  type PhAdjusterOption,
  type PhAdjustmentItem,
  type PhAdjustmentRequest,
  type PhAdjustmentResult,
  type PhAdjustmentSaveRequest,
  type PhContextResponse
} from '@/services/apiService';
import { useReportStore } from './reportStore';

function errorText(err: any, fallback: string): string {
  const detail = err?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail) && detail.length) {
    // خطاهای اعتبارسنجی Pydantic: «Value error, ...» → فقط متن فارسی
    const first = detail[0];
    const msg = typeof first?.msg === 'string' ? first.msg : '';
    return msg.replace(/^Value error,\s*/i, '') || fallback;
  }
  return err?.message || fallback;
}

export const usePhStore = defineStore('ph', () => {
  const adjusters = ref<PhAdjusterOption[]>([]);
  const context = ref<PhContextResponse | null>(null);
  const result = ref<PhAdjustmentResult | null>(null);
  const history = ref<PhAdjustmentItem[]>([]);

  const isLoadingAdjusters = ref(false);
  const isCalculating = ref(false);
  const isSaving = ref(false);
  const errorMessage = ref<string | null>(null);

  const activeItem = computed(() => history.value.find((h) => h.is_active) || null);

  async function loadAdjusters(): Promise<void> {
    isLoadingAdjusters.value = true;
    try {
      adjusters.value = await apiService.getPhAdjusters();
    } catch (err) {
      adjusters.value = [];
      errorMessage.value = errorText(err, 'خطا در دریافت اسید/بازهای پایگاه‌داده کود');
    } finally {
      isLoadingAdjusters.value = false;
    }
  }

  async function loadContext(): Promise<void> {
    const reportId = useReportStore().currentReportId;
    try {
      context.value = await apiService.getPhContext(reportId ?? undefined);
    } catch {
      context.value = null;
    }
  }

  async function loadHistory(): Promise<void> {
    const reportId = useReportStore().currentReportId;
    if (!reportId) {
      history.value = [];
      return;
    }
    try {
      history.value = await apiService.getPhAdjustments(reportId);
    } catch {
      history.value = [];
    }
  }

  async function refreshAll(): Promise<void> {
    await Promise.all([loadAdjusters(), loadContext(), loadHistory()]);
  }

  async function calculate(payload: PhAdjustmentRequest): Promise<boolean> {
    isCalculating.value = true;
    errorMessage.value = null;
    try {
      const reportId = useReportStore().currentReportId;
      result.value = await apiService.previewPhAdjustment({ ...payload, report_id: reportId ?? null });
      return true;
    } catch (err: any) {
      result.value = null;
      errorMessage.value = errorText(err, 'خطا در محاسبه');
      return false;
    } finally {
      isCalculating.value = false;
    }
  }

  async function save(payload: Omit<PhAdjustmentSaveRequest, 'report_id'>): Promise<PhAdjustmentItem | null> {
    const reportId = useReportStore().currentReportId;
    if (!reportId) {
      errorMessage.value = 'برای ثبت، ابتدا یک گزارش باز یا ذخیره کنید.';
      return null;
    }
    isSaving.value = true;
    errorMessage.value = null;
    try {
      const item = await apiService.savePhAdjustment({ ...payload, report_id: reportId });
      await Promise.all([loadHistory(), loadContext()]);
      return item;
    } catch (err: any) {
      errorMessage.value = errorText(err, 'خطا در ثبت');
      return null;
    } finally {
      isSaving.value = false;
    }
  }

  async function setApplied(id: number, applied: boolean): Promise<boolean> {
    try {
      if (applied) await apiService.applyPhAdjustment(id);
      else await apiService.unapplyPhAdjustment(id);
      await Promise.all([loadHistory(), loadContext()]);
      return true;
    } catch (err: any) {
      errorMessage.value = errorText(err, 'خطا در تغییر وضعیت اعمال');
      return false;
    }
  }

  async function remove(id: number): Promise<boolean> {
    try {
      await apiService.deletePhAdjustment(id);
      await Promise.all([loadHistory(), loadContext()]);
      return true;
    } catch (err: any) {
      errorMessage.value = errorText(err, 'خطا در حذف');
      return false;
    }
  }

  function clearResult() {
    result.value = null;
    errorMessage.value = null;
  }

  function reset() {
    result.value = null;
    history.value = [];
    context.value = null;
    errorMessage.value = null;
  }

  return {
    adjusters, context, result, history, activeItem,
    isLoadingAdjusters, isCalculating, isSaving, errorMessage,
    loadAdjusters, loadContext, loadHistory, refreshAll,
    calculate, save, setApplied, remove, clearResult, reset
  };
});
