<template>
  <div class="space-y-3">
    <!-- خلاصه -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="c in summary" :key="c.l" class="ad-card ad-hover p-4 flex items-center gap-3">
        <span class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :style="{ background: c.color + '1a', color: c.color }">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" :d="c.icon" /></svg>
        </span>
        <div class="min-w-0"><p class="text-lg font-extrabold tabular-nums text-gray-900 dark:text-white">{{ c.v }}</p><p class="text-[11px] text-gray-500 dark:text-gray-400">{{ c.l }}</p></div>
      </div>
    </div>

    <!-- فیلترها -->
    <div class="ad-card p-3 space-y-2.5">
      <div class="flex flex-wrap items-end gap-2.5">
        <div class="flex-1 min-w-[12rem]"><label class="ad-label">جستجو (نام، برند، فرمول)</label><input v-model="q" class="ad-input" /></div>
        <div class="w-40"><label class="ad-label">مرتب‌سازی</label>
          <select v-model="sort" class="ad-input"><option value="name">نام</option><option value="price_desc">گران‌ترین</option><option value="price_asc">ارزان‌ترین</option><option value="updated">آخرین ویرایش</option></select></div>
        <button class="ad-btn" @click="exportCsv">خروجی CSV</button>
        <button class="ad-btn" @click="bulkOpen = true">تغییر گروهی قیمت</button>
        <button class="ad-btn-primary" @click="openNew">+ کود سیستمی جدید</button>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <button v-for="c in chips" :key="c.k" class="px-3 py-1 rounded-full text-xs border transition"
          :class="chip === c.k ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:border-primary-400'" @click="chip = c.k">{{ c.l }}</button>
      </div>
    </div>
    <p class="text-xs text-gray-500 dark:text-gray-400 px-1">این فهرست همان «کودهای شرکتی» است که کاربران در پایگاه کود می‌بینند. تغییر قیمت یا عناصر روی کپی‌هایی که کاربران قبلاً برداشته‌اند اثری ندارد.</p>

    <div class="ad-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[52rem]">
          <thead><tr><th class="ad-th">نام</th><th class="ad-th">فرمول</th><th class="ad-th">شکل</th><th class="ad-th">عناصر</th><th class="ad-th">قیمت / کیلو (تومان)</th><th class="ad-th"></th></tr></thead>
          <tbody>
            <tr v-if="loading"><td colspan="6" class="ad-td text-center text-gray-400 py-10">در حال بارگذاری…</td></tr>
            <tr v-else-if="!view.length"><td colspan="6" class="ad-td text-center text-gray-400 py-10">کودی با این فیلتر پیدا نشد.</td></tr>
            <tr v-for="f in view" :key="f.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <td class="ad-td"><p class="font-semibold text-gray-900 dark:text-white">{{ f.name }}
                  <span v-if="f.is_acid" class="ad-chip bg-amber-100 text-amber-700 mr-1">اسید</span><span v-if="f.is_base" class="ad-chip bg-sky-100 text-sky-700 mr-1">باز</span></p>
                <p v-if="f.brand" class="text-[11px] text-gray-400">{{ f.brand }}</p></td>
              <td class="ad-td text-xs" dir="ltr">{{ f.formula || '—' }}</td>
              <td class="ad-td"><span v-if="f.form" class="ad-chip bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300">{{ FORMS[f.form] || f.form }}</span><span v-else class="text-gray-300">—</span></td>
              <td class="ad-td"><div class="flex flex-wrap gap-1 max-w-[18rem]" dir="ltr">
                  <span v-for="[el, v] in topElements(f.elements)" :key="el" class="inline-flex items-center rounded-md border border-gray-200 dark:border-gray-600 text-[11px] overflow-hidden"><b class="px-1.5 py-0.5 bg-gray-50 dark:bg-gray-700">{{ el }}</b><span class="px-1.5 tabular-nums">{{ v }}</span></span>
                  <span v-if="moreCount(f.elements)" class="text-[11px] text-gray-400 self-center">+{{ moreCount(f.elements) }}</span></div></td>
              <td class="ad-td tabular-nums font-semibold">{{ f.price_per_kg ? faN(Math.round(f.price_per_kg)) : '—' }}</td>
              <td class="ad-td whitespace-nowrap"><button class="ad-btn ad-btn-sm" @click="openEdit(f)">ویرایش</button> <button class="ad-btn ad-btn-sm !text-rose-700" @click="remove(f)">حذف</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-3 py-2 text-xs text-gray-400">{{ faN(view.length) }} از {{ faN(items.length) }} کود</div>
    </div>

    <!-- تغییر گروهی قیمت -->
    <AppModal :open="bulkOpen" title="تغییر گروهی قیمت" subtitle="روی کودهای سیستمی اعمال می‌شود" size="sm" @close="bulkOpen = false">
      <div class="space-y-3">
        <div><label class="ad-label">درصد تغییر (مثبت = افزایش، منفی = کاهش)</label>
          <div class="flex items-center gap-2"><input v-model.number="bulk.percent" type="number" step="1" min="-90" max="500" class="ad-input" dir="ltr" /><span class="text-sm text-gray-500">٪</span></div>
          <div class="flex gap-1.5 mt-2"><button v-for="v in [-10, 5, 10, 20, 30]" :key="v" class="ad-btn ad-btn-sm" @click="bulk.percent = v">{{ v > 0 ? '+' : '' }}{{ faN(v) }}٪</button></div></div>
        <div><label class="ad-label">شامل کدام کودها؟</label>
          <select v-model="bulk.form" class="ad-input"><option value="">همهٔ کودهای سیستمی</option><option v-for="(l, k) in FORMS" :key="k" :value="k">فقط {{ l }}</option></select></div>
        <p class="text-xs rounded-lg bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-200 p-2.5 leading-6">قیمت هر کود با درصد بالا ضرب و به تومان گرد می‌شود. کودهای بدون قیمت دست نمی‌خورند. این کار در لاگ مدیران ثبت می‌شود.</p>
      </div>
      <template #footer><div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="bulkOpen = false">انصراف</button><button class="ad-btn-primary" :disabled="!bulk.percent" @click="applyBulk">اعمال تغییر</button></div></template>
    </AppModal>

    <AppModal :open="!!edit" :title="edit?.id ? 'ویرایش کود سیستمی' : 'کود سیستمی جدید'" size="lg" @close="edit = null">
      <div v-if="edit" class="space-y-3">
        <div class="grid sm:grid-cols-2 gap-2.5">
          <div><label class="ad-label">نام *</label><input v-model="edit.name" class="ad-input" /></div>
          <div><label class="ad-label">فرمول</label><input v-model="edit.formula" class="ad-input" dir="ltr" /></div>
          <div><label class="ad-label">برند</label><input v-model="edit.brand" class="ad-input" /></div>
          <div><label class="ad-label">دسته‌بندی</label><input v-model="edit.category" class="ad-input" /></div>
          <div><label class="ad-label">شکل</label>
            <select v-model="edit.form" class="ad-input"><option :value="null">—</option><option v-for="(l, k) in FORMS" :key="k" :value="k">{{ l }}</option></select></div>
          <div><label class="ad-label">خلوص / غلظت (٪)</label><input v-model.number="edit.concentration" type="number" min="0" max="100" class="ad-input" dir="ltr" /></div>
          <div><label class="ad-label">قیمت هر کیلوگرم (تومان)</label><input v-model.number="edit.price_per_kg" type="number" min="0" class="ad-input" dir="ltr" /></div>
          <div><label class="ad-label">چگالی (g/mL) برای مایع‌ها</label><input v-model.number="edit.density_g_ml" type="number" step="0.01" min="0" class="ad-input" dir="ltr" /></div>
        </div>
        <div class="flex flex-wrap gap-4 text-sm">
          <label class="flex items-center gap-2"><input type="checkbox" v-model="edit.is_acid" /> اسید</label>
          <label class="flex items-center gap-2"><input type="checkbox" v-model="edit.is_base" /> باز تنظیم pH</label>
          <div v-if="edit.is_acid || edit.is_base" class="flex items-center gap-2"><span class="text-xs text-gray-500">نوع:</span><input v-model="edit.acid_type" class="ad-input !w-28" dir="ltr" placeholder="H3PO4" /></div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-1"><label class="ad-label !mb-0">درصد عناصر (٪ وزنی خالص)</label><button class="ad-btn ad-btn-sm" @click="elRows.push({ k: '', v: 0 })">+ عنصر</button></div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <div v-for="(r, i) in elRows" :key="i" class="flex gap-1.5">
              <input v-model="r.k" class="ad-input !w-20" dir="ltr" placeholder="Ca" />
              <input v-model.number="r.v" type="number" step="0.01" min="0" max="100" class="ad-input" dir="ltr" />
              <button class="text-gray-400 hover:text-rose-600 px-1" @click="elRows.splice(i, 1)">×</button>
            </div>
          </div>
          <p class="mt-1 text-[11px] text-gray-400">نمادها: N-NO3، N-NH4، P، K، Ca، Mg، S، Na، Cl، Fe، Mn، Zn، B، Cu، Mo، Si</p>
        </div>
        <div><label class="ad-label">توضیحات</label><textarea v-model="edit.description" rows="2" class="ad-input"></textarea></div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="edit = null">انصراف</button><button class="ad-btn-primary" :disabled="saving || !edit?.name" @click="save">ذخیره</button></div>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import { adminApi, apiError, faN } from '@/services/adminApi';
import { confirmDialog, toast } from './adminUi';

const FORMS: Record<string, string> = { powder: 'پودر', crystal: 'کریستال', granular: 'گرانول', liquid: 'مایع' };
const items = ref<any[]>([]);
const loading = ref(false), saving = ref(false);
const q = ref('');
const edit = ref<any | null>(null);
const sort = ref('name');
const chip = ref('all');
const bulkOpen = ref(false);
const bulk = reactive<{ percent: number; form: string }>({ percent: 10, form: '' });
const chips = [{ k: 'all', l: 'همه' }, { k: 'acid', l: 'اسیدها' }, { k: 'base', l: 'بازها' }, { k: 'liquid', l: 'مایع' }, { k: 'powder', l: 'پودر' }, { k: 'crystal', l: 'کریستال' }, { k: 'granular', l: 'گرانول' }, { k: 'noprice', l: 'بدون قیمت' }];

const view = computed(() => {
  let r = items.value.filter((f) => chip.value === 'all' ? true : chip.value === 'acid' ? f.is_acid : chip.value === 'base' ? f.is_base
    : chip.value === 'noprice' ? !f.price_per_kg : f.form === chip.value);
  const by: Record<string, (a: any, b: any) => number> = {
    name: (a, b) => String(a.name).localeCompare(String(b.name), 'fa'), price_desc: (a, b) => (b.price_per_kg || 0) - (a.price_per_kg || 0),
    price_asc: (a, b) => (a.price_per_kg || 0) - (b.price_per_kg || 0), updated: (a, b) => String(b.updated_at || '').localeCompare(String(a.updated_at || ''))
  };
  return [...r].sort(by[sort.value]);
});
const summary = computed(() => {
  const priced = items.value.filter((f) => f.price_per_kg > 0);
  const avg = priced.length ? Math.round(priced.reduce((a, f) => a + f.price_per_kg, 0) / priced.length) : 0;
  return [
    { l: 'کل کودهای سیستمی', v: faN(items.value.length), color: '#2563eb', icon: 'M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5m4.75-11.396c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3' },
    { l: 'میانگین قیمت / کیلو', v: avg ? faN(avg) : '—', color: '#10b981', icon: 'M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
    { l: 'اسید و باز', v: faN(items.value.filter((f) => f.is_acid || f.is_base).length), color: '#f59e0b', icon: 'M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z' },
    { l: 'بدون قیمت', v: faN(items.value.filter((f) => !f.price_per_kg).length), color: '#f43f5e', icon: 'M6 18L18 6M6 6l12 12' }
  ];
});
const topElements = (e: Record<string, number>) => Object.entries(e || {}).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([k, v]) => [k, +Number(v).toFixed(2)] as [string, number]);
const moreCount = (e: Record<string, number>) => Math.max(Object.values(e || {}).filter((v) => v > 0).length - 4, 0);

async function applyBulk() {
  const label = bulk.form ? `کودهای ${FORMS[bulk.form]}` : 'همهٔ کودهای سیستمی';
  if (!(await confirmDialog({ title: `تغییر ${bulk.percent > 0 ? '+' : ''}${faN(bulk.percent)}٪ قیمت`, message: `قیمت ${label} تغییر می‌کند. ادامه می‌دهید؟`, confirmText: 'اعمال کن', danger: Math.abs(bulk.percent) >= 30 }))) return;
  try { const r = await adminApi.bulkPrice({ percent: bulk.percent, form: bulk.form || null }); toast(`قیمت ${faN(r.updated)} کود تغییر کرد`); bulkOpen.value = false; load(); }
  catch (e) { toast(apiError(e), 'error'); }
}
function exportCsv() {
  const esc = (v: any) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const lines = [['نام', 'فرمول', 'برند', 'شکل', 'قیمت/کیلو', 'عناصر'].map(esc).join(',')];
  for (const f of view.value) lines.push([f.name, f.formula, f.brand, FORMS[f.form] || '', f.price_per_kg, Object.entries(f.elements || {}).filter(([, v]) => (v as number) > 0).map(([k, v]) => `${k}:${v}`).join(' ')].map(esc).join(','));
  const blob = new Blob(['\ufeff' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `fertilizers-${new Date().toISOString().slice(0, 10)}.csv`; a.click(); URL.revokeObjectURL(a.href);
}
const elRows = ref<{ k: string; v: number }[]>([]);


async function load() {
  loading.value = true;
  try { items.value = (await adminApi.fertilizers(q.value.trim())).items; }
  catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
let t: number | undefined;
watch(q, () => { clearTimeout(t); t = window.setTimeout(load, 350); });
onMounted(load);

const blank = () => ({ name: '', formula: '', brand: '', category: '', form: null, concentration: 100, price_per_kg: 0, density_g_ml: null, is_acid: false, is_base: false, acid_type: '', description: '' });
function openNew() { edit.value = blank(); elRows.value = [{ k: '', v: 0 }]; }
function openEdit(f: any) { edit.value = { ...blank(), ...f }; elRows.value = Object.entries(f.elements || {}).map(([k, v]) => ({ k, v: Number(v) })); }

async function save() {
  if (!edit.value) return;
  const elements: Record<string, number> = {};
  for (const r of elRows.value) if (r.k.trim() && Number(r.v) > 0) elements[r.k.trim()] = Number(r.v);
  const clean = (v: any) => (v === '' ? null : v);
  const body: any = {
    name: edit.value.name, formula: clean(edit.value.formula), brand: clean(edit.value.brand), category: clean(edit.value.category),
    form: edit.value.form || null, concentration: Number(edit.value.concentration ?? 100), price_per_kg: Number(edit.value.price_per_kg || 0),
    density_g_ml: edit.value.density_g_ml ? Number(edit.value.density_g_ml) : null, is_acid: !!edit.value.is_acid, is_base: !!edit.value.is_base,
    acid_type: clean(edit.value.acid_type), description: clean(edit.value.description), elements
  };
  saving.value = true;
  try {
    if (edit.value.id) await adminApi.updateFertilizer(edit.value.id, body); else await adminApi.createFertilizer(body);
    toast('کود ذخیره شد'); edit.value = null; load();
  } catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
async function remove(f: any) {
  if (!(await confirmDialog({ title: `حذف «${f.name}»`, message: 'از فهرست کودهای شرکتی حذف می‌شود. کپی‌های کاربران باقی می‌مانند.', confirmText: 'حذف کن', danger: true }))) return;
  try { await adminApi.deleteFertilizer(f.id); toast('کود حذف شد'); load(); } catch (e) { toast(apiError(e), 'error'); }
}
</script>
