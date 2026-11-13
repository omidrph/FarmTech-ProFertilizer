<!-- frontend/src/components/common/AnnouncementView.vue -->
<!-- نمایش یک اعلان به یکی از ۷ سبک: bar | ticker | ribbon | card | toast | corner | modal
     inline=true → برای پیش‌نمایش پنل مدیریت (بدون موقعیت ثابت) -->
<template>
  <!-- نوار -->
  <div v-if="a.style === 'bar' || !a.style" class="px-4 py-2 text-sm flex items-start justify-between gap-3" :class="solid[a.level] || solid.info">
    <p class="min-w-0"><b>{{ a.title }}</b><span v-if="a.body" class="opacity-90"> — {{ a.body }}</span>
      <a v-if="a.link_url" :href="a.link_url" target="_blank" rel="noopener" class="underline font-semibold mr-2">{{ a.link_label || 'بیشتر' }}</a></p>
    <button v-if="a.dismissible !== false" class="flex-shrink-0 opacity-80 hover:opacity-100 text-lg leading-none" aria-label="بستن اعلان" @click="$emit('dismiss')">×</button>
  </div>

  <!-- نوار متحرک -->
  <div v-else-if="a.style === 'ticker'" class="relative overflow-hidden text-sm py-1.5 flex items-center" :class="solid[a.level] || solid.info" dir="ltr">
    <div class="ann-ticker whitespace-nowrap flex-1" dir="rtl"><span class="inline-block px-8"><b>{{ a.title }}</b><span v-if="a.body"> — {{ a.body }}</span></span><span class="inline-block px-8" aria-hidden="true"><b>{{ a.title }}</b><span v-if="a.body"> — {{ a.body }}</span></span></div>
    <button v-if="a.dismissible !== false" class="px-3 text-lg leading-none opacity-80 hover:opacity-100 flex-shrink-0" aria-label="بستن اعلان" @click="$emit('dismiss')">×</button>
  </div>

  <!-- روبان گرادیانی -->
  <div v-else-if="a.style === 'ribbon'" class="px-4 py-2.5 text-sm flex items-center justify-between gap-3 text-white bg-gradient-to-l" :class="grad[a.level] || grad.info">
    <p class="min-w-0 flex items-center gap-2"><span class="text-base">{{ icon[a.level] }}</span><span><b>{{ a.title }}</b><span v-if="a.body" class="opacity-90"> {{ a.body }}</span></span></p>
    <div class="flex items-center gap-2 flex-shrink-0">
      <a v-if="a.link_url" :href="a.link_url" target="_blank" rel="noopener" class="px-3 py-1 rounded-full bg-white/20 hover:bg-white/30 text-xs font-semibold">{{ a.link_label || 'بیشتر' }}</a>
      <button v-if="a.dismissible !== false" class="text-lg leading-none opacity-80 hover:opacity-100" aria-label="بستن اعلان" @click="$emit('dismiss')">×</button>
    </div>
  </div>

  <!-- کارت / توست / گوشه / مودال: همگی کارت‌اند، فقط موقعیتشان فرق می‌کند (در SystemBanner) -->
  <div v-else-if="a.style === 'modal'" class="w-full max-w-sm rounded-3xl bg-white dark:bg-gray-800 shadow-2xl overflow-hidden" :class="inline ? 'mx-auto border border-gray-200 dark:border-gray-700' : ''">
    <div class="h-1.5 bg-gradient-to-l" :class="grad[a.level] || grad.info"></div>
    <div class="p-5 text-center">
      <div class="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center text-2xl mb-3" :class="soft[a.level] || soft.info">{{ icon[a.level] }}</div>
      <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ a.title }}</h3>
      <p v-if="a.body" class="text-sm text-gray-600 dark:text-gray-300 mt-2 leading-7 whitespace-pre-line">{{ a.body }}</p>
      <div class="mt-4 flex items-center justify-center gap-2">
        <a v-if="a.link_url" :href="a.link_url" target="_blank" rel="noopener" class="px-4 py-2 rounded-xl text-sm font-semibold text-white bg-primary-600 hover:bg-primary-700">{{ a.link_label || 'مشاهده' }}</a>
        <button class="px-4 py-2 rounded-xl text-sm border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700" @click="$emit('dismiss')">متوجه شدم</button>
      </div>
    </div>
  </div>

  <div v-else class="rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex" :class="a.style === 'corner' ? 'max-w-[18rem]' : 'max-w-md w-full'">
    <span class="w-1.5 flex-shrink-0" :class="bar[a.level] || bar.info"></span>
    <div class="p-3 flex items-start gap-2.5 min-w-0 flex-1">
      <span class="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0" :class="soft[a.level] || soft.info">{{ icon[a.level] }}</span>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ a.title }}</p>
        <p v-if="a.body" class="text-xs text-gray-600 dark:text-gray-300 mt-0.5 leading-6">{{ a.body }}</p>
        <a v-if="a.link_url" :href="a.link_url" target="_blank" rel="noopener" class="inline-block mt-1.5 text-xs font-semibold text-primary-600 dark:text-primary-400 hover:underline">{{ a.link_label || 'بیشتر' }} ←</a>
      </div>
      <button v-if="a.dismissible !== false" class="text-gray-400 hover:text-gray-600 text-lg leading-none flex-shrink-0" aria-label="بستن اعلان" @click="$emit('dismiss')">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface Ann { id?: number; title: string; body?: string | null; level: string; style?: string; dismissible?: boolean; link_url?: string | null; link_label?: string | null }
defineProps<{ a: Ann; inline?: boolean }>();
defineEmits<{ (e: 'dismiss'): void }>();

const solid: Record<string, string> = { info: 'bg-sky-600 text-white', success: 'bg-emerald-600 text-white', warning: 'bg-amber-500 text-white', danger: 'bg-rose-600 text-white' };
const grad: Record<string, string> = { info: 'from-sky-600 to-indigo-500', success: 'from-emerald-600 to-teal-500', warning: 'from-amber-500 to-orange-500', danger: 'from-rose-600 to-pink-500' };
const soft: Record<string, string> = { info: 'bg-sky-100 text-sky-600', success: 'bg-emerald-100 text-emerald-600', warning: 'bg-amber-100 text-amber-600', danger: 'bg-rose-100 text-rose-600' };
const bar: Record<string, string> = { info: 'bg-sky-500', success: 'bg-emerald-500', warning: 'bg-amber-500', danger: 'bg-rose-500' };
const icon: Record<string, string> = { info: 'ℹ️', success: '🎉', warning: '⚠️', danger: '🚨' };
</script>

<style scoped>
.ann-ticker { display: inline-flex; animation: ann-scroll 28s linear infinite; }
.ann-ticker:hover { animation-play-state: paused; }
@keyframes ann-scroll { from { transform: translateX(0); } to { transform: translateX(50%); } }
@media (prefers-reduced-motion: reduce) { .ann-ticker { animation: none; } }
</style>
