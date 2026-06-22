// frontend/src/composables/useApi.ts
import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios';
import { ref } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

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
    return config;
  });

  // Interceptor برای مدیریت خطاها - خطاها را در کنسول نشان نده
  api.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      // فقط خطاهای غیر از 401 را نمایش بده
      if (error.response?.status !== 401) {
        console.error('API Error:', error.message);
      }
      return Promise.reject(error);
    }
  );

  // تابع تست اتصال به بک‌اند
  const checkConnection = async (): Promise<boolean> => {
    try {
      const response = await axios.get('http://localhost:8000/health', {
        timeout: 3000,
      });
      isConnected.value = response.status === 200;
      return isConnected.value;
    } catch (err) {
      isConnected.value = false;
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
      }
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError;
      // فقط خطاهای غیر از 401 را نمایش بده
      if (axiosError.response?.status !== 401) {
        error.value = axiosError.message || 'خطا در ارتباط با سرور';
        console.error('API Error:', axiosError);
      }
      
      // اگر خطا 401 بود، خطا را برگردان (اما لاگ نکن)
      if (axiosError.response?.status === 401) {
        throw { response: { status: 401 }, message: 'Unauthorized' };
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