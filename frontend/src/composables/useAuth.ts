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
    try {
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith('access_token=')) {
          return trimmed.substring('access_token='.length);
        }
      }
      return null;
    } catch {
      return null;
    }
  };

  // ===== دریافت توکن =====
  const getToken = (): string | null => {
    if (token.value) return token.value;
    
    const cookieToken = getTokenFromCookie();
    if (cookieToken) {
      token.value = cookieToken;
      return cookieToken;
    }
    
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      token.value = storedToken;
      return storedToken;
    }
    
    return null;
  };

  const setToken = (newToken: string) => {
    token.value = newToken;
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
        withCredentials: true
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
        const cookieToken = getTokenFromCookie();
        if (cookieToken) {
          setToken(cookieToken);
          await fetchUser();
          return true;
        }
        
        if (response.data?.access_token) {
          setToken(response.data.access_token);
          await fetchUser();
          return true;
        }
        
        await login(data.phone_number, data.password);
        return true;
      }
      return false;
    } catch (err: any) {
      console.error('❌ Registration error:', err.response?.data);
      
      // ================================================================
      // مدیریت دقیق تمام انواع خطاها
      // ================================================================
      
      if (err.response) {
        const status = err.response.status;
        const responseData = err.response.data;
        
        // === خطاهای 400 (Bad Request) ===
        if (status === 400) {
          // حالت 1: detail به صورت string
          if (typeof responseData?.detail === 'string') {
            error.value = responseData.detail;
          }
          // حالت 2: detail به صورت object
          else if (responseData?.detail && typeof responseData.detail === 'object') {
            if (responseData.detail.msg) {
              error.value = responseData.detail.msg;
            } else if (responseData.detail.message) {
              error.value = responseData.detail.message;
            } else {
              error.value = 'اطلاعات وارد شده صحیح نیست. لطفاً بررسی کنید.';
            }
          }
          // حالت 3: message مستقیم
          else if (responseData?.message) {
            error.value = responseData.message;
          }
          // حالت 4: errors array
          else if (responseData?.errors && Array.isArray(responseData.errors)) {
            const firstError = responseData.errors[0];
            error.value = firstError?.message || firstError?.msg || 'خطا در اعتبارسنجی اطلاعات.';
          }
          // حالت پیش‌فرض
          else {
            error.value = 'این شماره تلفن قبلاً ثبت شده است یا اطلاعات وارد شده معتبر نیست.';
          }
          return false;
        }
        
        // === خطاهای 422 (Validation Error) ===
        if (status === 422) {
          if (typeof responseData?.detail === 'string') {
            error.value = responseData.detail;
          } else if (responseData?.errors && Array.isArray(responseData.errors)) {
            const firstError = responseData.errors[0];
            error.value = `${firstError.field || 'ورودی'}: ${firstError.message || 'نامعتبر است'}`;
          } else {
            error.value = 'خطا در اعتبارسنجی داده‌ها. لطفاً اطلاعات را بررسی کنید.';
          }
          return false;
        }
        
        // === خطاهای 403 (Forbidden) ===
        if (status === 403) {
          error.value = responseData?.detail || 'حساب کاربری غیرفعال یا قفل شده است.';
          return false;
        }
        
        // === خطاهای 404 (Not Found) ===
        if (status === 404) {
          error.value = responseData?.detail || 'منبع درخواستی یافت نشد.';
          return false;
        }
        
        // === خطاهای 429 (Too Many Requests) ===
        if (status === 429) {
          error.value = responseData?.detail || 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً چند دقیقه دیگر تلاش کنید.';
          return false;
        }
        
        // === سایر خطاهای 4xx و 5xx ===
        if (status >= 400 && status < 600) {
          if (typeof responseData?.detail === 'string') {
            error.value = responseData.detail;
          } else if (responseData?.message) {
            error.value = responseData.message;
          } else {
            error.value = `خطا در ثبت‌نام (کد ${status}). لطفاً دوباره تلاش کنید.`;
          }
          return false;
        }
      }
      
      // === خطاهای شبکه ===
      if (err.code === 'ECONNABORTED') {
        error.value = 'اتصال به سرور زمان‌بر است. لطفاً دوباره تلاش کنید.';
      } else if (err.message === 'Network Error') {
        error.value = 'ارتباط با سرور برقرار نیست. لطفاً مطمئن شوید بک‌اند در حال اجراست.';
      } else {
        error.value = err.message || 'خطای ناشناخته در ثبت‌نام.';
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

      const cookieToken = getTokenFromCookie();
      if (cookieToken) {
        setToken(cookieToken);
        const userFetched = await fetchUser();
        if (userFetched) {
          console.log('✅ Login successful for:', user.value?.full_name);
          return true;
        }
      }

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

  // ===== خروج - نسخه کامل اصلاح شده =====
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
      } catch (error) {
        // خطا را نادیده بگیر - حتی اگر سرور پاسخ ندهد، ما توکن را پاک می‌کنیم
        console.warn('Logout API error (ignored):', error);
      }
    }
    
    // ============================================================
    // ✅ پاک کردن کامل تمام state ها
    // ============================================================
    
    // 1. پاک کردن توکن از حافظه
    token.value = null;
    
    // 2. پاک کردن کاربر
    user.value = null;
    
    // 3. پاک کردن localStorage
    localStorage.removeItem('access_token');
    
    // 4. پاک کردن cookie (چندین روش برای اطمینان)
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; domain=localhost';
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; domain=.localhost';
    
    // 5. پاک کردن error
    error.value = null;
    
    console.log('👋 Logged out - All state cleared');
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