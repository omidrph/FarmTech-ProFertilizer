<template>
  <div class="space-y-3">
    <div class="flex gap-1.5">
      <button v-for="t in tabs" :key="t.k" class="ad-btn" :class="tab === t.k ? '!border-primary-500 !text-primary-700 dark:!text-primary-300 bg-primary-50 dark:bg-primary-900/20' : ''" @click="tab = t.k">{{ t.l }}</button>
    </div>

    <!-- لاگ امنیتی -->
    <template v-if="tab === 'security'">
      <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
        <div class="w-52"><label class="ad-label">نوع رویداد</label>
          <select v-model="sec.event_type" class="ad-input"><option value="">همه</option><option v-for="t in eventTypes" :key="t" :value="t">{{ t }}</option></select></div>
        <div class="w-36"><label class="ad-label">شدت</label>
          <select v-model="sec.severity" class="ad-input"><option value="">همه</option><option>INFO</option><option>WARNING</option><option>ERROR</option><option>CRITICAL</option></select></div>
        <div class="w-36"><label class="ad-label">شناسهٔ کاربر</label><input v-model="sec.user_id" class="ad-input" dir="ltr" inputmode="numeric" /></div>
        <div class="flex-1 min-w-[10rem]"><label class="ad-label">IP یا مسیر</label><input v-model="sec.q" class="ad-input" dir="ltr" /></div>
      </div>
      <div class="ad-card overflow-hidden">
        <div class="overflow-x-auto"><table class="w-full min-w-[44rem]">
          <thead><tr><th class="ad-th">زمان</th><th class="ad-th">رویداد</th><th class="ad-th">شدت</th><th class="ad-th">کاربر</th><th class="ad-th">IP</th><th class="ad-th">مسیر</th></tr></thead>
          <tbody>
            <tr v-if="!secRows.length"><td colspan="6" class="ad-td text-center text-gray-400 py-8">موردی نیست.</td></tr>
            <tr v-for="l in secRows" :key="l.id">
              <td class="ad-td text-xs text-gray-500">{{ faDate(l.created_at) }}</td>
              <td class="ad-td text-xs font-medium" dir="ltr">{{ l.event_type }}</td>
              <td class="ad-td"><span class="ad-chip" :class="sevCls(l.severity)">{{ l.severity }}</span></td>
              <td class="ad-td text-xs tabular-nums">{{ l.user_id ?? '—' }}</td>
              <td class="ad-td text-xs" dir="ltr">{{ l.ip || '—' }}</td>
              <td class="ad-td text-xs text-gray-500" dir="ltr">{{ l.method }} {{ l.endpoint }}</td>
            </tr>
          </tbody></table></div>
        <AdminPagination :page="secPage" :pages="secPages" :total="secTotal" @change="(p) => { secPage = p; loadSec(); }" />
      </div>
    </template>

    <!-- لاگ مدیریتی -->
    <template v-else>
      <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
        <div class="w-56"><label class="ad-label">عملیات</label>
          <select v-model="aud.action" class="ad-input"><option value="">همه</option><option v-for="a in ACTIONS" :key="a.k" :value="a.k">{{ a.l }}</option></select></div>
      </div>
      <div class="ad-card overflow-hidden">
        <div class="overflow-x-auto"><table class="w-full min-w-[44rem]">
          <thead><tr><th class="ad-th">زمان</th><th class="ad-th">مدیر</th><th class="ad-th">عملیات</th><th class="ad-th">مورد</th><th class="ad-th">جزئیات</th><th class="ad-th">IP</th></tr></thead>
          <tbody>
            <tr v-if="!audRows.length"><td colspan="6" class="ad-td text-center text-gray-400 py-8">موردی نیست.</td></tr>
            <tr v-for="a in audRows" :key="a.id">
              <td class="ad-td text-xs text-gray-500">{{ faDate(a.created_at) }}</td>
              <td class="ad-td">{{ a.admin_name || a.admin_id }}</td>
              <td class="ad-td"><span class="ad-chip bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300">{{ actionLabel(a.action) }}</span></td>
              <td class="ad-td text-xs">{{ a.target_label || '—' }}</td>
              <td class="ad-td text-[11px] text-gray-500 max-w-[16rem] truncate" dir="ltr" :title="JSON.stringify(a.details)">{{ a.details ? JSON.stringify(a.details) : '—' }}</td>
              <td class="ad-td text-xs" dir="ltr">{{ a.ip || '—' }}</td>
            </tr>
          </tbody></table></div>
        <AdminPagination :page="audPage" :pages="audPages" :total="audTotal" @change="(p) => { audPage = p; loadAud(); }" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import AdminPagination from './AdminPagination.vue';
import { adminApi, apiError, faDate } from '@/services/adminApi';
import { toast } from './adminUi';

const tabs: { k: 'security' | 'audit'; l: string }[] = [{ k: 'security', l: 'لاگ امنیتی' }, { k: 'audit', l: 'کارهای مدیران' }];
const tab = ref<'security' | 'audit'>('security');
const ACTIONS = [
  { k: 'user.', l: 'همهٔ کارهای کاربران' }, { k: 'user.ban', l: 'بن' }, { k: 'user.block', l: 'مسدودسازی' }, { k: 'user.restore', l: 'رفع مسدودیت' },
  { k: 'user.delete', l: 'حذف کاربر' }, { k: 'user.role', l: 'تغییر نقش' }, { k: 'user.reset_password', l: 'ریست رمز' },
  { k: 'fertilizer.', l: 'کودهای سیستمی' }, { k: 'announcement.', l: 'اعلان‌ها' }, { k: 'setting.', l: 'تنظیمات' }
];
const LABELS: Record<string, string> = {
  'user.create': 'ساخت کاربر', 'user.update': 'ویرایش کاربر', 'user.role': 'تغییر نقش', 'user.block': 'مسدودسازی', 'user.ban': 'بن', 'user.restore': 'رفع مسدودیت',
  'user.reset_password': 'ریست رمز', 'user.revoke_sessions': 'بستن نشست‌ها', 'user.unlock': 'رفع قفل', 'user.disable_2fa': 'غیرفعال‌سازی ۲FA', 'user.delete': 'حذف کاربر',
  'fertilizer.create': 'کود جدید', 'fertilizer.update': 'ویرایش کود', 'fertilizer.delete': 'حذف کود',
  'announcement.create': 'اعلان جدید', 'announcement.update': 'ویرایش اعلان', 'announcement.delete': 'حذف اعلان', 'setting.update': 'تغییر تنظیمات'
};
const actionLabel = (a: string) => LABELS[a] || a;
const sevCls = (s: string) => s === 'CRITICAL' || s === 'ERROR' ? 'bg-rose-100 text-rose-700' : s === 'WARNING' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300';

const sec = reactive({ event_type: '', severity: '', user_id: '', q: '' });
const secRows = ref<any[]>([]); const eventTypes = ref<string[]>([]);
const secPage = ref(1), secPages = ref(1), secTotal = ref(0);
async function loadSec() {
  try { const r = await adminApi.securityLogs({ ...sec, page: secPage.value }); secRows.value = r.items; secPages.value = r.pages; secTotal.value = r.total; eventTypes.value = r.event_types; }
  catch (e) { toast(apiError(e), 'error'); }
}
const aud = reactive({ action: '' });
const audRows = ref<any[]>([]); const audPage = ref(1), audPages = ref(1), audTotal = ref(0);
async function loadAud() {
  try { const r = await adminApi.audit({ ...aud, page: audPage.value }); audRows.value = r.items; audPages.value = r.pages; audTotal.value = r.total; }
  catch (e) { toast(apiError(e), 'error'); }
}
let t: number | undefined;
watch(sec, () => { clearTimeout(t); t = window.setTimeout(() => { secPage.value = 1; loadSec(); }, 350); });
watch(aud, () => { audPage.value = 1; loadAud(); });
onMounted(() => { loadSec(); loadAud(); });
</script>
