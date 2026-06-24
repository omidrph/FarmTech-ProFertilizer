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
            <p class="text-sm text-gray-500 dark:text-gray-400">۰۲۱-۱۲۳۴۵۶۷۸</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">۰۹۱۰-۴۷۳-۹۷۱۸</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <div>
            <p class="font-medium">ایمیل</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">info@farmtech.ir</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">support@farmtech.ir</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3 text-gray-700 dark:text-gray-300 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <svg class="w-5 h-5 text-primary-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <div>
            <p class="font-medium">آدرس دفتر مرکزی</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">تهران، خیابان انقلاب، بین خیابان‌های وصال و قدس، پلاک ۱۲۳، طبقه ۳</p>
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
            <p class="text-sm text-gray-500 dark:text-gray-400">جمعه: تعطیل</p>
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
        <a href="#" target="_blank" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/>
          </svg>
        </a>
        <a href="#" target="_blank" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.104c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 0021.761-11.815c0-.25-.005-.5-.015-.75a9.97 9.97 0 002.46-2.548l-.047-.02z"/>
          </svg>
        </a>
        <a href="#" target="_blank" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
          </svg>
        </a>
        <a href="#" target="_blank" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
        </a>
        <a href="#" target="_blank" class="p-2.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors group">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
          </svg>
        </a>
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