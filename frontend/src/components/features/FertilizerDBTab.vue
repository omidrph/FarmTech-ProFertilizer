<template>
  <div class="space-y-6">
    <!-- هدر با توضیحات -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm">
        اطلاعات مربوط به کودها در جدول زیر قابل مشاهده و ویرایش است. با فشردن دکمه "افزودن" می‌توانید کود جدید اضافه کنید.
      </p>
    </div>

    <!-- دکمه‌های اقدام -->
    <div class="flex flex-wrap gap-3">
      <button 
        @click="emit('show-add-modal')" 
        class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        افزودن کود جدید
      </button>
      <button 
        @click="refreshFertilizers" 
        class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors"
        :disabled="isLoading"
      >
        <span v-if="!isLoading">🔄 بروزرسانی از دیتابیس</span>
        <span v-else>در حال بارگذاری...</span>
      </button>
    </div>

    <!-- پیام خالی بودن دیتابیس -->
    <div v-if="fertilizers.length === 0 && !isLoading" class="bg-yellow-50 dark:bg-yellow-900/20 border-r-4 border-yellow-500 rounded-lg p-4">
      <p class="text-yellow-700 dark:text-yellow-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <span>هیچ کودی در دیتابیس وجود ندارد. لطفاً از دکمه "افزودن کود جدید" برای اضافه کردن کود استفاده کنید.</span>
      </p>
    </div>

    <!-- جدول کودها -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="overflow-x-auto">
        <table class="w-full text-xs border-collapse">
          <thead>
            <tr>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-right min-w-[120px]">
                نام کود
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[100px]">
                قیمت (تومان)
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">
                نوع
              </th>
              <th v-for="el in elements" :key="el" class="px-1 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[55px]">
                {{ el }}
              </th>
              <th class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[90px]">
                عملیات
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fertilizer in fertilizers" :key="fertilizer.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <td class="px-2 py-2 border border-gray-100 dark:border-gray-700 text-right font-medium">
                {{ fertilizer.name }}
              </td>
              <td class="px-2 py-2 border border-gray-100 dark:border-gray-700 text-center">
                {{ Number(fertilizer.pricePerKg).toLocaleString() }}
              </td>
              <td class="px-2 py-2 border border-gray-100 dark:border-gray-700 text-center">
                <span v-if="fertilizer.isAcid" class="px-2 py-0.5 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded-full text-xs">
                  اسید ({{ fertilizer.acidType || 'نامشخص' }})
                </span>
                <span v-else class="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-xs">
                  کود
                </span>
              </td>
              <td v-for="el in elements" :key="el" class="px-1 py-2 border border-gray-100 dark:border-gray-700 text-center">
                {{ fertilizer.elements && fertilizer.elements[el] ? Number(fertilizer.elements[el]).toFixed(2) : '0.00' }}
              </td>
              <td class="px-2 py-2 border border-gray-100 dark:border-gray-700 text-center">
                <button 
                  @click="editFertilizer(fertilizer.id)" 
                  class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 transition-colors px-1 text-sm"
                  title="ویرایش"
                >
                  ✏️
                </button>
                <button 
                  @click="deleteFertilizer(fertilizer.id)" 
                  class="text-danger-600 hover:text-danger-800 dark:text-danger-400 dark:hover:text-danger-300 transition-colors px-1 text-sm"
                  title="حذف"
                >
                  🗑️
                </button>
              </td>
            </tr>
            <tr v-if="fertilizers.length === 0 && !isLoading">
              <td :colspan="elements.length + 4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                <div class="flex flex-col items-center gap-2">
                  <svg class="w-12 h-12 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                  </svg>
                  <span>هیچ کودی در دیتابیس وجود ندارد.</span>
                  <span class="text-sm">دکمه "افزودن کود جدید" را بزنید تا اولین کود را اضافه کنید.</span>
                </div>
              </td>
            </tr>
            <tr v-if="isLoading">
              <td :colspan="elements.length + 4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                <div class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>در حال بارگذاری...</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- آمار -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-wrap gap-6 text-sm">
        <div>
          <span class="text-gray-500 dark:text-gray-400">تعداد کل کودها:</span>
          <span class="font-bold text-gray-900 dark:text-white mr-1">{{ fertilizers.length }}</span>
        </div>
        <div>
          <span class="text-gray-500 dark:text-gray-400">کودهای معمولی:</span>
          <span class="font-bold text-green-600 dark:text-green-400 mr-1">{{ normalFertilizersCount }}</span>
        </div>
        <div>
          <span class="text-gray-500 dark:text-gray-400">اسیدها:</span>
          <span class="font-bold text-yellow-600 dark:text-yellow-400 mr-1">{{ acidFertilizersCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';

// ===== Props =====
const props = defineProps<{
  fertilizers: any[];
}>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'show-add-modal'): void;
  (e: 'delete-fertilizer', id: string): void;
  (e: 'update:fertilizers', value: any[]): void;
}>();

// ===== Store =====
const fertilizerStore = useFertilizerStore();

// ===== State =====
const isLoading = ref(false);
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Computed =====
const normalFertilizersCount = computed(() => {
  return props.fertilizers.filter((f: any) => !f.isAcid).length;
});

const acidFertilizersCount = computed(() => {
  return props.fertilizers.filter((f: any) => f.isAcid).length;
});

// ===== Methods =====

// بروزرسانی از دیتابیس (جایگزین loadSampleFertilizers)
const refreshFertilizers = async () => {
  isLoading.value = true;
  try {
    await fertilizerStore.loadFertilizers();
    emit('update:fertilizers', fertilizerStore.fertilizers);
  } catch (error) {
    console.error('Error refreshing fertilizers:', error);
  } finally {
    isLoading.value = false;
  }
};

// حذف کود
const deleteFertilizer = (id: string) => {
  if (confirm('آیا از حذف این کود اطمینان دارید؟')) {
    emit('delete-fertilizer', id);
  }
};

// ویرایش کود
const editFertilizer = (id: string) => {
  // TODO: پیاده‌سازی ویرایش کود
  alert('ویرایش کود در حال توسعه است.');
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>