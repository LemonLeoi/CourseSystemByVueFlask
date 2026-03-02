import { ref, computed } from 'vue';

interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  message: string;
}

// 未使用的接口
// interface ValidationField {
//   value: any;
//   rules: ValidationRule[];
// }

interface ValidationErrors {
  [field: string]: string[];
}

export function useValidation() {
  const errors = ref<ValidationErrors>({});
  const isSubmitting = ref(false);

  const validateField = (_fieldName: string, value: any, rules: ValidationRule[]): string[] => {
    const fieldErrors: string[] = [];

    rules.forEach(rule => {
      if (rule.required && !value) {
        fieldErrors.push(rule.message);
      } else if (rule.minLength && String(value).length < rule.minLength) {
        fieldErrors.push(rule.message);
      } else if (rule.maxLength && String(value).length > rule.maxLength) {
        fieldErrors.push(rule.message);
      } else if (rule.pattern && !rule.pattern.test(String(value))) {
        fieldErrors.push(rule.message);
      }
    });

    return fieldErrors;
  };

  const validateForm = (formData: Record<string, any>, validationRules: Record<string, ValidationRule[]>): boolean => {
    const formErrors: ValidationErrors = {};
    let isValid = true;

    Object.keys(validationRules).forEach(fieldName => {
      const value = formData[fieldName];
      const rules = validationRules[fieldName] || [];
      const fieldErrors = validateField(fieldName, value, rules);

      if (fieldErrors.length > 0) {
        formErrors[fieldName] = fieldErrors;
        isValid = false;
      }
    });

    errors.value = formErrors;
    return isValid;
  };

  const resetErrors = () => {
    errors.value = {};
  };

  const setError = (fieldName: string, message: string) => {
    errors.value[fieldName] = [message];
  };

  const removeError = (fieldName: string) => {
    delete errors.value[fieldName];
  };

  const isValid = computed(() => {
    return Object.keys(errors.value).length === 0;
  });

  return {
    errors,
    isSubmitting,
    validateField,
    validateForm,
    resetErrors,
    setError,
    removeError,
    isValid
  };
}
