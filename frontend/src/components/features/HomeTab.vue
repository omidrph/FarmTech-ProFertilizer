<!-- frontend/src/components/features/HomeTab.vue -->
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
      class="flex items-center justify-between gap-3 rounded-xl border border-rose-200 dark:border-rose-700/60 bg-rose-50 dark:bg-rose-950/40 px-4 py-3"
    >
      <p class="text-sm text-rose-700 dark:text-rose-300">{{ error }}</p>
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
        :last-updated-text="lastUpdatedText"
        :summary-text="heroSummaryText"
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
          <HomeReservoirs :counts="reservoirCounts" :ph-note="phAdjustmentNote" />
        </div>
      </div>

      <HomeAttentionList :items="attentionItems" @details="emit('navigate', 'fertilizer-calc')" />

      <!-- پیام کوتاه -->
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
const hasCalculatedData = computed(() => calcStore.optimizationResult !== null);
const recentReports = computed(() => (reportStore.reports || []).slice(0, 3));

const openReport = (id: number) => {
  reportStore.loadReport(id);
};

// ============================================================
// Computed: مراحل محاسبه کود
// ============================================================
const hasTargets = computed(() =>
  Object.values(targetStore.targetElements || {}).some(value => Number(value) > 0)
);

const hasWater = computed(() =>
  Object.keys(waterStore.calcWaterValues).length > 0
);

const userFertilizersCount = computed(
  () => (fertilizerStore.fertilizers || []).filter((f: any) => !f.isSystemDefault).length
);

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
    // در حالت خصوصی مرورگر ممکن است ذخیره‌سازی در دسترس نباشد
  }
};

// ============================================================
// Computed: وضعیت کلی نتیجه
// ============================================================
const result = computed(() => calcStore.optimizationResult);

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

const costValue = computed(() => {
  const fromResult = Number(result.value?.cost_total) || 0;
  if (fromResult > 0) return fromResult;
  const fromStore = Number(calcStore.totalCost) || 0;
  if (fromStore > 0) return fromStore;
  // آخرین راه: جمع (وزن × قیمت) از روی نتیجه و پایگاه‌داده کود فعلی
  let sum = 0;
  for (const [id, grams] of Object.entries(result.value?.weights || {})) {
    const f: any = (fertilizerStore.fertilizers || []).find((x: any) => String(x.id) === String(id));
    if (f) sum += (Number(grams) / 1000) * (Number(f.pricePerKg) || 0);
  }
  return sum;
});
const costText = computed(() => Math.round(costValue.value).toLocaleString('fa-IR'));

const activeElementsCount = computed(() =>
  Object.values(targetStore.targetElements || {}).filter(v => Number(v) > 0).length
);

// ✅ از reservoir_data خودِ نتیجه (همان که صفحهٔ نتیجه نشان می‌دهد) خوانده می‌شود، نه state قدیمی.
// اسید/بازِ «اصلاح pH» هم در مخزن C (اسید) حساب می‌شود.
const phAdjustment = computed(() => result.value?.ph_adjustment || null);
const reservoirCounts = computed(() => {
  const data: any = result.value?.reservoir_data || calcStore.reservoirData;
  const count = (arr: any) => (Array.isArray(arr) ? arr.length : 0);
  return { A: count(data?.A), B: count(data?.B), C: count(data?.C) + (phAdjustment.value ? 1 : 0) };
});
const phAdjustmentNote = computed(() => (phAdjustment.value ? `شامل ${phAdjustment.value.chemical_name} (اصلاح pH)` : ''));

const fertilizerCount = computed(() =>
  Object.values(result.value?.weights || {}).filter(value => Number(value) > 0).length
);

const lastUpdatedText = computed(() => '');

// ============================================================
// متن خلاصه عناصر
// ============================================================
const heroSummaryText = computed(() => {
  const targets = targetStore.targetElements as Record<string, number>;
  const actual = (result.value?.concentrations || {}) as Record<string, number>;

  let preciseCount = 0;
  let totalCount = 0;
  const outliers: string[] = [];

  for (const [element, targetRaw] of Object.entries(targets)) {
    const target = Number(targetRaw);
    if (target <= 0) continue;
    totalCount++;
    const ratio = ((Number(actual[element]) || 0) / target) * 100;
    const deviation = Math.abs(ratio - 100);
    if (deviation <= 3) {
      preciseCount++;
    } else if (deviation > 10 && outliers.length < 3) {
      outliers.push(element);
    }
  }

  if (totalCount === 0) {
    return 'هنوز عنصر هدفی برای این گزارش ثبت نشده است.';
  }

  if (outliers.length === 0) {
    return `${preciseCount.toLocaleString('fa-IR')} از ${totalCount.toLocaleString('fa-IR')} عنصر دقیقاً در محدوده هدف قرار دارند.`;
  }

  return `${preciseCount.toLocaleString('fa-IR')} از ${totalCount.toLocaleString('fa-IR')} عنصر دقیق هستند؛ ${outliers.join('، ')} نیاز به بررسی دارند.`;
});

// ============================================================
// Computed: هشدارهای کوتاه
// ============================================================
type AttnKind = 'danger' | 'warn' | 'ph' | 'info';
const attentionItems = computed(() => {
  const items: Array<{ kind: AttnKind; title: string; text?: string; hint?: string }> = [];
  const actual = (result.value?.concentrations || {}) as Record<string, number>;
  const targets = targetStore.targetElements as Record<string, number>;
  const fa = (n: number, d = 1) => n.toLocaleString('fa-IR', { maximumFractionDigits: d });

  // ۱) تعادل یونی
  if (!ionBalanced.value && ionSource.value) {
    const cat = Number(ionSource.value.cation) || 0;
    const ani = Number(ionSource.value.anion) || 0;
    const diff = Math.abs(cat - ani);
    const pct = Math.max(cat, ani) > 0 ? (diff / Math.max(cat, ani)) * 100 : 0;
    items.push({ kind: pct > 10 ? 'danger' : 'warn', title: 'عدم تعادل یونی', text: `اختلاف کاتیون و آنیون ${fa(diff, 2)} meq/L (${fa(pct)}٪) است.`, hint: cat > ani ? 'آنیون کم است؛ کودی با آنیون بیشتر (نیترات، سولفات یا فسفات) اضافه کنید.' : 'کاتیون کم است؛ کودی با پتاسیم، کلسیم یا منیزیم اضافه کنید.' });
  }

  // ۲) خطای اصلاح pH (اسید/باز تب PH) — نمایش جدا با رنگ بنفش
  const adj = phAdjustment.value;
  if (adj) {
    for (const [el, added] of Object.entries(adj.element_contributions || {})) {
      const add = Number(added);
      if (!(add > 0)) continue;
      const tgt = Number(targets[el]) || 0;
      const act = Number(actual[el]) || 0;
      if (tgt > 0 && act - tgt > Math.max(2, tgt * 0.05)) {
        items.push({ kind: 'ph', title: `خطای اصلاح pH — ${el}`, text: `${adj.chemical_name} حدود ${fa(add)} ppm ${el} وارد کرده و غلظت نهایی ${fa(act)} ppm شد (هدف ${fa(tgt)}).`, hint: 'مقدار اسید/باز را در تب PH کاهش دهید یا ماده‌ای با عنصر مفیدتر انتخاب کنید.' });
      } else if (tgt === 0 && add > 2) {
        items.push({ kind: 'ph', title: `خطای اصلاح pH — ${el}`, text: `${adj.chemical_name} ${fa(add)} ppm ${el} وارد کرده، در حالی که این عنصر هدفی ندارد.`, hint: 'برای این عنصر هدف تعریف کنید یا ماده دیگری برای تنظیم pH انتخاب کنید.' });
      }
    }
  }

  // ۳) عناصر کمبود / مازاد (به‌جز موارد خطای اصلاح pH که بالاتر آمد)
  const phFlagged = new Set(items.filter(i => i.kind === 'ph').map(i => i.title.split('— ')[1]));
  const deficient: string[] = [];
  const severe: string[] = [];
  const excessive: string[] = [];
  for (const [element, target] of Object.entries(targets)) {
    if (!(Number(target) > 0) || phFlagged.has(element)) continue;
    const ratio = ((Number(actual[element]) || 0) / Number(target)) * 100;
    if (ratio < 50) severe.push(element);
    else if (ratio < 85) deficient.push(element);
    else if (ratio > 120) excessive.push(element);
  }
  const list = (a: string[]) => a.slice(0, 4).join('، ') + (a.length > 4 ? ' و ...' : '');
  if (severe.length) items.push({ kind: 'danger', title: 'کمبود شدید', text: `${list(severe)} کمتر از نیمی از هدف است.`, hint: 'کود حاوی این عناصر را به فهرست انتخابی اضافه کنید.' });
  if (deficient.length) items.push({ kind: 'warn', title: 'کمبود عنصر', text: `${list(deficient)} کمتر از ۸۵٪ هدف است.`, hint: 'مقدار یا نوع کود تأمین‌کنندهٔ این عناصر را بازبینی کنید.' });
  if (excessive.length) items.push({ kind: 'warn', title: 'مازاد عنصر', text: `${list(excessive)} بیشتر از ۱۲۰٪ هدف است.`, hint: 'کودی با درصد کمتر از این عناصر انتخاب کنید.' });

  // ۴) EC
  if (ec.value > 3.5) items.push({ kind: 'danger', title: 'EC بسیار بالا', text: `EC برابر ${ecText.value} dS/m است؛ خطر شوری.`, hint: 'غلظت کودها را کم کنید یا از آب با کیفیت‌تر استفاده کنید.' });
  else if (ec.value > 0 && ec.value < 0.8) items.push({ kind: 'warn', title: 'EC پایین', text: `EC برابر ${ecText.value} dS/m است.`, hint: 'غلظت کودها را متناسب با نیاز گیاه افزایش دهید.' });

  // ۵) هشدارهای بک‌اند (رسوب، سازگاری و ...) — تکراری‌ها حذف می‌شوند
  const seen = new Set<string>();
  for (const w of (result.value?.warnings || []) as string[]) {
    const t = String(w || '').replace(/^[^\p{L}\p{N}]+/u, '').replace(/\s+/g, ' ').trim();
    const key = t.slice(0, 50);
    if (!t || seen.has(key)) continue;
    seen.add(key);
    // «خطر رسوب: Ca3(PO4)2» (کوتاه) در عنوان و بقیه در متن؛ جملهٔ بلند فقط متن
    const short = t.length < 60 && /[:：]/.test(t);
    items.push({ kind: /رسوب|خطر/.test(t) ? 'danger' : 'info', title: /رسوب/.test(t) ? (short ? t : 'خطر رسوب') : 'نکته', text: short ? undefined : (t.length > 170 ? t.slice(0, 167) + '…' : t) });
  }

  const order: Record<AttnKind, number> = { danger: 0, ph: 1, warn: 2, info: 3 };
  return items.sort((a, b) => order[a.kind] - order[b.kind]);
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

    if (Object.keys(waterStore.calcWaterValues).length === 0) {
      try {
        const waterData = await apiService.getWaterAnalysis(String(reportStore.currentReportId));
        if (waterData) waterStore.loadFromAPI(waterData);
      } catch {
        // آنالیز آب اختیاری است
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