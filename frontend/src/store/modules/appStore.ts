import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

type ThemeType = 'light' | 'dark';
type LanguageType = 'fa' | 'en';

export const useAppStore = defineStore('app', () => {
  // ===== State =====
  const theme = ref<ThemeType>('light');
  const language = ref<LanguageType>('fa');
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  // ===== Getters =====
  const isDarkMode = computed(() => theme.value === 'dark');
  const isRTL = computed(() => language.value === 'fa');
  const currentLanguage = computed(() => language.value);

  // ===== Actions =====
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', theme.value);
  }

  function setTheme(newTheme: ThemeType) {
    theme.value = newTheme;
    localStorage.setItem('theme', theme.value);
  }

  function toggleLanguage() {
    language.value = language.value === 'fa' ? 'en' : 'fa';
    localStorage.setItem('language', language.value);
  }

  function setLanguage(newLanguage: LanguageType) {
    language.value = newLanguage;
    localStorage.setItem('language', language.value);
  }

  function setLoading(loading: boolean) {
    isLoading.value = loading;
  }

  function setError(newError: string | null) {
    error.value = newError;
  }

  function clearError() {
    error.value = null;
  }

  // ===== Init from localStorage =====
  function initFromStorage() {
    const savedTheme = localStorage.getItem('theme') as ThemeType | null;
    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      theme.value = savedTheme;
    }

    const savedLanguage = localStorage.getItem('language') as LanguageType | null;
    if (savedLanguage && (savedLanguage === 'fa' || savedLanguage === 'en')) {
      language.value = savedLanguage;
    }
  }

  initFromStorage();

  return {
    theme,
    language,
    isLoading,
    error,
    isDarkMode,
    isRTL,
    currentLanguage,
    toggleTheme,
    setTheme,
    toggleLanguage,
    setLanguage,
    setLoading,
    setError,
    clearError
  };
});