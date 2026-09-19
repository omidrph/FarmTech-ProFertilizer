<!-- frontend/src/components/features/calc/OptimizationResult.vue -->
<!--
  نمایش نتیجه بهینه‌سازی (بازطراحی‌شده)
  ساختار: نوار خلاصه + بخش‌های تاشو
  همه بخش‌های فرعی به‌صورت پیش‌فرض بسته‌اند تا صفحه شلوغ نشود.
-->
<template>
  <div v-if="result" class="space-y-3">

    <!-- ============================================================ -->
    <!-- خلاصه -->
    <!-- ============================================================ -->
    <ResultKpiBar :result="result" :used-count="usedCount" />

    <!-- نوار وضعیت کلی -->
    <div
      v-if="statusBanner"
      class="rounded-xl px-4 py-3 text-sm flex items-start gap-2 border"
      :class="statusBanner.class"
    >
      <svg class="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div class="min-w-0">
        <p class="font-medium">{{ statusBanner.message }}</p>
        <ul v-if="statusBanner.recommendations.length" class="mt-1 space-y-0.5 text-xs opacity-90 list-disc mr-4">
          <li v-for="item in statusBanner.recommendations" :key="item">{{ item }}</li>
        </ul>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مقادیر کود (باز به‌صورت پیش‌فرض) -->
    <!-- ============================================================ -->
    <ResultAccordion
      title="مقدار کودها"
      :subtitle="`${usedCount} کود در ترکیب نهایی`"
      tone="primary"
      :default-open="true"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
      </template>

      <ResultFertilizerTable
        :result="result"
        :fertilizers="fertilizers"
        :tank-volume="tankVolume"
        @update-weight="$emit('update-weight', $event)"
      />
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- دقت عناصر -->
    <!-- ============================================================ -->
    <ResultAccordion
      title="عناصر تأمین‌شده در برابر هدف"
      subtitle="واحد: ppm"
      tone="success"
      :badge="elementsBadge"
      :default-open="true"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </template>

      <ResultElementsGrid
        :target-values="targetValues"
        :concentrations="result.concentrations || {}"
      />
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- EC و pH + آموزش کوتاه -->
    <!-- ============================================================ -->
    <ResultAccordion
      title="EC و pH محلول"
      subtitle="تفسیر اعداد و کارهای لازم"
      tone="neutral"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
      </template>

      <div class="space-y-3">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-3">
            <p class="text-xs text-gray-500 dark:text-gray-400">EC نهایی</p>
            <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ toFixed(result.ec, 2) }} <span class="text-xs font-normal text-gray-400">dS/m</span></p>
            <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">وضعیت: {{ result.ec_status || 'نامشخص' }} • محدوده متداول ۰٫۸ تا ۲٫۵</p>
          </div>
          <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-3">
            <p class="text-xs text-gray-500 dark:text-gray-400">pH (تخمینی)</p>
            <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ toFixed(result.ph, 2) }}</p>
            <p v-if="result.ph_min !== undefined && result.ph_max !== undefined" class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">
              بازه محتمل: {{ toFixed(result.ph_min, 2) }} تا {{ toFixed(result.ph_max, 2) }} • محدوده مطلوب ۵٫۵ تا ۶٫۵
            </p>
          </div>
        </div>

        <!-- آموزش کوتاه pH: جایگزین ماشین‌حساب حذف‌شده -->
        <div class="rounded-lg bg-gray-50 dark:bg-gray-700/40 border border-gray-200 dark:border-gray-700 p-3">
          <p class="text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1.5">درباره pH چه باید بدانید؟</p>
          <ul class="text-xs text-gray-600 dark:text-gray-400 space-y-1 list-disc mr-4">
            <li>این عدد یک <strong>تخمین محاسباتی</strong> است و جای اندازه‌گیری با pH‌متر را نمی‌گیرد؛ همیشه محلول نهایی مخزن را اندازه بگیرید.</li>
            <li>محدوده مطلوب اغلب محصولات هیدروپونیک بین <strong>۵٫۵ تا ۶٫۵</strong> است؛ خارج از این محدوده جذب آهن، فسفر و ریزمغذی‌ها افت می‌کند.</li>
            <li>اگر pH اندازه‌گیری‌شده بالاتر از هدف بود، با افزودن تدریجی اسید (معمولاً نیتریک یا فسفریک) و هم‌زدن، مرحله‌به‌مرحله پایین بیاورید و بعد از هر افزودن دوباره اندازه بگیرید.</li>
            <li>مقدار اسید لازم به <strong>قلیائیت آب</strong> شما بستگی دارد، نه فقط به pH؛ برای همین یک عدد ثابت برای همه آب‌ها وجود ندارد.</li>
            <li>هرگز اسید و کود کلسیمی را در یک سطل استوک غلیظ با هم ترکیب نکنید.</li>
          </ul>
          <p v-if="result.ph_disclaimer" class="text-[11px] text-gray-500 dark:text-gray-400 mt-2">
            {{ result.ph_disclaimer }}
          </p>
        </div>
      </div>
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- تعادل یونی -->
    <!-- ============================================================ -->
    <ResultAccordion
      v-if="result.ion_balance"
      title="تعادل یونی"
      :subtitle="ionBalanceSubtitle"
      :tone="result.ion_balance.isBalanced ? 'success' : 'warning'"
      :badge="result.ion_balance.isBalanced ? 'متعادل' : 'نامتعادل'"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </template>

      <div class="space-y-2">
        <div class="grid grid-cols-3 gap-2 text-center">
          <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
            <p class="text-[11px] text-gray-500 dark:text-gray-400">کاتیون</p>
            <p class="text-sm font-bold text-blue-600 dark:text-blue-400 tabular-nums">{{ toFixed(result.ion_balance.cation, 2) }}</p>
          </div>
          <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
            <p class="text-[11px] text-gray-500 dark:text-gray-400">آنیون</p>
            <p class="text-sm font-bold text-purple-600 dark:text-purple-400 tabular-nums">{{ toFixed(result.ion_balance.anion, 2) }}</p>
          </div>
          <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-2">
            <p class="text-[11px] text-gray-500 dark:text-gray-400">اختلاف</p>
            <p class="text-sm font-bold tabular-nums" :class="result.ion_balance.isBalanced ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'">
              {{ toFixed(ionDifference, 2) }}
            </p>
          </div>
        </div>

        <div class="relative h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden flex">
          <div class="h-full bg-blue-500 transition-all duration-500" :style="{ width: ionPercent('cation') + '%' }"></div>
          <div class="h-full bg-purple-500 transition-all duration-500" :style="{ width: ionPercent('anion') + '%' }"></div>
        </div>
        <p class="text-[11px] text-gray-500 dark:text-gray-400">
          واحد اعداد meq/L است. اختلاف زیاد بین کاتیون و آنیون یعنی فرمول از نظر شیمیایی متوازن نیست.
        </p>
      </div>
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- ترتیب ساخت (پیش‌فرض بسته، فشرده و بدون متن تکراری) -->
    <!-- ============================================================ -->
    <ResultAccordion
      v-if="instructions.length > 0"
      title="ترتیب ساخت محلول"
      subtitle="راهنمای گام‌به‌گام کنار مخزن"
      tone="neutral"
      :badge="`${instructions.length} گام`"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      </template>

      <ol class="space-y-2">
        <li
          v-for="(inst, index) in instructions"
          :key="inst.fertilizer_id || index"
          class="flex items-start gap-2.5 rounded-lg border border-gray-200 dark:border-gray-700 p-2.5"
        >
          <span class="w-6 h-6 rounded-full bg-primary-600 text-white text-[11px] font-bold flex items-center justify-center flex-shrink-0">
            {{ index + 1 }}
          </span>
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ inst.fertilizer_name }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded" :class="tankBadgeClass(inst.reservoir)">مخزن {{ inst.reservoir }}</span>
            </div>
            <p class="text-xs text-gray-600 dark:text-gray-400 mt-0.5 tabular-nums">
              {{ toFixed(inst.weight_grams, 0) }} گرم در {{ inst.recommended_bucket_liters }} لیتر آب
            </p>
            <p v-if="inst.warning" class="text-[11px] text-amber-600 dark:text-amber-400 mt-0.5">{{ inst.warning }}</p>
          </div>
        </li>
      </ol>

      <div v-if="result.stock_info" class="mt-3 rounded-lg bg-gray-50 dark:bg-gray-700/40 border border-gray-200 dark:border-gray-700 p-2.5 text-[11px] text-gray-600 dark:text-gray-400 space-y-0.5">
        <p>مخزن اصلی: {{ result.stock_info.tank_volume }} لیتر</p>
        <p v-if="result.stock_info.total_stock_liters">حجم کل استوک لازم: {{ result.stock_info.total_stock_liters }} لیتر</p>
        <p v-if="result.stock_info.buckets_needed && result.stock_info.buckets_needed > 1">
          در {{ result.stock_info.buckets_needed }} نوبت آماده کنید.
        </p>
      </div>
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- هشدارها و پیشنهادها -->
    <!-- ============================================================ -->
    <ResultAccordion
      v-if="noteCount > 0"
      title="هشدارها و پیشنهادها"
      :subtitle="noteSubtitle"
      :tone="warnings.length > 0 ? 'warning' : 'primary'"
      :badge="String(noteCount)"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </template>

      <div class="space-y-2">
        <div v-if="warnings.length" class="rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 p-3">
          <p class="text-xs font-semibold text-amber-700 dark:text-amber-400 mb-1">هشدارها</p>
          <ul class="text-xs text-amber-700 dark:text-amber-300 space-y-0.5 list-disc mr-4">
            <li v-for="item in warnings" :key="item">{{ item }}</li>
          </ul>
        </div>
        <div v-if="suggestions.length" class="rounded-lg bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800 p-3">
          <p class="text-xs font-semibold text-primary-700 dark:text-primary-400 mb-1">پیشنهادها</p>
          <ul class="text-xs text-primary-700 dark:text-primary-300 space-y-0.5 list-disc mr-4">
            <li v-for="item in suggestions" :key="item">{{ item }}</li>
          </ul>
        </div>
      </div>
    </ResultAccordion>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OptimizationResponse } from '@/types';
import ResultKpiBar from './ResultKpiBar.vue';
import ResultAccordion from './ResultAccordion.vue';
import ResultFertilizerTable from './ResultFertilizerTable.vue';
import ResultElementsGrid from './ResultElementsGrid.vue';

const props = withDefaults(
  defineProps<{
    result: OptimizationResponse | null;
    fertilizers: any[];
    targetValues: Record<string, number>;
    tankVolume?: number;
  }>(),
  { tankVolume: 1000 }
);

defineEmits<{
  (e: 'update-weight', payload: { fertilizerId: string; weight: number }): void;
}>();

const result = computed(() => props.result);

const toFixed = (value: unknown, digits = 2): string => {
  const parsed = Number(value);
  return isFinite(parsed) ? parsed.toFixed(digits) : '—';
};

const usedCount = computed(() => {
  const weights = result.value?.weights || {};
  return Object.values(weights).filter((weight) => typeof weight === 'number' && weight > 0).length;
});

const warnings = computed(() => result.value?.warnings || []);
const suggestions = computed(() => result.value?.suggestions || []);
const noteCount = computed(() => warnings.value.length + suggestions.value.length);
const noteSubtitle = computed(() => {
  const parts: string[] = [];
  if (warnings.value.length) parts.push(`${warnings.value.length} هشدار`);
  if (suggestions.value.length) parts.push(`${suggestions.value.length} پیشنهاد`);
  return parts.join(' • ');
});

const instructions = computed<any[]>(() => result.value?.stock_instructions || []);

const elementsBadge = computed(() => {
  if (!result.value) return '';
  const targets = Object.entries(props.targetValues || {}).filter(([, value]) => Number(value) > 0);
  if (targets.length === 0) return '';
  const accurate = targets.filter(([element, target]) => {
    const actual = Number(result.value?.concentrations?.[element] || 0);
    return Math.abs((actual - Number(target)) / Number(target)) * 100 <= 3;
  }).length;
  return `${accurate} از ${targets.length} دقیق`;
});

const ionDifference = computed(() => {
  const balance = result.value?.ion_balance;
  if (!balance) return 0;
  return Math.abs((balance.cation || 0) - (balance.anion || 0));
});

const ionBalanceSubtitle = computed(() => `اختلاف ${toFixed(ionDifference.value, 2)} meq/L`);

const ionPercent = (type: 'cation' | 'anion'): number => {
  const balance = result.value?.ion_balance;
  if (!balance) return 50;
  const total = (balance.cation || 0) + (balance.anion || 0);
  if (total === 0) return 50;
  return ((type === 'cation' ? balance.cation : balance.anion) / total) * 100;
};

const statusBanner = computed(() => {
  const status: any = result.value?.ec_ph_status;
  if (!status?.message) return null;

  const map: Record<string, string> = {
    success: 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300',
    warning: 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300',
    danger: 'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300'
  };

  return {
    message: status.message,
    recommendations: status.recommendations || [],
    class: map[status.color] || 'bg-gray-50 dark:bg-gray-700/40 border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300'
  };
});

const tankBadgeClass = (tank: string): string => {
  const map: Record<string, string> = {
    A: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    B: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    C: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
  };
  return map[tank] || 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300';
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
