// frontend/src/services/apiService.ts
import axios, { type AxiosInstance, type AxiosResponse } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// ============================================================
// Types برای APIهای محاسباتی
// ============================================================
export interface IonBalanceRequest {
    elements: Record<string, number>;
    unit: 'ppm' | 'meq' | 'mmol';
}

export interface IonBalanceResponse {
    cation: number;
    anion: number;
    is_balanced: boolean;
    message: string;
}

export interface FinalSolutionRequest {
    target_values: Record<string, number>;
    water_values: Record<string, number>;
    fertilizer_contributions: Record<string, number>;
}

export interface FinalSolutionResponse {
    final_values: Record<string, number>;
    ion_balance: IonBalanceResponse;
}

export interface ReservoirRequest {
    fertilizers: Array<{
        fertilizer: any;
        weight: number;
        purity: number;
    }>;
}

export interface ReservoirResponse {
    reservoir_data: {
        A: Array<{ name: string; amount: number }>;
        B: Array<{ name: string; amount: number }>;
        C: Array<{ name: string; amount: number }>;
    };
    totals: { A: number; B: number; C: number };
}

export interface UnitConversionRequest {
    value: number;
    from_unit: string;
    to_unit: string;
    element: string;
}

export interface UnitConversionResponse {
    original_value: number;
    converted_value: number;
    from_unit: string;
    to_unit: string;
    element: string;
}

export interface HomeSummaryResponse {
    has_data: boolean;
    message?: string;
    ion_balance?: {
        cation: number;
        anion: number;
        is_balanced: boolean;
        message: string;
    };
    active_elements_count?: number;
    total_elements?: number;
    active_reservoirs_count?: number;
    total_cost?: number;
    total_reservoir_weight?: number;
    reservoir_data?: Record<string, any>;
    elements_data?: Array<{
        element: string;
        target: number;
        actual: number;
        difference: number;
        progress_percent: number;
    }>;
    recommendations?: Array<{
        type: 'success' | 'warning' | 'danger';
        title: string;
        description: string;
    }>;
    water_salinity?: number;
}

export interface LoadSystemFertilizersResponse {
    message: string;
    count?: number;
    stats?: {
        added: number;
        skipped: number;
        total: number;
        errors: any[];
    };
    already_loaded: boolean;
    success: boolean;
}

export interface ChangePasswordRequest {
    current_password: string;
    new_password: string;
}

export interface ChangePasswordResponse {
    message: string;
    success: boolean;
}

export interface UpdateProfileRequest {
    first_name?: string;
    last_name?: string;
}

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
    // 🆕 متدهای عمومی HTTP (برای انعطاف‌پذیری)
    // ============================================================
    async get<T = any>(url: string, config?: any): Promise<T> {
        const response: AxiosResponse<T> = await this.api.get(url, config);
        return response.data;
    }

    async post<T = any>(url: string, data?: any, config?: any): Promise<T> {
        const response: AxiosResponse<T> = await this.api.post(url, data, config);
        return response.data;
    }

    async put<T = any>(url: string, data?: any, config?: any): Promise<T> {
        const response: AxiosResponse<T> = await this.api.put(url, data, config);
        return response.data;
    }

    async delete<T = any>(url: string, config?: any): Promise<T> {
        const response: AxiosResponse<T> = await this.api.delete(url, config);
        return response.data;
    }

    // ============================================================
    // 🆕 APIهای محاسباتی
    // ============================================================
    async getHomeSummary(): Promise<HomeSummaryResponse> {
        try {
            const response: AxiosResponse<HomeSummaryResponse> = await this.api.get('/calculations/home-summary');
            return response.data;
        } catch (error) {
            console.error('Error fetching home summary:', error);
            throw error;
        }
    }

    async calculateIonBalance(data: IonBalanceRequest): Promise<IonBalanceResponse> {
        try {
            const response: AxiosResponse<IonBalanceResponse> = await this.api.post('/calculations/calculate-ion-balance', data);
            return response.data;
        } catch (error) {
            console.error('Error calculating ion balance:', error);
            throw error;
        }
    }

    async calculateFinalSolution(data: FinalSolutionRequest): Promise<FinalSolutionResponse> {
        try {
            const response: AxiosResponse<FinalSolutionResponse> = await this.api.post('/calculations/calculate-final-solution', data);
            return response.data;
        } catch (error) {
            console.error('Error calculating final solution:', error);
            throw error;
        }
    }

    async calculateReservoir(data: ReservoirRequest): Promise<ReservoirResponse> {
        try {
            const response: AxiosResponse<ReservoirResponse> = await this.api.post('/calculations/calculate-reservoir', data);
            return response.data;
        } catch (error) {
            console.error('Error calculating reservoir:', error);
            throw error;
        }
    }

    async convertUnit(data: UnitConversionRequest): Promise<UnitConversionResponse> {
        try {
            const response: AxiosResponse<UnitConversionResponse> = await this.api.post('/calculations/convert-unit', data);
            return response.data;
        } catch (error) {
            console.error('Error converting unit:', error);
            throw error;
        }
    }

    // ============================================================
    // 🆕 System Fertilizers
    // ============================================================
    async loadSystemFertilizers(): Promise<LoadSystemFertilizersResponse> {
        try {
            const response: AxiosResponse<LoadSystemFertilizersResponse> = await this.api.post('/fertilizers/load-system-fertilizers');
            return response.data;
        } catch (error) {
            console.error('Error loading system fertilizers:', error);
            throw error;
        }
    }

    // ============================================================
    // 🆕 Profile & User APIs
    // ============================================================
    /**
     * 🆕 به‌روزرسانی اطلاعات پروفایل کاربر
     */
    async updateProfile(data: UpdateProfileRequest): Promise<any> {
        try {
            const response: AxiosResponse = await this.api.put('/users/me', data);
            return response.data;
        } catch (error) {
            console.error('Error updating profile:', error);
            throw error;
        }
    }

    /**
     * 🆕 تغییر رمز عبور
     */
    async changePassword(data: ChangePasswordRequest): Promise<ChangePasswordResponse> {
        try {
            const response: AxiosResponse<ChangePasswordResponse> = await this.api.post('/auth/change-password', data);
            return response.data;
        } catch (error) {
            console.error('Error changing password:', error);
            throw error;
        }
    }

    /**
     * 🆕 دریافت اطلاعات کاربر فعلی
     */
    async getCurrentUser(): Promise<any> {
        try {
            const response: AxiosResponse = await this.api.get('/auth/me');
            return response.data;
        } catch (error) {
            console.error('Error fetching current user:', error);
            throw error;
        }
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