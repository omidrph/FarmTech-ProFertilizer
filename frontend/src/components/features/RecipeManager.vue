<!-- frontend/src/components/features/RecipeManager.vue -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- تب‌ها -->
    <div class="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50/60 dark:bg-gray-900/30 overflow-x-auto scrollbar-hide">
      <button v-for="tab in tabs" :key="tab.id" type="button" @click="activeTab = tab.id"
        class="flex items-center gap-2 px-4 sm:px-5 py-3 text-sm font-medium border-b-2 whitespace-nowrap transition-colors"
        :class="activeTab === tab.id
          ? 'border-primary-500 text-primary-600 dark:text-primary-400 bg-white dark:bg-gray-800'
          : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'">
        {{ tab.label }}
        <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 tabular-nums">
          {{ (tab.id === 'standard' ? systemRecipes.length : userRecipes.length).toLocaleString('fa-IR') }}
        </span>
      </button>
    </div>

    <!-- ===== رسپی‌های استاندارد ===== -->
    <div v-if="activeTab === 'standard'" class="p-4 sm:p-5 space-y-5">
      <div v-if="isLoading" class="flex justify-center items-center gap-2 py-8 text-sm text-gray-500 dark:text-gray-400">
        <div class="animate-spin w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full"></div>
        در حال بارگذاری...
      </div>
      <p v-else-if="systemRecipes.length === 0" class="text-center py-10 text-sm text-gray-500 dark:text-gray-400">رسپی استانداردی موجود نیست.</p>

      <template v-else>
        <div v-for="group in groupedSystem" :key="group.title">
          <p class="flex items-center gap-2 text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2.5">
            <span class="h-px flex-1 bg-gray-200 dark:bg-gray-700"></span>{{ group.title }}<span class="h-px flex-1 bg-gray-200 dark:bg-gray-700"></span>
          </p>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            <div v-for="recipe in group.items" :key="recipe.id"
              class="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-3.5 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-sm transition-all">
              <div class="flex items-start justify-between gap-2">
                <h4 class="text-sm font-semibold text-gray-900 dark:text-white leading-6">{{ recipe.name }}</h4>
                <span v-if="recipe.stage" class="flex-shrink-0 text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300">{{ recipe.stage }}</span>
              </div>
              <p v-if="recipe.description" class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400 line-clamp-3">{{ recipe.description }}</p>
              <div class="flex flex-wrap gap-1 mt-2.5">
                <span v-for="(value, element) in getTopElements(recipe.target_values, 5)" :key="element"
                  class="text-[11px] px-1.5 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 tabular-nums" dir="ltr">
                  {{ element }} {{ Number(value).toFixed(1) }}
                </span>
                <span v-if="elementCount(recipe) > 5" class="text-[11px] px-1.5 py-0.5 text-gray-400">+{{ (elementCount(recipe) - 5).toLocaleString('fa-IR') }}</span>
              </div>
              <div class="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 mt-auto">
                <button type="button" @click="applyRecipe(recipe.id)"
                  class="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-xs font-semibold transition-colors">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" /></svg>
                  اعمال در جدول
                </button>
                <button type="button" @click="copyRecipe(recipe.id)" title="ذخیره در رسپی‌های شخصی"
                  class="px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 text-xs transition-colors">
                  ذخیره در شخصی
                </button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- ===== رسپی‌های شخصی ===== -->
    <div v-else class="p-4 sm:p-5 space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <p class="text-sm text-gray-600 dark:text-gray-300">
          {{ userRecipes.length.toLocaleString('fa-IR') }} از {{ PERSONAL_RECIPE_LIMIT.toLocaleString('fa-IR') }} رسپی
        </p>
        <button type="button" @click="openSaveModal" :disabled="!hasTableValues"
          class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-primary-600 hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs sm:text-sm font-semibold transition-colors whitespace-nowrap">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
          افزودن از جدول
        </button>
      </div>

      <div v-if="userRecipes.length === 0" class="text-center py-10 rounded-xl border border-dashed border-gray-300 dark:border-gray-600">
        <p class="text-sm text-gray-500 dark:text-gray-400">هنوز رسپی شخصی ندارید.</p>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">مقادیر را در جدول عناصر هدف وارد کنید و «افزودن به رسپی شخصی» را بزنید.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        <div v-for="recipe in userRecipes" :key="recipe.id"
          class="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-3.5 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-sm transition-all">
          <div class="flex items-start justify-between gap-2">
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white leading-6">{{ recipe.name }}</h4>
            <div class="flex flex-shrink-0 gap-1">
              <span v-if="recipe.category" class="text-[10px] px-2 py-0.5 rounded-full bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300">{{ recipe.category }}</span>
              <span v-if="recipe.stage" class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300">{{ recipe.stage }}</span>
            </div>
          </div>
          <p v-if="recipe.description" class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400 line-clamp-3">{{ recipe.description }}</p>
          <div class="flex flex-wrap gap-1 mt-2.5">
            <span v-for="(value, element) in getTopElements(recipe.target_values, 5)" :key="element"
              class="text-[11px] px-1.5 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 tabular-nums" dir="ltr">
              {{ element }} {{ Number(value).toFixed(1) }}
            </span>
            <span v-if="elementCount(recipe) > 5" class="text-[11px] px-1.5 py-0.5 text-gray-400">+{{ (elementCount(recipe) - 5).toLocaleString('fa-IR') }}</span>
          </div>
          <div class="flex flex-wrap items-center gap-1.5 mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 mt-auto">
            <button type="button" @click="applyRecipe(recipe.id)"
              class="flex-1 min-w-[5rem] inline-flex items-center justify-center gap-1 px-3 py-1.5 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-xs font-semibold transition-colors">اعمال</button>
            <button type="button" @click="updateFromTable(recipe)" :disabled="!hasTableValues" title="جایگزینی مقادیر رسپی با مقادیر فعلی جدول"
              class="px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-40 text-xs transition-colors">به‌روزرسانی با جدول</button>
            <button type="button" @click="openEditModal(recipe)" title="ویرایش نام و توضیحات"
              class="p-1.5 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
            </button>
            <button type="button" @click="deleteRecipe(recipe.id)" title="حذف"
              class="p-1.5 rounded-lg border border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-300 hover:text-danger-600 hover:border-danger-300 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- مودال کوچک: فقط نام و توضیحات (مقادیر از جدول گرفته می‌شود) -->
    <AppModal :open="showModal" size="sm" :title="isEditing ? 'ویرایش رسپی' : 'افزودن به رسپی شخصی'" @close="closeModal">
      <div class="space-y-3">
        <p v-if="!isEditing" class="text-xs text-gray-500 dark:text-gray-400">
          مقادیر فعلی جدول ({{ tableCount.toLocaleString('fa-IR') }} عنصر) ذخیره می‌شود.
        </p>
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نام رسپی <span class="text-danger-500">*</span></label>
          <input type="text" v-model="formData.name" :class="inputCls" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">محصول</label>
            <input type="text" v-model="formData.category" :class="inputCls" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">مرحلهٔ رشد</label>
            <input type="text" v-model="formData.stage" :class="inputCls" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">توضیحات</label>
          <textarea v-model="formData.description" rows="3" :class="inputCls"></textarea>
        </div>
      </div>
      <template #footer>
        <div class="app-modal-actions">
          <button type="button" @click="closeModal" class="app-modal-btn app-modal-btn-secondary">انصراف</button>
          <button type="button" @click="saveRecipe" :disabled="isSaving || !formData.name.trim()" class="app-modal-btn app-modal-btn-primary">
            {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره' : 'افزودن') }}
          </button>
        </div>
      </template>
    </AppModal>

    <!-- Toast -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="toastMessage" class="fixed bottom-20 sm:bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 px-4 py-2.5 rounded-xl shadow-lg text-sm text-white"
          :class="toastType === 'success' ? 'bg-success-600' : 'bg-danger-600'">
          {{ toastMessage }}
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import AppModal from '@/components/common/AppModal.vue';
import { ref, reactive, onMounted, computed } from 'vue';
import { useRecipeStore } from '@/store/modules/recipeStore';
import { useTargetStore } from '@/store/modules/targetStore';

const emit = defineEmits<{ (e: 'recipe-applied'): void }>();

const recipeStore = useRecipeStore();
const targetStore = useTargetStore();

const systemRecipes = computed(() => recipeStore.systemRecipes);
const userRecipes = computed(() => recipeStore.userRecipes);
const isLoading = computed(() => recipeStore.isLoading);
const PERSONAL_RECIPE_LIMIT = 35;

const ALL_ELEMENTS = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Si'];

const inputCls = 'w-full px-3 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all';

const activeTab = ref<'standard' | 'personal'>('standard');
const tabs = [
  { id: 'standard' as const, label: 'رسپی‌های استاندارد' },
  { id: 'personal' as const, label: 'رسپی‌های شخصی' },
];

const showModal = ref(false);
const isEditing = ref(false);
const isSaving = ref(false);
const editingId = ref<number | null>(null);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

const formData = reactive({ name: '', description: '', category: '', stage: '' });

// مقادیر فعلی جدول عناصر هدف
const tableValues = computed<Record<string, number>>(() => {
  const out: Record<string, number> = {};
  for (const el of ALL_ELEMENTS) {
    const v = Number((targetStore.targetElements as any)[el]) || 0;
    if (v > 0) out[el] = v;
  }
  return out;
});
const tableCount = computed(() => Object.keys(tableValues.value).length);
const hasTableValues = computed(() => tableCount.value > 0);

const groupedSystem = computed(() => {
  const map = new Map<string, any[]>();
  for (const r of systemRecipes.value) {
    const key = r.category || 'سایر';
    if (!map.has(key)) map.set(key, []);
    map.get(key)!.push(r);
  }
  return Array.from(map, ([title, items]) => ({ title, items }));
});

const getTopElements = (targetValues: Record<string, number>, count: number) =>
  Object.fromEntries(
    Object.entries(targetValues || {}).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]).slice(0, count)
  );
const elementCount = (r: any) => Object.values(r.target_values || {}).filter((v: any) => v > 0).length;

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => { toastMessage.value = null; }, 3000);
};

const resetForm = () => {
  formData.name = '';
  formData.description = '';
  formData.category = '';
  formData.stage = '';
  isEditing.value = false;
  editingId.value = null;
};

// از بیرون (دکمهٔ «افزودن به رسپی شخصی» در جدول عناصر هدف) فراخوانی می‌شود
const openSaveModal = () => {
  if (!hasTableValues.value) {
    showToast('ابتدا مقادیر عناصر را در جدول وارد کنید', 'error');
    return;
  }
  if (userRecipes.value.length >= PERSONAL_RECIPE_LIMIT) {
    showToast('ظرفیت رسپی‌های شخصی تکمیل شده است.', 'error');
    return;
  }
  resetForm();
  showModal.value = true;
};

const openEditModal = (recipe: any) => {
  resetForm();
  isEditing.value = true;
  editingId.value = recipe.id;
  formData.name = recipe.name;
  formData.description = recipe.description || '';
  formData.category = recipe.category || '';
  formData.stage = recipe.stage || '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const saveRecipe = async () => {
  if (!formData.name.trim()) return;
  isSaving.value = true;
  try {
    const base = {
      name: formData.name.trim(),
      description: formData.description || null,
      category: formData.category || null,
      stage: formData.stage || null,
    };
    let result = null;
    if (isEditing.value && editingId.value !== null) {
      result = await recipeStore.updateRecipe(editingId.value, base as any);
      if (result) showToast('رسپی به‌روزرسانی شد');
    } else {
      result = await recipeStore.createRecipe({ ...base, target_values: { ...tableValues.value } } as any);
      if (result) showToast('رسپی به رسپی‌های شخصی اضافه شد');
    }
    if (result) {
      closeModal();
      await recipeStore.loadAllRecipes();
      if (!isEditing.value) activeTab.value = 'personal';
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در ذخیره رسپی', 'error');
  } finally {
    isSaving.value = false;
  }
};

const updateFromTable = async (recipe: any) => {
  if (!hasTableValues.value) return;
  if (!confirm(`مقادیر رسپی «${recipe.name}» با مقادیر فعلی جدول جایگزین شود؟`)) return;
  try {
    const result = await recipeStore.updateRecipe(recipe.id, { target_values: { ...tableValues.value } } as any);
    if (result) {
      showToast('مقادیر رسپی به‌روزرسانی شد');
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در به‌روزرسانی رسپی', 'error');
  }
};

// اعمال رسپی: همهٔ جدول با مقادیر رسپی جایگزین می‌شود (عناصر نبوده در رسپی صفر می‌شوند)
const applyRecipe = async (id: number) => {
  try {
    const result = await recipeStore.applyRecipe(id);
    if (result) {
      for (const el of ALL_ELEMENTS) {
        targetStore.setTargetElement(el as any, Number((result as any)[el]) || 0);
      }
      showToast('رسپی در جدول اعمال شد');
      emit('recipe-applied');
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در اعمال رسپی', 'error');
  }
};

const copyRecipe = async (id: number) => {
  if (userRecipes.value.length >= PERSONAL_RECIPE_LIMIT) {
    showToast('ظرفیت رسپی‌های شخصی تکمیل شده است.', 'error');
    return;
  }
  try {
    const result = await recipeStore.copySystemRecipe(id);
    if (result) {
      showToast(`رسپی «${result.name}» در رسپی‌های شخصی ذخیره شد`);
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در کپی رسپی', 'error');
  }
};

const deleteRecipe = async (id: number) => {
  if (!confirm('آیا از حذف این رسپی اطمینان دارید؟')) return;
  try {
    const success = await recipeStore.deleteRecipe(id);
    if (success) {
      showToast('رسپی حذف شد');
      await recipeStore.loadAllRecipes();
    }
  } catch (error: any) {
    showToast(error.message || 'خطا در حذف رسپی', 'error');
  }
};

defineExpose({ openSaveModal });

onMounted(async () => {
  await recipeStore.loadAllRecipes();
});
</script>

<style scoped>
.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translate(-50%, 10px); }
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; line-clamp: 3; }
.tabular-nums { font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }
</style>
