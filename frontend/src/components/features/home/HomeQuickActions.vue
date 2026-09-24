<!-- frontend/src/components/features/home/HomeQuickActions.vue -->
<!--
  اقدامات سریع بعد از محاسبه
  ------------------------------------------------------------
  - دکمه «محاسبه مجدد»: بدون تغییر صفحه، محاسبه را دوباره اجرا می‌کند
  - دکمه «ویرایش عناصر هدف»: به تب عناصر هدف می‌رود
-->
<template>
  <div class="flex flex-wrap items-center gap-2">
    <button
      type="button"
      @click="handleRecalculate"
      :disabled="isRecalculating"
      class="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
    >
      <svg v-if="!isRecalculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      {{ isRecalculating ? 'در حال محاسبه...' : 'محاسبه مجدد' }}
    </button>

    <button
      type="button"
      @click="emit('edit-targets')"
      :disabled="isRecalculating"
      class="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke-width="2" />
        <circle cx="12" cy="12" r="6" stroke-width="2" />
        <circle cx="12" cy="12" r="2" stroke-width="2" />
      </svg>
      ویرایش عناصر هدف
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';

const emit = defineEmits<{
  (e: 'edit-targets'): void;
}>();

const targetStore = useTargetStore();
const waterStore = useWaterStore();
const calcStore = useCalcStore();
const fertilizerStore = useFertilizerStore();

const isRecalculating = ref(false);

const handleRecalculate = async () => {
  if (isRecalculating.value) return;

  // اطمینان از وجود نیازمندی‌های محاسبه
  const selectedIds = fertilizerStore.selectedFertilizerIds || [];
  const selectedFertilizers = (fertilizerStore.fertilizers || []).filter(
    (f: any) => selectedIds.includes(f.id)
  );

  if (selectedFertilizers.length === 0) {
    // اگر کودی انتخاب نشده، از ردیف‌های محاسبه قبلی استفاده کن
    const fallback = (calcStore as any).lastFertilizersUsed || [];
    if (fallback.length === 0) {
      // در نهایت به تب محاسبه هدایت کن
      emit('edit-targets');
      return;
    }
    await runOptimization(fallback);
    return;
  }

  await runOptimization(selectedFertilizers);
};

const runOptimization = async (fertilizers: any[]) => {
  isRecalculating.value = true;
  try {
    // از همان تنظیمات استوک ذخیره‌شده استفاده کن
    const s = calcStore.stockSettings;

    await calcStore.optimizeFertilizers(
      targetStore.targetElements as Record<string, number>,
      waterStore.waterValues as Record<string, number>,
      fertilizers,
      undefined,
      s.tankVolume,
      s.stockVolume,
      s.injectionRatio
    );
  } catch (err) {
    console.error('Recalculate error:', err);
  } finally {
    isRecalculating.value = false;
  }
};
</script>