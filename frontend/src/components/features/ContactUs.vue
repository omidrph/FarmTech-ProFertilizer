<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
    <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-6 flex items-center gap-2">
      <svg class="w-6 h-6 sm:w-8 sm:h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
      </svg>
      ارتباط با ما
    </h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- اطلاعات تماس -->
      <div class="space-y-4">
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          <div>
            <p class="font-medium">تلفن تماس</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">۰۲۱-۸۸۴۱۴۶۷۹</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">۵-۰۹۹۸۱۹۱۱۳۸۲</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <div>
            <p class="font-medium">ایمیل</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">info@farmtech.ir</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <div>
            <p class="font-medium">آدرس</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">تهران، خیابان انقلاب، خیابان وصال شیرازی، کوچه شهید حامدی، پلاک ۵، واحد ۲</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <div>
            <p class="font-medium">ساعات کاری</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">شنبه تا چهارشنبه: ۸:۰۰ - ۱۷:۰۰</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">پنجشنبه: ۸:۰۰ - ۱۳:۰۰</p>
          </div>
        </div>
      </div>

      <!-- فرم تماس -->
      <div class="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">ارسال پیام</h3>
        
        <div v-if="submitStatus === 'success'" class="mb-4 bg-success-50 dark:bg-success-900/20 border-r-4 border-success-500 rounded-lg p-3">
          <p class="text-success-700 dark:text-success-400 text-sm">✅ پیام شما با موفقیت ارسال شد. به زودی با شما تماس گرفته می‌شود.</p>
          <button @click="submitStatus = ''" class="text-xs text-success-600 hover:text-success-800 mt-1">بستن</button>
        </div>
        
        <div v-if="submitStatus === 'error'" class="mb-4 bg-danger-50 dark:bg-danger-900/20 border-r-4 border-danger-500 rounded-lg p-3">
          <p class="text-danger-700 dark:text-danger-400 text-sm">❌ خطا در ارسال پیام. لطفاً دوباره تلاش کنید.</p>
          <button @click="submitStatus = ''" class="text-xs text-danger-600 hover:text-danger-800 mt-1">بستن</button>
        </div>

        <form @submit.prevent="submitContactForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              نام و نام خانوادگی <span class="text-danger-500">*</span>
            </label>
            <input 
              type="text" 
              v-model="form.name"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="نام و نام خانوادگی خود را وارد کنید"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              ایمیل <span class="text-danger-500">*</span>
            </label>
            <input 
              type="email" 
              v-model="form.email"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="ایمیل خود را وارد کنید"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              شماره تماس
            </label>
            <input 
              type="tel" 
              v-model="form.phone"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="شماره تماس خود را وارد کنید"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              موضوع <span class="text-danger-500">*</span>
            </label>
            <input 
              type="text" 
              v-model="form.subject"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="موضوع پیام"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              متن پیام <span class="text-danger-500">*</span>
            </label>
            <textarea 
              v-model="form.message"
              required
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              placeholder="متن پیام خود را وارد کنید..."
            ></textarea>
          </div>
          
          <button 
            type="submit"
            :disabled="isSubmitting"
            class="w-full px-4 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isSubmitting">ارسال پیام</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              در حال ارسال...
            </span>
          </button>
        </form>
      </div>
    </div>

    <!-- شبکه‌های اجتماعی -->
    <div class="border-t border-gray-200 dark:border-gray-700 pt-6 mt-6">
      <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 text-center">ما را در شبکه‌های اجتماعی دنبال کنید</h3>
      <div class="flex justify-center gap-4">
        <a href="https://www.instagram.com/farmtech.ir/" target="_blank" rel="noopener noreferrer" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-[#E4405F] transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
          </svg>
        </a>
        <a href="https://www.youtube.com/@farmtech" target="_blank" rel="noopener noreferrer" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-[#FF0000] transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
        </a>
        <a href="https://t.me/MJZafari_farmtech" target="_blank" rel="noopener noreferrer" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-[#0088cc] transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
          </svg>
        </a>
        <a href="https://wa.me/989981911384" target="_blank" rel="noopener noreferrer" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-[#25D366] transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
        </a>
      </div>
    </div>

    <!-- فوتر -->
    <div class="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-500 dark:text-gray-400">
        <div class="flex items-center gap-2">
          <span class="inline-block px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded text-[10px] font-medium">
            محصول دانش‌بنیان
          </span>
        </div>
        <p class="text-center">
          © ۱۴۰۱ – ۱۴۰۵ محصولی دانش‌بنیان از شرکت توسعه فناوری ستاره سهیل، تمامی حقوق محفوظ است.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useApi } from '@/composables/useApi';

// ===== API =====
const { request, isLoading: isSubmitting } = useApi();

// ===== Form =====
const form = reactive({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
});

const submitStatus = ref<'success' | 'error' | ''>('');

// ===== Submit =====
const submitContactForm = async () => {
  submitStatus.value = '';
  
  try {
    // ارسال به API واقعی
    const result = await request('post', '/contact', form);
    
    if (result) {
      submitStatus.value = 'success';
      // Reset form
      form.name = '';
      form.email = '';
      form.phone = '';
      form.subject = '';
      form.message = '';
      
      // Auto hide after 5 seconds
      setTimeout(() => {
        submitStatus.value = '';
      }, 5000);
    } else {
      submitStatus.value = 'error';
    }
  } catch (error) {
    console.error('Error sending contact form:', error);
    submitStatus.value = 'error';
    
    setTimeout(() => {
      submitStatus.value = '';
    }, 5000);
  }
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>