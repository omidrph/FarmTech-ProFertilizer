<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام گزارش</label>
        <input 
          type="text" 
          :value="reportName" 
          @input="updateReportName($event)"
          placeholder="نام گزارش..." 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام گیاه</label>
        <input 
          type="text" 
          :value="plantName" 
          @input="updatePlantName($event)"
          placeholder="مثال: گوجه فرنگی" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">فصل</label>
        <input 
          type="text" 
          :value="season" 
          @input="updateSeason($event)"
          placeholder="مثال: بهار" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">مرحله رشد</label>
        <input 
          type="text" 
          :value="growthStage" 
          @input="updateGrowthStage($event)"
          placeholder="مثال: گلدهی" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">تاریخ</label>
        <input 
          type="text" 
          :value="reportDate" 
          @input="updateReportDate($event)"
          placeholder="۱۴۰۵/۰۳/۲۶" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
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
  const target = event.target as HTMLInputElement;
  emit('update:season', target.value);
};

const updateGrowthStage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:growthStage', target.value);
};

const updateReportDate = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:reportDate', target.value);
};
</script>