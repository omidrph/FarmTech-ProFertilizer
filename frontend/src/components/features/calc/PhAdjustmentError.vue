<!-- frontend/src/components/features/calc/PhAdjustmentError.vue -->
<!--
  «خطای اصلاح pH»: وقتی عناصر واردشده از اسید/باز (مثلاً نیتروژن اسید نیتریک) باعث شود غلظت نهایی
  یک عنصر از هدف بیشتر شود یا عنصری که هدف ندارد وارد محلول شود. عمداً با ظاهر بنفش و جدا از
  هشدارهای عمومی (زرد/قرمز) نمایش داده می‌شود تا با بقیه قاطی نشود.
-->
<template>
  <section v-if="issues.length" class="rounded-xl border-2 border-violet-300 dark:border-violet-700 bg-violet-50 dark:bg-violet-900/15 overflow-hidden" role="alert">
    <header class="flex items-center gap-2.5 px-3.5 py-2.5 bg-violet-100 dark:bg-violet-900/30 border-b border-violet-200 dark:border-violet-800">
      <span class="w-7 h-7 rounded-lg bg-violet-600 text-white flex items-center justify-center flex-shrink-0">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4a2 2 0 001.8-3l-5-9V3" /></svg>
      </span>
      <div class="min-w-0">
        <h4 class="text-sm font-bold text-violet-900 dark:text-violet-100">خطای اصلاح pH</h4>
        <p class="text-[11px] text-violet-700 dark:text-violet-300">مربوط به {{ adjustment.kind === 'acid' ? 'اسید' : 'باز' }} «{{ adjustment.chemical_name }}» که در این محاسبه اعمال شده است</p>
      </div>
    </header>
    <ul class="px-3.5 py-3 space-y-2">
      <li v-for="i in issues" :key="i.element" class="text-xs leading-6 text-violet-900 dark:text-violet-100 flex gap-2">
        <span class="mt-2 w-1.5 h-1.5 rounded-full bg-violet-500 flex-shrink-0"></span>
        <span>
          <strong>{{ i.element }}</strong>:
          <template v-if="i.kind === 'over'">
            اسید/باز {{ fmt(i.added) }} ppm وارد کرده؛ غلظت نهایی {{ fmt(i.actual) }} ppm شد، {{ fmt(i.excess) }} ppm بیشتر از هدف ({{ fmt(i.target) }}).
          </template>
          <template v-else>
            این عنصر هدف ندارد ولی اسید/باز {{ fmt(i.added) }} ppm وارد محلول کرده است.
          </template>
        </span>
      </li>
    </ul>
    <p class="px-3.5 pb-3 text-[11px] leading-5 text-violet-700 dark:text-violet-300">
      راه‌حل: مقدار اسید/باز را در تب «PH» کمتر کنید (نمونهٔ دقیق‌تر یا pH هدف کمی بالاتر)، یا اسیدی با عنصر مفیدتر برای این رسپی انتخاب کنید (مثلاً اسید فسفریک وقتی فسفر کم است). این خطا فقط ناشی از اصلاح pH است و به کودها ربطی ندارد.
    </p>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OptimizationResponse } from '@/types';

type Adjustment = NonNullable<OptimizationResponse['ph_adjustment']>;
const props = defineProps<{
  adjustment: Adjustment;
  concentrations: Record<string, number>;
  targetValues: Record<string, number>;
}>();

const fmt = (n: number) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: 1 }).format(n);

const issues = computed(() => {
  const out: Array<{ element: string; kind: 'over' | 'extra'; added: number; actual: number; target: number; excess: number }> = [];
  for (const [el, added] of Object.entries(props.adjustment.element_contributions || {})) {
    const add = Number(added);
    if (!(add > 0)) continue;
    const target = Number(props.targetValues?.[el] || 0);
    const actual = Number(props.concentrations?.[el] || 0);
    if (target > 0) {
      const excess = actual - target;
      if (excess > Math.max(2, target * 0.05)) out.push({ element: el, kind: 'over', added: add, actual, target, excess });
    } else if (add > 2) {
      out.push({ element: el, kind: 'extra', added: add, actual, target: 0, excess: add });
    }
  }
  return out;
});
</script>
