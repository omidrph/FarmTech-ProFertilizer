// frontend/src/composables/useValidation.ts
import { ref } from 'vue';

export interface ValidationRule {
  required?: boolean;
  min?: number;
  max?: number;
  positive?: boolean;
  percent?: boolean;
  pattern?: RegExp;
  custom?: (value: any) => boolean;
  message?: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: Record<string, string>;
}

export function useValidation() {
  const errors = ref<Record<string, string>>({});
  const touched = ref<Record<string, boolean>>({});

  // ============================================================
  // اعتبارسنجی یک فیلد
  // ============================================================

  function validateField(
    value: any,
    rules: ValidationRule[],
    _fieldName: string
  ): { valid: boolean; message: string | null } {
    for (const rule of rules) {
      if (rule.required && (!value || value === '' || value === null || value === undefined)) {
        return {
          valid: false,
          message: rule.message || 'این فیلد اجباری است'
        };
      }

      if (value !== undefined && value !== null && value !== '') {
        const numValue = Number(value);
        
        if (isNaN(numValue)) {
          return {
            valid: false,
            message: 'لطفاً یک عدد معتبر وارد کنید'
          };
        }

        if (rule.min !== undefined && numValue < rule.min) {
          return {
            valid: false,
            message: rule.message || `حداقل مقدار ${rule.min} است`
          };
        }

        if (rule.max !== undefined && numValue > rule.max) {
          return {
            valid: false,
            message: rule.message || `حداکثر مقدار ${rule.max} است`
          };
        }

        if (rule.positive && numValue <= 0) {
          return {
            valid: false,
            message: 'مقدار باید مثبت باشد'
          };
        }

        if (rule.percent && (numValue < 0 || numValue > 100)) {
          return {
            valid: false,
            message: 'مقدار باید بین 0 تا 100 باشد'
          };
        }

        if (rule.pattern && !rule.pattern.test(String(value))) {
          return {
            valid: false,
            message: rule.message || 'فرمت وارد شده صحیح نیست'
          };
        }

        if (rule.custom && !rule.custom(value)) {
          return {
            valid: false,
            message: rule.message || 'مقدار وارد شده معتبر نیست'
          };
        }
      }
    }

    return { valid: true, message: null };
  }

  // ============================================================
  // اعتبارسنجی فرم
  // ============================================================

  function validateForm(
    fields: Record<string, { value: any; rules: ValidationRule[] }>
  ): ValidationResult {
    const result: ValidationResult = {
      valid: true,
      errors: {}
    };

    for (const [fieldName, field] of Object.entries(fields)) {
      const validation = validateField(field.value, field.rules, fieldName);
      if (!validation.valid) {
        result.valid = false;
        result.errors[fieldName] = validation.message || 'خطا در اعتبارسنجی';
      }
    }

    errors.value = result.errors;
    return result;
  }

  function showError(fieldName: string): boolean {
    return !!errors.value[fieldName] && touched.value[fieldName];
  }

  function getError(fieldName: string): string | null {
    return errors.value[fieldName] || null;
  }

  function markTouched(fieldName: string) {
    touched.value[fieldName] = true;
  }

  function clearErrors() {
    errors.value = {};
  }

  function clearTouched() {
    touched.value = {};
  }

  const rules = {
    required: (message?: string): ValidationRule[] => [
      { required: true, message: message || 'این فیلد اجباری است' }
    ],
    number: (min?: number, max?: number, message?: string): ValidationRule[] => {
      const rules: ValidationRule[] = [];
      if (min !== undefined) rules.push({ min, message });
      if (max !== undefined) rules.push({ max, message });
      return rules;
    },
    positiveNumber: (message?: string): ValidationRule[] => [
      { positive: true, message: message || 'مقدار باید مثبت باشد' }
    ],
    percent: (message?: string): ValidationRule[] => [
      { percent: true, message: message || 'مقدار باید بین 0 تا 100 باشد' }
    ],
    pattern: (pattern: RegExp, message?: string): ValidationRule[] => [
      { pattern, message: message || 'فرمت وارد شده صحیح نیست' }
    ],
    custom: (custom: (value: any) => boolean, message?: string): ValidationRule[] => [
      { custom, message: message || 'مقدار وارد شده معتبر نیست' }
    ]
  };

  return {
    errors,
    touched,
    validateField,
    validateForm,
    showError,
    getError,
    markTouched,
    clearErrors,
    clearTouched,
    rules
  };
}