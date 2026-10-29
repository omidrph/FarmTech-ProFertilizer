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
