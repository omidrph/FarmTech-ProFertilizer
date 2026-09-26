<!-- frontend/src/components/features/ph/PhHistoryPanel.vue -->
<!-- تاریخچه‌ی محاسبات ذخیره‌شده‌ی ماشین‌حساب pH (مستقل از چرخه‌ی رسمی محاسبه) -->
<template>
  <section class="rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
    <div class="flex items-center justify-between gap-2 mb-3">
      <h4 class="text-sm font-bold text-gray-900 dark:text-white">تاریخچه‌ی این ماشین‌حساب</h4>
      <span class="text-[11px] text-gray-400 dark:text-gray-500">{{ items.length.toLocaleString('fa-IR') }} مورد</span>
    </div>

    <p v-if="!items.length" class="text-xs text-gray-500 dark:text-gray-400">
      هنوز محاسبه‌ای برای این گزارش ذخیره نشده است.
    </p>

    <ul v-else class="space-y-2">
      <li
        v-for="item in items"
        :key="item.id"
        class="flex items-start justify-between gap-3 rounded-xl border border-gray-100 dark:border-gray-700 px-3 py-2.5"
      >
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-800 dark:text-gray-100 flex items-center gap-1.5 flex-wrap">
            <span
              class="text-[10px] px-1.5 py-0.5 rounded-full font-normal"
              :class="item.record_type === 'monitoring'
                ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300'
                : 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'"
            >
              {{ item.record_type === 'monitoring' ? 'پایش' : 'اصلاح' }}
            </span>
            <span v-if="item.record_type === 'correction'">
              {{ item.method === 'titration' ? 'تیتراسیون واقعی' : 'مدل تئوریک' }}
              <span v-if="item.chemical_name" class="text-gray-400 dark:text-gray-500 font-normal"> · {{ item.chemical_name }}</span>
            </span>
            <span v-else class="text-gray-500 dark:text-gray-400 font-normal">فقط ثبت اندازه‌گیری</span>
          </p>
          <p class="mt-0.5 text-xs text-gray-500 dark:text-gray-400 tabular-nums">
            <template v-if="item.record_type === 'correction'">
              {{ fmtVolumeL(item.outputs?.commercial_volume_l ?? 0) }}
              <span v-if="item.inputs?.current_ph && item.inputs?.target_ph">
                · pH {{ fmt(item.inputs.current_ph, 2) }} → {{ fmt(item.inputs.target_ph, 2) }}
              </span>
            </template>
            <template v-else>
              pH {{ fmt(item.inputs?.ph ?? item.outputs?.ph, 2) }}
            </template>
            <span v-if="item.ec_ms_cm !== null && item.ec_ms_cm !== undefined"> · EC {{ fmt(item.ec_ms_cm, 2) }} mS/cm</span>
          </p>
          <p v-if="item.note" class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ item.note }}</p>
          <p class="mt-1 text-[11px] text-gray-400 dark:text-gray-500">{{ formatDate(item.created_at) }}</p>
        </div>
        <button
          type="button"
          @click="$emit('delete', item.id)"
          class="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg text-gray-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-colors"
          :aria-label="'حذف رکورد'"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { PhHistoryItem } from '@/services/apiService';
import { fmt, fmtVolumeL } from './phFormat';

defineProps<{ items: PhHistoryItem[] }>();
defineEmits<{ (e: 'delete', id: number): void }>();

const formatDate = (iso: string): string => {
  try {
    return new Date(iso).toLocaleString('fa-IR', { dateStyle: 'medium', timeStyle: 'short' });
  } catch {
    return iso;
  }
};
</script>
