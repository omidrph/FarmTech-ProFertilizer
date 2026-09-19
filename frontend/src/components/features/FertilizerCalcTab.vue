<!-- frontend/src/components/features/FertilizerCalcTab.vue -->
<!--
  ============================================================
  صفحه محاسبه کود (بازطراحی‌شده)
  ------------------------------------------------------------
  ساختار جدید: ویزارد سه‌مرحله‌ای
    ۱) تنظیمات مخزن و استوک
    ۲) انتخاب کود و حالت بهینه‌سازی
    ۳) نتیجه و خروجی PDF
  تغییرات مهم نسبت به نسخه قبل:
    • حذف کامل ماشین‌حساب pH (به‌جای آن تفسیر و آموزش pH در نتیجه)
    • حذف خروجی CSV و جایگزینی با خروجی PDF حرفه‌ای
    • «تعادل یونی خودکار» به‌صورت پیش‌فرض خاموش
    • حالت بهینه‌سازی به‌صورت تک‌انتخابی (منطبق با رفتار واقعی بک‌اند)
  ============================================================
-->
<template>
  <div class="pb-24">

    <!-- ============================================================ -->
    <!-- نوار مراحل -->
    <!-- ============================================================ -->
    <nav class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-3 sm:p-4 mb-4">
      <ol class="flex items-center gap-1 sm:gap-2">
        <li v-for="(step, index) in steps" :key="step.id" class="flex items-center flex-1 min-w-0">
          <button
            type="button"
            @click="goToStep(step.id)"
            :disabled="!isStepReachable(step.id)"
            class="flex items-center gap-2 min-w-0 flex-1 text-right rounded-lg px-2 py-1.5 transition-colors disabled:cursor-not-allowed"
            :class="currentStep === step.id ? 'bg-primary-50 dark:bg-primary-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-700/40 disabled:hover:bg-transparent'"
          >
            <span
              class="w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 transition-colors"
              :class="stepCircleClass(step.id)"
            >
              <svg v-if="isStepDone(step.id)" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
              <template v-else>{{ index + 1 }}</template>
            </span>
            <span class="min-w-0 hidden sm:block">
              <span
                class="block text-sm font-semibold truncate"
                :class="currentStep === step.id ? 'text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300'"
              >{{ step.title }}</span>
              <span class="block text-[11px] text-gray-400 truncate">{{ step.subtitle }}</span>
            </span>
          </button>

          <span
            v-if="index < steps.length - 1"
            class="h-0.5 flex-1 mx-1 sm:mx-2 rounded-full transition-colors"
            :class="isStepDone(step.id) ? 'bg-primary-500' : 'bg-gray-200 dark:bg-gray-700'"
          ></span>
        </li>
      </ol>

      <!-- عنوان مرحله در موبایل -->
      <p class="sm:hidden mt-2 text-sm font-semibold text-primary-700 dark:text-primary-400">
        {{ activeStepMeta.title }}
        <span class="block text-[11px] font-normal text-gray-400">{{ activeStepMeta.subtitle }}</span>
      </p>
    </nav>

    <!-- ============================================================ -->
    <!-- محتوای مراحل -->
    <!-- ============================================================ -->
    <Transition name="step" mode="out-in">

      <!-- ===================== مرحله ۱ ===================== -->
      <div v-if="currentStep === 1" key="step-1" class="space-y-4">
        <!-- پیش‌نیازها -->
        <section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">پیش‌نیازهای محاسبه</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div
              v-for="item in prerequisites"
              :key="item.key"
              class="flex items-start gap-2 rounded-lg border p-2.5"
              :class="item.done
                ? 'border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20'
                : 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20'"
            >
              <span
                class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
                :class="item.done ? 'bg-emerald-500 text-white' : 'bg-amber-500 text-white'"
              >
                <svg v-if="item.done" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 9v2m0 4h.01" />
                </svg>
              </span>
              <div class="min-w-0">
                <p class="text-sm font-medium text-gray-800 dark:text-gray-100">{{ item.title }}</p>
                <p class="text-[11px]" :class="item.done ? 'text-emerald-700 dark:text-emerald-400' : 'text-amber-700 dark:text-amber-400'">
                  {{ item.hint }}
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- تنظیمات استوک (بدون تغییر) -->
        <StockSettings
          :main-tank-volume="mainTankVolume"
          :stock-volume="stockVolume"
          :injection-ratio="injectionRatio"
          @update:main-tank-volume="mainTankVolume = $event"
          @update:stock-volume="stockVolume = $event"
          @update:injection-ratio="injectionRatio = $event"
        />
      </div>

      <!-- ===================== مرحله ۲ ===================== -->
      <div v-else-if="currentStep === 2" key="step-2" class="space-y-4">
        <FertilizerSelector
          :fertilizers="fertilizers"
          :selected-fertilizers="localSelectedFertilizers"
          @update:selected-fertilizers="handleSelectionChange"
        />

        <!-- حالت بهینه‌سازی -->
        <section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <div class="flex items-center justify-between gap-2 mb-3 flex-wrap">
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white">حالت بهینه‌سازی</h3>
            <button
              type="button"
              @click="showAdvanced = !showAdvanced"
              class="text-xs text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
            >
              تنظیمات پیشرفته
              <svg class="w-3.5 h-3.5 transition-transform" :class="showAdvanced ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
            <button
              v-for="mode in optimizationModes"
              :key="mode.key"
              type="button"
              @click="optimizationMode = mode.key"
              class="text-right rounded-lg border-2 p-3 transition-all"
              :class="optimizationMode === mode.key
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'"
            >
              <span class="block text-sm font-semibold text-gray-900 dark:text-white">{{ mode.title }}</span>
              <span class="block text-[11px] text-gray-500 dark:text-gray-400 mt-0.5">{{ mode.description }}</span>
            </button>
          </div>

          <!-- تنظیمات پیشرفته -->
          <Transition name="step">
            <div v-show="showAdvanced" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 space-y-3">
              <label class="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  v-model="autoBalanceEnabled"
                  class="mt-0.5 w-4 h-4 rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500"
                />
                <span class="min-w-0">
                  <span class="block text-sm font-medium text-gray-700 dark:text-gray-200">تعادل یونی خودکار</span>
                  <span class="block text-[11px] text-gray-500 dark:text-gray-400">
                    در صورت فعال بودن، یون‌های پادبار (Na یا Cl) برای متعادل کردن فرمول اضافه می‌شوند. پیش‌فرض: خاموش.
                  </span>
                </span>
              </label>

              <div v-if="optimizationMode === 'fewer'" class="flex items-center gap-2">
                <span class="text-sm text-gray-600 dark:text-gray-300">حداکثر تعداد کود</span>
                <input
                  type="number"
                  min="1"
                  max="20"
                  v-model.number="maxFertilizersCount"
                  class="w-16 text-center rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 px-2 py-1 text-sm text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>

              <p v-if="optimizationMode !== 'accurate'" class="text-[11px] text-amber-600 dark:text-amber-400">
                در این حالت ممکن است دقت رسیدن به عناصر هدف کمی کاهش پیدا کند.
              </p>
            </div>
          </Transition>
        </section>
      </div>

      <!-- ===================== مرحله ۳ ===================== -->
      <div v-else key="step-3" class="space-y-4">
        <OptimizationResult
          v-if="hasOptimizationResult"
          :result="calcStore.optimizationResult"
          :fertilizers="fertilizers"
          :target-values="targetStore.targetElements"
          :tank-volume="mainTankVolume"
          @update-weight="handleWeightEdit"
        />

        <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-10 text-center">
          <p class="text-sm text-gray-500 dark:text-gray-400">هنوز محاسبه‌ای انجام نشده است.</p>
        </div>
      </div>
    </Transition>

    <!-- ============================================================ -->
    <!-- خطاهای محاسبه -->
    <!-- ============================================================ -->
    <div v-if="calcErrors.length > 0" class="mt-4 rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 p-4">
      <div class="flex items-start gap-2">
        <svg class="w-5 h-5 text-rose-600 dark:text-rose-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex-1 space-y-1">
          <p v-for="err in calcErrors" :key="err" class="text-sm text-rose-700 dark:text-rose-400">{{ err }}</p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نوار اقدام چسبان -->
    <!-- ============================================================ -->
    <div class="sticky bottom-0 z-30 mt-4 -mx-2 sm:mx-0">
      <div class="bg-white/95 dark:bg-gray-800/95 backdrop-blur border border-gray-200 dark:border-gray-700 sm:rounded-xl shadow-lg px-3 sm:px-4 py-3 flex items-center gap-2 flex-wrap">

        <!-- قبلی -->
        <button
          v-if="currentStep > 1"
          type="button"
          @click="goToStep(currentStep - 1)"
          class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          قبلی
        </button>

        <div class="flex-1"></div>

        <!-- بازنشانی -->
        <button
          type="button"
          @click="showResetConfirm = true"
          class="inline-flex items-center gap-1.5 px-3 py-2.5 text-sm font-medium rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span class="hidden sm:inline">بازنشانی</span>
        </button>

        <!-- مرحله ۱ -->
        <button
          v-if="currentStep === 1"
          type="button"
          @click="goToStep(2)"
          class="inline-flex items-center gap-1.5 px-5 py-2.5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          ادامه: انتخاب کود
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- مرحله ۲ -->
        <button
          v-else-if="currentStep === 2"
          type="button"
          @click="handleOptimize"
          :disabled="isOptimizing || !canOptimize"
          :title="optimizeBlockReason"
          class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
        >
          <svg v-if="!isOptimizing" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ isOptimizing ? 'در حال محاسبه...' : 'محاسبه و مشاهده نتیجه' }}
        </button>

        <!-- مرحله ۳ -->
        <template v-else>
          <button
            type="button"
            @click="handleOptimize"
            :disabled="isOptimizing || !canOptimize"
            class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-2.5 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="hidden sm:inline">محاسبه مجدد</span>
          </button>

          <button
            type="button"
            @click="handleExportPdf"
            :disabled="!hasOptimizationResult || isExporting"
            class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {{ isExporting ? 'در حال آماده‌سازی...' : 'خروجی PDF' }}
          </button>
        </template>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- تأیید بازنشانی -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showResetConfirm" class="fixed inset-0 z-[300] flex items-center justify-center p-4 bg-black/50" @click.self="showResetConfirm = false">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-sm p-5">
            <h3 class="text-base font-semibold text-gray-900 dark:text-white">بازنشانی محاسبه</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
              کودهای انتخاب‌شده، تنظیمات استوک و نتیجه فعلی پاک می‌شوند. ادامه می‌دهید؟
            </p>
            <div class="flex items-center justify-end gap-2 mt-5">
              <button
                type="button"
                @click="showResetConfirm = false"
                class="px-4 py-2 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700"
              >انصراف</button>
              <button
                type="button"
                @click="resetAll"
                class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-rose-600 hover:bg-rose-700"
              >بازنشانی</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ============================================================ -->
    <!-- پیام‌ها -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="toastMessage"
          class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[320] px-5 py-3 rounded-xl shadow-2xl flex items-center gap-2 max-w-[92vw]"
          :class="toastType === 'success' ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import { useCalcStore } from '@/store/modules/calcStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useReportStore } from '@/store/modules/reportStore';
import { useCalculations } from '@/composables/useCalculations';
import { usePdfExport } from '@/composables/usePdfExport';

import StockSettings from './calc/StockSettings.vue';
import FertilizerSelector from './calc/FertilizerSelector.vue';
import OptimizationResult from './calc/OptimizationResult.vue';

// ===== Props / Emits (بدون تغییر نسبت به نسخه قبل) =====
const props = defineProps<{
  fertilizers: any[];
  selectedFertilizers: string[];
  tankVolume: number;
  dilutionFactor: number;
  calcRows: any[];
  calcErrors: string[];
}>();

const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:tankVolume', value: number): void;
  (e: 'update:dilutionFactor', value: number): void;
  (e: 'update:calcRows', value: any[]): void;
  (e: 'update:calcErrors', value: string[]): void;
}>();

// ===== Stores / Composables =====
const calcStore = useCalcStore();
const targetStore = useTargetStore();
const waterStore = useWaterStore();
const reportStore = useReportStore();
const { optimizeFertilizers, isOptimizing } = useCalculations();
const { exportOptimizationPdf, isExporting } = usePdfExport();

// ===== تنظیمات استوک (از store) =====
const mainTankVolume = computed({
  get: () => calcStore.stockSettings.tankVolume,
  set: (value: number) => calcStore.setStockSettings({ tankVolume: value })
});
const stockVolume = computed({
  get: () => calcStore.stockSettings.stockVolume,
  set: (value: number) => calcStore.setStockSettings({ stockVolume: value })
});
const injectionRatio = computed({
  get: () => calcStore.stockSettings.injectionRatio,
  set: (value: number) => calcStore.setStockSettings({ injectionRatio: value })
});

// ===== وضعیت ویزارد =====
type StepId = 1 | 2 | 3;

const steps: Array<{ id: StepId; title: string; subtitle: string }> = [
  { id: 1, title: 'تنظیمات مخزن', subtitle: 'حجم مخزن، استوک و نسبت تزریق' },
  { id: 2, title: 'انتخاب کود', subtitle: 'کودها و حالت بهینه‌سازی' },
  { id: 3, title: 'نتیجه', subtitle: 'فرمول نهایی و خروجی PDF' }
];

const currentStep = ref<StepId>(1);
const activeStepMeta = computed(() => steps.find((step) => step.id === currentStep.value) || steps[0]);

// ===== State =====
const localSelectedFertilizers = ref<string[]>([...props.selectedFertilizers]);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');
const showResetConfirm = ref(false);
const showAdvanced = ref(false);

// 🆕 پیش‌فرض خاموش (درخواست کاربر)
const autoBalanceEnabled = ref(false);

type OptimizationMode = 'accurate' | 'fewer' | 'cheapest';
const optimizationMode = ref<OptimizationMode>('accurate');
const maxFertilizersCount = ref(6);

const optimizationModes: Array<{ key: OptimizationMode; title: string; description: string }> = [
  { key: 'accurate', title: 'دقیق‌ترین ترکیب', description: 'کمترین اختلاف با عناصر هدف' },
  { key: 'fewer', title: 'کمترین تعداد کود', description: 'ساخت ساده‌تر با کود کمتر' },
  { key: 'cheapest', title: 'کم‌هزینه‌ترین', description: 'اولویت با پایین‌ترین هزینه' }
];

// ===== Computed =====
const hasOptimizationResult = computed(() => calcStore.optimizationResult !== null);

const hasTargets = computed(() =>
  Object.values(targetStore.targetElements || {}).some((value) => Number(value) > 0)
);

const hasWaterAnalysis = computed(() =>
  Object.values(waterStore.waterValues || {}).some((value) => Number(value) > 0)
);

const prerequisites = computed(() => [
  {
    key: 'targets',
    title: 'عناصر هدف',
    done: hasTargets.value,
    hint: hasTargets.value ? 'ثبت شده است' : 'از تب «عناصر هدف» مقادیر را وارد کنید'
  },
  {
    key: 'water',
    title: 'آنالیز آب',
    done: hasWaterAnalysis.value,
    hint: hasWaterAnalysis.value ? 'ثبت شده است' : 'اختیاری، ولی دقت محاسبه را بالا می‌برد'
  },
  {
    key: 'fertilizers',
    title: 'کودهای انتخاب‌شده',
    done: localSelectedFertilizers.value.length > 0,
    hint: localSelectedFertilizers.value.length > 0
      ? `${localSelectedFertilizers.value.length} کود انتخاب شده`
      : 'در مرحله بعد حداقل یک کود انتخاب کنید'
  },
  {
    key: 'stock',
    title: 'تنظیمات استوک',
    done: mainTankVolume.value > 0 && stockVolume.value > 0 && injectionRatio.value > 0,
    hint: `مخزن ${mainTankVolume.value} لیتر • استوک ${stockVolume.value} لیتر • نسبت ۱:${injectionRatio.value}`
  }
]);

const canOptimize = computed(() => hasTargets.value && localSelectedFertilizers.value.length > 0);

const optimizeBlockReason = computed(() => {
  if (!hasTargets.value) return 'ابتدا عناصر هدف را وارد کنید';
  if (localSelectedFertilizers.value.length === 0) return 'حداقل یک کود انتخاب کنید';
  return '';
});

// ===== Watch =====
watch(
  () => props.selectedFertilizers,
  (value) => {
    localSelectedFertilizers.value = [...value];
  },
  { deep: true }
);

// ===== ناوبری مراحل =====
const isStepDone = (step: StepId): boolean => {
  if (step === 1) return currentStep.value > 1;
  if (step === 2) return hasOptimizationResult.value;
  return false;
};

const isStepReachable = (step: StepId): boolean => {
  if (step === 3) return hasOptimizationResult.value;
  return true;
};

const stepCircleClass = (step: StepId): string => {
  if (isStepDone(step)) return 'bg-emerald-500 text-white';
  if (currentStep.value === step) return 'bg-primary-600 text-white';
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400';
};

const goToStep = (step: number) => {
  const target = step as StepId;
  if (!isStepReachable(target)) return;
  currentStep.value = target;
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
};

// ===== اقدامات =====
const handleSelectionChange = (selectedIds: string[]) => {
  localSelectedFertilizers.value = selectedIds;
  emit('update:selectedFertilizers', selectedIds);
};

const handleOptimize = async () => {
  if (!hasTargets.value) {
    showToast('لطفاً ابتدا عناصر هدف را وارد کنید', 'error');
    return;
  }
  if (localSelectedFertilizers.value.length === 0) {
    showToast('لطفاً حداقل یک کود را انتخاب کنید', 'error');
    return;
  }

  const selectedFerts = props.fertilizers.filter((f) =>
    localSelectedFertilizers.value.includes(f.id)
  );

  try {
    const options = {
      auto_balance: autoBalanceEnabled.value,
      prefer_fewer_fertilizers: optimizationMode.value === 'fewer',
      max_fertilizers_count: optimizationMode.value === 'fewer' ? maxFertilizersCount.value : undefined,
      prefer_cheapest: optimizationMode.value === 'cheapest',
      prefer_most_accurate: optimizationMode.value === 'accurate'
    };

    const result = await optimizeFertilizers(
      selectedFerts,
      options,
      mainTankVolume.value,
      stockVolume.value,
      injectionRatio.value
    );

    if (result) {
      showToast('محاسبه با موفقیت انجام شد', 'success');
      goToStep(3);
    } else {
      showToast(calcStore.lastOptimizationError || 'خطا در محاسبه', 'error');
    }
  } catch (error: any) {
    showToast(error?.message || 'خطا در محاسبه', 'error');
  }
};

const handleWeightEdit = async (payload: { fertilizerId: string; weight: number }) => {
  const ok = await calcStore.recalculateManualWeight(payload.fertilizerId, payload.weight);
  if (ok) {
    showToast('وزن به‌روزرسانی و ذخیره شد', 'success');
  } else {
    const messages = calcStore.errorMessages;
    showToast(messages[messages.length - 1] || 'خطا در به‌روزرسانی وزن', 'error');
  }
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
      fertilizers: props.fertilizers,
      targetValues: targetStore.targetElements as Record<string, number>,
      meta: {
        reportName: report.reportName,
        plantName: report.plantName,
        season: report.season,
        tankVolume: mainTankVolume.value,
        stockVolume: stockVolume.value,
        injectionRatio: injectionRatio.value
      }
    });
    showToast('فایل PDF آماده شد؛ در پنجره چاپ گزینه Save as PDF را انتخاب کنید', 'success');
  } catch (error: any) {
    showToast(error?.message || 'خطا در ساخت خروجی PDF', 'error');
  }
};

const resetAll = () => {
  showResetConfirm.value = false;
  emit('update:calcRows', []);
  emit('update:calcErrors', []);
  localSelectedFertilizers.value = [];
  emit('update:selectedFertilizers', []);
  calcStore.setStockSettings({ tankVolume: 5000, stockVolume: 25, injectionRatio: 100 });
  calcStore.clearOptimizationResult();
  optimizationMode.value = 'accurate';
  autoBalanceEnabled.value = false;
  currentStep.value = 1;
  showToast('همه داده‌ها پاک شدند', 'success');
};

let toastTimer: ReturnType<typeof setTimeout> | null = null;
const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastMessage.value = null;
  }, 3500);
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.step-enter-active,
.step-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.step-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.step-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
