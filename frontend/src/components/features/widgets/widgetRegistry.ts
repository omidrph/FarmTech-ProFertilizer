// frontend/src/components/features/widgets/widgetRegistry.ts
// ============================================================
// فهرست ابزارک‌ها
// ------------------------------------------------------------
// برای افزودن یک ابزارک جدید فقط ۲ کار لازم است:
//   ۱) کامپوننت آن را در همین پوشه (widgets/) بسازید؛ مثلاً YourWidget.vue
//      (فقط «بدنه‌ی» ابزارک؛ عنوان و دکمه‌ی بازگشت را صفحه‌ی ابزارک‌ها می‌سازد)
//   ۲) یک مورد به آرایه‌ی زیر اضافه کنید و status را 'ready' بگذارید:
//        component: () => import('./YourWidget.vue')
// تا وقتی component نداشته باشد یا status برابر 'soon' باشد، کارت با برچسب «به‌زودی» و غیرفعال نمایش داده می‌شود.
//
// 🆕 «ماشین‌حساب PH» از اینجا خارج شده و اکنون یک تب مستقل در سطح
// اصلی برنامه است (بین «پایگاه‌داده کود» و «ابزارک‌ها»؛ به
// PhCalculatorTab.vue در components/features/ مراجعه کنید).
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

export const widgetRegistry: WidgetDefinition[] = [];




