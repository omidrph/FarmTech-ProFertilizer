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

  // ===== Actions =====

  // بارگذاری کودها از بک‌اند
  const loadFertilizers = async (): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const data = await apiService.getFertilizers();
      
      if (data && Array.isArray(data)) {
        fertilizers.value = data.map((item: any) => ({
          id: String(item.id),
          name: item.name,
          pricePerKg: item.price_per_kg || item.pricePerKg || 0,
          elements: item.elements || {},
          isAcid: item.is_acid || false,
          acidType: item.acid_type || null,
          createdAt: item.created_at ? new Date(item.created_at) : new Date(),
          updatedAt: item.updated_at ? new Date(item.updated_at) : new Date()
        }));
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
      const data = {
        name: fertilizerData.name,
        price_per_kg: fertilizerData.pricePerKg || fertilizerData.price_per_kg || 0,
        elements: fertilizerData.elements || {},
        is_acid: fertilizerData.isAcid || false,
        acid_type: fertilizerData.acidType || null
      };
      
      const result = await apiService.createFertilizer(data);
      
      if (result) {
        const newFertilizer: Fertilizer = {
          id: String(result.id),
          name: result.name,
          pricePerKg: result.price_per_kg || result.pricePerKg || 0,
          elements: result.elements || {},
          isAcid: result.is_acid || false,
          acidType: result.acid_type || null,
          createdAt: result.created_at ? new Date(result.created_at) : new Date(),
          updatedAt: result.updated_at ? new Date(result.updated_at) : new Date()
        };
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
  };

  // به‌روزرسانی کود
  const updateFertilizer = async (id: string, data: any): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const result = await apiService.updateFertilizer(id, data);
      
      if (result) {
        const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
        if (index !== -1) {
          fertilizers.value[index] = {
            ...fertilizers.value[index],
            name: result.name || fertilizers.value[index].name,
            pricePerKg: result.price_per_kg || result.pricePerKg || fertilizers.value[index].pricePerKg,
            elements: result.elements || fertilizers.value[index].elements,
            isAcid: result.is_acid !== undefined ? result.is_acid : fertilizers.value[index].isAcid,
            acidType: result.acid_type || fertilizers.value[index].acidType,
            updatedAt: new Date()
          };
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
  };

  // حذف کود
  const deleteFertilizer = async (id: string): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;
    
    try {
      await apiService.deleteFertilizer(id);
      
      const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
      if (index !== -1) {
        fertilizers.value.splice(index, 1);
        const selIndex = selectedFertilizerIds.value.indexOf(id);
        if (selIndex !== -1) {
          selectedFertilizerIds.value.splice(selIndex, 1);
        }
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

  // بارگذاری نمونه (برای زمانی که بک‌اند در دسترس نیست)
  const loadSampleFertilizers = () => {
    const samples: Fertilizer[] = [
      {
        id: 'sample-1',
        name: 'کلسیم نیترات + آمونیوم',
        pricePerKg: 25000,
        elements: { 'N-NO3': 14.5, 'N-NH4': 1.5, 'Ca': 19 } as Partial<Record<ElementName, number>>,
        isAcid: false,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'sample-2',
        name: 'پتاسیم نیترات',
        pricePerKg: 32000,
        elements: { 'N-NO3': 13, 'K': 38 } as Partial<Record<ElementName, number>>,
        isAcid: false,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'sample-3',
        name: 'فسفات پتاسیم',
        pricePerKg: 28000,
        elements: { 'P': 22, 'K': 28 } as Partial<Record<ElementName, number>>,
        isAcid: false,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'sample-4',
        name: 'سولفات منیزیم',
        pricePerKg: 15000,
        elements: { 'S': 13, 'Mg': 10 } as Partial<Record<ElementName, number>>,
        isAcid: false,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];
    fertilizers.value = samples;
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
    
    // Actions
    loadFertilizers,
    addFertilizer,
    updateFertilizer,
    deleteFertilizer,
    toggleSelectFertilizer,
    selectFertilizers,
    clearSelection,
    clearError,
    loadSampleFertilizers
  };
});