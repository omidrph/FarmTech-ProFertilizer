<!-- frontend/src/components/features/calc/AcidAmountModal.vue -->
<!--
  مقدار اسید/باز برای کل مخزن (هنگام انتخاب در «انتخاب کود»)
  ------------------------------------------------------------
  اگر کاربر از قبل می‌داند برای این رسپی چقدر اسید/باز لازم است، همین‌جا وارد می‌کند.
  بهینه‌ساز این مقدار را تغییر نمی‌دهد؛ عناصر آن از هدف کم می‌شود و سایر کودها باقی‌مانده را تأمین می‌کنند.
-->
<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="open" class="fixed inset-0 z-[70] flex items-end sm:items-center justify-center p-0 sm:p-4" @keydown.esc="$emit('cancel')">
        <div class="absolute inset-0 bg-gray-900/50 backdrop-blur-[2px]" @click="$emit('cancel')"></div>

        <div class="relative w-full sm:max-w-md bg-white dark:bg-gray-800 rounded-t-2xl sm:rounded-2xl shadow-2xl max-h-[92vh] overflow-y-auto" role="dialog" aria-modal="true">
          <div class="px-5 pt-5 pb-3 flex items-start gap-3 border-b border-gray-100 dark:border-gray-700">
            <span class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
              :class="fertilizer?.isBase ? 'bg-sky-100 text-sky-600 dark:bg-sky-900/30 dark:text-sky-300' : 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-300'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4a2 2 0 001.8-3l-5-9V3" /></svg>
            </span>
            <div class="min-w-0 flex-1">
              <h3 class="text-base font-bold text-gray-900 dark:text-white">مقدار {{ kindWord }} برای مخزن</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ fertilizer?.name }}</p>
            </div>
            <button type="button" class="w-8 h-8 rounded-lg text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700" @click="$emit('cancel')" aria-label="بستن">✕</button>
          </div>

          <div class="p-5 space-y-4">
            <p class="text-xs leading-6 text-gray-600 dark:text-gray-300">
              مقدار {{ kindWord }} را برای <strong>کل مخزن {{ fmt(tankVolume) }} لیتری</strong> وارد کنید.
              همین مقدار در فرمول ثابت می‌ماند و عناصرش از سهم کودهای دیگر کم می‌شود.
              اگر مقدار دقیق را نمی‌دانید، این {{ kindWord }} را اضافه نکنید و بعد از ساخت محلول از تب «PH» استفاده کنید.
            </p>

            <div class="grid grid-cols-[1fr_auto] gap-2">
              <div>
                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">مقدار</label>
                <input ref="inputRef" v-model="amountText" inputmode="decimal" placeholder="مثلاً ۲٫۵"
                  class="w-full px-3 py-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm outline-none focus:ring-2 focus:ring-primary-500"
                  :class="error ? 'border-rose-400' : 'border-gray-200 dark:border-gray-600'" @keydown.enter="confirm" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">واحد</label>
                <select v-model="unit" class="h-[42px] px-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-900 dark:text-gray-100">
                  <option v-for="u in units" :key="u.value" :value="u.value">{{ u.label }}</option>
                </select>
              </div>
            </div>

            <p v-if="error" class="text-xs text-rose-600 dark:text-rose-400">{{ error }}</p>

            <!-- پیش‌نمایش -->
            <div v-if="preview" class="rounded-xl bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 p-3 space-y-1.5">
              <p class="text-[11px] font-semibold text-gray-500 dark:text-gray-400">این مقدار در مخزن چه چیزی وارد می‌کند؟</p>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="row in preview.elements" :key="row.symbol" class="text-[11px] px-2 py-1 rounded-md bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 tabular-nums">
                  {{ row.symbol }} <strong>{{ fmt(row.ppm, 1) }}</strong> ppm
                </span>
                <span v-if="!preview.elements.length" class="text-[11px] text-gray-500">عنصری برای این کود ثبت نشده است.</span>
              </div>
              <p class="text-[11px] text-gray-500 dark:text-gray-400 tabular-nums">
                معادل {{ fmt(preview.per1000, 1) }} گرم محصول در هر ۱۰۰۰ لیتر · جرم کل {{ fmt(preview.grams, 1) }} گرم
              </p>
            </div>
            <p v-if="needsDensity" class="text-[11px] leading-5 text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg px-3 py-2">
              برای مصرف حجمی (لیتر/میلی‌لیتر) باید «چگالی» این کود در پایگاه‌داده کود ثبت شده باشد؛ فعلاً فقط گرم/کیلوگرم ممکن است.
            </p>
          </div>

          <div class="px-5 pb-5 flex flex-col-reverse sm:flex-row gap-2 sm:justify-end">
            <button type="button" @click="$emit('cancel')" class="px-5 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700">انصراف</button>
            <button type="button" @click="confirm" class="px-6 py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium">
              {{ editing ? 'ذخیره مقدار' : 'افزودن با این مقدار' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue';
import type { Fertilizer } from '@/types';
import { amountToGrams, canShowVolume, defaultUnit, unitOptions, type AmountUnit } from '@/utils/fertilizerUnits';

const props = defineProps<{
  open: boolean;
  fertilizer: Fertilizer | null;
  tankVolume: number;
  initial?: { amount: number; unit: AmountUnit } | null;
  editing?: boolean;
}>();
const emit = defineEmits<{
  (e: 'confirm', v: { amount: number; unit: AmountUnit }): void;
  (e: 'cancel'): void;
}>();

const amountText = ref('');
const unit = ref<AmountUnit>('g');
const error = ref('');
const inputRef = ref<HTMLInputElement | null>(null);

const kindWord = computed(() => (props.fertilizer?.isBase ? 'باز' : 'اسید'));
const units = computed(() => unitOptions(props.fertilizer));
const needsDensity = computed(() => props.fertilizer?.form === 'liquid' && !canShowVolume(props.fertilizer));

const fmt = (n: number, d = 0) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: d }).format(n);
const parse = (t: string): number | null => {
  const n = Number(t.replace(/[۰-۹]/g, (c) => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(c))).replace(/٫/g, '.').replace(/,/g, '').trim());
  return Number.isFinite(n) && t.trim() !== '' ? n : null;
};

// نکته: وقتی چند اسید/باز پشت‌سرهم پرسیده می‌شوند، مودال بسته/باز می‌شود ولی در همان تیک Vue
// تغییر «open» را نمی‌بیند؛ پس به تغییر «کود» هم گوش می‌دهیم تا فرم هر بار تازه شود.
watch(
  () => [props.open, props.fertilizer?.id] as const,
  async ([isOpen]) => {
    if (!isOpen) return;
    error.value = '';
    amountText.value = props.initial ? String(props.initial.amount) : '';
    unit.value = props.initial?.unit ?? defaultUnit(props.fertilizer);
    await nextTick();
    inputRef.value?.focus();
  }
);

const grams = computed(() => {
  const a = parse(amountText.value);
  if (a == null || a <= 0) return null;
  return amountToGrams(a, unit.value, props.fertilizer?.densityGMl);
});

const preview = computed(() => {
  const f = props.fertilizer;
  if (!f || grams.value == null || !(props.tankVolume > 0)) return null;
  const purity = (f.concentration || 100) / 100;
  const elements = Object.entries(f.elements || {})
    .filter(([, pct]) => Number(pct) > 0)
    .map(([symbol, pct]) => ({ symbol, ppm: (grams.value as number) * (Number(pct) / 100) * purity * 1000 / props.tankVolume }));
  return { elements, grams: grams.value, per1000: (grams.value * 1000) / props.tankVolume };
});

function confirm() {
  const a = parse(amountText.value);
  if (a == null || a <= 0) {
    error.value = 'یک مقدار بزرگ‌تر از صفر وارد کنید.';
    return;
  }
  if (amountToGrams(a, unit.value, props.fertilizer?.densityGMl) == null) {
    error.value = 'برای واحد حجمی، چگالی کود باید ثبت شده باشد.';
    return;
  }
  emit('confirm', { amount: a, unit: unit.value });
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.tabular-nums { font-variant-numeric: tabular-nums; }
</style>
