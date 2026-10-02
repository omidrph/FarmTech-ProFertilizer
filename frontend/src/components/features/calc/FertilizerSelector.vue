
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
          title="کودهای اسیدی به‌عمد اضافه نمی‌شوند؛ اگر لازم دارید عمداً از لیست انتخاب کنید"
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

    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50/70 dark:bg-gray-900/20">
      <label class="flex items-start gap-2 cursor-pointer">
        <input v-model="includeAcidBaseInSelectAll" type="checkbox" class="mt-0.5 w-4 h-4 rounded text-primary-600 focus:ring-primary-500" />
        <span class="min-w-0">
          <span class="block text-xs font-semibold text-gray-700 dark:text-gray-200">افزودن اسیدها و بازها در «افزودن همه»</span>
          <span class="block text-[10px] text-gray-500 dark:text-gray-400 mt-0.5">فقط وقتی فعال کنید که می‌خواهید مواد اصلاح‌کننده pH نیز وارد مجموعه انتخاب خودکار شوند.</span>
        </span>
      </label>
      <p v-if="includeAcidBaseInSelectAll" class="mt-2 text-[10px] text-amber-700 dark:text-amber-400 rounded-lg bg-amber-50 dark:bg-amber-900/20 px-3 py-2">هشدار: اسید و باز علاوه بر تأمین عناصر، روی pH اثر دارند؛ دوز آن‌ها را قبل از محاسبه بررسی کنید.</p>
    </div>

    <!-- 🆕 راهنمای نقش دوگانه‌ی کودهای اسیدی -->
    <div
      v-if="hasAcidFertilizers"
      class="px-4 py-2 border-b border-gray-200 dark:border-gray-700 bg-amber-50/60 dark:bg-amber-900/10 text-[11px] text-amber-800 dark:text-amber-300 leading-5"
    >
      کودهای اسیدی (برچسب «اسید») هم عنصر تأمین می‌کنند هم روی pH اثر می‌گذارند؛ به همین دلیل در «افزودن همه» گنجانده نشده‌اند. اصلاح دقیق pH بعد از ساخت محلول در تب «PH» انجام می‌شود.
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
              placeholder="جستجوی نام یا برند کود..."
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
                    :class="fertilizer.isAcid
                      ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                      : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'"
                    :title="fertilizer.isAcid ? 'این کود اسیدی است؛ هم می‌تواند عنصر تأمین کند هم روی pH اثر بگذارد. اصلاح دقیق pH پس از ساخت محلول در تب «PH» انجام می‌شود.' : undefined"
                  >
                    {{ fertilizer.isAcid ? 'اسید' : 'کود' }}
                  </span>
                  <span v-if="fertilizer.brand" class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400">
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
                    v-if="fertilizer.isAcid"
                    class="text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
                    title="این کود اسیدی است؛ هم می‌تواند عنصر تأمین کند هم روی pH اثر بگذارد."
                  >اسید</span>
                  <span v-if="fertilizer.isBase" class="text-[10px] px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">باز</span>
                  <span
                    v-for="el in mainElements(fertilizer)"
                    :key="el.symbol"
                    class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                  >{{ el.symbol }} {{ el.value }}٪</span>
                </div>
              </div>

              <button
                v-if="props.manualMode"
                type="button"
                @click.stop="openDoseModal(fertilizer)"
                class="px-2 py-1 rounded-md text-[10px] font-medium text-primary-600 bg-primary-50 dark:bg-primary-900/20 dark:text-primary-300"
              >دوز</button>

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

    <div v-if="doseModalFertilizer" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" @click.self="doseModalFertilizer = null">
      <div class="w-full max-w-sm rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-5 shadow-xl" dir="rtl">
        <h4 class="text-base font-bold text-gray-900 dark:text-white">دوز دستی {{ doseModalFertilizer.name }}</h4>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">مقدار این {{ doseModalFertilizer.isAcid ? 'اسید' : 'باز' }} را برای همین محاسبه وارد کنید.</p>
        <div class="mt-4">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1">مقدار ({{ manualDoseUnit }})</label>
          <input v-model.number="manualDose" type="number" min="0" step="0.01" class="w-full rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 px-3 py-2 text-sm" />
        </div>
        <div class="mt-4 flex gap-2 justify-end">
          <button type="button" class="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-600" @click="doseModalFertilizer = null">لغو</button>
          <button type="button" class="px-3 py-2 text-sm rounded-lg bg-primary-600 text-white" @click="() => { if (doseModalFertilizer && manualDose > 0) { emit('update:manualDoses', { [doseModalFertilizer.id]: { value: manualDose, unit: doseModalFertilizer.form === 'liquid' ? 'ml' : 'g' } }); } doseModalFertilizer = null; }">ثبت دوز</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// ===== Types =====
interface Fertilizer {
  id: string;
  name: string;
  brand?: string;
  isAcid: boolean;
  isBase: boolean;
  form?: string;
  densityGPerMl?: number;
  pricePerKg: number;
  concentration?: number;
  elements: Record<string, number>;
  isSystemDefault: boolean;
}

type Pane = 'available' | 'selected';

// ===== Props / Emits =====
const props = defineProps<{
  fertilizers: Fertilizer[];
  selectedFertilizers: string[];
  manualMode?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:selectedFertilizers', value: string[]): void;
  (e: 'update:manualDoses', value: Record<string, { value: number; unit: 'ml' | 'g' }>): void;
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
const includeAcidBaseInSelectAll = ref(false);
const doseModalFertilizer = ref<Fertilizer | null>(null);
const manualDose = ref<number>(0);
const manualDoseUnit = computed(() => doseModalFertilizer.value?.form === 'liquid' ? 'mL' : 'g');

const selectedList = computed(() =>
  props.selectedFertilizers
    .map((id) => userFertilizers.value.find((f) => f.id === id))
    .filter(Boolean) as Fertilizer[]
);

const availableList = computed(() =>
  userFertilizers.value.filter((f) => !props.selectedFertilizers.includes(f.id))
);

const filteredAvailable = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return availableList.value;
  return availableList.value.filter(
    (f) => f.name.toLowerCase().includes(query) || (f.brand || '').toLowerCase().includes(query)
  );
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
const openDoseModal = (fert: Fertilizer) => { doseModalFertilizer.value = fert; manualDose.value = 0; };

const addFertilizer = (id: string) => {
  if (props.selectedFertilizers.includes(id)) return;
  commit([...props.selectedFertilizers, id]);
  const fert = userFertilizers.value.find((f) => f.id === id);
  if (fert && (props.manualMode || fert.isAcid || fert.isBase)) openDoseModal(fert);
};

const removeFertilizer = (id: string) => {
  commit(props.selectedFertilizers.filter((item) => item !== id));
};

const selectAll = () => {
  const list = includeAcidBaseInSelectAll.value
    ? userFertilizers.value
    : userFertilizers.value.filter((f) => !f.isAcid && !f.isBase);
  commit(list.map((f) => f.id));
};

const clearAll = () => commit([]);

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
