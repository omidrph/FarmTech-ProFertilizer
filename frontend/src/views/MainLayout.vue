<!-- frontend/src/views/MainLayout.vue -->
<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200 flex flex-col">
    
    <!-- Header -->
    <AppHeader 
      v-model:activeTab="activeTab" 
      @new-report="handleNewReport"
    />

    <!-- Sub Navigation (تب‌های صفحه اصلی) - استایل کاملاً یکسان با هدر -->
    <nav v-if="activeTab === 'home'" class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky z-40" :style="{ top: headerHeight + 'px' }">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex items-center gap-1 overflow-x-auto py-1 scrollbar-hide snap-x snap-mandatory">
          <button
            v-for="subTab in subTabs"
            :key="subTab.id"
            @click="activeSubTab = subTab.id"
            class="relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all duration-200 text-sm group whitespace-nowrap snap-start flex-shrink-0"
            :class="activeSubTab === subTab.id
              ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20' 
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            <span class="relative z-10 flex items-center gap-1.5">
              <span v-html="subTab.icon" class="w-4 h-4 flex-shrink-0"></span>
              <span class="text-sm">{{ subTab.label }}</span>
            </span>
            <span v-if="activeSubTab === subTab.id" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-0.5 bg-primary-600 dark:bg-primary-400 rounded-full transition-all duration-300"></span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Sub Navigation برای تب Education - استایل کاملاً یکسان با هدر -->
    <nav v-if="activeTab === 'education'" class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky z-40" :style="{ top: headerHeight + 'px' }">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
        <div class="flex items-center gap-1 overflow-x-auto py-1 scrollbar-hide snap-x snap-mandatory">
          <button
            v-for="subTab in educationSubTabs"
            :key="subTab.id"
            @click="activeEducationSubTab = subTab.id"
            class="relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all duration-200 text-sm group whitespace-nowrap snap-start flex-shrink-0"
            :class="activeEducationSubTab === subTab.id
              ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20' 
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            <span class="relative z-10 flex items-center gap-1.5">
              <span v-html="subTab.icon" class="w-4 h-4 flex-shrink-0"></span>
              <span class="text-sm">{{ subTab.label }}</span>
            </span>
            <span v-if="activeEducationSubTab === subTab.id" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-0.5 bg-primary-600 dark:bg-primary-400 rounded-full transition-all duration-300"></span>
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
        <div v-if="activeSubTab === 'home'" :key="homeTabKey">
          <HomeTab :target-unit="targetStore.targetUnit" />
        </div>

        <!-- Water Analysis Sub Tab -->
        <div v-else-if="activeSubTab === 'water-analysis'" :key="waterTabKey">
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
        <div v-else-if="activeSubTab === 'target-elements'" :key="targetTabKey">
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

        <!-- Interpretation Sub Tab -->
        <div v-else-if="activeSubTab === 'interpretation'">
          <InterpretationTab
            v-model:interpretationResult="interpretationResult"
            @generate="generateInterpretation"
          />
        </div>

        <!-- Fertilizer DB Sub Tab -->
        <div v-else-if="activeSubTab === 'fertilizer-db'">
          <FertilizerDBTab
            v-model:fertilizers="fertilizerStore.fertilizers"
            @delete-fertilizer="handleDeleteFertilizer"
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

    <!-- Profile Modal -->
    <ProfileModal
      :is-open="isProfileModalOpen"
      @update:is-open="isProfileModalOpen = $event"
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
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { useFertilizerStore } from '@/store/modules/fertilizerStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { useAppStore } from '@/store/modules/appStore';
import { useApi } from '@/composables/useApi';
import { useCalculations } from '@/composables/useCalculations';

// Layout Components
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import ProfileModal from '@/components/layout/ProfileModal.vue';

// Feature Components
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
const { isLoading, error: apiError, checkConnection, clearError } = useApi();
const { generateInterpretation: generateInterpretationFromAPI } = useCalculations();

// ===== State =====
const activeTab = ref('home');
const activeSubTab = ref('home');
const activeEducationSubTab = ref('quick-start');
const isProfileModalOpen = ref(false);
const headerHeight = ref(56);
const analysisUnit = ref('ppm');
const interpretationResult = ref<any>(null);
const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

// ===== کلیدهای رندر مجدد اجباری برای کامپوننت‌ها =====
const homeTabKey = ref(0);
const waterTabKey = ref(0);
const targetTabKey = ref(0);

// ============================================================
// Navigation Tabs - کاملاً هماهنگ با هدر اصلی (استایل یکسان)
// ============================================================
const subTabs = [
  {
    id: 'home',
    label: 'خانه',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`
  },
  {
    id: 'water-analysis',
    label: 'آنالیز آب',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>`
  },
  {
    id: 'target-elements',
    label: 'عناصر هدف',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`
  },
  {
    id: 'fertilizer-calc',
    label: 'محاسبه کود',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/></svg>`
  },
  {
    id: 'interpretation',
    label: 'تفسیر داده‌ها',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`
  },
  {
    id: 'fertilizer-db',
    label: 'پایگاه داده کودها',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>`
  }
];

const educationSubTabs = [
  {
    id: 'quick-start',
    label: 'شروع سریع',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`
  },
  {
    id: 'videos',
    label: 'فیلم‌های آموزشی',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>`
  },
  {
    id: 'faq',
    label: 'سوالات متداول',
    icon: `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
  }
];

// ============================================================
// Toast Function
// ============================================================
const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = null;
  }, 3000);
};

// ============================================================
// Methods
// ============================================================
const loadData = async () => {
  const connected = await checkConnection();
  if (!connected) {
    console.warn('بک‌اند در دسترس نیست!');
    return;
  }
  await fertilizerStore.loadFertilizers();
};

const handleDeleteFertilizer = async (id: string) => {
  if (confirm('آیا از حذف این کود اطمینان دارید؟')) {
    await fertilizerStore.deleteFertilizer(id);
  }
};

const handleNewReport = async () => {
  console.log('📄 Creating new report...');
  
  reportStore.createNewReport();
  activeSubTab.value = 'home';
  
  homeTabKey.value++;
  waterTabKey.value++;
  targetTabKey.value++;
  
  await nextTick();
  showToast('گزارش جدید ایجاد شد', 'success');
};

const generateInterpretation = async () => {
  if (!calcStore.currentReportId) {
    alert('لطفاً ابتدا محاسبات را در بخش "محاسبه کود" ذخیره کنید');
    return;
  }
  const result = await generateInterpretationFromAPI(calcStore.currentReportId);
  if (result) {
    interpretationResult.value = result;
  } else {
    alert('خطا در تولید تفسیر');
  }
};

const clearErrors = () => {
  clearError();
  fertilizerStore.clearError();
  calcStore.clearErrors();
};

const updateHeaderHeight = () => {
  const header = document.querySelector('header');
  if (header) {
    headerHeight.value = header.offsetHeight;
  }
};

// ============================================================
// Event Listener for Profile Modal
// ============================================================
const openProfileModalHandler = () => {
  isProfileModalOpen.value = true;
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(async () => {
  updateHeaderHeight();
  window.addEventListener('resize', updateHeaderHeight);
  window.addEventListener('open-profile-modal', openProfileModalHandler);
  await loadData();
});

onUnmounted(() => {
  window.removeEventListener('resize', updateHeaderHeight);
  window.removeEventListener('open-profile-modal', openProfileModalHandler);
});
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

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