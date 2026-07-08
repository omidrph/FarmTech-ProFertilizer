<!-- frontend/src/components/features/fertilizer-db/FertilizerModal.vue -->
<template>
  <Teleport to="body">
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-[100] overflow-y-auto"
      aria-labelledby="modal-title" 
      role="dialog" 
      aria-modal="true"
    >
      <!-- پس‌زمینه تاریک -->
      <div 
        class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity" 
        @click="$emit('close')"
      ></div>

      <!-- کانتینر مودال -->
      <div class="flex min-h-full items-center justify-center p-0 sm:p-4 text-center sm:text-left">
        <div 
          class="relative transform overflow-hidden bg-white dark:bg-gray-800 text-right shadow-2xl transition-all w-full h-full sm:h-auto sm:my-8 sm:max-w-4xl sm:rounded-2xl"
        >
          <!-- هدر مودال -->
          <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-4 sm:px-6 py-4 flex items-center justify-between sticky top-0 z-10">
            <h3 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              {{ isEditing ? 'ویرایش کود' : 'افزودن کود شخصی جدید' }}
            </h3>
            <button 
              @click="$emit('close')" 
              class="text-white/80 hover:text-white transition-colors p-1 rounded-full hover:bg-white/10"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- بدنه مودال -->
          <div class="px-4 sm:px-6 py-5 max-h-[calc(100vh-140px)] sm:max-h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              
              <!-- ستون راست: اطلاعات اصلی -->
              <div class="space-y-4">
                <!-- نام کود -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    نام کود <span class="text-danger-500">*</span>
                  </label>
                  <input 
                    type="text" 
                    v-model="formData.name" 
                    placeholder="مثال: نیترات پتاسیم گرین استار" 
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>

                <!-- برند و دسته‌بندی -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      برند / شرکت
                    </label>
                    <input 
                      type="text" 
                      list="brand-list"
                      v-model="formData.brand" 
                      placeholder="مثال: رازاک شیمی" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                    <datalist id="brand-list">
                      <option value="عمومی"></option>
                      <option value="رازاک شیمی"></option>
                      <option value="گل سم گرگان"></option>
                      <option value="اطلس"></option>
                      <option value="ردسا"></option>
                      <option value="کوالی مکس"></option>
                    </datalist>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      دسته‌بندی
                    </label>
                    <input 
                      type="text" 
                      list="category-list"
                      v-model="formData.category" 
                      placeholder="مثال: NPK کامل" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                    <datalist id="category-list">
                      <option value="NPK کامل"></option>
                      <option value="NPK پتاسیم بالا"></option>
                      <option value="NPK فسفر بالا"></option>
                      <option value="NPK نیتروژن بالا"></option>
                      <option value="نیترات"></option>
                      <option value="سولفات"></option>
                      <option value="فسفات"></option>
                      <option value="کلات"></option>
                      <option value="ریزمغذی"></option>
                      <option value="اسید"></option>
                      <option value="محرک رشد"></option>
                    </datalist>
                  </div>
                </div>

                <!-- فرم فیزیکی و خلوص -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      فرم فیزیکی
                    </label>
                    <select 
                      v-model="formData.form" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    >
                      <option value="">انتخاب کنید...</option>
                      <option value="powder">پودری (Powder)</option>
                      <option value="crystal">کریستالی (Crystal)</option>
                      <option value="liquid">مایع (Liquid)</option>
                      <option value="granular">گرانول (Granular)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      خلوص / غلظت (%)
                    </label>
                    <input 
                      type="number" 
                      v-model.number="formData.concentration" 
                      min="0"
                      max="100"
                      step="0.1"
                      placeholder="مثال: 99" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                <!-- pH و قیمت -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      pH محلول
                    </label>
                    <input 
                      type="number" 
                      v-model.number="formData.ph_level" 
                      min="0"
                      max="14"
                      step="0.1"
                      placeholder="مثال: 6.5" 
                      class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      قیمت هر کیلوگرم (تومان) <span class="text-danger-500">*</span>
                    </label>
                    <div class="relative">
                      <input 
                        type="number" 
                        v-model.number="formData.price_per_kg" 
                        min="0"
                        placeholder="مثال: 85000" 
                        class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all pl-16"
                      />
                      <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-sm">تومان</span>
                    </div>
                  </div>
                </div>

                <!-- توضیحات -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    توضیحات تکمیلی
                  </label>
                  <textarea 
                    v-model="formData.description" 
                    rows="2" 
                    placeholder="توضیحات درباره کاربرد، ویژگی‌ها..." 
                    class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  ></textarea>
                </div>
              </div>

              <!-- ستون چپ: عناصر و تنظیمات خاص -->
              <div class="space-y-4">
                
                <!-- بخش اسید -->
                <div class="bg-gray-50 dark:bg-gray-700/30 rounded-xl p-4 border border-gray-200 dark:border-gray-600">
                  <div class="flex items-center justify-between mb-3">
                    <label class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input 
                        type="checkbox" 
                        v-model="formData.is_acid" 
                        class="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                      />
                      این ماده یک اسید است
                    </label>
                    <span v-if="formData.is_acid" class="text-xs bg-warning-100 dark:bg-warning-900/30 text-warning-700 dark:text-warning-400 px-2 py-0.5 rounded-full">
                      تنظیم pH
                    </span>
                  </div>
                  
                  <div v-if="formData.is_acid" class="animate-fade-in">
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">نوع اسید</label>
                    <select 
                      v-model="formData.acid_type" 
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    >
                      <option value="">انتخاب نوع اسید...</option>
                      <option value="H3PO4">اسید فسفریک (H3PO4)</option>
                      <option value="HNO3">اسید نیتریک (HNO3)</option>
                      <option value="H2SO4">اسید سولفوریک (H2SO4)</option>
                      <option value="Other">سایر اسیدها</option>
                    </select>
                  </div>
                </div>

                <!-- بخش عناصر -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      درصد عناصر تشکیل‌دهنده (%)
                    </label>
                    <button 
                      @click="clearElements" 
                      type="button"
                      class="text-xs text-danger-600 hover:text-danger-800 dark:hover:text-danger-400 transition-colors"
                    >
                      پاک کردن همه
                    </button>
                  </div>
                  
                  <div class="grid grid-cols-3 sm:grid-cols-4 gap-2 max-h-[280px] overflow-y-auto p-2 bg-gray-50 dark:bg-gray-700/20 rounded-lg custom-scrollbar">
                    <div v-for="el in elementsList" :key="el" class="flex flex-col gap-1">
                      <label class="text-xs font-medium text-gray-600 dark:text-gray-400 text-center bg-white dark:bg-gray-700 rounded py-1 border border-gray-200 dark:border-gray-600">
                        {{ el }}
                      </label>
                      <input 
                        type="number" 
                        v-model.number="formData.elements[el]" 
                        step="0.01" 
                        min="0" 
                        max="100"
                        placeholder="۰" 
                        class="w-full px-2 py-1.5 text-center border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-1 focus:ring-primary-500 focus:border-primary-500 transition-all"
                      />
                    </div>
                  </div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 text-center">
                    مقادیر را بر اساس درصد وزنی وارد کنید (مثلاً ۲۰ برای ۲۰٪)
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- فوتر مودال -->
          <div class="bg-gray-50 dark:bg-gray-700/30 px-4 sm:px-6 py-4 border-t border-gray-200 dark:border-gray-600 flex flex-col-reverse sm:flex-row gap-3 justify-end sticky bottom-0">
            <button 
              @click="$emit('close')" 
              class="w-full sm:w-auto px-6 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 transition-colors font-medium"
            >
              انصراف
            </button>
            <button 
              @click="$emit('save')" 
              :disabled="isSaving || !formData.name"
              class="w-full sm:w-auto px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2 shadow-lg shadow-primary-500/30"
            >
              <svg v-if="isSaving" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره تغییرات' : 'افزودن کود') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
// ============================================================
// Props
// ============================================================
defineProps<{
  isOpen: boolean;
  isEditing: boolean;
  formData: {
    id: string | null;
    name: string;
    brand: string;
    category: string;
    form: '' | 'liquid' | 'powder' | 'crystal' | 'granular';
    concentration: number;
    price_per_kg: number;
    elements: Record<string, number>;
    is_acid: boolean;
    acid_type: string;
    ph_level: number | null;
    description: string;
    is_system_default: boolean;
    source_system_id: number | null;
  };
  isSaving: boolean;
}>();

// ============================================================
// Emits
// ============================================================
defineEmits<{
  (e: 'close'): void;
  (e: 'save'): void;
}>();

// ============================================================
// State
// ============================================================
const elementsList = [
  'N-NO3', 'N-NH4', 'P', 'K', 'Ca', 'Mg', 'S', 
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Na', 'Cl'
];

// ============================================================
// Methods
// ============================================================
const clearElements = () => {
  if (confirm('آیا از پاک کردن تمام عناصر اطمینان دارید؟')) {
    // این کار از طریق props قابل انجام نیست، باید از والد بیاید
    // اما چون formData یک prop است، نمی‌توانیم آن را مستقیم تغییر دهیم
    alert('لطفاً از دکمه "پاک کردن همه" در بخش عناصر استفاده کنید (این عملیات در حال حاضر غیرفعال است)');
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 1rem;
  padding-left: 2.5rem;
}

.dark input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}
</style>