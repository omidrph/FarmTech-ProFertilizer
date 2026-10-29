<template>
  <div class="grid lg:grid-cols-2 gap-3">
    <div class="ad-card p-4 space-y-3">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">حالت تعمیر</h3>
      <p class="text-xs text-gray-500">در حالت تعمیر فقط مدیران می‌توانند از برنامه استفاده کنند. بقیه می‌توانند وارد شوند اما پیام زیر را می‌بینند.</p>
      <label class="flex items-center justify-between gap-3 rounded-xl bg-gray-50 dark:bg-gray-900/40 px-3.5 py-3 text-sm"><span>حالت تعمیر <b :class="s.maintenance_enabled ? 'text-amber-600' : 'text-gray-400'">{{ s.maintenance_enabled ? 'فعال' : 'غیرفعال' }}</b></span><AdminSwitch v-model="s.maintenance_enabled" /></label>
      <div><label class="ad-label">پیام برای کاربران</label><input v-model="s.maintenance_message" class="ad-input" maxlength="300" placeholder="سامانه در حال به‌روزرسانی است؛ کمی بعد دوباره تلاش کنید." /></div>
    </div>

    <div class="ad-card p-4 space-y-3">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white">ثبت‌نام کاربران جدید</h3>
      <p class="text-xs text-gray-500">با بستن ثبت‌نام، کاربران موجود همچنان وارد می‌شوند ولی حساب جدید ساخته نمی‌شود (شما می‌توانید از «کاربران» حساب بسازید).</p>
      <label class="flex items-center justify-between gap-3 rounded-xl bg-gray-50 dark:bg-gray-900/40 px-3.5 py-3 text-sm"><span>ثبت‌نام کاربران جدید <b :class="s.registration_enabled ? 'text-emerald-600' : 'text-rose-500'">{{ s.registration_enabled ? 'باز' : 'بسته' }}</b></span><AdminSwitch v-model="s.registration_enabled" /></label>
      <div><label class="ad-label">پیام وقتی بسته است</label><input v-model="s.registration_message" class="ad-input" maxlength="300" placeholder="ثبت‌نام جدید در حال حاضر غیرفعال است." /></div>
    </div>

    <div class="lg:col-span-2 flex items-center gap-2">
      <button class="ad-btn-primary" :disabled="saving || !loaded" @click="save">ذخیرهٔ تنظیمات</button>
      <span class="text-xs text-gray-400">تغییرات حداکثر تا ۱۰ ثانیه روی همهٔ سرورها اعمال می‌شود.</span>
    </div>

    <div class="ad-card p-4 lg:col-span-2">
      <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">سلامت سیستم</h3>
      <div v-if="!sys" class="text-sm text-gray-400">در حال بارگذاری…</div>
      <dl v-else class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm [&>div]:rounded-xl [&>div]:bg-gray-50 [&>div]:dark:bg-gray-900/40 [&>div]:p-3">
        <div><dt class="text-[11px] text-gray-500">دیتابیس</dt><dd :class="sys.database.ok ? 'text-emerald-600' : 'text-rose-600'" class="font-semibold">{{ sys.database.ok ? 'سالم' : 'مشکل دارد' }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">حجم دیتابیس</dt><dd class="font-semibold tabular-nums">{{ mb(sys.database.size_bytes) }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">نشست‌های فعال</dt><dd class="font-semibold tabular-nums">{{ faN(sys.active_sessions) }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">زمان کارکرد سرویس</dt><dd class="font-semibold">{{ uptime(sys.uptime_seconds) }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">نسخه</dt><dd class="font-semibold" dir="ltr">{{ sys.version }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">پایتون</dt><dd class="font-semibold" dir="ltr">{{ sys.python }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">حالت دیباگ</dt><dd class="font-semibold" :class="sys.debug ? 'text-amber-600' : ''">{{ sys.debug ? 'روشن (روی سرور واقعی خاموش باشد)' : 'خاموش' }}</dd></div>
        <div><dt class="text-[11px] text-gray-500">ساعت سرور</dt><dd class="font-semibold text-xs">{{ faDate(sys.server_time) }}</dd></div>
      </dl>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import AdminSwitch from './AdminSwitch.vue';
import { adminApi, apiError, faDate, faN } from '@/services/adminApi';
import { toast } from './adminUi';

const s = reactive({ maintenance_enabled: false, maintenance_message: '', registration_enabled: true, registration_message: '' });
const sys = ref<any>(null);
const loaded = ref(false), saving = ref(false);

onMounted(async () => {
  try { Object.assign(s, await adminApi.settings()); loaded.value = true; sys.value = await adminApi.system(); }
  catch (e) { toast(apiError(e), 'error'); }
});
async function save() {
  saving.value = true;
  try { Object.assign(s, await adminApi.updateSettings({ ...s })); toast('تنظیمات ذخیره شد'); }
  catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
const mb = (b: number | null) => (b == null ? '—' : (b / 1048576).toLocaleString('fa-IR', { maximumFractionDigits: 1 }) + ' MB');
const uptime = (sec: number) => { const d = Math.floor(sec / 86400), h = Math.floor((sec % 86400) / 3600), m = Math.floor((sec % 3600) / 60); return d ? `${faN(d)} روز و ${faN(h)} ساعت` : h ? `${faN(h)} ساعت و ${faN(m)} دقیقه` : `${faN(m)} دقیقه`; };
</script>
