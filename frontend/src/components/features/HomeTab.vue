<!-- frontend/src/components/features/HomeTab.vue -->
<!--
  ============================================================
  صفحه خانه (داشبورد وضعیت)
  ------------------------------------------------------------
  فقط «وضعیت کلی» را نشان می‌دهد؛ جزئیات کامل در تب «محاسبه کود ← نتیجه» است.
  این فایل فقط منطق و داده را دارد؛ ظاهر هر حالت در پوشه‌ی home/ است.

  سه حالت:
    ۱) گزارشی باز نیست        ← گزارش‌های اخیر
    ۲) گزارش باز، بدون محاسبه ← کارت «گام بعدی»
    ۳) محاسبه انجام شده        ← داشبورد: کارت اصلی با نمودار دایره‌ای، حلقه‌های عناصر،
                                 تعادل یونی، مخازن، هشدارها و اقدام‌های سریع
  ============================================================
-->
<template>
  <div class="space-y-3 sm:space-y-4">

    <!-- در حال بارگذاری -->
    <div
      v-if="isLoading"
      class="flex items-center justify-center gap-2 py-6 text-sm text-gray-500 dark:text-gray-400"
    >
      <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
      <span>در حال بارگذاری وضعیت...</span>
    </div>

    <!-- خطا -->
    <div
      v-else-if="error"
      class="flex items-center justify-between gap-3 rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 px-4 py-3"
    >
      <p class="text-sm text-rose-700 dark:text-rose-400">{{ error }}</p>
      <button
        type="button"
        @click="loadDashboardData"
        class="flex-shrink-0 text-sm font-medium text-rose-700 dark:text-rose-300 hover:underline"
      >
        تلاش مجدد
      </button>
    </div>

    <!-- ۱) گزارشی باز نیست -->
    <HomeRecentReports
      v-else-if="!hasActiveReport"
      :reports="recentReports"
      @open="openReport"
    />

    <!-- ۲) گزارش باز است ولی هنوز محاسبه نشده -->
    <HomeSteps
      v-else-if="!hasCalculatedData"
      :steps="steps"
      :current-key="currentStepKey"
      @go="goToStep"
      @skip="skipStep"
    />

    <!-- ۳) نتیجه محاسبه: داشبورد وضعیت -->
    <template v-else>
      <HomeHeroCard
        :tone="tone"
        :title="statusTitle"
        :subtitle="statusSubtitle"
        :accuracy="accuracy"
        :accuracy-text="accuracyText"
        :ec-text="ecText"
        :ec-out-of-range="ecOutOfRange"
        :cost-text="costText"
        :fertilizers-count="fertilizerCount"
        :is-exporting="isExporting"
        @view-details="emit('navigate', 'fertilizer-calc')"
        @export-pdf="handleExportPdf"
      />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 sm:gap-4">
        <HomeElementRings
          class="lg:col-span-2"
          :target-values="(targetStore.targetElements as Record<string, number>)"
          :concentrations="result?.concentrations || {}"
        />
        <div class="space-y-3 sm:space-y-4">
          <HomeIonBalance
            :cation="Number(ionSource?.cation) || 0"
            :anion="Number(ionSource?.anion) || 0"
            :balanced="ionBalanced"
          />
          <HomeReservoirs :counts="reservoirCounts" />
        </div>
      </div>

      <div class="flex flex-col sm:flex-row sm:items-start gap-3">
        <HomeAttentionList class="flex-1" :items="attentionItems" />
        <HomeQuickActions
          class="sm:mr-auto"
          @recalculate="emit('navigate', 'fertilizer-calc')"
          @edit-targets="emit('navigate', 'target-elements')"
        />
      </div>

      <!-- پیام کوتاه (مثلاً بعد از ساخت PDF) -->
      <Transition name="home-toast">
        <div
          v-if="toastMessage"
          class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[200] px-4 py-2.5 rounded-lg text-sm text-white shadow-lg max-w-[90vw]"
          :class="toastType === 'error' ? 'bg-rose-600' : 'bg-emerald-600'"
        >
          {{ toastMessage }}
        </div>
      </Transition>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';
import { apiService } from '@/services/apiService';
import { usePdfExport } from '@/composables/usePdfExport';

import HomeRecentReports from './home/HomeRecentReports.vue';
import HomeSteps from './home/HomeSteps.vue';
import type { HomeStepItem } from './home/HomeSteps.vue';
import HomeHeroCard from './home/HomeHeroCard.vue';
import HomeElementRings from './home/HomeElementRings.vue';
import HomeIonBalance from './home/HomeIonBalance.vue';
import HomeReservoirs from './home/HomeReservoirs.vue';
import HomeQuickActions from './home/HomeQuickActions.vue';
import HomeAttentionList from './home/HomeAttentionList.vue';

// ============================================================
// Emits
// ============================================================
const emit = defineEmits<{
  (e: 'navigate', tab: string): void;
}>();

// ============================================================
// Stores
// ============================================================
const reportStore = useReportStore();
const targetStore = useTargetStore();
const waterStore = useWaterStore();
const calcStore = useCalcStore();
const fertilizerStore = useFertilizerStore();

// ============================================================
// State
// ============================================================
const isLoading = ref(false);
const error = ref<string | null>(null);

// ============================================================
// Computed: وضعیت گزارش
// ============================================================
const hasActiveReport = computed(() => reportStore.hasActiveReport);

// فقط بعد از یک محاسبه‌ی واقعی (دکمه «محاسبه») وضعیت کلی نمایش داده می‌شود
const hasCalculatedData = computed(() => calcStore.optimizationResult !== null);

const recentReports = computed(() => (reportStore.reports || []).slice(0, 3));

const openReport = (id: number) => {
  reportStore.loadReport(id);
};

// ============================================================
// Computed: مراحل محاسبه کود (وقتی هنوز محاسبه‌ای نیست)
// ============================================================
const hasTargets = computed(() =>
  Object.values(targetStore.targetElements || {}).some(value => Number(value) > 0)
);

const hasWater = computed(() =>
  Object.values(waterStore.waterValues || {}).some(value => Number(value) > 0)
);

const userFertilizersCount = computed(
  () => (fertilizerStore.fertilizers || []).filter((f: any) => !f.isSystemDefault).length
);

// «رد کردن» مرحله‌ی اختیاری آنالیز آب؛ برای هر گزارش جداگانه و در همین نشست مرورگر نگه داشته می‌شود
const waterSkipKey = () => `farmtech_water_step_skipped_${reportStore.currentReportId ?? 'none'}`;
const readWaterSkipped = (): boolean => {
  try {
    return sessionStorage.getItem(waterSkipKey()) === '1';
  } catch {
    return false;
  }
};
const waterSkipped = ref(readWaterSkipped());

watch(
  () => reportStore.currentReportId,
  () => {
    waterSkipped.value = readWaterSkipped();
  }
);

const stockHint = computed(() => {
  const s = calcStore.stockSettings;
  return `مخزن ${s.tankVolume.toLocaleString('fa-IR')} لیتر • استوک ${s.stockVolume.toLocaleString('fa-IR')} لیتر • نسبت ۱:${s.injectionRatio.toLocaleString('fa-IR')}`;
});

const steps = computed<HomeStepItem[]>(() => [
  {
    key: 'target-elements',
    title: 'عناصر هدف',
    status: hasTargets.value ? 'done' : 'pending',
    hint: hasTargets.value
      ? `${activeElementsCount.value.toLocaleString('fa-IR')} عنصر ثبت شده است`
      : 'مقدار عناصر مورد نیاز گیاه را وارد کنید',
    actionLabel: 'ورود عناصر هدف'
  },
  {
    key: 'water-analysis',
    title: 'آنالیز آب',
    optional: true,
    status: hasWater.value ? 'done' : waterSkipped.value ? 'skipped' : 'pending',
    hint: hasWater.value
      ? 'ثبت شده است'
      : waterSkipped.value
        ? 'رد شد؛ هر زمان خواستید می‌توانید ثبتش کنید'
        : 'دقت محاسبه را بالا می‌برد',
    actionLabel: 'ثبت آنالیز آب'
  },
  {
    key: 'fertilizer-db',
    title: 'پایگاه‌داده کود',
    status: userFertilizersCount.value > 0 ? 'done' : 'pending',
    hint: userFertilizersCount.value > 0
      ? `${userFertilizersCount.value.toLocaleString('fa-IR')} کود ثبت شده است`
      : 'حداقل یک کود اضافه کنید تا برای انتخاب در دسترس باشد',
    actionLabel: 'افزودن کود'
  },
  {
    key: 'fertilizer-calc',
    title: 'تنظیمات استوک و محاسبه',
    status: hasCalculatedData.value ? 'done' : 'pending',
    hint: stockHint.value,
    actionLabel: 'تنظیم و محاسبه'
  }
]);

// مرحله‌ی جاری: اولین مرحله‌ای که نه انجام شده و نه رد شده است
const currentStepKey = computed<string | null>(
  () => steps.value.find(step => step.status === 'pending')?.key ?? null
);

const goToStep = (key: string) => {
  emit('navigate', key);
};

const skipStep = (key: string) => {
  if (key !== 'water-analysis') return;
  waterSkipped.value = true;
  try {
    sessionStorage.setItem(waterSkipKey(), '1');
  } catch {
    // در حالت خصوصی مرورگر ممکن است ذخیره‌سازی در دسترس نباشد؛ فقط در حافظه می‌ماند
  }
};

// ============================================================
// Computed: وضعیت کلی نتیجه
// ============================================================
const result = computed(() => calcStore.optimizationResult);
// تعادل یونی خودِ فرمول (از نتیجه‌ی محاسبه)؛ اگر نبود، از تعادل عناصر هدف
const ionSource = computed(() => {
  const fromResult = result.value?.ion_balance;
  if (fromResult && (Number(fromResult.cation) > 0 || Number(fromResult.anion) > 0)) return fromResult;
  return targetStore.ionBalance;
});
const ionBalanced = computed(() => ionSource.value?.isBalanced !== false);

const accuracy = computed(() => {
  const values = Object.values(result.value?.target_achievement || {});
  if (!values.length) return 0;
  const avg = values.reduce((sum, v) => sum + (Number(v) || 0), 0) / values.length;
  return Math.max(0, Math.min(100, avg));
});

const ec = computed(() => Math.max(0, Number(result.value?.ec) || 0));
const ecOutOfRange = computed(() => ec.value < 0.8 || ec.value > 3.5);

const tone = computed<'good' | 'warn' | 'bad'>(() => {
  if (accuracy.value >= 95 && ionBalanced.value && !ecOutOfRange.value) return 'good';
  if (accuracy.value >= 85) return 'warn';
  return 'bad';
});

const statusTitle = computed(() => {
  if (tone.value === 'good') return 'فرمول آماده است';
  if (tone.value === 'warn') return 'فرمول نیازمند بررسی است';
  return 'فرمول نیازمند اصلاح است';
});

const statusSubtitle = computed(
  () =>
    `${ionBalanced.value ? 'تعادل یونی مطلوب' : 'عدم تعادل یونی'} · ${
      result.value?.is_converged === false ? 'محاسبه همگرا نشد' : 'محاسبه همگرا شد'
    }`
);

const accuracyText = computed(() =>
  accuracy.value.toLocaleString('fa-IR', { maximumFractionDigits: 1 })
);
const ecText = computed(() =>
  ec.value.toLocaleString('fa-IR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
);
const costText = computed(() => Math.round(calcStore.totalCost || 0).toLocaleString('fa-IR'));

const activeElementsCount = computed(() =>
  Object.values(targetStore.targetElements || {}).filter(v => Number(v) > 0).length
);

const reservoirCounts = computed(() => {
  const data = calcStore.reservoirData;
  return { A: data?.A?.length || 0, B: data?.B?.length || 0, C: data?.C?.length || 0 };
});

const fertilizerCount = computed(() =>
  Object.values(result.value?.weights || {}).filter(value => Number(value) > 0).length
);

// ============================================================
// Computed: هشدارهای کوتاه (حداکثر ۳ مورد)
// ============================================================
const attentionItems = computed(() => {
  const items: Array<{ text: string; danger: boolean }> = [];

  if (!ionBalanced.value && ionSource.value) {
    const diff = Math.abs(ionSource.value.cation - ionSource.value.anion);
    items.push({
      text: `اختلاف کاتیون و آنیون ${diff.toLocaleString('fa-IR', { maximumFractionDigits: 2 })} meq/L است`,
      danger: true
    });
  }

  const actual = (result.value?.concentrations || {}) as Record<string, number>;
  const targets = targetStore.targetElements as Record<string, number>;
  const deficient: string[] = [];
  const excessive: string[] = [];

  for (const [element, target] of Object.entries(targets)) {
    if (!(Number(target) > 0)) continue;
    const ratio = ((Number(actual[element]) || 0) / Number(target)) * 100;
    if (ratio < 70) deficient.push(element);
    else if (ratio > 130) excessive.push(element);
  }

  if (deficient.length) {
    items.push({
      text: `${deficient.slice(0, 3).join('، ')}${deficient.length > 3 ? ' و ...' : ''} کمتر از ۷۰٪ هدف است`,
      danger: false
    });
  }
  if (excessive.length) {
    items.push({
      text: `${excessive.slice(0, 3).join('، ')}${excessive.length > 3 ? ' و ...' : ''} بیشتر از ۱۳۰٪ هدف است`,
      danger: false
    });
  }

  if (ec.value > 3.5) {
    items.push({ text: `EC بسیار بالا است (${ecText.value} dS/m)؛ خطر شوری`, danger: true });
  } else if (ec.value < 0.8) {
    items.push({ text: `EC پایین است (${ecText.value} dS/m)`, danger: false });
  }

  return items.slice(0, 3);
});

// ============================================================
// خروجی PDF و پیام کوتاه
// ============================================================
const { exportOptimizationPdf, isExporting } = usePdfExport();

const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');
let toastTimer: ReturnType<typeof setTimeout> | null = null;

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastMessage.value = null;
  }, 3500);
};

const handleExportPdf = async () => {
  if (!calcStore.optimizationResult) {
    showToast('ابتدا محاسبه را انجام دهید', 'error');
    return;
  }

  try {
    const report: any = (reportStore as any).reportData || {};
    await exportOptimizationPdf({
      result: calcStore.optimizationResult,
      fertilizers: fertilizerStore.fertilizers,
      targetValues: targetStore.targetElements as Record<string, number>,
      meta: {
        reportName: report.reportName,
        plantName: report.plantName,
        season: report.season,
        tankVolume: calcStore.stockSettings.tankVolume,
        stockVolume: calcStore.stockSettings.stockVolume,
        injectionRatio: calcStore.stockSettings.injectionRatio
      }
    });
    showToast('فایل PDF آماده شد؛ در پنجره چاپ گزینه Save as PDF را انتخاب کنید', 'success');
  } catch (err: any) {
    showToast(err?.message || 'خطا در ساخت خروجی PDF', 'error');
  }
};

// ============================================================
// Methods
// ============================================================
const loadDashboardData = async () => {
  if (!hasActiveReport.value) {
    isLoading.value = false;
    return;
  }

  isLoading.value = true;
  error.value = null;

  try {
    await targetStore.calculateIonBalanceFromAPI();

    if (Object.keys(waterStore.waterValues).length === 0) {
      try {
        const waterData = await apiService.getWaterAnalysis(String(reportStore.currentReportId));
        if (waterData) waterStore.loadFromAPI(waterData);
      } catch {
        // آنالیز آب اختیاری است؛ نبودنش خطا نیست
      }
    }
  } catch (err: any) {
    error.value = err?.message || 'خطا در بارگذاری داده‌ها';
    console.error('Error loading dashboard data:', err);
  } finally {
    isLoading.value = false;
  }
};

// ============================================================
// Watch & Event Listeners
// ============================================================
watch(
  () => reportStore.currentReportId,
  newId => {
    if (newId === null) {
      isLoading.value = false;
      error.value = null;
    } else {
      loadDashboardData();
    }
  },
  { immediate: true }
);

const handleReportChanged = () => {
  loadDashboardData();
};

const handleReportReset = () => {
  isLoading.value = false;
  error.value = null;
};

onMounted(() => {
  loadDashboardData();
  window.addEventListener('report-changed', handleReportChanged);
  window.addEventListener('report-reset', handleReportReset);
});

onUnmounted(() => {
  if (toastTimer) clearTimeout(toastTimer);
  window.removeEventListener('report-changed', handleReportChanged);
  window.removeEventListener('report-reset', handleReportReset);
});
</script>

<style scoped>
.home-toast-enter-active,
.home-toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.home-toast-enter-from,
.home-toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 8px);
}
</style>
