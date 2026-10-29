<!-- نشان نقش و وضعیت حساب -->
<template>
  <span v-if="role" class="ad-chip" :class="roleCls">{{ ROLE_LABEL[role] }}</span>
  <span v-if="status" class="ad-chip" :class="statusCls">{{ STATUS_LABEL[status] }}</span>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { ROLE_LABEL, STATUS_LABEL, type AccountStatus, type Role } from '@/services/adminApi';
const props = defineProps<{ role?: Role; status?: AccountStatus }>();
const roleCls = computed(() =>
  props.role === 'admin' ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300'
  : props.role === 'plus' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'
  : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300');
const statusCls = computed(() =>
  props.status === 'active' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300'
  : props.status === 'blocked' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300'
  : 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300');
</script>
