<!-- frontend/src/components/common/AppModal.vue -->
<!--
  ============================================================
  قالب یکپارچه‌ی همه‌ی مودال‌های برنامه
  ------------------------------------------------------------
  - دسکتاپ: وسط صفحه، با گوشه‌های گرد
  - موبایل: کشوی پایین‌صفحه (Bottom Sheet) با حداکثر ۹۲٪ ارتفاع
  - هدر، بدنه‌ی قابل‌اسکرول و فوتر ثابت
  - بستن با Esc، کلیک روی پس‌زمینه و دکمه ×
  ------------------------------------------------------------
  اسلات‌ها:
    icon       آیکون کنار عنوان (اختیاری)
    header     جایگزین کامل هدر پیش‌فرض (مثلاً هدر پروفایل)
    subheader  نوار ثابت زیر هدر (تب‌ها، جستجو)
    default    بدنه‌ی قابل‌اسکرول
    footer     فوتر ثابت (اختیاری)
  ============================================================
-->
<template>
  <Teleport to="body">
    <Transition name="app-modal">
      <div
        v-if="open"
        class="fixed inset-0 z-[100]"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <div
          class="app-modal-backdrop absolute inset-0 bg-gray-900/70 backdrop-blur-sm"
          @click="onBackdropClick"
        ></div>

        <div class="relative h-full flex items-end sm:items-center justify-center sm:p-6 pointer-events-none">
          <div
            class="app-modal-panel pointer-events-auto relative w-full flex flex-col bg-white dark:bg-gray-800 shadow-2xl overflow-hidden rounded-t-2xl sm:rounded-2xl"
            :class="[sizeClass, tall ? 'h-[92dvh] sm:h-[min(90dvh,760px)]' : 'max-h-[92dvh] sm:max-h-[90dvh]']"
          >
            <!-- هدر -->
            <header class="flex-shrink-0 bg-gradient-to-l from-primary-600 to-primary-700 dark:from-primary-800 dark:to-primary-900 text-white">
              <slot name="header" :close="close">
                <div class="px-4 sm:px-6 py-4 flex items-center justify-between gap-3">
                  <div class="flex items-center gap-3 min-w-0">
                    <div
                      v-if="$slots.icon"
                      class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center flex-shrink-0"
                    >
                      <span class="w-5 h-5 flex items-center justify-center"><slot name="icon" /></span>
                    </div>
                    <div class="min-w-0">
                      <h3 :id="titleId" class="text-base sm:text-lg font-bold text-white truncate">{{ title }}</h3>
                      <p v-if="subtitle" class="text-xs text-primary-100/90 truncate">{{ subtitle }}</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    @click="close"
                    aria-label="بستن"
                    class="flex-shrink-0 p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </slot>
            </header>

            <div v-if="$slots.subheader" class="flex-shrink-0">
              <slot name="subheader" />
            </div>

            <!-- بدنه -->
            <div
              class="app-modal-body flex-1 min-h-0 overflow-y-auto overscroll-contain"
              :class="flush ? '' : 'px-4 sm:px-6 py-4 sm:py-5'"
            >
              <slot />
            </div>

            <!-- فوتر -->
            <footer
              v-if="$slots.footer"
              class="flex-shrink-0 bg-gray-50 dark:bg-gray-700/30 border-t border-gray-200 dark:border-gray-600 px-4 sm:px-6 py-3 sm:py-4"
              style="padding-bottom: max(0.75rem, env(safe-area-inset-bottom));"
            >
              <slot name="footer" />
            </footer>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onBeforeUnmount } from 'vue';

let modalCounter = 0;

interface Props {
  open: boolean;
  title?: string;
  subtitle?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** بدنه بدون padding داخلی (برای لیست‌ها و تب‌ها) */
  flush?: boolean;
  /** ارتفاع ثابت؛ برای مودال‌هایی که با تغییر تب، اندازه‌شان نباید بپرد */
  tall?: boolean;
  closeOnBackdrop?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  subtitle: '',
  size: 'md',
  flush: false,
  tall: false,
  closeOnBackdrop: true
});

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const titleId = `app-modal-title-${++modalCounter}`;

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'sm:max-w-md';
    case 'lg':
      return 'sm:max-w-3xl';
    case 'xl':
      return 'sm:max-w-4xl';
    default:
      return 'sm:max-w-2xl';
  }
});

const close = () => emit('close');

const onBackdropClick = () => {
  if (props.closeOnBackdrop) close();
};

const onKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') close();
};

let previousOverflow = '';

const lockScroll = () => {
  previousOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  window.addEventListener('keydown', onKeydown);
};

const unlockScroll = () => {
  document.body.style.overflow = previousOverflow;
  window.removeEventListener('keydown', onKeydown);
};

watch(
  () => props.open,
  (isOpen, wasOpen) => {
    if (isOpen && !wasOpen) lockScroll();
    else if (!isOpen && wasOpen) unlockScroll();
  },
  { immediate: true }
);

onBeforeUnmount(() => {
  if (props.open) unlockScroll();
});
</script>

<style>
/* ---------- انیمیشن ---------- */
.app-modal-enter-active,
.app-modal-leave-active {
  transition: opacity 0.2s ease;
}
.app-modal-enter-active .app-modal-panel,
.app-modal-leave-active .app-modal-panel {
  transition: transform 0.22s ease, opacity 0.22s ease;
}
.app-modal-enter-from,
.app-modal-leave-to {
  opacity: 0;
}
.app-modal-enter-from .app-modal-panel,
.app-modal-leave-to .app-modal-panel {
  transform: translateY(32px);
  opacity: 0.6;
}
@media (min-width: 640px) {
  .app-modal-enter-from .app-modal-panel,
  .app-modal-leave-to .app-modal-panel {
    transform: scale(0.97);
  }
}
@media (prefers-reduced-motion: reduce) {
  .app-modal-enter-active,
  .app-modal-leave-active,
  .app-modal-enter-active .app-modal-panel,
  .app-modal-leave-active .app-modal-panel {
    transition: none;
  }
}

/* ---------- اسکرول‌بار ---------- */
.app-modal-body::-webkit-scrollbar {
  width: 6px;
}
.app-modal-body::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.dark .app-modal-body::-webkit-scrollbar-thumb {
  background: #4b5563;
}

/* ---------- دکمه‌های استاندارد مودال ---------- */
.app-modal-actions {
  @apply flex flex-col-reverse sm:flex-row sm:justify-end gap-2 sm:gap-3;
}
.app-modal-btn {
  @apply inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-colors w-full sm:w-auto disabled:opacity-50 disabled:cursor-not-allowed;
}
.app-modal-btn-primary {
  @apply bg-primary-600 hover:bg-primary-700 text-white;
}
.app-modal-btn-secondary {
  @apply bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700;
}
.app-modal-btn-danger {
  @apply bg-danger-600 hover:bg-danger-700 text-white;
}
</style>
