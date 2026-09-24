<!-- frontend/src/components/features/ReportHeader.vue -->
<!--
  باکس کامل گزارش (فقط در تب «خانه» نمایش داده می‌شود و تنها جای ویرایش مشخصات گزارش است)
  در بقیه‌ی تب‌ها به‌جای این باکس، نوار باریک ReportBar نمایش داده می‌شود.
-->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm p-4 sm:p-5">
    <div class="flex items-center justify-between gap-3 mb-4">
      <div class="flex items-center gap-3 min-w-0">
        <div class="w-10 h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
          </svg>
        </div>
        <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">گزارش</h2>
      </div>

      <span
        class="flex-shrink-0 text-xs px-2.5 py-1 rounded-full font-medium"
        :class="isComplete
          ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400'
          : 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400'"
      >
        {{ isComplete ? 'آماده ثبت' : 'تکمیل اطلاعات' }}
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
      <div>
        <label class="field-label">نام گزارش <span class="text-danger-500">*</span></label>
        <input type="text" :value="reportName" @input="updateReportName($event)" placeholder="نام گزارش" class="field-input" />
      </div>
      <div>
        <label class="field-label">نام گیاه <span class="text-danger-500">*</span></label>
        <input type="text" :value="plantName" @input="updatePlantName($event)" placeholder="مثلاً گوجه‌فرنگی" class="field-input" />
      </div>
      <div>
        <label class="field-label">فصل <span class="text-danger-500">*</span></label>
        <select :value="season" @change="updateSeason($event)" class="field-input">
          <option value="">انتخاب فصل</option>
          <option value="بهار">بهار</option>
          <option value="تابستان">تابستان</option>
          <option value="پاییز">پاییز</option>
          <option value="زمستان">زمستان</option>
        </select>
      </div>
      <div>
        <label class="field-label">مرحله رشد <span class="text-danger-500">*</span></label>
        <select :value="growthStage" @change="updateGrowthStage($event)" class="field-input">
          <option value="">انتخاب مرحله رشد</option>
          <option value="استقرار نشا">استقرار نشا</option>
          <option value="رشد رویشی">رشد رویشی</option>
          <option value="گلدهی">گلدهی</option>
          <option value="رسیدگی">رسیدگی</option>
          <option value="میوه‌دهی">میوه‌دهی</option>
          <option value="پایان دوره">پایان دوره</option>
        </select>
      </div>
      <div>
        <label class="field-label">تاریخ <span class="text-danger-500">*</span></label>
        <input type="text" :value="reportDate" @input="updateReportDate($event)" placeholder="مثلاً ۱۴۰۵/۰۶/۰۱" class="field-input" />
      </div>
    </div>

    <div class="mt-4 flex sm:justify-end">
      <button
        type="button"
        @click="emitSave"
        :disabled="isSaving"
        class="inline-flex items-center justify-center gap-2 w-full sm:w-auto px-6 py-2.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
      >
        <svg v-if="isSaving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ isSaving ? 'در حال ذخیره...' : 'ذخیره گزارش' }}
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  reportName: string;
  plantName: string;
  season: string;
  growthStage: string;
  reportDate: string;
  isSaving?: boolean;
}

const props = withDefaults(defineProps<Props>(), { isSaving: false });

const emit = defineEmits<{
  (e: 'update:reportName', value: string): void;
  (e: 'update:plantName', value: string): void;
  (e: 'update:season', value: string): void;
  (e: 'update:growthStage', value: string): void;
  (e: 'update:reportDate', value: string): void;
  (e: 'save'): void;
}>();

const isComplete = computed(() =>
  Boolean(
    props.reportName.trim() &&
    props.plantName.trim() &&
    props.season &&
    props.growthStage &&
    props.reportDate.trim()
  )
);

const updateReportName = (event: Event) => emit('update:reportName', (event.target as HTMLInputElement).value);
const updatePlantName = (event: Event) => emit('update:plantName', (event.target as HTMLInputElement).value);
const updateSeason = (event: Event) => emit('update:season', (event.target as HTMLSelectElement).value);
const updateGrowthStage = (event: Event) => emit('update:growthStage', (event.target as HTMLSelectElement).value);
const updateReportDate = (event: Event) => emit('update:reportDate', (event.target as HTMLInputElement).value);
const emitSave = () => emit('save');
</script>

<style scoped>
.field-label {
  @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5;
}
.field-input {
  @apply w-full px-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all;
}
select {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 0.9rem;
  padding-left: 2rem;
}
.dark select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}
</style>
