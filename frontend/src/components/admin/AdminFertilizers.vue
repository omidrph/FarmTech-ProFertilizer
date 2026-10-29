<template>
  <div class="space-y-3">
    <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
      <div class="flex-1 min-w-[12rem]"><label class="ad-label">جستجو (نام، برند، فرمول)</label><input v-model="q" class="ad-input" /></div>
      <button class="ad-btn-primary" @click="openNew">+ کود سیستمی جدید</button>
    </div>
    <p class="text-xs text-gray-500 dark:text-gray-400 px-1">این فهرست همان «کودهای شرکتی» است که کاربران در پایگاه کود می‌بینند. تغییر قیمت یا عناصر روی کپی‌هایی که کاربران قبلاً برداشته‌اند اثری ندارد.</p>

    <div class="ad-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[48rem]">
          <thead><tr><th class="ad-th">نام</th><th class="ad-th">فرمول</th><th class="ad-th">برند</th><th class="ad-th">شکل</th><th class="ad-th">عناصر</th><th class="ad-th">قیمت / کیلو</th><th class="ad-th"></th></tr></thead>
          <tbody>
            <tr v-if="loading"><td colspan="7" class="ad-td text-center text-gray-400 py-8">در حال بارگذاری…</td></tr>
            <tr v-else-if="!items.length"><td colspan="7" class="ad-td text-center text-gray-400 py-8">کودی ثبت نشده است.</td></tr>
            <tr v-for="f in items" :key="f.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30">
              <td class="ad-td font-medium">{{ f.name }} <span v-if="f.is_acid" class="ad-chip bg-amber-100 text-amber-700">اسید</span><span v-if="f.is_base" class="ad-chip bg-sky-100 text-sky-700">باز</span></td>
              <td class="ad-td text-xs" dir="ltr">{{ f.formula || '—' }}</td>
              <td class="ad-td text-xs">{{ f.brand || '—' }}</td>
              <td class="ad-td text-xs">{{ FORMS[f.form] || '—' }}</td>
              <td class="ad-td text-xs" dir="ltr">{{ elementsText(f.elements) }}</td>
              <td class="ad-td tabular-nums">{{ faN(Math.round(f.price_per_kg || 0)) }}</td>
              <td class="ad-td whitespace-nowrap"><button class="ad-btn ad-btn-sm" @click="openEdit(f)">ویرایش</button> <button class="ad-btn ad-btn-sm !text-rose-700" @click="remove(f)">حذف</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-3 py-2 text-xs text-gray-400">{{ faN(items.length) }} کود</div>
    </div>

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
import { onMounted, ref, watch } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import { adminApi, apiError, faN } from '@/services/adminApi';
import { confirmDialog, toast } from './adminUi';

const FORMS: Record<string, string> = { powder: 'پودر', crystal: 'کریستال', granular: 'گرانول', liquid: 'مایع' };
const items = ref<any[]>([]);
const loading = ref(false), saving = ref(false);
const q = ref('');
const edit = ref<any | null>(null);
const elRows = ref<{ k: string; v: number }[]>([]);

const elementsText = (e: Record<string, number>) => Object.entries(e || {}).filter(([, v]) => v > 0).map(([k, v]) => `${k} ${v}`).join(' · ') || '—';

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
