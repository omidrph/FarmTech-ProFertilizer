<!-- frontend/src/components/features/ph/PhHistoryPanel.vue -->
<!-- تاریخچهٔ اصلاح‌های ثبت‌شدهٔ این گزارش (آزمون و خطاها و رسپی‌ها) -->
<template>
  <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-2 mb-3">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">تاریخچهٔ اصلاح‌های این گزارش</h3>
      <span class="text-[11px] text-gray-400">{{ items.length }} مورد</span>
    </div>

    <p v-if="items.length === 0" class="text-sm text-gray-500 dark:text-gray-400 text-center py-6">
      هنوز اصلاحی ثبت نشده است.
    </p>

    <ul v-else class="space-y-2.5">
      <li
        v-for="item in items"
        :key="item.id"
        class="rounded-xl border px-3 py-3"
        :class="item.is_active
          ? 'border-emerald-300 dark:border-emerald-700 bg-emerald-50/60 dark:bg-emerald-900/10'
          : 'border-gray-200 dark:border-gray-700'"
      >
        <div class="flex items-start justify-between gap-3 flex-wrap">
          <div class="min-w-0">
            <p class="text-sm font-medium text-gray-900 dark:text-white flex items-center gap-2 flex-wrap">
              {{ item.chemical_name }}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                {{ item.mode === 'trial' ? 'آزمون روی نمونه' : 'رسپی' }}
              </span>
              <span v-if="item.is_active" class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300">
                اعمال‌شده در محاسبه
              </span>
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-6">
              {{ fmtDose(item.dose_tank, item.dose_unit) }} برای {{ fmt(item.tank_volume_l, 0) }} لیتر
              ({{ fmtDose(item.dose_per_1000l, item.dose_unit) }} در هر ۱۰۰۰ لیتر)
              <template v-if="item.initial_ph != null && item.final_ph != null">
                · pH {{ fmt(item.initial_ph, 2) }} ← {{ fmt(item.final_ph, 2) }}
              </template>
            </p>
            <p v-if="item.ec_before != null && item.ec_after != null" class="text-xs text-gray-500 dark:text-gray-400">
              EC اندازه‌گیری‌شده: {{ fmt(item.ec_before, 2) }} ← {{ fmt(item.ec_after, 2) }}
              (Δ {{ fmt(item.ec_after - item.ec_before, 2) }})
            </p>
            <p v-if="item.note" class="text-xs text-gray-600 dark:text-gray-300 mt-1">{{ item.note }}</p>
            <p class="text-[11px] text-gray-400 mt-1">{{ formatDate(item.created_at) }}</p>
          </div>

          <div class="flex items-center gap-1.5 flex-shrink-0">
            <button type="button" class="btn-sm" @click="$emit('reuse', item)">استفاده مجدد</button>
            <button
              v-if="!item.is_active"
              type="button"
              class="btn-sm btn-primary"
              @click="$emit('apply', item.id)"
            >اعمال</button>
            <button v-else type="button" class="btn-sm" @click="$emit('unapply', item.id)">لغو اعمال</button>
            <button type="button" class="btn-sm btn-danger" @click="confirmDelete(item.id)" aria-label="حذف">حذف</button>
          </div>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { PhAdjustmentItem } from '@/services/apiService';
import { fmt, fmtDose } from './phFormat';

defineProps<{ items: PhAdjustmentItem[] }>();
const emit = defineEmits<{
  (e: 'reuse', item: PhAdjustmentItem): void;
  (e: 'apply', id: number): void;
  (e: 'unapply', id: number): void;
  (e: 'delete', id: number): void;
}>();

const confirmDelete = (id: number) => {
  if (typeof window === 'undefined' || window.confirm('این مورد از تاریخچه حذف شود؟')) emit('delete', id);
};

const formatDate = (iso: string): string => {
  try {
    return new Date(iso).toLocaleString('fa-IR', { dateStyle: 'medium', timeStyle: 'short' });
  } catch {
    return iso;
  }
};
</script>

<style scoped>
.btn-sm {
  @apply px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 text-xs font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors;
}
.btn-primary {
  @apply border-primary-600 bg-primary-600 text-white hover:bg-primary-700 dark:hover:bg-primary-700;
}
.btn-danger {
  @apply text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-800 hover:bg-rose-50 dark:hover:bg-rose-900/20;
}
</style>
