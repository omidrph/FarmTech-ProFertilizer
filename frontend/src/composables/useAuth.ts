// frontend/src/composables/useAuth.ts
import { ref, computed } from 'vue';
import axios from 'axios';
import type { RegisterData, User } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export function useAuth() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('access_token'));

  const isAuthenticated = computed(() => !!token.value);

  const setToken = (newToken: string) => {
    token.value = newToken;
    localStorage.setItem('access_token', newToken);
  };

  const clearToken = () => {
    token.value = null;
    localStorage.removeItem('access_token');
    user.value = null;
  };

  // ===== دریافت اطلاعات کاربر (با توکن واقعی) =====
  const fetchUser = async (): Promise<boolean> => {
    if (!token.value) {
      return false;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        timeout: 5000,
      });
      
      if (response.data) {
        user.value = response.data;
        return true;
      }
      return false;
    } catch (error: any) {
      // اگر توکن نامعتبر بود، پاکش کن (اما خطا را نمایش نده)
      if (error.response?.status === 401) {
        // توکن منقضی شده است، پاکش کن
        clearToken();
        // فقط در حالت دیباگ لاگ کن
        if (import.meta.env.DEV) {
          console.debug('🔑 توکن منقضی شده، پاک شد');
        }
      }
      return false;
    }
  };

  // ===== ثبت‌نام =====
  const register = async (data: RegisterData): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, data, {
        timeout: 5000,
      });
      
      if (response.status === 200 || response.status === 201) {
        // بعد از ثبت‌نام، کاربر را وارد کن
        const loginSuccess = await login(data.phone_number, data.password);
        return loginSuccess;
      }
      return false;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'خطا در ثبت‌نام';
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // ===== ورود =====
  const login = async (phone_number: string, password: string): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        phone_number,
        password
      }, {
        timeout: 5000,
      });

      if (response.data.access_token) {
        const newToken = response.data.access_token;
        setToken(newToken);
        
        // دریافت اطلاعات کاربر
        const userFetched = await fetchUser();
        if (userFetched) {
          return true;
        }
        
        // اگر اطلاعات کاربر دریافت نشد، توکن را پاک کن
        clearToken();
        return false;
      }
      return false;
    } catch (err: any) {
      // خطای 401 را در کنسول نشان نده (کاربر قبلاً لاگین کرده)
      if (err.response?.status !== 401) {
        error.value = err.response?.data?.detail || 'خطا در ورود';
      }
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // ===== خروج =====
  const logout = () => {
    const currentToken = token.value;
    clearToken();
    
    // ارسال درخواست خروج به سرور (اختیاری)
    if (currentToken) {
      try {
        axios.post(`${API_BASE_URL}/auth/logout`, {}, {
          headers: {
            Authorization: `Bearer ${currentToken}`
          }
        }).catch(() => {});
      } catch {
        // خطا را نادیده بگیر
      }
    }
  };

  // ===== بررسی احراز هویت =====
  const checkAuth = async (): Promise<boolean> => {
    if (!token.value) {
      return false;
    }
    return await fetchUser();
  };

  // ===== بررسی اتصال به بک‌اند =====
  const checkConnection = async (): Promise<boolean> => {
    try {
      const response = await axios.get('http://localhost:8000/health', { 
        timeout: 3000 
      });
      return response.status === 200;
    } catch {
      return false;
    }
  };

  return {
    isLoading,
    error,
    user,
    token,
    isAuthenticated,
    register,
    login,
    logout,
    checkAuth,
    checkConnection,
    setToken,
    clearToken
  };
}