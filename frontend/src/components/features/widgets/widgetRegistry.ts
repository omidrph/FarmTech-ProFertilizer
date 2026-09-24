// frontend/src/components/features/widgets/widgetRegistry.ts
// ============================================================
// فهرست ابزارک‌ها
// ------------------------------------------------------------
// برای افزودن یک ابزارک جدید فقط ۲ کار لازم است:
//   ۱) کامپوننت آن را در همین پوشه (widgets/) بسازید؛ مثلاً YourWidget.vue
//      (فقط «بدنه‌ی» ابزارک؛ عنوان و دکمه‌ی بازگشت را صفحه‌ی ابزارک‌ها می‌سازد)
//      مثال آماده: PhCalculatorWidget.vue
//   ۲) یک مورد به آرایه‌ی زیر اضافه کنید و status را 'ready' بگذارید:
//        component: () => import('./YourWidget.vue')
// تا وقتی component نداشته باشد یا status برابر 'soon' باشد، کارت با برچسب «به‌زودی» و غیرفعال نمایش داده می‌شود.
// ============================================================
import type { Component } from 'vue';

export interface WidgetDefinition {
  /** شناسه‌ی یکتا (انگلیسی و بدون فاصله) */
  id: string;
  title: string;
  description: string;
  /** مسیر (d) یک آیکون outline با viewBox 24×24 */
  iconPath: string;
  status: 'ready' | 'soon';
  /** بارگذاری تنبل کامپوننت ابزارک؛ فقط وقتی کاربر آن را باز کند لود می‌شود */
  component?: () => Promise<{ default: Component }>;
}

export const widgetRegistry: WidgetDefinition[] = [
  {
    id: 'ph-calculator',
    title: 'ماشین حساب PH',
    description: 'محاسبه مقدار اسید یا باز لازم برای رساندن pH آب یا محلول به مقدار هدف؛ با مدل تئوریک یا تیتراسیون واقعی',
    iconPath:
      'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    status: 'ready',
    component: () => import('./PhCalculatorWidget.vue')
  }
];
