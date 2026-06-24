<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200 flex flex-col">
    <!-- Header -->
    <AppHeader v-model:activeTab="activeTab" />

    <!-- Sub Navigation (تب‌های صفحه اصلی) -->
    <nav v-if="activeTab === 'home'" class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky z-40 shadow-sm" :style="{ top: headerHeight + 'px' }">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex gap-1 overflow-x-auto py-2 scrollbar-hide snap-x snap-mandatory">
          <button
            v-for="subTab in subTabs"
            :key="subTab.id"
            @click="activeSubTab = subTab.id"
            class="flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium whitespace-nowrap transition-all duration-200 snap-start flex-shrink-0"
            :class="activeSubTab === subTab.id
              ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
          >
            <span v-html="subTab.icon" class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0"></span>
            <span class="text-xs sm:text-sm">{{ subTab.label }}</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Sub Navigation برای تب Education -->
    <nav v-if="activeTab === 'education'" class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky z-40 shadow-sm" :style="{ top: headerHeight + 'px' }">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex gap-1 overflow-x-auto py-2 scrollbar-hide snap-x snap-mandatory">
          <button
            v-for="subTab in educationSubTabs"
            :key="subTab.id"
            @click="activeEducationSubTab = subTab.id"
            class="flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium whitespace-nowrap transition-all duration-200 snap-start flex-shrink-0"
            :class="activeEducationSubTab === subTab.id
              ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'"
          >
            <span v-html="subTab.icon" class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0"></span>
            <span class="text-xs sm:text-sm">{{ subTab.label }}</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-6 w-full">
      <!-- Loading Indicator -->
      <div v-if="isLoading || fertilizerStore.isLoading || calcStore.isLoading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span class="mr-2 text-gray-600 dark:text-gray-400">در حال بارگذاری...</span>
      </div>

      <!-- Error Message -->
      <div v-if="apiError || fertilizerStore.error || calcStore.errorMessages.length > 0" class="bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-4 mb-4">
        <p class="text-danger-700 dark:text-danger-400 text-sm">
          {{ apiError || fertilizerStore.error || calcStore.errorMessages.join(', ') }}
        </p>
        <button @click="clearErrors" class="text-sm text-danger-600 hover:text-danger-800 mt-1">بستن</button>
      </div>

      <!-- Home Tab -->
      <div v-if="activeTab === 'home'" class="space-y-4 sm:space-y-6">
        <!-- Report Header -->
        <ReportHeader
          v-model:reportName="reportStore.reportData.reportName"
          v-model:plantName="reportStore.reportData.plantName"
          v-model:season="reportStore.reportData.season"
          v-model:growthStage="reportStore.reportData.growthStage"
          v-model:reportDate="reportStore.reportData.date"
        />

        <!-- Home Sub Tab -->
        <div v-if="activeSubTab === 'home'">
          <HomeTab
            :target-unit="targetStore.targetUnit"
          />
        </div>

        <!-- Water Analysis Sub Tab -->
        <div v-else-if="activeSubTab === 'water-analysis'">
          <WaterAnalysisTab
            v-model:waterPercentage="waterStore.waterMixData.waterPercentage"
            v-model:wastewaterPercentage="waterStore.waterMixData.wastewaterPercentage"
            v-model:waterSalinity="waterStore.waterMixData.waterSalinity"
            v-model:analysisUnit="analysisUnit"
            v-model:wastewaterValues="waterStore.wastewaterValues"
            v-model:waterValues="waterStore.waterValues"
          />
        </div>

        <!-- Target Elements Sub Tab -->
        <div v-else-if="activeSubTab === 'target-elements'">
          <TargetElementsTab
            v-model:targetUnit="targetStore.targetUnit"
            v-model:targetValues="targetStore.targetElements"
          />
        </div>

        <!-- Fertilizer Calc Sub Tab -->
        <div v-else-if="activeSubTab === 'fertilizer-calc'">
          <FertilizerCalcTab
            :fertilizers="fertilizerStore.fertilizers"
            v-model:selectedFertilizers="fertilizerStore.selectedFertilizerIds"
            v-model:tankVolume="calcStore.calculationInputs.tankVolume"
            v-model:dilutionFactor="calcStore.calculationInputs.dilutionFactor"
            v-model:calcRows="calcStore.calculationRows"
            v-model:calcErrors="calcStore.errorMessages"
          />
        </div>

        <!-- Fertilizer DB Sub Tab -->
        <div v-else-if="activeSubTab === 'fertilizer-db'">
          <FertilizerDBTab
            v-model:fertilizers="fertilizerStore.fertilizers"
            @show-add-modal="showAddFertilizerModal = true"
            @delete-fertilizer="handleDeleteFertilizer"
          />
        </div>

        <!-- Interpretation Sub Tab -->
        <div v-else-if="activeSubTab === 'interpretation'">
          <InterpretationTab
            v-model:interpretationResult="interpretationResult"
            @generate="generateInterpretation"
          />
        </div>
      </div>

      <!-- Education Tab -->
      <div v-else-if="activeTab === 'education'" class="space-y-4 sm:space-y-6">
        <div v-if="activeEducationSubTab === 'quick-start'">
          <EducationQuickStart />
        </div>
        <div v-else-if="activeEducationSubTab === 'faq'">
          <EducationFAQ />
        </div>
        <div v-else-if="activeEducationSubTab === 'videos'">
          <EducationVideos />
        </div>
      </div>

      <!-- Contact Tab -->
      <div v-else-if="activeTab === 'contact'">
        <ContactUs />
      </div>

      <!-- About Tab -->
      <div v-else-if="activeTab === 'about'">
        <AboutUs />
      </div>
    </main>

    <!-- Footer -->
    <AppFooter @navigate="activeTab = $event" />

    <!-- Modal Add Fertilizer -->
    <div v-if="showAddFertilizerModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="showAddFertilizerModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto p-4 sm:p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">افزودن کود جدید</h3>
          <button @click="showAddFertilizerModal = false" class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام کود</label>
            <input type="text" v-model="newFertilizer.name" placeholder="مثال: نیترات پتاسیم" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">قیمت هر کیلوگرم (تومان)</label>
            <input type="number" v-model="newFertilizer.pricePerKg" placeholder="مثال: ۲۵۰۰۰" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">درصد عناصر</label>
            <div class="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
              <div v-for="el in elements" :key="el" class="flex items-center gap-2">
                <label class="text-xs font-medium text-gray-600 dark:text-gray-400 w-12">{{ el }}</label>
                <input type="number" v-model="newFertilizer.elements[el]" step="0.01" placeholder="۰" class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
              </div>
            </div>
          </div>
          <div>
            <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
              <input type="checkbox" v-model="newFertilizer.isAcid" class="rounded border-gray-300 dark:border-gray-600" />
              کود اسیدی است
            </label>
          </div>
          <div v-if="newFertilizer.isAcid">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نوع اسید</label>
            <select v-model="newFertilizer.acidType" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all">
              <option value="">انتخاب کنید...</option>
              <option value="H3PO4">H3PO4</option>
              <option value="HNO3">HNO3</option>
              <option value="H2SO4">H2SO4</option>
            </select>
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button @click="handleAddFertilizer" :disabled="fertilizerStore.isLoading" class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50">
            {{ fertilizerStore.isLoading ? 'در حال ذخیره...' : 'ذخیره' }}
          </button>
          <button @click="showAddFertilizerModal = false" class="flex-1 px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
            انصراف
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, reactive } from 'vue';

// ===== Store Imports =====
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { useAppStore } from '@/store/modules/appStore';

// ===== Composables =====
import { useApi } from '@/composables/useApi';

// ===== Import Components =====
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import ReportHeader from '@/components/features/ReportHeader.vue';
import HomeTab from '@/components/features/HomeTab.vue';
import WaterAnalysisTab from '@/components/features/WaterAnalysisTab.vue';
import TargetElementsTab from '@/components/features/TargetElementsTab.vue';
import FertilizerCalcTab from '@/components/features/FertilizerCalcTab.vue';
import FertilizerDBTab from '@/components/features/FertilizerDBTab.vue';
import InterpretationTab from '@/components/features/InterpretationTab.vue';
import EducationQuickStart from '@/components/features/EducationQuickStart.vue';
import EducationFAQ from '@/components/features/EducationFAQ.vue';
import EducationVideos from '@/components/features/EducationVideos.vue';
import ContactUs from '@/components/features/ContactUs.vue';
import AboutUs from '@/components/features/AboutUs.vue';

// ===== Stores =====
const reportStore = useReportStore();
const targetStore = useTargetStore();
const waterStore = useWaterStore();
const fertilizerStore = useFertilizerStore();
const calcStore = useCalcStore();
const appStore = useAppStore();

// ===== API =====
const { isLoading, error: apiError, checkConnection, clearError } = useApi();

// ===== State =====
const activeTab = ref('home');
const activeSubTab = ref('home');
const activeEducationSubTab = ref('quick-start');
const showAddFertilizerModal = ref(false);
const headerHeight = ref(56);
const analysisUnit = ref('ppm');
const interpretationResult = ref<any>(null);
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== New Fertilizer =====
const newFertilizer = reactive({
  name: '',
  pricePerKg: 0,
  elements: {} as Record<string, number>,
  isAcid: false,
  acidType: '' as string
});

// ===== Sub Tabs =====
const subTabs = [
  {
    id: 'home',
    label: 'خانه',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`
  },
  {
    id: 'water-analysis',
    label: 'آنالیز آب',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>`
  },
  {
    id: 'target-elements',
    label: 'عناصر هدف',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`
  },
  {
    id: 'fertilizer-calc',
    label: 'محاسبه کود',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/></svg>`
  },
  {
    id: 'fertilizer-db',
    label: 'پایگاه داده کودها',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>`
  },
  {
    id: 'interpretation',
    label: 'تفسیر داده‌ها',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`
  }
];

// ===== Education Sub Tabs =====
const educationSubTabs = [
  {
    id: 'quick-start',
    label: 'شروع سریع',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`
  },
  {
    id: 'videos',
    label: 'فیلم‌های آموزشی',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>`
  },
  {
    id: 'faq',
    label: 'سوالات متداول',
    icon: `<svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
  }
];

// ===== Methods =====

// بارگذاری داده‌ها از بک‌اند
const loadData = async () => {
  // بررسی اتصال به بک‌اند
  const connected = await checkConnection();
  
  if (!connected) {
    console.warn('⚠️ بک‌اند در دسترس نیست! لطفاً بک‌اند را اجرا کنید.');
    return;
  }
  
  // بارگذاری کودها از بک‌اند
  await fertilizerStore.loadFertilizers();
  
  if (fertilizerStore.fertilizers.length === 0) {
    console.info('ℹ️ هیچ کودی در دیتابیس وجود ندارد. لطفاً از طریق دکمه "افزودن کود جدید" کود اضافه کنید.');
  }
};

// افزودن کود جدید
const handleAddFertilizer = async () => {
  if (!newFertilizer.name || !newFertilizer.pricePerKg) {
    alert('لطفاً نام و قیمت کود را وارد کنید');
    return;
  }
  
  const success = await fertilizerStore.addFertilizer(newFertilizer);
  if (success) {
    showAddFertilizerModal.value = false;
    newFertilizer.name = '';
    newFertilizer.pricePerKg = 0;
    newFertilizer.elements = {};
    newFertilizer.isAcid = false;
    newFertilizer.acidType = '';
    alert('کود با موفقیت افزوده شد');
  } else {
    alert(fertilizerStore.error || 'خطا در افزودن کود');
  }
};

// حذف کود
const handleDeleteFertilizer = async (id: string) => {
  if (confirm('آیا از حذف این کود اطمینان دارید؟')) {
    await fertilizerStore.deleteFertilizer(id);
  }
};

// تولید تفسیر
const generateInterpretation = () => {
  const targetVals = targetStore.targetElements;
  const finalVals = calcStore.elementTotals;
  const waterData = waterStore.waterMixData;
  
  let cation = 0;
  let anion = 0;
  const cations = ['K', 'Ca', 'Mg', 'Na'];
  const anions = ['N-NO3', 'P', 'S', 'N-NH4', 'Cl'];
  
  for (const [key, val] of Object.entries(targetVals)) {
    if (cations.includes(key)) cation += val || 0;
    else if (anions.includes(key)) anion += val || 0;
  }
  
  const isBalanced = Math.abs(cation - anion) < 0.5;
  
  const elementStatus = elements.map(el => {
    const target = (targetVals as any)[el] || 0;
    const actual = (finalVals as any)[el] || 0;
    const diff = target - actual;
    
    let status: 'deficient' | 'sufficient' | 'excessive' | 'toxic' = 'sufficient';
    let message = 'وضعیت مطلوب';
    
    if (diff > 5) {
      status = 'deficient';
      message = `کمبود ${diff.toFixed(2)} واحد`;
    } else if (diff < -5) {
      status = 'excessive';
      message = `بیش‌بود ${Math.abs(diff).toFixed(2)} واحد`;
    } else if (diff < -15) {
      status = 'toxic';
      message = 'سمیت احتمالی';
    }
    
    return {
      element: el as any,
      target,
      actual,
      difference: diff,
      status,
      message
    };
  });
  
  const salinity = waterData.waterSalinity || 0;
  let impact = 'مناسب';
  let recommendation = 'نیازی به اقدام نیست';
  
  if (salinity > 2.5) {
    impact = 'بالا';
    recommendation = 'استفاده از آب با شوری کمتر توصیه می‌شود';
  } else if (salinity > 1.5) {
    impact = 'متوسط';
    recommendation = 'توجه به عناصر سمی در آب';
  }
  
  const recommendations: any[] = [];
  
  if (!isBalanced) {
    recommendations.push({
      issue: 'عدم تعادل یونی',
      suggestion: 'مقادیر کاتیون و آنیون را تنظیم کنید تا برابر شوند',
      priority: 'high'
    });
  }
  
  for (const item of elementStatus) {
    if (item.status === 'deficient' || item.status === 'toxic') {
      recommendations.push({
        issue: `عنصر ${item.element}: ${item.message}`,
        suggestion: item.status === 'deficient' 
          ? 'افزایش مقدار این عنصر در فرمول غذایی' 
          : 'کاهش مقدار این عنصر یا بررسی کیفیت آب',
        priority: item.status === 'toxic' ? 'high' : 'medium'
      });
    }
  }
  
  const problemElements = elementStatus.filter(e => e.status !== 'sufficient').map(e => e.element);
  
  interpretationResult.value = {
    summary: `گزارش تفسیر تغذیه گیاه:\n- تعادل یونی: ${isBalanced ? 'برقرار ✅' : 'نامتعادل ⚠️'}\n- عناصر دارای مشکل: ${problemElements.length ? problemElements.join(', ') : 'هیچکدام'}\n- کیفیت آب: ${impact}\n- تعداد توصیه‌ها: ${recommendations.length}`,
    ionBalance: {
      cation,
      anion,
      isBalanced,
      message: isBalanced ? 'تعادل یونی برقرار است' : 'تعادل یونی برقرار نیست'
    },
    elementStatus,
    waterQuality: {
      salinity,
      impact,
      recommendation
    },
    fertilizerRecommendation: recommendations
  };
};

// پاک کردن خطاها
const clearErrors = () => {
  clearError();
  fertilizerStore.clearError();
  calcStore.clearErrors();
};

// ===== Lifecycle =====
const updateHeaderHeight = () => {
  const header = document.querySelector('header');
  if (header) {
    headerHeight.value = header.offsetHeight;
  }
};

onMounted(async () => {
  updateHeaderHeight();
  window.addEventListener('resize', updateHeaderHeight);
  await loadData();
});

onUnmounted(() => {
  window.removeEventListener('resize', updateHeaderHeight);
});
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

.snap-x {
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.snap-start {
  scroll-snap-align: start;
}
</style>