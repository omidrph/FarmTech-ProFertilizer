<!-- frontend/src/components/admin/AdminPermissions.vue -->
<!-- تعیین دسترسی هر نوع کاربر (معمولی / پلاس) به بخش‌های برنامه -->
<template>
  <div class="space-y-3">
    <div class="ad-card p-4 flex flex-wrap items-center justify-between gap-3">
      <div>
        <h3 class="ad-title">دسترسی‌های هر نوع حساب</h3>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-6">برای هر امکان مشخص کنید کدام نوع کاربر به آن دسترسی دارد. مدیران همیشه به همه‌چیز دسترسی دارند. تغییرات با ورود بعدی/بازخوانی صفحهٔ کاربران اعمال می‌شود.</p>
      </div>
      <div class="flex gap-2">
        <button class="ad-btn" :disabled="saving" @click="restoreDefaults">بازگشت به پیش‌فرض</button>
        <button class="ad-btn-primary" :disabled="saving || !dirty" @click="save">{{ saving ? 'در حال ذخیره…' : 'ذخیرهٔ تغییرات' }}</button>
      </div>
    </div>

    <div class="ad-card overflow-hidden">
      <div v-if="loading" class="p-10 text-center text-sm text-gray-400">در حال بارگذاری…</div>
      <table v-else class="w-full">
        <thead><tr><th class="ad-th">امکان</th><th class="ad-th text-center w-32">کاربر معمولی</th><th class="ad-th text-center w-32">کاربر پلاس</th></tr></thead>
        <tbody>
          <tr v-for="p in defs" :key="p.key" class="hover:bg-gray-50 dark:hover:bg-gray-700/30">
            <td class="ad-td"><p class="font-semibold text-gray-900 dark:text-white">{{ p.label }}</p><p class="text-[11px] text-gray-500">{{ p.hint }}</p></td>
            <td v-for="r in ROLES" :key="r" class="ad-td text-center"><AdminSwitch v-model="matrix[r][p.key]" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import AdminSwitch from './AdminSwitch.vue';
import { adminApi, apiError } from '@/services/adminApi';
import { toast } from './adminUi';

const ROLES = ['user', 'plus'] as const;
const defs = ref<{ key: string; label: string; hint: string }[]>([]);
const matrix = ref<Record<string, Record<string, boolean>>>({ user: {}, plus: {} });
const defaults = ref<Record<string, Record<string, boolean>>>({ user: {}, plus: {} });
const original = ref('');
const loading = ref(false), saving = ref(false);
const dirty = computed(() => JSON.stringify(matrix.value) !== original.value);

async function load() {
  loading.value = true;
  try {
    const r = await adminApi.permissions();
    defs.value = r.definitions; matrix.value = r.matrix; defaults.value = r.defaults;
    original.value = JSON.stringify(r.matrix);
  } catch (e) { toast(apiError(e), 'error'); } finally { loading.value = false; }
}
async function save() {
  saving.value = true;
  try { const r = await adminApi.savePermissions(matrix.value); matrix.value = r.matrix; original.value = JSON.stringify(r.matrix); toast('دسترسی‌ها ذخیره شد'); }
  catch (e) { toast(apiError(e), 'error'); } finally { saving.value = false; }
}
const restoreDefaults = () => { matrix.value = JSON.parse(JSON.stringify(defaults.value)); };
onMounted(load);
</script>
