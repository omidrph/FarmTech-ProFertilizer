import { computed, type Ref } from 'vue';

export function usePasswordRules(password: Ref<string>) {
  const rules = computed(() => {
    const p = password.value || '';
    return [
      { key: 'len', label: 'حداقل ۸ کاراکتر', ok: p.length >= 8 },
      { key: 'upper', label: 'یک حرف بزرگ انگلیسی', ok: /[A-Z]/.test(p) },
      { key: 'lower', label: 'یک حرف کوچک انگلیسی', ok: /[a-z]/.test(p) },
      { key: 'num', label: 'یک عدد', ok: /[0-9]/.test(p) },
      { key: 'sym', label: 'یک نماد مانند ! یا @', ok: /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]/.test(p) },
    ];
  });
  const isValid = computed(() => rules.value.every((r) => r.ok));
  return { rules, isValid };
}
