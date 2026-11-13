// frontend/src/store/modules/shopStore.ts
// وضعیت سبد خرید (ذخیره در سرور) و درخواست باز شدن تب فروشگاه از جاهای دیگر برنامه (مثل صفحهٔ محاسبه)
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { shopApi, shopError, type Cart } from '@/services/shopApi';

export const useShopStore = defineStore('shop', () => {
  const cart = ref<Cart | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  /** هر بار که عددش زیاد شود، MainLayout تب فروشگاه را باز می‌کند */
  const openRequest = ref(0);
  const openOn = ref<'catalog' | 'cart' | 'orders'>('cart');

  const count = computed(() => cart.value?.items.length || 0);

  async function loadCart() {
    try { cart.value = await shopApi.cart(); error.value = null; } catch (e) { error.value = shopError(e); }
  }
  async function addMany(items: { fertilizer_id: number; qty: number }[], replace = false): Promise<boolean> {
    loading.value = true;
    try { cart.value = await shopApi.addToCart(items, replace); error.value = null; return true; }
    catch (e) { error.value = shopError(e); return false; }
    finally { loading.value = false; }
  }
  async function setQty(items: { fertilizer_id: number; qty: number }[]) {
    loading.value = true;
    try { cart.value = await shopApi.saveCart(items, cart.value?.note || undefined); error.value = null; }
    catch (e) { error.value = shopError(e); }
    finally { loading.value = false; }
  }
  function open(where: 'catalog' | 'cart' | 'orders' = 'cart') { openOn.value = where; openRequest.value++; }

  return { cart, loading, error, count, openRequest, openOn, loadCart, addMany, setQty, open };
});
