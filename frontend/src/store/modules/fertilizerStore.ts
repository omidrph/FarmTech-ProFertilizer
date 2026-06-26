// frontend/src/store/modules/fertilizerStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Fertilizer, ElementName, FertilizerCreate, FertilizerUpdate } from '@/types';
import { apiService } from '@/services/apiService';

export const useFertilizerStore = defineStore('fertilizer', () => {
    // ===== State =====
    const fertilizers = ref<Fertilizer[]>([]);
    const systemFertilizers = ref<Fertilizer[]>([]);
    const selectedFertilizerIds = ref<string[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // ===== Getters =====
    const userFertilizers = computed(() => {
        return fertilizers.value.filter(f => !f.isSystemDefault);
    });

    const fertilizerOptions = computed(() => {
        return fertilizers.value.map((f: Fertilizer) => ({
            label: f.name,
            value: f.id
        }));
    });

    const selectedFertilizers = computed(() => {
        return fertilizers.value.filter((f: Fertilizer) => selectedFertilizerIds.value.includes(f.id));
    });

    const getFertilizerById = (id: string) => {
        return fertilizers.value.find((f: Fertilizer) => f.id === id);
    };

    const hasFertilizers = computed(() => fertilizers.value.length > 0);
    const hasSystemFertilizers = computed(() => systemFertilizers.value.length > 0);
    const hasUserFertilizers = computed(() => userFertilizers.value.length > 0);

    // ===== Helper: تبدیل داده بک‌اند به فرانت =====
    const mapBackendToFertilizer = (item: any): Fertilizer => {
        return {
            id: String(item.id),
            user_id: item.user_id ?? null,
            name: item.name,
            
            // فیلدهای اطلاعاتی
            brand: item.brand ?? '',
            category: item.category ?? '',
            form: item.form ?? undefined,
            
            // فیلدهای محاسباتی
            concentration: item.concentration ?? 100.0,
            elements: item.elements || {},
            pricePerKg: item.price_per_kg ?? item.pricePerKg ?? 0,
            
            // فیلدهای اسید و pH
            isAcid: item.is_acid ?? item.isAcid ?? false,
            acidType: item.acid_type ?? item.acidType ?? undefined,
            phLevel: item.ph_level ?? item.phLevel ?? undefined,
            
            // توضیحات
            description: item.description ?? '',
            
            // فیلدهای سیستمی
            isSystemDefault: item.is_system_default ?? item.isSystemDefault ?? false,
            sourceSystemId: item.source_system_id ?? item.sourceSystemId ?? undefined,
            
            // تاریخ‌ها
            createdAt: item.created_at ? new Date(item.created_at) : new Date(),
            updatedAt: item.updated_at ? new Date(item.updated_at) : new Date()
        };
    };

    // ===== Helper: تبدیل داده فرانت به بک‌اند =====
    const mapFertilizerToBackend = (fertilizerData: FertilizerCreate | FertilizerUpdate): any => {
        const result: any = {};
        
        if ('name' in fertilizerData && fertilizerData.name !== undefined) {
            result.name = fertilizerData.name;
        }
        if ('brand' in fertilizerData && fertilizerData.brand !== undefined) {
            result.brand = fertilizerData.brand || null;
        }
        if ('category' in fertilizerData && fertilizerData.category !== undefined) {
            result.category = fertilizerData.category || null;
        }
        if ('form' in fertilizerData && fertilizerData.form !== undefined) {
            result.form = fertilizerData.form || null;
        }
        if ('concentration' in fertilizerData && fertilizerData.concentration !== undefined) {
            result.concentration = fertilizerData.concentration;
        }
        if ('elements' in fertilizerData && fertilizerData.elements !== undefined) {
            result.elements = fertilizerData.elements || {};
        }
        if ('pricePerKg' in fertilizerData && fertilizerData.pricePerKg !== undefined) {
            result.price_per_kg = fertilizerData.pricePerKg;
        }
        if ('isAcid' in fertilizerData && fertilizerData.isAcid !== undefined) {
            result.is_acid = fertilizerData.isAcid;
        }
        if ('acidType' in fertilizerData && fertilizerData.acidType !== undefined) {
            result.acid_type = fertilizerData.acidType || null;
        }
        if ('phLevel' in fertilizerData && fertilizerData.phLevel !== undefined) {
            result.ph_level = fertilizerData.phLevel || null;
        }
        if ('description' in fertilizerData && fertilizerData.description !== undefined) {
            result.description = fertilizerData.description || null;
        }
        
        return result;
    };

    // ============================================================
    // 🆕 APIهای مربوط به کودهای سیستمی
    // ============================================================

    /**
     * بارگذاری کودهای سیستمی
     */
    async function loadSystemFertilizers(): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            const data = await apiService.get('/fertilizers/system');
            if (data && Array.isArray(data)) {
                systemFertilizers.value = data.map(mapBackendToFertilizer);
                return true;
            }
            return false;
        } catch (err: any) {
            error.value = err.message || 'خطا در بارگذاری کودهای سیستمی';
            console.error('Error loading system fertilizers:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * کپی همه کودهای سیستمی به بخش شخصی کاربر
     */
    async function copyAllSystemFertilizers(): Promise<{ success: boolean; stats?: any; message?: string }> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.post('/fertilizers/system/copy-all');
            if (result && result.success) {
                // بارگذاری مجدد کودهای شخصی
                await loadFertilizers();
                // بارگذاری مجدد کودهای سیستمی برای به‌روزرسانی وضعیت
                await loadSystemFertilizers();
                return { success: true, stats: result.stats, message: result.message };
            }
            return { success: false, message: 'خطا در کپی کودهای سیستمی' };
        } catch (err: any) {
            const errorMessage = err.message || 'خطا در کپی کودهای سیستمی';
            error.value = errorMessage;
            console.error('Error copying system fertilizers:', err);
            return { success: false, message: errorMessage };
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * کپی یک کود سیستمی خاص
     */
    async function copySystemFertilizer(systemFertilizerId: string): Promise<Fertilizer | null> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.post(`/fertilizers/system/${systemFertilizerId}/copy`);
            if (result && result.success && result.fertilizer) {
                const newFertilizer = mapBackendToFertilizer(result.fertilizer);
                fertilizers.value.push(newFertilizer);
                // به‌روزرسانی لیست کودهای سیستمی
                await loadSystemFertilizers();
                return newFertilizer;
            }
            return null;
        } catch (err: any) {
            error.value = err.message || 'خطا در کپی کود سیستمی';
            console.error('Error copying system fertilizer:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * بررسی وضعیت کپی کودهای سیستمی
     */
    async function checkSystemCopyStatus(): Promise<{
        hasSystemFertilizers: boolean;
        hasCopiedSystemFertilizers: boolean;
        systemCount: number;
        copiedCount: number;
    }> {
        try {
            const result = await apiService.get('/fertilizers/check-system-copy-status');
            return result;
        } catch (err) {
            console.error('Error checking system copy status:', err);
            return {
                hasSystemFertilizers: false,
                hasCopiedSystemFertilizers: false,
                systemCount: 0,
                copiedCount: 0
            };
        }
    }

    // ============================================================
    // APIهای مربوط به کودهای شخصی
    // ============================================================

    /**
     * بارگذاری کودهای شخصی کاربر (همراه با کودهای سیستمی در صورت نیاز)
     */
    async function loadFertilizers(includeSystem: boolean = true): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            const data = await apiService.get(`/fertilizers?include_system=${includeSystem}`);
            if (data && Array.isArray(data)) {
                fertilizers.value = data.map(mapBackendToFertilizer);
                // استخراج کودهای سیستمی از لیست کل
                systemFertilizers.value = fertilizers.value.filter(f => f.isSystemDefault);
                return true;
            }
            return false;
        } catch (err: any) {
            error.value = err.message || 'خطا در بارگذاری کودها';
            console.error('Error loading fertilizers:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * افزودن کود شخصی جدید
     */
    async function addFertilizer(fertilizerData: FertilizerCreate): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            const payload = mapFertilizerToBackend(fertilizerData);
            const result = await apiService.createFertilizer(payload);
            if (result) {
                const newFertilizer = mapBackendToFertilizer(result);
                fertilizers.value.push(newFertilizer);
                return true;
            }
            return false;
        } catch (err: any) {
            error.value = err.message || 'خطا در افزودن کود';
            console.error('Error adding fertilizer:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * به‌روزرسانی کود شخصی
     */
    async function updateFertilizer(id: string, data: FertilizerUpdate): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            const payload = mapFertilizerToBackend(data);
            const result = await apiService.updateFertilizer(id, payload);
            if (result) {
                const updatedFertilizer = mapBackendToFertilizer(result);
                const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
                if (index !== -1) {
                    fertilizers.value[index] = updatedFertilizer;
                }
                return true;
            }
            return false;
        } catch (err: any) {
            error.value = err.message || 'خطا در به‌روزرسانی کود';
            console.error('Error updating fertilizer:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    /**
     * حذف کود شخصی
     */
    async function deleteFertilizer(id: string): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            await apiService.deleteFertilizer(id);
            const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
            if (index !== -1) {
                fertilizers.value.splice(index, 1);
            }
            const selIndex = selectedFertilizerIds.value.indexOf(id);
            if (selIndex !== -1) {
                selectedFertilizerIds.value.splice(selIndex, 1);
            }
            return true;
        } catch (err: any) {
            error.value = err.message || 'خطا در حذف کود';
            console.error('Error deleting fertilizer:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    // ============================================================
    // توابع کمکی
    // ============================================================

    function toggleSelectFertilizer(id: string) {
        const index = selectedFertilizerIds.value.indexOf(id);
        if (index === -1) {
            selectedFertilizerIds.value.push(id);
        } else {
            selectedFertilizerIds.value.splice(index, 1);
        }
    }

    function selectFertilizers(ids: string[]) {
        selectedFertilizerIds.value = ids;
    }

    function clearSelection() {
        selectedFertilizerIds.value = [];
    }

    function clearError() {
        error.value = null;
    }

    return {
        // State
        fertilizers,
        systemFertilizers,
        selectedFertilizerIds,
        isLoading,
        error,
        
        // Getters
        userFertilizers,
        fertilizerOptions,
        selectedFertilizers,
        getFertilizerById,
        hasFertilizers,
        hasSystemFertilizers,
        hasUserFertilizers,
        
        // Actions - System
        loadSystemFertilizers,
        copyAllSystemFertilizers,
        copySystemFertilizer,
        checkSystemCopyStatus,
        
        // Actions - User
        loadFertilizers,
        addFertilizer,
        updateFertilizer,
        deleteFertilizer,
        
        // Actions - Selection
        toggleSelectFertilizer,
        selectFertilizers,
        clearSelection,
        clearError
    };
});

export default useFertilizerStore;