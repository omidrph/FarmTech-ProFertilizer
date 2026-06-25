<template>
<div class="space-y-6">
  <!-- ============================================================ -->
  <!-- هدر با توضیحات (یکپارچه با سایر تب‌ها) -->
  <!-- ============================================================ -->
  <div class="bg-primary-50 dark:bg-primary-900/20 border-r-4 border-primary-500 rounded-lg p-4">
    <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
      مقادیر آب و پساب را در جدول زیر وارد کنید. نرم‌افزار به صورت خودکار مقادیر تامینی را محاسبه می‌کند.
      همچنین می‌توانید نتایج آزمایش آب خود را ذخیره کرده و در گزارش‌های بعدی استفاده کنید.
    </p>
  </div>

  <!-- ============================================================ -->
  <!-- بخش تنظیمات درصد -->
  <!-- ============================================================ -->
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex flex-wrap justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">تنظیمات مخلوط آب</h3>
      <div class="text-xs text-gray-500 dark:text-gray-400">
        مجموع باید ۱۰۰٪ باشد
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- درصد آب -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">استفاده از آب (%)</label>
        <input
          type="number"
          :value="waterPercentage"
          @input="updateWaterPercentage($event)"
          min="0"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        />
      </div>

      <!-- درصد پساب -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">استفاده از پساب (%)</label>
        <input
          type="number"
          :value="wastewaterPercentage"
          @input="updateWastewaterPercentage($event)"
          min="0"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        />
      </div>
    </div>

    <!-- هشدار مجموع درصد -->
    <div v-if="totalPercentage !== 100" class="mt-3 bg-yellow-50 dark:bg-yellow-900/20 border-r-4 border-yellow-500 rounded-lg p-3">
      <p class="text-yellow-700 dark:text-yellow-400 text-sm flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        مجموع درصد آب و پساب باید برابر ۱۰۰ باشد. (فعلاً {{ totalPercentage }}٪)
      </p>
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- جدول آنالیز آب و پساب -->
  <!-- ============================================================ -->
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex flex-wrap justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">مقادیر آنالیز آب و پساب</h3>
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-600 dark:text-gray-400">واحد:</label>
        <select
          v-model="analysisUnit"
          class="px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
        >
          <option value="ppm">PPM/L</option>
          <option value="meq">MEQ/L</option>
          <option value="mmol">MMOLS/L</option>
        </select>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-sm border-collapse">
        <thead>
          <tr>
            <th class="px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[80px]">
              عنصر
            </th>
            <th v-for="el in waterElements" :key="el" class="px-2 py-2 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold border border-gray-200 dark:border-gray-600 text-center min-w-[70px]">
              <div class="flex items-center justify-center gap-1">
                <span>{{ el }}</span>
                <!-- واحد EC فقط برای ستون EC -->
                <select 
                  v-if="el === 'EC'" 
                  v-model="ecUnit"
                  class="text-[10px] bg-transparent border-none focus:ring-0 cursor-pointer text-primary-600 dark:text-primary-400 font-bold"
                  title="تغییر واحد EC"
                >
                  <option value="dS/m">dS/m</option>
                  <option value="mS/cm">mS/cm</option>
                  <option value="μS/cm">μS/cm</option>
                </select>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- ردیف پساب - فقط وقتی درصد پساب > 0 یا مقداری وارد شده -->
          <tr v-if="showWastewaterRow" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
            <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">
              پساب
            </td>
            <td v-for="el in waterElements" :key="'waste-'+el" class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center">
              <!-- عناصر معمولی -->
              <input
                v-if="!['EC', 'pH'].includes(el)"
                type="number"
                :value="getWastewaterValue(el)"
                @input="updateWastewaterValue(el, $event)"
                step="0.01"
                min="0"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                placeholder="۰"
              />
              <!-- EC برای پساب -->
              <input
                v-else-if="el === 'EC'"
                type="number"
                :value="wastewaterEC"
                @input="updateWastewaterEC($event)"
                step="0.01"
                min="0"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200 font-bold text-orange-600 dark:text-orange-400"
                placeholder="-"
              />
              <!-- pH برای پساب -->
              <input
                v-else-if="el === 'pH'"
                type="number"
                :value="wastewaterPH"
                @input="updateWastewaterPH($event)"
                step="0.1"
                min="0"
                max="14"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                placeholder="-"
              />
            </td>
          </tr>

          <!-- ردیف آب -->
          <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
            <td class="px-3 py-2 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-center font-medium text-gray-600 dark:text-gray-400">
              آب
            </td>
            <td v-for="el in waterElements" :key="'water-'+el" class="px-2 py-1 border border-gray-200 dark:border-gray-600 text-center">
              <!-- عناصر معمولی -->
              <input
                v-if="!['EC', 'pH'].includes(el)"
                type="number"
                :value="getWaterValue(el)"
                @input="updateWaterValue(el, $event)"
                step="0.01"
                min="0"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                placeholder="۰"
              />
              <!-- EC برای آب -->
              <input
                v-else-if="el === 'EC'"
                type="number"
                :value="waterSalinity"
                @input="updateWaterSalinity($event)"
                @blur="validateWaterSalinity"
                step="0.01"
                min="0"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200 font-bold text-primary-600 dark:text-primary-400"
              />
              <!-- pH برای آب -->
              <input
                v-else-if="el === 'pH'"
                type="number"
                :value="waterPH"
                @input="updateWaterPH($event)"
                step="0.1"
                min="0"
                max="14"
                class="w-full max-w-[70px] px-1.5 py-1 text-center bg-transparent border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500 rounded transition-all duration-200"
                placeholder="-"
              />
            </td>
          </tr>

          <!-- ردیف مقادیر تامینی -->
          <tr class="bg-primary-50 dark:bg-primary-900/10">
            <td class="px-3 py-2 bg-primary-50 dark:bg-primary-900/10 border border-gray-200 dark:border-gray-600 text-center font-semibold text-primary-600 dark:text-primary-400">
              مقادیر تامینی
            </td>
            <td v-for="el in waterElements" :key="'final-'+el" class="px-2 py-2 border border-gray-200 dark:border-gray-600 text-center font-semibold text-primary-600 dark:text-primary-400">
              {{ getFinalValue(el) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- دکمه‌های اقدام -->
    <div class="flex flex-wrap gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="saveWaterAnalysis"
        class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="totalPercentage !== 100 || waterSalinity <= 0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        ذخیره آنالیز آب
      </button>
      <button
        @click="resetWaterAnalysis"
        class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        بازنشانی
      </button>
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- بخش قالب‌های آنالیز آب (بدون تب‌بندی) -->
  <!-- ============================================================ -->
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">قالب‌های ذخیره شده</h3>
      <button
        @click="openSaveTemplateModal"
        class="px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm flex items-center gap-1"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        ذخیره قالب جدید
      </button>
    </div>

    <!-- لیست قالب‌ها -->
    <div v-if="waterTemplates.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      <div
        v-for="template in waterTemplates"
        :key="template.id"
        class="group relative bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 transition-all"
      >
        <div class="flex items-start justify-between mb-2">
          <h4 class="font-medium text-gray-900 dark:text-white text-sm truncate pr-6">
            {{ template.name }}
          </h4>
          <div class="absolute top-2 left-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              @click="loadWaterTemplate(template)"
              class="p-1 rounded text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/30"
              title="بارگذاری"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
              </svg>
            </button>
            <button
              @click="deleteWaterTemplate(template.id)"
              class="p-1 rounded text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/30"
              title="حذف"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="flex flex-wrap gap-2 text-[10px] text-gray-500 dark:text-gray-400">
          <span>آب: {{ template.water_percentage }}%</span>
          <span>EC: {{ template.water_salinity }} {{ template.water_salinity_unit }}</span>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-6 text-sm text-gray-400 dark:text-gray-500">
      هنوز قالبی ذخیره نشده است
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- مودال ذخیره قالب -->
  <!-- ============================================================ -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showSaveTemplateModal" class="fixed inset-0 z-[100] overflow-y-auto" role="dialog">
        <div class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm" @click="closeSaveTemplateModal"></div>
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">ذخیره قالب جدید</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام قالب</label>
                <input
                  type="text"
                  v-model="templateForm.name"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-1 focus:ring-indigo-500 text-sm"
                  placeholder="مثال: آب چاه شماره ۱"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">توضیحات (اختیاری)</label>
                <textarea
                  v-model="templateForm.description"
                  rows="2"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-1 focus:ring-indigo-500 text-sm resize-none"
                ></textarea>
              </div>
            </div>
            <div class="mt-6 flex justify-end gap-3">
              <button
                @click="closeSaveTemplateModal"
                class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
              >
                انصراف
              </button>
              <button
                @click="saveWaterTemplate"
                :disabled="isSavingTemplate || !templateForm.name"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm disabled:opacity-50"
              >
                {{ isSavingTemplate ? '...' : 'ذخیره' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ============================================================ -->
  <!-- پیام‌های وضعیت (Toast) -->
  <!-- ============================================================ -->
  <Transition name="fade">
    <div v-if="toastMessage" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[200] px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 text-sm"
      :class="toastType === 'success' ? 'bg-success-600 text-white' : 'bg-danger-600 text-white'"
    >
      <span>{{ toastMessage }}</span>
    </div>
  </Transition>
</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useWaterStore, EC_STANDARDS, convertECUnit, calculateTDS } from '@/store/modules/waterStore';
import { apiService } from '@/services/apiService';

// ===== Store =====
const waterStore = useWaterStore();

// ===== State =====
const waterElements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo', 'EC', 'pH'];
const analysisUnit = ref('ppm');

// Toast State
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

// Template State
const waterTemplates = ref<any[]>([]);
const showSaveTemplateModal = ref(false);
const isSavingTemplate = ref(false);
const templateForm = ref({ name: '', description: '' });

// ===== Computed =====
const waterPercentage = computed({
  get: () => waterStore.waterMixData.waterPercentage,
  set: (val: number) => waterStore.setWaterMix({ waterPercentage: val })
});

const wastewaterPercentage = computed({
  get: () => waterStore.waterMixData.wastewaterPercentage,
  set: (val: number) => waterStore.setWaterMix({ wastewaterPercentage: val })
});

const waterSalinity = computed({
  get: () => waterStore.waterMixData.waterSalinity,
  set: (val: number) => waterStore.setWaterMix({ waterSalinity: val })
});

const ecUnit = computed({
  get: () => waterStore.ecUnit,
  set: (val: any) => waterStore.setECUnit(val)
});

const waterPH = computed({
  get: () => waterStore.waterPH,
  set: (val: number | null) => waterStore.setWaterPH(val)
});

// EC پساب - از wastewaterValues خوانده می‌شود
const wastewaterEC = computed({
  get: () => (waterStore.wastewaterValues as any)['EC'] || 0,
  set: (val: number) => waterStore.setWastewaterValue('EC', val)
});

// pH پساب - از wastewaterValues خوانده می‌شود
const wastewaterPH = computed({
  get: () => (waterStore.wastewaterValues as any)['pH'] || 0,
  set: (val: number) => waterStore.setWastewaterValue('pH', val)
});

const totalPercentage = computed(() => {
  return (waterPercentage.value || 0) + (wastewaterPercentage.value || 0);
});

// ردیف پساب فقط وقتی درصد پساب > 0 یا مقداری وارد شده نمایش داده می‌شود
const showWastewaterRow = computed(() => {
  if (wastewaterPercentage.value > 0) return true;
  return Object.values(waterStore.wastewaterValues).some(v => v > 0);
});

// ===== Methods =====
const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg;
  toastType.value = type;
  setTimeout(() => { toastMessage.value = null; }, 3000);
};

const getWastewaterValue = (element: string): number => {
  if (element === 'EC' || element === 'pH') return 0;
  return (waterStore.wastewaterValues as any)[element] || 0;
};

const getWaterValue = (element: string): number => {
  if (element === 'EC') return waterSalinity.value;
  if (element === 'pH') return waterPH.value || 0;
  return (waterStore.waterValues as any)[element] || 0;
};

const getFinalValue = (element: string): string => {
  if (element === 'EC' || element === 'pH') return '-';
  const waterPct = (waterPercentage.value || 0) / 100;
  const wastePct = (wastewaterPercentage.value || 0) / 100;
  const waterVal = getWaterValue(element);
  const wasteVal = getWastewaterValue(element);
  const val = (waterVal * waterPct) + (wasteVal * wastePct);
  return val.toFixed(2);
};

// محاسبه خودکار درصد - وقتی آب تغییر می‌کند، پساب خودکار تغییر می‌کند
const updateWaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value = parseFloat(target.value) || 0;
  if (value > 100) value = 100;
  if (value < 0) value = 0;
  waterPercentage.value = value;
  wastewaterPercentage.value = 100 - value;
};

const updateWastewaterPercentage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value = parseFloat(target.value) || 0;
  if (value > 100) value = 100;
  if (value < 0) value = 0;
  wastewaterPercentage.value = value;
  waterPercentage.value = 100 - value;
};

const updateWaterSalinity = (event: Event) => {
  const target = event.target as HTMLInputElement;
  let value = parseFloat(target.value) || 0;
  if (value > 0 && value < EC_STANDARDS.MIN_VALID_EC) value = EC_STANDARDS.MIN_VALID_EC;
  waterSalinity.value = value;
};

const validateWaterSalinity = () => {
  if (waterSalinity.value <= 0) waterSalinity.value = EC_STANDARDS.DEFAULT_EC;
};

const updateWaterPH = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const value = parseFloat(target.value);
  waterPH.value = isNaN(value) ? null : value;
};

const updateWastewaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  waterStore.setWastewaterValue(element, parseFloat(target.value) || 0);
};

const updateWaterValue = (element: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  waterStore.setWaterValue(element, parseFloat(target.value) || 0);
};

const updateWastewaterEC = (event: Event) => {
  const target = event.target as HTMLInputElement;
  waterStore.setWastewaterValue('EC', parseFloat(target.value) || 0);
};

const updateWastewaterPH = (event: Event) => {
  const target = event.target as HTMLInputElement;
  waterStore.setWastewaterValue('pH', parseFloat(target.value) || 0);
};

const saveWaterAnalysis = () => {
  if (totalPercentage.value !== 100) {
    showToast('مجموع درصد آب و پساب باید ۱۰۰ باشد', 'error');
    return;
  }
  if (waterSalinity.value <= 0) {
    showToast('EC آب نمی‌تواند صفر باشد', 'error');
    return;
  }
  showToast('آنالیز آب ذخیره شد', 'success');
};

const resetWaterAnalysis = () => {
  waterStore.resetWaterData();
  showToast('تنظیمات بازنشانی شد', 'success');
};

// Template Methods
const loadWaterTemplates = async () => {
  try {
    const templates = await apiService.get('/water-templates');
    waterTemplates.value = Array.isArray(templates) ? templates : [];
  } catch (error) { console.error(error); }
};

const openSaveTemplateModal = () => {
  templateForm.value = { name: '', description: '' };
  showSaveTemplateModal.value = true;
};

const closeSaveTemplateModal = () => {
  showSaveTemplateModal.value = false;
};

const saveWaterTemplate = async () => {
  if (!templateForm.value.name) return;
  isSavingTemplate.value = true;
  try {
    await apiService.post('/water-templates', {
      name: templateForm.value.name,
      description: templateForm.value.description || null,
      water_percentage: waterPercentage.value,
      wastewater_percentage: wastewaterPercentage.value,
      water_salinity: waterSalinity.value,
      water_salinity_unit: ecUnit.value,
      water_ph: waterPH.value,
      water_values: waterStore.waterValues,
      wastewater_values: waterStore.wastewaterValues
    });
    await loadWaterTemplates();
    closeSaveTemplateModal();
    showToast('قالب ذخیره شد', 'success');
  } catch (error: any) {
    showToast('خطا در ذخیره قالب', 'error');
  } finally {
    isSavingTemplate.value = false;
  }
};

const loadWaterTemplate = async (template: any) => {
  waterPercentage.value = template.water_percentage;
  wastewaterPercentage.value = template.wastewater_percentage;
  waterSalinity.value = template.water_salinity;
  waterStore.setECUnit(template.water_salinity_unit || 'dS/m');
  waterStore.setWaterPH(template.water_ph);
  waterStore.wastewaterValues = {};
  waterStore.waterValues = {};
  if (template.water_values) {
    for (const [key, value] of Object.entries(template.water_values)) {
      waterStore.setWaterValue(key, value as number);
    }
  }
  if (template.wastewater_values) {
    for (const [key, value] of Object.entries(template.wastewater_values)) {
      waterStore.setWastewaterValue(key, value as number);
    }
  }
  showToast(`قالب "${template.name}" بارگذاری شد`, 'success');
};

const deleteWaterTemplate = async (templateId: number) => {
  try {
    await apiService.delete(`/water-templates/${templateId}`);
    await loadWaterTemplates();
    showToast('قالب حذف شد', 'success');
  } catch (error) {
    showToast('خطا در حذف قالب', 'error');
  }
};

onMounted(() => {
  loadWaterTemplates();
});
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .relative, .modal-leave-to .relative { transform: scale(0.95); }

.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translate(-50%, 10px); }
</style>