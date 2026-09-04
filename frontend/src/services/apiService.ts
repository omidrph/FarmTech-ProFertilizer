// frontend/src/services/apiService.ts
import axios, { type AxiosInstance, type AxiosResponse } from 'axios';
import type {
    OptimizationRequest,
    OptimizationResponse,
    PrecipitationCheckResponse,
    OptimizationLogResponse
} from '@/types';

// 🔧 همان اصلاح useApi.ts: پیش‌فرض به مسیر نسبی هم‌مبدأ تغییر کرد چون
// آدرس لوکال قبلی در build نهایی برای کاربران واقعی کار نمی‌کرد.
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

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
        A: Array<{ 
            name: string; 
            amount: number; 
            fertilizer_id?: string;
            has_calcium?: boolean;
        }>;
        B: Array<{ 
            name: string; 
            amount: number; 
            fertilizer_id?: string;
            has_calcium?: boolean;
            is_acid?: boolean;
        }>;
        C: Array<{ 
            name: string; 
            amount: number; 
            fertilizer_id?: string;
            is_acid?: boolean;
        }>;
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

// ============================================================
// 🔐 انواع جدید برای فراموشی رمز عبور و 2FA
// ============================================================

export interface ForgotPasswordRequest {
    phone_number: string;
}

export interface ForgotPasswordResponse {
    message: string;
    success: boolean;
    reset_id?: string;
}

export interface ResetPasswordRequest {
    phone_number: string;
    code: string;
    new_password: string;
}

export interface ResetPasswordResponse {
    message: string;
    success: boolean;
}

export interface Enable2FARequest {
    phone_number: string;
}

export interface Enable2FAResponse {
    secret: string;
    backup_codes: string[];
    qr_code_url?: string;
    message: string;
    success: boolean;
}

export interface Verify2FARequest {
    code: string;
}

export interface Verify2FAResponse {
    message: string;
    success: boolean;
}

export interface Disable2FARequest {
    code: string;
}

export interface Disable2FAResponse {
    message: string;
    success: boolean;
}

// ============================================================
// Recipe Types
// ============================================================
export interface Recipe {
    id: number;
    name: string;
    description?: string;
    target_values: Record<string, number>;
    category?: string;
    stage?: string;
    is_system: boolean;
    user_id?: number;
    created_at: string;
    updated_at?: string;
}

export interface RecipeCreate {
    name: string;
    description?: string;
    target_values: Record<string, number>;
    category?: string;
    stage?: string;
}

export interface RecipeUpdate {
    name?: string;
    description?: string;
    target_values?: Record<string, number>;
    category?: string;
    stage?: string;
}

export interface RecipeListResponse {
    system_recipes: Recipe[];
    user_recipes: Recipe[];
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
            withCredentials: true, // 🔐 برای ارسال Cookie
        });

        // 🔐 Interceptor برای اضافه کردن توکن از Cookie
        this.api.interceptors.request.use((config) => {
            // تلاش برای دریافت توکن از Cookie
            const token = this.getTokenFromCookie();
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            } else {
                // Fallback به localStorage برای سازگاری
                const storedToken = localStorage.getItem('access_token');
                if (storedToken) {
                    config.headers.Authorization = `Bearer ${storedToken}`;
                }
            }
            return config;
        });

        // 🔐 Interceptor برای مدیریت خطاهای احراز هویت
        this.api.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    this.clearToken();
                    if (!window.location.pathname.includes('/login') && 
                        !window.location.pathname.includes('/register') &&
                        !window.location.pathname.includes('/forgot-password')) {
                        window.location.href = '/login';
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    // ============================================================
    // 🔐 توابع کمکی برای مدیریت توکن
    // ============================================================

    private getTokenFromCookie(): string | null {
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
    }

    private clearToken(): void {
        localStorage.removeItem('access_token');
        // Cookie در سرور پاک می‌شود
    }

    // ============================================================
    // متدهای عمومی HTTP
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
    // APIهای بهینه‌سازی
    // ============================================================

    async optimizeFertilizers(data: OptimizationRequest): Promise<OptimizationResponse> {
        try {
            const response: AxiosResponse<OptimizationResponse> = await this.api.post(
                '/calculations/optimize',
                data
            );
            return response.data;
        } catch (error) {
            console.error('Error optimizing fertilizers:', error);
            throw error;
        }
    }

    /**
     * 🆕 محاسبه مجدد نتیجه پس از ویرایش دستی وزن یک کود در جدول نتیجه
     * (بدون اجرای دوباره الگوریتم بهینه‌سازی NNLS)
     */
    async recalculateManualWeights(data: {
        fertilizers: any[];
        weights: Record<string, number>;
        target_values: Record<string, number>;
        water_values?: Record<string, number>;
        tank_volume: number;
    }): Promise<OptimizationResponse> {
        try {
            const response: AxiosResponse<OptimizationResponse> = await this.api.post(
                '/calculations/recalculate-manual',
                data
            );
            return response.data;
        } catch (error) {
            console.error('Error recalculating manual weights:', error);
            throw error;
        }
    }

    async checkPrecipitation(concentrations: Record<string, number>, temperature: number = 25): Promise<PrecipitationCheckResponse> {
        try {
            const response: AxiosResponse<PrecipitationCheckResponse> = await this.api.post(
                '/calculations/check-precipitation',
                { concentrations, temperature }
            );
            return response.data;
        } catch (error) {
            console.error('Error checking precipitation:', error);
            throw error;
        }
    }

    async getOptimizationHistory(skip: number = 0, limit: number = 50, report_id?: number): Promise<OptimizationLogResponse[]> {
        try {
            let url = `/calculations/optimization-history?skip=${skip}&limit=${limit}`;
            if (report_id) {
                url += `&report_id=${report_id}`;
            }
            const response: AxiosResponse<OptimizationLogResponse[]> = await this.api.get(url);
            return response.data;
        } catch (error) {
            console.error('Error fetching optimization history:', error);
            throw error;
        }
    }

    // ============================================================
    // APIهای محاسباتی
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
    // System Fertilizers
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
    // Profile & User APIs
    // ============================================================
    async updateProfile(data: UpdateProfileRequest): Promise<any> {
        try {
            const response: AxiosResponse = await this.api.put('/users/me', data);
            return response.data;
        } catch (error) {
            console.error('Error updating profile:', error);
            throw error;
        }
    }

    async changePassword(data: ChangePasswordRequest): Promise<ChangePasswordResponse> {
        try {
            const response: AxiosResponse<ChangePasswordResponse> = await this.api.post('/auth/change-password', data);
            return response.data;
        } catch (error) {
            console.error('Error changing password:', error);
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

    // ============================================================
    // 🔐 Auth APIs جدید
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

    // ============================================================
    // 🔐 فراموشی رمز عبور
    // ============================================================

    async forgotPassword(phone_number: string): Promise<ForgotPasswordResponse> {
        try {
            const response: AxiosResponse<ForgotPasswordResponse> = await this.api.post('/auth/forgot-password', {
                phone_number
            });
            return response.data;
        } catch (error) {
            console.error('Error during forgot password:', error);
            throw error;
        }
    }

    async resetPassword(phone_number: string, code: string, new_password: string): Promise<ResetPasswordResponse> {
        try {
            const response: AxiosResponse<ResetPasswordResponse> = await this.api.post('/auth/reset-password', {
                phone_number,
                code,
                new_password
            });
            return response.data;
        } catch (error) {
            console.error('Error during reset password:', error);
            throw error;
        }
    }

    // ============================================================
    // 🔐 تأیید دو مرحله‌ای (2FA)
    // ============================================================

    async enable2FA(phone_number: string): Promise<Enable2FAResponse> {
        try {
            const response: AxiosResponse<Enable2FAResponse> = await this.api.post('/auth/enable-2fa', {
                phone_number
            });
            return response.data;
        } catch (error) {
            console.error('Error enabling 2FA:', error);
            throw error;
        }
    }

    async verify2FA(code: string): Promise<Verify2FAResponse> {
        try {
            const response: AxiosResponse<Verify2FAResponse> = await this.api.post('/auth/verify-2fa', {
                code
            });
            return response.data;
        } catch (error) {
            console.error('Error verifying 2FA:', error);
            throw error;
        }
    }

    async disable2FA(code: string): Promise<Disable2FAResponse> {
        try {
            const response: AxiosResponse<Disable2FAResponse> = await this.api.post('/auth/disable-2fa', {
                code
            });
            return response.data;
        } catch (error) {
            console.error('Error disabling 2FA:', error);
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
    // Recipe APIs
    // ============================================================
    
    async getRecipes(): Promise<RecipeListResponse> {
        try {
            const response: AxiosResponse<RecipeListResponse> = await this.api.get('/recipes');
            return response.data;
        } catch (error) {
            console.error('Error fetching recipes:', error);
            throw error;
        }
    }

    async getSystemRecipes(): Promise<Recipe[]> {
        try {
            const response: AxiosResponse<Recipe[]> = await this.api.get('/recipes/system');
            return response.data;
        } catch (error) {
            console.error('Error fetching system recipes:', error);
            throw error;
        }
    }

    async getUserRecipes(): Promise<Recipe[]> {
        try {
            const response: AxiosResponse<Recipe[]> = await this.api.get('/recipes/user');
            return response.data;
        } catch (error) {
            console.error('Error fetching user recipes:', error);
            throw error;
        }
    }

    async getRecipe(id: string): Promise<Recipe> {
        try {
            const response: AxiosResponse<Recipe> = await this.api.get(`/recipes/${id}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching recipe:', error);
            throw error;
        }
    }

    async createRecipe(data: RecipeCreate): Promise<Recipe> {
        try {
            const response: AxiosResponse<Recipe> = await this.api.post('/recipes', data);
            return response.data;
        } catch (error) {
            console.error('Error creating recipe:', error);
            throw error;
        }
    }

    async updateRecipe(id: string, data: RecipeUpdate): Promise<Recipe> {
        try {
            const response: AxiosResponse<Recipe> = await this.api.put(`/recipes/${id}`, data);
            return response.data;
        } catch (error) {
            console.error('Error updating recipe:', error);
            throw error;
        }
    }

    async deleteRecipe(id: string): Promise<any> {
        try {
            const response: AxiosResponse = await this.api.delete(`/recipes/${id}`);
            return response.data;
        } catch (error) {
            console.error('Error deleting recipe:', error);
            throw error;
        }
    }

    async applyRecipe(id: string): Promise<{ target_values: Record<string, number> }> {
        try {
            const response: AxiosResponse<{ target_values: Record<string, number> }> = await this.api.post(`/recipes/${id}/apply`);
            return response.data;
        } catch (error) {
            console.error('Error applying recipe:', error);
            throw error;
        }
    }

    async copyRecipe(id: string): Promise<{ recipe: Recipe }> {
        try {
            const response: AxiosResponse<{ recipe: Recipe }> = await this.api.post(`/recipes/${id}/copy`);
            return response.data;
        } catch (error) {
            console.error('Error copying recipe:', error);
            throw error;
        }
    }
}

export const apiService = new ApiService();
export default apiService;


