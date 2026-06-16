<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
      <!-- نام گزارش -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام گزارش</label>
        <input 
          type="text" 
          :value="reportName" 
          @input="updateReportName($event)"
          placeholder="نام گزارش..." 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" 
        />
      </div>

      <!-- نام گیاه -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام گیاه</label>
        <input 
          type="text" 
          :value="plantName" 
          @input="updatePlantName($event)"
          placeholder="مثال: گوجه فرنگی" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" 
        />
      </div>

      <!-- فصل -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">فصل</label>
        <select 
          :value="season" 
          @change="updateSeason($event)"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all appearance-none"
        >
          <option value="">انتخاب فصل...</option>
          <option value="بهار">بهار</option>
          <option value="تابستان">تابستان</option>
          <option value="پاییز">پاییز</option>
          <option value="زمستان">زمستان</option>
        </select>
      </div>

      <!-- مرحله رشد -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">مرحله رشد</label>
        <select 
          :value="growthStage" 
          @change="updateGrowthStage($event)"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all appearance-none"
        >
          <option value="">انتخاب مرحله رشد...</option>
          <option value="استقرار نشا">استقرار نشا</option>
          <option value="رشد رویشی">رشد رویشی</option>
          <option value="گلدهی">گلدهی</option>
          <option value="میوه دهی">میوه دهی</option>
        </select>
      </div>

      <!-- تاریخ (ورودی دستی) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تاریخ</label>
        <input 
          type="text" 
          :value="reportDate" 
          @input="updateReportDate($event)"
          placeholder="مثال: ۱۴۰۵/۰۳/۲۶" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" 
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
</style>