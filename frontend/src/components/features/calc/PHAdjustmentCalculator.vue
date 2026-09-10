<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1 flex items-center gap-2">
      <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
      </svg>
      ماشین‌حساب اصلاح pH
    </h4>
    <p class="text-xs text-gray-500 dark:text-gray-400 mb-4">
      پس از ساخت محلول، pH واقعی را با دستگاه pH‑متر اندازه‌گیری کنید و اینجا وارد کنید تا مقدار دقیق اسید یا باز لازم محاسبه شود.
      <span class="text-amber-600 dark:text-amber-400">این محاسبه جایگزین اندازه‌گیری با دستگاه نیست.</span>
    </p>

    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">pH فعلی (اندازه‌گیری‌شده)</label>
        <input
          type="number"
          step="0.01"
          min="0"
          max="14"
          v-model.number="currentPh"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">pH هدف</label>
        <input
          type="number"
          step="0.01"
          min="0"
          max="14"
          v-model.number="targetPh"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">قلیائیت آب (ppm CaCO₃)</label>
        <input
          type="number"
          step="1"
          min="0"
          v-model.number="alkalinity"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">حجم مخزن (لیتر)</label>
        <input
          type="number"
          step="1"
          min="1"
          v-model.number="tankVolume"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        />
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3 mb-4">
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نوع اسید/باز</label>
        <select
          v-model="productType"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        >
          <option value="HNO3">اسید نیتریک (HNO3)</option>
          <option value="H3PO4">اسید فسفریک (H3PO4)</option>
          <option value="H2SO4">اسید سولفوریک (H2SO4)</option>
          <option value="KOH">هیدروکسید پتاسیم (KOH) - باز</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">درصد خلوص محصول (٪)</label>
        <input
          type="number"
          step="1"
          min="1"
          max="100"
          v-model.number="productConcentration"
          class="w-full px-2.5 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        />
      </div>
    </div>

    <button
      @click="calculate"
      :disabled="isCalculating"
      class="w-full sm:w-auto px-5 py-2.5 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white rounded-lg transition-colors text-sm font-medium flex items-center justify-center gap-2"
    >
      <svg v-if="isCalculating" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
      محاسبه مقدار اسید/باز لازم
    </button>

    <!-- نتیجه -->
    <div v-if="result" class="mt-4 p-4 rounded-lg" :class="result.needs_acid ? 'bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800' : 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'">
      <div v-if="result.type_mismatch_warning" class="mb-3 p-2 rounded bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-sm font-medium">
        ⚠️ {{ result.type_mismatch_warning }}
      </div>
      <div v-else class="flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            برای رساندن pH از {{ result.ph_current.toFixed(2) }} به {{ result.ph_target.toFixed(2) }}:
          </p>
          <p class="text-lg font-bold" :class="result.needs_acid ? 'text-amber-700 dark:text-amber-400' : 'text-blue-700 dark:text-blue-400'">
            {{ result.grams_needed.toFixed(2) }} گرم {{ result.product_name }}
          </p>
          <p v-if="result.estimated_cost" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            هزینه تخمینی: {{ result.estimated_cost.toLocaleString('fa-IR') }} تومان
          </p>
        </div>
      </div>
      <div class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 flex items-start gap-2">
        <svg class="w-3.5 h-3.5 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ result.safety_instruction }}</span>
      </div>
    </div>

    <div v-if="errorMessage" class="mt-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-sm">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import apiService from '@/services/apiService';

// ===== Props =====
const props = defineProps<{
  // مقادیر اولیه پیشنهادی (از تب محاسبه کود، اگر موجود باشد)
  initialTargetPh?: number;
  initialAlkalinity?: number;
  initialTankVolume?: number;
}>();

// ===== State =====
const currentPh = ref<number>(7.0);
const targetPh = ref<number>(props.initialTargetPh ?? 6.0);
const alkalinity = ref<number>(props.initialAlkalinity ?? 0);
const tankVolume = ref<number>(props.initialTankVolume ?? 1000);
const productType = ref<string>('HNO3');
const productConcentration = ref<number>(63);

const isCalculating = ref(false);
const errorMessage = ref<string | null>(null);
const result = ref<any>(null);

// همگام‌سازی با مقادیر بیرونی در صورت تغییر (مثلاً وقتی کاربر تنظیمات استوک را عوض می‌کند)
watch(() => props.initialTankVolume, (v) => { if (v) tankVolume.value = v; });
watch(() => props.initialAlkalinity, (v) => { if (v !== undefined) alkalinity.value = v; });
watch(() => props.initialTargetPh, (v) => { if (v !== undefined) targetPh.value = v; });

// پیش‌فرض درصد خلوص متناسب با نوع محصول انتخابی
watch(productType, (type) => {
  if (type === 'HNO3') productConcentration.value = 63;
  else if (type === 'H3PO4') productConcentration.value = 75;
  else if (type === 'H2SO4') productConcentration.value = 98;
  else if (type === 'KOH') productConcentration.value = 100;
});

const calculate = async () => {
  errorMessage.value = null;
  result.value = null;
  isCalculating.value = true;
  try {
    const res = await apiService.calculatePHAdjustment({
      current_ph: currentPh.value,
      target_ph: targetPh.value,
      alkalinity_ppm_caco3: alkalinity.value,
      tank_volume: tankVolume.value,
      acid_or_base_type: productType.value,
      product_concentration_percent: productConcentration.value
    });
    result.value = res;
  } catch (error: any) {
    errorMessage.value = error?.response?.data?.detail || 'خطا در محاسبه اصلاح pH';
  } finally {
    isCalculating.value = false;
  }
};
</script>
