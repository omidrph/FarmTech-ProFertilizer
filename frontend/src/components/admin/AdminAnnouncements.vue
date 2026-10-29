<template>
  <div class="space-y-3">
    <div class="ad-card p-3 flex items-center justify-between gap-2">
      <p class="text-sm text-gray-600 dark:text-gray-300">اعلان‌های فعال بالای برنامه به کاربران نشان داده می‌شود.</p>
      <button class="ad-btn-primary flex-shrink-0" @click="openNew">+ اعلان جدید</button>
    </div>

    <div class="space-y-2">
      <div v-if="!items.length" class="ad-card p-8 text-center text-sm text-gray-400">{{ loading ? 'در حال بارگذاری…' : 'اعلانی ثبت نشده است.' }}</div>
      <div v-for="a in items" :key="a.id" class="ad-card p-3.5 flex flex-wrap items-start justify-between gap-3">
        <div class="min-w-0">
          <div class="flex flex-wrap items-center gap-1.5">
            <span class="ad-chip" :class="LEVELS[a.level].cls">{{ LEVELS[a.level].label }}</span>
            <span class="ad-chip bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300">{{ AUD[a.audience] }}</span>
            <span class="ad-chip" :class="a.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'">{{ a.is_active ? 'فعال' : 'غیرفعال' }}</span>
          </div>
          <p class="mt-1.5 font-semibold text-gray-900 dark:text-white">{{ a.title }}</p>
          <p v-if="a.body" class="text-sm text-gray-600 dark:text-gray-300 mt-0.5">{{ a.body }}</p>
          <p v-if="a.starts_at || a.ends_at" class="text-[11px] text-gray-400 mt-1">{{ a.starts_at ? 'از ' + faDate(a.starts_at) : '' }} {{ a.ends_at ? 'تا ' + faDate(a.ends_at) : '' }}</p>
        </div>
        <div class="flex gap-1.5 flex-shrink-0">
          <button class="ad-btn ad-btn-sm" @click="toggle(a)">{{ a.is_active ? 'غیرفعال کن' : 'فعال کن' }}</button>
          <button class="ad-btn ad-btn-sm" @click="openEdit(a)">ویرایش</button>
          <button class="ad-btn ad-btn-sm !text-rose-700" @click="remove(a)">حذف</button>
        </div>
      </div>
    </div>

    <AppModal :open="!!edit" :title="edit?.id ? 'ویرایش اعلان' : 'اعلان جدید'" size="md" @close="edit = null">
      <div v-if="edit" class="space-y-2.5">
        <div><label class="ad-label">عنوان *</label><input v-model="edit.title" class="ad-input" maxlength="150" /></div>
        <div><label class="ad-label">متن</label><textarea v-model="edit.body" rows="3" class="ad-input" maxlength="2000"></textarea></div>
        <div class="grid grid-cols-2 gap-2.5">
          <div><label class="ad-label">نوع</label><select v-model="edit.level" class="ad-input"><option v-for="(l, k) in LEVELS" :key="k" :value="k">{{ l.label }}</option></select></div>
          <div><label class="ad-label">مخاطب</label><select v-model="edit.audience" class="ad-input"><option v-for="(l, k) in AUD" :key="k" :value="k">{{ l }}</option></select></div>
          <div><label class="ad-label">شروع (اختیاری)</label><input v-model="edit.starts_at" type="datetime-local" class="ad-input" dir="ltr" /></div>
          <div><label class="ad-label">پایان (اختیاری)</label><input v-model="edit.ends_at" type="datetime-local" class="ad-input" dir="ltr" /></div>
        </div>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="edit.is_active" /> فعال باشد</label>
      </div>
      <template #footer><div class="flex justify-end gap-2 p-3"><button class="ad-btn" @click="edit = null">انصراف</button><button class="ad-btn-primary" :disabled="saving || !edit?.title" @click="save">ذخیره</button></div></template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import { adminApi, apiError, faDate } from '@/services/adminApi';
import { confirmDialog, toast } from './adminUi';

const LEVELS: Record<string, { label: string; cls: string }> = {
  info: { label: 'اطلاع‌رسانی', cls: 'bg-sky-100 text-sky-700' }, success: { label: 'خبر خوب', cls: 'bg-emerald-100 text-emerald-700' },
  warning: { label: 'هشدار', cls: 'bg-amber-100 text-amber-700' }, danger: { label: 'مهم', cls: 'bg-rose-100 text-rose-700' }
};
const AUD: Record<string, string> = { all: 'همه', user: 'فقط کاربران معمولی', plus: 'کاربران پلاس و مدیران' };

const items = ref<any[]>([]);
const loading = ref(false), saving = ref(false);
const edit = ref<any | null>(null);

async function load() { loading.value = true; try { items.value = (await adminApi.announcements()).items; } catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; } }
onMounted(load);

// datetime-local ⇄ ISO
const toLocal = (iso: string | null) => { if (!iso) return ''; const d = new Date(iso); const p = (n: number) => String(n).padStart(2, '0'); return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`; };
const toIso = (v: string) => (v ? new Date(v).toISOString() : null);

const openNew = () => (edit.value = { title: '', body: '', level: 'info', audience: 'all', is_active: true, starts_at: '', ends_at: '' });
const openEdit = (a: any) => (edit.value = { ...a, starts_at: toLocal(a.starts_at), ends_at: toLocal(a.ends_at) });
const payload = (a: any) => ({ title: a.title, body: a.body || null, level: a.level, audience: a.audience, is_active: !!a.is_active, starts_at: toIso(a.starts_at || ''), ends_at: toIso(a.ends_at || '') });

async function save() {
  if (!edit.value) return;
  saving.value = true;
  try { edit.value.id ? await adminApi.updateAnnouncement(edit.value.id, payload(edit.value)) : await adminApi.createAnnouncement(payload(edit.value)); toast('اعلان ذخیره شد'); edit.value = null; load(); }
  catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
async function toggle(a: any) { try { await adminApi.updateAnnouncement(a.id, payload({ ...a, starts_at: toLocal(a.starts_at), ends_at: toLocal(a.ends_at), is_active: !a.is_active })); load(); } catch (e) { toast(apiError(e), 'error'); } }
async function remove(a: any) {
  if (!(await confirmDialog({ title: `حذف اعلان «${a.title}»`, confirmText: 'حذف کن', danger: true }))) return;
  try { await adminApi.deleteAnnouncement(a.id); toast('اعلان حذف شد'); load(); } catch (e) { toast(apiError(e), 'error'); }
}
</script>
