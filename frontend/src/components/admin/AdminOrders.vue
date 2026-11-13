<!-- frontend/src/components/admin/AdminOrders.vue -->
<!-- سفارش‌های فروشگاه: صف بررسی رسید، تأیید/رد، پیگیری ارسال + تنظیمات پرداخت کارت‌به‌کارت و فروشگاه -->
<template>
  <div class="space-y-3">
    <div class="flex gap-1 p-1 rounded-xl bg-gray-100 dark:bg-gray-800 w-fit">
      <button v-for="t in subs" :key="t.k" class="px-4 py-1.5 rounded-lg text-sm transition" :class="sub === t.k ? 'bg-white dark:bg-gray-700 shadow text-primary-700 dark:text-primary-300 font-semibold' : 'text-gray-500'" @click="sub = t.k">{{ t.l }}<span v-if="t.k === 'orders' && (counts.awaiting_review || 0)" class="mr-1.5 px-1.5 rounded-full bg-rose-500 text-white text-[10px]">{{ faN(counts.awaiting_review) }}</span></button>
    </div>

    <!-- ================= سفارش‌ها ================= -->
    <template v-if="sub === 'orders'">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div v-for="c in cards" :key="c.l" class="ad-card p-4"><p class="text-lg font-extrabold tabular-nums" :class="c.cls">{{ c.v }}</p><p class="text-[11px] text-gray-500">{{ c.l }}</p></div>
      </div>
      <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
        <div class="flex-1 min-w-[12rem]"><label class="ad-label">جستجو (کد سفارش، نام، شماره)</label><input v-model="q" class="ad-input" @keyup.enter="reload" /></div>
        <div class="w-52"><label class="ad-label">وضعیت</label>
          <select v-model="status" class="ad-input" @change="reload"><option value="">همه</option><option v-for="(l, k) in statuses" :key="k" :value="k">{{ l }}{{ counts[k] ? ` (${faN(counts[k])})` : '' }}</option></select>
        </div>
        <button class="ad-btn" @click="reload">جستجو</button>
      </div>
      <div class="ad-card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full min-w-[46rem]">
            <thead><tr><th class="ad-th">سفارش</th><th class="ad-th">مشتری</th><th class="ad-th">مبلغ</th><th class="ad-th">وضعیت</th><th class="ad-th">زمان</th><th class="ad-th"></th></tr></thead>
            <tbody>
              <tr v-if="loading && !rows.length"><td colspan="6" class="ad-td text-center text-gray-400 py-10">در حال بارگذاری…</td></tr>
              <tr v-else-if="!rows.length"><td colspan="6" class="ad-td text-center text-gray-400 py-10">سفارشی وجود ندارد.</td></tr>
              <tr v-for="o in rows" :key="o.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 cursor-pointer" @click="open(o.id)">
                <td class="ad-td"><p class="font-bold tabular-nums" dir="ltr">{{ o.code }}</p><p class="text-[11px] text-gray-400">{{ faN(o.items.length) }} قلم</p></td>
                <td class="ad-td"><p class="font-semibold text-gray-900 dark:text-white">{{ o.user_name }}</p><p class="text-[11px] text-gray-400" dir="ltr">{{ o.phone_number }}</p></td>
                <td class="ad-td tabular-nums">{{ faN(o.total) }}</td>
                <td class="ad-td"><span class="ad-chip" :class="CHIP[o.status]">{{ o.status_label }}</span><span v-if="o.has_receipt && o.status === 'awaiting_review'" class="mr-1">🧾</span></td>
                <td class="ad-td text-xs text-gray-500">{{ faDate(o.created_at) }}</td>
                <td class="ad-td text-left"><span class="ad-btn ad-btn-sm">بررسی</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <AdminPagination :page="page" :pages="pages" :total="total" @change="(p: number) => { page = p; load(); }" />
      </div>
    </template>

    <!-- ================= تنظیمات ================= -->
    <div v-else class="grid lg:grid-cols-2 gap-3">
      <div class="ad-card p-4 space-y-3">
        <h3 class="ad-title">پرداخت کارت‌به‌کارت</h3>
        <div><label class="ad-label">شمارهٔ کارت</label><input v-model="cfg.card_number" class="ad-input" dir="ltr" inputmode="numeric" maxlength="30" placeholder="6037-xxxx-xxxx-xxxx" /></div>
        <div class="grid grid-cols-2 gap-2.5">
          <div><label class="ad-label">نام صاحب کارت</label><input v-model="cfg.card_holder" class="ad-input" /></div>
          <div><label class="ad-label">نام بانک</label><input v-model="cfg.bank_name" class="ad-input" /></div>
        </div>
        <div><label class="ad-label">راهنمای پرداخت برای مشتری</label><textarea v-model="cfg.payment_note" rows="3" class="ad-input"></textarea></div>
        <label class="flex items-center justify-between text-sm"><span>ارسال تصویر رسید الزامی باشد</span><AdminSwitch v-model="cfg.receipt_required" /></label>
      </div>
      <div class="ad-card p-4 space-y-3">
        <h3 class="ad-title">قوانین فروشگاه</h3>
        <label class="flex items-center justify-between text-sm"><span>فروشگاه فعال باشد</span><AdminSwitch v-model="cfg.enabled" /></label>
        <label class="flex items-center justify-between text-sm"><span>آدرس تحویل الزامی باشد</span><AdminSwitch v-model="cfg.require_address" /></label>
        <div class="grid grid-cols-2 gap-2.5">
          <div><label class="ad-label">هزینهٔ ارسال</label><input v-model.number="cfg.shipping_fee" type="number" min="0" class="ad-input" /></div>
          <div><label class="ad-label">ارسال رایگان از مبلغ (۰ = ندارد)</label><input v-model.number="cfg.free_shipping_over" type="number" min="0" class="ad-input" /></div>
          <div><label class="ad-label">حداقل مبلغ سفارش</label><input v-model.number="cfg.min_order_total" type="number" min="0" class="ad-input" /></div>
          <div><label class="ad-label">واحد پول</label><input v-model="cfg.currency_label" class="ad-input" maxlength="20" /></div>
        </div>
        <div><label class="ad-label">پیام بالای فروشگاه (اختیاری)</label><textarea v-model="cfg.shop_note" rows="2" class="ad-input"></textarea></div>
        <p class="text-[11px] text-gray-500">قیمت و موجودی هر کود را در تب «کودهای سیستمی» با دکمهٔ 🛒 تعیین کنید.</p>
      </div>
      <div class="lg:col-span-2 flex justify-end"><button class="ad-btn-primary" :disabled="saving" @click="saveCfg">{{ saving ? 'در حال ذخیره…' : 'ذخیرهٔ تنظیمات' }}</button></div>
    </div>

    <!-- ================= جزئیات سفارش ================= -->
    <AppModal :open="!!cur" :title="cur ? 'سفارش ' + cur.code : ''" size="lg" @close="cur = null">
      <div v-if="cur" class="space-y-4">
        <div class="flex flex-wrap items-center gap-2"><span class="ad-chip" :class="CHIP[cur.status]">{{ cur.status_label }}</span><span class="text-xs text-gray-500">{{ faDate(cur.created_at) }}</span></div>
        <div class="grid sm:grid-cols-2 gap-3 text-sm">
          <div class="rounded-xl bg-gray-50 dark:bg-gray-900/40 p-3"><p class="text-[11px] text-gray-500">مشتری</p><p class="font-semibold">{{ cur.user_name }}</p><p class="text-xs text-gray-500" dir="ltr">{{ cur.phone_number }}</p></div>
          <div class="rounded-xl bg-gray-50 dark:bg-gray-900/40 p-3"><p class="text-[11px] text-gray-500">آدرس تحویل</p><p v-if="cur.address" class="text-xs leading-6">{{ cur.address.receiver }} · {{ cur.address.phone }}<br />{{ [cur.address.province, cur.address.city, cur.address.address].filter(Boolean).join('، ') }}<template v-if="cur.address.postal_code"><br />کدپستی: {{ cur.address.postal_code }}</template></p><p v-else class="text-xs text-gray-400">ثبت نشده</p></div>
        </div>
        <table class="w-full text-sm"><thead><tr><th class="ad-th">کود</th><th class="ad-th">مقدار</th><th class="ad-th">قیمت واحد</th><th class="ad-th">جمع</th></tr></thead>
          <tbody>
            <tr v-for="(it, i) in cur.items" :key="i"><td class="ad-td">{{ it.name }}</td><td class="ad-td tabular-nums">{{ faN(it.qty) }} {{ it.unit }}</td><td class="ad-td tabular-nums">{{ faN(it.unit_price) }}</td><td class="ad-td tabular-nums">{{ faN(it.line_total) }}</td></tr>
            <tr><td class="ad-td text-gray-500" colspan="3">هزینهٔ ارسال</td><td class="ad-td tabular-nums">{{ faN(cur.shipping) }}</td></tr>
            <tr><td class="ad-td font-bold" colspan="3">مبلغ کل</td><td class="ad-td font-bold tabular-nums">{{ faN(cur.total) }}</td></tr>
          </tbody></table>
        <p v-if="cur.customer_note" class="text-xs rounded-xl bg-amber-50 dark:bg-amber-900/20 p-3">یادداشت مشتری: {{ cur.customer_note }}</p>

        <div v-if="cur.receipt_image" class="space-y-1.5">
          <p class="text-xs font-semibold">رسید ارسالی <span v-if="cur.receipt_info?.last4" class="text-gray-500 font-normal">· ۴ رقم آخر کارت: {{ cur.receipt_info.last4 }}</span><span v-if="cur.receipt_info?.paid_amount" class="text-gray-500 font-normal"> · مبلغ اعلامی: {{ faN(cur.receipt_info.paid_amount) }}</span></p>
          <a :href="cur.receipt_image" target="_blank" rel="noopener"><img :src="cur.receipt_image" alt="رسید" class="max-h-72 rounded-xl border border-gray-200 dark:border-gray-700" /></a>
          <p v-if="cur.receipt_info?.note" class="text-xs text-gray-500">توضیح مشتری: {{ cur.receipt_info.note }}</p>
        </div>
        <p v-else class="text-xs text-gray-400">هنوز رسیدی ارسال نشده است.</p>

        <div class="space-y-2.5 border-t border-gray-100 dark:border-gray-700 pt-3">
          <div class="flex flex-wrap gap-1.5">
            <button v-for="a in actions(cur.status)" :key="a.s" class="ad-btn" :class="a.cls" :disabled="busy" @click="setStatus(a.s)">{{ a.l }}</button>
          </div>
          <div class="grid sm:grid-cols-2 gap-2.5">
            <div><label class="ad-label">کد رهگیری</label><input v-model="form.tracking_code" class="ad-input" dir="ltr" /></div>
            <div><label class="ad-label">دلیل رد (هنگام رد سفارش)</label><input v-model="form.reject_reason" class="ad-input" /></div>
          </div>
          <div><label class="ad-label">یادداشت خصوصی مدیر</label><textarea v-model="form.admin_note" rows="2" class="ad-input"></textarea></div>
          <button class="ad-btn-primary" :disabled="busy" @click="saveNotes">ذخیرهٔ یادداشت و رهگیری</button>
        </div>
      </div>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import AdminSwitch from './AdminSwitch.vue';
import AdminPagination from './AdminPagination.vue';
import { adminApi, apiError, faDate, faN } from '@/services/adminApi';
import { toast } from './adminUi';

const emit = defineEmits<{ (e: 'waiting', n: number): void }>();
const CHIP: Record<string, string> = {
  awaiting_payment: 'bg-gray-100 text-gray-600', awaiting_review: 'bg-amber-100 text-amber-700', approved: 'bg-emerald-100 text-emerald-700',
  processing: 'bg-sky-100 text-sky-700', shipped: 'bg-indigo-100 text-indigo-700', completed: 'bg-emerald-600 text-white', rejected: 'bg-rose-100 text-rose-700', cancelled: 'bg-gray-200 text-gray-500',
};
const subs = [{ k: 'orders', l: 'سفارش‌ها' }, { k: 'settings', l: 'تنظیمات پرداخت و فروشگاه' }] as const;
const sub = ref<'orders' | 'settings'>('orders');

const rows = ref<any[]>([]), page = ref(1), pages = ref(1), total = ref(0), loading = ref(false), busy = ref(false), saving = ref(false);
const q = ref(''), status = ref('');
const counts = ref<Record<string, number>>({}), statuses = ref<Record<string, string>>({});
const summary = ref({ revenue: 0, waiting_review: 0, total: 0 });
const cards = computed(() => [
  { l: 'در انتظار بررسی رسید', v: faN(summary.value.waiting_review), cls: 'text-amber-600' },
  { l: 'کل سفارش‌ها', v: faN(summary.value.total), cls: '' },
  { l: 'فروش تأییدشده', v: faN(summary.value.revenue), cls: 'text-emerald-600' },
  { l: 'لغو/رد شده', v: faN((counts.value.cancelled || 0) + (counts.value.rejected || 0)), cls: 'text-gray-500' },
]);

async function load() {
  loading.value = true;
  try {
    const [r, s] = await Promise.all([adminApi.orders({ q: q.value, status: status.value, page: page.value }), adminApi.ordersSummary()]);
    rows.value = r.items; pages.value = r.pages; total.value = r.total; counts.value = r.counts; statuses.value = r.statuses; summary.value = s;
    emit('waiting', s.waiting_review);
  } catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
const reload = () => { page.value = 1; load(); };

// ===== جزئیات =====
const cur = ref<any | null>(null);
const form = reactive({ tracking_code: '', reject_reason: '', admin_note: '' });
async function open(id: number) {
  try { cur.value = await adminApi.order(id); Object.assign(form, { tracking_code: cur.value.tracking_code || '', reject_reason: cur.value.reject_reason || '', admin_note: cur.value.admin_note || '' }); }
  catch (e) { toast(apiError(e), 'error'); }
}
const actions = (s: string) => {
  const A = (st: string, l: string, cls = '') => ({ s: st, l, cls });
  if (s === 'awaiting_review') return [A('approved', '✅ تأیید پرداخت', '!border-emerald-400 !text-emerald-700'), A('rejected', '✖ رد رسید', '!border-rose-300 !text-rose-700')];
  if (s === 'awaiting_payment') return [A('approved', 'تأیید دستی پرداخت'), A('cancelled', 'لغو سفارش', '!text-rose-700')];
  if (s === 'approved') return [A('processing', 'در حال آماده‌سازی'), A('shipped', 'ارسال شد')];
  if (s === 'processing') return [A('shipped', 'ارسال شد'), A('completed', 'تکمیل شد')];
  if (s === 'shipped') return [A('completed', 'تکمیل شد')];
  if (s === 'rejected' || s === 'cancelled') return [A('awaiting_review', 'بازگرداندن به صف')];
  return [];
};
async function setStatus(s: string) {
  if (!cur.value) return;
  if (s === 'rejected' && !form.reject_reason.trim()) return toast('دلیل رد را بنویسید', 'error');
  busy.value = true;
  try { cur.value = { ...cur.value, ...(await adminApi.updateOrder(cur.value.id, { status: s, reject_reason: form.reject_reason || undefined, tracking_code: form.tracking_code || undefined, admin_note: form.admin_note || undefined })) }; toast('وضعیت سفارش به‌روز شد'); load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { busy.value = false; }
}
async function saveNotes() {
  if (!cur.value) return; busy.value = true;
  try { await adminApi.updateOrder(cur.value.id, { tracking_code: form.tracking_code, admin_note: form.admin_note }); toast('ذخیره شد'); load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { busy.value = false; }
}

// ===== تنظیمات =====
const cfg = reactive<any>({ enabled: true, card_number: '', card_holder: '', bank_name: '', payment_note: '', shipping_fee: 0, free_shipping_over: 0, min_order_total: 0, receipt_required: true, require_address: true, currency_label: 'تومان', shop_note: '' });
async function loadCfg() { try { Object.assign(cfg, await adminApi.shopSettings()); } catch (e) { toast(apiError(e), 'error'); } }
async function saveCfg() {
  saving.value = true;
  try { Object.assign(cfg, await adminApi.saveShopSettings({ ...cfg })); toast('تنظیمات ذخیره شد'); } catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
onMounted(() => { load(); loadCfg(); });
</script>
