<!-- frontend/src/components/features/widgets/CompositionWidget.vue -->
<!-- ابزارک «تحلیل ترکیب کودی»: ترکیب را بنویسید، درصد هر عنصر و غلظت آن در محلول را ببینید -->
<template>
  <div class="space-y-3">
    <p class="text-sm leading-7 text-gray-600 dark:text-gray-300">
      فرمول مواد کود را بنویسید (مثلاً <code dir="ltr" class="px-1 rounded bg-gray-100 dark:bg-gray-700">KNO3</code>) و بگویید هر ماده چند درصد وزن کود است؛
      درصد هر عنصر و غلظت آن در محلول خودکار نمایش داده می‌شود. اگر مقدار یک عنصر را از روی برچسب می‌دانید، همان را مستقیم وارد کنید.
    </p>
    <AdvancedBuilder standalone />
  </div>
</template>

<script setup lang="ts">
import AdvancedBuilder from '../fertilizer-db/AdvancedBuilder.vue';
</script>
