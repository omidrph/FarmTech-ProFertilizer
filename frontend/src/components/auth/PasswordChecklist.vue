<template>
  <ul class="grid grid-cols-2 gap-x-3 gap-y-1.5 mt-2.5">
    <li v-for="r in rules" :key="r.key" class="flex items-center gap-1.5 text-xs transition-colors"
        :class="r.ok ? 'text-success-600 dark:text-success-400' : 'text-gray-500 dark:text-gray-400'">
      <span class="w-4 h-4 rounded-full flex items-center justify-center border transition-colors flex-shrink-0"
            :class="r.ok ? 'bg-success-500 border-success-500 text-white' : 'border-gray-300 dark:border-gray-600'">
        <svg v-if="r.ok" class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" d="M5 13l4 4L19 7" /></svg>
      </span>
      {{ r.label }}
    </li>
  </ul>
</template>

<script setup lang="ts">
defineProps<{ rules: { key: string; label: string; ok: boolean }[] }>();
</script>
