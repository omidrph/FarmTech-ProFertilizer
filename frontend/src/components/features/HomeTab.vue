<!-- frontend/src/components/features/HomeTab.vue -->
<!--
  ============================================================
  صفحه خانه (بازطراحی مینیمال)
  ------------------------------------------------------------
  فقط «وضعیت کلی» را نشان می‌دهد؛ جزئیات کامل در تب «محاسبه کود ← نتیجه» است.
  این فایل فقط منطق و داده را دارد؛ ظاهر هر حالت در پوشه‌ی home/ است.

  سه حالت:
    ۱) گزارشی باز نیست        ← گزارش‌های اخیر
    ۲) گزارش باز، بدون محاسبه ← کارت «گام بعدی»
    ۳) محاسبه انجام شده        ← کارت وضعیت + هشدارهای کوتاه
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
    <HomeNextStep
      v-else-if="!hasCalculatedData"
      :title="nextStep.title"
      :action-label="nextStep.action"
      :steps="progressSteps"
      @go="emit('navigate', nextStep.tab)"
    />

    <!-- ۳) نتیجه محاسبه: فقط وضعیت کلی -->
    <template v-else>
      <HomeStatusCard
        :tone="tone"
        :title="statusTitle"
        :ion-balanced="ionBalanced"
        :accuracy-text="accuracyText"
        :ec-text="ecText"
        :ec-out-of-range="ecOutOfRange"
        :cost-text="costText"
        :elements-count="activeElementsCount"
        :reservoirs-count="activeReservoirsCount"
        :fertilizers-count="fertilizerCount"
        @view-details="emit('navigate', 'fertilizer-calc')"
      />
      <HomeAttentionList :items="attentionItems" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { apiService } from '@/services/apiService';

import HomeRecentReports from './home/HomeRecentReports.vue';
import HomeNextStep from './home/HomeNextStep.vue';
import HomeStatusCard from './home/HomeStatusCard.vue';
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
// Computed: گام بعدی (وقتی هنوز محاسبه‌ای نیست)
// ============================================================
const hasTargets = computed(() =>
  Object.values(targetStore.targetElements || {}).some(value => Number(value) > 0)
);

const hasWater = computed(() =>
  Object.values(waterStore.waterValues || {}).some(value => Number(value) > 0)
);

const progressSteps = computed(() => [
  { key: 'targets', label: 'عناصر هدف', done: hasTargets.value },
  { key: 'water', label: 'آنالیز آب (اختیاری)', done: hasWater.value },
  { key: 'calc', label: 'محاسبه کود', done: hasCalculatedData.value }
]);

const nextStep = computed(() => {
  if (!hasTargets.value) {
    return { title: 'عناصر هدف را وارد کنید', action: 'عناصر هدف', tab: 'target-elements' };
  }
  return { title: 'آماده‌ی محاسبه کود هستید', action: 'محاسبه کود', tab: 'fertilizer-calc' };
});

// ============================================================
// Computed: وضعیت کلی نتیجه
// ============================================================
const result = computed(() => calcStore.optimizationResult);
const ionBalance = computed(() => targetStore.ionBalance);
const ionBalanced = computed(() => ionBalance.value?.isBalanced !== false);

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

const activeReservoirsCount = computed(() => {
  const data = calcStore.reservoirData;
  return (['A', 'B', 'C'] as const).filter(key => (data?.[key]?.length || 0) > 0).length;
});

const fertilizerCount = computed(() =>
  Object.values(result.value?.weights || {}).filter(value => Number(value) > 0).length
);

// ============================================================
// Computed: هشدارهای کوتاه (حداکثر ۳ مورد)
// ============================================================
const attentionItems = computed(() => {
  const items: Array<{ text: string; danger: boolean }> = [];

  if (!ionBalanced.value && ionBalance.value) {
    const diff = Math.abs(ionBalance.value.cation - ionBalance.value.anion);
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
  window.removeEventListener('report-changed', handleReportChanged);
  window.removeEventListener('report-reset', handleReportReset);
});
</script>
