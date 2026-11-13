// frontend/src/composables/usePermissions.ts
// دسترسی‌های نقش کاربر (از پنل مدیریت) + وضعیت «ورود به‌جای کاربر»
import { reactive, ref } from 'vue';
import axios from 'axios';

const API = import.meta.env.VITE_API_URL || '/api/v1';
const perms = reactive<Record<string, boolean>>({});
const loaded = ref(false);
const impersonating = ref(false);
const role = ref<string>('user');

// تا قبل از رسیدن پاسخ سرور، امکانات حساس بسته می‌مانند
const RESTRICTED_BY_DEFAULT = ['interpretation', 'manual_fertilizer', 'advanced_fertilizer'];

async function load(): Promise<void> {
  try {
    const token = localStorage.getItem('access_token');
    const r = await axios.get(`${API}/system/context`, { timeout: 8000, withCredentials: true, headers: token ? { Authorization: `Bearer ${token}` } : {} });
    Object.keys(perms).forEach((k) => delete perms[k]);
    Object.assign(perms, r.data.permissions || {});
    impersonating.value = !!r.data.impersonating;
    role.value = r.data.role || 'user';
    loaded.value = true;
  } catch { /* بی‌صدا: با پیش‌فرض‌ها ادامه می‌دهیم */ }
}

async function stopImpersonation(): Promise<boolean> {
  try {
    await axios.post(`${API}/system/stop-impersonation`, {}, { withCredentials: true });
    return true;
  } catch { return false; }
}

export function usePermissions() {
  const can = (key: string): boolean => (loaded.value ? perms[key] === true : !RESTRICTED_BY_DEFAULT.includes(key));
  return { can, load, loaded, impersonating, role, stopImpersonation };
}
