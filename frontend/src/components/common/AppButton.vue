<template>
  <button 
    :type="type"
    :class="[
      'inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      variantClasses,
      sizeClasses,
      fullWidth ? 'w-full' : ''
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    
    <!-- Icon -->
    <span v-if="icon" class="text-lg leading-none" v-html="icon"></span>
    
    <!-- Slot -->
    <slot>
      <span>{{ label }}</span>
    </slot>
    
    <!-- Badge -->
    <span v-if="badge" class="absolute -top-1 -right-1 bg-danger-500 text-white text-xs rounded-full min-w-[20px] h-5 px-1.5 flex items-center justify-center">
      {{ badge }}
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ===== Props =====
interface Props {
  label?: string;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
  loading?: boolean;
  icon?: string;
  badge?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  type: 'button',
  variant: 'primary',
  size: 'md',
  fullWidth: false,
  disabled: false,
  loading: false,
  icon: '',
  badge: ''
});

// ===== Emits =====
const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void;
}>();

// ===== Computed =====
const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-sm hover:shadow-md border border-primary-600 hover:border-primary-700 focus:ring-primary-500',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-700 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200 border border-gray-300 dark:border-gray-600 focus:ring-gray-500',
    success: 'bg-success-600 hover:bg-success-700 text-white shadow-sm hover:shadow-md border border-success-600 hover:border-success-700 focus:ring-success-500',
    danger: 'bg-danger-600 hover:bg-danger-700 text-white shadow-sm hover:shadow-md border border-danger-600 hover:border-danger-700 focus:ring-danger-500',
    warning: 'bg-warning-600 hover:bg-warning-700 text-white shadow-sm hover:shadow-md border border-warning-600 hover:border-warning-700 focus:ring-warning-500',
    outline: 'bg-transparent hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-gray-300 dark:border-gray-600 focus:ring-gray-500',
    ghost: 'bg-transparent hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 border border-transparent focus:ring-gray-500'
  };
  return variants[props.variant] || variants.primary;
});

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-6 py-3.5 text-base'
  };
  return sizes[props.size] || sizes.md;
});

// ===== Methods =====
const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

button {
  position: relative;
  min-height: 38px;
}

button:active:not(:disabled) {
  transform: scale(0.97);
}
</style>