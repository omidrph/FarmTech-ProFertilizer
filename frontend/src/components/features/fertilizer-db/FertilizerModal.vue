<!-- frontend/src/components/features/fertilizer-db/FertilizerModal.vue -->
<template>
  <AppModal :open="isOpen" size="xl" :title="isEditing ? 'ویرایش کود' : 'افزودن کود'" @close="$emit('close')">
    <template #icon>
      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </template>

    <!-- ===== خلاصهٔ زندهٔ کود ===== -->
    <div class="mb-4 rounded-2xl border border-primary-100 dark:border-primary-900/40 bg-gradient-to-l from-primary-50 via-white to-emerald-50 dark:from-primary-900/20 dark:via-gray-800 dark:to-emerald-900/10 p-3.5 flex items-center gap-3">
      <span class="w-11 h-11 rounded-xl bg-gradient-to-br from-primary-500 to-emerald-500 shadow-md shadow-primary-500/20 flex items-center justify-center flex-shrink-0">
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="S.elements.icon" /></svg>
      </span>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-bold text-gray-900 dark:text-white truncate">{{ formData.name || 'کود جدید' }}</p>
        <p v-if="formData.formula" dir="ltr" class="text-xs text-gray-500 dark:text-gray-400 text-right truncate">{{ formData.formula }}</p>
        <div class="flex flex-wrap gap-1.5 mt-1.5">
          <span v-if="formData.form" class="text-[10px] px-2 py-0.5 rounded-full bg-white/80 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300">{{ formLabel }}</span>
          <span v-if="kind === 'acid'" class="text-[10px] px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300">اسید</span>
          <span v-if="kind === 'base'" class="text-[10px] px-2 py-0.5 rounded-full bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300">باز</span>
          <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300">{{ filledCount.toLocaleString('fa-IR') }} عنصر</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-5 items-start">
      <!-- ===== مشخصات ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <div :class="stripCls(S.identity)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.identity)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.identity.icon" /></svg></span>
          <div>
            <h4 :class="titleCls">مشخصات</h4>
            <p :class="descCls">نام و فرمول را جدا بنویسید تا کود در فهرست راحت‌تر پیدا شود.</p>
          </div>
        </header>
        <div>
          <label :class="labelCls">نام کود <span class="text-danger-500">*</span></label>
          <input type="text" v-model="formData.name" @focus="isTouched = true" :class="[inputCls, !formData.name && isTouched ? '!border-danger-400 !ring-2 !ring-danger-200' : '']" />
          <p v-if="!formData.name && isTouched" class="text-[11px] text-danger-600 mt-1">نام کود را وارد کنید</p>
        </div>
        <div>
          <label :class="labelCls">فرمول</label>
          <input type="text" dir="ltr" v-model="formData.formula" @blur="formData.formula = prettyFormula(formData.formula || '')" :class="[inputCls, 'text-left']" />
          <p class="text-[11px] text-gray-400 mt-1">اعداد به‌صورت خودکار زیرنویس می‌شوند.</p>
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
        <div v-if="formData.form === 'liquid'" class="rounded-xl bg-sky-50/70 dark:bg-sky-900/10 border border-sky-100 dark:border-sky-800/40 p-3">
          <label :class="labelCls">چگالی (g/mL)</label>
          <input type="number" v-model.number="formData.density_g_ml" min="0" max="5" step="0.001" dir="ltr" :class="[inputCls, 'text-left']" />
          <p class="text-[11px] text-sky-700/80 dark:text-sky-300/80 mt-1.5 leading-5">با ثبت چگالی، مصرف کود به لیتر و میلی‌لیتر هم نشان داده می‌شود. درصد عناصر را «وزنی» (گرم در ۱۰۰ گرم محلول) وارد کنید.</p>
        </div>
      </section>

      <!-- ===== عناصر ===== -->
      <section :class="cardCls" class="lg:col-start-2 lg:row-start-1 lg:row-span-4">
        <div :class="stripCls(S.elements)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.elements)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.elements.icon" /></svg></span>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <h4 :class="titleCls">عناصر</h4>
              <button type="button" @click="clearEntries" class="text-xs text-gray-400 hover:text-danger-600 transition-colors">پاک کردن</button>
            </div>
            <p :class="descCls">مقدار را همان‌طور که روی برچسب نوشته شده وارد کنید. برای تغییر فرم (مثلاً اکسید یا تک‌عنصر) روی نام عنصر بزنید؛ برنامه خودش به عنصر خالص تبدیل می‌کند.</p>
          </div>
        </header>

        <!-- نوار مجموع -->
        <div>
          <div class="h-2 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
            <div class="h-full rounded-full transition-all duration-500" :class="totalElementsPercentage > 100 ? 'bg-danger-500' : 'bg-gradient-to-l from-emerald-400 to-emerald-600'" :style="{ width: Math.min(totalElementsPercentage, 100) + '%' }"></div>
          </div>
          <p class="text-[11px] mt-1" :class="totalElementsPercentage > 100 ? 'text-danger-600 dark:text-danger-400 font-medium' : 'text-gray-500 dark:text-gray-400'">
            {{ totalElementsPercentage > 100 ? 'مجموع عناصر از ۱۰۰٪ بیشتر است؛ مقدارها را بررسی کنید.' : `مجموع عنصر خالص: ${totalElementsPercentage.toLocaleString('fa-IR')}٪ از ۱۰۰٪` }}
          </p>
        </div>

        <template v-for="group in groups" :key="group.title">
          <p class="flex items-center gap-2 text-[11px] font-semibold text-gray-500 dark:text-gray-400 pt-1">
            <span class="h-px flex-1 bg-gray-200 dark:bg-gray-700"></span>{{ group.title }}<span class="h-px flex-1 bg-gray-200 dark:bg-gray-700"></span>
          </p>
          <div class="space-y-2">
            <div v-for="def in group.items" :key="def.key" class="relative">
              <div class="flex items-center gap-2">
                <button type="button" @click="openMenu = openMenu === def.key ? null : def.key"
                  class="flex-1 min-w-0 h-10 flex items-center gap-2 px-3 rounded-xl border transition-all duration-200"
                  :class="rowCls(def)">
                  <span class="w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-bold flex-shrink-0" :class="symbolCls(def)" dir="ltr">{{ def.symbol }}</span>
                  <span class="truncate text-sm text-gray-800 dark:text-gray-100">{{ def.name }}</span>
                  <span class="mr-auto flex items-center gap-0.5 text-xs font-semibold text-primary-600 dark:text-primary-400" dir="ltr">
                    {{ currentForm(def).label }}
                    <svg class="w-3 h-3 transition-transform" :class="openMenu === def.key ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </button>
                <input type="number" v-model.number="entries[def.key].value" step="0.01" min="0" max="100" dir="ltr" placeholder="۰"
                  class="w-24 h-10 px-2 text-sm text-center border rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
                  :class="Number(entries[def.key].value) > 0 ? 'border-emerald-300 dark:border-emerald-700 font-semibold' : 'border-gray-300 dark:border-gray-600'" />
              </div>
              <p v-if="Number(entries[def.key].value) > 0 && currentForm(def).factor !== 1" class="text-[11px] text-gray-500 dark:text-gray-400 mt-1 pr-1">
                معادل <span class="font-semibold text-emerald-700 dark:text-emerald-400">{{ pct(def).toLocaleString('fa-IR') }}٪</span> {{ def.symbol }} خالص
              </p>

              <Transition name="pop">
                <div v-if="openMenu === def.key" class="absolute z-30 inset-x-0 top-full mt-1 rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-xl p-1">
                  <button v-for="fm in def.forms" :key="fm.key" type="button" @click="selectForm(def, fm.key)"
                    class="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-lg text-sm transition-colors hover:bg-gray-50 dark:hover:bg-gray-700"
                    :class="entries[def.key].form === fm.key ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'">
                    <span class="flex items-center gap-2">
                      <svg v-if="entries[def.key].form === fm.key" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                      <span v-else class="w-3.5"></span>
                      {{ fm.hint }}
                    </span>
                    <span class="font-semibold" dir="ltr">{{ fm.label }}</span>
                  </button>
                </div>
              </Transition>
              <div v-if="openMenu === def.key" class="fixed inset-0 z-20" @click="openMenu = null"></div>
            </div>
          </div>
        </template>
      </section>

      <!-- ===== قیمت ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <div :class="stripCls(S.price)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.price)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.price.icon" /></svg></span>
          <div>
            <h4 :class="titleCls">قیمت <span class="text-[11px] font-normal text-gray-400 mr-1">اختیاری</span></h4>
            <p :class="descCls">فقط برای محاسبهٔ هزینهٔ فرمول و حالت کم‌هزینه استفاده می‌شود.</p>
          </div>
        </header>
        <div class="flex items-center gap-2">
          <input type="number" v-model.number="formData.price_per_kg" min="0" dir="ltr" :class="[inputCls, 'text-left flex-1']" />
          <span class="text-xs text-gray-500 whitespace-nowrap">{{ priceLabel }}</span>
        </div>
        <div v-if="formData.form === 'liquid'" class="grid grid-cols-2 gap-1.5">
          <button v-for="opt in priceUnitOptions" :key="opt.value" type="button" @click="formData.price_unit = opt.value"
            class="h-9 rounded-xl border text-xs font-medium transition-all"
            :class="formData.price_unit === opt.value ? 'border-amber-400 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 shadow-sm' : 'border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400'">
            {{ opt.label }}
          </button>
        </div>
      </section>

      <!-- ===== تنظیم‌کنندهٔ pH ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <div :class="stripCls(S.ph)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.ph)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.ph.icon" /></svg></span>
          <div>
            <h4 :class="titleCls">تنظیم pH</h4>
            <p :class="descCls">اگر از این ماده برای پایین‌آوردن یا بالابردن pH محلول استفاده می‌کنید، نوع آن را انتخاب کنید.</p>
          </div>
        </header>
        <div class="grid grid-cols-3 gap-1.5">
          <button v-for="opt in kindOptions" :key="opt.value" type="button" @click="setKind(opt.value)"
            class="h-10 rounded-xl border text-sm font-medium transition-all"
            :class="kind === opt.value ? opt.active : 'border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:border-gray-300'">
            {{ opt.label }}
          </button>
        </div>
        <Transition name="pop">
          <div v-if="kind !== 'none'" class="rounded-xl p-3 space-y-3 border" :class="kind === 'acid' ? 'bg-amber-50/60 dark:bg-amber-900/10 border-amber-100 dark:border-amber-800/40' : 'bg-sky-50/60 dark:bg-sky-900/10 border-sky-100 dark:border-sky-800/40'">
            <p class="text-[11px] leading-5 text-gray-600 dark:text-gray-400">این سه مقدار برای محاسبهٔ دقیق قدرت خنثی‌سازی لازم است و از برگهٔ مشخصات ماده یا فرمول آن به‌دست می‌آید.</p>
            <div class="grid grid-cols-2 gap-3">
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
                <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">{{ kind === 'acid' ? 'تعداد پروتون‌هایی که هر مولکول اسید آزاد می‌کند.' : 'تعداد یون هیدروکسید (یا معادل آن) که هر مولکول باز تأمین می‌کند.' }}</p>
              </div>
            </div>
          </div>
        </Transition>
      </section>

      <!-- ===== اطلاعات بیشتر ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <div :class="stripCls(S.more)"></div>
        <button type="button" @click="showMore = !showMore" class="flex items-center justify-between w-full gap-2.5">
          <span class="flex items-center gap-2.5">
            <span :class="badgeCls(S.more)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.more.icon" /></svg></span>
            <span class="text-right">
              <span :class="titleCls" class="block">اطلاعات بیشتر</span>
              <span :class="descCls" class="block">دسته‌بندی و توضیحات (اختیاری)</span>
            </span>
          </span>
          <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showMore ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
        </button>
        <Transition name="pop">
          <div v-if="showMore" class="space-y-3">
            <div>
              <label :class="labelCls">دسته‌بندی</label>
              <input type="text" v-model="formData.category" :class="inputCls" />
            </div>
            <div>
              <label :class="labelCls">توضیحات</label>
              <textarea v-model="formData.description" rows="2" :class="inputCls"></textarea>
            </div>
          </div>
        </Transition>
      </section>
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
const cardCls = 'relative overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800/60 shadow-sm p-4 space-y-3';
const descCls = 'text-[11px] leading-5 text-gray-500 dark:text-gray-400 mt-0.5';

// رنگ و آیکون هر بخش (کلاس‌ها کامل نوشته شده‌اند تا Tailwind آن‌ها را حذف نکند)
const S = {
  identity: { icon: 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z',
    badge: 'bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400', strip: 'from-primary-500 to-primary-300' },
  elements: { icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    badge: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400', strip: 'from-emerald-500 to-emerald-300' },
  price: { icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    badge: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400', strip: 'from-amber-500 to-amber-300' },
  ph: { icon: 'M12 3.5s6 6.2 6 10.5a6 6 0 11-12 0c0-4.3 6-10.5 6-10.5z',
    badge: 'bg-sky-100 text-sky-600 dark:bg-sky-900/30 dark:text-sky-400', strip: 'from-sky-500 to-sky-300' },
  more: { icon: 'M4 6h16M4 12h16M4 18h7',
    badge: 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400', strip: 'from-gray-400 to-gray-200' },
};
const badgeCls = (x: { badge: string }) => `w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${x.badge}`;
const stripCls = (x: { strip: string }) => `absolute inset-x-0 top-0 h-1 bg-gradient-to-l ${x.strip}`;

const formLabel = computed(() => ({ liquid: 'مایع', powder: 'پودری', crystal: 'کریستالی', granular: 'گرانول' } as Record<string, string>)[props.formData.form] || '');
const filledCount = computed(() => ELEMENT_DEFS.filter((d) => Number(entries[d.key].value) > 0).length);

// ظاهر ردیف عنصر: پس از وارد کردن مقدار، با رنگ کاتیون/آنیون پررنگ می‌شود
const rowCls = (d: ElementDef) => {
  const filled = Number(entries[d.key].value) > 0;
  if (!filled) return 'border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50 hover:border-primary-400';
  return d.type === 'cation'
    ? 'border-blue-300 dark:border-blue-700 bg-blue-50/70 dark:bg-blue-900/20'
    : 'border-red-300 dark:border-red-700 bg-red-50/70 dark:bg-red-900/20';
};
const symbolCls = (d: ElementDef) =>
  d.type === 'cation'
    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300'
    : 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300';

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
  { value: 'none', label: 'ندارد', active: 'border-gray-400 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 shadow-sm' },
  { value: 'acid', label: 'اسید', active: 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 shadow-sm' },
  { value: 'base', label: 'باز', active: 'border-sky-500 bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300 shadow-sm' },
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
.pop-enter-active, .pop-leave-active { transition: opacity .18s ease, transform .18s ease; }
.pop-enter-from, .pop-leave-to { opacity: 0; transform: translateY(-4px) scale(.98); }
</style>
