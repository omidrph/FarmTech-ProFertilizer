<template>
  <div class="space-y-3">
    <!-- میان‌برهای فیلتر -->
    <div class="flex flex-wrap items-center gap-2">
      <button v-for="c in chips" :key="c.k" class="px-3 py-1.5 rounded-full text-xs border transition"
        :class="chip === c.k ? 'bg-primary-600 border-primary-600 text-white shadow-sm' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:border-primary-400'"
        @click="chip = c.k">{{ c.l }}</button>
    </div>

    <!-- جستجو و ابزارها -->
    <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
      <div class="flex-1 min-w-[12rem]"><label class="ad-label">جستجو</label>
        <div class="relative"><svg class="w-4 h-4 absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" /></svg>
          <input v-model="q" class="ad-input !pr-9" placeholder="نام یا شماره تلفن" /></div></div>
      <div class="w-40"><label class="ad-label">مرتب‌سازی</label>
        <select v-model="sort" class="ad-input"><option value="created_at">تاریخ عضویت</option><option value="last_login">آخرین ورود</option><option value="name">نام خانوادگی</option><option value="role">نقش</option></select></div>
      <button class="ad-btn" :disabled="exporting" @click="exportCsv">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" /></svg>
        {{ exporting ? 'در حال آماده‌سازی…' : 'خروجی CSV' }}
      </button>
      <button class="ad-btn-primary" @click="createOpen = true">+ کاربر جدید</button>
    </div>

    <!-- عملیات گروهی -->
    <div v-if="selected.size" class="ad-card p-3 flex flex-wrap items-center gap-2 !border-primary-300 dark:!border-primary-700 bg-primary-50/60 dark:bg-primary-900/10">
      <b class="text-sm">{{ selected.size.toLocaleString('fa-IR') }} کاربر انتخاب شده</b>
      <button class="ad-btn ad-btn-sm" @click="bulk('restore')">رفع مسدودیت</button>
      <button class="ad-btn ad-btn-sm" @click="bulk('block')">مسدود (۱ روز)</button>
      <button class="ad-btn ad-btn-sm !text-rose-700" @click="bulk('ban')">بن</button>
      <select class="ad-input !w-auto !py-1 text-xs" @change="bulkRole(($event.target as HTMLSelectElement))"><option value="">تغییر نقش…</option><option value="user">معمولی</option><option value="plus">پلاس</option><option value="admin">مدیر</option></select>
      <button class="ad-btn ad-btn-sm" @click="bulk('revoke_sessions')">خروج از دستگاه‌ها</button>
      <button class="ad-btn ad-btn-sm !text-rose-700" @click="bulk('delete')">حذف</button>
      <button class="ad-btn ad-btn-sm mr-auto" @click="selected.clear()">لغو انتخاب</button>
    </div>

    <!-- جدول -->
    <div class="ad-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[56rem]">
          <thead><tr>
            <th class="ad-th w-8"><input type="checkbox" :checked="allSelected" @change="toggleAll" /></th>
            <th class="ad-th">کاربر</th><th class="ad-th">شماره</th><th class="ad-th">نقش / وضعیت</th>
            <th class="ad-th">گزارش</th><th class="ad-th">محاسبه</th><th class="ad-th">آخرین ورود</th><th class="ad-th">عضویت</th><th class="ad-th"></th>
          </tr></thead>
          <tbody>
            <tr v-if="loading"><td colspan="9" class="ad-td text-center text-gray-400 py-8">در حال بارگذاری…</td></tr>
            <tr v-else-if="!rows.length"><td colspan="9" class="ad-td text-center text-gray-400 py-8">کاربری پیدا نشد.</td></tr>
            <tr v-for="u in rows" :key="u.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30">
              <td class="ad-td"><input type="checkbox" :checked="selected.has(u.id)" @change="toggle(u.id)" /></td>
              <td class="ad-td font-medium"><button class="flex items-center gap-2.5 hover:text-primary-600" @click="openId = u.id"><span class="ad-avatar" :style="avatarStyle(u.full_name)">{{ initials(u.full_name) }}</span>{{ u.full_name }}</button></td>
              <td class="ad-td tabular-nums" dir="ltr">{{ u.phone_number }}</td>
              <td class="ad-td"><div class="flex flex-wrap gap-1"><AdminBadges :role="u.role" :status="u.status" /></div></td>
              <td class="ad-td tabular-nums">{{ faN(u.reports_count) }}</td>
              <td class="ad-td tabular-nums">{{ faN(u.calculations_count) }}</td>
              <td class="ad-td text-xs text-gray-500">{{ faDate(u.last_login) }}</td>
              <td class="ad-td text-xs text-gray-500">{{ faDate(u.created_at, false) }}</td>
              <td class="ad-td"><button class="ad-btn ad-btn-sm" @click="openId = u.id">مدیریت</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <AdminPagination :page="page" :pages="pages" :total="total" @change="(p) => { page = p; load(); }" />
    </div>

    <AdminUserModal v-if="openId" :user-id="openId" :self-id="selfId" @close="openId = null" @changed="load" />

    <!-- ساخت کاربر -->
    <AppModal :open="createOpen" title="ساخت کاربر جدید" size="md" @close="createOpen = false">
      <div class="space-y-2.5">
        <div class="grid grid-cols-2 gap-2.5">
          <div><label class="ad-label">نام</label><input v-model="nu.first_name" class="ad-input" /></div>
          <div><label class="ad-label">نام خانوادگی</label><input v-model="nu.last_name" class="ad-input" /></div>
        </div>
        <div><label class="ad-label">شماره تلفن</label><input v-model="nu.phone_number" class="ad-input" dir="ltr" inputmode="numeric" placeholder="09123456789" /></div>
        <div><label class="ad-label">رمز عبور</label><input v-model="nu.password" class="ad-input" dir="ltr" /></div>
        <div><label class="ad-label">نقش</label>
          <select v-model="nu.role" class="ad-input"><option value="user">کاربر معمولی</option><option value="plus">کاربر پلاس</option><option value="admin">مدیر</option></select></div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="createOpen = false">انصراف</button><button class="ad-btn-primary" :disabled="creating" @click="create">ساخت کاربر</button></div>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import AdminBadges from './AdminBadges.vue';
import AdminPagination from './AdminPagination.vue';
import AdminUserModal from './AdminUserModal.vue';
import { adminApi, apiError, faDate, faN, type AdminUserRow } from '@/services/adminApi';
import { avatarStyle, confirmDialog, initials, toast } from './adminUi';

const props = defineProps<{ selfId?: number; openUserId?: number | null; initialQuery?: string }>();

const rows = ref<AdminUserRow[]>([]);
const total = ref(0), pages = ref(1), page = ref(1);
const loading = ref(false);
const q = ref(props.initialQuery || ''), sort = ref('created_at');
const chips = [
  { k: 'all', l: 'همه' }, { k: 'admin', l: 'مدیران' }, { k: 'plus', l: 'کاربران پلاس' }, { k: 'blocked', l: 'مسدود' },
  { k: 'banned', l: 'بن‌شده' }, { k: 'new', l: 'جدید (۷ روز)' }, { k: 'never', l: 'هرگز وارد نشده' }, { k: 'twofa', l: 'دارای ۲FA' }
];
const chip = ref('all');
const exporting = ref(false);
const filterParams = () => ({
  q: q.value.trim(), sort: sort.value,
  role: chip.value === 'admin' ? 'admin' : chip.value === 'plus' ? 'plus' : '',
  status: chip.value === 'blocked' ? 'blocked' : chip.value === 'banned' ? 'banned' : '',
  new_days: chip.value === 'new' ? 7 : '', never_logged_in: chip.value === 'never' ? true : '',
  two_fa: chip.value === 'twofa' ? true : ''
});
const selected = reactive(new Set<number>());
const openId = ref<number | null>(props.openUserId ?? null);
const createOpen = ref(false), creating = ref(false);
const nu = reactive({ first_name: '', last_name: '', phone_number: '', password: '', role: 'user' });

const allSelected = computed(() => rows.value.length > 0 && rows.value.every((r) => selected.has(r.id)));
const toggle = (id: number) => (selected.has(id) ? selected.delete(id) : selected.add(id));
const toggleAll = () => (allSelected.value ? selected.clear() : rows.value.forEach((r) => selected.add(r.id)));

async function load() {
  loading.value = true;
  try {
    const r = await adminApi.users({ ...filterParams(), page: page.value, page_size: 20 });
    rows.value = r.items; total.value = r.total; pages.value = r.pages;
  } catch (e) { toast(apiError(e, 'دریافت کاربران ناموفق بود'), 'error'); }
  finally { loading.value = false; }
}
let t: number | undefined;
watch([q], () => { clearTimeout(t); t = window.setTimeout(() => { page.value = 1; load(); }, 350); });
watch([chip, sort], () => { page.value = 1; selected.clear(); load(); });
onMounted(load);

async function create() {
  creating.value = true;
  try { await adminApi.createUser({ ...nu }); toast('کاربر ساخته شد'); createOpen.value = false; Object.assign(nu, { first_name: '', last_name: '', phone_number: '', password: '', role: 'user' }); load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { creating.value = false; }
}

async function bulk(action: string, extra: Record<string, any> = {}) {
  const danger = ['delete', 'ban'].includes(action);
  const label: Record<string, string> = { restore: 'رفع مسدودیت', block: 'مسدودسازی ۱ روزه', ban: 'بن', delete: 'حذف دائمی', revoke_sessions: 'بستن نشست‌ها', set_role: 'تغییر نقش' };
  if (!(await confirmDialog({ title: `${label[action]} ${selected.size.toLocaleString('fa-IR')} کاربر`, message: danger ? 'این کار روی همهٔ کاربران انتخاب‌شده اعمال می‌شود.' : '', confirmText: 'انجام بده', danger }))) return;
  try {
    const r = await adminApi.bulk({ ids: [...selected], action, hours: action === 'block' ? 24 : undefined, ...extra });
    toast(`${r.done.length.toLocaleString('fa-IR')} مورد انجام شد${r.skipped.length ? ` · ${r.skipped.length.toLocaleString('fa-IR')} مورد رد شد (${r.skipped[0].reason})` : ''}`, r.skipped.length ? 'error' : 'success');
    selected.clear(); load();
  } catch (e) { toast(apiError(e), 'error'); }
}
function bulkRole(el: HTMLSelectElement) { const v = el.value; el.value = ''; if (v) bulk('set_role', { role: v }); }

// خروجی CSV از همهٔ نتایجِ فیلتر فعلی (حداکثر ۲۰۰۰ ردیف)؛ BOM برای فارسی در Excel
async function exportCsv() {
  exporting.value = true;
  try {
    const all: AdminUserRow[] = [];
    for (let pg = 1; pg <= 20; pg++) {
      const r = await adminApi.users({ ...filterParams(), page: pg, page_size: 100 });
      all.push(...r.items);
      if (pg >= r.pages) break;
    }
    const ROLE: Record<string, string> = { user: 'معمولی', plus: 'پلاس', admin: 'مدیر' };
    const ST: Record<string, string> = { active: 'فعال', blocked: 'مسدود', banned: 'بن‌شده' };
    const esc = (v: any) => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const lines = [['نام', 'نام خانوادگی', 'شماره', 'نقش', 'وضعیت', 'گزارش‌ها', 'محاسبه‌ها', 'آخرین ورود', 'عضویت'].map(esc).join(',')];
    for (const u of all) lines.push([u.first_name, u.last_name, u.phone_number, ROLE[u.role], ST[u.status], u.reports_count, u.calculations_count, u.last_login || '', u.created_at || ''].map(esc).join(','));
    const blob = new Blob(['\ufeff' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `users-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
    toast(`${all.length.toLocaleString('fa-IR')} کاربر خروجی گرفته شد`);
  } catch (e) { toast(apiError(e), 'error'); } finally { exporting.value = false; }
}

defineExpose({ reload: load });
</script>
