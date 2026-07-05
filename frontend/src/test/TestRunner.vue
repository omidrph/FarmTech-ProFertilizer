<!-- frontend/src/test/TestRunner.vue -->
<template>
  <div class="fixed inset-0 z-[9999] bg-gray-900/95 backdrop-blur-sm flex items-center justify-center p-4" v-if="isOpen">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-5xl w-full max-h-[95vh] overflow-hidden flex flex-col">
      
      <!-- Header -->
      <div class="px-6 py-4 bg-gradient-to-l from-primary-600 to-primary-700 flex items-center justify-between flex-shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white">🧪 تست پیشرفته فرانت‌اند</h3>
            <p class="text-xs text-primary-100">تشخیص دقیق مشکل ریست نشدن تب خانه</p>
          </div>
        </div>
        <button @click="closeModal" class="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Status Bar -->
      <div class="px-6 py-2 bg-gray-50 dark:bg-gray-900/50 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between flex-wrap gap-2 flex-shrink-0">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <div class="w-2.5 h-2.5 rounded-full" :class="connectionStatus === 'connected' ? 'bg-success-500' : 'bg-danger-500'"></div>
            <span class="text-xs" :class="connectionStatus === 'connected' ? 'text-success-700 dark:text-success-400' : 'text-danger-700 dark:text-danger-400'">
              {{ connectionStatus === 'connected' ? '✅ متصل' : '❌ قطع' }}
            </span>
          </div>
          <span class="text-xs text-gray-400">|</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">گزارش: {{ reportStore.currentReportId || 'هیچ' }}</span>
          <span class="text-xs text-gray-400">|</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">عناصر هدف: {{ targetCount }} عدد</span>
          <span class="text-xs text-gray-400">|</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">بهینه‌سازی: {{ hasOptimization ? '✅ دارد' : '❌ ندارد' }}</span>
        </div>
        <button @click="copyResults" class="px-3 py-1 text-xs bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
          </svg>
          کپی نتایج
        </button>
      </div>

      <!-- Body -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar">
        
        <!-- دکمه‌های اقدام اصلی -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <button @click="step1_CreateFullReport" :disabled="isRunning" 
                  class="p-2.5 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 text-sm hover:bg-blue-100 transition-colors text-right disabled:opacity-50">
            <span class="font-semibold text-blue-700 dark:text-blue-400 text-xs">۱. ایجاد گزارش کامل</span>
            <p class="text-[10px] text-gray-500 dark:text-gray-400">+ عناصر هدف + آب</p>
          </button>
          
          <button @click="step2_Optimize" :disabled="isRunning || !reportStore.currentReportId"
                  class="p-2.5 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 text-sm hover:bg-green-100 transition-colors text-right disabled:opacity-50">
            <span class="font-semibold text-green-700 dark:text-green-400 text-xs">۲. بهینه‌سازی</span>
            <p class="text-[10px] text-gray-500 dark:text-gray-400">محاسبه ترکیب کودها</p>
          </button>
          
          <button @click="step3_LoadReport" :disabled="isRunning"
                  class="p-2.5 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800 text-sm hover:bg-purple-100 transition-colors text-right disabled:opacity-50">
            <span class="font-semibold text-purple-700 dark:text-purple-400 text-xs">۳. بارگذاری مجدد</span>
            <p class="text-[10px] text-gray-500 dark:text-gray-400">بررسی داده‌ها</p>
          </button>
          
          <button @click="step4_CheckHomeTab" :disabled="isRunning"
                  class="p-2.5 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800 text-sm hover:bg-orange-100 transition-colors text-right disabled:opacity-50">
            <span class="font-semibold text-orange-700 dark:text-orange-400 text-xs">۴. بررسی تب خانه</span>
            <p class="text-[10px] text-gray-500 dark:text-gray-400">وضعیت نمایش</p>
          </button>
        </div>

        <!-- دکمه تست کامل -->
        <button @click="runFullAutoTest" :disabled="isRunning" 
                class="w-full p-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium flex items-center justify-center gap-2 disabled:opacity-50">
          <svg v-if="isRunning" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ isRunning ? 'در حال اجرای تست‌ها...' : '▶️ اجرای تست کامل خودکار' }}
        </button>

        <!-- نتایج تست -->
        <div v-if="testResults.length > 0" class="space-y-2">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              نتایج تست‌ها
              <span class="text-xs font-normal text-gray-400">({{ testResults.length }} تست)</span>
            </h4>
            <div class="flex items-center gap-3 text-xs">
              <span class="text-success-600 dark:text-success-400">✅ {{ testResults.filter(r => r.passed).length }}</span>
              <span class="text-danger-600 dark:text-danger-400">❌ {{ testResults.filter(r => !r.passed).length }}</span>
            </div>
          </div>
          
          <div class="space-y-1 max-h-80 overflow-y-auto custom-scrollbar">
            <div v-for="(result, index) in testResults" :key="index" 
                 class="p-2 rounded-lg text-sm flex items-start gap-2"
                 :class="result.passed ? 'bg-success-50 dark:bg-success-900/10 border-r-4 border-success-500' : 'bg-danger-50 dark:bg-danger-900/10 border-r-4 border-danger-500'">
              <span class="flex-shrink-0 mt-0.5 text-base">{{ result.passed ? '✅' : '❌' }}</span>
              <div class="flex-1 min-w-0">
                <span class="font-medium" :class="result.passed ? 'text-success-700 dark:text-success-400' : 'text-danger-700 dark:text-danger-400'">
                  {{ result.name }}
                </span>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ result.message }}</p>
                <pre v-if="result.data" class="mt-1 p-2 bg-gray-100 dark:bg-gray-800 rounded text-xs overflow-x-auto max-h-32">{{ JSON.stringify(result.data, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- جمع‌بندی نهایی -->
        <div v-if="testResults.length > 0" class="p-3 rounded-lg border-2"
             :class="allPassed ? 'border-success-500 bg-success-50 dark:bg-success-900/10' : 'border-danger-500 bg-danger-50 dark:bg-danger-900/10'">
          <div class="flex items-center justify-between">
            <span class="font-bold" :class="allPassed ? 'text-success-700 dark:text-success-400' : 'text-danger-700 dark:text-danger-400'">
              {{ allPassed ? '🎉 همه تست‌ها با موفقیت انجام شدند!' : '⚠️ برخی تست‌ها ناموفق بودند!' }}
            </span>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              موفق: {{ testResults.filter(r => r.passed).length }}/{{ testResults.length }}
            </span>
          </div>
          <div v-if="!allPassed" class="mt-2 text-xs text-danger-600 dark:text-danger-400">
            <span class="font-semibold">مشکل اصلی: </span>
            <span v-for="(msg, idx) in errorMessages" :key="idx" class="block">
              {{ idx + 1 }}. {{ msg }}
            </span>
          </div>
        </div>

        <!-- لاگ اجرا -->
        <div v-if="logs.length > 0" class="mt-2">
          <button @click="showLogs = !showLogs" class="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
            {{ showLogs ? '📕 بستن لاگ' : '📗 نمایش لاگ' }} ({{ logs.length }})
          </button>
          <div v-if="showLogs" class="mt-1 p-2 bg-gray-900 text-gray-300 rounded-lg text-xs font-mono max-h-40 overflow-y-auto custom-scrollbar">
            <div v-for="(log, idx) in logs" :key="idx" class="py-0.5 border-b border-gray-800">
              <span class="text-gray-500">[{{ log.time }}]</span>
              <span :class="log.type === 'error' ? 'text-red-400' : log.type === 'success' ? 'text-green-400' : 'text-gray-300'">
                {{ log.message }}
              </span>
            </div>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="px-6 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between flex-shrink-0">
        <span class="text-xs text-gray-500 dark:text-gray-400">نسخه تست v2.0 | {{ new Date().toLocaleTimeString() }}</span>
        <button @click="closeAndRefresh" class="px-4 py-1.5 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
          بستن و رفرش
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useReportStore } from '@/store/modules/reportStore';
import { useTargetStore } from '@/store/modules/targetStore';
import { useCalcStore } from '@/store/modules/calcStore';
import { useWaterStore } from '@/store/modules/waterStore';
import { apiService } from '@/services/apiService';
import { useCalculations } from '@/composables/useCalculations';

// ===== Props & Emits =====
const props = defineProps<{ isOpen: boolean }>();
const emit = defineEmits<{ (e: 'update:isOpen', value: boolean): void }>();

// ===== Stores =====
const reportStore = useReportStore();
const targetStore = useTargetStore();
const calcStore = useCalcStore();
const waterStore = useWaterStore();
const { optimizeFertilizers } = useCalculations();

// ===== State =====
const isRunning = ref(false);
const showLogs = ref(false);
const connectionStatus = ref<'connected' | 'disconnected' | 'checking'>('checking');
const testResults = ref<Array<{ name: string; passed: boolean; message: string; data?: any }>>([]);
const logs = ref<Array<{ time: string; type: 'info' | 'success' | 'error'; message: string }>>([]);

// ===== Computed =====
const allPassed = computed(() => {
  return testResults.value.length > 0 && testResults.value.every(r => r.passed);
});

const targetCount = computed(() => {
  return Object.values(targetStore.targetElements).filter(v => v > 0).length;
});

const hasOptimization = computed(() => {
  return calcStore.optimizationResult !== null && 
         Object.keys(calcStore.optimizationResult.concentrations || {}).length > 0;
});

const errorMessages = computed(() => {
  return testResults.value.filter(r => !r.passed).map(r => r.message);
});

// ===== Methods =====
const closeModal = () => emit('update:isOpen', false);
const closeAndRefresh = () => { closeModal(); window.location.reload(); };

const addLog = (message: string, type: 'info' | 'success' | 'error' = 'info') => {
  const time = new Date().toLocaleTimeString();
  logs.value.push({ time, type, message });
};

const addResult = (name: string, passed: boolean, message: string, data?: any) => {
  testResults.value.push({ name, passed, message, data });
  addLog(`${passed ? '✅' : '❌'} ${name}: ${message}`, passed ? 'success' : 'error');
};

const checkConnection = async () => {
  connectionStatus.value = 'checking';
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);
    const response = await fetch('http://localhost:8000/health', { signal: controller.signal });
    clearTimeout(timeoutId);
    connectionStatus.value = response.ok ? 'connected' : 'disconnected';
  } catch {
    connectionStatus.value = 'disconnected';
  }
};

// ============================================================
// مرحله ۱: ایجاد گزارش کامل
// ============================================================
const step1_CreateFullReport = async () => {
  isRunning.value = true;
  testResults.value = [];
  logs.value = [];
  addLog('🚀 شروع مرحله ۱: ایجاد گزارش کامل');

  try {
    // 1.1 ایجاد گزارش
    addLog('📝 ایجاد گزارش جدید...');
    reportStore.resetReportData();
    reportStore.updateReportData({
      reportName: 'گزارش تست خودکار',
      plantName: 'گوجه فرنگی',
      season: 'تابستان',
      growthStage: 'گلدهی',
      date: new Date().toLocaleDateString('fa-IR')
    });
    
    const saveSuccess = await reportStore.saveCurrentReport();
    addResult('ایجاد گزارش', saveSuccess, saveSuccess ? `گزارش با ID ${reportStore.currentReportId} ایجاد شد` : 'خطا در ایجاد گزارش');
    
    if (!saveSuccess || !reportStore.currentReportId) {
      isRunning.value = false;
      return;
    }

    // 1.2 وارد کردن عناصر هدف
    addLog('🎯 وارد کردن عناصر هدف...');
    const targetData = {
      'N-NO3': 140, 'N-NH4': 0, 'P': 50, 'K': 350,
      'Mg': 50, 'Ca': 200, 'S': 150,
      'Fe': 3, 'Mn': 0.8, 'Zn': 0.1, 'B': 0.3, 'Cu': 0.07, 'Mo': 0.03, 'Cl': 320
    };
    
    for (const [key, value] of Object.entries(targetData)) {
      targetStore.setTargetElement(key as any, value);
    }
    
    const targetCount = Object.values(targetStore.targetElements).filter(v => v > 0).length;
    addResult('وارد کردن عناصر هدف', targetCount > 0, `${targetCount} عنصر وارد شد`);

    // 1.3 وارد کردن آنالیز آب
    addLog('💧 وارد کردن آنالیز آب...');
    waterStore.setWaterMix({ waterPercentage: 100, wastewaterPercentage: 0, waterSalinity: 0.8 });
    waterStore.setWaterValue('K', 35);
    waterStore.setWaterValue('Ca', 50);
    
    const waterSave = await reportStore.saveCurrentReport();
    addResult('ذخیره آنالیز آب', waterSave, 'آنالیز آب ذخیره شد');

    addLog('✅ مرحله ۱ کامل شد');
    
  } catch (error: any) {
    addResult('مرحله ۱', false, `خطا: ${error.message}`);
    addLog(`❌ خطا: ${error.message}`, 'error');
  }
  
  isRunning.value = false;
};

// ============================================================
// مرحله ۲: بهینه‌سازی
// ============================================================
const step2_Optimize = async () => {
  isRunning.value = true;
  addLog('🚀 شروع مرحله ۲: بهینه‌سازی');

  try {
    if (!reportStore.currentReportId) {
      addResult('بهینه‌سازی', false, 'هیچ گزارشی وجود ندارد');
      isRunning.value = false;
      return;
    }

    // دریافت کودها
    const fertilizers = await apiService.getFertilizers();
    const selectedFerts = fertilizers.filter((f: any) => f.is_system_default === false).slice(0, 10);
    
    if (selectedFerts.length === 0) {
      addResult('بهینه‌سازی', false, 'هیچ کود شخصی برای بهینه‌سازی وجود ندارد');
      isRunning.value = false;
      return;
    }

    addLog(`🧪 ${selectedFerts.length} کود انتخاب شد`);

    const result = await optimizeFertilizers(
      selectedFerts,
      { auto_balance: true },
      5000, 25, 100
    );

    if (result) {
      addResult('بهینه‌سازی', true, `موفق - ${Object.keys(result.weights).length} کود استفاده شد`);
      addLog(`💰 هزینه: ${result.cost_total?.toLocaleString()} تومان`);
      addLog(`📊 خطا: ${(result.residual_error * 100).toFixed(2)}%`);
    } else {
      addResult('بهینه‌سازی', false, calcStore.lastOptimizationError || 'خطا در بهینه‌سازی');
    }

  } catch (error: any) {
    addResult('بهینه‌سازی', false, `خطا: ${error.message}`);
    addLog(`❌ خطا: ${error.message}`, 'error');
  }
  
  isRunning.value = false;
};

// ============================================================
// مرحله ۳: بارگذاری مجدد گزارش
// ============================================================
const step3_LoadReport = async () => {
  isRunning.value = true;
  testResults.value = [];
  addLog('🚀 شروع مرحله ۳: بارگذاری مجدد گزارش');

  try {
    // دریافت لیست گزارش‌ها
    const reports = await apiService.getReports();
    if (!reports || reports.length === 0) {
      addResult('بارگذاری گزارش', false, 'هیچ گزارشی وجود ندارد');
      isRunning.value = false;
      return;
    }

    const reportId = reports[0].id;
    addLog(`📂 بارگذاری گزارش ${reportId}...`);

    // بارگذاری گزارش
    const success = await reportStore.loadReport(reportId);
    addResult('بارگذاری گزارش', success, success ? `گزارش ${reportId} بارگذاری شد` : 'خطا در بارگذاری');

    if (success) {
      // بررسی currentReportId
      addResult('currentReportId', reportStore.currentReportId === reportId, 
                `currentReportId: ${reportStore.currentReportId}`);

      // بررسی targetElements
      const hasTargets = Object.values(targetStore.targetElements).some(v => v > 0);
      addResult('targetElements بارگذاری شد', hasTargets, 
                hasTargets ? `${targetCount.value} عنصر بارگذاری شد` : 'هیچ عنصری بارگذاری نشد!');

      // بررسی optimizationResult
      const hasOpt = calcStore.optimizationResult !== null && 
                     Object.keys(calcStore.optimizationResult.concentrations || {}).length > 0;
      addResult('optimizationResult بارگذاری شد', hasOpt, 
                hasOpt ? `${Object.keys(calcStore.optimizationResult!.concentrations).length} عنصر` : 'خالی است!');

      // بررسی final_values
      if (calcStore.optimizationResult) {
        const conc = calcStore.optimizationResult.concentrations || {};
        const hasFinal = Object.keys(conc).length > 0;
        addResult('final_values', hasFinal, 
                  hasFinal ? `${Object.keys(conc).length} عنصر` : 'خالی است!', 
                  hasFinal ? conc : null);
      } else {
        addResult('final_values', false, 'optimizationResult null است');
      }
    }

  } catch (error: any) {
    addResult('مرحله ۳', false, `خطا: ${error.message}`);
    addLog(`❌ خطا: ${error.message}`, 'error');
  }
  
  isRunning.value = false;
};

// ============================================================
// مرحله ۴: بررسی تب خانه
// ============================================================
const step4_CheckHomeTab = async () => {
  isRunning.value = true;
  testResults.value = [];
  addLog('🚀 شروع مرحله ۴: بررسی تب خانه');

  try {
    const summary = await apiService.getHomeSummary();
    
    addResult('دریافت خلاصه خانه', summary !== null, summary ? 'دریافت شد' : 'خطا');
    
    if (summary) {
      addResult('has_data', summary.has_data === true, `has_data: ${summary.has_data}`);
      
      const elementsData = summary.elements_data || [];
      const hasElements = elementsData.length > 0;
      addResult('elements_data', hasElements, 
                hasElements ? `${elementsData.length} عنصر دارد` : 'خالی است!', 
                hasElements ? elementsData.slice(0, 3) : null);
      
      if (hasElements) {
        const hasActual = elementsData.some((item: any) => item.actual > 0);
        addResult('مقادیر تامین شده', hasActual, 
                  hasActual ? 'موجود است' : 'همه صفر هستند!');
      }
    }
  } catch (error: any) {
    addResult('مرحله ۴', false, `خطا: ${error.message}`);
    addLog(`❌ خطا: ${error.message}`, 'error');
  }
  
  isRunning.value = false;
};

// ============================================================
// تست کامل خودکار
// ============================================================
const runFullAutoTest = async () => {
  isRunning.value = true;
  testResults.value = [];
  logs.value = [];
  
  await checkConnection();
  
  if (connectionStatus.value !== 'connected') {
    addResult('اتصال به بک‌اند', false, 'لطفاً بک‌اند را راه‌اندازی کنید');
    isRunning.value = false;
    return;
  }

  addLog('🧪 شروع تست کامل خودکار...');
  
  // مرحله ۱: ایجاد گزارش
  await step1_CreateFullReport();
  await new Promise(r => setTimeout(r, 500));
  
  // مرحله ۲: بهینه‌سازی
  if (reportStore.currentReportId) {
    await step2_Optimize();
    await new Promise(r => setTimeout(r, 500));
  }
  
  // مرحله ۳: بارگذاری مجدد
  await step3_LoadReport();
  await new Promise(r => setTimeout(r, 500));
  
  // مرحله ۴: بررسی تب خانه
  await step4_CheckHomeTab();
  
  addLog('✅ تست کامل به پایان رسید');
  isRunning.value = false;
};

// ============================================================
// کپی نتایج
// ============================================================
const copyResults = async () => {
  const text = testResults.value.map(r => 
    `${r.passed ? '✅' : '❌'} ${r.name}: ${r.message}`
  ).join('\n');
  
  const summary = `
🧪 نتایج تست فرانت‌اند
=====================
تاریخ: ${new Date().toLocaleString()}
گزارش: ${reportStore.currentReportId || 'هیچ'}
عناصر هدف: ${targetCount.value}
بهینه‌سازی: ${hasOptimization.value ? 'دارد' : 'ندارد'}
----------------------
${text}
=====================
موفق: ${testResults.value.filter(r => r.passed).length}/${testResults.value.length}
`;
  
  try {
    await navigator.clipboard.writeText(summary);
    addLog('📋 نتایج کپی شد', 'success');
  } catch {
    // fallback
    const textarea = document.createElement('textarea');
    textarea.value = summary;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    addLog('📋 نتایج کپی شد', 'success');
  }
};

// ============================================================
// Lifecycle
// ============================================================
onMounted(() => {
  checkConnection();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
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
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>