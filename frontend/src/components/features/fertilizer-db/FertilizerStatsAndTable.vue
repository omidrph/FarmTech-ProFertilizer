<!-- frontend/src/components/features/fertilizer-db/FertilizerStatsAndTable.vue -->
<template>
  <div>
    <!-- ============================================================ -->
    <!-- کارت‌های آماری -->
    <!-- ============================================================ -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کل کودهای شخصی</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white tabular-nums">{{ userFertilizers.length }}</p>
        </div>
      </div>
      
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-success-50 dark:bg-success-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کودهای معمولی</p>
          <p class="text-xl font-bold text-success-600 dark:text-success-400 tabular-nums">{{ normalFertilizersCount }}</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-warning-50 dark:bg-warning-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">اسیدها</p>
          <p class="text-xl font-bold text-warning-600 dark:text-warning-400 tabular-nums">{{ acidFertilizersCount }}</p>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">کودهای سیستمی</p>
          <p class="text-xl font-bold text-indigo-600 dark:text-indigo-400 tabular-nums">{{ systemFertilizers.length }}</p>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- نوار ابزار (جستجو + دکمه‌ها) -->
    <!-- ============================================================ -->
    <div class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
        
        <!-- بخش راست: جستجو و فیلتر -->
        <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
          <!-- جستجو -->
          <div class="relative flex-1 min-w-[200px] max-w-md">
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
          
          <!-- فیلتر نوع -->
          <select
            v-model="filterType"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          >
            <option value="all">همه کودها</option>
            <option value="fertilizer">فقط کودها</option>
            <option value="acid">فقط اسیدها</option>
          </select>
        </div>

        <!-- بخش چپ: دکمه‌های عملیاتی -->
        <div class="flex flex-wrap gap-2 w-full lg:w-auto justify-end">
          <!-- دکمه افزودن دستی -->
          <button
            @click="$emit('open-modal')"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 shadow-sm hover:shadow-md"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            افزودن کود شخصی
          </button>

          <!-- دکمه بروزرسانی -->
          <button
            @click="$emit('refresh')"
            :disabled="isLoading"
            class="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <svg v-if="!isLoading" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            بروزرسانی
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول کودهای شخصی -->
    <!-- ============================================================ -->
    <div v-if="filteredFertilizers.length > 0" class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- هدر جدول -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gray-50 dark:bg-gray-700/50">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">
            کودهای شخصی
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mr-2">({{ filteredFertilizers.length }} مورد)</span>
          </h3>
        </div>
      </div>
      
      <!-- جدول با اسکرول افقی -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700/50">
              <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700/50 px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[200px]">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                  نام کود / برند
                </div>
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[70px]">
                فرم
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[80px]">
                خلوص %
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px]">
                pH
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[120px]">
                قیمت (تومان)
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[200px]">
                عناصر
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[100px]">
                عملیات
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="fertilizer in filteredFertilizers"
              :key="fertilizer.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group"
            >
              <!-- نام کود -->
              <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-3 text-right">
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="fertilizer.isAcid ? 'bg-warning-50 dark:bg-warning-900/30' : 'bg-primary-50 dark:bg-primary-900/30'"
                  >
                    <svg
                      class="w-5 h-5"
                      :class="fertilizer.isAcid ? 'text-warning-600 dark:text-warning-400' : 'text-primary-600 dark:text-primary-400'"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path v-if="fertilizer.isAcid" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                    <div class="flex items-center gap-2 mt-0.5 flex-wrap">
                      <span v-if="fertilizer.brand" class="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-1.5 py-0.5 rounded">
                        {{ fertilizer.brand }}
                      </span>
                      <span v-if="fertilizer.sourceSystemId" class="text-[10px] text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30 px-1.5 py-0.5 rounded border border-indigo-100 dark:border-indigo-800">
                        کپی از سیستمی
                      </span>
                    </div>
                  </div>
                </div>
              </td>
              
              <!-- فرم -->
              <td class="px-4 py-3 text-center">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                  {{ getFormLabel(fertilizer.form) }}
                </span>
              </td>
              
              <!-- خلوص -->
              <td class="px-4 py-3 text-center">
                <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                  {{ fertilizer.concentration || 100 }}%
                </span>
              </td>
              
              <!-- pH -->
              <td class="px-4 py-3 text-center">
                <span v-if="fertilizer.phLevel !== undefined && fertilizer.phLevel !== null" class="font-semibold text-gray-900 dark:text-white tabular-nums">
                  {{ fertilizer.phLevel }}
                </span>
                <span v-else class="text-gray-400 dark:text-gray-500 text-xs">-</span>
              </td>
              
              <!-- قیمت -->
              <td class="px-4 py-3 text-center">
                <span class="font-semibold text-gray-900 dark:text-white tabular-nums">
                  {{ Number(fertilizer.pricePerKg || 0).toLocaleString('fa-IR') }}
                </span>
              </td>
              
              <!-- عناصر -->
              <td class="px-4 py-3">
                <div class="flex flex-wrap gap-1 justify-center">
                  <template v-if="hasElements(fertilizer)">
                    <span
                      v-for="(percentage, element) in getActiveElements(fertilizer)"
                      :key="element"
                      class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-600"
                      :title="`${element}: ${percentage}%`"
                    >
                      <span class="font-bold text-primary-600 dark:text-primary-400">{{ element }}</span>
                      <span class="mx-1 text-gray-400">|</span>
                      <span>{{ percentage }}%</span>
                    </span>
                  </template>
                  <span v-else class="text-xs text-gray-400 dark:text-gray-500 italic">بدون عنصر</span>
                </div>
              </td>
              
              <!-- عملیات -->
              <td class="px-4 py-3 text-center">
                <div class="flex items-center justify-center gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                  <button
                    @click="$emit('edit-fertilizer', fertilizer)"
                    class="p-1.5 rounded-lg text-primary-600 hover:text-primary-800 hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
                    title="ویرایش"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button
                    @click="$emit('delete-fertilizer', fertilizer.id)"
                    class="p-1.5 rounded-lg text-danger-600 hover:text-danger-800 hover:bg-danger-50 dark:hover:bg-danger-900/30 transition-colors"
                    title="حذف"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- پیام خالی بودن -->
    <!-- ============================================================ -->
    <div v-else-if="!isLoading" class="mt-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
        <svg class="w-10 h-10 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
      </div>
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {{ searchQuery || filterType !== 'all' ? 'نتیجه‌ای یافت نشد' : 'هنوز کود شخصی ایجاد نکرده‌اید' }}
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        {{ searchQuery || filterType !== 'all' ? 'لطفاً عبارت جستجو یا فیلتر را تغییر دهید.' : 'برای شروع، روی دکمه "کپی کودهای سیستمی" کلیک کنید یا اولین کود شخصی خود را اضافه نمایید.' }}
      </p>
      <div class="mt-6 flex justify-center gap-3 flex-wrap">
        <button
          v-if="!searchQuery && filterType === 'all'"
          @click="$emit('copy-all')"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
          </svg>
          کپی کودهای سیستمی
        </button>
        <button
          @click="$emit('open-modal')"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          افزودن دستی
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// ============================================================
// Props
// ============================================================
const props = defineProps<{
  userFertilizers: any[];
  systemFertilizers: any[];
  isLoading: boolean;
}>();

// ============================================================
// Emits
// ============================================================
defineEmits<{
  (e: 'refresh'): void;
  (e: 'open-modal'): void;
  (e: 'edit-fertilizer', fertilizer: any): void;
  (e: 'delete-fertilizer', id: string): void;
  (e: 'copy-all'): void;
}>();

// ============================================================
// State
// ============================================================
const searchQuery = ref('');
const filterType = ref<'all' | 'fertilizer' | 'acid'>('all');

// ============================================================
// Computed
// ============================================================
const normalFertilizersCount = computed(() => {
  return props.userFertilizers.filter((f: any) => !f.isAcid).length;
});

const acidFertilizersCount = computed(() => {
  return props.userFertilizers.filter((f: any) => f.isAcid).length;
});

const filteredFertilizers = computed(() => {
  let result = props.userFertilizers;
  
  if (filterType.value === 'fertilizer') {
    result = result.filter((f: any) => !f.isAcid);
  } else if (filterType.value === 'acid') {
    result = result.filter((f: any) => f.isAcid);
  }
  
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase();
    result = result.filter((f: any) =>
      f.name.toLowerCase().includes(query) ||
      (f.brand && f.brand.toLowerCase().includes(query)) ||
      (f.category && f.category.toLowerCase().includes(query))
    );
  }
  
  return result;
});

// ============================================================
// Methods
// ============================================================
const getFormLabel = (form: string | undefined): string => {
  const labels: Record<string, string> = {
    liquid: 'مایع',
    powder: 'پودر',
    crystal: 'کریستال',
    granular: 'گرانول'
  };
  return form ? labels[form] || form : 'نامشخص';
};

const hasElements = (fertilizer: any): boolean => {
  if (!fertilizer.elements) return false;
  return Object.values(fertilizer.elements).some((v: any) => v && v > 0);
};

const getActiveElements = (fertilizer: any): Record<string, number> => {
  if (!fertilizer.elements) return {};
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(fertilizer.elements)) {
    if (value && (value as number) > 0) {
      result[key] = value as number;
    }
  }
  return result;
};
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>