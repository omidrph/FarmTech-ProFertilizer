<!-- frontend/src/components/features/fertilizer-db/ChelatePanel.vue -->
<!--
  بخش «کلات‌ها»: برای هر فلز (Fe، Mn، Zn، Cu، Mg، Ca) یک عامل کلات‌ساز و درصد فلز را وارد کنید.
  مقدار همان «درصد فلز» روی برچسب محصول است؛ بنابراین هر عددی (۶، ۷٫۵، ۱۰، ۱۳، …) مجاز است.
  داده در همان entries جدول عناصر ذخیره می‌شود (form = chelate-EDDHA، …).
-->
<template>
  <div class="rounded-2xl border border-violet-200 dark:border-violet-800/50 bg-gradient-to-b from-violet-50/80 to-white dark:from-violet-900/15 dark:to-gray-800/40 p-3.5 space-y-3.5 shadow-sm">
    <!-- سربرگ -->
    <header class="flex items-start gap-3">
      <span class="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-500 text-white flex items-center justify-center flex-shrink-0 shadow-sm shadow-violet-500/30">
        <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.7"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>
      </span>
      <div class="min-w-0">
        <h5 class="text-sm font-bold text-violet-900 dark:text-violet-200">کلات‌ها</h5>
        <p class="text-[12px] leading-5 text-gray-600 dark:text-gray-400">عامل کلات‌ساز را انتخاب و <b class="text-gray-800 dark:text-gray-200">درصد فلز</b> را همان‌طور که روی برچسب نوشته شده وارد کنید. هر درصدی مجاز است.</p>
      </div>
    </header>

    <!-- حالت خالی: افزودن سریع -->
    <div v-if="!rows.length" class="rounded-xl border border-dashed border-violet-300 dark:border-violet-700/60 bg-white/60 dark:bg-gray-800/40 p-3 text-center space-y-2.5">
      <p class="text-xs text-gray-500 dark:text-gray-400">هنوز کلاتی اضافه نشده. یک مورد رایج را انتخاب کنید یا از پایین فلز دلخواه را بزنید:</p>
      <div class="flex flex-wrap justify-center gap-1.5">
        <button v-for="q in QUICK" :key="q.metal + q.agent" type="button" :disabled="!isFree(q.metal)" @click="addRow(q.metal, q.agent)"
          class="px-3 py-1.5 rounded-full text-xs font-semibold border border-violet-200 dark:border-violet-700 bg-white dark:bg-gray-800 text-violet-700 dark:text-violet-300 hover:bg-violet-600 hover:text-white hover:border-violet-600 transition-colors disabled:opacity-40 disabled:pointer-events-none" dir="ltr">
          {{ q.metal }}-{{ q.agent }}
        </button>
      </div>
    </div>

    <!-- ردیف‌های کلات -->
    <TransitionGroup name="cl" tag="div" class="space-y-2.5">
      <article v-for="r in rows" :key="r.metal" class="rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-3 space-y-2.5 shadow-sm">
        <div class="flex items-center gap-3">
          <span class="w-11 h-11 rounded-2xl flex items-center justify-center text-sm font-extrabold flex-shrink-0 shadow-inner" :class="METAL_CLS[r.metal] || 'bg-gray-100 text-gray-700'" dir="ltr">{{ r.metal }}</span>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-bold text-gray-900 dark:text-white truncate">{{ metalName(r.metal) }}</p>
            <p class="text-[11px] text-gray-500 dark:text-gray-400">کلات با <b dir="ltr" class="text-violet-700 dark:text-violet-300">{{ agentOf(r.agent)?.label }}</b></p>
          </div>
          <label class="flex items-center h-11 rounded-xl border-2 bg-white dark:bg-gray-700 overflow-hidden focus-within:border-violet-500 transition-colors"
            :class="Number(entries[r.metal].value) > 0 ? 'border-violet-300 dark:border-violet-600' : 'border-gray-200 dark:border-gray-600'">
            <input type="number" v-model.number="entries[r.metal].value" min="0" max="100" step="0.01" dir="ltr" placeholder="۰" :aria-label="`درصد ${r.metal}`"
              class="w-20 h-full px-2 text-center text-lg font-extrabold bg-transparent text-gray-900 dark:text-white outline-none tabular-nums" />
            <span class="h-full px-2.5 flex items-center text-xs font-semibold bg-gray-50 dark:bg-gray-600/60 text-gray-500 dark:text-gray-300 border-r border-gray-200 dark:border-gray-600">٪</span>
          </label>
          <button type="button" @click="remove(r.metal)" class="p-2 rounded-xl text-gray-400 hover:text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors" title="حذف این کلات" aria-label="حذف">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>

        <!-- انتخاب عامل کلات‌ساز -->
        <div>
          <p class="text-[11px] font-medium text-gray-500 dark:text-gray-400 mb-1.5">عامل کلات‌ساز</p>
          <div class="flex flex-wrap gap-1.5">
            <button v-for="a in CHELATE_AGENTS" :key="a.key" type="button" @click="setAgent(r.metal, a.key)"
              class="px-2.5 py-1 rounded-full text-[12px] border transition-all"
              :class="r.agent === a.key
                ? 'bg-violet-600 border-violet-600 text-white font-semibold shadow-sm'
                : 'bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-violet-300 hover:text-violet-700'"
              :dir="/^[A-Za-z]/.test(a.label) ? 'ltr' : 'rtl'">{{ a.label }}</button>
          </div>
        </div>

        <!-- نکته‌ها -->
        <div v-if="hasTips(r)" class="flex flex-wrap items-center gap-2">
          <button v-if="preset(r.metal, r.agent) && Number(entries[r.metal].value) !== preset(r.metal, r.agent)" type="button" @click="entries[r.metal].value = preset(r.metal, r.agent) ?? null"
            class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium bg-violet-50 dark:bg-violet-900/20 text-violet-700 dark:text-violet-300 border border-violet-200 dark:border-violet-800/60 hover:bg-violet-100 transition-colors">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" /></svg>
            مقدار رایج: {{ preset(r.metal, r.agent)?.toLocaleString('fa-IR') }}٪ (قابل تغییر)
          </button>
          <span v-if="r.metal === 'Fe' && agentOf(r.agent)?.stability" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300 border border-sky-100 dark:border-sky-800/50">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" /></svg>
            {{ agentOf(r.agent)?.stability }} (تقریبی)
          </span>
        </div>
      </article>
    </TransitionGroup>

    <!-- افزودن فلز -->
    <div class="flex flex-wrap items-center gap-1.5 pt-0.5">
      <span class="text-[11px] font-medium text-gray-500 dark:text-gray-400 ml-1">افزودن کلات برای:</span>
      <button v-for="m in CHELATE_METALS" :key="m" type="button" :disabled="!isFree(m)" @click="addRow(m, m === 'Fe' ? 'EDDHA' : 'EDTA')"
        class="inline-flex items-center gap-1.5 pl-2.5 pr-1.5 py-1 rounded-full text-xs border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:border-violet-400 hover:text-violet-700 transition-colors disabled:opacity-40 disabled:pointer-events-none"
        :title="!isFree(m) ? 'این فلز قبلاً در جدول پر شده یا کلات دارد' : ''">
        <span class="w-5 h-5 rounded-full text-[10px] font-bold flex items-center justify-center" :class="METAL_CLS[m]" dir="ltr">{{ m }}</span>{{ metalName(m) }}
      </button>
    </div>
    <p class="text-[11px] leading-5 text-gray-500 dark:text-gray-400 flex items-start gap-1.5">
      <svg class="w-3.5 h-3.5 mt-0.5 flex-shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" /></svg>
      هر فلز فقط یک شکل دارد: یا نمک/اکسید در جدول، یا کلات. اگر محصول چند فلز کلاته دارد، برای هر فلز یک کلات اضافه کنید.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  CHELATE_AGENTS, CHELATE_METALS, CHELATE_PRESETS, chelateAgentOf, chelateFormKey, getElementDef, isChelateForm, ELEMENT_DEFS
} from '@/utils/labelForms';

const props = defineProps<{ entries: Record<string, { form: string; value: number | null }> }>();

const QUICK = [
  { metal: 'Fe', agent: 'EDDHA' }, { metal: 'Fe', agent: 'EDTA' }, { metal: 'Fe', agent: 'DTPA' },
  { metal: 'Mn', agent: 'EDTA' }, { metal: 'Zn', agent: 'EDTA' }, { metal: 'Cu', agent: 'EDTA' }
];
const METAL_CLS: Record<string, string> = {
  Fe: 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300',
  Mn: 'bg-fuchsia-100 text-fuchsia-700 dark:bg-fuchsia-900/40 dark:text-fuchsia-300',
  Zn: 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300',
  Cu: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  Mg: 'bg-lime-100 text-lime-700 dark:bg-lime-900/40 dark:text-lime-300',
  Ca: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300'
};

const metalName = (m: string) => getElementDef(m)?.name || m;
const agentOf = (key: string) => CHELATE_AGENTS.find((a) => a.key === key);
const preset = (metal: string, agent: string): number | undefined => CHELATE_PRESETS[metal]?.[agent];

const rows = computed(() =>
  ELEMENT_DEFS.map((d) => d.key)
    .filter((k) => props.entries[k] && isChelateForm(props.entries[k].form))
    .map((k) => ({ metal: k, agent: chelateAgentOf(props.entries[k].form) }))
);
const hasTips = (r: { metal: string; agent: string }) =>
  (!!preset(r.metal, r.agent) && Number(props.entries[r.metal].value) !== preset(r.metal, r.agent)) || (r.metal === 'Fe' && !!agentOf(r.agent)?.stability);

// فلز «آزاد» = هنوز در جدول مقدار غیرکلات ندارد و کلات هم نیست
const isFree = (m: string) => {
  const e = props.entries[m];
  if (!e) return true;
  if (isChelateForm(e.form)) return false;
  return !(Number(e.value) > 0);
};

const setAgent = (metal: string, agent: string) => { props.entries[metal].form = chelateFormKey(agent); };
const addRow = (metal: string, agent: string) => {
  if (!isFree(metal)) return;
  props.entries[metal] = { form: chelateFormKey(agent), value: null };
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
.cl-enter-active, .cl-leave-active { transition: all .22s ease; }
.cl-enter-from { opacity: 0; transform: translateY(-8px) scale(.98); }
.cl-leave-to { opacity: 0; transform: translateX(16px); }
</style>
