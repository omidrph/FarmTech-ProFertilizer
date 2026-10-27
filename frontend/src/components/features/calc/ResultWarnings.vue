
<!-- frontend/src/components/features/calc/ResultWarnings.vue -->
<!--
  ============================================================
  بازطراحی کامل بخش هشدارها (به‌جای دامپ کردن رشته‌های خام بک‌اند)
  ------------------------------------------------------------
  چرا این بازطراحی لازم بود:
    نسخه قبلی هرچه از سرور می‌آمد را بدون فیلتر و بدون اولویت‌بندی
    زیر هم می‌ریخت: پیام‌های تکراری با بخش عناصر/تعادل یونی، پیشنهادهای
    کلی و بی‌اثر («دوباره بهینه‌سازی را اجرا کنید»)، و هیچ اقدام
    مشخصی به کاربر پیشنهاد نمی‌شد.
  ------------------------------------------------------------
  منطق جدید:
    ۱) خطر رسوب شیمیایی → همیشه با شدت «خطر» و برجسته (این تنها موردی
       است که واقعاً ایمنی/کیفیت محلول را تهدید می‌کند)
    ۲) کیفیت ترکیب (همگرا نشدن، دقت پایین، کود بلااستفاده) → یک کارت
       واحد با توضیح روشن + دکمه «بازگشت به انتخاب کود»
    ۳) هر پیام دیگری که از این دو دسته خارج باشد → فهرست «سایر نکات»
       (فقط اگر واقعاً چیزی برای گفتن باقی مانده باشد)
    ۴) اگر هیچ‌کدام نبود → پیام اطمینان‌بخش «ترکیب مشکلی ندارد»
  ============================================================
-->
<template>
  <div class="space-y-3">

    <!-- ============================================================ -->
    <!-- ۱) سیستم هشدار ترکیبات رسوب‌زا (ساختاریافته: استوک / محلول نهایی / آب) -->
    <!-- ============================================================ -->
    <div
      v-for="item in alertItems"
      :key="item.id"
      class="rounded-lg border p-3"
      :class="SEV[item.severity].box"
    >
      <div class="flex items-start gap-2.5">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" :class="SEV[item.severity].icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m0 3.75h.008v.008H12v-.008zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-2 flex-wrap">
            <p class="text-sm font-semibold" :class="SEV[item.severity].title">{{ item.title }}</p>
            <span class="text-[10px] px-1.5 py-0.5 rounded-full" :class="SEV[item.severity].chip">{{ SCOPE[item.scope] }}</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded-full" :class="SEV[item.severity].chip">{{ SEV[item.severity].label }}</span>
          </div>
          <p class="text-xs mt-1 leading-5" :class="SEV[item.severity].text">{{ item.detail }}</p>
          <p class="text-xs mt-1 leading-5 font-medium" :class="SEV[item.severity].text">راه‌حل: {{ item.solution }}</p>
        </div>
      </div>
    </div>

    <!-- سازگاری با نتیجه‌های قدیمی که هنوز هشدار ساختاریافته ندارند -->
    <div
      v-for="item in legacyPrecipitation"
      :key="'precip-' + item.compound"
      class="flex items-start gap-2.5 rounded-lg border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20 p-3"
    >
      <svg class="w-5 h-5 text-rose-600 dark:text-rose-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m0 3.75h.008v.008H12v-.008zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div class="min-w-0">
        <p class="text-sm font-semibold text-rose-700 dark:text-rose-400">خطر رسوب: {{ item.compound }}</p>
        <p class="text-xs text-rose-600 dark:text-rose-300 mt-0.5">کودهای مربوطه را در سطل‌های جدا حل کنید و پیش از رقیق‌سازی مخلوط نکنید.</p>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- ۲) کیفیت ترکیب -->
    <!-- ============================================================ -->
    <div
      v-if="qualityIssues.length > 0"
      class="rounded-lg border p-3"
      :class="qualitySeverity === 'warning'
        ? 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20'
        : 'border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/20'"
    >
      <div class="flex items-start gap-2.5">
        <svg
          class="w-5 h-5 flex-shrink-0 mt-0.5"
          :class="qualitySeverity === 'warning' ? 'text-amber-600 dark:text-amber-400' : 'text-primary-600 dark:text-primary-400'"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <div class="min-w-0 flex-1">
          <p
            class="text-sm font-semibold"
            :class="qualitySeverity === 'warning' ? 'text-amber-700 dark:text-amber-400' : 'text-primary-700 dark:text-primary-400'"
          >
            کیفیت ترکیب
          </p>
          <ul class="text-xs mt-1 space-y-1 list-disc mr-4" :class="qualitySeverity === 'warning' ? 'text-amber-700 dark:text-amber-300' : 'text-primary-700 dark:text-primary-300'">
            <li v-for="issue in qualityIssues" :key="issue">{{ issue }}</li>
          </ul>

          <button
            v-if="showSelectionCta"
            type="button"
            @click="$emit('go-to-selection')"
            class="mt-2.5 inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg transition-colors"
            :class="qualitySeverity === 'warning'
              ? 'bg-amber-600 text-white hover:bg-amber-700'
              : 'bg-primary-600 text-white hover:bg-primary-700'"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 17l-5-5m0 0l5-5m-5 5h12" />
            </svg>
            بازگشت به انتخاب کود
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- ۳) سایر نکات (فقط اگر چیزی خارج از دو دسته بالا باقی مانده باشد) -->
    <!-- ============================================================ -->
    <div v-if="otherNotes.length > 0" class="rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/30 p-3">
      <p class="text-xs font-semibold text-gray-600 dark:text-gray-300 mb-1.5">سایر نکات</p>
      <ul class="text-xs text-gray-600 dark:text-gray-400 space-y-1 list-disc mr-4">
        <li v-for="note in otherNotes" :key="note">{{ note }}</li>
      </ul>
    </div>

    <!-- ============================================================ -->
    <!-- ۴) وضعیت مطلوب -->
    <!-- ============================================================ -->
    <div
      v-if="alertItems.length === 0 && legacyPrecipitation.length === 0 && qualityIssues.length === 0 && otherNotes.length === 0"
      class="flex items-center gap-2.5 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 p-3"
    >
      <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-sm text-emerald-700 dark:text-emerald-400">هیچ هشداری برای این ترکیب ثبت نشده؛ از نظر شیمیایی و دقت هدف در وضعیت مطلوبی است.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { cleanNote, isCoveredElsewhere, isGenericNote } from '@/utils/resultNotes';
import type { PrecipitationAlert } from '@/types';

const SEV = {
  danger: { label: 'خطر', box: 'border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-900/20', icon: 'text-rose-600 dark:text-rose-400', title: 'text-rose-700 dark:text-rose-400', text: 'text-rose-700/90 dark:text-rose-300', chip: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300' },
  warn: { label: 'هشدار', box: 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20', icon: 'text-amber-600 dark:text-amber-400', title: 'text-amber-700 dark:text-amber-400', text: 'text-amber-800 dark:text-amber-300', chip: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300' },
  info: { label: 'نکته', box: 'border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-900/20', icon: 'text-sky-600 dark:text-sky-400', title: 'text-sky-700 dark:text-sky-400', text: 'text-sky-800 dark:text-sky-300', chip: 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300' }
} as const;
const SCOPE = { stock: 'داخل استوک', final: 'محلول نهایی', water: 'آب منبع' } as const;

const props = defineProps<{
  warnings: string[];
  suggestions: string[];
  isConverged: boolean;
  accuracy: number;
  unusedCount: number;
  badElementsCount: number;
  alerts?: PrecipitationAlert[];
}>();

defineEmits<{
  (e: 'go-to-selection'): void;
}>();

const alertItems = computed(() => props.alerts || []);

const legacyPrecipitation = computed(() => {
  if (alertItems.value.length) return [];
  const seen = new Set<string>();
  return props.warnings
    .map((raw) => {
      const text = cleanNote(raw);
      const match = text.match(/^خطر رسوب:\s*(.+)$/);
      return match ? { compound: match[1].trim() } : null;
    })
    .filter((item): item is { compound: string } => {
      if (!item) return false;
      if (seen.has(item.compound)) return false;
      seen.add(item.compound);
      return true;
    });
});

const accuracy = computed(() => Math.max(0, Math.min(100, Number(props.accuracy) || 0)));

const qualityIssues = computed(() => {
  const issues: string[] = [];

  if (!props.isConverged) {
    issues.push('الگوریتم به یک ترکیب کاملاً پایدار نرسید؛ اعداد نمایش‌داده‌شده نزدیک‌ترین جواب ممکن هستند.');
  }

  if (accuracy.value < 85) {
    issues.push(`دقت کلی رسیدن به عناصر هدف پایین است (${accuracy.value.toFixed(0)}٪). با کودهای انتخاب‌شده، رسیدن دقیق به همه اهداف ممکن نیست.`);
  }

  if (props.badElementsCount > 0) {
    issues.push(`${props.badElementsCount} عنصر بیش از ۱۰٪ با هدف فاصله دارند (جزئیات در بخش «عناصر تأمین‌شده»).`);
  }

  if (props.unusedCount > 0) {
    issues.push(`${props.unusedCount} کود از لیست انتخابی شما در ترکیب نهایی وزنی نگرفت؛ می‌توانید آن را حذف کنید.`);
  }

  return issues;
});

const qualitySeverity = computed(() => {
  const critical = !props.isConverged || accuracy.value < 70 || props.badElementsCount >= 2;
  return critical ? 'warning' : 'info';
});

// دکمه «بازگشت به انتخاب کود» فقط وقتی نمایش داده می‌شود که واقعاً
// تغییر کودها می‌تواند مشکل را حل کند (نه صرفاً یک کود بلااستفاده)
const showSelectionCta = computed(
  () => !props.isConverged || accuracy.value < 85 || props.badElementsCount > 0
);

const otherNotes = computed(() => {
  const combined = [...props.warnings, ...props.suggestions].map(cleanNote);
  const seen = new Set<string>();
  const result: string[] = [];

  for (const text of combined) {
    if (text.length < 4) continue;
    if (/^خطر رسوب[:：]/.test(text)) continue;
    if (isCoveredElsewhere(text) || isGenericNote(text)) continue;
    if (seen.has(text)) continue;
    seen.add(text);
    result.push(text);
  }

  return result;
});
</script>
