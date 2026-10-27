
<!-- frontend/src/components/features/calc/FertilizerSelector.vue -->
<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">

    <!-- ============================================================ -->
    <!-- هدر -->
    <!-- ============================================================ -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between gap-3 flex-wrap">
      <div class="flex items-center gap-2">
        <span class="w-8 h-8 rounded-lg bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-4 h-4 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </span>
        <div>
          <h3 class="text-base font-semibold text-gray-900 dark:text-white">انتخاب کود</h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ selectedList.length }} کود انتخاب شده از {{ userFertilizers.length }} کود
          </p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="selectAll"
          :disabled="availableList.length === 0"
          :title="includeAcidsBases ? 'اسیدها و بازها هم اضافه می‌شوند (طبق تنظیمات پیشرفته)' : 'اسیدها و بازها اضافه نمی‌شوند؛ برای اضافه‌شدن، گزینهٔ آن را در تنظیمات پیشرفته روشن کنید'"
          class="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          افزودن همه
        </button>
        <button
          type="button"
          @click="clearAll"
          :disabled="selectedList.length === 0"
          class="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          پاک کردن
        </button>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- بدنه: دو ستون در دسکتاپ، تک‌ستون در موبایل -->
    <!-- ============================================================ -->
    <div class="p-4 grid grid-cols-1 lg:grid-cols-2 gap-4">

      <!-- ===================== ستون کودهای موجود ===================== -->
      <section
        class="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/60 dark:bg-gray-900/30 overflow-hidden"
        :class="dropTarget === 'available' ? 'ring-2 ring-primary-400' : ''"
        @dragover.prevent="onDragOver('available')"
        @dragleave="onDragLeave('available')"
        @drop.prevent="onDrop('available')"
      >
        <div class="px-3 py-2 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <span class="text-xs font-semibold text-gray-600 dark:text-gray-300">کودهای موجود</span>
          <span class="text-[11px] text-gray-400">{{ filteredAvailable.length }} مورد</span>
        </div>

        <!-- جستجو -->
        <div class="p-3 pb-2">
          <div class="relative">
            <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="جستجو: نام، فرمول یا عنصر"
              class="w-full pr-9 pl-8 py-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
            />
            <button
              v-if="searchQuery"
              type="button"
              @click="searchQuery = ''"
              class="absolute left-2 top-1/2 -translate-y-1/2 w-5 h-5 rounded-full flex items-center justify-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
              aria-label="پاک کردن جستجو"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- لیست -->
        <div class="px-3 pb-3 space-y-2 overflow-y-auto custom-scrollbar" style="max-height: 340px">
          <article
            v-for="fertilizer in filteredAvailable"
            :key="fertilizer.id"
            :draggable="isDesktop"
            @dragstart="onDragStart(fertilizer.id, 'available', $event)"
            @dragend="onDragEnd"
            @click="addFertilizer(fertilizer.id)"
            class="group relative rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-2.5 cursor-pointer hover:border-primary-400 hover:shadow-sm transition-all"
            :class="draggingId === fertilizer.id ? 'opacity-40' : ''"
          >
            <div class="flex items-start gap-2">
              <span
                v-if="isDesktop"
                class="mt-0.5 text-gray-300 dark:text-gray-600 group-hover:text-primary-400 transition-colors cursor-grab active:cursor-grabbing"
                title="بکشید و رها کنید"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <circle cx="7" cy="5" r="1.3" /><circle cx="13" cy="5" r="1.3" />
                  <circle cx="7" cy="10" r="1.3" /><circle cx="13" cy="10" r="1.3" />
                  <circle cx="7" cy="15" r="1.3" /><circle cx="13" cy="15" r="1.3" />
                </svg>
              </span>

              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                <div class="flex items-center gap-1.5 mt-1 flex-wrap">
                  <span
                    class="text-[10px] px-1.5 py-0.5 rounded"
                    :class="kindClass(fertilizer)"
                  >
                    {{ kindLabel(fertilizer) }}
                  </span>
                  <span v-if="fertilizer.form === 'liquid'" class="text-[10px] px-1.5 py-0.5 rounded bg-cyan-50 text-cyan-700 dark:bg-cyan-900/20 dark:text-cyan-300">مایع</span>
                  <span v-if="isCompany(fertilizer)" class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400">
                    {{ fertilizer.brand }}
                  </span>
                  <span
                    v-for="el in mainElements(fertilizer)"
                    :key="el.symbol"
                    class="text-[10px] px-1.5 py-0.5 rounded bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                  >
                    {{ el.symbol }} {{ el.value }}٪
                  </span>
                </div>
              </div>

              <span class="mt-0.5 w-6 h-6 rounded-md flex items-center justify-center text-gray-400 group-hover:bg-primary-500 group-hover:text-white transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
              </span>
            </div>
          </article>

          <!-- خالی -->
          <div v-if="filteredAvailable.length === 0" class="py-10 text-center">
            <svg class="w-10 h-10 mx-auto text-gray-300 dark:text-gray-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ emptyAvailableTitle }}
            </p>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
              {{ emptyAvailableHint }}
            </p>
          </div>
        </div>
      </section>

      <!-- ===================== ستون کودهای انتخاب‌شده ===================== -->
      <section
        class="flex flex-col rounded-xl border-2 border-dashed transition-colors overflow-hidden"
        :class="dropTarget === 'selected'
          ? 'border-primary-500 bg-primary-50/60 dark:bg-primary-900/20'
          : 'border-gray-200 dark:border-gray-700 bg-gray-50/60 dark:bg-gray-900/30'"
        @dragover.prevent="onDragOver('selected')"
        @dragleave="onDragLeave('selected')"
        @drop.prevent="onDrop('selected')"
      >
        <div class="px-3 py-2 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <span class="text-xs font-semibold text-gray-600 dark:text-gray-300">کودهای انتخاب‌شده</span>
          <span class="text-[11px] text-gray-400">{{ selectedList.length }} مورد</span>
        </div>

        <div class="p-3 space-y-2 overflow-y-auto custom-scrollbar" style="max-height: 396px">
          <article
            v-for="(fertilizer, index) in selectedList"
            :key="fertilizer.id"
            :draggable="isDesktop"
            @dragstart="onDragStart(fertilizer.id, 'selected', $event)"
            @dragend="onDragEnd"
            @dragover.prevent="onItemDragOver(index)"
            class="group relative rounded-lg border border-primary-200 dark:border-primary-900/50 bg-white dark:bg-gray-800 p-2.5 transition-all"
            :class="[
              draggingId === fertilizer.id ? 'opacity-40' : '',
              hoverIndex === index && draggingFrom === 'selected' ? 'ring-2 ring-primary-400' : ''
            ]"
          >
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-md bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 text-[11px] font-bold flex items-center justify-center flex-shrink-0">
                {{ index + 1 }}
              </span>

              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ fertilizer.name }}</p>
                <div class="flex items-center gap-1.5 mt-0.5 flex-wrap">
                  <span
                    v-if="isAdjuster(fertilizer)"
                    class="text-[10px] px-1.5 py-0.5 rounded"
                    :class="kindClass(fertilizer)"
                  >{{ kindLabel(fertilizer) }}</span>
                  <button
                    v-if="isAdjuster(fertilizer)"
                    type="button"
                    @click.stop="openModal(fertilizer, true)"
                    class="text-[10px] px-1.5 py-0.5 rounded bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 hover:bg-primary-100 dark:hover:bg-primary-900/50"
                    title="ویرایش مقدار"
                  >{{ amountLabel(fertilizer.id) }} ✎</button>
                  <span
                    v-for="el in mainElements(fertilizer)"
                    :key="el.symbol"
                    class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                  >{{ el.symbol }} {{ el.value }}٪</span>
                </div>
              </div>

              <button
                type="button"
                @click.stop="removeFertilizer(fertilizer.id)"
                class="w-6 h-6 rounded-md flex items-center justify-center text-gray-400 hover:bg-rose-500 hover:text-white transition-colors flex-shrink-0"
                aria-label="حذف"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </article>

          <!-- حالت خالی / ناحیه رها کردن -->
          <div v-if="selectedList.length === 0" class="py-12 text-center">
            <svg class="w-10 h-10 mx-auto text-gray-300 dark:text-gray-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4" />
            </svg>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ isDesktop ? 'کودها را اینجا رها کنید' : 'برای افزودن، روی کود بزنید' }}
            </p>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
              ترتیب انتخاب روی نتیجه اثری ندارد
            </p>
          </div>
        </div>
      </section>
    </div>
  
    <AcidAmountModal
      :open="modalOpen"
      :fertilizer="modalFertilizer as any"
      :tank-volume="tankVolume"
      :initial="modalFertilizer ? fixedAmounts[modalFertilizer.id] || null : null"
      :editing="modalEditing"
      @confirm="onModalConfirmWrapped"
      @cancel="onModalCancelWrapped"
    />
</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import AcidAmountModal from './AcidAmountModal.vue';
import { unitLabel, type AmountUnit } from '@/utils/fertilizerUnits';

// ===== Types =====
interface Fertilizer {
  id: string;
  name: string;
  brand?: string;
  isAcid: boolean;
  isBase?: boolean;
  form?: string;
  densityGMl?: number;
  pricePerKg: number;
  concentration?: number;
  elements: Record<string, number>;
  isSystemDefault: boolean;
}

type Pane = 'available' | 'selected';

// ===== Props / Emits =====
const props = withDefaults(defineProps<{
  fertilizers: Fertilizer[];
  selectedFertilizers: string[];
  fixedAmounts?: Record<string, { amount: number; unit: AmountUnit }>;
  includeAcidsBases?: boolean;
  tankVolume?: number;
}>(), { fixedAmounts: () => ({}), includeAcidsBases: false, tankVolume: 1000 });

const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:fixedAmounts', value: Record<string, { amount: number; unit: AmountUnit }>): void;
}>();

// ===== State =====
const searchQuery = ref('');
const draggingId = ref<string | null>(null);
const draggingFrom = ref<Pane | null>(null);
const dropTarget = ref<Pane | null>(null);
const hoverIndex = ref<number | null>(null);
const isDesktop = ref(false);

let mediaQuery: MediaQueryList | null = null;
const syncViewport = () => {
  isDesktop.value = !!mediaQuery?.matches;
};

onMounted(() => {
  if (typeof window !== 'undefined' && window.matchMedia) {
    mediaQuery = window.matchMedia('(min-width: 1024px)');
    syncViewport();
    mediaQuery.addEventListener?.('change', syncViewport);
  }
});

onBeforeUnmount(() => {
  mediaQuery?.removeEventListener?.('change', syncViewport);
});

// ===== Computed =====
const userFertilizers = computed(() => props.fertilizers.filter((f) => !f.isSystemDefault));
const isAdjuster = (f: Fertilizer) => !!(f.isAcid || f.isBase);
const hasAcidFertilizers = computed(() => userFertilizers.value.some(isAdjuster));

const isCompany = (f: Fertilizer) => !!f.brand && f.brand.trim() !== '' && f.brand.trim() !== 'استاندارد';
const kindLabel = (f: Fertilizer) => (f.isBase ? 'باز' : f.isAcid ? 'اسید' : isCompany(f) ? 'شرکتی' : 'کود');
const kindClass = (f: Fertilizer) =>
  f.isBase
    ? 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300'
    : f.isAcid
      ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
      : isCompany(f)
        ? 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300'
        : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400';

const fmtNum = (n: number) => new Intl.NumberFormat('fa-IR', { maximumFractionDigits: 3 }).format(n);
const amountLabel = (id: string) => {
  const fa = props.fixedAmounts[id];
  return fa ? `${fmtNum(fa.amount)} ${unitLabel(fa.unit)}` : 'تعیین مقدار';
};

// ===== مودال مقدار اسید/باز =====
const modalFertilizer = ref<Fertilizer | null>(null);
const modalEditing = ref(false);
const modalOpen = ref(false);

const openModal = (f: Fertilizer, editing = false) => {
  modalFertilizer.value = f;
  modalEditing.value = editing;
  modalOpen.value = true;
};
const closeModal = () => {
  modalOpen.value = false;
  modalFertilizer.value = null;
};
const onModalConfirm = (v: { amount: number; unit: AmountUnit }) => {
  const f = modalFertilizer.value;
  if (!f) return;
  emit('update:fixedAmounts', { ...props.fixedAmounts, [f.id]: v });
  if (!props.selectedFertilizers.includes(f.id)) commit([...props.selectedFertilizers, f.id]);
  closeModal();
};

const selectedList = computed(() =>
  props.selectedFertilizers
    .map((id) => userFertilizers.value.find((f) => f.id === id))
    .filter(Boolean) as Fertilizer[]
);

const availableList = computed(() =>
  userFertilizers.value.filter((f) => !props.selectedFertilizers.includes(f.id))
);

// ===== 🆕 جستجوی هوشمند: نام، برند، فرمول، عنصر (نماد یا نام فارسی)، اسید/باز، شکل کود =====
const EL_ALIASES: Record<string, string[]> = {
  'N-NO3': ['n-no3', 'no3', 'نیترات', 'نیتروژن نیتراتی'],
  'N-NH4': ['n-nh4', 'nh4', 'آمونیوم', 'نیتروژن آمونیومی'],
  P: ['p', 'فسفر', 'فسفات'],
  K: ['k', 'پتاسیم'],
  Ca: ['ca', 'کلسیم'],
  Mg: ['mg', 'منیزیم'],
  S: ['s', 'گوگرد', 'سولفات'],
  Na: ['na', 'سدیم'],
  Cl: ['cl', 'کلر', 'کلرید'],
  Fe: ['fe', 'آهن'],
  Mn: ['mn', 'منگنز'],
  Zn: ['zn', 'روی'],
  B: ['b', 'بور'],
  Cu: ['cu', 'مس'],
  Mo: ['mo', 'مولیبدن'],
  Si: ['si', 'سیلیسیم', 'سیلیس']
};
const FORM_ALIASES: Record<string, string[]> = {
  liquid: ['مایع', 'liquid'],
  powder: ['پودر', 'powder'],
  crystal: ['کریستال', 'بلوری', 'crystal'],
  granular: ['granular', 'گرانول', 'دانه‌ای', 'دانه ای']
};
const norm = (t: string) => t.toLowerCase().replace(/[ي]/g, 'ی').replace(/[ك]/g, 'ک').replace(/\u200c/g, ' ').trim();

/** یک عبارت (توکن) با یک کود می‌خواند؟ «Ca»، «کلسیم»، «ca>15» (حداقل درصد عنصر)، «اسید»، «مایع»، نام/فرمول/برند */
const tokenMatches = (f: Fertilizer, raw: string): boolean => {
  const t = norm(raw);
  if (!t) return true;
  const els: Record<string, number> = ((f as any).elements || {}) as Record<string, number>;

  // شرط مقدار: ca>15 ، k>=20 ، n-no3<5
  const cmp = t.match(/^([a-z0-9\-\u0600-\u06ff]+)\s*(>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)$/);
  if (cmp) {
    const key = Object.keys(EL_ALIASES).find((k) => EL_ALIASES[k].includes(cmp[1]));
    if (!key) return false;
    const v = Number(els[key]) || 0;
    const n = Number(cmp[3]);
    return cmp[2] === '>' ? v > n : cmp[2] === '>=' ? v >= n : cmp[2] === '<' ? v < n && v > 0 : cmp[2] === '<=' ? v <= n && v > 0 : v === n;
  }

  // عنصر (تطبیق دقیق نماد/نام؛ فقط اگر کود آن عنصر را داشته باشد)
  for (const [key, aliases] of Object.entries(EL_ALIASES)) {
    if (aliases.includes(t)) return (Number(els[key]) || 0) > 0;
  }
  if (['اسید', 'acid'].includes(t)) return !!(f as any).isAcid;
  if (['باز', 'base'].includes(t)) return !!(f as any).isBase;
  for (const [form, aliases] of Object.entries(FORM_ALIASES)) {
    if (aliases.includes(t)) return (f as any).form === form;
  }
  if (['کلاته', 'chelate', 'chelated'].includes(t)) return /کلات|edta|dtpa|eddha|chelate/i.test(f.name || '');

  const hay = norm([f.name, (f as any).brand, (f as any).formula].filter(Boolean).join(' '));
  return hay.includes(t);
};

const filteredAvailable = computed(() => {
  const tokens = searchQuery.value.split(/[\s,،+]+/).filter(Boolean);
  if (!tokens.length) return availableList.value;
  return availableList.value.filter((f) => tokens.every((t) => tokenMatches(f, t)));
});

const emptyAvailableTitle = computed(() => {
  if (searchQuery.value) return 'کودی با این عبارت پیدا نشد';
  if (userFertilizers.value.length === 0) return 'هنوز کود شخصی ثبت نکرده‌اید';
  return 'همه کودها انتخاب شده‌اند';
});

const emptyAvailableHint = computed(() => {
  if (searchQuery.value) return 'عبارت جستجو را تغییر دهید';
  if (userFertilizers.value.length === 0) return 'ابتدا از بخش پایگاه داده کود، کودهای خود را اضافه کنید';
  return '';
});

// ===== Helpers =====
const mainElements = (fertilizer: Fertilizer): Array<{ symbol: string; value: number }> => {
  if (!fertilizer.elements) return [];
  return Object.entries(fertilizer.elements)
    .filter(([, value]) => Number(value) > 0)
    .map(([symbol, value]) => ({ symbol, value: Number(value) }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);
};

const commit = (ids: string[]) => emit('update:selectedFertilizers', ids);

// ===== Actions =====
const addFertilizer = (id: string) => {
  if (props.selectedFertilizers.includes(id)) return;
  const f = userFertilizers.value.find((x) => x.id === id);
  // اسید/باز: ابتدا مقدار مصرفی را می‌پرسیم (کاربر ممکن است انصراف دهد)
  if (f && isAdjuster(f)) {
    openModal(f, false);
    return;
  }
  commit([...props.selectedFertilizers, id]);
};

const removeFertilizer = (id: string) => {
  commit(props.selectedFertilizers.filter((item) => item !== id));
  if (props.fixedAmounts[id]) {
    const next = { ...props.fixedAmounts };
    delete next[id];
    emit('update:fixedAmounts', next);
  }
};

const selectAll = () => {
  // اسید/باز فقط وقتی اضافه می‌شوند که گزینهٔ «تنظیمات پیشرفته» روشن باشد؛
  // چون مقدار آن‌ها را کاربر باید خودش مشخص کند، «افزودن همه» فقط کودهای معمولی را اضافه
  // می‌کند و اگر اسید/باز هم روشن باشد، مقدارِ تعیین‌نشده‌ها بعداً با مودال پرسیده می‌شود.
  const normal = userFertilizers.value.filter((f) => !isAdjuster(f)).map((f) => f.id);
  const keepAdjusters = props.selectedFertilizers.filter((id) => {
    const f = userFertilizers.value.find((x) => x.id === id);
    return f && isAdjuster(f);
  });
  commit([...new Set([...normal, ...keepAdjusters])]);
  if (props.includeAcidsBases) {
    const pending = userFertilizers.value.filter((f) => isAdjuster(f) && !props.fixedAmounts[f.id]);
    pendingQueue.value = pending.slice(1);
    if (pending.length) openModal(pending[0], false);
  }
};

// صف اسید/بازهایی که بعد از «افزودن همه» باید مقدارشان پرسیده شود
const pendingQueue = ref<Fertilizer[]>([]);
const onModalCancelWrapped = () => {
  closeModal();
  const next = pendingQueue.value.shift();
  if (next) openModal(next, false);
};
const onModalConfirmWrapped = (v: { amount: number; unit: AmountUnit }) => {
  onModalConfirm(v);
  const next = pendingQueue.value.shift();
  if (next) openModal(next, false);
};

const clearAll = () => {
  pendingQueue.value = [];
  commit([]);
  emit('update:fixedAmounts', {});
};

// ===== Drag & Drop (فقط دسکتاپ) =====
const onDragStart = (id: string, from: Pane, event: DragEvent) => {
  if (!isDesktop.value) return;
  draggingId.value = id;
  draggingFrom.value = from;
  event.dataTransfer?.setData('text/plain', id);
  if (event.dataTransfer) event.dataTransfer.effectAllowed = 'move';
};

const onDragEnd = () => {
  draggingId.value = null;
  draggingFrom.value = null;
  dropTarget.value = null;
  hoverIndex.value = null;
};

const onDragOver = (pane: Pane) => {
  if (!draggingId.value) return;
  dropTarget.value = pane;
};

const onDragLeave = (pane: Pane) => {
  if (dropTarget.value === pane) dropTarget.value = null;
};

const onItemDragOver = (index: number) => {
  if (draggingFrom.value !== 'selected') return;
  hoverIndex.value = index;
};

const onDrop = (pane: Pane) => {
  const id = draggingId.value;
  const from = draggingFrom.value;
  const targetIndex = hoverIndex.value;
  onDragEnd();

  if (!id || !from) return;

  if (pane === 'selected') {
    if (from === 'available') {
      addFertilizer(id);
      return;
    }
    // جابه‌جایی ترتیب داخل ستون انتخاب‌شده‌ها
    if (targetIndex === null) return;
    const ids = [...props.selectedFertilizers];
    const currentIndex = ids.indexOf(id);
    if (currentIndex === -1 || currentIndex === targetIndex) return;
    ids.splice(currentIndex, 1);
    ids.splice(targetIndex, 0, id);
    commit(ids);
    return;
  }

  if (pane === 'available' && from === 'selected') {
    removeFertilizer(id);
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 999px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
:global(.dark) .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
</style>
