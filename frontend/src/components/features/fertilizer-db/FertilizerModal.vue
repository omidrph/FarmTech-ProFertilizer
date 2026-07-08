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
        class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity" 
        @click="isMobile ? null : $emit('close')"
      ></div>

      <!-- کانتینر مودال -->
      <div 
        class="flex min-h-full items-end sm:items-center justify-center p-0 sm:p-4"
        @click.self="isMobile ? null : $emit('close')"
      >
        <div 
          class="relative transform overflow-hidden bg-white dark:bg-gray-800 text-right shadow-xl transition-all w-full sm:w-auto sm:max-w-4xl sm:rounded-xl"
          :class="isMobile ? 'h-full max-h-screen rounded-none' : 'sm:my-6 max-h-[95vh]'"
          style="max-height: 100vh;"
        >
          <!-- ============================================================ -->
          <!-- هدر مودال - ارتفاع یکپارچه با سایر مودال‌ها (py-4) -->
          <!-- ============================================================ -->
          <div class="bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 px-4 sm:px-6 py-4 flex items-center justify-between sticky top-0 z-20">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
              </div>
              <div class="min-w-0">
                <h3 id="modal-title" class="text-lg sm:text-xl font-bold text-white truncate">
                  {{ isEditing ? 'ویرایش کود' : 'افزودن کود شخصی' }}
                </h3>
                <p class="text-xs text-primary-100/80 hidden sm:block">
                  {{ isEditing ? 'تغییرات را اعمال کنید' : 'اطلاعات کود جدید را وارد کنید' }}
                </p>
              </div>
            </div>
            <button 
              @click="$emit('close')" 
              class="text-white/70 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/10 flex-shrink-0"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- ============================================================ -->
          <!-- بدنه مودال -->
          <!-- ============================================================ -->
          <div 
            class="px-3 sm:px-6 py-4 overflow-y-auto"
            :class="isMobile ? 'pb-24' : ''"
            style="max-height: calc(100vh - 130px);"
            ref="modalBodyRef"
          >
            
            <!-- هشدارها -->
            <div v-if="!formData.name && isTouched" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-2.5 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4 text-danger-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span class="text-sm text-danger-700 dark:text-danger-400">نام کود الزامی است</span>
            </div>

            <div v-if="totalElementsPercentage > 100" class="bg-warning-50 dark:bg-warning-900/20 border-r-4 border-warning-500 rounded-lg p-2.5 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4 text-warning-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span class="text-sm text-warning-700 dark:text-warning-400">مجموع درصد عناصر از ۱۰۰ بیشتر است ({{ totalElementsPercentage }}%)</span>
            </div>

            <!-- ============================================================ -->
            <!-- فرم - دسکتاپ: ۲ ستون، موبایل: ۱ ستون -->
            <!-- ============================================================ -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5">
              
              <!-- ============================================================ -->
              <!-- ستون راست: اطلاعات اصلی -->
              <!-- ============================================================ -->
              <div class="space-y-3 sm:space-y-4">
                <!-- نام کود -->
                <div>
                  <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    نام کود <span class="text-danger-500">*</span>
                  </label>
                  <input 
                    type="text" 
                    v-model="formData.name" 
                    @focus="isTouched = true"
                    placeholder="مثال: نیترات پتاسیم" 
                    class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  />
                </div>

                <!-- برند و دسته‌بندی -->
                <div class="grid grid-cols-2 gap-2 sm:gap-3">
                  <div>
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      برند
                    </label>
                    <input 
                      type="text" 
                      list="brand-list"
                      v-model="formData.brand" 
                      placeholder="رازاک شیمی" 
                      class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      دسته‌بندی
                    </label>
                    <input 
                      type="text" 
                      list="category-list"
                      v-model="formData.category" 
                      placeholder="NPK کامل" 
                      class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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
                <div class="grid grid-cols-2 gap-2 sm:gap-3">
                  <div>
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      فرم
                    </label>
                    <select 
                      v-model="formData.form" 
                      class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    >
                      <option value="">انتخاب...</option>
                      <option value="powder">پودری</option>
                      <option value="crystal">کریستالی</option>
                      <option value="liquid">مایع</option>
                      <option value="granular">گرانول</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      خلوص (%)
                    </label>
                    <input 
                      type="number" 
                      v-model.number="formData.concentration" 
                      min="0"
                      max="100"
                      step="0.1"
                      placeholder="۹۹" 
                      class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                <!-- فیلدهای مخصوص کود مایع -->
                <div v-if="formData.form === 'liquid'" class="bg-blue-50/30 dark:bg-blue-900/10 rounded-lg p-3 border border-blue-200 dark:border-blue-800/30 space-y-2">
                  <div class="flex items-center gap-2 text-xs font-medium text-blue-700 dark:text-blue-300">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                    </svg>
                    <span>ویژگی‌های کود مایع</span>
                  </div>
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] font-medium text-gray-600 dark:text-gray-400 mb-0.5">
                        حجم (لیتر)
                      </label>
                      <input 
                        type="number" 
                        v-model.number="formData.liquid_volume" 
                        min="0"
                        step="0.1"
                        placeholder="۱" 
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                    </div>
                    <div>
                      <label class="block text-[10px] font-medium text-gray-600 dark:text-gray-400 mb-0.5">
                        وزن مخصوص (g/cm³)
                      </label>
                      <input 
                        type="number" 
                        v-model.number="formData.specific_gravity" 
                        min="0"
                        step="0.01"
                        placeholder="۱.۲" 
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      />
                    </div>
                  </div>
                  <div>
                    <label class="block text-[10px] font-medium text-gray-600 dark:text-gray-400 mb-0.5">
                      غلظت ماده موثره (%)
                    </label>
                    <input 
                      type="number" 
                      v-model.number="formData.active_concentration" 
                      min="0"
                      max="100"
                      step="0.1"
                      placeholder="۵۰" 
                      class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                <!-- pH و قیمت -->
                <div class="grid grid-cols-2 gap-2 sm:gap-3">
                  <div>
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      pH
                    </label>
                    <input 
                      type="number" 
                      v-model.number="formData.ph_level" 
                      min="0"
                      max="14"
                      step="0.1"
                      placeholder="۶.۵" 
                      class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      قیمت (تومان) <span class="text-danger-500">*</span>
                    </label>
                    <div class="relative">
                      <input 
                        type="number" 
                        v-model.number="formData.price_per_kg" 
                        min="0"
                        placeholder="۸۵۰۰۰" 
                        class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all pr-14 sm:pr-16"
                      />
                      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] sm:text-xs text-gray-400">تومان</span>
                    </div>
                  </div>
                </div>

                <!-- توضیحات -->
                <div>
                  <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    توضیحات
                  </label>
                  <textarea 
                    v-model="formData.description" 
                    rows="2" 
                    placeholder="توضیحات درباره کاربرد، ویژگی‌ها..." 
                    class="w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  ></textarea>
                </div>
              </div>

              <!-- ============================================================ -->
              <!-- ستون چپ: عناصر و تنظیمات خاص -->
              <!-- ============================================================ -->
              <div class="space-y-3 sm:space-y-4">
                
                <!-- بخش اسید -->
                <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600">
                  <label class="flex items-center gap-2 text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer">
                    <input 
                      type="checkbox" 
                      v-model="formData.is_acid" 
                      class="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                    />
                    <span>اسید است</span>
                  </label>
                </div>

                <!-- بخش عناصر -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300">
                      عناصر تشکیل‌دهنده (%)
                    </label>
                    <button 
                      @click="clearElements" 
                      type="button"
                      class="text-[10px] sm:text-xs text-danger-500 hover:text-danger-700 dark:hover:text-danger-300 transition-colors"
                    >
                      پاک کردن
                    </button>
                  </div>
                  
                  <!-- موبایل: ۲ ستون، دسکتاپ: ۳-۴ ستون -->
                  <div 
                    class="grid gap-1.5 max-h-[200px] sm:max-h-[240px] overflow-y-auto p-2 bg-gray-50 dark:bg-gray-700/20 rounded-lg custom-scrollbar"
                    :class="isMobile ? 'grid-cols-2' : 'grid-cols-3 sm:grid-cols-4'"
                  >
                    <div 
                      v-for="el in elementsList" 
                      :key="el" 
                      class="flex flex-col gap-1"
                    >
                      <label 
                        class="text-[9px] sm:text-[10px] font-medium text-center rounded py-1 border transition-colors"
                        :class="getElementLabelClass(el)"
                      >
                        {{ el }}
                      </label>
                      <input 
                        type="number" 
                        v-model.number="formData.elements[el]" 
                        step="0.01" 
                        min="0" 
                        max="100"
                        placeholder="۰" 
                        class="w-full px-1 py-1.5 text-center border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-[10px] sm:text-xs focus:ring-1 focus:ring-primary-500 focus:border-primary-500 transition-all"
                        :class="getElementInputClass(el)"
                      />
                    </div>
                  </div>
                  
                  <!-- راهنمای رنگ‌ها و مجموع -->
                  <div class="flex flex-wrap items-center justify-between gap-1 mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
                    <div class="flex flex-wrap items-center gap-2 text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500">
                      <span class="flex items-center gap-1">
                        <span class="w-2.5 h-2.5 rounded-full bg-blue-400"></span>
                        <span>کاتیون</span>
                      </span>
                      <span class="flex items-center gap-1">
                        <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                        <span>آنیون</span>
                      </span>
                      <span class="flex items-center gap-1">
                        <span class="w-2.5 h-2.5 rounded-full bg-gray-400"></span>
                        <span>خنثی</span>
                      </span>
                    </div>
                    <span class="text-[10px] sm:text-xs font-mono text-gray-400 dark:text-gray-500" style="font-family: 'Vazirmatn', sans-serif;">
                      مجموع: <span class="font-bold" :class="totalElementsPercentage > 100 ? 'text-danger-500' : 'text-emerald-600 dark:text-emerald-400'">{{ totalElementsPercentage }}%</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- فوتر مودال - چسبیده به پایین -->
          <!-- ============================================================ -->
          <div 
            class="bg-gray-50 dark:bg-gray-700/30 px-3 sm:px-6 py-3 border-t border-gray-200 dark:border-gray-600 sticky bottom-0 z-10"
            :class="isMobile ? 'shadow-[0_-4px_12px_rgba(0,0,0,0.05)]' : ''"
          >
            <button 
              @click="handleSave" 
              :disabled="isSaving || !formData.name || totalElementsPercentage > 100"
              class="w-full py-2.5 sm:py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium shadow-sm hover:shadow-md"
            >
              <span v-if="isSaving" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <span>در حال ذخیره...</span>
              </span>
              <span v-else>
                {{ isEditing ? 'ذخیره تغییرات' : 'افزودن کود' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';

// ============================================================
// تعریف کاتیون‌ها، آنیون‌ها و خنثی‌ها
// ============================================================
const CATION_ELEMENTS = ['N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Fe', 'Mn', 'Zn', 'Cu'];
const ANION_ELEMENTS = ['N-NO3', 'P', 'S', 'Cl', 'B', 'Mo'];

const getElementType = (element: string): 'cation' | 'anion' | 'neutral' => {
  if (CATION_ELEMENTS.includes(element)) return 'cation';
  if (ANION_ELEMENTS.includes(element)) return 'anion';
  return 'neutral';
};

// ============================================================
// Props
// ============================================================
const props = defineProps<{
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
    liquid_volume?: number;
    specific_gravity?: number;
    active_concentration?: number;
  };
  isSaving: boolean;
}>();

// ============================================================
// Emits
// ============================================================
const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save'): void;
}>();

// ============================================================
// State
// ============================================================
const isTouched = ref(false);
const isMobile = ref(window.innerWidth < 640);
const modalBodyRef = ref<HTMLElement | null>(null);

const elementsList = [
  'N-NO3', 'N-NH4', 'P', 'K', 'Ca', 'Mg', 'S', 
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'Na', 'Cl'
];

// ============================================================
// Computed - مجموع درصد عناصر
// ============================================================
const totalElementsPercentage = computed(() => {
  const sum = Object.values(props.formData.elements).reduce((acc, val) => acc + (Number(val) || 0), 0);
  return parseFloat(sum.toFixed(1));
});

// ============================================================
// توابع رنگ‌آمیزی عناصر
// ============================================================
const getElementLabelClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800';
    case 'anion':
      return 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800';
    default:
      return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-600';
  }
};

const getElementInputClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'focus:ring-blue-500 focus:border-blue-500';
    case 'anion':
      return 'focus:ring-red-500 focus:border-red-500';
    default:
      return 'focus:ring-gray-500 focus:border-gray-500';
  }
};

// ============================================================
// Methods
// ============================================================
const clearElements = () => {
  if (confirm('آیا از پاک کردن تمام عناصر اطمینان دارید؟')) {
    for (const el of elementsList) {
      props.formData.elements[el] = 0;
    }
  }
};

const handleSave = () => {
  isTouched.value = true;
  if (!props.formData.name) return;
  if (totalElementsPercentage.value > 100) return;
  emit('save');
};

// ============================================================
// تشخیص موبایل
// ============================================================
const handleResize = () => {
  isMobile.value = window.innerWidth < 640;
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
/* ============================================================ */
/* اسکرول بار سفارشی */
/* ============================================================ */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
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

/* ============================================================ */
/* انیمیشن اسپین */
/* ============================================================ */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================================ */
/* حذف اسپینرهای input number */
/* ============================================================ */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

/* ============================================================ */
/* استایل دیتالیست */
/* ============================================================ */
input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 0.75rem center;
  background-size: 0.875rem;
  padding-left: 2.25rem;
}

.dark input[list] {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
}

/* ============================================================ */
/* بهینه‌سازی موبایل */
/* ============================================================ */
@media (max-width: 640px) {
  .custom-scrollbar::-webkit-scrollbar {
    width: 3px;
  }
  
  input[list] {
    background-size: 0.75rem;
    padding-left: 2rem;
  }
  
  /* فاصله بیشتر برای فوتر در موبایل */
  .pb-24 {
    padding-bottom: 6rem;
  }
}

/* ============================================================ */
/* مینیمال و تمیز */
/* ============================================================ */
input:focus, select:focus, textarea:focus {
  outline: none;
}
</style>