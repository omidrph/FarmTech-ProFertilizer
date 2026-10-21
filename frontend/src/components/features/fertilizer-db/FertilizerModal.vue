<!-- frontend/src/components/features/fertilizer-db/FertilizerModal.vue -->
<template>
  <AppModal
    :open="isOpen"
    size="xl"
    :title="isEditing ? 'ویرایش کود' : 'افزودن کود'"
    :subtitle="isEditing ? 'تغییرات را اعمال کنید' : 'اطلاعات کود را همان‌طور که روی برچسب نوشته شده وارد کنید'"
    @close="$emit('close')"
  >
    <template #icon>
      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </template>

    <div v-if="!formData.name && isTouched" class="flex items-center gap-2 p-3 mb-3 rounded-lg bg-danger-50 dark:bg-danger-900/20 border border-danger-200 dark:border-danger-800">
      <span class="text-sm text-danger-700 dark:text-danger-400">نام کود الزامی است</span>
    </div>
    <div v-if="totalElementsPercentage > 100" class="flex items-center gap-2 p-3 mb-3 rounded-lg bg-warning-50 dark:bg-warning-900/20 border border-warning-200 dark:border-warning-800">
      <span class="text-sm text-warning-700 dark:text-warning-400">مجموع درصد عناصر (پس از تبدیل به عنصر) از ۱۰۰ بیشتر است ({{ totalElementsPercentage }}%)؛ فرم یا مقدار را بررسی کنید.</span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5">
      <!-- ============ ستون اطلاعات اصلی ============ -->
      <div class="space-y-3 sm:space-y-4">
        <div>
          <label :class="labelCls">نام کود <span class="text-danger-500">*</span></label>
          <input type="text" v-model="formData.name" @focus="isTouched = true" placeholder="مثال: نیترات پتاسیم" :class="inputCls" />
        </div>

        <div>
          <label :class="labelCls">فرمول کود</label>
          <input type="text" dir="ltr" v-model="formData.formula" @blur="formData.formula = prettyFormula(formData.formula || '')"
            placeholder="KNO3  یا  Ca(NO3)2.4H2O" :class="[inputCls, 'text-left']" />
          <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1">اعداد به‌صورت خودکار زیرنویس می‌شوند (KNO3 ← KNO₃).</p>
        </div>

        <div class="grid grid-cols-2 gap-2 sm:gap-3">
          <div>
            <label :class="labelCls">نام شرکت</label>
            <input type="text" v-model="formData.brand" placeholder="اختیاری" :class="inputCls" />
          </div>
          <div>
            <label :class="labelCls">دسته‌بندی</label>
            <input type="text" list="category-list" v-model="formData.category" placeholder="اختیاری" :class="inputCls" />
            <datalist id="category-list">
              <option value="NPK کامل"></option><option value="نیترات"></option><option value="سولفات"></option>
              <option value="فسفات"></option><option value="کلات"></option><option value="ریزمغذی"></option>
              <option value="اسید"></option><option value="باز"></option>
            </datalist>
          </div>
        </div>

        <div>
          <label :class="labelCls">فرم فیزیکی</label>
          <select v-model="formData.form" :class="inputCls">
            <option value="">انتخاب...</option>
            <option value="powder">پودری</option>
            <option value="crystal">کریستالی</option>
            <option value="liquid">مایع</option>
            <option value="granular">گرانول</option>
          </select>
        </div>

        <!-- کود مایع -->
        <div v-if="formData.form === 'liquid'" class="bg-sky-50/50 dark:bg-sky-900/10 rounded-lg p-3 border border-sky-200 dark:border-sky-800/40 space-y-2.5">
          <p class="text-xs font-semibold text-sky-700 dark:text-sky-300">ویژگی‌های کود مایع</p>
          <div>
            <label class="block text-[11px] font-medium text-gray-600 dark:text-gray-400 mb-1">چگالی (g/mL)</label>
            <input type="number" v-model.number="formData.density_g_ml" min="0" max="5" step="0.001" placeholder="مثلاً ۱٫۲۰" :class="inputCls" />
          </div>
          <p class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">
            درصدها را «درصد وزنی» (گرم در ۱۰۰ گرم محلول) بنویسید. اگر برچسب «گرم در لیتر» (w/v) دارد، آن را بر چگالی تقسیم کنید.
            با ثبت چگالی، مصرف به لیتر/میلی‌لیتر نمایش داده می‌شود.
          </p>
          <div class="grid grid-cols-2 gap-1.5">
            <button v-for="opt in priceUnitOptions" :key="opt.value" type="button" @click="formData.price_unit = opt.value"
              class="h-8 rounded-lg border text-xs font-medium transition-colors"
              :class="formData.price_unit === opt.value ? 'border-sky-500 bg-white dark:bg-gray-800 text-sky-700 dark:text-sky-300' : 'border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400'">
              قیمت {{ opt.label }}
            </button>
          </div>
        </div>

        <div>
          <label :class="labelCls">قیمت ({{ priceLabel }}) <span class="text-gray-400 font-normal">— اختیاری</span></label>
          <input type="number" v-model.number="formData.price_per_kg" min="0" placeholder="اختیاری" :class="inputCls" />
        </div>

        <!-- اسید / باز -->
        <div class="rounded-lg border border-gray-200 dark:border-gray-600 p-3 space-y-2">
          <p class="text-xs font-medium text-gray-700 dark:text-gray-300">تنظیم‌کنندهٔ pH (در صورت نیاز)</p>
          <div class="flex flex-wrap gap-4">
            <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
              <input type="checkbox" :checked="formData.is_acid" @change="toggleAcid(($event.target as HTMLInputElement).checked)" class="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              این کود اسید است
            </label>
            <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
              <input type="checkbox" :checked="formData.is_base" @change="toggleBase(($event.target as HTMLInputElement).checked)" class="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              این کود باز است
            </label>
          </div>
          <p v-if="formData.is_acid || formData.is_base" class="text-[11px] leading-5 text-gray-500 dark:text-gray-400">
            عناصر موجود در ماده را در بخش عناصر وارد کنید{{ formData.form === 'liquid' ? ' و چگالی را بالاتر ثبت کنید' : '' }}؛ اطلاعات دیگری لازم نیست.
          </p>
        </div>

        <div>
          <label :class="labelCls">توضیحات</label>
          <textarea v-model="formData.description" rows="2" placeholder="اختیاری" :class="inputCls"></textarea>
        </div>
      </div>

      <!-- ============ ستون عناصر ============ -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300">عناصر موجود در کود (مطابق برچسب)</label>
          <button type="button" @click="clearEntries" class="text-xs text-gray-500 hover:text-danger-600 transition-colors">پاک کردن</button>
        </div>
        <p class="text-[11px] leading-5 text-gray-500 dark:text-gray-400 mb-3">
          روی نام هر عنصر بزنید تا فرم نوشته‌شده روی برچسب (مثلاً K₂O یا P₂O₅) را انتخاب کنید؛ برنامه خودش به مقدار عنصر خالص تبدیل می‌کند.
        </p>

        <template v-for="group in groups" :key="group.title">
          <p class="text-[11px] font-semibold text-gray-500 dark:text-gray-400 mt-3 mb-1.5">{{ group.title }}</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div v-for="def in group.items" :key="def.key" class="relative">
              <div class="flex items-stretch gap-1.5">
                <button type="button" @click="openMenu = openMenu === def.key ? null : def.key"
                  class="flex-1 min-w-0 flex items-center justify-between gap-1 px-2 py-2 rounded-lg border text-xs font-semibold transition-colors"
                  :class="typeClass(def.type)">
                  <span class="truncate">{{ def.name }}</span>
                  <span class="flex items-center gap-0.5 opacity-80" dir="ltr">
                    {{ currentForm(def).label }}
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </button>
                <input type="number" v-model.number="entries[def.key].value" step="0.01" min="0" max="100" placeholder="۰" dir="ltr"
                  class="w-20 px-2 py-2 text-sm text-center border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
              </div>
              <p v-if="entries[def.key].value && currentForm(def).factor !== 1" class="text-[10px] text-gray-400 mt-0.5 px-1" dir="rtl">
                = {{ pct(def).toLocaleString('fa-IR') }}٪ {{ def.symbol }}
              </p>

              <!-- منوی فرم‌ها -->
              <div v-if="openMenu === def.key" class="fixed inset-0 z-20" @click="openMenu = null"></div>
              <div v-if="openMenu === def.key" class="absolute z-30 top-full mt-1 right-0 w-64 max-w-[85vw] rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-lg p-1">
                <button v-for="fm in def.forms" :key="fm.key" type="button" @click="selectForm(def, fm.key)"
                  class="w-full flex items-center justify-between gap-2 px-2.5 py-2 rounded-md text-right text-xs hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  :class="entries[def.key].form === fm.key ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'">
                  <span class="min-w-0">
                    <span class="font-semibold" dir="ltr">{{ fm.label }}</span>
                    <span class="block text-[10px] text-gray-500 dark:text-gray-400 truncate">{{ fm.hint }}</span>
                  </span>
                  <span class="text-[10px] text-gray-400 whitespace-nowrap" dir="ltr">× {{ fm.factor.toFixed(4) }}</span>
                </button>
              </div>
            </div>
          </div>
        </template>

        <div class="flex items-center justify-between mt-4 text-xs">
          <div class="flex items-center gap-3 text-gray-500">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-blue-400"></span>کاتیون</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>آنیون</span>
          </div>
          <span class="text-gray-600 dark:text-gray-400">
            مجموع عنصر خالص:
            <span class="font-bold" :class="totalElementsPercentage > 100 ? 'text-danger-600' : 'text-gray-900 dark:text-white'">{{ totalElementsPercentage }}%</span>
          </span>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="app-modal-actions">
        <button type="button" @click="$emit('close')" class="app-modal-btn app-modal-btn-secondary">انصراف</button>
        <button type="button" @click="handleSave" :disabled="isSaving || !formData.name || totalElementsPercentage > 100" class="app-modal-btn app-modal-btn-primary">
          {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره تغییرات' : 'افزودن کود') }}
        </button>
      </div>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import AppModal from '@/components/common/AppModal.vue';
import { computed, reactive, ref, watch } from 'vue';
import { ELEMENT_DEFS, toElementPct, labelKey, prettyFormula, type ElementDef } from '@/utils/labelForms';

const props = defineProps<{
  isOpen: boolean;
  isEditing: boolean;
  formData: {
    id: string | null;
    name: string;
    formula: string;
    brand: string;
    category: string;
    form: '' | 'liquid' | 'powder' | 'crystal' | 'granular';
    concentration: number;
    price_per_kg: number | null;
    elements: Record<string, number>;
    label_values: Record<string, number>;
    is_acid: boolean;
    is_base: boolean;
    description: string;
    is_system_default: boolean;
    source_system_id: number | null;
    density_g_ml: number | null;
    price_unit: 'kg' | 'l';
  };
  isSaving: boolean;
}>();

const emit = defineEmits<{ (e: 'close'): void; (e: 'save'): void }>();

const inputCls = 'w-full px-3 sm:px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all';
const labelCls = 'block text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 mb-1';

const isTouched = ref(false);
const openMenu = ref<string | null>(null);

const groups = [
  { title: 'عناصر پرمصرف', items: ELEMENT_DEFS.slice(0, 7) },
  { title: 'عناصر کم‌مصرف و سایر', items: ELEMENT_DEFS.slice(7) },
];

// ورودی‌های فرم: برای هر عنصر، فرم انتخابی و مقدار روی برچسب
const entries = reactive<Record<string, { form: string; value: number | null }>>({});
const resetEntries = () => {
  for (const d of ELEMENT_DEFS) entries[d.key] = { form: d.defaultForm, value: null };
};
resetEntries();

const pureFormKey = (d: ElementDef) => (d.key.startsWith('N-') ? 'N' : d.key);

// هنگام باز شدن مودال، ورودی‌ها را از داده‌های کود پر می‌کنیم
watch(() => props.isOpen, (open) => {
  if (!open) return;
  isTouched.value = false;
  openMenu.value = null;
  resetEntries();
  const lv = props.formData.label_values || {};
  const purity = Number(props.formData.concentration) || 100;
  for (const d of ELEMENT_DEFS) {
    const hit = Object.keys(lv).find((k) => k.startsWith(d.key + '|'));
    if (hit) {
      entries[d.key] = { form: hit.split('|')[1], value: Number(lv[hit]) };
    } else if (Number(props.formData.elements?.[d.key]) > 0) {
      // کودهای قدیمی: مقدار عنصری (ضرب‌شده در خلوص) را به‌صورت عنصر خالص نشان می‌دهیم
      const v = Number(props.formData.elements[d.key]) * purity / 100;
      entries[d.key] = { form: pureFormKey(d), value: Math.round(v * 10000) / 10000 };
    }
  }
});

const currentForm = (d: ElementDef) => d.forms.find((f) => f.key === entries[d.key].form) || d.forms[0];
const pct = (d: ElementDef) => toElementPct(d.key, entries[d.key].form, Number(entries[d.key].value) || 0);
const selectForm = (d: ElementDef, key: string) => { entries[d.key].form = key; openMenu.value = null; };

const totalElementsPercentage = computed(() =>
  parseFloat(ELEMENT_DEFS.reduce((s, d) => s + pct(d), 0).toFixed(2)));

const typeClass = (t: string) =>
  t === 'cation'
    ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800'
    : t === 'anion'
      ? 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800'
      : 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-600';

const clearEntries = () => {
  if (confirm('آیا از پاک کردن تمام عناصر اطمینان دارید؟')) resetEntries();
};

const priceUnitOptions: Array<{ value: 'kg' | 'l'; label: string }> = [
  { value: 'kg', label: 'هر کیلوگرم' },
  { value: 'l', label: 'هر لیتر' },
];
const priceLabel = computed(() =>
  props.formData.form === 'liquid' && props.formData.price_unit === 'l' ? 'تومان / لیتر' : 'تومان / کیلوگرم');

const toggleAcid = (checked: boolean) => { props.formData.is_acid = checked; if (checked) props.formData.is_base = false; };
const toggleBase = (checked: boolean) => { props.formData.is_base = checked; if (checked) props.formData.is_acid = false; };

const handleSave = () => {
  isTouched.value = true;
  if (!props.formData.name || totalElementsPercentage.value > 100) return;

  // تبدیل مقادیر برچسب → عنصر خالص (ذخیره‌سازی همیشه عنصری است)
  const elements: Record<string, number> = {};
  const labels: Record<string, number> = {};
  for (const d of ELEMENT_DEFS) {
    const v = Number(entries[d.key].value) || 0;
    if (v > 0) {
      elements[d.key] = toElementPct(d.key, entries[d.key].form, v);
      labels[labelKey(d.key, entries[d.key].form)] = v;
    }
  }
  props.formData.elements = elements;
  props.formData.label_values = labels;
  props.formData.concentration = 100; // درصدها همان درصد محصول روی برچسب‌اند
  props.formData.formula = prettyFormula(props.formData.formula || '');
  emit('save');
};
</script>

<style scoped>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; appearance: textfield; }
input:focus, select:focus, textarea:focus { outline: none; }
</style>
