<template>
  <div class="w-full">
    <!-- Label -->
    <label 
      v-if="label" 
      :for="id" 
      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
      :class="{ 'text-danger-600 dark:text-danger-400': error }"
    >
      {{ label }}
      <span v-if="required" class="text-danger-500">*</span>
    </label>

    <!-- Input Wrapper -->
    <div 
      class="relative rounded-lg transition-all duration-200"
      :class="[
        error ? 'ring-2 ring-danger-500 border-danger-500' : 'focus-within:ring-2 focus-within:ring-primary-500 focus-within:border-primary-500',
        disabled ? 'opacity-60 cursor-not-allowed' : ''
      ]"
    >
      <!-- Prefix Icon -->
      <span v-if="prefixIcon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
        <span v-html="prefixIcon" class="text-lg leading-none"></span>
      </span>

      <!-- Input -->
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :minlength="minlength"
        :maxlength="maxlength"
        :autocomplete="autocomplete"
        class="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none transition-all duration-200"
        :class="[
          prefixIcon ? 'pl-10' : '',
          suffixIcon ? 'pr-10' : '',
          error ? 'border-danger-500' : ''
        ]"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        @change="handleChange"
      />

      <!-- Suffix Icon -->
      <span v-if="suffixIcon" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
        <span v-html="suffixIcon" class="text-lg leading-none"></span>
      </span>

      <!-- Clear Button -->
      <button 
        v-if="clearable && modelValue && !disabled"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        @click="clear"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>

      <!-- Toggle Password -->
      <button 
        v-if="type === 'password'"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        @click="togglePasswordVisibility"
      >
        <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
        </svg>
      </button>
    </div>

    <!-- Hint -->
    <p v-if="hint && !error" class="mt-1 text-xs text-gray-500 dark:text-gray-400">
      {{ hint }}
    </p>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-xs text-danger-600 dark:text-danger-400 flex items-center gap-1">
      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
      </svg>
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// ===== Props =====
interface Props {
  modelValue: string | number;
  label?: string;
  placeholder?: string;
  type?: 'text' | 'number' | 'password' | 'email' | 'tel' | 'url' | 'date';
  id?: string;
  disabled?: boolean;
  readonly?: boolean;
  required?: boolean;
  error?: string;
  hint?: string;
  prefixIcon?: string;
  suffixIcon?: string;
  clearable?: boolean;
  min?: number;
  max?: number;
  step?: string | number;
  minlength?: number;
  maxlength?: number;
  autocomplete?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  placeholder: '',
  type: 'text',
  id: '',
  disabled: false,
  readonly: false,
  required: false,
  error: '',
  hint: '',
  prefixIcon: '',
  suffixIcon: '',
  clearable: false,
  min: undefined,
  max: undefined,
  step: 'any',
  minlength: undefined,
  maxlength: undefined,
  autocomplete: 'off'
});

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void;
  (e: 'blur', event: FocusEvent): void;
  (e: 'focus', event: FocusEvent): void;
  (e: 'change', event: Event): void;
  (e: 'clear'): void;
}>();

// ===== State =====
const showPassword = ref(false);
const inputId = computed(() => props.id || `input-${Math.random().toString(36).substring(2, 9)}`);

// ===== Methods =====
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value: string | number = target.value;
  
  if (props.type === 'number') {
    value = value === '' ? '' : Number(value);
  }
  
  emit('update:modelValue', value);
};

const handleBlur = (event: FocusEvent) => {
  emit('blur', event);
};

const handleFocus = (event: FocusEvent) => {
  emit('focus', event);
};

const handleChange = (event: Event) => {
  emit('change', event);
};

const clear = () => {
  emit('update:modelValue', props.type === 'number' ? '' : '');
  emit('clear');
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};
</script>

<style scoped>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.dark input:disabled {
  background-color: #374151;
}
</style>