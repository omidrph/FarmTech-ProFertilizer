<!-- frontend/src/components/features/calc/ResultFertilizerTable.vue -->
<!--
  جدول مقادیر کود، گروه‌بندی‌شده بر اساس مخزن.
  دسکتاپ: جدول | موبایل: کارت (بدون اسکرول افقی)
  وزن هر کود مستقیماً قابل ویرایش است.
-->
<template>
  <div class="space-y-3">
    <!-- سوییچ واحد نمایش -->
    <div class="flex items-center justify-between gap-3 flex-wrap">
      <div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden text-xs">
        <button
          v-for="mode in modes"
          :key="mode.key"
          type="button"
          @click="activeMode = mode.key"
          class="px-3 py-1.5 font-medium transition-colors"
          :class="activeMode === mode.key
            ? 'bg-primary-600 text-white'
            : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'"
        >{{ mode.label }}</button>
      </div>
      <p class="text-[11px] text-gray-500 dark:text-gray-400">
        {{ activeModeHint }}
      </p>
    </div>

    <!-- گروه‌های مخزن -->
    <div v-for="group in groups" :key="group.tank" class="rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="px-3 py-2 flex items-center justify-between" :class="tankHeaderClass(group.tank)">
        <span class="text-xs font-bold">{{ group.title }}</span>
        <span class="text-[11px] opacity-80">{{ group.items.length }} کود</span>
      </div>

      <!-- دسکتاپ: ردیف‌های هم‌ارتفاع (۵۲px) در هر دو حالت نمایش -->
      <div class="hidden sm:block">
        <div class="grid grid-cols-[minmax(0,1fr)_230px_140px] bg-gray-50 dark:bg-gray-700/40 text-xs font-semibold text-gray-600 dark:text-gray-300">
          <div class="px-4 py-2.5 text-right">نام کود</div>
          <div class="px-3 py-2.5 text-center">{{ weightColumnLabel }}</div>
          <div class="px-4 py-2.5 text-left">هزینه (تومان)</div>
        </div>
        <div class="divide-y divide-gray-100 dark:divide-gray-700">
          <div v-for="item in group.items" :key="item.id" class="grid grid-cols-[minmax(0,1fr)_230px_140px] items-center h-[52px] hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
            <div class="px-4 flex items-center gap-1.5 min-w-0">
              <span class="font-medium text-sm text-gray-900 dark:text-white truncate">{{ item.name }}</span>
              <span v-if="item.isAcid || item.isBase" class="text-[10px] px-1.5 py-0.5 rounded flex-shrink-0" :class="item.isBase ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'">{{ item.isBase ? 'باز' : 'اسید' }}</span>
              <span v-if="item.fixed" class="text-[10px] px-1.5 py-0.5 rounded flex-shrink-0 bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300" title="مقدار را خودتان تعیین کرده‌اید">مقدار شما</span>
            </div>
            <div class="px-3 flex items-center justify-center gap-2">
              <span v-if="litersText(item)" class="text-[10px] text-gray-400 whitespace-nowrap">{{ litersText(item) }}</span>
              <div class="amount-pill" :class="activeMode === 'stock' ? 'amount-pill-edit' : ''">
                <input
                  v-if="activeMode === 'stock'"
                  type="number" step="0.001" min="0" dir="ltr"
                  class="w-20 text-center tabular-nums bg-transparent outline-none text-sm font-semibold text-gray-900 dark:text-white"
                  :value="displayWeight(item)"
                  @input="onWeightInput(item.id, $event)"
                  @change="onWeightCommit(item.id)"
                  @keyup.enter="onWeightCommit(item.id)"
                />
                <span v-else class="w-20 text-center tabular-nums text-sm font-semibold text-gray-900 dark:text-white" dir="ltr">{{ formatNumber(convertAmount(item), item.isVolume ? 1 : 2) }}</span>
                <span class="amount-unit">{{ unitText(item) }}</span>
              </div>
            </div>
            <div class="px-4 text-left tabular-nums text-sm text-gray-700 dark:text-gray-300" dir="ltr">{{ formatCurrency(item.cost) }}</div>
          </div>
        </div>
      </div>

      <!-- موبایل -->
      <div class="sm:hidden divide-y divide-gray-100 dark:divide-gray-700">
        <div v-for="item in group.items" :key="item.id" class="px-3 py-3">
          <div class="flex items-center justify-between gap-2">
            <span class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ item.name }}</span>
            <span v-if="item.isAcid || item.isBase" class="text-[10px] px-1.5 py-0.5 rounded flex-shrink-0" :class="item.isBase ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'">{{ item.isBase ? 'باز' : 'اسید' }}</span>
          </div>
          <div class="flex items-center justify-between mt-2 gap-2">
            <span class="text-[11px] text-gray-500 dark:text-gray-400">{{ weightColumnLabel }}</span>
            <div class="amount-pill" :class="activeMode === 'stock' ? 'amount-pill-edit' : ''">
              <input v-if="activeMode === 'stock'" type="number" step="0.001" min="0" dir="ltr" class="w-20 text-center tabular-nums bg-transparent outline-none text-sm font-semibold text-gray-900 dark:text-white" :value="displayWeight(item)" @input="onWeightInput(item.id, $event)" @change="onWeightCommit(item.id)" />
              <span v-else class="w-20 text-center tabular-nums text-sm font-semibold text-gray-900 dark:text-white" dir="ltr">{{ formatNumber(convertAmount(item), item.isVolume ? 1 : 2) }}</span>
              <span class="amount-unit">{{ unitText(item) }}</span>
            </div>
          </div>
          <div class="flex items-center justify-between mt-1.5">
            <span class="text-[11px] text-gray-500 dark:text-gray-400">هزینه<template v-if="litersText(item)"> · {{ litersText(item) }}</template></span>
            <span class="tabular-nums text-xs text-gray-700 dark:text-gray-300">{{ formatCurrency(item.cost) }} تومان</span>
          </div>
        </div>
      </div>
    </div>

    <!-- جمع‌بندی -->
    <div class="flex items-center justify-between gap-3 flex-wrap rounded-xl bg-gray-50 dark:bg-gray-700/40 border border-gray-200 dark:border-gray-700 px-4 py-3">
      <span class="text-sm text-gray-600 dark:text-gray-300">مجموع هزینه ترکیب</span>
      <span class="text-base font-bold text-emerald-600 dark:text-emerald-400 tabular-nums">
        {{ formatCurrency(result.cost_total) }} تومان
      </span>
    </div>

    <p v-if="unusedCount > 0" class="text-xs text-gray-500 dark:text-gray-400">
      {{ unusedCount }} کود انتخاب شده بود اما در ترکیب نهایی وزنی نگرفت.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import type { OptimizationResponse } from '@/types';

interface RowItem {
  id: string;
  name: string;
  isAcid: boolean;
  isBase: boolean;
  /** 🆕 کود مایع با چگالی معتبر: مقدار به میلی‌لیتر نمایش داده/ویرایش می‌شود */
  isVolume: boolean;
  density: number;
  fixed: boolean;
  weight: number;
  cost: number;
  tank: string;
}

const props = defineProps<{
  result: OptimizationResponse;
  fertilizers: any[];
  tankVolume: number;
}>();

const emit = defineEmits<{
  (e: 'update-weight', payload: { fertilizerId: string; weight: number }): void;
}>();

// ===== واحد نمایش =====
type Mode = 'stock' | 'per1000';
const modes: Array<{ key: Mode; label: string }> = [
  { key: 'stock', label: 'مقدار در استوک' },
  { key: 'per1000', label: 'مقدار در ۱۰۰۰ لیتر محلول نهایی' }
];
const activeMode = ref<Mode>('stock');

const activeModeHint = computed(() =>
  activeMode.value === 'stock'
    ? 'مقداری که باید داخل سطل استوک بریزید (قابل ویرایش)'
    : 'معادل همان مقدار به ازای هر ۱۰۰۰ لیتر محلول آماده مصرف'
);

const weightColumnLabel = computed(() =>
  activeMode.value === 'stock' ? 'مقدار' : 'مقدار / ۱۰۰۰ لیتر'
);

// 🆕 واحد هر ردیف: جامد → گرم ، مایع → میلی‌لیتر
const unitText = (item: RowItem): string => (item.isVolume ? 'میلی‌لیتر' : 'گرم');

/** کود مایع بزرگ‌تر از ۱ لیتر: معادل لیتری هم کنار میلی‌لیتر نمایش داده می‌شود */
const litersText = (item: RowItem): string => {
  if (!item.isVolume) return '';
  const ml = convertAmount(item);
  return ml >= 1000 ? `≈ ${formatNumber(ml / 1000, 2)} لیتر` : '';
};

/** مقدار نمایشی (در مود استوک یا در ۱۰۰۰ لیتر) با تبدیل جرم → حجم برای مایعات */
const convertAmount = (item: RowItem): number => {
  const grams = convertWeight(item.weight);
  return item.isVolume ? grams / item.density : grams;
};

const convertWeight = (weight: number): number => {
  if (activeMode.value === 'stock') return weight;
  const volume = Number(props.tankVolume) || 0;
  if (volume <= 0) return weight;
  return (weight / volume) * 1000;
};

// ===== ویرایش وزن =====
const editedWeights = ref<Record<string, number>>({});
watch(() => props.result, () => { editedWeights.value = {}; });

// editedWeights: «مقدار نمایشی» ویرایش‌شده (گرم یا میلی‌لیتر، بسته به نوع کود)
const displayWeight = (item: RowItem): number =>
  editedWeights.value[item.id] ?? Number((item.isVolume ? item.weight / item.density : item.weight).toFixed(3));

const onWeightInput = (fertilizerId: string, event: Event) => {
  const value = parseFloat((event.target as HTMLInputElement).value);
  editedWeights.value[fertilizerId] = isNaN(value) ? 0 : value;
};

const onWeightCommit = (fertilizerId: string) => {
  const edited = editedWeights.value[fertilizerId];
  if (edited === undefined) return;
  const row = rows.value.find((r) => r.id === fertilizerId);
  // مایع: میلی‌لیتر → گرم با چگالی ؛ بک‌اند همیشه گرم می‌گیرد
  const newWeight = row?.isVolume ? edited * row.density : edited;
  const oldWeight = props.result.weights?.[fertilizerId] ?? 0;
  if (Math.abs(newWeight - oldWeight) < 0.0005) return;
  emit('update-weight', { fertilizerId, weight: newWeight });
};

// ===== نگاشت مخزن هر کود =====
const tankMap = computed(() => {
  const map: Record<string, string> = {};
  const data: any = props.result?.reservoir_data;
  if (!data) return map;

  (['A', 'B', 'C'] as const).forEach((tank) => {
    const list = data[tank];
    if (!Array.isArray(list)) return;
    for (const item of list) {
      if (item?.fertilizer_id) {
        map[item.fertilizer_id] = tank;
      } else if (item?.name) {
        const fert = props.fertilizers.find((f) => f.name === item.name);
        if (fert) map[fert.id] = tank;
      }
    }
  });
  return map;
});

// ===== ردیف‌ها =====
const rows = computed<RowItem[]>(() => {
  const weights = props.result?.weights || {};
  return Object.entries(weights)
    .filter(([, weight]) => typeof weight === 'number' && weight > 0)
    .map(([id, weight]) => {
      const fert = props.fertilizers.find((f) => f.id === id);
      const density = Number(fert?.densityGMl) || 0;
      return {
        id,
        name: fert?.name || id,
        isAcid: !!fert?.isAcid,
        isBase: !!fert?.isBase,
        isVolume: fert?.form === 'liquid' && density > 0,
        density,
        fixed: !!(props.result as any)?.fixed_fertilizers?.[id],
        weight: weight as number,
        cost: fert ? ((weight as number) / 1000) * (fert.pricePerKg || 0) : 0,
        tank: tankMap.value[id] || 'other'
      };
    })
    .sort((a, b) => b.weight - a.weight);
});

const groups = computed(() => {
  const order = ['A', 'B', 'C', 'other'];
  const titles: Record<string, string> = {
    A: 'مخزن A',
    B: 'مخزن B',
    C: 'مخزن C (اسید)',
    other: 'بدون مخزن مشخص'
  };

  return order
    .map((tank) => {
      const items = rows.value.filter((row) => row.tank === tank);
      return {
        tank,
        title: titles[tank],
        items,
        totalWeight: items.reduce((sum, item) => sum + item.weight, 0)
      };
    })
    .filter((group) => group.items.length > 0);
});

const unusedCount = computed(() => {
  const weights = props.result?.weights || {};
  const total = Object.keys(weights).length;
  return Math.max(0, total - rows.value.length);
});

// ===== کمکی‌ها =====
const tankHeaderClass = (tank: string): string => {
  const map: Record<string, string> = {
    A: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300',
    B: 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300',
    C: 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300',
    other: 'bg-gray-50 dark:bg-gray-700/40 text-gray-600 dark:text-gray-300'
  };
  return map[tank] || map.other;
};

const formatNumber = (value: number, digits = 2): string => {
  const parsed = Number(value);
  return isFinite(parsed) ? parsed.toFixed(digits) : '—';
};

const formatCurrency = (value: unknown): string => {
  const parsed = Number(value);
  if (!isFinite(parsed)) return '۰';
  return Math.round(parsed).toLocaleString('fa-IR');
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
.amount-pill { @apply inline-flex items-center h-9 pr-2 pl-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/40; }
.amount-pill-edit { @apply bg-white dark:bg-gray-900 hover:border-gray-300 focus-within:border-primary-500 focus-within:ring-2 focus-within:ring-primary-500/30; }
.amount-unit { @apply text-[11px] text-gray-500 dark:text-gray-400 mr-1.5 min-w-[52px] text-right; }
</style>
