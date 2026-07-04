<!-- frontend/src/components/features/target/BalanceAndGuide.vue -->
<template>
  <div id="balance-guide-section" class="space-y-2">
    <!-- ============================================================ -->
    <!-- هدر اکوردئون (مینیمال) -->
    <!-- ============================================================ -->
    <button
      @click="isOpen = !isOpen"
      class="w-full flex items-center justify-between p-3 sm:p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 transition-all duration-200 group"
    >
      <div class="flex items-center gap-2 sm:gap-3 min-w-0">
        <svg 
          class="w-4 h-4 sm:w-5 sm:h-5 text-gray-400 transition-transform duration-200 flex-shrink-0"
          :class="{ 'rotate-180': isOpen }"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
        <span class="text-sm sm:text-base font-medium text-gray-700 dark:text-gray-300 truncate">
          جدول توازن عناصر
        </span>
        <span class="text-xs text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-gray-700 px-1.5 sm:px-2 py-0.5 rounded-full flex-shrink-0">
          {{ elements.length }}
        </span>
      </div>
      <div class="text-xs text-gray-400 dark:text-gray-500 flex-shrink-0">
        {{ isOpen ? 'بستن' : 'باز کردن' }}
      </div>
    </button>

    <!-- ============================================================ -->
    <!-- محتوای اکوردئون -->
    <!-- ============================================================ -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="max-h-0 opacity-0"
      enter-to-class="max-h-[3000px] opacity-100"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="max-h-[3000px] opacity-100"
      leave-to-class="max-h-0 opacity-0"
    >
      <div v-show="isOpen" class="overflow-hidden">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          
          <!-- ========================================================== -->
          <!-- جدول توازن عناصر (ریسپانسیو) -->
          <!-- ========================================================== -->
          <div class="p-3 sm:p-5">
            <div v-if="isConverting && !convertedValues" class="flex items-center justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <span class="mr-2 text-gray-600 dark:text-gray-400 text-sm">در حال تبدیل واحدها...</span>
            </div>

            <div v-else class="overflow-x-auto custom-scrollbar">
              <table class="w-full text-xs sm:text-sm border-collapse min-w-[500px]">
                <thead>
                  <tr>
                    <th class="sticky right-0 z-10 bg-gray-50 dark:bg-gray-700 px-2 sm:px-4 py-2 sm:py-3 text-right text-[10px] sm:text-xs font-semibold text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 min-w-[60px] sm:min-w-[80px] shadow-sm">
                      واحد
                    </th>
                    <th 
                      v-for="element in elements" 
                      :key="element" 
                      class="px-1.5 sm:px-3 py-2 sm:py-3 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[50px] sm:min-w-[70px] transition-colors text-[10px] sm:text-xs"
                      :class="getElementHeaderClass(element)"
                    >
                      {{ element }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-2 sm:px-4 py-1.5 sm:py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm text-[10px] sm:text-sm">
                      PPM/L
                    </td>
                    <td 
                      v-for="element in elements" 
                      :key="'ppm-'+element" 
                      class="px-1.5 sm:px-3 py-1.5 sm:py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300 text-[10px] sm:text-sm"
                      :class="getElementCellClass(element)"
                    >
                      {{ getConvertedValue(element, 'ppm') }}
                    </td>
                  </tr>
                  <tr>
                    <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-2 sm:px-4 py-1.5 sm:py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm text-[10px] sm:text-sm">
                      MEQ/L
                    </td>
                    <td 
                      v-for="element in elements" 
                      :key="'meq-'+element" 
                      class="px-1.5 sm:px-3 py-1.5 sm:py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300 text-[10px] sm:text-sm"
                      :class="getElementCellClass(element)"
                    >
                      {{ getConvertedValue(element, 'meq') }}
                    </td>
                  </tr>
                  <tr>
                    <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-2 sm:px-4 py-1.5 sm:py-2.5 text-right font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm text-[10px] sm:text-sm">
                      MMOL/L
                    </td>
                    <td 
                      v-for="element in elements" 
                      :key="'mmol-'+element" 
                      class="px-1.5 sm:px-3 py-1.5 sm:py-2.5 border-l border-gray-100 dark:border-gray-700 text-center tabular-nums text-gray-700 dark:text-gray-300 text-[10px] sm:text-sm"
                      :class="getElementCellClass(element)"
                    >
                      {{ getConvertedValue(element, 'mmol') }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- راهنمای رنگ‌ها (ریسپانسیو) -->
            <div class="mt-3 px-2 sm:px-4 py-2 sm:py-2.5 bg-gray-50 dark:bg-gray-700/30 rounded-lg flex flex-wrap items-center gap-2 sm:gap-4 text-[10px] sm:text-xs">
              <span class="text-gray-600 dark:text-gray-400 font-medium">راهنما:</span>
              <div class="flex items-center gap-1 sm:gap-1.5">
                <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-blue-500"></span>
                <span class="text-gray-600 dark:text-gray-400">کاتیون</span>
              </div>
              <div class="flex items-center gap-1 sm:gap-1.5">
                <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
                <span class="text-gray-600 dark:text-gray-400">آنیون</span>
              </div>
              <div class="flex items-center gap-1 sm:gap-1.5">
                <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-gray-400"></span>
                <span class="text-gray-600 dark:text-gray-400">خنثی</span>
              </div>
            </div>
          </div>

          <!-- ========================================================== -->
          <!-- راهنمای عناصر غذایی (طراحی ریسپانسیو) -->
          <!-- ========================================================== -->
          <div class="border-t border-gray-200 dark:border-gray-700 p-3 sm:p-5">
            <h4 class="text-sm sm:text-base font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2 mb-3">
              <svg class="w-4 h-4 sm:w-5 sm:h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
              راهنمای عناصر غذایی
            </h4>

            <!-- تب‌های عناصر (ریسپانسیو - اسکرول افقی با اسکرول نازک) -->
            <div class="overflow-x-auto custom-scrollbar-tabs pb-2 -mx-1 px-1">
              <div class="flex flex-nowrap gap-1 min-w-max">
                <button
                  v-for="element in elements"
                  :key="element"
                  @click="selectElement(element)"
                  class="px-2 sm:px-3 py-1 text-[10px] sm:text-xs font-medium rounded-lg transition-all duration-200 whitespace-nowrap flex-shrink-0"
                  :class="selectedElement === element
                    ? getElementActiveTabClass(element)
                    : getElementTabClass(element)"
                >
                  {{ element }}
                </button>
              </div>
            </div>

            <!-- اطلاعات عنصر انتخاب شده (بدون باکس رنگی) -->
            <div v-if="selectedElementData" class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 sm:p-4 border border-gray-200 dark:border-gray-600">
              <div class="flex flex-col">
                <!-- هدر اطلاعات -->
                <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-1 sm:gap-2 mb-3">
                  <div class="w-full sm:w-auto">
                    <h5 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white">
                      {{ selectedElementData.name }}
                    </h5>
                    <p class="text-[10px] sm:text-xs text-gray-500 dark:text-gray-400 flex flex-wrap items-center gap-1">
                      <span>{{ selectedElementData.symbol }}</span>
                      <span class="text-gray-300 dark:text-gray-600">•</span>
                      <span :class="getCategoryClass(selectedElementData.category)">
                        {{ selectedElementData.category === 'macro' ? 'ماکرو' : 'میکرو' }}
                      </span>
                      <span class="text-gray-300 dark:text-gray-600">•</span>
                      <span :class="getMobilityClass(selectedElementData.mobility)">
                        {{ selectedElementData.mobility === 'mobile' ? 'متحرک' : 'غیرمتحرک' }}
                      </span>
                    </p>
                  </div>
                  <div class="text-[10px] sm:text-xs text-gray-400 dark:text-gray-500 bg-white dark:bg-gray-800 px-2 sm:px-3 py-0.5 sm:py-1 rounded-full border border-gray-200 dark:border-gray-600 flex-shrink-0">
                    {{ selectedElementData.idealRange.min }} - {{ selectedElementData.idealRange.max }} {{ selectedElementData.idealRange.unit }}
                  </div>
                </div>

                <!-- کارت‌های اطلاعات (ریسپانسیو) -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <!-- نقش -->
                  <div class="bg-white dark:bg-gray-800 rounded-lg p-2.5 sm:p-3 border border-gray-200 dark:border-gray-600">
                    <div class="flex items-center gap-1.5 mb-0.5 sm:mb-1">
                      <svg class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <span class="text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500 font-medium">نقش در گیاه</span>
                    </div>
                    <p class="text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ selectedElementData.role }}</p>
                  </div>

                  <!-- کمبود -->
                  <div class="bg-white dark:bg-gray-800 rounded-lg p-2.5 sm:p-3 border border-gray-200 dark:border-gray-600">
                    <div class="flex items-center gap-1.5 mb-0.5 sm:mb-1">
                      <svg class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                      </svg>
                      <span class="text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500 font-medium">علائم کمبود</span>
                    </div>
                    <p class="text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ selectedElementData.deficiency }}</p>
                  </div>

                  <!-- سمیت -->
                  <div class="bg-white dark:bg-gray-800 rounded-lg p-2.5 sm:p-3 border border-gray-200 dark:border-gray-600">
                    <div class="flex items-center gap-1.5 mb-0.5 sm:mb-1">
                      <svg class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                      </svg>
                      <span class="text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500 font-medium">علائم سمیت</span>
                    </div>
                    <p class="text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ selectedElementData.toxicity }}</p>
                  </div>

                  <!-- منابع -->
                  <div class="bg-white dark:bg-gray-800 rounded-lg p-2.5 sm:p-3 border border-gray-200 dark:border-gray-600">
                    <div class="flex items-center gap-1.5 mb-0.5 sm:mb-1">
                      <svg class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                      </svg>
                      <span class="text-[9px] sm:text-[10px] text-gray-400 dark:text-gray-500 font-medium">منابع تأمین</span>
                    </div>
                    <div class="flex flex-wrap gap-1">
                      <span 
                        v-for="source in selectedElementData.sources" 
                        :key="source"
                        class="text-[9px] sm:text-xs px-1.5 sm:px-2 py-0.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full"
                      >
                        {{ source }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- نکات ویژه -->
                <div v-if="selectedElementData.notes" class="mt-2 bg-blue-50 dark:bg-blue-900/10 rounded-lg p-2.5 sm:p-3 border border-blue-100 dark:border-blue-800/30">
                  <div class="flex items-center gap-1.5 mb-0.5">
                    <svg class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span class="text-[9px] sm:text-[10px] text-blue-500 dark:text-blue-400 font-medium">نکته ویژه</span>
                  </div>
                  <p class="text-xs sm:text-sm text-blue-700 dark:text-blue-300 leading-relaxed">{{ selectedElementData.notes }}</p>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-6 sm:py-8 text-gray-400 dark:text-gray-500">
              <svg class="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-2 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-xs sm:text-sm">برای مشاهده اطلاعات، روی یکی از عناصر کلیک کنید</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

// ===== Props =====
interface Props {
  elements: string[];
  targetUnit: string;
  targetValues: Record<string, number>;
  convertedValues: Record<string, Record<string, number>> | null;
  isConverting: boolean;
  selectedElement: string;
}

const props = defineProps<Props>();

// ===== Emits =====
const emit = defineEmits<{
  (e: 'update:selectedElement', value: string): void;
  (e: 'openGuide', element: string): void;
}>();

// ===== State =====
const isOpen = ref(false);

// ============================================================
// ✅ داده‌های عناصر
// ============================================================
const ELEMENTS_DATA: Record<string, any> = {
  'N-NO3': {
    name: 'نیتروژن (نیتراتی)',
    symbol: 'N-NO3',
    role: 'ساخت پروتئین، کلروفیل، آنزیم‌ها و رشد رویشی گیاه',
    deficiency: 'زردی برگ‌های پیر، کاهش رشد، کوچک شدن برگ‌ها',
    toxicity: 'رشد رویشی بیش از حد، تأخیر در گلدهی، حساسیت به آفات',
    idealRange: { min: 140, max: 200, unit: 'ppm' },
    sources: ['نیترات کلسیم', 'نیترات پتاسیم', 'نیترات آمونیوم'],
    notes: 'شکل نیترات باعث افزایش pH ریشه می‌شود. برای گیاهان جوان و رشد رویشی مفید است.',
    category: 'macro',
    mobility: 'mobile'
  },
  'N-NH4': {
    name: 'نیتروژن (آمونیومی)',
    symbol: 'N-NH4',
    role: 'ساخت پروتئین و کلروفیل، جذب سریع توسط گیاه',
    deficiency: 'زردی برگ‌ها، کاهش رشد، کاهش کیفیت محصول',
    toxicity: 'سوختگی ریشه، کاهش جذب کلسیم و منیزیم',
    idealRange: { min: 0, max: 50, unit: 'ppm' },
    sources: ['سولفات آمونیوم', 'فسفات آمونیوم', 'نیترات آمونیوم'],
    notes: 'مصرف همزمان با نیترات باعث تعادل pH می‌شود. برای گیاهان بالغ مفید است.',
    category: 'macro',
    mobility: 'mobile'
  },
  'P': {
    name: 'فسفر',
    symbol: 'P',
    role: 'انتقال انرژی، فتوسنتز، تشکیل DNA و RNA، رشد ریشه و گلدهی',
    deficiency: 'رنگ ارغوانی برگ‌ها، رشد ریشه ضعیف، تأخیر در گلدهی',
    toxicity: 'کمبود آهن و روی، کاهش جذب عناصر ریز',
    idealRange: { min: 40, max: 60, unit: 'ppm' },
    sources: ['فسفات مونوپتاسیم', 'فسفات آمونیوم', 'سوپر فسفات'],
    notes: 'جذب فسفر در pH 6-6.5 بهینه است. با کلسیم واکنش داده و رسوب می‌کند.',
    category: 'macro',
    mobility: 'mobile'
  },
  'K': {
    name: 'پتاسیم',
    symbol: 'K',
    role: 'تنظیم فشار اسمزی، فعال‌سازی آنزیم‌ها، کیفیت میوه و مقاومت به تنش',
    deficiency: 'زردی و سوختگی حاشیه برگ‌ها، ساقه ضعیف، میوه‌های کوچک',
    toxicity: 'کمبود کلسیم و منیزیم، کاهش جذب عناصر',
    idealRange: { min: 250, max: 400, unit: 'ppm' },
    sources: ['نیترات پتاسیم', 'سولفات پتاسیم', 'فسفات مونوپتاسیم'],
    notes: 'پتاسیم با افزایش TSS و سفتی میوه، کیفیت محصول را بهبود می‌بخشد.',
    category: 'macro',
    mobility: 'mobile'
  },
  'Ca': {
    name: 'کلسیم',
    symbol: 'Ca',
    role: 'ساخت دیواره سلولی، تقسیم سلولی، رشد ریشه و مقاومت به بیماری‌ها',
    deficiency: 'نکروز نوک برگ‌ها، پوسیدگی انتهای میوه، رشد ریشه ضعیف',
    toxicity: 'کمبود پتاسیم و منیزیم، افزایش pH',
    idealRange: { min: 150, max: 250, unit: 'ppm' },
    sources: ['نیترات کلسیم', 'کلرید کلسیم', 'سولفات کلسیم'],
    notes: 'کلسیم در آوند چوبی حرکت می‌کند و به سختی در گیاه جابه‌جا می‌شود.',
    category: 'macro',
    mobility: 'immobile'
  },
  'Mg': {
    name: 'منیزیم',
    symbol: 'Mg',
    role: 'ساخت کلروفیل، فعال‌سازی آنزیم‌ها، فتوسنتز و متابولیسم کربوهیدرات',
    deficiency: 'کلروز بین رگبرگی برگ‌های پیر، افتادگی برگ‌ها',
    toxicity: 'کمبود کلسیم و پتاسیم',
    idealRange: { min: 40, max: 60, unit: 'ppm' },
    sources: ['سولفات منیزیم', 'نیترات منیزیم', 'کلرید منیزیم'],
    notes: 'منیزیم هسته مرکزی کلروفیل است. نسبت کلسیم به منیزیم باید ۳:۱ تا ۵:۱ باشد.',
    category: 'macro',
    mobility: 'mobile'
  },
  'S': {
    name: 'گوگرد',
    symbol: 'S',
    role: 'ساخت پروتئین و اسیدهای آمینه، کلروفیل، متابولیسم نیتروژن',
    deficiency: 'کلروز عمومی برگ‌های جوان، زردی مشابه نیتروژن',
    toxicity: 'کاهش جذب نیتروژن',
    idealRange: { min: 50, max: 80, unit: 'ppm' },
    sources: ['سولفات پتاسیم', 'سولفات منیزیم', 'سولفات آمونیوم'],
    notes: 'گوگرد با کاهش pH محلول، جذب عناصر را افزایش می‌دهد.',
    category: 'macro',
    mobility: 'immobile'
  },
  'Fe': {
    name: 'آهن',
    symbol: 'Fe',
    role: 'ساخت کلروفیل، تنفس سلولی، فتوسنتز و متابولیسم نیتروژن',
    deficiency: 'کلروز بین رگبرگی برگ‌های جوان، زردی شدید',
    toxicity: 'سمیت آهن باعث نکروز و لکه‌های قهوه‌ای روی برگ‌ها می‌شود',
    idealRange: { min: 2, max: 5, unit: 'ppm' },
    sources: ['کلات آهن (Fe-EDTA)', 'کلات آهن (Fe-DTPA)', 'سولفات آهن'],
    notes: 'جذب آهن در pH پایین (کمتر از ۶.۵) بهتر است. با فسفر واکنش داده و رسوب می‌کند.',
    category: 'micro',
    mobility: 'immobile'
  },
  'Mn': {
    name: 'منگنز',
    symbol: 'Mn',
    role: 'فتوسنتز، تنفس، فعال‌سازی آنزیم‌ها و متابولیسم نیتروژن',
    deficiency: 'کلروز بین رگبرگی برگ‌های جوان، لکه‌های نکروتیک',
    toxicity: 'لکه‌های قهوه‌ای روی برگ‌ها، کاهش رشد',
    idealRange: { min: 0.5, max: 1.5, unit: 'ppm' },
    sources: ['کلات منگنز', 'سولفات منگنز', 'کلات منگنز (Mn-EDTA)'],
    notes: 'منگنز در pH بالا (بیشتر از ۶.۵) جذب نمی‌شود. با آهن تداخل دارد.',
    category: 'micro',
    mobility: 'immobile'
  },
  'Zn': {
    name: 'روی',
    symbol: 'Zn',
    role: 'ساخت هورمون‌های رشد، فعال‌سازی آنزیم‌ها، متابولیسم کربوهیدرات',
    deficiency: 'کوچکی برگ‌ها، روزت، کلروز بین رگبرگی',
    toxicity: 'کمبود آهن و منگنز، نکروز برگ‌ها',
    idealRange: { min: 0.05, max: 0.15, unit: 'ppm' },
    sources: ['کلات روی', 'سولفات روی', 'کلات روی (Zn-EDTA)'],
    notes: 'روی در pH بالا جذب نمی‌شود. با فسفر واکنش داده و رسوب می‌کند.',
    category: 'micro',
    mobility: 'immobile'
  },
  'B': {
    name: 'بُر',
    symbol: 'B',
    role: 'تشکیل دیواره سلولی، تقسیم سلولی، انتقال قندها و گرده‌افشانی',
    deficiency: 'نکروز نوک برگ و ساقه، ریزش جوانه‌ها، میوه‌های بدشکل',
    toxicity: 'نکروز حاشیه برگ‌ها، زردی و ریزش برگ‌ها',
    idealRange: { min: 0.2, max: 0.5, unit: 'ppm' },
    sources: ['بوریک اسید', 'بورات سدیم', 'کلات بور'],
    notes: 'بُر در آوند آبکش حرکت می‌کند. دامنه سمیت و کمبود آن بسیار نزدیک است.',
    category: 'micro',
    mobility: 'immobile'
  },
  'Cu': {
    name: 'مس',
    symbol: 'Cu',
    role: 'فتوسنتز، تنفس، فعال‌سازی آنزیم‌ها، مقاومت به بیماری‌ها',
    deficiency: 'پژمردگی برگ‌های جوان، کلروز، کاهش رشد',
    toxicity: 'نکروز ریشه، کاهش رشد، لکه‌های قهوه‌ای روی برگ‌ها',
    idealRange: { min: 0.05, max: 0.1, unit: 'ppm' },
    sources: ['کلات مس', 'سولفات مس', 'اکسی کلرید مس'],
    notes: 'مس با آهن و روی تداخل دارد. در pH بالا جذب نمی‌شود.',
    category: 'micro',
    mobility: 'immobile'
  },
  'Mo': {
    name: 'مولیبدن',
    symbol: 'Mo',
    role: 'متابولیسم نیتروژن، آنزیم نیترات ردوکتاز، تثبیت نیتروژن',
    deficiency: 'کلروز بین رگبرگی، سوختگی حاشیه برگ‌ها، شبیه کمبود نیتروژن',
    toxicity: 'زردی برگ‌ها، کاهش رشد (نادر است)',
    idealRange: { min: 0.01, max: 0.05, unit: 'ppm' },
    sources: ['مولیبدات آمونیوم', 'مولیبدات سدیم'],
    notes: 'مولیبدن تنها عنصری است که در pH بالا (۷-۸) جذب بهتری دارد.',
    category: 'micro',
    mobility: 'mobile'
  },
  'Na': {
    name: 'سدیم',
    symbol: 'Na',
    role: 'تنظیم فشار اسمزی، بهبود طعم میوه (مقدار کم)',
    deficiency: 'نادر است (در گیاهان حساس به نمک رخ نمی‌دهد)',
    toxicity: 'نکروز برگ‌ها، کاهش رشد، مسمومیت نمک',
    idealRange: { min: 0, max: 50, unit: 'ppm' },
    sources: ['کلرید سدیم', 'نیترات سدیم', 'بیکربنات سدیم'],
    notes: 'سدیم در آب آبیاری و کودها وجود دارد. در گیاهان C4 مفید است اما در بیشتر گیاهان مضر است.',
    category: 'neutral',
    mobility: 'mobile'
  },
  'Cl': {
    name: 'کلر',
    symbol: 'Cl',
    role: 'فتوسنتز، تنظیم فشار اسمزی، فعال‌سازی آنزیم‌ها (مقدار کم)',
    deficiency: 'پژمردگی برگ‌ها، کاهش رشد، لکه‌های برنزی',
    toxicity: 'سوختگی حاشیه و نوک برگ‌ها، کاهش رشد',
    idealRange: { min: 0, max: 50, unit: 'ppm' },
    sources: ['کلرید پتاسیم', 'کلرید کلسیم', 'کلرید سدیم'],
    notes: 'کلر در آب و کودها به وفور یافت می‌شود. حساسیت به کلر در محصولاتی مانند انگور و مرکبات بالاست.',
    category: 'neutral',
    mobility: 'mobile'
  }
};

// ============================================================
// ✅ توابع رنگ‌آمیزی
// ============================================================

const CATION_ELEMENTS = ['N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Fe', 'Mn', 'Zn', 'Cu'];
const ANION_ELEMENTS = ['N-NO3', 'P', 'S', 'Cl', 'B', 'Mo'];

const getElementType = (element: string): 'cation' | 'anion' | 'neutral' => {
  if (CATION_ELEMENTS.includes(element)) return 'cation';
  if (ANION_ELEMENTS.includes(element)) return 'anion';
  return 'neutral';
};

const getElementHeaderClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300';
    case 'anion':
      return 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300';
    default:
      return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400';
  }
};

const getElementCellClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-50/30 dark:bg-blue-900/5';
    case 'anion':
      return 'bg-red-50/30 dark:bg-red-900/5';
    default:
      return '';
  }
};

const getElementTabClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-blue-50 dark:hover:bg-blue-900/20';
    case 'anion':
      return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-red-50 dark:hover:bg-red-900/20';
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600';
  }
};

const getElementActiveTabClass = (element: string): string => {
  const type = getElementType(element);
  switch (type) {
    case 'cation':
      return 'bg-blue-500 text-white shadow-sm';
    case 'anion':
      return 'bg-red-500 text-white shadow-sm';
    default:
      return 'bg-gray-500 text-white shadow-sm';
  }
};

const getElementSymbol = (element: string): string => {
  const data = ELEMENTS_DATA[element];
  return data?.symbol || element;
};

const getCategoryClass = (category: string): string => {
  return category === 'macro' 
    ? 'text-purple-600 dark:text-purple-400 font-medium' 
    : 'text-orange-600 dark:text-orange-400 font-medium';
};

const getMobilityClass = (mobility: string): string => {
  return mobility === 'mobile'
    ? 'text-green-600 dark:text-green-400'
    : 'text-yellow-600 dark:text-yellow-400';
};

// ===== Computed =====
const selectedElementData = computed(() => {
  return ELEMENTS_DATA[props.selectedElement] || null;
});

const getConvertedValue = (element: string, unit: string): string => {
  if (!props.convertedValues || !props.convertedValues[element]) {
    return '0.00';
  }
  const value = props.convertedValues[element][unit];
  if (value === undefined || value === null) {
    return '0.00';
  }
  return value.toFixed(3);
};

// ===== Methods =====
const selectElement = (element: string) => {
  emit('update:selectedElement', element);
  emit('openGuide', element);
};

// ===== Watch =====
watch(() => props.selectedElement, (newVal) => {
  if (newVal && !ELEMENTS_DATA[newVal]) {
    emit('update:selectedElement', props.elements[0]);
  }
}, { immediate: true });
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* اسکرول بار جدول */
.custom-scrollbar::-webkit-scrollbar {
  height: 4px;
  width: 4px;
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

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

/* اسکرول بار نازک برای تب‌ها */
.custom-scrollbar-tabs {
  scrollbar-width: thin;
  scrollbar-color: #c1c1c1 transparent;
}

.custom-scrollbar-tabs::-webkit-scrollbar {
  height: 3px;
}

.custom-scrollbar-tabs::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
}

.custom-scrollbar-tabs::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar-tabs::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.dark .custom-scrollbar-tabs::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .custom-scrollbar-tabs::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

.max-h-0 {
  max-height: 0;
}
.max-h-\[3000px\] {
  max-height: 3000px;
}

/* بهبود نمایش در موبایل */
@media (max-width: 640px) {
  .custom-scrollbar::-webkit-scrollbar {
    height: 3px;
  }
  
  .custom-scrollbar-tabs::-webkit-scrollbar {
    height: 2px;
  }
}
</style>