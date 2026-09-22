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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6l.5 4M9 3L7.5 15.5A2 2 0 009.48 18h5.04a2 2 0 001.98-2.5L15 7M9 3l-.5 4m6.5-4l.5 4M5.5 12h13" />
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
      subtitle="قابل تغییر به ppm یا درصد"
      tone="success"
      :badge="elementsBadge"
      :default-open="true"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="8" stroke-width="2" />
          <circle cx="12" cy="12" r="4" stroke-width="2" />
          <circle cx="12" cy="12" r="0.6" fill="currentColor" stroke="none" />
        </svg>
      </template>

      <ResultElementsGrid
        :target-values="targetValues"
        :concentrations="result.concentrations || {}"
      />
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v3m0 0l-6 12a5 5 0 0010 0L12 6zm0 0l6 12a5 5 0 01-10 0M4 9h4m8 0h4" />
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
    <!-- هشدارها (بازطراحی کامل) -->
    <!-- ============================================================ -->
    <ResultAccordion
      title="هشدارها و بررسی کیفیت"
      :subtitle="warningsSubtitle"
      :tone="warningsTone"
      :badge="warningsBadge"
      :default-open="warningsTone !== 'neutral'"
    >
      <template #icon>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m0 3.75h.008v.008H12v-.008zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </template>

      <ResultWarnings
        :warnings="warnings"
        :suggestions="suggestions"
        :is-converged="!!result.is_converged"
        :accuracy="accuracy"
        :unused-count="unusedCount"
        :bad-elements-count="badElementsCount"
        @go-to-selection="$emit('go-to-selection')"
      />
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
import ResultWarnings from './ResultWarnings.vue';

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
  (e: 'go-to-selection'): void;
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

const unusedCount = computed(() => {
  const weights = result.value?.weights || {};
  const total = Object.keys(weights).length;
  return Math.max(0, total - usedCount.value);
});

const badElementsCount = computed(() => {
  const targets = Object.entries(props.targetValues || {}).filter(([, value]) => Number(value) > 0);
  return targets.filter(([element, target]) => {
    const actual = Number(result.value?.concentrations?.[element] || 0);
    const deviation = Math.abs(((actual - Number(target)) / Number(target)) * 100);
    return deviation > 10;
  }).length;
});

const warnings = computed(() => result.value?.warnings || []);
const suggestions = computed(() => result.value?.suggestions || []);

// 🆕 دقت واقعی از میانگین target_achievement (نه residual_error خام)
const accuracy = computed(() => {
  const values = Object.values(result.value?.target_achievement || {});
  if (values.length === 0) return 100;
  const sum = values.reduce((total, value) => total + (Number(value) || 0), 0);
  return Math.max(0, Math.min(100, sum / values.length));
});

const warningsTone = computed<'neutral' | 'warning' | 'danger'>(() => {
  const hasPrecipitation = warnings.value.some((text) => text.startsWith('خطر رسوب:'));
  if (hasPrecipitation) return 'danger';
  if (!result.value?.is_converged || accuracy.value < 85 || badElementsCount.value > 0) return 'warning';
  return 'neutral';
});

const warningsBadge = computed(() => {
  if (warningsTone.value === 'danger') return 'نیاز به توجه';
  if (warningsTone.value === 'warning') return 'قابل بهبود';
  return 'مطلوب';
});

const warningsSubtitle = computed(() => {
  if (warningsTone.value === 'danger') return 'خطر رسوب شیمیایی شناسایی شد';
  if (warningsTone.value === 'warning') return 'چند نکته برای بهبود ترکیب وجود دارد';
  return 'مشکلی در ترکیب یافت نشد';
});

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
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
