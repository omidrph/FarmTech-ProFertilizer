// frontend/src/services/apiService.ts
import axios, { type AxiosInstance, type AxiosResponse } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 15000,
    });

    // Interceptor برای اضافه کردن توکن
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Interceptor برای مدیریت خطاهای 401
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // ============================================================
  // Fertilizer APIs
  // ============================================================

  async getFertilizers(): Promise<any[]> {
    try {
      const response: AxiosResponse = await this.api.get('/fertilizers');
      return response.data || [];
    } catch (error) {
      console.error('Error fetching fertilizers:', error);
      throw error;
    }
  }

  async createFertilizer(data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post('/fertilizers', data);
      return response.data;
    } catch (error) {
      console.error('Error creating fertilizer:', error);
      throw error;
    }
  }

  async updateFertilizer(id: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.put(`/fertilizers/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating fertilizer:', error);
      throw error;
    }
  }

  async deleteFertilizer(id: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.delete(`/fertilizers/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting fertilizer:', error);
      throw error;
    }
  }

  // ============================================================
  // Report APIs
  // ============================================================

  async getReports(): Promise<any[]> {
    try {
      const response: AxiosResponse = await this.api.get('/reports');
      return response.data || [];
    } catch (error) {
      console.error('Error fetching reports:', error);
      throw error;
    }
  }

  async createReport(data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post('/reports', data);
      return response.data;
    } catch (error) {
      console.error('Error creating report:', error);
      throw error;
    }
  }

  async getReport(id: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.get(`/reports/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching report:', error);
      throw error;
    }
  }

  async updateReport(id: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.put(`/reports/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating report:', error);
      throw error;
    }
  }

  async deleteReport(id: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.delete(`/reports/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting report:', error);
      throw error;
    }
  }

  // ============================================================
  // Water Analysis APIs
  // ============================================================

  async getWaterAnalysis(reportId: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.get(`/water-analysis/${reportId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching water analysis:', error);
      throw error;
    }
  }

  async createWaterAnalysis(reportId: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post(`/water-analysis/${reportId}`, data);
      return response.data;
    } catch (error) {
      console.error('Error creating water analysis:', error);
      throw error;
    }
  }

  async updateWaterAnalysis(id: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.put(`/water-analysis/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating water analysis:', error);
      throw error;
    }
  }

  // ============================================================
  // Calculation APIs
  // ============================================================

  async getCalculation(reportId: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.get(`/calculations/${reportId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching calculation:', error);
      throw error;
    }
  }

  async createCalculation(reportId: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post(`/calculations/${reportId}`, data);
      return response.data;
    } catch (error) {
      console.error('Error creating calculation:', error);
      throw error;
    }
  }

  async updateCalculation(id: string, data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.put(`/calculations/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating calculation:', error);
      throw error;
    }
  }

  async calculateInterpretation(reportId: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post(`/calculations/${reportId}/calculate`);
      return response.data;
    } catch (error) {
      console.error('Error calculating interpretation:', error);
      throw error;
    }
  }

  // ============================================================
  // Auth APIs
  // ============================================================

  async login(phone_number: string, password: string): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post('/auth/login', {
        phone_number,
        password
      });
      return response.data;
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  }

  async register(data: any): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post('/auth/register', data);
      return response.data;
    } catch (error) {
      console.error('Error during registration:', error);
      throw error;
    }
  }

  async getCurrentUser(): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Error fetching current user:', error);
      throw error;
    }
  }

  async logout(): Promise<any> {
    try {
      const response: AxiosResponse = await this.api.post('/auth/logout');
      return response.data;
    } catch (error) {
      console.error('Error during logout:', error);
      throw error;
    }
  }
}

export const apiService = new ApiService();
export default apiService;