// frontend/src/services/shopApi.ts
// کلاینت API فروشگاه کاربر (کودهای سیستمی، سبد خرید، سفارش و رسید)
import axios from 'axios';

const BASE = (import.meta.env.VITE_API_URL || '/api/v1') + '/shop';
const http = axios.create({ baseURL: BASE, timeout: 25000, withCredentials: true });
http.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('access_token');
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export interface ShopProduct {
  id: number; name: string; brand?: string; category?: string; form?: string; formula?: string;
  elements: Record<string, number>; concentration?: number; price: number; unit: string;
  stock: number | null; min_qty: number | null; description?: string;
}
export interface CartLine { fertilizer_id: number; name: string; formula?: string; unit: string; qty: number; unit_price: number; line_total: number }
export interface Cart { items: CartLine[]; dropped: number[]; subtotal: number; shipping: number; total: number; note: string | null }
export interface ShopInfo { enabled: boolean; shipping_fee: number; free_shipping_over: number; min_order_total: number; currency_label: string; shop_note: string; require_address: boolean }
export interface Address { receiver: string; phone: string; province?: string; city?: string; address: string; postal_code?: string }

export const shopApi = {
  info: async () => (await http.get<ShopInfo>('/info')).data,
  items: async (q?: string) => (await http.get<{ items: ShopProduct[]; total: number }>('/items', { params: q ? { q } : {} })).data,
  cart: async () => (await http.get<Cart>('/cart')).data,
  saveCart: async (items: { fertilizer_id: number; qty: number }[], note?: string) => (await http.put<Cart>('/cart', { items, note: note || null })).data,
  addToCart: async (items: { fertilizer_id: number; qty: number }[], replace = false) => (await http.post<Cart>('/cart/add', { items, replace })).data,
  checkout: async (body: { address?: Address; customer_note?: string }) => (await http.post<any>('/orders', body)).data,
  orders: async () => (await http.get<{ items: any[] }>('/orders')).data.items,
  order: async (id: number) => (await http.get<any>(`/orders/${id}`)).data,
  sendReceipt: async (id: number, b: { image: string; last4?: string; paid_amount?: number; note?: string }) => (await http.post<any>(`/orders/${id}/receipt`, b)).data,
  cancel: async (id: number) => (await http.post<any>(`/orders/${id}/cancel`)).data,
  reopen: async (id: number) => (await http.post<any>(`/orders/${id}/reopen`)).data,
};

export function shopError(e: any, fallback = 'خطایی رخ داد'): string {
  const d = e?.response?.data?.detail;
  if (typeof d === 'string') return d;
  if (Array.isArray(d) && d[0]?.msg) return String(d[0].msg).replace('Value error, ', '');
  return fallback;
}
