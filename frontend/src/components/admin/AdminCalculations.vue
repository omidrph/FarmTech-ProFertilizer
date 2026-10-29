<template>
  <div class="space-y-3">
    <!-- خلاصهٔ ۷ روز اخیر -->
    <div v-if="sum" class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="c in tiles" :key="c.l" class="ad-card ad-hover p-4">
        <p class="text-[11px] text-gray-500 dark:text-gray-400">{{ c.l }}</p>
        <p class="mt-1 text-2xl font-extrabold tabular-nums" :class="c.cls || 'text-gray-900 dark:text-white'">{{ c.v }}</p>
        <div v-if="c.bar !== undefined" class="mt-2 h-1.5 rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden"><div class="h-full rounded-full bg-emerald-500 transition-all duration-700" :style="{ width: c.bar + '%' }"></div></div>
      </div>
    </div>

    <div class="ad-card p-3 flex flex-wrap items-end gap-2.5">
      <div class="w-44"><label class="ad-label">نتیجه</label>
        <select v-model="success" class="ad-input"><option value="">همه</option><option value="true">موفق</option><option value="false">ناموفق</option></select></div>
      <label class="flex items-center gap-2 text-sm pb-2"><input type="checkbox" v-model="warnOnly" /> فقط دارای هشدار</label>
      <div class="w-36"><label class="ad-label">شناسهٔ کاربر</label><input v-model="userId" class="ad-input" inputmode="numeric" dir="ltr" /></div>
    </div>

    <div class="ad-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[48rem]">
          <thead><tr><th class="ad-th">زمان</th><th class="ad-th">کاربر</th><th class="ad-th">نتیجه</th><th class="ad-th">کودها</th><th class="ad-th">هزینه</th><th class="ad-th">خطای باقیمانده</th><th class="ad-th">هشدار</th><th class="ad-th">مدت</th><th class="ad-th"></th></tr></thead>
          <tbody>
            <tr v-if="!rows.length"><td colspan="9" class="ad-td text-center text-gray-400 py-8">{{ loading ? 'در حال بارگذاری…' : 'موردی پیدا نشد.' }}</td></tr>
            <tr v-for="o in rows" :key="o.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30">
              <td class="ad-td text-xs text-gray-500">{{ faDate(o.created_at) }}</td>
              <td class="ad-td">{{ o.user_name }}</td>
              <td class="ad-td"><span class="ad-chip" :class="o.is_successful ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'">{{ o.is_successful ? 'موفق' : 'ناموفق' }}</span></td>
              <td class="ad-td tabular-nums">{{ faN(o.fertilizers_count) }}</td>
              <td class="ad-td tabular-nums">{{ o.cost_total ? faN(Math.round(o.cost_total)) : '—' }}</td>
              <td class="ad-td tabular-nums text-xs">{{ o.residual_error != null ? o.residual_error.toFixed(2) : '—' }}</td>
              <td class="ad-td tabular-nums">{{ o.warnings_count ? faN(o.warnings_count) : '—' }}</td>
              <td class="ad-td tabular-nums text-xs">{{ o.convergence_time_ms != null ? Math.round(o.convergence_time_ms) + ' ms' : '—' }}</td>
              <td class="ad-td"><button class="ad-btn ad-btn-sm" @click="show(o.id)">جزئیات</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <AdminPagination :page="page" :pages="pages" :total="total" @change="(p) => { page = p; load(); }" />
    </div>

    <AppModal :open="!!detail" :title="`محاسبه #${detail?.id}`" :subtitle="detail ? `${detail.user.name} · ${faDate(detail.created_at)}` : ''" size="xl" @close="detail = null">
      <div v-if="detail" class="space-y-3 text-sm">
        <p v-if="detail.error_message" class="rounded-lg bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-300 p-2.5">{{ detail.error_message }}</p>
        <div v-if="detail.warnings?.length"><h4 class="font-bold mb-1">هشدارها</h4><ul class="list-disc pr-5 text-xs space-y-0.5"><li v-for="(w, i) in detail.warnings" :key="i">{{ w }}</li></ul></div>
        <div class="grid sm:grid-cols-2 gap-3">
          <div v-for="b in blocks" :key="b.t"><h4 class="font-bold mb-1">{{ b.t }}</h4><pre class="text-[11px] leading-5 bg-gray-50 dark:bg-gray-900/50 rounded-lg p-2.5 overflow-auto max-h-56" dir="ltr">{{ pretty(b.v) }}</pre></div>
        </div>
      </div>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import AppModal from '@/components/common/AppModal.vue';
import AdminPagination from './AdminPagination.vue';
import { adminApi, apiError, faDate, faN } from '@/services/adminApi';
import { faNum } from './charts/chartUtils';
import { toast } from './adminUi';

const rows = ref<any[]>([]);
const total = ref(0), pages = ref(1), page = ref(1), loading = ref(false);
const success = ref(''), warnOnly = ref(false), userId = ref('');
const detail = ref<any | null>(null);

async function load() {
  loading.value = true;
  try {
    const r = await adminApi.calculations({ success: success.value, has_warnings: warnOnly.value ? true : '', user_id: userId.value.trim(), page: page.value });
    rows.value = r.items; total.value = r.total; pages.value = r.pages;
  } catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
watch([success, warnOnly, userId], () => { page.value = 1; load(); });
const sum = ref<any>(null);
const tiles = computed(() => !sum.value ? [] : [
  { l: 'محاسبه در ۷ روز', v: faN(sum.value.period.current.calculations) },
  { l: 'نرخ موفقیت', v: sum.value.period.current.success_rate === null ? '—' : faNum(sum.value.period.current.success_rate, 1) + '٪', bar: sum.value.period.current.success_rate ?? 0 },
  { l: 'ناموفق', v: faN(sum.value.period.current.failed), cls: sum.value.period.current.failed ? 'text-rose-600 dark:text-rose-400' : undefined },
  { l: 'میانگین زمان', v: sum.value.period.current.avg_time_ms === null ? '—' : faN(Math.round(sum.value.period.current.avg_time_ms)) + ' ms' }
]);
onMounted(async () => { load(); try { sum.value = await adminApi.stats(7); } catch { /* خلاصه اختیاری است */ } });

async function show(id: number) { try { detail.value = await adminApi.calculation(id); } catch (e) { toast(apiError(e), 'error'); } }
const pretty = (v: any) => JSON.stringify(v ?? null, null, 2);
const blocks = computed(() => !detail.value ? [] : [
  { t: 'اهداف', v: detail.value.target_values }, { t: 'آب', v: detail.value.water_values },
  { t: 'مقادیر کود (گرم)', v: detail.value.weights }, { t: 'غلظت نهایی (ppm)', v: detail.value.final_concentrations },
  { t: 'گزینه‌ها', v: detail.value.options }, { t: 'تعادل یونی', v: detail.value.ion_balance }
]);
</script>
