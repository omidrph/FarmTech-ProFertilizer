<!-- frontend/src/components/features/WidgetsTab.vue -->
<!--
  تب «ابزارک‌ها»
  ------------------------------------------------------------
  • حالت لیست: کارت‌های ابزارک‌ها (از widgetRegistry.ts)
  • حالت ابزارک باز: عنوان + دکمه‌ی بازگشت + بدنه‌ی ابزارک
  برای افزودن ابزارک جدید فقط widgets/widgetRegistry.ts را ویرایش کنید.
-->
<template>
  <div class="space-y-4 sm:space-y-5">

    <!-- ===================== لیست ابزارک‌ها ===================== -->
    <template v-if="!activeWidget">
      <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-10 h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </div>
            <div class="min-w-0">
              <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white">ابزارک‌ها</h2>
              <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">ابزارهای کمکی و ماشین‌حساب‌های سریع</p>
            </div>
          </div>

          <div v-if="widgets.length > SEARCH_THRESHOLD" class="relative sm:w-64">
            <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="query"
              type="text"
              placeholder="جستجوی ابزارک..."
              class="w-full pr-9 pl-3 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-700 transition-all"
            />
          </div>
        </div>
      </section>

      <div v-if="filteredWidgets.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        <component
          :is="isAvailable(widget) ? 'button' : 'div'"
          v-for="widget in filteredWidgets"
          :key="widget.id"
          :type="isAvailable(widget) ? 'button' : undefined"
          @click="isAvailable(widget) && openWidget(widget.id)"
          class="group text-right bg-white dark:bg-gray-800 rounded-2xl border p-4 sm:p-5 transition-all"
          :class="isAvailable(widget)
            ? 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-md cursor-pointer'
            : 'border-gray-200 dark:border-gray-700 opacity-75'"
        >
          <div class="flex items-start justify-between gap-3">
            <div
              class="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 transition-colors"
              :class="isAvailable(widget)
                ? 'bg-primary-50 dark:bg-primary-900/30 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'
                : 'bg-gray-100 dark:bg-gray-700'"
            >
              <svg
                class="w-5 h-5"
                :class="isAvailable(widget) ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400 dark:text-gray-500'"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="widget.iconPath" />
              </svg>
            </div>

            <span
              v-if="!isAvailable(widget)"
              class="text-[11px] font-medium px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
            >به‌زودی</span>
            <svg
              v-else
              class="w-4 h-4 mt-1 text-gray-300 dark:text-gray-600 group-hover:text-primary-500 transition-colors"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </div>

          <h3 class="mt-3 text-sm sm:text-base font-bold text-gray-900 dark:text-white">{{ widget.title }}</h3>
          <p class="mt-1 text-xs sm:text-sm text-gray-500 dark:text-gray-400 leading-6">{{ widget.description }}</p>
        </component>
      </div>

      <div
        v-else
        class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 py-10 text-center"
      >
        <p class="text-sm text-gray-500 dark:text-gray-400">ابزارکی با این عبارت پیدا نشد.</p>
      </div>
    </template>

    <!-- ===================== ابزارک باز ===================== -->
    <template v-else>
      <div class="flex items-center gap-3">
        <button
          type="button"
          @click="closeWidget"
          class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex-shrink-0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          ابزارک‌ها
        </button>
        <div class="min-w-0">
          <h2 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white truncate">{{ activeWidget.title }}</h2>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate hidden sm:block">{{ activeWidget.description }}</p>
        </div>
      </div>

      <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
        <component :is="activeComponent" v-if="activeComponent" />
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent, shallowRef, watch } from 'vue';
import type { Component } from 'vue';
import { widgetRegistry } from './widgets/widgetRegistry';
import type { WidgetDefinition } from './widgets/widgetRegistry';

const SEARCH_THRESHOLD = 6;

const widgets = widgetRegistry;
const query = ref('');
const activeWidgetId = ref<string | null>(null);
const activeComponent = shallowRef<Component | null>(null);

const isAvailable = (widget: WidgetDefinition) => widget.status === 'ready' && !!widget.component;

const filteredWidgets = computed(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return widgets;
  return widgets.filter(w => `${w.title} ${w.description}`.toLowerCase().includes(q));
});

const activeWidget = computed(() => widgets.find(w => w.id === activeWidgetId.value) || null);

// کامپوننت ابزارک فقط هنگام باز شدن بارگذاری می‌شود
watch(activeWidget, widget => {
  const loader = widget?.component;
  activeComponent.value = loader
    ? defineAsyncComponent(async () => (await loader()).default)
    : null;
});

const openWidget = (id: string) => {
  activeWidgetId.value = id;
  window.scrollTo({ top: 0, behavior: 'auto' });
};

const closeWidget = () => {
  activeWidgetId.value = null;
};
</script>
