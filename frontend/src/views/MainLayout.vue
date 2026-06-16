<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors duration-200">
    <!-- Header -->
    <AppHeader v-model:activeTab="activeTab" />

    <!-- Sub Navigation (تب‌های صفحه اصلی) -->
    <nav v-if="activeTab === 'home'" class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky top-16 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex gap-1 overflow-x-auto py-2">
          <button
            v-for="subTab in subTabs"
            :key="subTab.id"
            @click="activeSubTab = subTab.id"
            class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all duration-200"
            :class="activeSubTab === subTab.id
              ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 border-b-2 border-primary-500'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            <span v-html="subTab.icon"></span>
            {{ subTab.label }}
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Home Tab -->
      <div v-if="activeTab === 'home'" class="space-y-6">
        <!-- Report Header -->
        <ReportHeader
          v-model:reportName="reportName"
          v-model:plantName="plantName"
          v-model:season="season"
          v-model:growthStage="growthStage"
          v-model:reportDate="reportDate"
        />

        <!-- Home Sub Tab -->
        <div v-if="activeSubTab === 'home'">
          <HomeTab
            v-model:targetUnit="targetUnit"
            v-model:targetValues="targetValues"
            v-model:finalValues="finalValues"
            v-model:reservoirData="reservoirData"
          />
        </div>

        <!-- Water Analysis Sub Tab -->
        <div v-else-if="activeSubTab === 'water-analysis'">
          <WaterAnalysisTab
            v-model:waterPercentage="waterPercentage"
            v-model:wastewaterPercentage="wastewaterPercentage"
            v-model:waterSalinity="waterSalinity"
            v-model:analysisUnit="analysisUnit"
            v-model:wastewaterValues="wastewaterValues"
            v-model:waterValues="waterValues"
          />
        </div>

        <!-- Target Elements Sub Tab -->
        <div v-else-if="activeSubTab === 'target-elements'">
          <TargetElementsTab
            v-model:targetUnit="targetUnit"
            v-model:targetValues="targetValues"
          />
        </div>

        <!-- Fertilizer Calc Sub Tab -->
        <div v-else-if="activeSubTab === 'fertilizer-calc'">
          <FertilizerCalcTab
            :fertilizers="fertilizers"
            v-model:selectedFertilizers="selectedFertilizers"
            v-model:tankVolume="tankVolume"
            v-model:dilutionFactor="dilutionFactor"
            v-model:calcRows="calcRows"
            v-model:calcErrors="calcErrors"
          />
        </div>

        <!-- Fertilizer DB Sub Tab -->
        <div v-else-if="activeSubTab === 'fertilizer-db'">
          <FertilizerDBTab
            v-model:fertilizers="fertilizers"
            @show-add-modal="showAddFertilizerModal = true"
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
      <div v-else-if="activeTab === 'education'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">📚 آموزش</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 hover:shadow-md transition-shadow">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">راهنمای شروع سریع</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">با این راهنما در کمتر از 5 دقیقه با نرم‌افزار آشنا شوید.</p>
            <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
              مشاهده
            </button>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 hover:shadow-md transition-shadow">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">فیلم‌های آموزشی</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">مجموعه کامل فیلم‌های آموزشی برای تمام بخش‌ها.</p>
            <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
              مشاهده
            </button>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 hover:shadow-md transition-shadow">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">سوالات متداول</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">پاسخ به سوالات رایج کاربران.</p>
            <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
              مشاهده
            </button>
          </div>
        </div>
      </div>

      <!-- Contact Tab -->
      <div v-else-if="activeTab === 'contact'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">📧 ارتباط با ما</h2>
        <div class="space-y-3">
          <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
            <span class="text-2xl">📞</span>
            <span>تلفن: ۰۲۱-۱۲۳۴۵۶۷۸</span>
          </div>
          <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
            <span class="text-2xl">📧</span>
            <span>ایمیل: info@farmtech.ir</span>
          </div>
          <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
            <span class="text-2xl">📍</span>
            <span>آدرس: تهران، خیابان انقلاب، پلاک ۱۲۳</span>
          </div>
        </div>
      </div>

      <!-- About Tab -->
      <div v-else-if="activeTab === 'about'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">ℹ️ درباره</h2>
        <div class="space-y-4 text-gray-700 dark:text-gray-300 leading-relaxed">
          <p><strong>تغذیه سبز</strong> یک نرم‌افزار تخصصی برای محاسبه، تحلیل و مدیریت فرمول‌های تغذیه گیاهان در سیستم‌های کشت بدون خاک، هیدروپونیک و گلخانه‌ای است.</p>
          <p>این نرم‌افزار قابلیت تحلیل آب و پساب، تعیین عناصر هدف، محاسبه خودکار مقدار کود مصرفی، مدیریت پایگاه داده کودها و ارائه تفسیر هوشمند از داده‌ها را دارد.</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">نسخه: ۰.۱.۰</p>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <AppFooter @navigate="activeTab = $event" />

    <!-- Modal Add Fertilizer -->
    <div v-if="showAddFertilizerModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto p-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">افزودن کود جدید</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">نام کود</label>
            <input type="text" v-model="newFertilizer.name" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">قیمت هر کیلوگرم (تومان)</label>
            <input type="number" v-model="newFertilizer.pricePerKg" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
          </div>
          <div v-for="el in elements" :key="el" class="grid grid-cols-2 gap-2">
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ el }} (%)</label>
            <input type="number" v-model="newFertilizer.elements[el]" step="0.01" class="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button @click="saveFertilizer" class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
            ذخیره
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
import { ref, reactive, onMounted } from 'vue';

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

// ===== State =====
const activeTab = ref('home');
const activeSubTab = ref('home');
const showAddFertilizerModal = ref(false);

// ===== Report Fields =====
const reportName = ref('');
const plantName = ref('');
const season = ref('');
const growthStage = ref('');
const reportDate = ref(new Date().toLocaleDateString('fa-IR'));

// ===== Elements =====
const elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'];

// ===== Sub Tabs =====
const subTabs = [
  {
    id: 'home',
    label: 'خانه',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>'
  },
  {
    id: 'water-analysis',
    label: 'آنالیز آب',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2C8 6 4 10 4 14c0 4 8 8 8 8s8-4 8-8c0-4-4-8-8-12z"/><path d="M12 6v2"/><path d="M12 10v2"/></svg>'
  },
  {
    id: 'target-elements',
    label: 'عناصر هدف',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
  },
  {
    id: 'fertilizer-calc',
    label: 'محاسبه کود',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/></svg>'
  },
  {
    id: 'fertilizer-db',
    label: 'پایگاه داده کودها',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
  },
  {
    id: 'interpretation',
    label: 'تفسیر داده‌ها',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 12v-2a5 5 0 00-5-5H8a5 5 0 00-5 5v2"/><path d="M3 12v6a5 5 0 005 5h8a5 5 0 005-5v-6"/></svg>'
  }
];

// ===== Target Elements =====
const targetUnit = ref('ppm');
const targetValues = reactive<Record<string, number>>({});
const finalValues = reactive<Record<string, number>>({});
const reservoirData = ref({});

// ===== Water Analysis =====
const waterPercentage = ref(80);
const wastewaterPercentage = ref(20);
const waterSalinity = ref(0);
const analysisUnit = ref('ppm');
const wastewaterValues = reactive<Record<string, number>>({});
const waterValues = reactive<Record<string, number>>({});

// ===== Fertilizer DB =====
const fertilizers = ref<any[]>([]);
const newFertilizer = reactive({
  name: '',
  pricePerKg: 0,
  elements: {} as Record<string, number>
});

// ===== Fertilizer Calc =====
const selectedFertilizers = ref<string[]>([]);
const tankVolume = ref(1000);
const dilutionFactor = ref(1);
const calcRows = ref<any[]>([]);
const calcErrors = ref<string[]>([]);

// ===== Interpretation =====
const interpretationResult = ref<any>(null);

// ===== Methods =====
const generateInterpretation = () => {
  // Simulate interpretation generation
  interpretationResult.value = {
    summary: 'گزارش تفسیر تغذیه گیاه:\n- تعادل یونی: برقرار ✅\n- عناصر دارای مشکل: هیچکدام\n- کیفیت آب: مناسب\n- تعداد توصیه‌ها: 0',
    ionBalance: {
      cation: 10.5,
      anion: 10.2,
      isBalanced: true,
      message: 'تعادل یونی برقرار است'
    },
    elementStatus: elements.map(el => ({
      element: el,
      target: targetValues[el] || 0,
      actual: (targetValues[el] || 0) * 0.95,
      difference: (targetValues[el] || 0) * 0.05,
      status: 'sufficient',
      message: 'وضعیت مطلوب'
    })),
    waterQuality: {
      salinity: waterSalinity.value,
      impact: 'مناسب',
      recommendation: 'نیازی به اقدام نیست'
    },
    fertilizerRecommendation: []
  };
};

const saveFertilizer = () => {
  if (!newFertilizer.name || !newFertilizer.pricePerKg) {
    alert('لطفاً نام و قیمت کود را وارد کنید');
    return;
  }
  fertilizers.value.push({
    id: Date.now().toString(),
    ...newFertilizer
  });
  showAddFertilizerModal.value = false;
  newFertilizer.name = '';
  newFertilizer.pricePerKg = 0;
  newFertilizer.elements = {};
};

// ===== Load Sample Data =====
const loadSampleData = () => {
  fertilizers.value = [
    {
      id: '1',
      name: 'کلسیم نیترات + آمونیوم',
      pricePerKg: 25000,
      elements: { 'N-NO3': 14.5, 'N-NH4': 1.5, 'Ca': 19 }
    },
    {
      id: '2',
      name: 'پتاسیم نیترات',
      pricePerKg: 32000,
      elements: { 'N-NO3': 13, 'K': 38 }
    },
    {
      id: '3',
      name: 'فسفات پتاسیم',
      pricePerKg: 28000,
      elements: { 'P': 22, 'K': 28 }
    },
    {
      id: '4',
      name: 'سولفات منیزیم',
      pricePerKg: 15000,
      elements: { 'S': 13, 'Mg': 10 }
    }
  ];
};

// ===== Lifecycle =====
onMounted(() => {
  loadSampleData();
});
</script>