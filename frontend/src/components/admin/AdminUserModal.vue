<template>
  <AppModal :open="true" :title="d ? d.full_name : 'کاربر'" :subtitle="d?.phone_number" size="lg" @close="$emit('close')">
    <div v-if="!d" class="py-10 text-center text-sm text-gray-500">{{ error || 'در حال بارگذاری…' }}</div>
    <div v-else class="space-y-5">
      <!-- خلاصه -->
      <div class="flex flex-wrap items-center gap-2">
        <AdminBadges :role="d.role" :status="d.status" />
        <span v-if="d.is_2fa_enabled" class="ad-chip bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300">۲FA فعال</span>
        <span v-if="d.locked_until" class="ad-chip bg-orange-100 text-orange-700">قفل موقت ورود</span>
      </div>
      <div v-if="d.status !== 'active'" class="rounded-xl border border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20 p-3 text-sm text-orange-800 dark:text-orange-200">
        <b>{{ d.status === 'banned' ? 'بن دائم' : 'مسدود' }}</b>
        <span v-if="d.status_until"> تا {{ faDate(d.status_until) }}</span>
        <span v-if="d.status_reason"> — دلیل: {{ d.status_reason }}</span>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center">
        <div v-for="c in countCards" :key="c.l" class="rounded-xl bg-gray-50 dark:bg-gray-900/40 p-2.5">
          <p class="text-lg font-bold tabular-nums text-gray-900 dark:text-white">{{ faN(c.v) }}</p>
          <p class="text-[10px] text-gray-500">{{ c.l }}</p>
        </div>
      </div>
      <dl class="grid sm:grid-cols-2 gap-x-6 gap-y-1.5 text-xs text-gray-600 dark:text-gray-300">
        <div class="flex justify-between"><dt>عضویت</dt><dd>{{ faDate(d.created_at) }}</dd></div>
        <div class="flex justify-between"><dt>آخرین ورود</dt><dd>{{ faDate(d.last_login) }}</dd></div>
        <div class="flex justify-between"><dt>آخرین IP</dt><dd dir="ltr">{{ d.last_ip || '—' }}</dd></div>
        <div class="flex justify-between"><dt>تلاش ناموفق ورود</dt><dd>{{ faN(d.failed_attempts) }}</dd></div>
      </dl>

      <!-- ویرایش -->
      <section>
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">ویرایش اطلاعات</h4>
        <div class="grid sm:grid-cols-3 gap-2.5">
          <div><label class="ad-label">نام</label><input v-model="form.first_name" class="ad-input" /></div>
          <div><label class="ad-label">نام خانوادگی</label><input v-model="form.last_name" class="ad-input" /></div>
          <div><label class="ad-label">شماره تلفن</label><input v-model="form.phone_number" class="ad-input" dir="ltr" inputmode="numeric" /></div>
        </div>
        <label class="ad-label mt-2.5">یادداشت خصوصی مدیر</label>
        <textarea v-model="form.admin_note" rows="2" class="ad-input" placeholder="فقط برای مدیران قابل مشاهده است"></textarea>
        <button class="ad-btn-primary mt-2.5" :disabled="busy || !dirty" @click="saveInfo">ذخیره تغییرات</button>
      </section>

      <!-- نقش -->
      <section>
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">نقش کاربر</h4>
        <div class="flex flex-wrap gap-2">
          <button v-for="r in roles" :key="r" class="ad-btn" :class="d.role === r ? '!border-primary-500 !text-primary-700 dark:!text-primary-300 bg-primary-50 dark:bg-primary-900/20' : ''" :disabled="busy || d.role === r" @click="changeRole(r)">
            {{ ROLE_LABEL[r] }}
          </button>
        </div>
      </section>

      <!-- وضعیت حساب -->
      <section>
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">وضعیت حساب</h4>
        <div v-if="d.status !== 'active'" class="mb-2"><button class="ad-btn-primary" :disabled="busy" @click="restore">رفع مسدودیت / بن</button></div>
        <div v-else class="space-y-2.5">
          <div class="grid sm:grid-cols-[1fr_9rem_auto] gap-2 items-end">
            <div><label class="ad-label">دلیل مسدودیت (اختیاری)</label><input v-model="blockForm.reason" class="ad-input" /></div>
            <div>
              <label class="ad-label">مدت</label>
              <select v-model="blockForm.hours" class="ad-input">
                <option :value="1">۱ ساعت</option><option :value="6">۶ ساعت</option><option :value="24">۱ روز</option>
                <option :value="72">۳ روز</option><option :value="168">۷ روز</option><option :value="720">۳۰ روز</option>
                <option :value="null">نامحدود</option>
              </select>
            </div>
            <button class="ad-btn !text-orange-700 !border-orange-300" :disabled="busy || isSelf" @click="block">مسدود کن</button>
          </div>
          <button class="ad-btn !text-rose-700 !border-rose-300" :disabled="busy || isSelf" @click="ban">بن دائم (با همان دلیل)</button>
        </div>
        <p v-if="isSelf" class="mt-1 text-[11px] text-gray-400">این حساب خودِ شماست؛ مسدود/حذف آن ممکن نیست.</p>
      </section>

      <!-- امنیت -->
      <section>
        <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">امنیت</h4>
        <div class="flex flex-wrap gap-2">
          <button class="ad-btn" :disabled="busy" @click="resetPassword(false)">ریست رمز (تصادفی)</button>
          <button class="ad-btn" :disabled="busy" @click="resetPassword(true)">تعیین رمز دلخواه…</button>
          <button class="ad-btn" :disabled="busy" @click="revoke">خروج از همهٔ دستگاه‌ها</button>
          <button class="ad-btn" :disabled="busy || !d.locked_until && !d.failed_attempts" @click="unlock">رفع قفل ورود</button>
          <button class="ad-btn" :disabled="busy || !d.is_2fa_enabled" @click="disable2fa">غیرفعال‌سازی ۲FA</button>
        </div>
        <div v-if="customPw !== null" class="mt-2.5 flex gap-2">
          <input v-model="customPw" class="ad-input" dir="ltr" placeholder="رمز جدید (حداقل ۸ کاراکتر، حرف بزرگ/کوچک و عدد)" />
          <button class="ad-btn-primary flex-shrink-0" :disabled="busy || !customPw" @click="submitCustomPw">اعمال</button>
        </div>
        <div v-if="newPassword" class="mt-2.5 rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 p-3 text-sm">
          رمز جدید (فقط همین یک‌بار نمایش داده می‌شود):
          <div class="mt-1.5 flex items-center gap-2">
            <code class="px-2 py-1 rounded bg-white dark:bg-gray-800 font-mono select-all" dir="ltr">{{ newPassword }}</code>
            <button class="ad-btn ad-btn-sm" @click="copyPw">کپی</button>
          </div>
        </div>
      </section>

      <!-- فعالیت‌ها -->
      <section class="grid sm:grid-cols-2 gap-3">
        <div>
          <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">رویدادهای امنیتی اخیر</h4>
          <p v-if="!d.recent_security.length" class="text-xs text-gray-400">موردی نیست.</p>
          <ul class="space-y-1 text-xs">
            <li v-for="l in d.recent_security" :key="l.id" class="flex justify-between gap-2"><span>{{ l.event_type }}</span><span class="text-gray-400">{{ faDate(l.created_at) }}</span></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-2">محاسبه‌های اخیر</h4>
          <p v-if="!d.recent_calculations.length" class="text-xs text-gray-400">موردی نیست.</p>
          <ul class="space-y-1 text-xs">
            <li v-for="c in d.recent_calculations" :key="c.id" class="flex justify-between gap-2">
              <span :class="c.is_successful ? '' : 'text-rose-600'">{{ c.is_successful ? 'موفق' : 'ناموفق' }}<template v-if="c.cost_total"> · {{ Math.round(c.cost_total).toLocaleString('fa-IR') }} تومان</template></span>
              <span class="text-gray-400">{{ faDate(c.created_at) }}</span>
            </li>
          </ul>
        </div>
      </section>

      <!-- حذف -->
      <section class="rounded-xl border border-rose-200 dark:border-rose-900 p-3">
        <h4 class="text-sm font-bold text-rose-700 dark:text-rose-400 mb-1">حذف حساب</h4>
        <p class="text-xs text-gray-500 mb-2">با حذف، گزارش‌ها، کودها و همهٔ داده‌های این کاربر برای همیشه پاک می‌شود. اگر فقط می‌خواهید دسترسی را ببندید، «مسدود/بن» را بزنید.</p>
        <button class="ad-btn-danger" :disabled="busy || isSelf" @click="remove">حذف دائمی کاربر</button>
      </section>
    </div>
  </AppModal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import AdminBadges from './AdminBadges.vue';
import { adminApi, apiError, faDate, faN, ROLE_LABEL, type AdminUserDetail, type Role } from '@/services/adminApi';
import { confirmDialog, toast } from './adminUi';

const props = defineProps<{ userId: number; selfId?: number }>();
const emit = defineEmits<{ (e: 'close'): void; (e: 'changed'): void }>();

const roles: Role[] = ['user', 'plus', 'admin'];
const d = ref<AdminUserDetail | null>(null);
const error = ref('');
const busy = ref(false);
const form = reactive({ first_name: '', last_name: '', phone_number: '', admin_note: '' });
const blockForm = reactive<{ reason: string; hours: number | null }>({ reason: '', hours: 24 });
const newPassword = ref('');
const customPw = ref<string | null>(null);

const isSelf = computed(() => !!props.selfId && props.selfId === props.userId);
const dirty = computed(() => !!d.value && (form.first_name !== d.value.first_name || form.last_name !== d.value.last_name ||
  form.phone_number !== d.value.phone_number || (form.admin_note || '') !== (d.value.admin_note || '')));
const countCards = computed(() => d.value ? [
  { l: 'گزارش', v: d.value.counts.reports }, { l: 'محاسبه', v: d.value.counts.calculations },
  { l: 'کود شخصی', v: d.value.counts.fertilizers }, { l: 'تنظیم pH', v: d.value.counts.ph_adjustments },
  { l: 'نشست فعال', v: d.value.counts.active_sessions }
] : []);

async function load() {
  try {
    d.value = await adminApi.user(props.userId);
    Object.assign(form, { first_name: d.value.first_name, last_name: d.value.last_name, phone_number: d.value.phone_number, admin_note: d.value.admin_note || '' });
  } catch (e) { error.value = apiError(e, 'دریافت اطلاعات کاربر ناموفق بود'); }
}
onMounted(load);

async function run(fn: () => Promise<any>, ok: string) {
  busy.value = true;
  try { await fn(); toast(ok); await load(); emit('changed'); }
  catch (e) { toast(apiError(e), 'error'); }
  finally { busy.value = false; }
}

const saveInfo = () => run(() => adminApi.updateUser(props.userId, { ...form }), 'اطلاعات ذخیره شد');
const changeRole = async (r: Role) => {
  if (r === 'admin' && !(await confirmDialog({ title: 'ارتقا به مدیر', message: 'این کاربر به همهٔ بخش‌های پنل مدیریت دسترسی کامل پیدا می‌کند. مطمئنید؟', confirmText: 'ارتقا بده', danger: true }))) return;
  await run(() => adminApi.setRole(props.userId, r), 'نقش تغییر کرد');
};
const block = () => run(() => adminApi.block(props.userId, blockForm.reason, blockForm.hours), 'کاربر مسدود شد');
const ban = async () => {
  if (!(await confirmDialog({ title: 'بن دائم کاربر', message: 'کاربر دیگر نمی‌تواند وارد شود تا زمانی که شما رفعش کنید.', confirmText: 'بن کن', danger: true }))) return;
  await run(() => adminApi.ban(props.userId, blockForm.reason), 'کاربر بن شد');
};
const restore = () => run(() => adminApi.restore(props.userId), 'دسترسی کاربر برگشت');
const revoke = () => run(() => adminApi.revokeSessions(props.userId), 'همهٔ نشست‌ها بسته شد');
const unlock = () => run(() => adminApi.unlock(props.userId), 'قفل ورود برداشته شد');
const disable2fa = async () => {
  if (!(await confirmDialog({ title: 'غیرفعال‌سازی ۲FA', message: 'احراز هویت دومرحله‌ای این کاربر خاموش می‌شود.', confirmText: 'غیرفعال کن' }))) return;
  await run(() => adminApi.disable2fa(props.userId), '۲FA غیرفعال شد');
};

async function resetPassword(custom: boolean) {
  newPassword.value = '';
  if (custom) { customPw.value = customPw.value === null ? '' : null; return; }
  if (!(await confirmDialog({ title: 'ریست رمز', message: 'یک رمز تصادفی ساخته می‌شود و کاربر از همهٔ دستگاه‌ها خارج می‌شود.', confirmText: 'ریست کن' }))) return;
  busy.value = true;
  try { const r = await adminApi.resetPassword(props.userId); newPassword.value = r.password || ''; toast('رمز ریست شد'); emit('changed'); await load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { busy.value = false; }
}
async function submitCustomPw() {
  await run(() => adminApi.resetPassword(props.userId, customPw.value || ''), 'رمز تغییر کرد');
  customPw.value = null;
}
async function copyPw() {
  try { await navigator.clipboard.writeText(newPassword.value); toast('کپی شد'); } catch { toast('کپی ناموفق بود', 'error'); }
}
async function remove() {
  if (!d.value) return;
  if (!(await confirmDialog({ title: `حذف دائمی «${d.value.full_name}»`, message: 'این کار برگشت‌پذیر نیست و همهٔ داده‌های کاربر پاک می‌شود.', confirmText: 'حذف کن', danger: true }))) return;
  busy.value = true;
  try { await adminApi.deleteUser(props.userId); toast('کاربر حذف شد'); emit('changed'); emit('close'); }
  catch (e) { toast(apiError(e), 'error'); } finally { busy.value = false; }
}
</script>
