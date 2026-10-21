export type AuthContext = 'login' | 'register' | 'reset';
export interface FriendlyMessage { title: string; hint?: string }

const PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹';
const ARABIC_DIGITS = '٠١٢٣٤٥٦٧٨٩';

/** تبدیل ارقام فارسی/عربی به انگلیسی */
export const normalizeDigits = (s: string): string =>
  s.replace(/[۰-۹٠-٩]/g, (d) => {
    const i = PERSIAN_DIGITS.indexOf(d);
    return String(i >= 0 ? i : ARABIC_DIGITS.indexOf(d));
  });

export const isValidPhone = (s: string): boolean => /^09\d{9}$/.test(s);

/** تبدیل پیام خام سرور/سیستم به پیام قابل‌فهم برای کاربر */
export function friendlyAuthError(raw: string, ctx: AuthContext): FriendlyMessage {
  const m = raw || '';
  if (/بک‌اند|Network|ارتباط با سرور|اتصال به سرور برقرار/i.test(m))
    return { title: 'ارتباط با سرور برقرار نشد', hint: 'اینترنت خود را بررسی کنید و دوباره تلاش کنید.' };
  if (/زمان‌بر|timeout/i.test(m))
    return { title: 'پاسخ سرور دیر رسید', hint: 'چند لحظه صبر کنید و دوباره تلاش کنید.' };
  if (/قبلاً ثبت|already|موجود است/i.test(m))
    return { title: 'این شماره قبلاً ثبت شده است.', hint: 'وارد شوید یا از «فراموشی رمز عبور» استفاده کنید.' };
  if (/تعداد درخواست|rate|too many/i.test(m))
    return { title: 'تلاش‌های شما بیش از حد مجاز بود.', hint: 'چند دقیقه بعد دوباره امتحان کنید.' };
  if (/غیرفعال|قفل/.test(m))
    return { title: 'حساب شما در دسترس نیست.', hint: 'برای رفع مشکل با پشتیبانی تماس بگیرید.' };
  if (ctx === 'login' && /اشتباه|یافت نشد|incorrect|invalid/i.test(m))
    return { title: 'شمارهٔ موبایل یا رمز عبور درست نیست.', hint: 'اگر رمز را فراموش کرده‌اید، از لینک بازیابی استفاده کنید.' };
  if (ctx === 'reset' && /کد|code/i.test(m) && /نادرست|منقضی|نامعتبر|اشتباه|invalid|expired/i.test(m))
    return { title: 'کد نادرست یا منقضی شده است.', hint: 'دوباره کد بگیرید و کد تازه را وارد کنید.' };
  if (/اعتبارسنجی|422|صحیح نیست|نامعتبر/.test(m))
    return { title: 'برخی اطلاعات درست وارد نشده‌اند.', hint: 'فیلدها را بررسی کنید و دوباره تلاش کنید.' };
  return { title: m || 'مشکلی پیش آمد.', hint: 'دوباره تلاش کنید؛ اگر ادامه داشت با پشتیبانی تماس بگیرید.' };
}
