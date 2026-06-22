// frontend/src/composables/useApi.ts
import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios';
import { ref } from 'vue';

// استفاده از متغیر محیطی
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export function useApi() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const isConnected = ref(false);

  const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 10000,
  });

  // Interceptor برای اضافه کردن توکن
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // لاگ برای دیباگ
    console.log(`📤 ${config.method?.toUpperCase()} ${config.url}`, config.data);
    return config;
  });

  // Interceptor برای مدیریت خطاها
  api.interceptors.response.use(
    (response) => {
      console.log(`✅ ${response.status} ${response.config.url}`);
      return response;
    },
    (error: AxiosError) => {
      // لاگ خطا برای دیباگ
      console.error('❌ API Error:', {
        status: error.response?.status,
        url: error.config?.url,
        data: error.response?.data,
        message: error.message
      });
      
      // اگر خطا ۴۰۱ بود، توکن را پاک کن
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        // اگر در صفحه لاگین نیستیم، به لاگین هدایت کن
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
      }
      
      return Promise.reject(error);
    }
  );

  // تابع تست اتصال به بک‌اند
  const checkConnection = async (): Promise<boolean> => {
    try {
      const response = await axios.get(`${BACKEND_URL}/health`, {
        timeout: 3000,
      });
      isConnected.value = response.status === 200;
      console.log(`🔗 Connection status: ${isConnected.value ? '✅ Connected' : '❌ Disconnected'}`);
      return isConnected.value;
    } catch (err) {
      isConnected.value = false;
      console.warn('⚠️ Cannot connect to backend:', err);
      return false;
    }
  };

  // تابع اصلی برای درخواست‌ها
  const request = async <T>(
    method: 'get' | 'post' | 'put' | 'delete',
    url: string,
    data?: any
  ): Promise<T | null> => {
    isLoading.value = true;
    error.value = null;

    try {
      let response: AxiosResponse<T>;
      switch (method) {
        case 'get':
          response = await api.get<T>(url);
          break;
        case 'post':
          response = await api.post<T>(url, data);
          break;
        case 'put':
          response = await api.put<T>(url, data);
          break;
        case 'delete':
          response = await api.delete<T>(url);
          break;
        default:
          throw new Error(`Method ${method} not supported`);
      }
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError;
      
      // خطاهای خاص را مدیریت کن
      if (axiosError.response?.status === 401) {
        // توکن منقضی شده - اجازه بده خطا به بالا برود
        throw err;
      }
      
      if (axiosError.response?.status === 422) {
        error.value = 'خطا در اعتبارسنجی داده‌ها';
      } else if (axiosError.code === 'ECONNABORTED') {
        error.value = 'مدت زمان درخواست به پایان رسید';
      } else if (axiosError.message === 'Network Error') {
        error.value = 'ارتباط با سرور برقرار نیست';
      } else {
        error.value = axiosError.message || 'خطا در ارتباط با سرور';
      }
      
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    api,
    isLoading,
    error,
    isConnected,
    checkConnection,
    request,
  };
}