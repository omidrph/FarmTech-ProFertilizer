<!-- frontend/src/components/features/home/HomeAttentionList.vue -->
<!-- نوار هشدار (حداکثر ۳ مورد). اگر مشکلی نباشد اصلاً نمایش داده نمی‌شود. -->
<template>
  <ul
    v-if="items.length"
    class="rounded-2xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 px-4 py-3 space-y-1.5"
  >
    <li
      v-for="item in items"
      :key="item.text"
      class="flex items-start gap-2 text-sm text-amber-900 dark:text-amber-200"
    >
      <svg
        class="w-4 h-4 mt-0.5 flex-shrink-0"
        :class="item.danger ? 'text-rose-500' : 'text-amber-600 dark:text-amber-400'"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span>{{ item.text }}</span>
    </li>
  </ul>
</template>

<script setup lang="ts">
defineProps<{
  items: Array<{ text: string; danger: boolean }>;
}>();
</script>
