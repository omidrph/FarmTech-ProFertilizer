import { ref, computed } from 'vue';
import axios from 'axios';

export function useConnection() {
  const status = ref<'checking' | 'connected' | 'disconnected'>('checking');
  const isDown = computed(() => status.value === 'disconnected');

  const check = async (): Promise<boolean> => {
    status.value = 'checking';
    try {
      const r = await axios.get('/health', { timeout: 3000 });
      status.value = r.status === 200 ? 'connected' : 'disconnected';
    } catch {
      status.value = 'disconnected';
    }
    return status.value === 'connected';
  };

  return { status, isDown, check };
}
