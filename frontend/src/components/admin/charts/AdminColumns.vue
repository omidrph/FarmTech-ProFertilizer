<!-- ستون‌های عمودی ساده (توزیع هفتگی) با تولتیپ -->
<template>
  <div class="flex items-end gap-2 h-36">
    <div v-for="(it, i) in items" :key="i" class="flex-1 flex flex-col items-center justify-end h-full group relative">
      <span class="text-[10px] tabular-nums text-gray-500 dark:text-gray-400 mb-1 opacity-0 group-hover:opacity-100 transition">{{ faNum(it.count) }}</span>
      <div class="w-full max-w-[2.2rem] rounded-t-lg transition-all duration-700"
        :style="{ height: ready ? Math.max((it.count / max) * 100, it.count ? 6 : 2) + '%' : '0%', background: i === peak ? `linear-gradient(0deg, ${color}, ${color}cc)` : color + '55' }"></div>
      <span class="mt-1.5 text-[10px] text-gray-500 dark:text-gray-400 whitespace-nowrap">{{ it.label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { faNum } from './chartUtils';
const props = withDefaults(defineProps<{ items: { label: string; count: number }[]; color?: string }>(), { color: '#2563eb' });
const ready = ref(false);
onMounted(() => requestAnimationFrame(() => (ready.value = true)));
const max = computed(() => Math.max(1, ...props.items.map((i) => i.count)));
const peak = computed(() => props.items.reduce((p, it, i, a) => (it.count > a[p].count ? i : p), 0));
</script>
