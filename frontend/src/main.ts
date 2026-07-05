// frontend/src/main.ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// Import styles
import './assets/styles/main.css';

// Import fonts
import './assets/styles/fonts.css';

// Import print styles (only for print)
import './assets/styles/print.css';

// 🆕 Import test (فقط در حالت development)
if (import.meta.env.DEV) {
  import('./test').then(() => {
    console.log('🧪 تست فرانت‌اند بارگذاری شد!');
    console.log('📝 برای اجرا: openTestRunner()');
  });
}

const app = createApp(App);

// Plugins
app.use(createPinia());
app.use(router);

// Mount
app.mount('#app');