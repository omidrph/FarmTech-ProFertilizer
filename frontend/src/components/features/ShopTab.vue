<!-- frontend/src/components/features/ShopTab.vue -->
<!-- فروشگاه: کودهای سیستمی، سبد خرید قابل‌ویرایش، ثبت سفارش، پرداخت کارت‌به‌کارت و پیگیری سفارش‌ها -->
<template>
  <div class="space-y-4" dir="rtl">
    <div v-if="info && !info.enabled" class="rounded-2xl border border-amber-200 bg-amber-50 dark:bg-amber-900/20 dark:border-amber-800 p-6 text-center text-sm text-amber-800 dark:text-amber-200">فروشگاه موقتاً غیرفعال است.</div>
    <template v-else>
      <!-- زیرتب‌ها -->
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex gap-1 p-1 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <button v-for="t in subs" :key="t.k" class="relative px-3.5 py-1.5 rounded-lg text-sm transition" :class="sub === t.k ? 'bg-violet-600 text-white shadow' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'" @click="go(t.k)">
            {{ t.l }}<span v-if="t.k === 'cart' && shop.count" class="mr-1.5 px-1.5 rounded-full text-[10px]" :class="sub === 'cart' ? 'bg-white/25' : 'bg-violet-600 text-white'">{{ shop.count.toLocaleString('fa-IR') }}</span>
          </button>
        </div>
        <p v-if="info?.shop_note" class="text-xs text-gray-500 max-w-md">{{ info.shop_note }}</p>
      </div>
      <p v-if="msg" class="text-sm rounded-xl px-4 py-2.5" :class="msgErr ? 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-300' : 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300'">{{ msg }}</p>

      <!-- ================= کاتالوگ ================= -->
      <div v-if="sub === 'catalog'" class="space-y-3">
        <div class="relative max-w-md"><input v-model="q" :class="inp" class="pr-3" placeholder="جستجوی کود (نام، برند، فرمول)…" /></div>
        <div v-if="loadingItems" class="py-10 text-center text-sm text-gray-500">در حال بارگذاری…</div>
        <div v-else-if="!filtered.length" class="py-10 text-center text-sm text-gray-500">کودی برای فروش موجود نیست.</div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="p in filtered" :key="p.id" class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 flex flex-col gap-2.5 hover:shadow-md transition">
            <div class="flex items-start justify-between gap-2">
              <div class="min-w-0"><p class="font-bold text-gray-900 dark:text-white truncate">{{ p.name }}</p><p class="text-[11px] text-gray-500 truncate">{{ [p.brand, p.formula].filter(Boolean).join(' · ') || '—' }}</p></div>
              <span class="px-2 py-0.5 rounded-full text-[10px] bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 flex-shrink-0">{{ FORM[p.form || ''] || p.form || 'کود' }}</span>
            </div>
            <div class="flex flex-wrap gap-1"><span v-for="[el, v] in topEls(p)" :key="el" class="px-1.5 py-0.5 rounded-md text-[10px] bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300">{{ el }} {{ v.toLocaleString('fa-IR') }}٪</span></div>
            <div class="mt-auto flex items-end justify-between gap-2 pt-1">
              <div><p class="text-base font-extrabold tabular-nums text-gray-900 dark:text-white">{{ fa(p.price) }} <span class="text-[11px] font-normal text-gray-500">{{ cur }} / {{ p.unit }}</span></p><p v-if="p.stock !== null" class="text-[10px]" :class="p.stock > 0 ? 'text-gray-400' : 'text-rose-500'">{{ p.stock > 0 ? 'موجودی: ' + fa(p.stock) : 'ناموجود' }}</p></div>
              <div class="flex items-center gap-1.5">
                <input v-model.number="qtyOf[p.id]" type="number" min="0" step="0.5" class="w-16 px-2 py-1.5 text-sm text-center rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 tabular-nums" :placeholder="String(p.min_qty || 1)" />
                <button class="px-3 py-1.5 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-sm disabled:opacity-40" :disabled="p.stock === 0" @click="add(p)">+ سبد</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= سبد خرید ================= -->
      <div v-else-if="sub === 'cart'" class="grid lg:grid-cols-[1fr_20rem] gap-4 items-start">
        <div class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden">
          <div v-if="!lines.length" class="p-10 text-center text-sm text-gray-500">سبد خرید شما خالی است. <button class="text-violet-600 hover:underline mr-1" @click="go('catalog')">رفتن به فروشگاه</button></div>
          <ul v-else class="divide-y divide-gray-100 dark:divide-gray-700">
            <li v-for="l in lines" :key="l.fertilizer_id" class="p-3.5 flex flex-wrap items-center justify-between gap-3">
              <div class="min-w-0"><p class="font-semibold text-gray-900 dark:text-white">{{ l.name }}</p><p class="text-[11px] text-gray-500">{{ fa(l.unit_price) }} {{ cur }} / {{ l.unit }}</p></div>
              <div class="flex items-center gap-2">
                <input :value="l.qty" type="number" min="0" step="0.5" class="w-20 px-2 py-1.5 text-sm text-center rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 tabular-nums" @change="(e: any) => changeQty(l.fertilizer_id, Number(e.target.value))" />
                <span class="text-xs text-gray-500 w-10">{{ l.unit }}</span>
                <b class="tabular-nums w-24 text-left">{{ fa(l.line_total) }}</b>
                <button class="text-rose-500 hover:text-rose-700 text-lg leading-none" title="حذف" @click="changeQty(l.fertilizer_id, 0)">×</button>
              </div>
            </li>
          </ul>
        </div>

        <aside v-if="lines.length" class="rounded-2xl border border-violet-200 dark:border-violet-900/60 bg-white dark:bg-gray-800 p-4 space-y-3 lg:sticky lg:top-28">
          <h4 class="font-bold text-gray-900 dark:text-white">خلاصهٔ سفارش</h4>
          <div class="text-sm space-y-1">
            <p class="flex justify-between text-gray-500"><span>جمع اقلام</span><span class="tabular-nums">{{ fa(shop.cart?.subtotal || 0) }}</span></p>
            <p class="flex justify-between text-gray-500"><span>هزینهٔ ارسال</span><span class="tabular-nums">{{ fa(shop.cart?.shipping || 0) }}</span></p>
            <p class="flex justify-between font-bold text-gray-900 dark:text-white text-base pt-1.5 border-t border-gray-100 dark:border-gray-700"><span>مبلغ کل</span><span class="tabular-nums">{{ fa(shop.cart?.total || 0) }} {{ cur }}</span></p>
          </div>
          <template v-if="info?.require_address">
            <p class="text-xs font-semibold text-gray-700 dark:text-gray-300">آدرس تحویل</p>
            <input v-model="addr.receiver" :class="inp" placeholder="نام گیرنده *" />
            <input v-model="addr.phone" :class="inp" dir="ltr" inputmode="tel" placeholder="شمارهٔ تماس *" />
            <div class="grid grid-cols-2 gap-2"><input v-model="addr.province" :class="inp" placeholder="استان" /><input v-model="addr.city" :class="inp" placeholder="شهر" /></div>
            <textarea v-model="addr.address" rows="2" :class="inp" placeholder="آدرس کامل *"></textarea>
            <input v-model="addr.postal_code" :class="inp" dir="ltr" inputmode="numeric" placeholder="کدپستی" />
          </template>
          <textarea v-model="note" rows="2" :class="inp" placeholder="یادداشت برای سفارش (اختیاری)"></textarea>
          <button class="w-full py-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-white text-sm font-semibold disabled:opacity-50" :disabled="busy" @click="checkout">ثبت سفارش و رفتن به پرداخت</button>
          <p class="text-[11px] text-gray-500 leading-5">پس از ثبت سفارش، شمارهٔ کارت نمایش داده می‌شود و می‌توانید عکس رسید را بفرستید.</p>
        </aside>
      </div>

      <!-- ================= سفارش‌ها ================= -->
      <div v-else>
        <OrderPanel v-if="openOrder" :key="openOrder" :order-id="openOrder" @back="openOrder = null; loadOrders()" @changed="loadOrders" @reopened="reopened" />
        <div v-else class="space-y-2">
          <div v-if="!orders.length" class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-10 text-center text-sm text-gray-500">هنوز سفارشی ثبت نکرده‌اید.</div>
          <button v-for="o in orders" :key="o.id" class="w-full text-right rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 flex items-center justify-between gap-3 hover:shadow-md transition" @click="openOrder = o.id">
            <div><p class="font-bold tabular-nums text-gray-900 dark:text-white" dir="ltr">{{ o.code }}</p><p class="text-[11px] text-gray-500">{{ new Date(o.created_at).toLocaleDateString('fa-IR') }} · {{ o.items.length.toLocaleString('fa-IR') }} قلم</p></div>
            <div class="text-left"><p class="font-bold tabular-nums">{{ fa(o.total) }}</p><span class="text-[11px] px-2 py-0.5 rounded-full" :class="CHIP[o.status]">{{ o.status_label }}</span></div>
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import OrderPanel from './shop/OrderPanel.vue';
import { useShopStore } from '@/store/modules/shopStore';
import { shopApi, shopError, type ShopInfo, type ShopProduct } from '@/services/shopApi';

const shop = useShopStore();
const subs = [{ k: 'catalog', l: 'فروشگاه' }, { k: 'cart', l: 'سبد خرید' }, { k: 'orders', l: 'سفارش‌های من' }] as const;
type Sub = 'catalog' | 'cart' | 'orders';
const sub = ref<Sub>(shop.openOn);
const FORM: Record<string, string> = { liquid: 'مایع', powder: 'پودر', crystal: 'کریستال', granular: 'گرانول' };
const CHIP: Record<string, string> = {
  awaiting_payment: 'bg-gray-100 text-gray-600', awaiting_review: 'bg-amber-100 text-amber-700', approved: 'bg-emerald-100 text-emerald-700',
  processing: 'bg-sky-100 text-sky-700', shipped: 'bg-indigo-100 text-indigo-700', completed: 'bg-emerald-600 text-white', rejected: 'bg-rose-100 text-rose-700', cancelled: 'bg-gray-200 text-gray-500',
};
const inp = 'w-full px-3 py-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-violet-500 focus:border-transparent';

const info = ref<ShopInfo | null>(null);
const items = ref<ShopProduct[]>([]);
const loadingItems = ref(false);
const q = ref('');
const qtyOf = reactive<Record<number, number>>({});
const orders = ref<any[]>([]);
const openOrder = ref<number | null>(null);
const busy = ref(false);
const msg = ref(''), msgErr = ref(false);
const note = ref('');
const addr = reactive({ receiver: '', phone: '', province: '', city: '', address: '', postal_code: '' });

const cur = computed(() => info.value?.currency_label || 'تومان');
const fa = (v: number) => Math.round(v ?? 0).toLocaleString('fa-IR');
const lines = computed(() => shop.cart?.items || []);
const filtered = computed(() => {
  const t = q.value.trim().toLowerCase();
  return t ? items.value.filter((p) => [p.name, p.brand, p.formula].some((x) => (x || '').toLowerCase().includes(t))) : items.value;
});
const topEls = (p: ShopProduct) => Object.entries(p.elements || {}).filter(([, v]) => Number(v) > 0).sort((a, b) => Number(b[1]) - Number(a[1])).slice(0, 3) as [string, number][];

function flash(text: string, err = false) { msg.value = text; msgErr.value = err; if (!err) setTimeout(() => { if (msg.value === text) msg.value = ''; }, 3500); }
function go(k: Sub) { sub.value = k; msg.value = ''; if (k === 'orders') { openOrder.value = null; loadOrders(); } }

async function loadItems() { loadingItems.value = true; try { items.value = (await shopApi.items()).items; } catch (e) { flash(shopError(e), true); } finally { loadingItems.value = false; } }
async function loadOrders() { try { orders.value = await shopApi.orders(); } catch (e) { flash(shopError(e), true); } }

async function add(p: ShopProduct) {
  const qty = Number(qtyOf[p.id]) || p.min_qty || 1;
  if (await shop.addMany([{ fertilizer_id: p.id, qty }])) { flash(`«${p.name}» به سبد اضافه شد`); qtyOf[p.id] = 0 as any; } else flash(shop.error || 'خطا', true);
}
async function changeQty(id: number, qty: number) {
  const next = lines.value.map((l) => ({ fertilizer_id: l.fertilizer_id, qty: l.fertilizer_id === id ? qty : l.qty })).filter((l) => l.qty > 0);
  await shop.setQty(next);
  if (shop.error) flash(shop.error, true);
}
async function checkout() {
  msg.value = '';
  if (info.value?.require_address && (addr.receiver.trim().length < 2 || addr.phone.trim().length < 7 || addr.address.trim().length < 5)) return flash('نام گیرنده، شمارهٔ تماس و آدرس را کامل وارد کنید', true);
  busy.value = true;
  try {
    const o = await shopApi.checkout({ address: info.value?.require_address ? { ...addr } : undefined, customer_note: note.value || undefined });
    localStorage.setItem('shop_address', JSON.stringify(addr));
    await shop.loadCart(); note.value = '';
    sub.value = 'orders'; openOrder.value = o.id; loadOrders();
  } catch (e) { flash(shopError(e), true); } finally { busy.value = false; }
}
async function reopened() { await shop.loadCart(); openOrder.value = null; go('cart'); }

watch(() => shop.openRequest, () => { go(shop.openOn); if (shop.openOn === 'cart') shop.loadCart(); });
onMounted(async () => {
  try { Object.assign(addr, JSON.parse(localStorage.getItem('shop_address') || '{}')); } catch { /* ignore */ }
  try { info.value = await shopApi.info(); } catch (e) { flash(shopError(e), true); }
  shop.loadCart(); loadItems(); loadOrders();
  go(shop.openOn);
});
</script>
