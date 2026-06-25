// frontend/src/store/modules/recipeStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/apiService';

export interface Recipe {
    id: number;
    name: string;
    description?: string | null;
    target_values: Record<string, number>;
    category?: string | null;
    stage?: string | null;
    is_system: boolean;
    user_id?: number;
    created_at: string;
    updated_at?: string;
}

export interface RecipeCreate {
    name: string;
    description?: string | null;
    target_values: Record<string, number>;
    category?: string | null;
    stage?: string | null;
}

export interface RecipeUpdate {
    name?: string;
    description?: string | null;
    target_values?: Record<string, number>;
    category?: string | null;
    stage?: string | null;
}

export interface RecipeListResponse {
    system_recipes: Recipe[];
    user_recipes: Recipe[];
}

export const useRecipeStore = defineStore('recipe', () => {
    // ===== State =====
    const systemRecipes = ref<Recipe[]>([]);
    const userRecipes = ref<Recipe[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // ===== Getters =====
    const allRecipes = computed(() => {
        return [...systemRecipes.value, ...userRecipes.value];
    });

    const getRecipeById = (id: number) => {
        return allRecipes.value.find(r => r.id === id);
    };

    const hasSystemRecipes = computed(() => systemRecipes.value.length > 0);
    const hasUserRecipes = computed(() => userRecipes.value.length > 0);

    // ===== Actions =====

    async function loadAllRecipes(): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            const data = await apiService.get<RecipeListResponse>('/recipes');
            if (data) {
                systemRecipes.value = data.system_recipes || [];
                userRecipes.value = data.user_recipes || [];
                return true;
            }
            return false;
        } catch (err: any) {
            error.value = err.message || 'خطا در بارگذاری رسپی‌ها';
            console.error('Error loading recipes:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    async function createRecipe(data: RecipeCreate): Promise<Recipe | null> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.post<Recipe>('/recipes', data);
            if (result) {
                userRecipes.value.push(result);
                return result;
            }
            return null;
        } catch (err: any) {
            error.value = err.message || 'خطا در ایجاد رسپی';
            console.error('Error creating recipe:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    async function updateRecipe(id: number, data: RecipeUpdate): Promise<Recipe | null> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.put<Recipe>(`/recipes/${id}`, data);
            if (result) {
                const index = userRecipes.value.findIndex(r => r.id === id);
                if (index !== -1) {
                    userRecipes.value[index] = result;
                }
                return result;
            }
            return null;
        } catch (err: any) {
            error.value = err.message || 'خطا در به‌روزرسانی رسپی';
            console.error('Error updating recipe:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    async function deleteRecipe(id: number): Promise<boolean> {
        isLoading.value = true;
        error.value = null;
        try {
            await apiService.delete(`/recipes/${id}`);
            userRecipes.value = userRecipes.value.filter(r => r.id !== id);
            return true;
        } catch (err: any) {
            error.value = err.message || 'خطا در حذف رسپی';
            console.error('Error deleting recipe:', err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    async function applyRecipe(id: number): Promise<Record<string, number> | null> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.post<{ target_values: Record<string, number> }>(`/recipes/${id}/apply`);
            if (result) {
                return result.target_values;
            }
            return null;
        } catch (err: any) {
            error.value = err.message || 'خطا در اعمال رسپی';
            console.error('Error applying recipe:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    async function copySystemRecipe(id: number): Promise<Recipe | null> {
        isLoading.value = true;
        error.value = null;
        try {
            const result = await apiService.post<{ recipe: Recipe }>(`/recipes/${id}/copy`);
            if (result && result.recipe) {
                userRecipes.value.push(result.recipe);
                return result.recipe;
            }
            return null;
        } catch (err: any) {
            error.value = err.message || 'خطا در کپی رسپی';
            console.error('Error copying recipe:', err);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

    function clearError() {
        error.value = null;
    }

    return {
        systemRecipes,
        userRecipes,
        isLoading,
        error,
        allRecipes,
        getRecipeById,
        hasSystemRecipes,
        hasUserRecipes,
        loadAllRecipes,
        createRecipe,
        updateRecipe,
        deleteRecipe,
        applyRecipe,
        copySystemRecipe,
        clearError
    };
});

export default useRecipeStore;