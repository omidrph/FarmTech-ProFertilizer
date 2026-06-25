// frontend/src/store/index.ts
import { createPinia } from 'pinia';
import { useAppStore } from './modules/appStore';
import { useCalcStore } from './modules/calcStore';
import { useEducationStore } from './modules/educationStore';
import { useFertilizerStore } from './modules/fertilizerStore';
import { useReportStore } from './modules/reportStore';
import { useTargetStore } from './modules/targetStore';
import { useWaterStore } from './modules/waterStore';
import { useRecipeStore } from './modules/recipeStore';

const pinia = createPinia();

// Export all stores for easy access
export {
    useAppStore,
    useCalcStore,
    useEducationStore,
    useFertilizerStore,
    useReportStore,
    useTargetStore,
    useWaterStore,
    useRecipeStore
};

export default pinia;