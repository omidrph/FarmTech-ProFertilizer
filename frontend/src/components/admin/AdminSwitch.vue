<!-- کلید روشن/خاموش هم‌سبک برنامه -->
<template>
  <button type="button" role="switch" :aria-checked="modelValue" @click="$emit('update:modelValue', !modelValue)"
    class="relative inline-flex h-6 w-11 flex-shrink-0 items-center rounded-full transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40"
    :class="modelValue ? 'bg-primary-600' : 'bg-gray-300 dark:bg-gray-600'">
    <span class="inline-block h-5 w-5 rounded-full bg-white shadow transition-transform" :class="modelValue ? '-translate-x-[1.35rem]' : '-translate-x-0.5'"></span>
  </button>
</template>
<script setup lang="ts">
defineProps<{ modelValue: boolean }>();
defineEmits<{ (e: 'update:modelValue', v: boolean): void }>();
</script>
