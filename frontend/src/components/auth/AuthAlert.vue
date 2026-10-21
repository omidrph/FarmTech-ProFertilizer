<template>
  <Transition name="alert">
    <div
      v-if="title"
      role="alert"
      class="rounded-xl p-3 mb-4 border flex items-start gap-3"
      :class="styles.box"
    >
      <svg class="w-5 h-5 flex-shrink-0 mt-0.5" :class="styles.icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path v-if="type === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        <path v-else-if="type === 'info'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
      </svg>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold" :class="styles.title">{{ title }}</p>
        <p v-if="hint" class="text-xs mt-1 leading-relaxed" :class="styles.hint">{{ hint }}</p>
        <button v-if="actionLabel" type="button" @click="$emit('action')" class="text-xs font-semibold mt-2 underline underline-offset-2" :class="styles.title">
          {{ actionLabel }}
        </button>
      </div>
      <button v-if="dismissible" type="button" @click="$emit('close')" aria-label="بستن" class="opacity-60 hover:opacity-100 transition-opacity" :class="styles.title">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  type?: 'error' | 'success' | 'info';
  title?: string | null;
  hint?: string;
  actionLabel?: string;
  dismissible?: boolean;
}>(), { type: 'error', dismissible: false });

defineEmits<{ (e: 'close'): void; (e: 'action'): void }>();

const styles = computed(() => ({
  error: {
    box: 'bg-danger-50 dark:bg-danger-900/20 border-danger-200 dark:border-danger-800',
    icon: 'text-danger-600 dark:text-danger-400',
    title: 'text-danger-700 dark:text-danger-300',
    hint: 'text-danger-600/90 dark:text-danger-400/90',
  },
  success: {
    box: 'bg-success-50 dark:bg-success-900/20 border-success-200 dark:border-success-800',
    icon: 'text-success-600 dark:text-success-400',
    title: 'text-success-700 dark:text-success-300',
    hint: 'text-success-600/90 dark:text-success-400/90',
  },
  info: {
    box: 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800',
    icon: 'text-primary-600 dark:text-primary-400',
    title: 'text-primary-700 dark:text-primary-300',
    hint: 'text-primary-600/90 dark:text-primary-400/90',
  },
}[props.type]));
</script>

<style scoped>
.alert-enter-active, .alert-leave-active { transition: all .25s ease; }
.alert-enter-from, .alert-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
