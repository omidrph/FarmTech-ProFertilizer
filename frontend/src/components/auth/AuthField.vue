<template>
  <div>
    <label :for="id" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ label }}</label>
    <div class="relative group">
      <div v-if="icon" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <svg class="w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icon" />
        </svg>
      </div>
      <input
        :id="id"
        :type="isPassword && show ? 'text' : type"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :inputmode="inputmode"
        :maxlength="maxlength"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @blur="$emit('blur')"
        class="w-full py-3 bg-white dark:bg-gray-800 border-2 rounded-xl text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-4 transition-all duration-200"
        :class="[
          icon ? 'pr-10' : 'pr-4',
          isPassword ? 'pl-12' : 'pl-4',
          error
            ? 'border-danger-400 focus:border-danger-500 focus:ring-danger-500/20'
            : 'border-gray-200 dark:border-gray-700 focus:border-primary-500 focus:ring-primary-500/20',
        ]"
      />
      <button
        v-if="isPassword"
        type="button"
        @click="show = !show"
        :aria-label="show ? 'پنهان کردن رمز' : 'نمایش رمز'"
        class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        <svg v-if="!show" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M3 3l18 18" />
        </svg>
      </button>
    </div>
    <p v-if="error" class="text-xs text-danger-600 dark:text-danger-400 mt-1.5">{{ error }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = withDefaults(defineProps<{
  modelValue: string;
  label: string;
  id: string;
  type?: string;
  placeholder?: string;
  icon?: string;
  error?: string;
  autocomplete?: string;
  inputmode?: 'text' | 'tel' | 'numeric';
  maxlength?: number;
}>(), { type: 'text' });

defineEmits<{ (e: 'update:modelValue', v: string): void; (e: 'blur'): void }>();

const show = ref(false);
const isPassword = computed(() => props.type === 'password');
</script>
