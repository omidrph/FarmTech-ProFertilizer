<!-- نوار افقی رتبه‌بندی‌شده (کاربران برتر، گیاهان، کودها) -->
<template>
  <ul v-if="items.length" class="space-y-2.5">
    <li v-for="(it, i) in items" :key="i" class="group" :class="clickable ? 'cursor-pointer' : ''" @click="clickable && $emit('select', it)">
      <div class="flex items-center justify-between gap-2 text-xs mb-1">
        <span class="flex items-center gap-2 min-w-0">
          <span class="w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-bold flex-shrink-0"
            :style="{ background: color + '1f', color }">{{ (i + 1).toLocaleString('fa-IR') }}</span>
          <span class="truncate text-gray-700 dark:text-gray-200 group-hover:text-primary-600">{{ it.label }}</span>
        </span>
        <b class="tabular-nums text-gray-900 dark:text-white flex-shrink-0">{{ faNum(it.count) }}<span v-if="unit" class="font-normal text-gray-400"> {{ unit }}</span></b>
      </div>
      <div class="h-2 rounded-full bg-gray-100 dark:bg-gray-700/60 overflow-hidden">
        <div class="h-full rounded-full transition-all duration-700" :style="{ width: (ready ? (it.count / max) * 100 : 0) + '%', background: `linear-gradient(270deg, ${color}, ${color}aa)` }"></div>
      </div>
    </li>
  </ul>
  <p v-else class="text-sm text-gray-400 py-6 text-center">هنوز داده‌ای ثبت نشده است.</p>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { faNum } from './chartUtils';
const props = withDefaults(defineProps<{ items: { label: string; count: number; id?: number }[]; color?: string; unit?: string; clickable?: boolean }>(), { color: '#2563eb' });
defineEmits<{ (e: 'select', it: { label: string; count: number; id?: number }): void }>();
const ready = ref(false);
onMounted(() => requestAnimationFrame(() => (ready.value = true)));
const max = computed(() => Math.max(1, ...props.items.map((i) => i.count)));
</script>
