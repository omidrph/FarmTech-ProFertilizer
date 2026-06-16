// frontend/src/store/modules/fertilizerStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Fertilizer } from '@/types';
import { generateId } from '@/utils/helpers';

export const useFertilizerStore = defineStore('fertilizer', () => {
  // ===== State =====
  const fertilizers = ref<Fertilizer[]>([]);
  const selectedFertilizerIds = ref<string[]>([]);

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
  function addFertilizer(fertilizer: Omit<Fertilizer, 'id' | 'createdAt' | 'updatedAt'>) {
    const newFertilizer: Fertilizer = {
      ...fertilizer,
      id: generateId(),
      createdAt: new Date(),
      updatedAt: new Date()
    };
    fertilizers.value.push(newFertilizer);
    return newFertilizer;
  }

  function updateFertilizer(id: string, data: Partial<Omit<Fertilizer, 'id' | 'createdAt' | 'updatedAt'>>) {
    const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
    if (index !== -1) {
      fertilizers.value[index] = {
        ...fertilizers.value[index],
        ...data,
        updatedAt: new Date()
      };
      return true;
    }
    return false;
  }

  function deleteFertilizer(id: string) {
    const index = fertilizers.value.findIndex((f: Fertilizer) => f.id === id);
    if (index !== -1) {
      fertilizers.value.splice(index, 1);
      const selIndex = selectedFertilizerIds.value.indexOf(id);
      if (selIndex !== -1) {
        selectedFertilizerIds.value.splice(selIndex, 1);
      }
      return true;
    }
    return false;
  }

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

  // ===== Sample Data =====
  function loadSampleFertilizers() {
    const sampleFertilizers: Omit<Fertilizer, 'id' | 'createdAt' | 'updatedAt'>[] = [
      {
        name: 'کلسیم نیترات + آمونیوم',
        pricePerKg: 25000,
        elements: {
          'N-NO3': 14.5,
          'N-NH4': 1.5,
          'Ca': 19
        }
      },
      {
        name: 'پتاسیم نیترات',
        pricePerKg: 32000,
        elements: {
          'N-NO3': 13,
          'K': 38
        }
      },
      {
        name: 'فسفات پتاسیم',
        pricePerKg: 28000,
        elements: {
          'P': 22,
          'K': 28
        }
      },
      {
        name: 'سولفات منیزیم',
        pricePerKg: 15000,
        elements: {
          'S': 13,
          'Mg': 10
        }
      }
    ];

    sampleFertilizers.forEach((f: Omit<Fertilizer, 'id' | 'createdAt' | 'updatedAt'>) => addFertilizer(f));
  }

  return {
    // State
    fertilizers,
    selectedFertilizerIds,
    
    // Getters
    fertilizerOptions,
    selectedFertilizers,
    getFertilizerById,
    
    // Actions
    addFertilizer,
    updateFertilizer,
    deleteFertilizer,
    toggleSelectFertilizer,
    selectFertilizers,
    clearSelection,
    loadSampleFertilizers
  };
});