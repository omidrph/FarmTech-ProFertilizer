<!-- frontend/src/components/features/TargetElementsTab.vue -->
<template>
  <div class="space-y-4">
    <!-- ============================================================ -->
    <!-- نوار ابزار -->
    <!-- ============================================================ -->
    <div class="flex flex-wrap items-center gap-3 bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
      <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[200px]">
        <h3 class="text-base font-semibold text-gray-900 dark:text-white flex items-center gap-2 whitespace-nowrap">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" />
          </svg>
          عناصر هدف
        </h3>

        <div class="flex items-center gap-1.5 mr-1 sm:mr-0">
          <label class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">واحد:</label>
          <select v-model="targetUnit" @change="handleUnitChange"
            class="px-1.5 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 transition-all">
            <option value="ppm">PPM</option>
            <option value="meq">MEQ/L</option>
            <option value="mmol">MMOL/L</option>
          </select>
        </div>
      </div>

      <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap w-full sm:w-auto justify-end">
        <!-- وضعیت ذخیره‌سازی -->
        <span v-if="isSaving" class="inline-flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
          <svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
          در حال ذخیره...
        </span>
        <span v-else-if="saveStatus === 'success'" class="inline-flex items-center gap-1 text-xs text-success-600 dark:text-success-400">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          ذخیره شد
        </span>

        <button type="button" @click="saveAsRecipe" :disabled="!hasAnyTarget"
          class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 border border-primary-200 dark:border-primary-800 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 whitespace-nowrap"
          title="ذخیرهٔ مقادیر جدول به‌عنوان رسپی شخصی">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
          افزودن به رسپی شخصی
        </button>

        <button @click="resetTargets"
          class="flex-1 sm:flex-none px-2.5 sm:px-4 py-1.5 sm:py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-xs sm:text-sm flex items-center justify-center gap-1 sm:gap-1.5 min-w-[60px] sm:min-w-0"
          title="بازنشانی تمام مقادیر">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          بازنشانی
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- دسکتاپ: جدول‌های جدا برای هر گروه -->
    <!-- ============================================================ -->
    <div class="hidden lg:block space-y-4">
      <div v-for="g in groups" :key="'d-' + g.id" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div class="px-4 py-2.5 bg-gray-50 dark:bg-gray-700/50 border-b border-gray-200 dark:border-gray-700 text-xs font-semibold text-gray-600 dark:text-gray-300">{{ g.title }}</div>
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr>
                <th class="sticky right-0 z-10 w-32 bg-gray-50 dark:bg-gray-700 px-4 py-3 text-right text-sm font-bold text-gray-700 dark:text-gray-200 border-b border-gray-200 dark:border-gray-600 shadow-sm">عنصر</th>
                <th v-for="el in g.rows" :key="el.key" class="px-3 py-3 font-semibold border-b border-gray-200 dark:border-gray-600 text-center min-w-[88px]" :class="tone(el).th">
                  <div class="inline-flex flex-col items-center gap-0.5">
                    <span class="text-sm">{{ el.name }}</span>
                    <span class="text-xs font-medium opacity-80" dir="ltr">{{ el.label }}</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
                <td class="sticky right-0 z-10 bg-white dark:bg-gray-800 px-4 py-2.5 text-right text-sm font-medium text-gray-600 dark:text-gray-400 border-l border-gray-100 dark:border-gray-700 shadow-sm">
                  <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary-500"></span>مقدار هدف</div>
                </td>
                <td v-for="el in g.rows" :key="'v-' + el.key" class="px-2 py-2 border-l border-gray-100 dark:border-gray-700 text-center transition-colors" :class="tone(el).cell">
                  <input type="text" inputmode="decimal" dir="ltr" placeholder="۰" :value="getDisplayText(el.key)" @change="updateElementValue(el.key, $event)" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-full max-w-[96px] mx-auto px-2 py-2 text-center tabular-nums bg-transparent border border-transparent hover:border-gray-300 dark:hover:border-gray-500 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 rounded transition-all duration-200 text-gray-700 dark:text-gray-300" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 px-4 py-3 flex flex-wrap items-center gap-4 text-xs">
        <span class="text-gray-600 dark:text-gray-400 font-medium">راهنما:</span>
        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-500"></span><span class="text-gray-600 dark:text-gray-400">کاتیون</span></div>
        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-red-500"></span><span class="text-gray-600 dark:text-gray-400">آنیون</span></div>
        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-gray-400"></span><span class="text-gray-600 dark:text-gray-400">خنثی</span></div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- موبایل / تبلت: لیست آکاردئونی -->
    <!-- ============================================================ -->
    <div class="lg:hidden space-y-3">
      <div v-for="g in groups" :key="'m-' + g.id" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <button type="button" @click="openGroups[g.id] = !openGroups[g.id]" class="w-full flex items-center justify-between px-4 py-3">
          <span class="flex items-center gap-2 text-sm font-semibold text-gray-900 dark:text-white">
            {{ g.title }}
            <span v-if="filledCount(g)" class="text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 tabular-nums">{{ filledCount(g).toLocaleString('fa-IR') }}</span>
          </span>
          <svg class="w-4 h-4 text-gray-400 transition-transform" :class="openGroups[g.id] ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </button>
        <div v-show="openGroups[g.id]" class="px-3 pb-3 pt-3 space-y-2.5 border-t border-gray-100 dark:border-gray-700">
          <div v-for="el in g.rows" :key="'mr-' + el.key" class="flex items-center gap-2">
            <div class="flex-1 min-w-0 h-10 flex items-center justify-between gap-1 px-2.5 rounded-lg border" :class="tone(el).pill">
              <span class="truncate text-xs font-medium">{{ el.name }}</span>
              <span class="text-xs font-bold" dir="ltr">{{ el.label }}</span>
            </div>
            <input type="text" inputmode="decimal" dir="ltr" placeholder="۰" :value="getDisplayText(el.key)" @change="updateElementValue(el.key, $event)" @keydown.enter="($event.target as HTMLInputElement).blur()" class="w-[6rem] flex-shrink-0 h-10 px-2 text-center text-sm tabular-nums border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 placeholder-gray-300 focus:bg-white dark:focus:bg-gray-700 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors" />
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- تعادل کاتیون و آنیون -->
    <!-- ============================================================ -->
    <div v-if="targetStore.isCalculatingBalance" class="flex items-center justify-center gap-2 p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
      <div class="animate-spin w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full"></div>
      <span class="text-sm text-gray-500 dark:text-gray-400">در حال محاسبه تعادل یونی...</span>
    </div>
    <HomeIonBalance
      v-else-if="ionBalance"
      compact
      :cation="Number(ionBalance.cation) || 0"
      :anion="Number(ionBalance.anion) || 0"
      :balanced="!!ionBalance.isBalanced"
    />

    <!-- رسپی‌ها -->
    <RecipeManager ref="recipeRef" @recipe-applied="handleRecipeApplied" />

    <!-- جدول توازن عناصر + راهنما -->
    <BalanceAndGuide
      :elements="elements"
      :target-unit="targetUnit"
      :target-values="targetValues"
      :converted-values="convertedValues"
      :is-converting="isConverting"
      :selected-element="selectedElement"
      @update:selected-element="selectedElement = $event"
      @open-guide="openElementGuide"
    />

    <!-- پیام Toast -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="toastMessage" class="fixed bottom-20 sm:bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 px-4 py-2.5 rounded-xl shadow-lg text-sm text-white"
          :class="toastType === 'success' ? 'bg-success-600' : 'bg-danger-600'">
          <span class="text-center">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import HomeIonBalance from './home/HomeIonBalance.vue';
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useTargetStore } from '@/store/modules/targetStore';
import { useReportStore } from '@/store/modules/reportStore';
import { apiService } from '@/services/apiService';
import { normalizeNumberText } from '@/utils/waterForms';
import RecipeManager from './RecipeManager.vue';
import BalanceAndGuide from './BalanceAndGuide.vue';

// ===== Stores =====
const targetStore = useTargetStore();
const reportStore = useReportStore();

// ===== عناصر (مبنای ذخیره: ppm بر حسب «عنصر»؛ N-NO3 و N-NH4 بر مبنای N) =====
interface ElDef { key: string; name: string; label: string; type: 'cation' | 'anion' | 'neutral'; mw: number; z: number }
const EL_DEFS: ElDef[] = [
  { key: 'N-NO3', name: 'نیتروژن نیتراتی', label: 'N-NO₃', type: 'anion', mw: 14.007, z: 1 },
  { key: 'N-NH4', name: 'نیتروژن آمونیومی', label: 'N-NH₄', type: 'cation', mw: 14.007, z: 1 },
  { key: 'P', name: 'فسفر', label: 'P', type: 'anion', mw: 30.974, z: 1 },
  { key: 'K', name: 'پتاسیم', label: 'K', type: 'cation', mw: 39.098, z: 1 },
  { key: 'Ca', name: 'کلسیم', label: 'Ca', type: 'cation', mw: 40.078, z: 2 },
  { key: 'Mg', name: 'منیزیم', label: 'Mg', type: 'cation', mw: 24.305, z: 2 },
  { key: 'S', name: 'گوگرد', label: 'S', type: 'anion', mw: 32.065, z: 2 },
  { key: 'Na', name: 'سدیم', label: 'Na', type: 'cation', mw: 22.99, z: 1 },
  { key: 'Cl', name: 'کلر', label: 'Cl', type: 'anion', mw: 35.453, z: 1 },
  { key: 'Fe', name: 'آهن', label: 'Fe', type: 'cation', mw: 55.845, z: 2 },
  { key: 'Mn', name: 'منگنز', label: 'Mn', type: 'cation', mw: 54.938, z: 2 },
  { key: 'Zn', name: 'روی', label: 'Zn', type: 'cation', mw: 65.38, z: 2 },
  { key: 'B', name: 'بور', label: 'B', type: 'anion', mw: 10.81, z: 1 },
  { key: 'Cu', name: 'مس', label: 'Cu', type: 'cation', mw: 63.546, z: 2 },
  { key: 'Mo', name: 'مولیبدن', label: 'Mo', type: 'anion', mw: 95.95, z: 2 },
  { key: 'Si', name: 'سیلیسیم', label: 'Si', type: 'neutral', mw: 28.086, z: 1 },
];
const elements = EL_DEFS.map((e) => e.key);
const DEF_BY_KEY: Record<string, ElDef> = Object.fromEntries(EL_DEFS.map((e) => [e.key, e]));

const groups = [
  { id: 'macro', title: 'عناصر پرمصرف', rows: EL_DEFS.slice(0, 9) },
  { id: 'micro', title: 'عناصر کم‌مصرف و سیلیسیم', rows: EL_DEFS.slice(9) },
];
// آکاردئون موبایل
const openGroups = reactive<Record<string, boolean>>({ macro: true, micro: false });

// ===== State =====
const recipeRef = ref<InstanceType<typeof RecipeManager> | null>(null);

const isSaving = ref(false);
const saveStatus = ref<'idle' | 'saving' | 'success'>('idle');
let saveTimeout: ReturnType<typeof setTimeout> | null = null;

const toastMessage = ref<string | null>(null);
const toastType = ref<'success' | 'error'>('success');

const isConverting = ref(false);
const convertedValues = ref<Record<string, Record<string, number>> | null>(null);
const selectedElement = ref<string>('N-NO3');

// ===== Computed =====
const targetUnit = computed({
  get: () => targetStore.targetUnit,
  set: (val: any) => targetStore.setTargetUnit(val)
});
const targetValues = computed(() => targetStore.targetElements);
const ionBalance = computed(() => targetStore.ionBalance);
const hasAnyTarget = computed(() => Object.values(targetValues.value || {}).some((v) => Number(v) > 0));

// ===== رنگ‌آمیزی (همان رنگ‌های جدول آنالیز آب) =====
const tone = (el: ElDef) =>
  el.type === 'cation'
    ? { pill: 'bg-blue-50 border-blue-200 text-blue-700 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-300', th: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300', cell: 'bg-blue-50/30 dark:bg-blue-900/5' }
    : el.type === 'anion'
      ? { pill: 'bg-red-50 border-red-200 text-red-700 dark:bg-red-900/20 dark:border-red-800 dark:text-red-300', th: 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300', cell: 'bg-red-50/30 dark:bg-red-900/5' }
      : { pill: 'bg-gray-50 border-gray-200 text-gray-700 dark:bg-gray-700/40 dark:border-gray-600 dark:text-gray-300', th: 'bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300', cell: '' };

const filledCount = (g: { rows: ElDef[] }): number =>
  g.rows.filter((r) => Number((targetValues.value as any)[r.key]) > 0).length;

// ===== تبدیل واحد (هم‌مبنا با بک‌اند: N بر مبنای نیتروژن، ظرفیت واقعی یون‌ها) =====
function convertToDisplay(value: number, element: string, unit: string): number {
  const d = DEF_BY_KEY[element];
  if (!d || unit === 'ppm') return value;
  if (unit === 'meq') return (value * d.z) / d.mw;
  if (unit === 'mmol') return value / d.mw;
  return value;
}
function convertFromDisplay(displayValue: number, element: string, unit: string): number {
  const d = DEF_BY_KEY[element];
  if (!d || unit === 'ppm') return displayValue;
  if (unit === 'meq') return (displayValue * d.mw) / d.z;
  if (unit === 'mmol') return displayValue * d.mw;
  return displayValue;
}

const getDisplayText = (element: string): string => {
  const raw = Number((targetValues.value as any)[element]) || 0;
  if (!(raw > 0)) return '';
  return String(parseFloat(convertToDisplay(raw, element, targetUnit.value).toFixed(4)));
};

const updateElementValue = (element: string, event: Event) => {
  const input = event.target as HTMLInputElement;
  const txt = normalizeNumberText(input.value);
  const n = txt === '' ? 0 : parseFloat(txt);
  if (!Number.isFinite(n) || n < 0) {
    input.value = getDisplayText(element);
    return;
  }
  targetStore.setTargetElement(element as any, convertFromDisplay(n, element, targetUnit.value));
  input.value = getDisplayText(element);
  triggerAutoSave();
};

const handleUnitChange = () => {
  loadConvertedValues();
  triggerAutoSave();
};

const resetTargets = () => {
  targetStore.resetTargets();
  convertedValues.value = null;
  showToast('همه مقادیر بازنشانی شدند', 'success');
  triggerAutoSave();
  setTimeout(() => { loadConvertedValues(); }, 200);
};

const saveAsRecipe = () => {
  recipeRef.value?.openSaveModal();
};

const openElementGuide = (element: string) => {
  selectedElement.value = element;
  setTimeout(() => {
    const guideElement = document.getElementById('balance-guide-section');
    if (guideElement) guideElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
};

// ===== Auto-save =====
const triggerAutoSave = () => {
  if (saveTimeout) clearTimeout(saveTimeout);
  saveStatus.value = 'saving';
  isSaving.value = true;
  saveTimeout = setTimeout(async () => {
    if (reportStore.currentReportId) {
      const success = await reportStore.saveCurrentReport();
      isSaving.value = false;
      if (success) {
        saveStatus.value = 'success';
        setTimeout(() => { saveStatus.value = 'idle'; }, 2000);
      } else {
        saveStatus.value = 'idle';
      }
    } else {
      isSaving.value = false;
      saveStatus.value = 'idle';
    }
  }, 1000);
};

// ===== Toast =====
const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg;
  toastType.value = type;
  setTimeout(() => { toastMessage.value = null; }, 3000);
};

// ===== جدول توازن عناصر =====
const loadConvertedValues = async () => {
  isConverting.value = true;
  try {
    const result: Record<string, Record<string, number>> = {};
    for (const element of elements) {
      const raw = Number((targetValues.value as any)[element]) || 0;
      if (!(raw > 0)) {
        result[element] = { ppm: 0, meq: 0, mmol: 0 };
        continue;
      }
      const meqResult = await apiService.convertUnit({ value: raw, from_unit: 'ppm', to_unit: 'meq', element });
      const mmolResult = await apiService.convertUnit({ value: raw, from_unit: 'ppm', to_unit: 'mmol', element });
      result[element] = { ppm: raw, meq: meqResult.converted_value, mmol: mmolResult.converted_value };
    }
    convertedValues.value = result;
  } catch (error: any) {
    console.error('خطا در تبدیل واحدها:', error);
    showToast('خطا در تبدیل واحدها', 'error');
  } finally {
    isConverting.value = false;
  }
};

const handleRecipeApplied = () => {
  loadConvertedValues();
  triggerAutoSave();
};

watch(targetValues, () => { setTimeout(() => { loadConvertedValues(); }, 500); }, { deep: true });
onMounted(() => { loadConvertedValues(); });
</script>

<style scoped>
.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translate(-50%, 10px); }
.custom-scrollbar::-webkit-scrollbar { height: 6px; width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 3px; }
.dark .custom-scrollbar::-webkit-scrollbar-track { background: #374151; }
.dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #4b5563; }
.tabular-nums { font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }
</style>
