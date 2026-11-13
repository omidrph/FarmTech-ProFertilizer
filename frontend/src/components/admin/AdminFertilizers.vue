<!-- frontend/src/components/admin/AdminFertilizers.vue -->
<!-- مدیریت کودهای سیستمی: همان جدول و همان مودال افزودن/ویرایش صفحهٔ کاربر + امکانات مدیر (فروشگاه، قیمت گروهی، موجودی) -->
<template>
  <div class="space-y-4">
    <!-- خلاصه -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="c in summary" :key="c.l" class="ad-card ad-hover p-4 flex items-center gap-3">
        <span class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-lg" :style="{ background: c.color + '1a', color: c.color }">{{ c.icon }}</span>
        <div class="min-w-0">
          <p class="text-lg font-extrabold tabular-nums text-gray-900 dark:text-white">{{ c.v }}</p>
          <p class="text-[11px] text-gray-500 dark:text-gray-400">{{ c.l }}</p>
        </div>
      </div>
    </div>

    <p class="text-xs text-gray-500 dark:text-gray-400 px-1 leading-6">
      این فهرست همان «کودهای شرکتی» است که کاربران در پایگاه داده کودها می‌بینند. افزودن و ویرایش با همان مودال کاربران انجام می‌شود؛
      دکمهٔ <b>🛒</b> کنار هر کود، قیمت فروش و موجودی آن را در فروشگاه تعیین می‌کند.
    </p>

    <div class="ad-card p-3 sm:p-4">
      <FertilizerStatsAndTable
        :user-fertilizers="rows"
        :system-fertilizers="[]"
        :is-loading="loading"
        :active-filter="activeFilter"
        admin-mode
        @refresh="load"
        @open-modal="openAdd"
        @edit-fertilizer="openEdit"
        @delete-fertilizer="remove"
        @filter-change="(f: string | null) => (activeFilter = f)"
      >
        <template #toolbar-extra>
          <button type="button" class="h-9 px-3 rounded-lg border border-gray-200 dark:border-gray-600 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex-shrink-0" @click="bulkOpen = true">تغییر گروهی قیمت</button>
        </template>
        <template #row-extra="{ fertilizer }">
          <button type="button" class="p-1.5 rounded-lg hover:bg-violet-50 dark:hover:bg-violet-900/30 text-sm relative" :title="shopTitle(fertilizer)" @click="openShop(fertilizer)">
            🛒<span v-if="shopOf(fertilizer)?.shop_enabled === false" class="absolute -top-0.5 -left-0.5 w-2 h-2 rounded-full bg-rose-500"></span>
          </button>
        </template>
      </FertilizerStatsAndTable>
    </div>

    <!-- همان مودال کاربران -->
    <FertilizerModal :is-open="showModal" :is-editing="isEditing" :form-data="formData" :is-saving="saving" @close="closeModal" @save="save" />

    <!-- تنظیمات فروش یک کود -->
    <AppModal :open="!!shopForm" title="تنظیمات فروش کود" size="sm" @close="shopForm = null">
      <div v-if="shopForm" class="space-y-3 p-1">
        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ shopForm.name }}</p>
        <label class="flex items-center justify-between gap-3 text-sm"><span>نمایش در فروشگاه</span><input v-model="shopForm.enabled" type="checkbox" class="w-5 h-5 accent-violet-600" /></label>
        <div><label class="ad-label">قیمت فروش (به {{ shopForm.unit }}؛ خالی = همان قیمت پایگاه داده: {{ faN(shopForm.base) }})</label><input v-model.number="shopForm.price" type="number" min="0" class="ad-input" placeholder="خودکار" /></div>
        <div><label class="ad-label">موجودی (خالی = نامحدود)</label><input v-model.number="shopForm.stock" type="number" min="0" class="ad-input" placeholder="نامحدود" /></div>
        <div><label class="ad-label">حداقل مقدار سفارش</label><input v-model.number="shopForm.min" type="number" min="0" class="ad-input" placeholder="بدون حداقل" /></div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="shopForm = null">انصراف</button><button class="ad-btn-primary" :disabled="saving" @click="saveShop">ذخیره</button></div>
      </template>
    </AppModal>

    <!-- تغییر گروهی قیمت -->
    <AppModal :open="bulkOpen" title="تغییر گروهی قیمت کودهای سیستمی" size="sm" @close="bulkOpen = false">
      <div class="space-y-3 p-1">
        <div><label class="ad-label">درصد تغییر (مثلاً ۱۰ = ده درصد گران‌تر، -۵ = ارزان‌تر)</label><input v-model.number="bulk.percent" type="number" class="ad-input" /></div>
        <div><label class="ad-label">شامل</label>
          <select v-model="bulk.form" class="ad-input"><option value="">همهٔ کودها</option><option value="liquid">فقط مایع</option><option value="powder">فقط پودر</option><option value="crystal">فقط کریستال</option><option value="granular">فقط گرانول</option></select>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="bulkOpen = false">انصراف</button><button class="ad-btn-primary" :disabled="saving || !bulk.percent" @click="applyBulk">اعمال</button></div>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import FertilizerStatsAndTable from '@/components/features/fertilizer-db/FertilizerStatsAndTable.vue';
import FertilizerModal from '@/components/features/fertilizer-db/FertilizerModal.vue';
import { adminApi, apiError, faN } from '@/services/adminApi';
import { confirmDialog, toast } from './adminUi';

const loading = ref(false);
const saving = ref(false);
const raw = ref<any[]>([]);
const activeFilter = ref<string | null>(null);
const showModal = ref(false);
const isEditing = ref(false);

// ردیف‌ها با ساختار «camelCase» که جدول کاربران انتظار دارد
const rows = computed(() => raw.value.map((r) => ({
  id: String(r.id), user_id: null, name: r.name, brand: r.brand ?? '', category: r.category ?? '', form: r.form ?? undefined,
  concentration: r.concentration ?? 100, elements: r.elements || {}, pricePerKg: r.price_per_kg ?? 0,
  isAcid: !!r.is_acid, isBase: !!r.is_base, densityGMl: r.density_g_ml ?? undefined, priceUnit: r.price_unit ?? undefined,
  formula: r.formula ?? '', labelValues: r.label_values ?? {}, phParams: r.ph_params ?? undefined, description: r.description ?? '',
  isSystemDefault: true, createdAt: r.created_at ? new Date(r.created_at) : new Date(), updatedAt: r.updated_at ? new Date(r.updated_at) : new Date(),
})));
const shopOf = (f: any) => raw.value.find((r) => String(r.id) === String(f.id));
const shopTitle = (f: any) => { const s = shopOf(f); return s?.shop_enabled === false ? 'در فروشگاه نمایش داده نمی‌شود' : 'تنظیمات فروش' + (s?.shop_stock != null ? ` (موجودی ${faN(s.shop_stock)})` : ''); };

const summary = computed(() => {
  const a = raw.value;
  const priced = a.filter((x) => x.price_per_kg > 0);
  const avg = priced.length ? Math.round(priced.reduce((s, x) => s + x.price_per_kg, 0) / priced.length) : 0;
  return [
    { l: 'کل کودهای سیستمی', v: faN(a.length), icon: '🧪', color: '#2563eb' },
    { l: 'نمایش در فروشگاه', v: faN(a.filter((x) => x.shop_enabled !== false && (x.shop_price ?? x.price_per_kg) > 0).length), icon: '🛒', color: '#8b5cf6' },
    { l: 'بدون قیمت', v: faN(a.length - priced.length), icon: '⚠️', color: '#f59e0b' },
    { l: 'میانگین قیمت', v: faN(avg), icon: '💰', color: '#10b981' },
  ];
});

async function load() {
  loading.value = true;
  try { raw.value = (await adminApi.fertilizers()).items; } catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
onMounted(load);

// ===== فرم (همان ساختار فرم صفحهٔ کاربر) =====
const initial = {
  id: null as string | null, name: '', brand: '', category: '', form: '' as '' | 'liquid' | 'powder' | 'crystal' | 'granular',
  concentration: 100, price_per_kg: null as number | null, formula: '', elements: {} as Record<string, number>,
  label_values: {} as Record<string, number>, is_acid: false, is_base: false, ph_purity: null as number | null,
  ph_mw: null as number | null, ph_eq: null as number | null, description: '', is_system_default: true,
  source_system_id: null as number | null, density_g_ml: null as number | null, price_unit: 'kg' as 'kg' | 'l',
};
const formData = reactive({ ...initial });
const reset = () => { Object.assign(formData, { ...initial, elements: {}, label_values: {} }); isEditing.value = false; };
const openAdd = () => { reset(); showModal.value = true; };
const closeModal = () => { showModal.value = false; reset(); };

const displayPrice = (f: any) => {
  const perKg = Number(f.pricePerKg || 0), d = Number(f.densityGMl || 0);
  return f.priceUnit === 'l' && d > 0 ? Math.round(perKg * d * 100) / 100 : perKg;
};
const openEdit = (f: any) => {
  isEditing.value = true;
  const pp = f.phParams || {};
  Object.assign(formData, {
    id: f.id, name: f.name || '', brand: f.brand || '', category: f.category || '', form: f.form || '',
    concentration: f.concentration || 100, price_per_kg: displayPrice(f) || null, formula: f.formula || '',
    elements: { ...(f.elements || {}) }, label_values: { ...(f.labelValues || {}) }, is_acid: !!f.isAcid, is_base: !!f.isBase,
    ph_purity: pp.purity_pct ?? null, ph_mw: pp.molar_mass ?? null, ph_eq: pp.equivalents ?? null, description: f.description || '',
    is_system_default: true, source_system_id: null, density_g_ml: f.densityGMl || null,
    price_unit: f.priceUnit === 'l' && f.densityGMl ? 'l' : 'kg',
  });
  showModal.value = true;
};

async function save() {
  const f = formData;
  if (!f.name.trim()) return toast('نام کود را وارد کنید', 'error');
  if (Number(f.price_per_kg) < 0) return toast('قیمت نمی‌تواند منفی باشد', 'error');
  if (f.concentration < 0 || f.concentration > 100) return toast('خلوص باید بین ۰ تا ۱۰۰ باشد', 'error');
  const liquid = f.form === 'liquid';
  if (liquid && (f.price_unit === 'l' || f.is_acid || f.is_base) && !(Number(f.density_g_ml) > 0)) return toast('برای کود مایع در این حالت چگالی را وارد کنید', 'error');
  const adj = f.is_acid || f.is_base;
  if (adj && !(Number(f.ph_purity) > 0 && Number(f.ph_purity) <= 100 && Number(f.ph_mw) > 0 && Number(f.ph_eq) > 0)) return toast('برای اسید/باز، غلظت، جرم مولی و تعداد H⁺/OH⁻ را وارد کنید', 'error');
  if (f.is_acid && f.is_base) return toast('یک ماده همزمان اسید و باز نیست', 'error');

  const elements: Record<string, number> = {};
  for (const [k, v] of Object.entries(f.elements)) { const n = Number(v); if (!isNaN(n) && n > 0) elements[k] = n; }
  const density = liquid && Number(f.density_g_ml) > 0 ? Number(f.density_g_ml) : null;
  const perL = liquid && f.price_unit === 'l' && density !== null;
  const body: any = {
    name: f.name.trim(), brand: f.brand || null, category: f.category || null, form: f.form || null, concentration: f.concentration,
    price_per_kg: (perL ? Number(f.price_per_kg) / (density as number) : Number(f.price_per_kg)) || 0,
    formula: f.formula || null, label_values: f.label_values || {}, elements, is_acid: f.is_acid, is_base: f.is_base,
    ph_params: adj ? { purity_pct: Number(f.ph_purity), molar_mass: Number(f.ph_mw), equivalents: Number(f.ph_eq) } : null,
    description: f.description || null, density_g_ml: density, price_unit: liquid ? (perL ? 'l' : 'kg') : null,
  };
  saving.value = true;
  try {
    if (isEditing.value && f.id) await adminApi.updateFertilizer(Number(f.id), body);
    else await adminApi.createFertilizer(body);
    toast(isEditing.value ? 'کود سیستمی به‌روزرسانی شد' : 'کود سیستمی افزوده شد');
    closeModal();
    await load();
  } catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}

async function remove(id: string) {
  const r = raw.value.find((x) => String(x.id) === String(id));
  if (!(await confirmDialog({ title: 'حذف کود سیستمی', message: `«${r?.name}» برای همهٔ کاربران از فهرست شرکتی و فروشگاه حذف می‌شود (نسخه‌های کپی‌شدهٔ کاربران می‌ماند).`, confirmText: 'حذف', danger: true }))) return;
  try { await adminApi.deleteFertilizer(Number(id)); toast('حذف شد'); await load(); } catch (e) { toast(apiError(e), 'error'); }
}

// ===== فروشگاه =====
const shopForm = ref<null | { id: number; name: string; enabled: boolean; price: number | null; stock: number | null; min: number | null; unit: string; base: number }>(null);
const openShop = (f: any) => {
  const r = shopOf(f); if (!r) return;
  shopForm.value = { id: r.id, name: r.name, enabled: r.shop_enabled !== false, price: r.shop_price ?? null, stock: r.shop_stock ?? null, min: r.shop_min_qty ?? null, unit: r.price_unit === 'l' ? 'لیتر' : 'کیلوگرم', base: r.price_per_kg || 0 };
};
async function saveShop() {
  const s = shopForm.value; if (!s) return;
  saving.value = true;
  try {
    await adminApi.fertilizerShop(s.id, {
      shop_enabled: s.enabled,
      shop_price: s.price ?? undefined, clear_price: s.price === null || (s.price as any) === '',
      shop_stock: s.stock ?? undefined, clear_stock: s.stock === null || (s.stock as any) === '',
      shop_min_qty: s.min ?? 0,
    });
    toast('تنظیمات فروش ذخیره شد'); shopForm.value = null; await load();
  } catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}

// ===== قیمت گروهی =====
const bulkOpen = ref(false);
const bulk = reactive({ percent: 0, form: '' });
async function applyBulk() {
  if (!(await confirmDialog({ title: 'تغییر گروهی قیمت', message: `قیمت ${bulk.form ? 'کودهای این شکل' : 'همهٔ کودهای سیستمی'} ${bulk.percent > 0 ? '+' : ''}${bulk.percent}٪ تغییر می‌کند.`, confirmText: 'اعمال' }))) return;
  saving.value = true;
  try { const r = await adminApi.bulkPrice({ percent: bulk.percent, form: bulk.form || null }); toast(`قیمت ${faN(r.updated)} کود به‌روزرسانی شد`); bulkOpen.value = false; bulk.percent = 0; await load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
</script>
