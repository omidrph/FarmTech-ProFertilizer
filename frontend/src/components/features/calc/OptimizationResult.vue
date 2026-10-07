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

      <!-- 🆕 اصلاح pH اعمال‌شده در این محاسبه (از تب PH) -->
      <PhAdjustmentBanner v-if="result.ph_adjustment" :adjustment="result.ph_adjustment" class="mt-3" />
      <div
        v-if="phStale"
        class="mt-3 rounded-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 text-xs leading-6 text-amber-800 dark:text-amber-200"
      >
        {{ phStaleText }}
      </div>
    </ResultAccordion>

    <!-- ============================================================ -->
    <!-- عناصر هدف (همان ظاهر صفحهٔ خانه: حلقه‌های دایره‌ای؛ ۸ مورد و «نمایش همه») -->
    <!-- ============================================================ -->
    <HomeElementRings :target-values="targetValues" :concentrations="result.concentrations" />
    <p v-if="result.ph_adjustment" class="-mt-1 px-1 text-[11px] text-sky-700 dark:text-sky-400">
      این مقادیر (و تعادل یونی و EC) شامل سهم اسید/باز تنظیم pH هم هستند.
    </p>

    <!-- ============================================================ -->
    <!-- تعادل یونی (همان ظاهر صفحهٔ خانه: کاتیون آبی، آنیون قرمز) -->
    <!-- ============================================================ -->
    <HomeIonBalance
      v-if="result.ion_balance"
      :cation="Number(result.ion_balance.cation) || 0"
      :anion="Number(result.ion_balance.anion) || 0"
      :balanced="!!result.ion_balance.isBalanced"
    />

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
import HomeElementRings from '../home/HomeElementRings.vue';
import HomeIonBalance from '../home/HomeIonBalance.vue';
import ResultWarnings from './ResultWarnings.vue';
import PhAdjustmentBanner from './PhAdjustmentBanner.vue';
import type { PhActiveSummary } from '@/services/apiService';

const props = withDefaults(
  defineProps<{
    result: OptimizationResponse | null;
    fertilizers: any[];
    targetValues: Record<string, number>;
    tankVolume?: number;
    activePh?: PhActiveSummary | null;
  }>(),
  { tankVolume: 1000, activePh: null }
);

defineEmits<{
  (e: 'update-weight', payload: { fertilizerId: string; weight: number }): void;
  (e: 'go-to-selection'): void;
}>();

const result = computed(() => props.result);

// 🆕 آیا اصلاح pH فعال گزارش با آنچه در این نتیجه اعمال شده یکی است؟
// (اگر کاربر در تب PH اصلاحی را اعمال/لغو/عوض کرده باشد، نتیجه باید دوباره محاسبه شود)
const phStale = computed(() => {
  const applied = result.value?.ph_adjustment ?? null;
  const active = props.activePh ?? null;
  if (!applied && !active) return false;
  if (!applied || !active) return true;
  return applied.id !== active.id || (applied.updated_at ?? null) !== (active.updated_at ?? null);
});

const phStaleText = computed(() =>
  props.activePh
    ? 'اصلاح pH فعال این گزارش با این نتیجه هم‌خوان نیست؛ برای اعمال آن دوباره «محاسبه» را بزنید.'
    : 'اصلاح pH که در این نتیجه اعمال شده بود دیگر فعال نیست؛ برای حذف سهم آن دوباره «محاسبه» را بزنید.'
);

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
