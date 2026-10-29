<template>
  <div class="space-y-4">
    <div v-if="loading" class="ad-card p-8 text-center text-sm text-gray-500">در حال بارگذاری…</div>
    <template v-else-if="s">
      <!-- کارت‌های شاخص -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div v-for="c in cards" :key="c.label" class="ad-card p-4">
          <p class="text-[11px] text-gray-500 dark:text-gray-400">{{ c.label }}</p>
          <p class="mt-1 text-2xl font-bold tabular-nums" :class="c.cls || 'text-gray-900 dark:text-white'">{{ faN(c.value) }}</p>
          <p v-if="c.sub" class="mt-0.5 text-[11px] text-gray-400">{{ c.sub }}</p>
        </div>
      </div>

      <!-- نمودارها -->
      <div class="grid lg:grid-cols-2 gap-3">
        <div class="ad-card p-4">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">محاسبه‌ها در ۱۴ روز گذشته</h3>
          <div class="flex gap-1 h-28">
            <div v-for="(v, i) in s.series.calculations" :key="i" class="flex-1 flex flex-col justify-end gap-0.5" :title="`${faDay(i)}: ${v} محاسبه، ${s.series.failed[i]} ناموفق`">
              <div class="w-full rounded-t bg-primary-500/80" :style="{ height: bar(v, maxCalc) }"></div>
              <div v-if="s.series.failed[i]" class="w-full rounded-t bg-rose-500" :style="{ height: bar(s.series.failed[i], maxCalc) }"></div>
            </div>
          </div>
          <div class="mt-1 flex justify-between text-[10px] text-gray-400"><span>{{ faDay(0) }}</span><span>{{ faDay(13) }}</span></div>
        </div>
        <div class="ad-card p-4">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">کاربران جدید در ۱۴ روز گذشته</h3>
          <div class="flex gap-1 h-28">
            <div v-for="(v, i) in s.series.new_users" :key="i" class="flex-1 flex flex-col justify-end" :title="`${faDay(i)}: ${v} کاربر`">
              <div class="w-full rounded-t bg-purple-500/80" :style="{ height: bar(v, maxUsers) }"></div>
            </div>
          </div>
          <div class="mt-1 flex justify-between text-[10px] text-gray-400"><span>{{ faDay(0) }}</span><span>{{ faDay(13) }}</span></div>
        </div>
      </div>

      <div class="grid lg:grid-cols-3 gap-3">
        <!-- نقش‌ها و وضعیت‌ها -->
        <div class="ad-card p-4">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">ترکیب کاربران</h3>
          <div class="space-y-2 text-sm">
            <div v-for="r in roleRows" :key="r.k" class="flex items-center justify-between"><span class="text-gray-600 dark:text-gray-300">{{ r.label }}</span><b class="tabular-nums">{{ faN(r.v) }}</b></div>
            <hr class="border-gray-100 dark:border-gray-700" />
            <div v-for="r in statusRows" :key="r.k" class="flex items-center justify-between"><span class="text-gray-600 dark:text-gray-300">{{ r.label }}</span><b class="tabular-nums">{{ faN(r.v) }}</b></div>
          </div>
        </div>
        <!-- تازه‌ترین کاربران -->
        <div class="ad-card p-4">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">تازه‌ترین ثبت‌نام‌ها</h3>
          <ul class="space-y-2">
            <li v-for="u in s.recent_users" :key="u.id" class="flex items-center justify-between gap-2 text-sm">
              <button class="truncate text-right hover:text-primary-600" @click="$emit('open-user', u.id)">{{ u.name }}</button>
              <span class="text-[11px] text-gray-400 flex-shrink-0">{{ faDate(u.created_at, false) }}</span>
            </li>
          </ul>
        </div>
        <!-- رویدادهای امنیتی -->
        <div class="ad-card p-4">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">رویدادهای امنیتی اخیر</h3>
          <p v-if="!s.recent_security.length" class="text-sm text-gray-400">رویداد هشداری ثبت نشده است.</p>
          <ul class="space-y-2">
            <li v-for="l in s.recent_security" :key="l.id" class="flex items-center justify-between gap-2 text-xs">
              <span class="ad-chip" :class="l.severity === 'WARNING' ? 'bg-amber-100 text-amber-700' : 'bg-rose-100 text-rose-700'">{{ l.event_type }}</span>
              <span class="text-gray-400 tabular-nums" dir="ltr">{{ l.ip || '—' }}</span>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { adminApi, apiError, faDate, faN } from '@/services/adminApi';
import { toast } from './adminUi';

defineEmits<{ (e: 'open-user', id: number): void }>();
const s = ref<any>(null);
const loading = ref(true);

onMounted(async () => {
  try { s.value = await adminApi.stats(); } catch (e) { toast(apiError(e, 'دریافت آمار ناموفق بود'), 'error'); }
  finally { loading.value = false; }
});

const cards = computed(() => !s.value ? [] : [
  { label: 'کل کاربران', value: s.value.users.total, sub: `${faN(s.value.users.new_7d)} جدید در ۷ روز` },
  { label: 'فعال در ۲۴ ساعت', value: s.value.users.active_24h, sub: `${faN(s.value.users.active_7d)} نفر در ۷ روز`, cls: 'text-emerald-600 dark:text-emerald-400' },
  { label: 'محاسبه‌ها (۷ روز)', value: s.value.calculations.last_7d, sub: `${faN(s.value.calculations.last_24h)} در ۲۴ ساعت` },
  { label: 'محاسبهٔ ناموفق (۷ روز)', value: s.value.calculations.failed_7d, cls: s.value.calculations.failed_7d ? 'text-rose-600 dark:text-rose-400' : undefined },
  { label: 'گزارش‌ها', value: s.value.content.reports },
  { label: 'کودهای سیستمی', value: s.value.content.system_fertilizers },
  { label: 'کودهای کاربران', value: s.value.content.user_fertilizers },
  { label: 'تنظیم‌های pH', value: s.value.content.ph_adjustments }
]);
const roleRows = computed(() => [
  { k: 'user', label: 'کاربر معمولی', v: s.value.users.by_role.user || 0 },
  { k: 'plus', label: 'کاربر پلاس', v: s.value.users.by_role.plus || 0 },
  { k: 'admin', label: 'مدیر', v: s.value.users.by_role.admin || 0 }
]);
const statusRows = computed(() => [
  { k: 'active', label: 'فعال', v: s.value.users.by_status.active || 0 },
  { k: 'blocked', label: 'مسدود', v: s.value.users.by_status.blocked || 0 },
  { k: 'banned', label: 'بن‌شده', v: s.value.users.by_status.banned || 0 }
]);
const maxCalc = computed(() => Math.max(1, ...(s.value?.series.calculations || [0])));
const maxUsers = computed(() => Math.max(1, ...(s.value?.series.new_users || [0])));
const bar = (v: number, max: number) => (v ? Math.max((v / max) * 100, 4) : 0) + '%';
const faDay = (i: number) => faDate(s.value.series.days[i] + 'T12:00:00', false);
</script>
