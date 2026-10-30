<!-- frontend/src/components/features/fertilizer-db/ChelatePanel.vue -->
<!--
  بخش «کلات‌ها»: هر فلز می‌تواند کلات باشد (Fe، Mn، Zn، Cu، Mg، Ca) با هر عامل کلات‌ساز
  و هر درصدی (۶٪، ۷٫۵٪، ۱۰٪، ۱۳٪، ...). مقدار همان «درصد فلز» روی برچسب محصول است.
  داده در همان entries جدول عناصر ذخیره می‌شود (form = chelate-EDDHA، ...).
-->
<template>
  <div class="rounded-xl border border-violet-200 dark:border-violet-800/50 bg-violet-50/50 dark:bg-violet-900/10 p-3 space-y-3">
    <div>
      <p class="text-sm font-semibold text-violet-800 dark:text-violet-300">کلات‌ها</p>
      <p class="text-[11px] leading-5 text-gray-600 dark:text-gray-400 mt-0.5">
        درصد <b>فلز</b> را همان‌طور که روی برچسب محصول نوشته شده وارد کنید (مثلاً «Fe ۶٪»). هر درصدی مجاز است؛ مقدارهای پیشنهادی فقط میان‌بر هستند و ممکن است با محصول شما فرق داشته باشند.
      </p>
    </div>

    <p v-if="!rows.length" class="text-xs text-gray-500 dark:text-gray-400 py-1">هنوز کلاتی اضافه نشده است.</p>

    <div v-for="r in rows" :key="r.metal" class="rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-2.5 space-y-2">
      <div class="flex items-center gap-2">
        <span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300 text-xs font-bold flex items-center justify-center flex-shrink-0" dir="ltr">{{ r.metal }}</span>
        <div class="flex-1 min-w-0">
          <select :value="r.agent" @change="setAgent(r.metal, ($event.target as HTMLSelectElement).value)" class="w-full h-9 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
            <option v-for="a in CHELATE_AGENTS" :key="a.key" :value="a.key">{{ metalName(r.metal) }} — {{ a.label }}</option>
          </select>
        </div>
        <div class="flex items-center gap-1 flex-shrink-0">
          <input type="number" v-model.number="entries[r.metal].value" min="0" max="100" step="0.01" dir="ltr" placeholder="۰"
            class="w-20 h-9 px-2 text-sm text-center rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 font-semibold" />
          <span class="text-xs text-gray-500">٪ {{ r.metal }}</span>
        </div>
        <button type="button" @click="remove(r.metal)" class="p-1.5 rounded-lg text-gray-400 hover:text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20" title="حذف این کلات">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
      <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-gray-500 dark:text-gray-400">
        <button v-if="preset(r.metal, r.agent) && Number(entries[r.metal].value) !== preset(r.metal, r.agent)" type="button" @click="entries[r.metal].value = preset(r.metal, r.agent) ?? null"
          class="px-2 py-0.5 rounded-full border border-violet-300 dark:border-violet-700 text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-900/30">
          مقدار رایج: {{ preset(r.metal, r.agent)?.toLocaleString('fa-IR') }}٪
        </button>
        <span v-if="agentOf(r.agent)?.stability && r.metal === 'Fe'">ثبات آهن: {{ agentOf(r.agent)?.stability }} (تقریبی)</span>
      </div>
    </div>

    <!-- افزودن -->
    <div class="flex flex-wrap items-center gap-2 pt-1">
      <select v-model="newMetal" class="h-9 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
        <option value="">فلز…</option>
        <option v-for="m in CHELATE_METALS" :key="m" :value="m" :disabled="!isFree(m)">{{ metalName(m) }} ({{ m }}){{ !isFree(m) ? ' — قبلاً پر شده' : '' }}</option>
      </select>
      <select v-model="newAgent" class="h-9 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
        <option v-for="a in CHELATE_AGENTS" :key="a.key" :value="a.key">{{ a.label }}</option>
      </select>
      <button type="button" :disabled="!newMetal" @click="add" class="h-9 px-3 rounded-lg text-sm font-medium bg-violet-600 text-white hover:bg-violet-700 disabled:opacity-40">+ افزودن کلات</button>
    </div>
    <p class="text-[11px] text-gray-500 dark:text-gray-400 leading-5">برای هر فلز فقط یک شکل ثبت می‌شود (یا نمک/اکسید در جدول، یا کلات). اگر محصول شما چند فلز کلاته دارد، برای هر فلز یک ردیف اضافه کنید.</p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import {
  CHELATE_AGENTS, CHELATE_METALS, CHELATE_PRESETS, chelateAgentOf, chelateFormKey, getElementDef, isChelateForm, ELEMENT_DEFS
} from '@/utils/labelForms';

const props = defineProps<{ entries: Record<string, { form: string; value: number | null }> }>();

const newMetal = ref('');
const newAgent = ref('EDTA');

const metalName = (m: string) => getElementDef(m)?.name || m;
const agentOf = (key: string) => CHELATE_AGENTS.find((a) => a.key === key);
const preset = (metal: string, agent: string): number | undefined => CHELATE_PRESETS[metal]?.[agent];

const rows = computed(() =>
  ELEMENT_DEFS.map((d) => d.key)
    .filter((k) => props.entries[k] && isChelateForm(props.entries[k].form))
    .map((k) => ({ metal: k, agent: chelateAgentOf(props.entries[k].form) }))
);
// فلز «آزاد» = هنوز در جدول مقدار غیرکلات ندارد
const isFree = (m: string) => {
  const e = props.entries[m];
  if (!e) return true;
  if (isChelateForm(e.form)) return false;   // همین‌حالا یک ردیف کلات دارد
  return !(Number(e.value) > 0);
};

const setAgent = (metal: string, agent: string) => { props.entries[metal].form = chelateFormKey(agent); };
const add = () => {
  const m = newMetal.value;
  if (!m || !isFree(m)) return;
  props.entries[m] = { form: chelateFormKey(newAgent.value), value: null };
  newMetal.value = '';
};
const remove = (metal: string) => {
  const def = getElementDef(metal);
  props.entries[metal] = { form: def?.defaultForm || metal, value: null };
};
</script>

<style scoped>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; appearance: textfield; }
input:focus, select:focus { outline: none; }
</style>
