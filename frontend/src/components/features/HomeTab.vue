
<!-- frontend/src/components/features/HomeTab.vue -->
<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- Loading State -->
    <HomeEmptyState v-if="isLoading" type="loading" />

    <!-- Error State -->
    <HomeEmptyState 
      v-else-if="error" 
      type="error" 
      :message="error"
      @retry="loadDashboardData"
    />

    <!-- Empty State - No Report: خودِ ReportHeader بزرگ در MainLayout آموزش لازم را نشان می‌دهد -->

    <!-- گزارش هست ولی هنوز محاسبه نشده: چک‌لیست + گزارش‌های اخیر -->
    <template v-else-if="hasActiveReport && !hasCalculatedData">
      <HomeEmptyState type="no-data" />
      <div v-if="recentReports.length > 0" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 mt-4">
        <p class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">گزارش‌های اخیر</p>
        <div class="space-y-1.5">
          <button
            v-for="r in recentReports"
            :key="r.id"
            type="button"
            @click="openReport(r.id)"
            class="w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-right hover:bg-gray-50 dark:hover:bg-gray-700/40 transition-colors"
          >
            <span class="text-sm text-gray-700 dark:text-gray-200 truncate">{{ r.report_name || 'بدون نام' }}</span>
            <span class="text-[11px] text-gray-400 flex-shrink-0">{{ r.plant_name || '' }}</span>
          </button>
        </div>
      </div>
    </template>

    <!-- Full Dashboard: سامری بالا، جزئیات داخل آکاردئون جمع‌شده -->
    <template v-else-if="hasCalculatedData">
      <!-- 🆕 خلاصه دایره‌ای (همیشه باز، اولویت اول) -->
      <HomeSummaryGauges
        :target-achievement="calcStore.optimizationResult?.target_achievement || {}"
        :ec="calcStore.optimizationResult?.ec || 0"
        :total-cost="totalCost"
      />

      <!-- 🆕 خط خلاصه گزارش -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center justify-between gap-2 flex-wrap">
        <span class="text-sm text-gray-700 dark:text-gray-200 truncate">
          {{ reportStore.reportData.reportName || 'بدون نام' }}
          <span v-if="reportStore.reportData.plantName" class="text-gray-400"> • {{ reportStore.reportData.plantName }}</span>
        </span>
        <span
          class="text-[11px] px-2 py-0.5 rounded-full font-medium"
          :class="ionBalance.isBalanced ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' : 'bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'"
        >{{ ionBalance.isBalanced ? 'تعادل یونی مطلوب' : 'تعادل یونی نامتعادل' }}</span>
      </div>

      <!-- 🆕 جزئیات بیشتر: پیش‌فرض بسته تا صفحه شلوغ نباشد -->
      <ResultAccordion title="جزئیات بیشتر" subtitle="آمار کامل، عناصر، مخازن و توصیه‌ها" tone="neutral">
        <template #icon>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </template>

        <div class="space-y-4">
          <HomeStatsCards
            :ion-balance="ionBalance"
            :ion-balance-status="ionBalanceStatus"
            :active-elements-count="activeElementsCount"
            :active-reservoirs-count="activeReservoirsCount"
            :total-cost="totalCost"
          />
          <HomeElementsTable :elements-data="elementComparisonData" :target-unit="targetUnit" />
          <HomeReservoirCards :reservoir-data="reservoirData" :total-weight="totalReservoirWeight" />
          <HomeRecommendations :recommendations="recommendations" />
        </div>
      </ResultAccordion>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import ResultAccordion from './calc/ResultAccordion.vue';
import { apiService } from '@/services/apiService';

// ===== Sub-Components =====
import HomeEmptyState from './home/HomeEmptyState.vue';
import HomeStatsCards from './home/HomeStatsCards.vue';
import HomeElementsTable from './home/HomeElementsTable.vue';
import HomeReservoirCards from './home/HomeReservoirCards.vue';
import HomeRecommendations from './home/HomeRecommendations.vue';
import HomeSummaryGauges from './home/HomeSummaryGauges.vue';

// ============================================================
// Props
// ============================================================
interface Props {
  targetUnit?: string;
}

const props = defineProps<Props>();

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
const targetUnit = computed(() => props.targetUnit || 'ppm');

// لیست عناصر
const ELEMENTS = [
  'N-NO3',
  'P',
  'S',
  'N-NH4',
  'K',
  'Ca',
  'Mg',
  'Na',
  'Cl',
  'Fe',
  'Mn',
  'Zn',
  'B',
  'Cu',
  'Mo'
];

// ============================================================
// Computed
// ============================================================
const hasActiveReport = computed(() => reportStore.hasActiveReport);

// 🆕 رفع باگ: قبلاً با هر مقدار جزئی (فقط یک عنصر هدف یا آب) کل داشبورد
// پر از اعداد صفر/نامرتبط نشان داده می‌شد. حالا فقط بعد از یک محاسبه
// واقعی (دکمه «محاسبه») داشبورد کامل نشان داده می‌شود.
const hasCalculatedData = computed(() => calcStore.optimizationResult !== null);

// 🆕 چند گزارش اخیر برای دسترسی سریع، وقتی هنوز محاسبه‌ای انجام نشده
const recentReports = computed(() => (reportStore.reports || []).slice(0, 5));

const openReport = (id: number) => {
  reportStore.loadReport(id);
};

const ionBalance = computed(() => targetStore.ionBalance);

const targetElements = computed(() => targetStore.targetElements);

const actualElements = computed(() => {
  if (calcStore.optimizationResult?.concentrations) {
    return calcStore.optimizationResult.concentrations;
  }

  const result: Record<string, number> = {};

  for (const row of calcStore.calculationRows) {
    if (row.elements) {
      for (const [element, percentage] of Object.entries(row.elements)) {
        if (
          percentage &&
          percentage > 0 &&
          row.weight &&
          row.weight > 0
        ) {
          const contribution =
            (percentage / 100) *
            row.weight *
            (row.purity / 100);

          result[element] =
            (result[element] || 0) + contribution;
        }
      }
    }
  }

  return result;
});

const activeElementsCount = computed(() => {
  return Object.values(targetElements.value).filter(
    v => v && v > 0
  ).length;
});

const reservoirData = computed(() => calcStore.reservoirData);

const activeReservoirsCount = computed(() => {
  let count = 0;

  if (reservoirData.value.A?.length > 0) count++;
  if (reservoirData.value.B?.length > 0) count++;
  if (reservoirData.value.C?.length > 0) count++;

  return count;
});

const totalReservoirWeight = computed(() => {
  let total = 0;

  for (const key of ['A', 'B', 'C'] as const) {
    for (const item of reservoirData.value[key] || []) {
      total += item.amount || 0;
    }
  }

  return total;
});

const totalCost = computed(() => calcStore.totalCost || 0);

const elementComparisonData = computed(() => {
  return ELEMENTS.map(element => {
    const target =
      (targetElements.value as any)[element] || 0;

    const actual =
      (actualElements.value as any)[element] || 0;

    const difference = actual - target;

    const progressPercent =
      target > 0
        ? Math.min((actual / target) * 100, 150)
        : 0;

    return {
      element,
      target,
      actual,
      difference,
      progressPercent
    };
  });
});

const ionBalanceStatus = computed(() => {
  if (!ionBalance.value) {
    return {
      borderClass:
        'border-l-gray-300 dark:border-l-gray-600',
      bgClass:
        'bg-gray-100 dark:bg-gray-700',
      iconClass:
        'text-gray-500 dark:text-gray-400',
      badgeClass:
        'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
    };
  }

  if (ionBalance.value.isBalanced) {
    return {
      borderClass:
        'border-l-success-500',
      bgClass:
        'bg-success-50 dark:bg-success-900/30',
      iconClass:
        'text-success-600 dark:text-success-400',
      badgeClass:
        'bg-success-100 dark:bg-success-900/50 text-success-700 dark:text-success-400'
    };
  }

  return {
    borderClass:
      'border-l-danger-500',
    bgClass:
      'bg-danger-50 dark:bg-danger-900/30',
    iconClass:
      'text-danger-600 dark:text-danger-400',
    badgeClass:
      'bg-danger-100 dark:bg-danger-900/50 text-danger-700 dark:text-danger-400'
  };
});

const recommendations = computed(() => {
  const recs: Array<{
    type: 'success' | 'warning' | 'danger';
    title: string;
    description: string;
  }> = [];

  // ============================================================
  // Ion Balance
  // ============================================================
  if (!ionBalance.value.isBalanced) {
    const diff = Math.abs(
      ionBalance.value.cation -
      ionBalance.value.anion
    );

    recs.push({
      type: 'danger',
      title: 'عدم تعادل یونی',
      description:
        `اختلاف کاتیون و آنیون ${diff.toFixed(2)} meq/L است.`
    });
  }

  // ============================================================
  // Element Deficiency / Excess
  // ============================================================
  const deficient: string[] = [];
  const excessive: string[] = [];

  for (const item of elementComparisonData.value) {
    if (item.target === 0) continue;

    if (item.progressPercent < 70) {
      deficient.push(item.element);
    } else if (item.progressPercent > 130) {
      excessive.push(item.element);
    }
  }

  if (deficient.length > 0) {
    recs.push({
      type: 'warning',
      title: `${deficient.length} عنصر با کمبود شدید`,
      description:
        `عناصر ${deficient.slice(0, 3).join(', ')}${
          deficient.length > 3 ? ' و...' : ''
        } کمتر از 70% مقدار هدف هستند.`
    });
  }

  if (excessive.length > 0) {
    recs.push({
      type: 'warning',
      title: `${excessive.length} عنصر با بیش‌بود`,
      description:
        `عناصر ${excessive.slice(0, 3).join(', ')}${
          excessive.length > 3 ? ' و...' : ''
        } بیشتر از 130% مقدار هدف هستند.`
    });
  }

  // ============================================================
  // EC
  // ============================================================
  if (calcStore.optimizationResult?.ec !== undefined) {
    const ec = calcStore.optimizationResult.ec;

    if (ec < 0.8) {
      recs.push({
        type: 'warning',
        title: 'EC کم',
        description:
          `EC پایین است (${ec.toFixed(
            2
          )} dS/m). ممکن است نیاز به افزایش غلظت کودها باشد.`
      });
    } else if (ec > 3.5) {
      recs.push({
        type: 'danger',
        title: 'EC بحرانی',
        description:
          `EC بسیار بالا است (${ec.toFixed(
            2
          )} dS/m). خطر شوری جدی است!`
      });
    }
  }

  // ============================================================
  // No Problems
  // ============================================================
  if (recs.length === 0) {
    recs.push({
      type: 'success',
      title: 'وضعیت مطلوب',
      description:
        'تمام پارامترها در محدوده مناسب قرار دارند.'
    });
  }

  return recs;
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

    if (
      Object.keys(waterStore.waterValues).length === 0 &&
      hasActiveReport.value
    ) {
      try {
        const waterData =
          await apiService.getWaterAnalysis(
            String(reportStore.currentReportId)
          );

        if (waterData) {
          waterStore.loadFromAPI(waterData);
        }
      } catch (e) {}
    }
  } catch (err: any) {
    error.value =
      err.message ||
      'خطا در بارگذاری داده‌ها';

    console.error(
      'Error loading dashboard data:',
      err
    );
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
    console.log(
      `🔄 Report ID changed: ${newId}`
    );

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
  console.log(
    '📊 Report changed event received'
  );

  loadDashboardData();
};

const handleReportReset = () => {
  console.log(
    '🔄 Report reset event received'
  );

  isLoading.value = false;
  error.value = null;
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(() => {
  console.log('🏠 HomeTab mounted');

  loadDashboardData();

  window.addEventListener(
    'report-changed',
    handleReportChanged
  );

  window.addEventListener(
    'report-reset',
    handleReportReset
  );
});

onUnmounted(() => {
  console.log('🏠 HomeTab unmounted');

  window.removeEventListener(
    'report-changed',
    handleReportChanged
  );

  window.removeEventListener(
    'report-reset',
    handleReportReset
  );
});
</script>

