<!-- frontend/src/components/features/home/HomeAttentionList.vue -->
<!--
  لیست هشدارهای صفحه خانه
  ------------------------------------------------------------
  - طراحی هماهنگ با ResultWarnings (صفحه محاسبه کود)
  - هر هشدار با آیکون، عنوان و توضیح
  - بدون هدر (طبق درخواست)
  - کنتراست بالا در dark mode (استفاده از 950/40)
-->
<template>
  <ul v-if="items.length" class="space-y-2.5">
    <li
      v-for="(item, index) in items"
      :key="index"
      class="flex items-start gap-3 rounded-xl border p-3 sm:p-3.5 transition-colors"
      :class="item.danger
        ? 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-700/60'
        : 'bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-700/60'"
    >
      <!-- آیکون -->
      <span
        class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center"
        :class="item.danger
          ? 'bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400'
          : 'bg-amber-100 dark:bg-amber-900/50 text-amber-600 dark:text-amber-400'"
      >
        <svg v-if="item.danger" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
      </span>

      <!-- متن -->
      <div class="flex-1 min-w-0">
        <p
          class="text-sm font-medium leading-6"
          :class="item.danger
            ? 'text-rose-800 dark:text-rose-200'
            : 'text-amber-800 dark:text-amber-200'"
        >
          {{ item.text }}
        </p>
        <p
          v-if="item.hint"
          class="text-xs mt-1 leading-5"
          :class="item.danger
            ? 'text-rose-700 dark:text-rose-300'
            : 'text-amber-700 dark:text-amber-300'"
        >
          {{ item.hint }}
        </p>
      </div>
    </li>
  </ul>
</template>

<script setup lang="ts">
interface AttentionItem {
  text: string;
  danger: boolean;
  hint?: string;
}

defineProps<{
  items: AttentionItem[];
}>();
</script>