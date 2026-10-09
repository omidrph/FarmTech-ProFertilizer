<!-- frontend/src/components/features/FertilizerDBTab.vue -->
<template>
  <div class="space-y-6">
    <!-- ============================================================ -->
    <!-- هدر با توضیحات -->
    <!-- ============================================================ -->
    <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
      <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
        در این بخش می‌توانید کودهای شخصی خود را مدیریت کنید.
        همچنین با کلیک روی دکمه "کپی کودهای سیستمی" می‌توانید کودهای استاندارد را به بخش شخصی خود اضافه کنید.
      </p>
    </div>

    <!-- ============================================================ -->
    <!-- بخش کودهای سیستمی -->
    <!-- ============================================================ -->
    <SystemFertilizersSection
      :system-fertilizers="systemFertilizers"
      :user-fertilizers="userFertilizers"
      :copy-status="copyStatus"
      :is-copying="isCopying"
      @copy-all="handleCopyAllSystemFertilizers"
      @copy-single="handleCopySingleSystemFertilizer"
      @copy-many="handleCopyManySystemFertilizers"
    />

    <!-- ============================================================ -->
    <!-- بخش آمار + جدول + جستجو -->
    <!-- ============================================================ -->
    <FertilizerStatsAndTable
      :user-fertilizers="userFertilizers"
      :system-fertilizers="systemFertilizers"
      :is-loading="isLoading"
      :active-filter="activeFilter"
      @refresh="refreshFertilizers"
      @open-modal="openAddModal"
      @edit-fertilizer="editFertilizer"
      @delete-fertilizer="deleteFertilizer"
      @filter-change="handleFilterChange"
      @clear-table="handleClearTable"
    />

    <!-- ============================================================ -->
    <!-- مودال افزودن/ویرایش کود -->
    <!-- ============================================================ -->
    <FertilizerModal
      :is-open="showModal"
      :is-editing="isEditing"
      :form-data="formData"
      :is-saving="isSaving"
      @close="closeModal"
      @save="saveFertilizer"
    />

    <!-- ============================================================ -->
    <!-- پیام موفقیت/خطا (Toast) -->
    <!-- ============================================================ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="toastMessage"
          class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-xl shadow-2xl flex items-center gap-2"
          :class="toastType === 'success' 
            ? 'bg-success-600 text-white' 
            : 'bg-danger-600 text-white'"
        >
          <svg v-if="toastType === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
          <button 
            @click="toastMessage = null"
            class="text-white/80 hover:text-white transition-colors mr-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';

// ============================================================
// Import کامپوننت‌های داخلی
// ============================================================
import SystemFertilizersSection from './fertilizer-db/SystemFertilizersSection.vue';
import FertilizerStatsAndTable from './fertilizer-db/FertilizerStatsAndTable.vue';
import FertilizerModal from './fertilizer-db/FertilizerModal.vue';

// ============================================================
// Props & Emits
// ============================================================
const props = defineProps<{
  fertilizers: any[];
}>();

const emit = defineEmits<{
  (e: 'update:fertilizers', value: any[]): void;
  (e: 'delete-fertilizer', id: string): void;
}>();

// ============================================================
// Store
// ============================================================
const fertilizerStore = useFertilizerStore();

// ============================================================
// State
// ============================================================
const isLoading = ref(false);
const isSaving = ref(false);
const isCopying = ref(false);
const showModal = ref(false);
const isEditing = ref(false);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');
const activeFilter = ref<string | null>(null);

// Copy Status
const copyStatus = ref({
  hasSystemFertilizers: false,
  hasCopiedSystemFertilizers: false,
  systemCount: 0,
  copiedCount: 0
});

// لیست عناصر برای فرم
const elementsList = [
  'N-NO3', 'N-NH4', 'P', 'K', 'Ca', 'Mg', 'S', 
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Na', 'Cl'
];

// داده‌های فرم
const initialFormData = {
  id: null as string | null,
  name: '',
  brand: '',
  category: '',
  form: '' as '' | 'liquid' | 'powder' | 'crystal' | 'granular',
  concentration: 100,
  price_per_kg: 0,
  elements: {} as Record<string, number>,
  is_acid: false,
  is_base: false,
  acid_type: '',
  ph_level: null as number | null,
  description: '',
  is_system_default: false,
  source_system_id: null as number | null,
  // 🆕 کود مایع: چگالی (g/mL) و واحد قیمت؛ price_per_kg در فرم «به همان واحد انتخاب‌شده» است
  density_g_ml: null as number | null,
  price_unit: 'kg' as 'kg' | 'l'
};

const formData = reactive({ ...initialFormData });

// ============================================================
// Computed
// ============================================================
const userFertilizers = computed(() => {
  return fertilizerStore.userFertilizers;
});

const systemFertilizers = computed(() => {
  return fertilizerStore.systemFertilizers;
});

// ============================================================
// Methods - Toast
// ============================================================
const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

// ============================================================
// Methods - Form
// ============================================================
const resetForm = () => {
  Object.assign(formData, { ...initialFormData, elements: {} });
  isEditing.value = false;
};

const openAddModal = () => {
  resetForm();
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

// قیمت ذخیره‌شده همیشه به‌ازای کیلوگرم است؛ برای مایع با واحد «لیتر» در فرم به‌ازای لیتر نشان می‌دهیم
const displayPrice = (f: any): number => {
  const perKg = Number(f.pricePerKg || f.price_per_kg || 0);
  const density = Number(f.densityGMl || f.density_g_ml || 0);
  if (f.priceUnit === 'l' && density > 0) return Math.round(perKg * density * 100) / 100;
  return perKg;
};

const editFertilizer = (fertilizer: any) => {
  isEditing.value = true;
  Object.assign(formData, {
    id: fertilizer.id,
    name: fertilizer.name || '',
    brand: fertilizer.brand || '',
    category: fertilizer.category || '',
    form: fertilizer.form || '',
    concentration: fertilizer.concentration || 100,
    price_per_kg: displayPrice(fertilizer),
    elements: { ...(fertilizer.elements || {}) },
    is_acid: fertilizer.isAcid || fertilizer.is_acid || false,
    is_base: fertilizer.isBase || fertilizer.is_base || false,
    acid_type: fertilizer.acidType || fertilizer.acid_type || '',
    ph_level: fertilizer.phLevel || fertilizer.ph_level || null,
    description: fertilizer.description || '',
    is_system_default: fertilizer.isSystemDefault || fertilizer.is_system_default || false,
    source_system_id: fertilizer.sourceSystemId || fertilizer.source_system_id || null,
    density_g_ml: fertilizer.densityGMl || fertilizer.density_g_ml || null,
    price_unit: fertilizer.priceUnit === 'l' && (fertilizer.densityGMl || fertilizer.density_g_ml) ? 'l' : 'kg'
  });
  showModal.value = true;
};

const saveFertilizer = async () => {
  if (!formData.name) {
    showToast('لطفاً نام کود را وارد کنید', 'error');
    return;
  }

  if (Number(formData.price_per_kg) < 0) {
    showToast('قیمت نمی‌تواند منفی باشد', 'error');
    return;
  }

  if (formData.concentration < 0 || formData.concentration > 100) {
    showToast('خلوص باید بین 0 تا 100 باشد', 'error');
    return;
  }

  const isLiquid = formData.form === 'liquid';
  if (isLiquid && formData.price_unit === 'l' && !(Number(formData.density_g_ml) > 0)) {
    showToast('برای قیمت هر لیتر، چگالی کود را وارد کنید', 'error');
    return;
  }
  if (formData.is_acid && formData.is_base) {
    showToast('یک ماده همزمان اسید و باز نیست؛ فقط یکی را انتخاب کنید', 'error');
    return;
  }

  isSaving.value = true;

  try {
    const cleanElements: Record<string, number> = {};
    for (const [key, value] of Object.entries(formData.elements)) {
      const numValue = Number(value);
      if (!isNaN(numValue) && numValue > 0) {
        cleanElements[key] = numValue;
      }
    }

    // قیمت همیشه به‌ازای کیلوگرم ذخیره می‌شود: قیمت هر لیتر ÷ چگالی
    const density = isLiquid && Number(formData.density_g_ml) > 0 ? Number(formData.density_g_ml) : null;
    const usePerLiter = isLiquid && formData.price_unit === 'l' && density !== null;
    const pricePerKg = usePerLiter ? Number(formData.price_per_kg) / (density as number) : Number(formData.price_per_kg);

    const payload = {
      name: formData.name,
      brand: formData.brand || undefined,
      category: formData.category || undefined,
      form: formData.form || undefined,
      concentration: formData.concentration,
      pricePerKg,
      elements: cleanElements,
      isAcid: formData.is_acid,
      isBase: formData.is_base,
      acidType: (formData.is_acid || formData.is_base) ? (formData.acid_type || undefined) : undefined,
      phLevel: formData.ph_level || undefined,
      description: formData.description || undefined,
      // کود غیرمایع: چگالی/واحد قیمت پاک می‌شود تا داده‌ی قدیمی باقی نماند
      densityGMl: density,
      priceUnit: isLiquid ? (usePerLiter ? 'l' : 'kg') : null
    } as any;

    let success = false;

    if (isEditing.value && formData.id) {
      success = await fertilizerStore.updateFertilizer(String(formData.id), payload);
      if (success) {
        showToast('کود با موفقیت به‌روزرسانی شد', 'success');
      }
    } else {
      success = await fertilizerStore.addFertilizer(payload);
      if (success) {
        showToast('کود با موفقیت افزوده شد', 'success');
      }
    }

    if (success) {
      closeModal();
      await refreshFertilizers();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در ذخیره‌سازی', 'error');
  } finally {
    isSaving.value = false;
  }
};

// ============================================================
// Methods - Delete (فقط اینجا confirm دارد)
// ============================================================
const deleteFertilizer = async (id: string) => {
  if (!confirm('آیا از حذف این کود اطمینان دارید؟ این عملیات غیرقابل بازگشت است.')) {
    return;
  }

  try {
    const success = await fertilizerStore.deleteFertilizer(id);
    if (success) {
      showToast('کود با موفقیت حذف شد', 'success');
      await refreshFertilizers();
      emit('delete-fertilizer', id);
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در حذف کود', 'error');
  }
};

// ============================================================
// Methods - Clear Table
// ============================================================
const handleClearTable = async () => {
  // حذف همه کودهای شخصی
  const userFerts = userFertilizers.value;
  if (userFerts.length === 0) return;
  
  let deletedCount = 0;
  let errorCount = 0;
  
  for (const fert of userFerts) {
    try {
      const success = await fertilizerStore.deleteFertilizer(fert.id);
      if (success) {
        deletedCount++;
      } else {
        errorCount++;
      }
    } catch {
      errorCount++;
    }
  }
  
  if (errorCount === 0) {
    showToast(`${deletedCount} کود با موفقیت حذف شدند`, 'success');
  } else {
    showToast(`${deletedCount} کود حذف شدند و ${errorCount} مورد خطا داشت`, 'error');
  }
  
  await refreshFertilizers();
  await loadSystemFertilizers();
};

// ============================================================
// Methods - System Fertilizers
// ============================================================
const loadSystemFertilizers = async () => {
  await fertilizerStore.loadSystemFertilizers();
  copyStatus.value = await fertilizerStore.checkSystemCopyStatus();
};

const handleCopyAllSystemFertilizers = async () => {
  if (!confirm('آیا می‌خواهید همه کودهای سیستمی را به بخش شخصی خود کپی کنید؟')) {
    return;
  }

  isCopying.value = true;
  try {
    const result = await fertilizerStore.copyAllSystemFertilizers();
    if (result.success) {
      showToast(result.message || 'کودهای سیستمی با موفقیت کپی شدند', 'success');
      await refreshFertilizers();
      await loadSystemFertilizers();
    } else {
      showToast(result.message || 'خطا در کپی کودهای سیستمی', 'error');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در کپی کودهای سیستمی', 'error');
  } finally {
    isCopying.value = false;
  }
};

// کپی گروهی (فقط مواردی که هنوز کپی نشده‌اند؛ به ترتیب، با همان endpoint کپی تکی)
const handleCopyManySystemFertilizers = async (ids: string[]) => {
  if (!ids.length) return;
  isCopying.value = true;
  let ok = 0;
  try {
    for (const id of ids) {
      const r = await fertilizerStore.copySystemFertilizer(id);
      if (r) ok++;
    }
    showToast(`${ok.toLocaleString('fa-IR')} کود به بخش شخصی شما اضافه شد`, ok ? 'success' : 'error');
    await refreshFertilizers();
    await loadSystemFertilizers();
  } catch (error: any) {
    showToast(error.message || 'خطا در کپی کودها', 'error');
  } finally {
    isCopying.value = false;
  }
};

const handleCopySingleSystemFertilizer = async (systemFertilizerId: string) => {
  try {
    const result = await fertilizerStore.copySystemFertilizer(systemFertilizerId);
    if (result) {
      showToast(`کود "${result.name}" با موفقیت کپی شد`, 'success');
      await refreshFertilizers();
      await loadSystemFertilizers();
    } else {
      showToast('خطا در کپی کود', 'error');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در کپی کود', 'error');
  }
};

// ============================================================
// Methods - Filter
// ============================================================
const handleFilterChange = (filter: string | null) => {
  activeFilter.value = filter;
};

// ============================================================
// Methods - General
// ============================================================
const refreshFertilizers = async () => {
  isLoading.value = true;
  try {
    await fertilizerStore.loadFertilizers(true);
    emit('update:fertilizers', fertilizerStore.fertilizers);
  } catch (error) {
    console.error('Error refreshing fertilizers:', error);
  } finally {
    isLoading.value = false;
  }
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(async () => {
  await refreshFertilizers();
  await loadSystemFertilizers();
});

// Watch for changes in store fertilizers to emit
watch(() => fertilizerStore.fertilizers, (newVal) => {
  emit('update:fertilizers', newVal);
}, { deep: true });
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}
</style>
