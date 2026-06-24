// frontend/src/store/modules/fertilizerStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Fertilizer, ElementName } from '@/types';
import { apiService } from '@/services/apiService';

export const useFertilizerStore = defineStore('fertilizer', () => {
    // ===== State =====
    const fertilizers = ref<Fertilizer[]>([]);
    const selectedFertilizerIds = ref<string[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // ===== Getters =====
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

    // ===== Helper: تبدیل داده بک‌اند به فرانت =====
    const mapBackendToFertilizer = (item: any): Fertilizer => {
        return {
            id: String(item.id),
            name: item.name,
            pricePerKg: item.price_per_kg ?? item.pricePerKg ?? 0,
            elements: item.elements || {},
            isAcid: item.is_acid ?? item.isAcid ?? false,
            acidType: item.acid_type ?? item.acidType ?? null,
            // 🆕 فیلدهای جدید
            isSystemDefault: item.is_system_default ?? item.isSystemDefault ?? false,
            brand: item.brand ?? '',
            category: item.category ?? '',
            form: item.form ?? '',
            solubility: item.solubility ?? '',
            phLevel: item.ph_level ?? item.phLevel ?? '',
            description: item.description ?? '',
            applicationMethod: item.application_method ?? item.applicationMethod ?? '',
            packaging: item.packaging ?? '',
            registrationCode: item.registration_code ?? item.registrationCode ?? '',
            npkRatio: item.npk_ratio ?? item.npkRatio ?? '',
            organicMatter: item.organic_matter ?? item.organicMatter ?? 0,
            chelatingAgent: item.chelating_agent ?? item.chelatingAgent ?? '',
            createdAt: item.created_at ? new Date(item.created_at) : new Date(),
            updatedAt: item.updated_at ? new Date(item.updated_at) : new Date()
        };
    };

    // ===== Helper: تبدیل داده فرانت به بک‌اند =====
    const mapFertilizerToBackend = (fertilizerData: any): any => {
        return {
            name: fertilizerData.name,
            price_per_kg: fertilizerData.pricePerKg ?? fertilizerData.price_per_kg ?? 0,
            elements: fertilizerData.elements || {},
            is_acid: fertilizerData.isAcid ?? fertilizerData.is_acid ?? false,
            acid_type: fertilizerData.acidType ?? fertilizerData.acid_type ?? null,
            // 🆕 فیلدهای جدید
            brand: fertilizerData.brand || null,
            category: fertilizerData.category || null,
            form: fertilizerData.form || null,
            solubility: fertilizerData.solubility || null,
            ph_level: fertilizerData.phLevel || fertilizerData.ph_level || null,
            description: fertilizerData.description || null,
            application_method: fertilizerData.applicationMethod || fertilizerData.application_method || null,
            packaging: fertilizerData.packaging || null,
            registration_code: fertilizerData.registrationCode || fertilizerData.registration_code || null,
            npk_ratio: fertilizerData.npkRatio || fertilizerData.npk_ratio || null,
            organic_matter: fertilizerData.organicMatter || fertilizerData.organic_matter || null,
            chelating_agent: fertilizerData.chelatingAgent || fertilizerData.chelating_agent || null
        };
    };

    // ===== Actions =====
    // بارگذاری کودها از بک‌اند
    const loadFertilizers = async (): Promise<boolean> => {
        isLoading.value = true;
        error.value = null;
        try {
            const data = await apiService.getFertilizers();
            if (data && Array.isArray(data)) {
                fertilizers.value = data.map(mapBackendToFertilizer);
                console.log(`✅ ${fertilizers.value.length} کود از بک‌اند بارگذاری شد`);
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
    };

    // افزودن کود جدید به بک‌اند
    const addFertilizer = async (fertilizerData: any): Promise<boolean> => {
        isLoading.value = true;
        error.value = null;
        try {
            const payload = mapFertilizerToBackend(fertilizerData);
            const result = await apiService.createFertilizer(payload);
            if (result) {
                const newFertilizer = mapBackendToFertilizer(result);
                fertilizers.value.push(newFertilizer);
                console.log(`✅ کود "${newFertilizer.name}" با موفقیت افزوده شد`);
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
    };

    // به‌روزرسانی کود
    const updateFertilizer = async (id: string, data: any): Promise<boolean> => {
        isLoading.value = true;
        error.value = null;
        try {
            const payload = mapFertilizerToBackend(data);
            const result = await apiService.updateFertilizer(id, payload);
            if (result) {
                const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
                const updatedFertilizer = mapBackendToFertilizer(result);
                
                if (index !== -1) {
                    fertilizers.value[index] = updatedFertilizer;
                } else {
                    // اگر کود سیستمی بود و کپی ساخته شد، به لیست اضافه کن
                    fertilizers.value.push(updatedFertilizer);
                }
                
                console.log(`✅ کود "${updatedFertilizer.name}" با موفقیت به‌روزرسانی شد`);
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
    };

    // حذف کود
    const deleteFertilizer = async (id: string): Promise<boolean> => {
        isLoading.value = true;
        error.value = null;
        try {
            await apiService.deleteFertilizer(id);
            const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
            if (index !== -1) {
                const name = fertilizers.value[index].name;
                fertilizers.value.splice(index, 1);
                const selIndex = selectedFertilizerIds.value.indexOf(id);
                if (selIndex !== -1) {
                    selectedFertilizerIds.value.splice(selIndex, 1);
                }
                console.log(`✅ کود "${name}" با موفقیت حذف شد`);
            }
            return true;
        } catch (err: any) {
            error.value = err.message || 'خطا در حذف کود';
            console.error('Error deleting fertilizer:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    // انتخاب/عدم انتخاب کود
    const toggleSelectFertilizer = (id: string) => {
        const index = selectedFertilizerIds.value.indexOf(id);
        if (index === -1) {
            selectedFertilizerIds.value.push(id);
        } else {
            selectedFertilizerIds.value.splice(index, 1);
        }
    };

    const selectFertilizers = (ids: string[]) => {
        selectedFertilizerIds.value = ids;
    };

    const clearSelection = () => {
        selectedFertilizerIds.value = [];
    };

    const clearError = () => {
        error.value = null;
    };

    return {
        // State
        fertilizers,
        selectedFertilizerIds,
        isLoading,
        error,
        // Getters
        fertilizerOptions,
        selectedFertilizers,
        getFertilizerById,
        hasFertilizers,
        // Actions
        loadFertilizers,
        addFertilizer,
        updateFertilizer,
        deleteFertilizer,
        toggleSelectFertilizer,
        selectFertilizers,
        clearSelection,
        clearError
    };
});

// Export default برای اطمینان از اینکه ماژول به درستی صادر می‌شود
export default useFertilizerStore;