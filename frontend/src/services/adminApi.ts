// frontend/src/services/adminApi.ts
// کلاینت API پنل مدیریت (همهٔ مسیرها زیر /admin و فقط برای نقش admin)
import axios, { type AxiosInstance } from 'axios';

const BASE = import.meta.env.VITE_API_URL || '/api/v1';

export type Role = 'user' | 'plus' | 'admin';
export type AccountStatus = 'active' | 'blocked' | 'banned';

export interface Paged<T> { items: T[]; total: number; page: number; page_size: number; pages: number }

export interface AdminUserRow {
  id: number; first_name: string; last_name: string; full_name: string; phone_number: string;
  role: Role; status: AccountStatus; is_active: boolean; status_reason: string | null; status_until: string | null;
  created_at: string | null; last_login: string | null; last_ip: string | null; is_2fa_enabled: boolean;
  reports_count: number; calculations_count: number;
}
export interface AdminUserDetail extends AdminUserRow {
  admin_note: string | null; failed_attempts: number; locked_until: string | null; last_user_agent: string | null;
  status_changed_at: string | null; status_changed_by: number | null;
  counts: { reports: number; fertilizers: number; calculations: number; ph_adjustments: number; active_sessions: number };
  recent_security: { id: number; event_type: string; severity: string; ip: string | null; created_at: string }[];
  recent_calculations: { id: number; is_successful: boolean; cost_total: number | null; created_at: string }[];
}

class AdminApi {
  private http: AxiosInstance;
  constructor() {
    this.http = axios.create({ baseURL: BASE + '/admin', timeout: 20000, withCredentials: true });
    this.http.interceptors.request.use((cfg) => {
      const cookie = document.cookie.split(';').map((c) => c.trim()).find((c) => c.startsWith('access_token='));
      const token = cookie ? cookie.substring('access_token='.length) : localStorage.getItem('access_token');
      if (token) cfg.headers.Authorization = `Bearer ${token}`;
      return cfg;
    });
  }
  private async get<T>(url: string, params?: Record<string, any>): Promise<T> {
    const clean = Object.fromEntries(Object.entries(params || {}).filter(([, v]) => v !== '' && v !== null && v !== undefined));
    return (await this.http.get<T>(url, { params: clean })).data;
  }
  private async post<T>(url: string, body?: any): Promise<T> { return (await this.http.post<T>(url, body ?? {})).data; }
  private async put<T>(url: string, body?: any): Promise<T> { return (await this.http.put<T>(url, body ?? {})).data; }
  private async del<T>(url: string): Promise<T> { return (await this.http.delete<T>(url)).data; }

  stats = () => this.get<any>('/stats');
  system = () => this.get<any>('/system');

  users = (p: Record<string, any>) => this.get<Paged<AdminUserRow>>('/users', p);
  user = (id: number) => this.get<AdminUserDetail>(`/users/${id}`);
  createUser = (b: any) => this.post<AdminUserRow>('/users', b);
  updateUser = (id: number, b: any) => this.put<AdminUserRow>(`/users/${id}`, b);
  setRole = (id: number, role: Role) => this.put<AdminUserRow>(`/users/${id}/role`, { role });
  block = (id: number, reason?: string, hours?: number | null) => this.post<AdminUserRow>(`/users/${id}/block`, { reason, hours });
  ban = (id: number, reason?: string) => this.post<AdminUserRow>(`/users/${id}/ban`, { reason });
  restore = (id: number) => this.post<AdminUserRow>(`/users/${id}/restore`);
  resetPassword = (id: number, new_password?: string) => this.post<{ ok: boolean; password: string | null }>(`/users/${id}/reset-password`, { new_password });
  revokeSessions = (id: number) => this.post(`/users/${id}/revoke-sessions`);
  unlock = (id: number) => this.post<AdminUserRow>(`/users/${id}/unlock`);
  disable2fa = (id: number) => this.post<AdminUserRow>(`/users/${id}/disable-2fa`);
  deleteUser = (id: number) => this.del(`/users/${id}`);
  bulk = (b: any) => this.post<{ done: number[]; skipped: { id: number; reason: string }[] }>('/users/bulk', b);

  fertilizers = (q?: string) => this.get<{ items: any[]; total: number }>('/fertilizers', { q });
  createFertilizer = (b: any) => this.post<any>('/fertilizers', b);
  updateFertilizer = (id: number, b: any) => this.put<any>(`/fertilizers/${id}`, b);
  deleteFertilizer = (id: number) => this.del(`/fertilizers/${id}`);

  calculations = (p: Record<string, any>) => this.get<Paged<any>>('/calculations', p);
  calculation = (id: number) => this.get<any>(`/calculations/${id}`);
  securityLogs = (p: Record<string, any>) => this.get<Paged<any> & { event_types: string[] }>('/security-logs', p);
  audit = (p: Record<string, any>) => this.get<Paged<any>>('/audit', p);

  announcements = () => this.get<{ items: any[] }>('/announcements');
  createAnnouncement = (b: any) => this.post<any>('/announcements', b);
  updateAnnouncement = (id: number, b: any) => this.put<any>(`/announcements/${id}`, b);
  deleteAnnouncement = (id: number) => this.del(`/announcements/${id}`);

  settings = () => this.get<any>('/settings');
  updateSettings = (b: any) => this.put<any>('/settings', b);
}

export const adminApi = new AdminApi();

/** پیام خطای فارسی از پاسخ API */
export function apiError(e: any, fallback = 'خطایی رخ داد'): string {
  const d = e?.response?.data?.detail;
  if (typeof d === 'string') return d;
  if (Array.isArray(d) && d[0]?.msg) return String(d[0].msg).replace('Value error, ', '');
  return e?.response?.data?.message || fallback;
}

// ===== قالب‌بندی مشترک =====
export const faN = (v: number | null | undefined) => (v ?? 0).toLocaleString('fa-IR');
export const faDate = (iso: string | null | undefined, withTime = true): string => {
  if (!iso) return '—';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '—';
  const opts: Intl.DateTimeFormatOptions = withTime
    ? { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
    : { year: 'numeric', month: '2-digit', day: '2-digit' };
  return d.toLocaleString('fa-IR', opts).replace(/[،,]\s*/, ' ');
};
export const ROLE_LABEL: Record<Role, string> = { user: 'کاربر معمولی', plus: 'کاربر پلاس', admin: 'مدیر' };
export const STATUS_LABEL: Record<AccountStatus, string> = { active: 'فعال', blocked: 'مسدود', banned: 'بن‌شده' };
