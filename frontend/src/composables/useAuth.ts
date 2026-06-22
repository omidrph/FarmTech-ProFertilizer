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
    console.log('🔑 Token set:', newToken.substring(0, 20) + '...');
  };

  const clearToken = () => {
    token.value = null;
    localStorage.removeItem('access_token');
    user.value = null;
    console.log('🔑 Token cleared');
  };

  // ===== دریافت اطلاعات کاربر =====
  const fetchUser = async (): Promise<boolean> => {
    if (!token.value) {
      console.warn('⚠️ No token available');
      return false;
    }

    try {
      console.log('👤 Fetching user info...');
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        timeout: 5000,
      });
      
      if (response.data) {
        user.value = response.data;
        console.log('✅ User fetched:', response.data.full_name);
        return true;
      }
      return false;
    } catch (error: any) {
      console.error('❌ Error fetching user:', error.response?.status, error.response?.data);
      
      if (error.response?.status === 401) {
        clearToken();
        console.warn('⚠️ Token expired, cleared');
      }
      return false;
    }
  };

  // ===== ثبت‌نام =====
  const register = async (data: RegisterData): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      console.log('📝 Registering user:', data.phone_number);
      const response = await axios.post(`${API_BASE_URL}/auth/register`, data, {
        timeout: 5000,
      });
      
      console.log('✅ Registration response:', response.status);
      
      if (response.status === 200 || response.status === 201) {
        // بعد از ثبت‌نام، کاربر را وارد کن
        const loginSuccess = await login(data.phone_number, data.password);
        return loginSuccess;
      }
      return false;
    } catch (err: any) {
      console.error('❌ Registration error:', err.response?.data);
      
      if (err.response?.status === 400) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          error.value = detail;
        } else if (detail && typeof detail === 'object' && 'msg' in detail) {
          error.value = detail.msg;
        } else {
          error.value = 'این شماره تلفن قبلاً ثبت شده است';
        }
      } else if (err.response?.status === 422) {
        const errors = err.response?.data?.errors;
        if (errors && Array.isArray(errors)) {
          error.value = errors.map((e: any) => e.message).join(', ');
        } else {
          error.value = 'خطا در اعتبارسنجی اطلاعات';
        }
      } else {
        error.value = err.response?.data?.detail || 'خطا در ثبت‌نام';
      }
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
      console.log('🔐 Logging in:', phone_number);
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        phone_number,
        password
      }, {
        timeout: 5000,
      });

      console.log('✅ Login response:', response.status);

      if (response.data.access_token) {
        const newToken = response.data.access_token;
        setToken(newToken);
        
        // دریافت اطلاعات کاربر
        const userFetched = await fetchUser();
        if (userFetched) {
          console.log('✅ Login successful for:', user.value?.full_name);
          return true;
        }
        
        // اگر اطلاعات کاربر دریافت نشد، توکن را پاک کن
        clearToken();
        error.value = 'خطا در دریافت اطلاعات کاربر';
        return false;
      }
      
      error.value = 'پاسخ سرور معتبر نیست';
      return false;
    } catch (err: any) {
      console.error('❌ Login error:', err.response?.status, err.response?.data);
      
      if (err.response?.status === 401) {
        error.value = 'شماره تلفن یا رمز عبور اشتباه است';
      } else if (err.response?.status === 403) {
        error.value = 'حساب کاربری غیرفعال است';
      } else if (err.response?.status === 404) {
        error.value = 'کاربر با این شماره تلفن یافت نشد';
      } else if (err.code === 'ECONNABORTED') {
        error.value = 'اتصال به سرور زمان‌بر است';
      } else if (err.message === 'Network Error') {
        error.value = 'ارتباط با سرور برقرار نیست. لطفاً مطمئن شوید بک‌اند در حال اجراست.';
      } else {
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
          },
          timeout: 2000
        }).catch(() => {});
      } catch {
        // خطا را نادیده بگیر
      }
    }
    console.log('👋 Logged out');
  };

  // ===== بررسی احراز هویت =====
  const checkAuth = async (): Promise<boolean> => {
    if (!token.value) {
      console.log('ℹ️ No token found');
      return false;
    }
    console.log('🔍 Checking auth...');
    return await fetchUser();
  };

  // ===== بررسی اتصال به بک‌اند =====
  const checkConnection = async (): Promise<boolean> => {
    try {
      const response = await axios.get('http://localhost:8000/health', { 
        timeout: 3000 
      });
      const connected = response.status === 200;
      console.log(`🔗 Backend connection: ${connected ? '✅ OK' : '❌ Failed'}`);
      return connected;
    } catch {
      console.warn('⚠️ Cannot connect to backend');
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