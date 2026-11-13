<!-- frontend/src/components/admin/AdminResets.vue -->
<!-- کدهای «فراموشی رمز» کاربران: وقتی پیامک نمی‌رسد، مدیر کد را می‌بیند/می‌دهد یا مستقیم رمز را تغییر می‌دهد -->
<template>
  <div class="space-y-3">
    <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
      <div class="flex-1 min-w-[12rem]"><label class="ad-label">جستجو (نام یا شماره)</label><input v-model="q" class="ad-input" @keyup.enter="reload" /></div>
      <div class="w-40"><label class="ad-label">وضعیت</label>
        <select v-model="state" class="ad-input" @change="reload"><option value="">همه</option><option value="pending">در انتظار (معتبر)</option><option value="used">استفاده‌شده</option><option value="expired">منقضی</option></select>
      </div>
      <button class="ad-btn" @click="reload">جستجو</button>
      <button class="ad-btn" @click="load">↻ تازه‌سازی</button>
      <label class="flex items-center gap-1.5 text-xs text-gray-500"><input v-model="auto" type="checkbox" class="accent-primary-600" /> به‌روزرسانی خودکار</label>
    </div>

    <div class="ad-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[42rem]">
          <thead><tr><th class="ad-th">کاربر</th><th class="ad-th">کد پیامکی</th><th class="ad-th">وضعیت</th><th class="ad-th">زمان درخواست</th><th class="ad-th">عملیات</th></tr></thead>
          <tbody>
            <tr v-if="loading && !rows.length"><td colspan="5" class="ad-td text-center text-gray-400 py-10">در حال بارگذاری…</td></tr>
            <tr v-else-if="!rows.length"><td colspan="5" class="ad-td text-center text-gray-400 py-10">درخواستی ثبت نشده است.</td></tr>
            <tr v-for="r in rows" :key="r.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30">
              <td class="ad-td"><p class="font-semibold text-gray-900 dark:text-white">{{ r.user_name }}</p><p class="text-[11px] text-gray-400 tabular-nums" dir="ltr">{{ r.phone_number }}</p></td>
              <td class="ad-td">
                <div class="flex items-center gap-1.5">
                  <code class="px-2.5 py-1 rounded-lg bg-gray-100 dark:bg-gray-900/50 font-mono text-base tracking-widest select-all" dir="ltr">{{ r.code || '—' }}</code>
                  <button v-if="r.code" class="ad-btn ad-btn-sm" @click="copy(r.code)">کپی</button>
                </div>
              </td>
              <td class="ad-td"><span class="ad-chip" :class="CHIP[r.state]">{{ LABEL[r.state] }}</span><p v-if="r.state === 'pending'" class="text-[10px] text-gray-400 mt-0.5">تا {{ faDate(r.expires_at) }}</p></td>
              <td class="ad-td text-xs text-gray-500">{{ faDate(r.created_at) }}</td>
              <td class="ad-td">
                <div class="flex flex-wrap gap-1.5">
                  <button class="ad-btn ad-btn-sm" @click="openPw(r)">تعیین رمز</button>
                  <button class="ad-btn ad-btn-sm" @click="regen(r)">کد جدید</button>
                  <button v-if="r.state === 'pending'" class="ad-btn ad-btn-sm !text-rose-700" @click="expire(r)">باطل</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <AdminPagination :page="page" :pages="pages" :total="total" @change="(p: number) => { page = p; load(); }" />
    </div>

    <AppModal :open="!!pw" :title="'تعیین رمز برای ' + (pw?.user_name || '')" size="sm" @close="pw = null">
      <div v-if="pw" class="space-y-2.5">
        <p class="text-xs text-gray-500">رمز جدید فوراً اعمال می‌شود و کاربر از همهٔ دستگاه‌ها خارج می‌شود. رمز را به‌صورت امن به کاربر بدهید.</p>
        <div class="flex gap-2"><input v-model="newPw" class="ad-input" dir="ltr" placeholder="حداقل ۸ کاراکتر، حرف بزرگ/کوچک و عدد" /><button class="ad-btn flex-shrink-0" @click="newPw = gen()">ساخت رمز</button></div>
      </div>
      <template #footer><div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="pw = null">انصراف</button><button class="ad-btn-primary" :disabled="!newPw || busy" @click="applyPw">اعمال رمز</button></div></template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import AdminPagination from './AdminPagination.vue';
import { adminApi, apiError, faDate } from '@/services/adminApi';
import { toast } from './adminUi';

const LABEL: Record<string, string> = { pending: 'در انتظار', used: 'استفاده‌شده', expired: 'منقضی' };
const CHIP: Record<string, string> = { pending: 'bg-amber-100 text-amber-700', used: 'bg-emerald-100 text-emerald-700', expired: 'bg-gray-100 text-gray-500' };
const total = ref(0)
const rows = ref<any[]>([]), page = ref(1), pages = ref(1), loading = ref(false), busy = ref(false);
const q = ref(''), state = ref(''), auto = ref(true);
const pw = ref<any | null>(null), newPw = ref('');
const emit = defineEmits<{ (e: 'pending', n: number): void }>();

async function load() {
  loading.value = true;
  try { const r = await adminApi.resetRequests({ q: q.value, state: state.value, page: page.value }); rows.value = r.items; pages.value = r.pages; total.value = r.total; emit('pending', r.pending); }
  catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
const reload = () => { page.value = 1; load(); };
const copy = async (t: string) => { try { await navigator.clipboard.writeText(t); toast('کپی شد'); } catch { toast('کپی ناموفق بود', 'error'); } };
const openPw = (r: any) => { pw.value = r; newPw.value = ''; };
const gen = () => { const c = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'; let s = ''; for (let i = 0; i < 9; i++) s += c[Math.floor(Math.random() * c.length)]; return s + 'a7K'; };
async function applyPw() {
  if (!pw.value) return; busy.value = true;
  try { await adminApi.resetPassword(pw.value.user_id, newPw.value); await adminApi.expireReset(pw.value.id).catch(() => {}); toast('رمز تغییر کرد'); pw.value = null; load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { busy.value = false; }
}
async function regen(r: any) { try { const c = await adminApi.makeResetCode(r.user_id, false); toast(`کد جدید: ${c.code}`); load(); } catch (e) { toast(apiError(e), 'error'); } }
async function expire(r: any) { try { await adminApi.expireReset(r.id); toast('کد باطل شد'); load(); } catch (e) { toast(apiError(e), 'error'); } }

let timer: number | undefined;
const arm = () => { clearInterval(timer); if (auto.value) timer = window.setInterval(load, 15000); };
watch(auto, arm);
onMounted(() => { load(); arm(); });
onUnmounted(() => clearInterval(timer));
</script>
