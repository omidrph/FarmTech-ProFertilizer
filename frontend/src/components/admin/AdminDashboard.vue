<template>
  <div class="space-y-4">
    <!-- بنر خوش‌آمد -->
    <section class="relative overflow-hidden rounded-2xl bg-gradient-to-l from-primary-600 via-primary-700 to-primary-900 text-white p-5 sm:p-6 shadow-lg shadow-primary-900/10">
      <div class="absolute -left-10 -top-16 w-56 h-56 rounded-full bg-white/10 blur-2xl"></div>
      <div class="absolute left-24 -bottom-20 w-48 h-48 rounded-full bg-sky-300/10 blur-2xl"></div>
      <div class="relative flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-xs text-primary-100/90">{{ today }}</p>
          <h2 class="mt-1 text-xl sm:text-2xl font-extrabold">{{ greeting }}، {{ name }} 👋</h2>
          <p class="mt-1 text-sm text-primary-100/90">
            <template v-if="s"><b class="tabular-nums">{{ faNum(s.users.active_24h) }}</b> کاربر در ۲۴ ساعت گذشته فعال بوده و <b class="tabular-nums">{{ faNum(s.calculations.last_24h) }}</b> محاسبه انجام شده است.</template>
            <template v-else>در حال بارگذاری آمار…</template>
          </p>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button class="hero-btn" @click="$emit('go', 'users')"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0z" /></svg>کاربران</button>
          <button class="hero-btn" @click="$emit('go', 'announcements')">اعلان جدید</button>
          <button class="hero-btn" @click="$emit('go', 'settings')">حالت تعمیر</button>
        </div>
      </div>
    </section>

    <!-- بازهٔ زمانی -->
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div class="inline-flex rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-1 shadow-sm">
        <button v-for="r in ranges" :key="r" class="px-3.5 py-1.5 text-xs rounded-lg transition"
          :class="days === r ? 'bg-primary-600 text-white shadow' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'" @click="days = r">
          {{ faNum(r) }} روز
        </button>
      </div>
      <button class="ad-btn ad-btn-sm" :disabled="loading" @click="load">
        <svg class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>
        به‌روزرسانی
      </button>
    </div>

    <div v-if="loading && !s" class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3"><div v-for="i in 6" :key="i" class="ad-card h-32 animate-pulse"></div></div>

    <template v-if="s">
      <!-- شاخص‌ها -->
      <div class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
        <AdminStatCard title="کل کاربران" :value="faNum(s.users.total)" :spark="s.series.total_users" :trend="null" :sub="`${faNum(s.users.new_7d)} جدید در ۷ روز`" color="#2563eb" :icon="I.users" />
        <AdminStatCard title="کاربران جدید" :value="faNum(p.current.new_users)" :trend="p.trend.new_users" :spark="s.series.new_users" :sub="`در ${faNum(days)} روز`" color="#8b5cf6" :icon="I.userPlus" />
        <AdminStatCard title="کاربران فعال" :value="faNum(p.current.active_users)" :trend="p.trend.active_users" :spark="s.series.active_users" :sub="`دست‌کم یک محاسبه`" color="#0ea5e9" :icon="I.bolt" />
        <AdminStatCard title="محاسبه‌ها" :value="faNum(p.current.calculations)" :trend="p.trend.calculations" :spark="s.series.calculations" :sub="`${faNum(s.calculations.total)} در کل`" color="#10b981" :icon="I.calc" />
        <AdminStatCard title="نرخ موفقیت" :value="p.current.success_rate === null ? '—' : faNum(p.current.success_rate, 1)" :unit="p.current.success_rate === null ? '' : '٪'" :trend="rateTrend" :sub="`${faNum(p.current.failed)} محاسبهٔ ناموفق`" color="#f59e0b" :icon="I.check" />
        <AdminStatCard title="میانگین زمان محاسبه" :value="p.current.avg_time_ms === null ? '—' : faNum(Math.round(p.current.avg_time_ms))" :unit="p.current.avg_time_ms === null ? '' : 'ms'" :trend="null" :sub="p.current.avg_cost ? `میانگین هزینه ${faShort(Math.round(p.current.avg_cost))} تومان` : ''" color="#f43f5e" :icon="I.clock" />
      </div>

      <!-- نمودار اصلی -->
      <section class="ad-card p-4 sm:p-5">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div><h3 class="ad-title">فعالیت در {{ faNum(days) }} روز گذشته</h3><p class="text-[11px] text-gray-400">روی نمودار حرکت کنید یا برای پنهان‌کردن یک خط، روی راهنما بزنید</p></div>
        </div>
        <AdminAreaChart :labels="dayLabels" :series="mainSeries" :height="270" />
      </section>

      <!-- ترکیب‌ها -->
      <div class="grid lg:grid-cols-3 gap-3">
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-4">نقش کاربران</h3>
          <AdminDonut :segments="roleSegs" center-label="کاربر" /></section>
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-4">وضعیت حساب‌ها</h3>
          <AdminDonut :segments="statusSegs" center-label="حساب" /></section>
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-4">محتوای سیستم</h3>
          <div class="grid grid-cols-2 gap-2.5">
            <div v-for="c in contentCards" :key="c.l" class="rounded-xl bg-gray-50 dark:bg-gray-900/40 p-3">
              <p class="text-lg font-extrabold tabular-nums text-gray-900 dark:text-white">{{ faNum(c.v) }}</p>
              <p class="text-[11px] text-gray-500 dark:text-gray-400">{{ c.l }}</p>
            </div>
          </div>
        </section>
      </div>

      <!-- الگوی استفاده -->
      <div class="grid lg:grid-cols-5 gap-3">
        <section class="ad-card p-4 sm:p-5 lg:col-span-3">
          <h3 class="ad-title">ساعت‌های شلوغی (به وقت تهران)</h3>
          <p class="text-[11px] text-gray-400 mb-3">هر خانه یک ساعت شبانه‌روز؛ پررنگ‌تر = محاسبهٔ بیشتر</p>
          <AdminHeatStrip :items="hourItems" color="#2563eb" />
        </section>
        <section class="ad-card p-4 sm:p-5 lg:col-span-2">
          <h3 class="ad-title mb-3">محاسبه‌ها بر حسب روز هفته</h3>
          <AdminColumns :items="s.by_weekday" color="#8b5cf6" />
        </section>
      </div>

      <!-- برترین‌ها -->
      <div class="grid lg:grid-cols-3 gap-3">
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-3">فعال‌ترین کاربران</h3>
          <AdminBars :items="topUsers" color="#2563eb" unit="محاسبه" clickable @select="(it) => it.id && $emit('open-user', it.id)" /></section>
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-3">پرکاربردترین کودها</h3>
          <AdminBars :items="s.top_fertilizers" color="#10b981" unit="بار" /></section>
        <section class="ad-card p-4 sm:p-5"><h3 class="ad-title mb-3">گیاهان پرتکرار در گزارش‌ها</h3>
          <AdminBars :items="s.top_plants" color="#f59e0b" unit="گزارش" /></section>
      </div>

      <!-- فهرست‌ها -->
      <div class="grid lg:grid-cols-2 gap-3">
        <section class="ad-card p-4 sm:p-5">
          <div class="flex items-center justify-between mb-3"><h3 class="ad-title">تازه‌ترین ثبت‌نام‌ها</h3><button class="text-xs text-primary-600 hover:underline" @click="$emit('go', 'users')">همهٔ کاربران</button></div>
          <ul class="divide-y divide-gray-100 dark:divide-gray-700/60">
            <li v-for="u in s.recent_users" :key="u.id" class="py-2 flex items-center gap-3">
              <span class="ad-avatar" :style="avatarStyle(u.name)">{{ initials(u.name) }}</span>
              <button class="flex-1 min-w-0 text-right hover:text-primary-600" @click="$emit('open-user', u.id)">
                <p class="text-sm font-medium truncate text-gray-900 dark:text-white">{{ u.name }}</p>
                <p class="text-[11px] text-gray-400 tabular-nums" dir="ltr" style="text-align:right">{{ u.phone }}</p>
              </button>
              <AdminBadges :role="u.role" />
              <span class="text-[11px] text-gray-400 flex-shrink-0">{{ faDate(u.created_at, false) }}</span>
            </li>
          </ul>
        </section>
        <section class="ad-card p-4 sm:p-5">
          <div class="flex items-center justify-between mb-3"><h3 class="ad-title">رویدادهای امنیتی اخیر</h3><button class="text-xs text-primary-600 hover:underline" @click="$emit('go', 'logs')">همهٔ لاگ‌ها</button></div>
          <div v-if="!s.recent_security.length" class="py-8 text-center text-sm text-gray-400"><span class="text-2xl block mb-1">🛡️</span>رویداد هشداری ثبت نشده است.</div>
          <ul class="divide-y divide-gray-100 dark:divide-gray-700/60">
            <li v-for="l in s.recent_security" :key="l.id" class="py-2.5 flex items-center justify-between gap-2">
              <span class="flex items-center gap-2 min-w-0"><i class="w-2 h-2 rounded-full flex-shrink-0" :class="l.severity === 'WARNING' ? 'bg-amber-500' : 'bg-rose-500'"></i><span class="text-xs font-medium truncate" dir="ltr">{{ l.event_type }}</span></span>
              <span class="text-[11px] text-gray-400 tabular-nums flex-shrink-0" dir="ltr">{{ l.ip || '—' }} · {{ faDate(l.created_at) }}</span>
            </li>
          </ul>
        </section>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import AdminAreaChart from './charts/AdminAreaChart.vue';
import AdminDonut from './charts/AdminDonut.vue';
import AdminBars from './charts/AdminBars.vue';
import AdminHeatStrip from './charts/AdminHeatStrip.vue';
import AdminColumns from './charts/AdminColumns.vue';
import AdminStatCard from './AdminStatCard.vue';
import AdminBadges from './AdminBadges.vue';
import { adminApi, apiError, faDate } from '@/services/adminApi';
import { faDay, faNum, faShort, PALETTE } from './charts/chartUtils';
import { avatarStyle, initials } from './adminUi';
import { toast } from './adminUi';

const props = defineProps<{ name?: string }>();
defineEmits<{ (e: 'open-user', id: number): void; (e: 'go', tab: string): void }>();

const ranges = [7, 14, 30, 90];
const days = ref(14);
const s = ref<any>(null);
const loading = ref(false);

async function load() {
  loading.value = true;
  try { s.value = await adminApi.stats(days.value); }
  catch (e) { toast(apiError(e, 'دریافت آمار ناموفق بود'), 'error'); }
  finally { loading.value = false; }
}
onMounted(load);
watch(days, load);

const p = computed(() => s.value.period);
const rateTrend = computed(() => {
  const a = p.value.current.success_rate, b = p.value.previous.success_rate;
  return a === null || b === null ? null : a - b;
});
const dayLabels = computed(() => s.value.series.days.map((d: string) => faDay(d)));
const mainSeries = computed(() => [
  { key: 'calc', name: 'محاسبه', color: PALETTE.primary, values: s.value.series.calculations },
  { key: 'users', name: 'کاربر فعال', color: PALETTE.emerald, values: s.value.series.active_users },
  { key: 'new', name: 'ثبت‌نام جدید', color: PALETTE.purple, values: s.value.series.new_users, area: false },
  { key: 'fail', name: 'ناموفق', color: PALETTE.rose, values: s.value.series.failed, area: false, dashed: true }
]);
const roleSegs = computed(() => [
  { label: 'معمولی', value: s.value.users.by_role.user || 0, color: PALETTE.gray },
  { label: 'پلاس', value: s.value.users.by_role.plus || 0, color: PALETTE.amber },
  { label: 'مدیر', value: s.value.users.by_role.admin || 0, color: PALETTE.purple }
]);
const statusSegs = computed(() => [
  { label: 'فعال', value: s.value.users.by_status.active || 0, color: PALETTE.emerald },
  { label: 'مسدود', value: s.value.users.by_status.blocked || 0, color: PALETTE.orange },
  { label: 'بن‌شده', value: s.value.users.by_status.banned || 0, color: PALETTE.rose }
]);
const contentCards = computed(() => [
  { l: 'گزارش‌ها', v: s.value.content.reports }, { l: 'کودهای سیستمی', v: s.value.content.system_fertilizers },
  { l: 'کودهای کاربران', v: s.value.content.user_fertilizers }, { l: 'تنظیم‌های pH', v: s.value.content.ph_adjustments }
]);
const topUsers = computed(() => (s.value.top_users || []).map((u: any) => ({ id: u.id, label: u.name, count: u.count })));
const hourItems = computed(() => s.value.by_hour.map((count: number, h: number) => ({ label: `${faNum(h)}:۰۰`, count })));

const today = new Date().toLocaleDateString('fa-IR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const greeting = (() => { const h = new Date().getHours(); return h < 5 ? 'شب بخیر' : h < 12 ? 'صبح بخیر' : h < 17 ? 'ظهر بخیر' : h < 21 ? 'عصر بخیر' : 'شب بخیر'; })();
const name = computed(() => props.name?.split(' ')[0] || 'مدیر');

const I = {
  users: 'M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0z',
  userPlus: 'M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM3 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 019.374 21c-2.331 0-4.512-.645-6.374-1.766z',
  bolt: 'M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z',
  calc: 'M15.75 15.75V18m-7.5-6.75h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V13.5zm0 2.25h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V18zm2.498-6.75h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V13.5zm0 2.25h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V18zm2.504-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zm0 2.25h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V18zm2.498-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zM8.25 6h7.5v2.25h-7.5V6zM12 2.25c-1.892 0-3.758.11-5.593.322C5.307 2.7 4.5 3.65 4.5 4.757V19.5a2.25 2.25 0 002.25 2.25h10.5a2.25 2.25 0 002.25-2.25V4.757c0-1.108-.806-2.057-1.907-2.185A48.507 48.507 0 0012 2.25z',
  check: 'M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  clock: 'M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z'
};
</script>
