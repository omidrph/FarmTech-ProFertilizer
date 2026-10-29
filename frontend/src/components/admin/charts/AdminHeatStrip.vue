<!-- نوار گرمایی ساعت‌های شبانه‌روز (یا هر فهرست برچسب‌دار) -->
<template>
  <div>
    <div class="grid gap-1" :style="{ gridTemplateColumns: `repeat(${items.length}, minmax(0, 1fr))` }">
      <div v-for="(it, i) in items" :key="i" class="relative group">
        <div class="aspect-[1/2.4] sm:aspect-[1/2] rounded-md transition-transform group-hover:scale-110"
          :style="{ background: it.count ? color : 'transparent', opacity: it.count ? 0.15 + 0.85 * (it.count / max) : 1 }"
          :class="it.count ? '' : 'bg-gray-100 dark:bg-gray-700/50'"></div>
        <div class="pointer-events-none absolute -top-8 left-1/2 -translate-x-1/2 hidden group-hover:block z-10 whitespace-nowrap rounded-lg bg-gray-900 text-white text-[10px] px-2 py-1 shadow-lg">
          {{ it.label }} · {{ faNum(it.count) }}
        </div>
      </div>
    </div>
    <div class="mt-1.5 flex justify-between text-[10px] text-gray-400"><span>{{ items[0]?.label }}</span><span>{{ items[Math.floor(items.length / 2)]?.label }}</span><span>{{ items[items.length - 1]?.label }}</span></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { faNum } from './chartUtils';
const props = withDefaults(defineProps<{ items: { label: string; count: number }[]; color?: string }>(), { color: '#2563eb' });
const max = computed(() => Math.max(1, ...props.items.map((i) => i.count)));
</script>
