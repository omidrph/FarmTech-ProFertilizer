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

    <!-- Select Wrapper -->
    <div 
      class="relative rounded-lg transition-all duration-200"
      :class="[
        error ? 'ring-2 ring-danger-500 border-danger-500' : 'focus-within:ring-2 focus-within:ring-primary-500',
        disabled ? 'opacity-60 cursor-not-allowed' : ''
      ]"
    >
      <!-- Single Select -->
      <select
        v-if="!multiple"
        :id="id"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 focus:outline-none transition-all duration-200 appearance-none"
        :class="[
          error ? 'border-danger-500' : '',
          prefixIcon ? 'pl-10' : ''
        ]"
        @change="handleChange"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option v-if="placeholder" value="" disabled selected class="text-gray-400 dark:text-gray-500">
          {{ placeholder }}
        </option>
        <option 
          v-for="option in options" 
          :key="String(option.value)"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>

      <!-- Multi Select -->
      <select
        v-else
        :id="id"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        multiple
        class="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 focus:outline-none transition-all duration-200 min-h-[100px]"
        :class="[error ? 'border-danger-500' : '']"
        @change="handleMultiChange"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option 
          v-for="option in options" 
          :key="String(option.value)"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>

      <!-- Dropdown Icon -->
      <div v-if="!multiple" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </div>

      <!-- Prefix Icon -->
      <span v-if="prefixIcon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
        <span v-html="prefixIcon" class="text-lg leading-none"></span>
      </span>
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

    <!-- Selected Items (Multi) -->
    <div v-if="multiple && selectedItems.length > 0" class="flex flex-wrap gap-1.5 mt-2">
      <span 
        v-for="item in selectedItems" 
        :key="String(item.value)"
        class="inline-flex items-center gap-1 px-2.5 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-lg text-xs font-medium"
      >
        {{ item.label }}
        <button 
          v-if="!disabled"
          type="button"
          class="hover:text-primary-900 dark:hover:text-primary-100 transition-colors"
          @click="removeItem(item.value)"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// ===== Types =====
interface Option {
  value: string | number;
  label: string;
  disabled?: boolean;
}

type ModelValue = string | number | string[] | number[];

// ===== Props =====
interface Props {
  modelValue: ModelValue;
  options: Option[];
  label?: string;
  placeholder?: string;
  id?: string;
  disabled?: boolean;
  required?: boolean;
  multiple?: boolean;
  error?: string;
  hint?: string;
  prefixIcon?: string;
  suffixIcon?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  options: () => [],
  label: '',
  placeholder: '',
  id: '',
  disabled: false,
  required: false,
  multiple: false,
  error: '',
  hint: '',
  prefixIcon: '',
  suffixIcon: ''
});

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:modelValue', value: ModelValue): void;
  (e: 'blur', event: FocusEvent): void;
  (e: 'focus', event: FocusEvent): void;
  (e: 'change', event: Event): void;
  (e: 'remove', value: string | number): void;
}>();

// ===== Helper Functions =====
const toArray = (value: ModelValue): (string | number)[] => {
  if (Array.isArray(value)) return value;
  return [value];
};

// ===== Computed =====
const inputId = computed(() => props.id || `select-${Math.random().toString(36).substring(2, 9)}`);

const selectedItems = computed<Option[]>(() => {
  if (!props.multiple) return [];
  
  const values = toArray(props.modelValue);
  return props.options.filter((opt: Option) => values.includes(opt.value));
});

// ===== Methods =====
const handleChange = (event: Event): void => {
  const target = event.target as HTMLSelectElement;
  emit('update:modelValue', target.value);
  emit('change', event);
};

const handleMultiChange = (event: Event): void => {
  const target = event.target as HTMLSelectElement;
  const values: string[] = Array.from(target.selectedOptions).map((opt: HTMLOptionElement) => opt.value);
  emit('update:modelValue', values);
  emit('change', event);
};

const handleBlur = (event: FocusEvent): void => {
  emit('blur', event);
};

const handleFocus = (event: FocusEvent): void => {
  emit('focus', event);
};

const removeItem = (value: string | number): void => {
  if (props.multiple) {
    const currentValues = toArray(props.modelValue);
    const newValue = currentValues.filter((v: string | number) => v !== value);
    // استفاده از emit با type assertion برای رفع خطای TypeScript
    (emit as any)('update:modelValue', newValue);
    (emit as any)('remove', value);
  }
};
</script>

<style scoped>
select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

select:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.dark select:disabled {
  background-color: #374151;
}

select[multiple] {
  appearance: auto;
  -webkit-appearance: auto;
  -moz-appearance: auto;
}

select[multiple] option {
  padding: 4px 8px;
}

select[multiple] option:checked {
  background: #2563eb;
  color: white;
}

.dark select[multiple] option:checked {
  background: #3b82f6;
  color: white;
}
</style>