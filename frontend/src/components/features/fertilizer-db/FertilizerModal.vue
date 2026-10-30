
<!-- frontend/src/components/features/fertilizer-db/FertilizerModal.vue -->
<template>
  <AppModal :open="isOpen" size="xl" :title="isEditing ? 'ویرایش کود' : 'افزودن کود'" @close="$emit('close')">
    <template #icon>
      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </template>

    <div class="grid grid-cols-1 lg:grid-cols-2 lg:grid-rows-[auto_auto_auto_auto_1fr] gap-4 lg:gap-5 items-start">
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
        <div>
          <label :class="labelCls">درصد خلوص (٪)</label>
          <input type="number" v-model.number="formData.concentration" min="0.1" max="100" step="0.1" dir="ltr" :class="[inputCls, 'text-left']" />
          <p class="text-[11px] text-gray-400 mt-1">درصد عناصر در خلوص ضرب می‌شود.</p>
        </div>
        <div v-if="formData.form === 'liquid'" class="rounded-xl bg-sky-50/70 dark:bg-sky-900/10 border border-sky-100 dark:border-sky-800/40 p-3">
          <label :class="labelCls">چگالی (g/mL)</label>
          <input type="number" v-model.number="formData.density_g_ml" min="0" max="5" step="0.001" dir="ltr" :class="[inputCls, 'text-left']" />
          <p class="text-[11px] text-sky-700/80 dark:text-sky-300/80 mt-1.5 leading-5">با ثبت چگالی، مصرف کود به لیتر و میلی‌لیتر هم نشان داده می‌شود. درصد عناصر را «وزنی» (گرم در ۱۰۰ گرم محلول) وارد کنید.</p>
        </div>
      </section>

      <!-- ===== عناصر ===== -->
      <section :class="cardCls" class="lg:col-start-2 lg:row-start-1 lg:row-span-5">
        <div :class="stripCls(S.elements)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.elements)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.elements.icon" /></svg></span>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <h4 :class="titleCls">عناصر</h4>
              <button type="button" @click="clearEntries" class="text-xs text-gray-400 hover:text-danger-600 transition-colors">پاک کردن</button>
            </div>
            <p :class="descCls">مقدار را مطابق برچسب وارد کنید؛ برای تغییر فرم (اکسید، نمک، کلات، …) روی نام عنصر بزنید. برای ترکیب‌های دلخواه از «پیشرفته» استفاده کنید.</p>
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
                <button type="button" @click="toggleMenu(def, $event)"
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

            </div>
          </div>
        </template>

        <!-- دکمه‌های کلات‌ها و پیشرفته -->
        <div class="grid grid-cols-2 gap-2 pt-1">
          <button type="button" @click="togglePanel('chelate')"
            class="h-10 rounded-xl border text-sm font-medium transition-all flex items-center justify-center gap-1.5"
            :class="panel === 'chelate' ? 'border-violet-400 bg-violet-50 dark:bg-violet-900/20 text-violet-700 dark:text-violet-300 shadow-sm' : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-violet-300'">
            کلات‌ها
            <span v-if="chelateCount" class="min-w-[1.25rem] h-5 px-1 rounded-full bg-violet-600 text-white text-[10px] font-bold flex items-center justify-center tabular-nums">{{ chelateCount.toLocaleString('fa-IR') }}</span>
          </button>
          <button type="button" @click="togglePanel('advanced')"
            class="h-10 rounded-xl border text-sm font-medium transition-all flex items-center justify-center gap-1.5"
            :class="panel === 'advanced' ? 'border-teal-400 bg-teal-50 dark:bg-teal-900/20 text-teal-700 dark:text-teal-300 shadow-sm' : 'border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-teal-300'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281zM15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            پیشرفته
          </button>
        </div>
        <Transition name="pop">
          <ChelatePanel v-if="panel === 'chelate'" :entries="entries" />
          <AdvancedBuilder v-else-if="panel === 'advanced'" :entries="entries" @applied="onAdvancedApplied" />
        </Transition>
      </section>

      <!-- منوی انتخاب فرم (خارج از کارت و با موقعیت ثابت تا هرگز بریده نشود؛ به بالا یا پایین باز می‌شود) -->
      <Teleport to="body">
        <template v-if="menuDef && menuStyle">
          <div class="fixed inset-0 z-[300]" @click="closeMenu"></div>
          <div class="fixed z-[310] overflow-y-auto rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-2xl p-1.5 space-y-0.5" :style="menuStyle" dir="rtl">
            <button v-for="fm in menuDef.forms" :key="fm.key" type="button" @click="selectForm(menuDef, fm.key)"
              class="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-lg text-sm transition-colors hover:bg-gray-50 dark:hover:bg-gray-700"
              :class="entries[menuDef.key].form === fm.key ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'">
              <span class="flex items-center gap-2 min-w-0">
                <svg v-if="entries[menuDef.key].form === fm.key" class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                <span v-else class="w-3.5 flex-shrink-0"></span>
                <span class="truncate">{{ fm.hint }}</span>
              </span>
              <span class="font-semibold flex-shrink-0" dir="ltr">{{ fm.label }}</span>
            </button>
            <button v-if="CHELATE_METALS.includes(menuDef.key)" type="button" @click="goChelate(menuDef)"
              class="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-lg text-sm border-t border-gray-100 dark:border-gray-700 mt-1 pt-2.5 text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-900/20"
              :class="isChelateForm(entries[menuDef.key].form) ? 'bg-violet-50 dark:bg-violet-900/20' : ''">
              <span class="flex items-center gap-2"><span class="w-3.5 flex-shrink-0"></span>کلات (با هر درصد و هر نوع)</span>
              <span class="text-xs" dir="ltr">Chelate →</span>
            </button>
          </div>
        </template>
      </Teleport>

      <!-- ===== قیمت ===== -->
      <section :class="cardCls" class="lg:col-start-1">
        <div :class="stripCls(S.price)"></div>
        <header class="flex items-start gap-2.5">
          <span :class="badgeCls(S.price)"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="S.price.icon" /></svg></span>
          <div>
            <h4 :class="titleCls">قیمت</h4>
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
            <p class="text-[11px] leading-5 text-gray-600 dark:text-gray-400">این دو مقدار (به‌همراه درصد خلوص) برای محاسبهٔ دقیق قدرت خنثی‌سازی لازم است و از برگهٔ مشخصات ماده یا فرمول آن به‌دست می‌آید.</p>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label :class="labelCls">جرم مولی (g/mol)</label>
                <input type="number" v-model.number="formData.ph_mw" min="0" step="0.01" dir="ltr" :class="[inputCls, 'text-left']" />
              </div>
              <div>
                <label :class="labelCls">{{ kind === 'acid' ? 'تعداد H⁺ مؤثر در هر مولکول' : 'تعداد OH⁻ مؤثر در هر مولکول' }}</label>
                <input type="number" v-model.number="formData.ph_eq" min="0" step="0.1" dir="ltr" :class="[inputCls, 'text-left']" />
                <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1">{{ kind === 'acid' ? 'پروتونی که در pH کشت (۵ تا ۷) آزاد می‌شود؛ مثلاً اسید فسفریک حدود ۱ است.' : 'یون هیدروکسید (یا معادل آن) که هر مولکول در pH کشت تأمین می‌کند.' }}</p>
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
        <button type="button" @click="handleSave" :disabled="isSaving || !formData.name || totalElementsPercentage > 100" class="app-modal-btn app-modal-btn-primary">
          {{ isSaving ? 'در حال ذخیره...' : (isEditing ? 'ذخیره تغییرات' : 'افزودن کود') }}
        </button>
      </div>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import AppModal from '@/components/common/AppModal.vue';
import { computed, onBeforeUnmount, reactive, ref, watch } from 'vue';
import ChelatePanel from './ChelatePanel.vue';
import AdvancedBuilder from './AdvancedBuilder.vue';
import {
  ELEMENT_DEFS, toElementPct, labelKey, prettyFormula, chelateAgentLabel, chelateFormKey, isChelateForm,
  CHELATE_METALS, LEGACY_CHELATES, type ElementDef, type LabelForm
} from '@/utils/labelForms';

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
const panel = ref<'chelate' | 'advanced' | null>(null);
const togglePanel = (p: 'chelate' | 'advanced') => { panel.value = panel.value === p ? null : p; };
const chelateCount = computed(() => ELEMENT_DEFS.filter((d) => entries[d.key] && isChelateForm(entries[d.key].form)).length);
const onAdvancedApplied = (info: { formula: string | null }) => {
  if (info.formula && !props.formData.formula) props.formData.formula = info.formula;
  panel.value = null;
};

// ===== منوی فرم‌ها: موقعیت ثابت، چرخش به بالا اگر پایین جا نبود =====
const menuStyle = ref<Record<string, string> | null>(null);
const menuDef = computed(() => (openMenu.value ? ELEMENT_DEFS.find((d) => d.key === openMenu.value) || null : null));
const closeMenu = () => { openMenu.value = null; menuStyle.value = null; anchorEl = null; };
let anchorEl: HTMLElement | null = null;
const placeMenu = (d: ElementDef) => {
  if (!anchorEl || !anchorEl.isConnected) return closeMenu();
  const r = anchorEl.getBoundingClientRect();
  const margin = 10, gap = 6;
  const below = window.innerHeight - r.bottom - margin;
  const above = r.top - margin;
  const want = Math.min(d.forms.length * 40 + (CHELATE_METALS.includes(d.key) ? 52 : 0) + 16, 380);
  const up = below < Math.min(want, 220) && above > below;
  const maxH = Math.max(Math.min(want, up ? above : below), 140);
  const width = Math.min(Math.max(r.width, 260), window.innerWidth - 2 * margin);
  const left = Math.min(Math.max(r.right - width, margin), window.innerWidth - width - margin);
  menuStyle.value = { left: left + 'px', width: width + 'px', maxHeight: maxH + 'px', ...(up ? { bottom: window.innerHeight - r.top + gap + 'px' } : { top: r.bottom + gap + 'px' }) };
};
const toggleMenu = (d: ElementDef, ev: Event) => {
  if (openMenu.value === d.key) return closeMenu();
  anchorEl = ev.currentTarget as HTMLElement;
  openMenu.value = d.key;
  placeMenu(d);
};
const goChelate = (d: ElementDef) => {
  if (!isChelateForm(entries[d.key].form) && !(Number(entries[d.key].value) > 0)) entries[d.key] = { form: chelateFormKey('EDTA'), value: null };
  closeMenu();
  panel.value = 'chelate';
};
// با اسکرول یا تغییر اندازه (مثلاً جمع‌شدن نوار آدرس موبایل) منو بسته نمی‌شود؛ دوباره کنار دکمه می‌نشیند
let raf = 0;
const onViewportChange = () => {
  if (!openMenu.value || raf) return;
  raf = requestAnimationFrame(() => { raf = 0; if (menuDef.value) placeMenu(menuDef.value); });
};
window.addEventListener('resize', onViewportChange);
window.addEventListener('scroll', onViewportChange, true);
onBeforeUnmount(() => { window.removeEventListener('resize', onViewportChange); window.removeEventListener('scroll', onViewportChange, true); });
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
  closeMenu();
  panel.value = null;
  showMore.value = !!(props.formData.category || props.formData.description);
  resetEntries();
  const lv = props.formData.label_values || {};
  for (const d of ELEMENT_DEFS) {
    const hit = Object.keys(lv).find((k) => k.startsWith(d.key + '|'));
    if (hit) {
      const form = hit.split('|')[1];
      const legacy = LEGACY_CHELATES[form];
      if (legacy) {
        // کلات‌های قدیمی (مثل Fe-EDTA ۱۰٪) ← فرم جدید کلات با «درصد فلز» واقعی
        const metalPct = Number(props.formData.elements?.[d.key]) || Number(lv[hit]) * legacy.factor;
        entries[d.key] = { form: chelateFormKey(legacy.agent), value: Math.round(metalPct * 10000) / 10000 };
      } else {
        entries[d.key] = { form, value: Number(lv[hit]) };
      }
    } else if (Number(props.formData.elements?.[d.key]) > 0) {
      const v = Number(props.formData.elements[d.key]);
      entries[d.key] = { form: pureFormKey(d), value: Math.round(v * 10000) / 10000 };
    }
  }
});

const currentForm = (d: ElementDef): LabelForm => {
  const k = entries[d.key].form;
  if (isChelateForm(k)) return { key: k, label: `${d.symbol}-${chelateAgentLabel(k)}`, hint: 'کلات', factor: 1 };
  return d.forms.find((f) => f.key === k) || d.forms[0];
};
const pct = (d: ElementDef) => toElementPct(d.key, entries[d.key].form, Number(entries[d.key].value) || 0);
const selectForm = (d: ElementDef, key: string) => { entries[d.key].form = key; closeMenu(); };
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
  const purity = Number(props.formData.concentration);
  if (!(purity > 0 && purity <= 100)) props.formData.concentration = 100;
  if (kind.value !== 'none') props.formData.ph_purity = props.formData.concentration;
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
