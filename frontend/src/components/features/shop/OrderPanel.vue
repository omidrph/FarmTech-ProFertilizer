<!-- frontend/src/components/features/shop/OrderPanel.vue -->
<!-- جزئیات یک سفارش: پرداخت کارت‌به‌کارت، ارسال عکس رسید، پیگیری وضعیت -->
<template>
  <div class="space-y-4" v-if="o">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <button class="text-sm text-primary-600 dark:text-primary-400 hover:underline" @click="$emit('back')">← بازگشت به سفارش‌ها</button>
      <span class="px-3 py-1 rounded-full text-xs font-semibold" :class="CHIP[o.status]">{{ o.status_label }}</span>
    </div>

    <div class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
        <h3 class="font-bold text-gray-900 dark:text-white">سفارش <span dir="ltr" class="tabular-nums">{{ o.code }}</span></h3>
        <span class="text-xs text-gray-500">{{ date(o.created_at) }}</span>
      </div>
      <ul class="divide-y divide-gray-100 dark:divide-gray-700 text-sm">
        <li v-for="(it, i) in o.items" :key="i" class="py-2 flex items-center justify-between gap-3">
          <span class="min-w-0"><b class="text-gray-900 dark:text-white">{{ it.name }}</b><span class="text-xs text-gray-500"> · {{ fa(it.qty) }} {{ it.unit }} × {{ fa(it.unit_price) }}</span></span>
          <span class="tabular-nums flex-shrink-0">{{ fa(it.line_total) }}</span>
        </li>
      </ul>
      <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700 text-sm space-y-1">
        <p class="flex justify-between text-gray-500"><span>هزینهٔ ارسال</span><span class="tabular-nums">{{ fa(o.shipping) }}</span></p>
        <p class="flex justify-between font-bold text-gray-900 dark:text-white"><span>مبلغ قابل پرداخت</span><span class="tabular-nums">{{ fa(o.total) }} {{ o.payment?.currency_label || 'تومان' }}</span></p>
      </div>
    </div>

    <!-- پرداخت -->
    <div v-if="o.payment && ['awaiting_payment', 'awaiting_review', 'rejected'].includes(o.status)" class="rounded-2xl border border-violet-200 dark:border-violet-900/60 bg-violet-50/60 dark:bg-violet-900/10 p-4 space-y-3">
      <h4 class="font-bold text-violet-900 dark:text-violet-200">پرداخت کارت‌به‌کارت</h4>
      <div v-if="o.payment.card_number" class="rounded-xl bg-white dark:bg-gray-800 border border-violet-100 dark:border-violet-900/50 p-3.5 text-center space-y-1">
        <p class="text-[11px] text-gray-500">مبلغ را به این کارت واریز کنید</p>
        <p class="text-xl font-extrabold tracking-wider tabular-nums text-gray-900 dark:text-white select-all" dir="ltr">{{ fmtCard(o.payment.card_number) }}</p>
        <p class="text-sm text-gray-700 dark:text-gray-300">{{ o.payment.card_holder }}<span v-if="o.payment.bank_name"> · {{ o.payment.bank_name }}</span></p>
        <button class="mt-1 px-3 py-1 rounded-lg text-xs border border-violet-200 dark:border-violet-800 text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-900/30" @click="copy(o.payment.card_number)">کپی شمارهٔ کارت</button>
      </div>
      <p v-else class="text-sm text-amber-700 dark:text-amber-300">اطلاعات کارت هنوز توسط مدیر ثبت نشده است؛ لطفاً با پشتیبانی تماس بگیرید.</p>
      <p v-if="o.payment.payment_note" class="text-xs leading-6 text-gray-600 dark:text-gray-300">{{ o.payment.payment_note }}</p>
      <p v-if="o.status === 'rejected'" class="text-sm rounded-xl bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-300 p-3">رسید شما رد شد: {{ o.reject_reason || '—' }}. می‌توانید رسید جدید بفرستید.</p>

      <div class="space-y-2.5">
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-300">عکس رسید پرداخت</label>
        <input ref="fileEl" type="file" accept="image/png,image/jpeg,image/webp" class="hidden" @change="onFile" />
        <button class="w-full rounded-xl border-2 border-dashed border-violet-300 dark:border-violet-700 py-5 text-sm text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-900/20 transition" @click="fileEl?.click()">
          {{ image ? 'تغییر تصویر' : '📷 انتخاب یا گرفتن عکس رسید' }}
        </button>
        <img v-if="image" :src="image" alt="رسید" class="max-h-56 mx-auto rounded-xl border border-gray-200 dark:border-gray-700" />
        <img v-else-if="o.receipt_image" :src="o.receipt_image" alt="رسید ارسال‌شده" class="max-h-56 mx-auto rounded-xl border border-gray-200 dark:border-gray-700 opacity-80" />
        <div class="grid grid-cols-2 gap-2.5">
          <div><label class="block text-[11px] text-gray-500 mb-1">۴ رقم آخر کارت پرداخت‌کننده (اختیاری)</label><input v-model="last4" maxlength="4" inputmode="numeric" dir="ltr" :class="inp" /></div>
          <div><label class="block text-[11px] text-gray-500 mb-1">توضیح (اختیاری)</label><input v-model="note" maxlength="300" :class="inp" /></div>
        </div>
        <button class="w-full py-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-white text-sm font-semibold disabled:opacity-50" :disabled="busy || !image" @click="send">{{ o.status === 'awaiting_review' ? 'ارسال رسید جدید' : 'ارسال رسید و ثبت در صف بررسی' }}</button>
        <p v-if="o.status === 'awaiting_review'" class="text-xs text-center text-emerald-600 dark:text-emerald-400">رسید شما ارسال شده و در صف بررسی مدیر است ✓</p>
      </div>
    </div>

    <p v-else-if="o.status === 'approved' || o.status === 'processing'" class="rounded-2xl bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-200 text-sm p-4">پرداخت شما تأیید شد و سفارش در حال آماده‌سازی است.</p>
    <p v-if="o.tracking_code" class="rounded-2xl bg-indigo-50 dark:bg-indigo-900/20 text-indigo-800 dark:text-indigo-200 text-sm p-4">کد رهگیری مرسوله: <b class="tabular-nums select-all" dir="ltr">{{ o.tracking_code }}</b></p>
    <p v-if="o.status === 'cancelled'" class="text-sm text-gray-500">این سفارش لغو شده است.</p>

    <div class="flex flex-wrap gap-2">
      <button v-if="['awaiting_payment', 'awaiting_review', 'rejected'].includes(o.status)" class="px-4 py-2 rounded-xl text-sm border border-rose-200 dark:border-rose-900 text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/20" :disabled="busy" @click="cancel">لغو سفارش</button>
      <button v-if="['cancelled', 'rejected'].includes(o.status)" class="px-4 py-2 rounded-xl text-sm border border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700" :disabled="busy" @click="reopen">برگرداندن اقلام به سبد</button>
    </div>
    <p v-if="err" class="text-sm text-rose-600">{{ err }}</p>
  </div>
  <div v-else class="py-10 text-center text-sm text-gray-500">{{ err || 'در حال بارگذاری…' }}</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { shopApi, shopError } from '@/services/shopApi';

const props = defineProps<{ orderId: number }>();
const emit = defineEmits<{ (e: 'back'): void; (e: 'changed'): void; (e: 'reopened'): void }>();

const CHIP: Record<string, string> = {
  awaiting_payment: 'bg-gray-100 text-gray-600', awaiting_review: 'bg-amber-100 text-amber-700', approved: 'bg-emerald-100 text-emerald-700',
  processing: 'bg-sky-100 text-sky-700', shipped: 'bg-indigo-100 text-indigo-700', completed: 'bg-emerald-600 text-white', rejected: 'bg-rose-100 text-rose-700', cancelled: 'bg-gray-200 text-gray-500',
};
const inp = 'w-full px-3 py-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100';
const o = ref<any | null>(null);
const err = ref(''), busy = ref(false);
const image = ref(''), last4 = ref(''), note = ref('');
const fileEl = ref<HTMLInputElement | null>(null);
const fa = (v: number) => (v ?? 0).toLocaleString('fa-IR');
const date = (iso: string) => (iso ? new Date(iso).toLocaleString('fa-IR', { dateStyle: 'medium', timeStyle: 'short' }) : '');
const fmtCard = (c: string) => c.replace(/\D/g, '').replace(/(\d{4})(?=\d)/g, '$1 ').trim() || c;

async function load() {
  try { o.value = await shopApi.order(props.orderId); err.value = ''; } catch (e) { err.value = shopError(e, 'سفارش پیدا نشد'); }
}
onMounted(load);
const copy = async (t: string) => { try { await navigator.clipboard.writeText(t.replace(/\D/g, '')); } catch { /* ignore */ } };

// عکس را قبل از ارسال کوچک می‌کنیم (حداکثر ۱۴۰۰ پیکسل، JPEG) تا سریع و کم‌حجم آپلود شود
function onFile(ev: Event) {
  const f = (ev.target as HTMLInputElement).files?.[0];
  if (!f) return;
  if (!/^image\/(png|jpe?g|webp)$/.test(f.type)) { err.value = 'فقط تصویر PNG، JPG یا WebP'; return; }
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      const k = Math.min(1, 1400 / Math.max(img.width, img.height));
      const c = document.createElement('canvas');
      c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
      c.getContext('2d')!.drawImage(img, 0, 0, c.width, c.height);
      image.value = c.toDataURL('image/jpeg', 0.82); err.value = '';
    };
    img.onerror = () => (err.value = 'تصویر خوانده نشد');
    img.src = String(reader.result);
  };
  reader.readAsDataURL(f);
}
async function send() {
  busy.value = true; err.value = '';
  try {
    await shopApi.sendReceipt(props.orderId, { image: image.value, last4: last4.value || undefined, note: note.value || undefined });
    image.value = ''; await load(); emit('changed');
  } catch (e) { err.value = shopError(e); } finally { busy.value = false; }
}
async function cancel() {
  if (!confirm('این سفارش لغو شود؟')) return;
  busy.value = true;
  try { await shopApi.cancel(props.orderId); await load(); emit('changed'); } catch (e) { err.value = shopError(e); } finally { busy.value = false; }
}
async function reopen() {
  busy.value = true;
  try { await shopApi.reopen(props.orderId); emit('reopened'); } catch (e) { err.value = shopError(e); } finally { busy.value = false; }
}
</script>
