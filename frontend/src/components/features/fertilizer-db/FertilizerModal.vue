<!-- frontend/src/components/features/fertilizer-db/FertilizerModal.vue -->
<template>
  <AppModal :open="isOpen" size="xl" :title="isEditing ? 'ویرایش کود' : 'افزودن کود'" @close="$emit('close')">
    <template #icon>
      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </template>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-5 items-start">
      <!-- ===== مشخصات ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <h4 :class="titleCls">مشخصات</h4>
        <div>
          <label :class="labelCls">نام کود <span class="text-danger-500">*</span></label>
          <input type="text" v-model="formData.name" @focus="isTouched = true" :class="[inputCls, !formData.name && isTouched ? '!border-danger-400' : '']" />
        </div>
        <div>
          <label :class="labelCls">فرمول</label>
          <input type="text" dir="ltr" v-model="formData.formula" @blur="formData.formula = prettyFormula(formData.formula || '')" :class="[inputCls, 'text-left']" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label :class="labelCls">شرکت</label>
            <input type="text" v-model="formData.brand" :class="inputCls" />
          </div>
          <div>
            <label :class="labelCls">فرم</label>
            <select v-model="formData.form" :class="inputCls">
              <option value="">—</option>
              <option value="powder">پودری</option>
              <option value="crystal">کریستالی</option>
              <option value="granular">گرانول</option>
              <option value="liquid">مایع</option>
            </select>
          </div>
        </div>
        <div v-if="formData.form === 'liquid'">
          <label :class="labelCls">چگالی (g/mL)</label>
          <input type="number" v-model.number="formData.density_g_ml" min="0" max="5" step="0.001" dir="ltr" :class="[inputCls, 'text-left']" />
        </div>
      </section>

      <!-- ===== عناصر ===== -->
      <section :class="cardCls" class="lg:col-start-2 lg:row-start-1 lg:row-span-4">
        <div class="flex items-center justify-between">
          <h4 :class="titleCls">
            عناصر
            <span v-if="formData.form === 'liquid'" class="text-[11px] font-normal text-gray-400 mr-1">درصد وزنی</span>
          </h4>
          <button type="button" @click="clearEntries" class="text-xs text-gray-400 hover:text-danger-600 transition-colors">پاک کردن</button>
        </div>

        <p v-if="totalElementsPercentage > 100" class="text-xs text-danger-600 dark:text-danger-400">مجموع عناصر از ۱۰۰٪ بیشتر است</p>

        <template v-for="group in groups" :key="group.title">
          <p class="text-[11px] font-semibold text-gray-400 pt-1">{{ group.title }}</p>
          <div class="space-y-2">
            <div v-for="def in group.items" :key="def.key" class="relative">
              <div class="flex items-center gap-2">
                <button type="button" @click="openMenu = openMenu === def.key ? null : def.key"
                  class="flex-1 min-w-0 h-10 flex items-center gap-2 px-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50 hover:border-primary-400 transition-colors">
                  <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" :class="def.type === 'cation' ? 'bg-blue-400' : 'bg-red-400'"></span>
                  <span class="truncate text-sm text-gray-800 dark:text-gray-100">{{ def.name }}</span>
                  <span class="mr-auto flex items-center gap-0.5 text-xs font-semibold text-primary-600 dark:text-primary-400" dir="ltr">
                    {{ currentForm(def).label }}
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </button>
                <input type="number" v-model.number="entries[def.key].value" step="0.01" min="0" max="100" dir="ltr" placeholder="۰"
                  class="w-24 h-10 px-2 text-sm text-center border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
              </div>

              <template v-if="openMenu === def.key">
                <div class="fixed inset-0 z-20" @click="openMenu = null"></div>
                <div class="absolute z-30 inset-x-0 top-full mt-1 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-lg p-1">
                  <button v-for="fm in def.forms" :key="fm.key" type="button" @click="selectForm(def, fm.key)"
                    class="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-md text-sm transition-colors hover:bg-gray-50 dark:hover:bg-gray-700"
                    :class="entries[def.key].form === fm.key ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'">
                    <span>{{ fm.hint }}</span>
                    <span class="font-semibold" dir="ltr">{{ fm.label }}</span>
                  </button>
                </div>
              </template>
            </div>
          </div>
        </template>
      </section>

      <!-- ===== قیمت ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <h4 :class="titleCls">قیمت <span class="text-[11px] font-normal text-gray-400 mr-1">اختیاری</span></h4>
        <div class="flex items-center gap-2">
          <input type="number" v-model.number="formData.price_per_kg" min="0" dir="ltr" :class="[inputCls, 'text-left flex-1']" />
          <span class="text-xs text-gray-500 whitespace-nowrap">{{ priceLabel }}</span>
        </div>
        <div v-if="formData.form === 'liquid'" class="grid grid-cols-2 gap-1.5">
          <button v-for="opt in priceUnitOptions" :key="opt.value" type="button" @click="formData.price_unit = opt.value"
            class="h-8 rounded-lg border text-xs font-medium transition-colors"
            :class="formData.price_unit === opt.value ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400'">
            {{ opt.label }}
          </button>
        </div>
      </section>

      <!-- ===== تنظیم‌کنندهٔ pH ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <h4 :class="titleCls">تنظیم pH</h4>
        <div class="grid grid-cols-3 gap-1.5">
          <button v-for="opt in kindOptions" :key="opt.value" type="button" @click="setKind(opt.value)"
            class="h-9 rounded-lg border text-sm font-medium transition-colors"
            :class="kind === opt.value ? opt.active : 'border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400'">
            {{ opt.label }}
          </button>
        </div>
        <div v-if="kind !== 'none'" class="grid grid-cols-2 gap-3">
          <div>
            <label :class="labelCls">غلظت (٪ وزنی)</label>
            <input type="number" v-model.number="formData.ph_purity" min="0" max="100" step="0.1" dir="ltr" :class="[inputCls, 'text-left']" />
          </div>
          <div>
            <label :class="labelCls">جرم مولی (g/mol)</label>
            <input type="number" v-model.number="formData.ph_mw" min="0" step="0.01" dir="ltr" :class="[inputCls, 'text-left']" />
          </div>
          <div class="col-span-2">
            <label :class="labelCls">{{ kind === 'acid' ? 'تعداد H⁺ در هر مولکول' : 'تعداد OH⁻ در هر مولکول' }}</label>
            <input type="number" v-model.number="formData.ph_eq" min="0" step="0.1" dir="ltr" :class="[inputCls, 'text-left']" />
          </div>
        </div>
      </section>

      <!-- ===== اطلاعات بیشتر ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <button type="button" @click="showMore = !showMore" class="flex items-center justify-between w-full">
          <h4 :class="titleCls">اطلاعات بیشتر</h4>
          <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showMore ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </button>
        <template v-if="showMore">
          <div>
            <label :class="labelCls">دسته‌بندی</label>
            <input type="text" v-model="formData.category" :class="inputCls" />
          </div>
          <div>
            <label :class="labelCls">توضیحات</label>
            <textarea v-model="formData.description" rows="2" :class="inputCls"></textarea>
          </div>
        </template>
      </section>
    </div>

    <template #footer>
      <div class="app-modal-actions">
        <button type="button" @click="$emit('close')" class="app-modal-btn app-modal-btn-secondary">انصراف</button>
        <button type="button" @click="handleSave" :disabled="isSaving || !formData.name || totalElementsPercentage > 100" class="app-modal-btn app-modal-btn-primary">
          {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره' : 'افزودن') }}
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
    ph_purity: number | null;
    ph_mw: number | null;
    ph_eq: number | null;
    description: string;
    is_system_default: boolean;
    source_system_id: number | null;
    density_g_ml: number | null;
    price_unit: 'kg' | 'l';
  };
  isSaving: boolean;
}>();

const emit = defineEmits<{ (e: 'close'): void; (e: 'save'): void }>();

const inputCls = 'w-full px-3 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all';
const labelCls = 'block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1';
const titleCls = 'text-sm font-semibold text-gray-900 dark:text-white';
const cardCls = 'rounded-xl border border-gray-200 dark:border-gray-700 p-3.5 space-y-3';

const isTouched = ref(false);
const openMenu = ref<string | null>(null);
const showMore = ref(false);

const groups = [
  { title: 'پرمصرف', items: ELEMENT_DEFS.slice(0, 7) },
  { title: 'کم‌مصرف و سایر', items: ELEMENT_DEFS.slice(7) },
];

const entries = reactive<Record<string, { form: string; value: number | null }>>({});
const resetEntries = () => {
  for (const d of ELEMENT_DEFS) entries[d.key] = { form: d.defaultForm, value: null };
};
resetEntries();

const pureFormKey = (d: ElementDef) => (d.key.startsWith('N-') ? 'N' : d.key);

watch(() => props.isOpen, (open) => {
  if (!open) return;
  isTouched.value = false;
  openMenu.value = null;
  showMore.value = !!(props.formData.category || props.formData.description);
  resetEntries();
  const lv = props.formData.label_values || {};
  const purity = Number(props.formData.concentration) || 100;
  for (const d of ELEMENT_DEFS) {
    const hit = Object.keys(lv).find((k) => k.startsWith(d.key + '|'));
    if (hit) {
      entries[d.key] = { form: hit.split('|')[1], value: Number(lv[hit]) };
    } else if (Number(props.formData.elements?.[d.key]) > 0) {
      const v = Number(props.formData.elements[d.key]) * purity / 100;
      entries[d.key] = { form: pureFormKey(d), value: Math.round(v * 10000) / 10000 };
    }
  }
});

const currentForm = (d: ElementDef) => d.forms.find((f) => f.key === entries[d.key].form) || d.forms[0];
const pct = (d: ElementDef) => toElementPct(d.key, entries[d.key].form, Number(entries[d.key].value) || 0);
const selectForm = (d: ElementDef, key: string) => { entries[d.key].form = key; openMenu.value = null; };
const totalElementsPercentage = computed(() => parseFloat(ELEMENT_DEFS.reduce((s, d) => s + pct(d), 0).toFixed(2)));
const clearEntries = () => { if (confirm('همهٔ عناصر پاک شوند؟')) resetEntries(); };

// تنظیم pH: ندارد / اسید / باز
const kind = computed<'none' | 'acid' | 'base'>(() => (props.formData.is_acid ? 'acid' : props.formData.is_base ? 'base' : 'none'));
const kindOptions: Array<{ value: 'none' | 'acid' | 'base'; label: string; active: string }> = [
  { value: 'none', label: 'ندارد', active: 'border-gray-400 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100' },
  { value: 'acid', label: 'اسید', active: 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300' },
  { value: 'base', label: 'باز', active: 'border-sky-500 bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300' },
];
const setKind = (k: 'none' | 'acid' | 'base') => {
  props.formData.is_acid = k === 'acid';
  props.formData.is_base = k === 'base';
};

const priceUnitOptions: Array<{ value: 'kg' | 'l'; label: string }> = [
  { value: 'kg', label: 'هر کیلوگرم' },
  { value: 'l', label: 'هر لیتر' },
];
const priceLabel = computed(() =>
  props.formData.form === 'liquid' && props.formData.price_unit === 'l' ? 'تومان / لیتر' : 'تومان / کیلوگرم');

const handleSave = () => {
  isTouched.value = true;
  if (!props.formData.name || totalElementsPercentage.value > 100) return;

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
  props.formData.concentration = 100;
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
