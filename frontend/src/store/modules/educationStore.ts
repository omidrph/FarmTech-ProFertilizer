// frontend/src/store/modules/educationStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface QuickStartStep {
  id: string;
  title: string;
  description: string;
  details: string[];
  tips: string[];
  warnings: string[];
  order: number;
}

export const useEducationStore = defineStore('education', () => {
  // ===== State =====
  const faqItems = ref<FAQItem[]>([]);
  const quickStartSteps = ref<QuickStartStep[]>([]);
  const searchQuery = ref('');
  const activeCategory = ref<string>('all');

  // ===== Getters =====
  const filteredFAQs = computed(() => {
    let items = faqItems.value;
    
    if (activeCategory.value !== 'all') {
      items = items.filter(item => item.category === activeCategory.value);
    }
    
    if (searchQuery.value.trim()) {
      const query = searchQuery.value.trim().toLowerCase();
      items = items.filter(item => 
        item.question.toLowerCase().includes(query) ||
        item.answer.toLowerCase().includes(query) ||
        item.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }
    
    return items;
  });

  const sortedQuickStartSteps = computed(() => {
    return [...quickStartSteps.value].sort((a, b) => a.order - b.order);
  });

  const categories = computed(() => {
    const cats = new Set(faqItems.value.map(item => item.category));
    return ['all', ...cats];
  });

  const totalFAQs = computed(() => faqItems.value.length);
  const totalQuickStartSteps = computed(() => quickStartSteps.value.length);

  // ===== Actions =====
  function addFAQ(faq: Omit<FAQItem, 'id' | 'createdAt' | 'updatedAt'>) {
    const newFAQ: FAQItem = {
      ...faq,
      id: generateId(),
      createdAt: new Date(),
      updatedAt: new Date()
    };
    faqItems.value.push(newFAQ);
    return newFAQ;
  }

  function updateFAQ(id: string, data: Partial<Omit<FAQItem, 'id' | 'createdAt' | 'updatedAt'>>) {
    const index = faqItems.value.findIndex(item => item.id === id);
    if (index !== -1) {
      faqItems.value[index] = {
        ...faqItems.value[index],
        ...data,
        updatedAt: new Date()
      };
      return true;
    }
    return false;
  }

  function deleteFAQ(id: string) {
    const index = faqItems.value.findIndex(item => item.id === id);
    if (index !== -1) {
      faqItems.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function addQuickStartStep(step: Omit<QuickStartStep, 'id'>) {
    const newStep: QuickStartStep = {
      ...step,
      id: generateId()
    };
    quickStartSteps.value.push(newStep);
    return newStep;
  }

  function updateQuickStartStep(id: string, data: Partial<Omit<QuickStartStep, 'id'>>) {
    const index = quickStartSteps.value.findIndex(step => step.id === id);
    if (index !== -1) {
      quickStartSteps.value[index] = {
        ...quickStartSteps.value[index],
        ...data
      };
      return true;
    }
    return false;
  }

  function deleteQuickStartStep(id: string) {
    const index = quickStartSteps.value.findIndex(step => step.id === id);
    if (index !== -1) {
      quickStartSteps.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function setSearchQuery(query: string) {
    searchQuery.value = query;
  }

  function setActiveCategory(category: string) {
    activeCategory.value = category;
  }

  function clearSearch() {
    searchQuery.value = '';
  }

  function resetCategories() {
    activeCategory.value = 'all';
  }

  // ===== Helper Functions =====
  function generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substring(2, 9);
  }

  // ===== Initialize with Sample Data =====
  function initializeSampleFAQs() {
    const sampleFAQs: Omit<FAQItem, 'id' | 'createdAt' | 'updatedAt'>[] = [
      {
        question: 'چطور یک کود جدید به پایگاه داده اضافه کنم؟',
        answer: 'برای افزودن کود جدید مراحل زیر را دنبال کنید:\n1. به تب "خانه" و سپس "پایگاه داده کودها" بروید\n2. روی دکمه "افزودن کود جدید" کلیک کنید\n3. نام کود، قیمت هر کیلوگرم و درصد عناصر را وارد کنید\n4. برای ذخیره، روی "ذخیره" کلیک کنید\n\n⚠️ توجه: درصد عناصر باید بین ۰ تا ۱۰۰ باشد.',
        category: 'پایگاه داده',
        tags: ['کود', 'پایگاه داده', 'افزودن']
      },
      {
        question: 'واحدهای اندازه‌گیری در نرم‌افزار چیست و چگونه تغییر کنم؟',
        answer: 'نرم‌افزار از سه واحد اندازه‌گیری پشتیبانی می‌کند:\n- PPM/L (قسمت در میلیون) - واحد پیش‌فرض\n- MEQ/L (میلی‌اکی والان در لیتر)\n- MMOLS/L (میلی‌مول در لیتر)\n\nبرای تغییر واحد، در بخش‌های "عناصر هدف" یا "آنالیز آب"، از منوی کشویی "واحد" استفاده کنید.',
        category: 'تنظیمات',
        tags: ['واحد', 'اندازه‌گیری', 'PPM', 'MEQ', 'MMOL']
      },
      {
        question: 'تعادل یونی چیست و چرا مهم است؟',
        answer: 'تعادل یونی به برابری مجموع بارهای مثبت (کاتیون‌ها) و منفی (آنیون‌ها) در محلول غذایی گفته می‌شود.\n\nاهمیت تعادل یونی:\n- جذب بهینه عناصر توسط گیاه\n- پیشگیری از تنش‌های تغذیه‌ای\n- افزایش بازده محصول\n\n✅ نرم‌افزار به صورت خودکار تعادل یونی را محاسبه و در صورت نامتعادل بودن هشدار می‌دهد.',
        category: 'تغذیه',
        tags: ['تعادل یونی', 'کاتیون', 'آنیون', 'تغذیه']
      },
      {
        question: 'چطور می‌توانم گزارش را چاپ کنم؟',
        answer: 'برای چاپ گزارش از هر بخشی از نرم‌افزار، کافیست روی دکمه "🖨️ چاپ" که در پایین هر تب وجود دارد کلیک کنید.\n\nهمچنین می‌توانید از کلیدهای میانبر زیر استفاده کنید:\n- Ctrl + P (ویندوز/لینوکس)\n- Cmd + P (مک)\n\n💡 نکته: قبل از چاپ، می‌توانید از حالت "پیش‌نمایش چاپ" مرورگر خود استفاده کنید.',
        category: 'گزارش',
        tags: ['چاپ', 'گزارش', 'پرینت']
      },
      {
        question: 'آیا می‌توانم از نرم‌افزار به صورت آفلاین استفاده کنم؟',
        answer: 'نرم‌افزار FarmTech - ProFertilizer به صورت آفلاین کار می‌کند و تمام داده‌ها در دیتابیس محلی (SQLite) ذخیره می‌شوند.\n\nمزایای استفاده آفلاین:\n- بدون نیاز به اتصال اینترنت\n- سرعت بالا در پردازش\n- امنیت بیشتر داده‌ها\n\n⚠️ توجه: برای نصب اولیه و به‌روزرسانی‌ها به اتصال اینترنت نیاز دارید.',
        category: 'عمومی',
        tags: ['آفلاین', 'اینترنت', 'دیتابیس', 'محلی']
      },
      {
        question: 'فرمول‌های محاسباتی نرم‌افزار بر چه اساسی است؟',
        answer: 'محاسبات نرم‌افزار بر اساس اصول علمی زیر انجام می‌شود:\n- تبدیل واحدها: PPM ↔ MEQ ↔ MMOL با استفاده از وزن مولکولی و ظرفیت یونی\n- تعادل یونی: مجموع کاتیون‌ها = مجموع آنیون‌ها (با تلرانس ۰.۵)\n- محاسبه سهم کود: (وزن × درصد عنصر × خلوص) ÷ ۱۰۰\n- محاسبه هزینه: (وزن ÷ ۱۰۰۰) × قیمت هر کیلوگرم\n\n🔬 فرمول‌ها بر اساس استانداردهای بین‌المللی تغذیه گیاهان طراحی شده‌اند.',
        category: 'محاسبات',
        tags: ['فرمول', 'محاسبه', 'علمی', 'استاندارد']
      },
      {
        question: 'چطور می‌توانم داده‌های خود را پشتیبان‌گیری کنم؟',
        answer: 'برای پشتیبان‌گیری از داده‌های خود، می‌توانید از روش‌های زیر استفاده کنید:\n1. پشتیبان‌گیری دستی: فایل farmtech.db را کپی کنید\n2. استفاده از ابزار backup_tool.py: در ریشه پروژه وجود دارد\n3. خروجی JSON: از طریق API می‌توانید داده‌ها را به صورت JSON دریافت کنید\n\n✅ پیشنهاد می‌شود به صورت دوره‌ای از داده‌های خود پشتیبان‌گیری کنید.',
        category: 'عمومی',
        tags: ['پشتیبان', 'بکاپ', 'داده', 'امنیت']
      },
      {
        question: 'آیا نرم‌افزار از چند زبان پشتیبانی می‌کند؟',
        answer: 'در حال حاضر نرم‌افزار به دو زبان زیر در دسترس است:\n- فارسی (زبان پیش‌فرض)\n- انگلیسی (در حال توسعه)\n\n💡 برای تغییر زبان، از بخش تنظیمات (در حال توسعه) استفاده کنید.',
        category: 'تنظیمات',
        tags: ['زبان', 'فارسی', 'انگلیسی', 'چندزبانه']
      },
      {
        question: 'چه عناصری در نرم‌افزار قابل تنظیم هستند؟',
        answer: 'نرم‌افزار از ۱۵ عنصر اصلی تغذیه گیاه پشتیبانی می‌کند:\nN-NO3, P, S, N-NH4, K, Ca, Mg, Na, Cl, Fe, Mn, Zn, B, Cu, Mo\n\n* عناصر پرکاربرد و ضروری برای تغذیه گیاهان',
        category: 'تغذیه',
        tags: ['عناصر', 'تغذیه', 'جدول تناوبی']
      },
      {
        question: 'چطور می‌توانم با تیم پشتیبانی تماس بگیرم؟',
        answer: 'برای ارتباط با تیم پشتیبانی FarmTech از روش‌های زیر استفاده کنید:\n- تلفن: ۰۲۱-۱۲۳۴۵۶۷۸\n- ایمیل: info@farmtech.ir\n- بخش ارتباط با ما: در منوی اصلی نرم‌افزار\n\n✅ تیم پشتیبانی در ساعات کاری پاسخگوی شما خواهد بود.',
        category: 'پشتیبانی',
        tags: ['پشتیبانی', 'تماس', 'ارتباط']
      }
    ];

    sampleFAQs.forEach(faq => addFAQ(faq));
  }

  function initializeQuickStartSteps() {
    const steps: Omit<QuickStartStep, 'id'>[] = [
      {
        title: 'ثبت‌نام و ورود به سیستم',
        description: 'برای استفاده از نرم‌افزار ابتدا باید ثبت‌نام کنید. پس از ثبت‌نام، با شماره تلفن و رمز عبور وارد شوید.',
        details: [
          'روی دکمه "ثبت‌نام" در صفحه ورود کلیک کنید',
          'نام، نام خانوادگی، شماره تلفن و رمز عبور خود را وارد کنید',
          'شماره تلفن باید با 09 شروع شود',
          'رمز عبور باید حداقل ۶ کاراکتر باشد'
        ],
        tips: [
          'پس از ورود، توکن احراز هویت به صورت خودکار در مرورگر ذخیره می‌شود',
          'توکن تا ۲۴ ساعت معتبر است'
        ],
        warnings: [
          'شماره تلفن باید یکتا باشد',
          'رمز عبور را فراموش نکنید'
        ],
        order: 1
      },
      {
        title: 'تعریف کودها در پایگاه داده',
        description: 'قبل از محاسبه کود، باید کودهای مورد نظر خود را در پایگاه داده تعریف کنید.',
        details: [
          'به تب "پایگاه داده کودها" بروید',
          'روی دکمه "افزودن کود جدید" کلیک کنید',
          'نام کود، قیمت هر کیلوگرم و درصد عناصر موجود در آن را وارد کنید',
          'برای بارگذاری نمونه‌های آماده، روی "بارگذاری نمونه" کلیک کنید'
        ],
        tips: [
          'می‌توانید کودهای اسیدی مانند H3PO4، HNO3 و H2SO4 را نیز تعریف کنید'
        ],
        warnings: [
          'درصد عناصر باید بین ۰ تا ۱۰۰ باشد',
          'مجموع درصد عناصر نباید از ۱۰۰ بیشتر شود'
        ],
        order: 2
      },
      {
        title: 'وارد کردن آنالیز آب',
        description: 'اطلاعات آنالیز آب و پساب خود را وارد کنید تا نرم‌افزار بتواند محاسبات دقیق انجام دهد.',
        details: [
          'درصد آب و پساب را در بخش بالایی وارد کنید (مثلاً ۸۰٪ آب و ۲۰٪ پساب)',
          'مقدار شوری آب را وارد کنید',
          'در جدول، مقادیر هر عنصر را برای آب و پساب به صورت مجزا وارد کنید',
          'ستون "مقادیر تامینی" به صورت خودکار محاسبه می‌شود'
        ],
        tips: [
          'واحدهای قابل انتخاب شامل PPM/L، MEQ/L و MMOLS/L هستند',
          'واحد پیش‌فرض PPM/L است'
        ],
        warnings: [],
        order: 3
      },
      {
        title: 'تعیین عناصر هدف',
        description: 'مقدار مورد نظر خود را برای هر عنصر غذایی تعیین کنید. نرم‌افزار تعادل یونی را به صورت خودکار بررسی می‌کند.',
        details: [
          'مقادیر مورد نظر خود را برای هر عنصر در جدول وارد کنید',
          'نرم‌افزار به صورت خودکار تعادل کاتیون و آنیون را محاسبه می‌کند',
          'اگر تعادل برقرار نباشد، پیام هشدار نمایش داده می‌شود',
          'با کلیک روی "اعمال تغییرات" مقادیر ذخیره می‌شوند'
        ],
        tips: [
          'عناصر قابل تنظیم: N-NO3، P، S، N-NH4، K، Ca، Mg، Na، Cl، Fe، Mn، Zn، B، Cu، Mo'
        ],
        warnings: [
          'اختلاف کاتیون و آنیون باید کمتر از ۰.۵ باشد تا تعادل برقرار شود'
        ],
        order: 4
      },
      {
        title: 'محاسبه خودکار مقدار کود',
        description: 'با انتخاب کودهای تعریف شده، نرم‌افزار به صورت خودکار مقدار دقیق هر کود را محاسبه می‌کند.',
        details: [
          'از لیست، کودهای مورد نظر خود را انتخاب کنید (با نگه‌داشتن Ctrl می‌توانید چند کود انتخاب کنید)',
          'روی دکمه "افزودن" کلیک کنید تا کودها به جدول محاسبه اضافه شوند',
          'حجم مخزن (لیتر) و ضریب رقیق‌سازی را وارد کنید',
          'برای هر کود، وزن (گرم) و خلوص (درصد) را وارد کنید',
          'روی دکمه "محاسبه" کلیک کنید'
        ],
        tips: [
          'اسیدها (H3PO4، HNO3، H2SO4) به صورت پیش‌فرض در جدول وجود دارند',
          'اسیدها قابل حذف نیستند'
        ],
        warnings: [],
        order: 5
      },
      {
        title: 'تفسیر داده‌ها و دریافت گزارش',
        description: 'پس از تکمیل محاسبات، نرم‌افزار یک تفسیر کامل از وضعیت تغذیه گیاه و توصیه‌های کودی ارائه می‌دهد.',
        details: [
          'اطمینان حاصل کنید که آنالیز آب و عناصر هدف را وارد کرده‌اید',
          'محاسبات کود را انجام داده باشید',
          'روی دکمه "تولید تفسیر" کلیک کنید'
        ],
        tips: [
          'با کلیک روی دکمه "چاپ گزارش" می‌توانید خروجی را پرینت بگیرید'
        ],
        warnings: [],
        order: 6
      }
    ];

    steps.forEach(step => addQuickStartStep(step));
  }

  // ===== Initialize =====
  initializeSampleFAQs();
  initializeQuickStartSteps();

  return {
    // State
    faqItems,
    quickStartSteps,
    searchQuery,
    activeCategory,
    
    // Getters
    filteredFAQs,
    sortedQuickStartSteps,
    categories,
    totalFAQs,
    totalQuickStartSteps,
    
    // Actions
    addFAQ,
    updateFAQ,
    deleteFAQ,
    addQuickStartStep,
    updateQuickStartStep,
    deleteQuickStartStep,
    setSearchQuery,
    setActiveCategory,
    clearSearch,
    resetCategories
  };
});