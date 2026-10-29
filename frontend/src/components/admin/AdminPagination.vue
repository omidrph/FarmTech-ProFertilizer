<template>
  <div v-if="pages > 1" class="flex items-center justify-between gap-2 px-3 py-2.5 border-t border-gray-100 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400">
    <span>{{ total.toLocaleString('fa-IR') }} مورد · صفحه {{ page.toLocaleString('fa-IR') }} از {{ pages.toLocaleString('fa-IR') }}</span>
    <div class="flex items-center gap-1.5">
      <button class="ad-btn ad-btn-sm" :disabled="page <= 1" @click="$emit('change', page - 1)">قبلی</button>
      <button class="ad-btn ad-btn-sm" :disabled="page >= pages" @click="$emit('change', page + 1)">بعدی</button>
    </div>
  </div>
  <div v-else class="px-3 py-2 text-xs text-gray-400">{{ total.toLocaleString('fa-IR') }} مورد</div>
</template>
<script setup lang="ts">
defineProps<{ page: number; pages: number; total: number }>();
defineEmits<{ (e: 'change', p: number): void }>();
</script>
