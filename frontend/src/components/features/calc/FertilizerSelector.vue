<!-- frontend/src/components/features/calc/FertilizerSelector.vue -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">انتخاب کود</h3>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="toggleSelectAll"
          class="px-3 py-1.5 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors font-medium"
        >
          {{ isAllSelected ? 'لغو انتخاب همه' : 'انتخاب همه' }}
        </button>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {{ selectedFertilizers.length }} از {{ userFertilizersList.length }} کود
        </span>
      </div>
    </div>

    <!-- جستجو -->
    <div class="relative mb-4">
      <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="جستجوی نام کود یا برند..."
        class="w-full pr-10 pl-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
      />
    </div>

    <!-- آمار -->
    <div class="flex items-center gap-3 mb-3 text-xs text-gray-500 dark:text-gray-400">
      <span>تعداد کل کودهای شخصی: {{ userFertilizersList.length }}</span>
      <span class="text-gray-300 dark:text-gray-600">|</span>
      <span>کودهای معمولی: {{ normalFertilizersCount }}</span>
      <span class="text-gray-300 dark:text-gray-600">|</span>
      <span>اسیدها: {{ acidFertilizersCount }}</span>
    </div>

    <!-- لیست کودها -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[350px] overflow-y-auto custom-scrollbar p-1">
      <div
        v-for="fertilizer in filteredFertilizers"
        :key="fertilizer.id"
        @click="toggleSelection(fertilizer.id)"
        class="relative cursor-pointer rounded-lg border-2 p-3 transition-all hover:shadow-md"
        :class="selectedFertilizers.includes(fertilizer.id)
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-sm'
          : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-primary-300 dark:hover:border-primary-700'"
      >
        <!-- Checkbox -->
        <div class="absolute top-2 left-2">
          <div
            class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
            :class="selectedFertilizers.includes(fertilizer.id)
              ? 'bg-primary-500 border-primary-500'
              : 'bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600'"
          >
            <svg
              v-if="selectedFertilizers.includes(fertilizer.id)"
              class="w-3 h-3 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
        </div>

        <div class="pr-6">
          <p class="font-medium text-sm text-gray-900 dark:text-white truncate">
            {{ fertilizer.name }}
          </p>
          <div class="flex items-center gap-2 mt-1 flex-wrap">
            <span
              class="text-[10px] px-1.5 py-0.5 rounded"
              :class="fertilizer.isAcid
                ? 'bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400'
                : 'bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-400'"
            >
              {{ fertilizer.isAcid ? 'اسید' : 'کود' }}
            </span>
            <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
              {{ fertilizer.brand }}
            </span>
            <span class="text-[10px] text-gray-500 dark:text-gray-400">
              {{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }} تومان/kg
            </span>
            <span v-if="fertilizer.concentration && fertilizer.concentration < 100" class="text-[10px] text-warning-600 dark:text-warning-400 bg-warning-50 dark:bg-warning-900/30 px-1.5 py-0.5 rounded">
              {{ fertilizer.concentration }}% خلوص
            </span>
          </div>
          <div v-if="getMainElements(fertilizer).length > 0" class="flex flex-wrap gap-1 mt-2">
            <span
              v-for="el in getMainElements(fertilizer)"
              :key="el.symbol"
              class="text-[9px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
            >
              {{ el.symbol }}: {{ el.value }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- پیام خالی -->
    <div v-if="filteredFertilizers.length === 0" class="text-center py-8">
      <svg class="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
      </svg>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        {{ searchQuery ? 'هیچ کودی با این مشخصات یافت نشد' : 'هیچ کود شخصی در دسترس نیست' }}
      </p>
      <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
        {{ searchQuery ? 'عبارت جستجو را تغییر دهید' : 'لطفاً ابتدا کودهای خود را در بخش پایگاه داده کود اضافه کنید' }}
      </p>
    </div>

    <!-- راهنمای انتخاب -->
    <div class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 text-center text-xs text-gray-400 dark:text-gray-500">
      با کلیک روی هر کود، آن را انتخاب یا لغو انتخاب کنید
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// ===== Types =====
interface Fertilizer {
  id: string;
  name: string;
  brand?: string;
  isAcid: boolean;
  pricePerKg: number;
  concentration?: number;
  elements: Record<string, number>;
  isSystemDefault: boolean;
}

// ===== Props =====
interface Props {
  fertilizers: Fertilizer[];
  selectedFertilizers: string[];
}

const props = defineProps<Props>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
}>();

// ===== State =====
const searchQuery = ref('');

// ===== Computed =====

/**
 * فقط کودهای شخصی کاربر (isSystemDefault === false)
 */
const userFertilizersList = computed(() => {
  return props.fertilizers.filter((f: Fertilizer) => !f.isSystemDefault);
});

/**
 * تعداد کودهای معمولی (غیر اسید)
 */
const normalFertilizersCount = computed(() => {
  return userFertilizersList.value.filter((f: Fertilizer) => !f.isAcid).length;
});

/**
 * تعداد اسیدها
 */
const acidFertilizersCount = computed(() => {
  return userFertilizersList.value.filter((f: Fertilizer) => f.isAcid).length;
});

/**
 * فیلتر شده بر اساس جستجو
 */
const filteredFertilizers = computed(() => {
  let result = userFertilizersList.value;
  
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase();
    result = result.filter((f: Fertilizer) =>
      f.name.toLowerCase().includes(query) ||
      (f.brand && f.brand.toLowerCase().includes(query))
    );
  }
  
  return result;
});

/**
 * آیا همه کودهای شخصی انتخاب شده‌اند؟
 */
const isAllSelected = computed(() => {
  return userFertilizersList.value.length > 0 && 
         props.selectedFertilizers.length === userFertilizersList.value.length;
});

// ===== Methods =====

/**
 * دریافت عناصر اصلی یک کود (حداکثر 3 عنصر با بیشترین درصد)
 */
const getMainElements = (fertilizer: Fertilizer): Array<{ symbol: string; value: number }> => {
  if (!fertilizer.elements) return [];
  
  const entries = Object.entries(fertilizer.elements)
    .filter(([_, value]) => value && value > 0)
    .map(([symbol, value]) => ({ symbol, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);
  
  return entries;
};

/**
 * انتخاب/عدم انتخاب یک کود
 * با هر کلیک، لیست انتخاب‌ها به‌روزرسانی می‌شود
 */
const toggleSelection = (id: string) => {
  const current = [...props.selectedFertilizers];
  const index = current.indexOf(id);
  
  if (index === -1) {
    current.push(id);
  } else {
    current.splice(index, 1);
  }
  
  // ارسال لیست به‌روز شده به والد
  emit('update:selectedFertilizers', current);
};

/**
 * انتخاب همه / لغو انتخاب همه
 */
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    emit('update:selectedFertilizers', []);
  } else {
    const allIds = userFertilizersList.value.map((f: Fertilizer) => f.id);
    emit('update:selectedFertilizers', allIds);
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
</style>