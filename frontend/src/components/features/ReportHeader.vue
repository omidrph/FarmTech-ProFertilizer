<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-3 sm:p-4 transition-all hover:shadow-md">
    
    <!-- هدر -->
    <div class="flex items-center gap-2 mb-3 pb-2 border-b border-gray-100 dark:border-gray-700">
      <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
        <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">اطلاعات گزارش</span>
    </div>

    <!-- فیلدها -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2 sm:gap-3">
      <!-- نام گزارش -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نام گزارش</label>
        <input 
          type="text" 
          :value="reportName" 
          @input="updateReportName($event)"
          placeholder="نام گزارش..." 
          class="w-full px-3 py-1.5 sm:py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200" 
        />
      </div>

      <!-- نام گیاه -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نام گیاه</label>
        <input 
          type="text" 
          :value="plantName" 
          @input="updatePlantName($event)"
          placeholder="مثال: گوجه فرنگی" 
          class="w-full px-3 py-1.5 sm:py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200" 
        />
      </div>

      <!-- فصل -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">فصل</label>
        <select 
          :value="season" 
          @change="updateSeason($event)"
          class="w-full px-3 py-1.5 sm:py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200 appearance-none cursor-pointer"
        >
          <option value="">انتخاب فصل...</option>
          <option value="بهار">🌱 بهار</option>
          <option value="تابستان">☀️ تابستان</option>
          <option value="پاییز">🍂 پاییز</option>
          <option value="زمستان">❄️ زمستان</option>
        </select>
      </div>

      <!-- مرحله رشد -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">مرحله رشد</label>
        <select 
          :value="growthStage" 
          @change="updateGrowthStage($event)"
          class="w-full px-3 py-1.5 sm:py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200 appearance-none cursor-pointer"
        >
          <option value="">انتخاب مرحله...</option>
          <option value="استقرار نشا">🌱 استقرار نشا</option>
          <option value="رشد رویشی">🌿 رشد رویشی</option>
          <option value="گلدهی">🌸 گلدهی</option>
          <option value="رسیدگی">🍎 رسیدگی</option>
          <option value="میوه‌دهی">🍅 میوه‌دهی</option>
          <option value="پایان دوره">🌾 پایان دوره</option>
        </select>
      </div>

      <!-- تاریخ -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">تاریخ</label>
        <input 
          type="text" 
          :value="reportDate" 
          @input="updateReportDate($event)"
          placeholder="مثال: ۱۴۰۵/۰۳/۲۶" 
          class="w-full px-3 py-1.5 sm:py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all duration-200" 
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ===== Props =====
interface Props {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  reportDate: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'update:reportName', value: string): void;
  (e: 'update:plantName', value: string): void;
  (e: 'update:season', value: string): void;
  (e: 'update:growthStage', value: string): void;
  (e: 'update:reportDate', value: string): void;
}>();

// ===== Methods =====
const updateReportName = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:reportName', target.value);
};

const updatePlantName = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:plantName', target.value);
};

const updateSeason = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:season', target.value);
};

const updateGrowthStage = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:growthStage', target.value);
};

const updateReportDate = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:reportDate', target.value);
};
</script>

<style scoped>
/* Custom select styling */
select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 1rem;
  padding-left: 2.5rem;
}

.dark select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}

/* انیمیشن focus */
input:focus, select:focus {
  outline: none;
}

/* ریسپانسیو برای موبایل */
@media (max-width: 640px) {
  .grid {
    gap: 0.5rem;
  }
  
  input, select {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
    font-size: 0.875rem;
  }
  
  label {
    font-size: 0.7rem;
  }
}
</style>