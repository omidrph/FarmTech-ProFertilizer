// وضعیت سراسری توست و دیالوگ تأیید پنل مدیریت (در AdminView نمایش داده می‌شوند)
import { reactive } from 'vue';

export const toasts = reactive<{ id: number; msg: string; type: 'success' | 'error' }[]>([]);
let seq = 0;
export function toast(msg: string, type: 'success' | 'error' = 'success') {
  const id = ++seq;
  toasts.push({ id, msg, type });
  setTimeout(() => {
    const i = toasts.findIndex((t) => t.id === id);
    if (i >= 0) toasts.splice(i, 1);
  }, 3800);
}

export const confirmState = reactive({
  open: false, title: '', message: '', confirmText: 'تأیید', danger: false,
  resolve: null as null | ((v: boolean) => void)
});
export function confirmDialog(o: { title: string; message?: string; confirmText?: string; danger?: boolean }): Promise<boolean> {
  return new Promise((resolve) => {
    Object.assign(confirmState, { open: true, title: o.title, message: o.message || '', confirmText: o.confirmText || 'تأیید', danger: !!o.danger, resolve });
  });
}
export function answerConfirm(v: boolean) {
  confirmState.open = false;
  confirmState.resolve?.(v);
  confirmState.resolve = null;
}

// ===== آواتار حروف اولیه با رنگ ثابت برای هر نام =====
const AVATAR_COLORS = ['#2563eb', '#8b5cf6', '#0ea5e9', '#10b981', '#f59e0b', '#f43f5e', '#14b8a6', '#6366f1'];
export function initials(name: string): string {
  const parts = (name || '').trim().split(/\s+/);
  return ((parts[0]?.charAt(0) || '') + (parts[1]?.charAt(0) || '')).trim() || '؟';
}
export function avatarStyle(name: string): Record<string, string> {
  let h = 0;
  for (const ch of name || '') h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const c = AVATAR_COLORS[h % AVATAR_COLORS.length];
  return { background: c + '22', color: c };
}
