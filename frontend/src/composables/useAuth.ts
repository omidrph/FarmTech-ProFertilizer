// frontend/src/composables/useAuth.ts
import { ref, computed } from 'vue';
import axios from 'axios';
import type { RegisterData, User } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export function useAuth() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value);

  // ===== تنظیم توکن از Cookie =====
  const getTokenFromCookie = (): string | null => {
    // تلاش برای دریافت توکن از Cookie
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'access_token') {
        return value;
      }
    }
    return null;
  };

  // ===== دریافت توکن =====
  const getToken = (): string | null => {
    if (token.value) return token.value;
    
    // تلاش از Cookie
    const cookieToken = getTokenFromCookie();
    if (cookieToken) {
      token.value = cookieToken;
      return cookieToken;
    }
    
    // Fallback به localStorage (برای سازگاری با نسخه‌های قبلی)
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      token.value = storedToken;
      return storedToken;
    }
    
    return null;
  };

  const setToken = (newToken: string) => {
    token.value = newToken;
    // برای سازگاری، در localStorage هم ذخیره کن (فعلاً)
    localStorage.setItem('access_token', newToken);
  };

  const clearToken = () => {
    token.value = null;
    localStorage.removeItem('access_token');
    user.value = null;
  };

  // ===== دریافت اطلاعات کاربر =====
  const fetchUser = async (): Promise<boolean> => {
    const currentToken = getToken();
    if (!currentToken) {
      console.warn('⚠️ No token available');
      return false;
    }

    try {
      console.log('👤 Fetching user info...');
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${currentToken}`
        },
        timeout: 5000,
        withCredentials: true // برای ارسال Cookie
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
        withCredentials: true
      });
      
      console.log('✅ Registration response:', response.status);
      
      if (response.status === 200 || response.status === 201) {
        // دریافت توکن از Cookie
        const cookieToken = getTokenFromCookie();
        if (cookieToken) {
          setToken(cookieToken);
          await fetchUser();
          return true;
        }
        
        // Fallback: از response
        if (response.data?.access_token) {
          setToken(response.data.access_token);
          await fetchUser();
          return true;
        }
        
        // اگر توکنی نبود، با اطلاعات کاربر وارد شو
        await login(data.phone_number, data.password);
        return true;
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
        withCredentials: true
      });

      console.log('✅ Login response:', response.status);

      // دریافت توکن از Cookie
      const cookieToken = getTokenFromCookie();
      if (cookieToken) {
        setToken(cookieToken);
        const userFetched = await fetchUser();
        if (userFetched) {
          console.log('✅ Login successful for:', user.value?.full_name);
          return true;
        }
      }

      // Fallback: از response
      if (response.data?.access_token) {
        const newToken = response.data.access_token;
        setToken(newToken);
        
        const userFetched = await fetchUser();
        if (userFetched) {
          console.log('✅ Login successful for:', user.value?.full_name);
          return true;
        }
        
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
        error.value = err.response?.data?.detail || 'حساب کاربری غیرفعال یا قفل شده است';
      } else if (err.response?.status === 404) {
        error.value = 'کاربر با این شماره تلفن یافت نشد';
      } else if (err.response?.status === 429) {
        error.value = err.response?.data?.detail || 'تعداد درخواست‌های شما بیش از حد مجاز است';
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
  const logout = async () => {
    const currentToken = getToken();
    
    // ارسال درخواست خروج به سرور
    if (currentToken) {
      try {
        await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
          headers: {
            Authorization: `Bearer ${currentToken}`
          },
          timeout: 2000,
          withCredentials: true
        });
      } catch {
        // خطا را نادیده بگیر
      }
    }
    
    clearToken();
    console.log('👋 Logged out');
  };

  // ===== بررسی احراز هویت =====
  const checkAuth = async (): Promise<boolean> => {
    const currentToken = getToken();
    if (!currentToken) {
      console.log('ℹ️ No token found');
      return false;
    }
    console.log('🔍 Checking auth...');
    return await fetchUser();
  };

  // ===== فراموشی رمز عبور =====
  const forgotPassword = async (phone_number: string): Promise<{ success: boolean; message: string }> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/forgot-password`, {
        phone_number
      }, {
        timeout: 10000,
        withCredentials: true
      });

      if (response.data?.success) {
        return {
          success: true,
          message: response.data.message || 'کد تأیید به شماره تلفن شما ارسال شد'
        };
      }
      
      return {
        success: false,
        message: response.data?.message || 'خطا در ارسال کد تأیید'
      };
    } catch (err: any) {
      console.error('❌ Forgot password error:', err);
      const message = err.response?.data?.detail || 'خطا در درخواست فراموشی رمز عبور';
      error.value = message;
      return { success: false, message };
    } finally {
      isLoading.value = false;
    }
  };

  // ===== بازنشانی رمز عبور =====
  const resetPassword = async (phone_number: string, code: string, new_password: string): Promise<{ success: boolean; message: string }> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/reset-password`, {
        phone_number,
        code,
        new_password
      }, {
        timeout: 10000,
        withCredentials: true
      });

      if (response.data?.success) {
        return {
          success: true,
          message: response.data.message || 'رمز عبور با موفقیت بازنشانی شد'
        };
      }
      
      return {
        success: false,
        message: response.data?.message || 'خطا در بازنشانی رمز عبور'
      };
    } catch (err: any) {
      console.error('❌ Reset password error:', err);
      const message = err.response?.data?.detail || 'خطا در بازنشانی رمز عبور';
      error.value = message;
      return { success: false, message };
    } finally {
      isLoading.value = false;
    }
  };

  // ===== تغییر رمز عبور =====
  const changePassword = async (current_password: string, new_password: string): Promise<{ success: boolean; message: string }> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/change-password`, {
        current_password,
        new_password
      }, {
        timeout: 10000,
        withCredentials: true
      });

      if (response.data?.success) {
        return {
          success: true,
          message: response.data.message || 'رمز عبور با موفقیت تغییر کرد'
        };
      }
      
      return {
        success: false,
        message: response.data?.message || 'خطا در تغییر رمز عبور'
      };
    } catch (err: any) {
      console.error('❌ Change password error:', err);
      const message = err.response?.data?.detail || 'خطا در تغییر رمز عبور';
      error.value = message;
      return { success: false, message };
    } finally {
      isLoading.value = false;
    }
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
    clearToken,
    getToken,
    forgotPassword,
    resetPassword,
    changePassword
  };
}