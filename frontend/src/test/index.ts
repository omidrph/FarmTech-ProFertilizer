// frontend/src/test/index.ts
import { createApp } from 'vue';
import TestRunner from './TestRunner.vue';

let testApp: any = null;
let container: HTMLElement | null = null;

export function openTestRunner() {
  // اگر قبلاً باز است، ببند
  if (testApp) {
    testApp.unmount();
    testApp = null;
  }
  
  if (container) {
    container.remove();
    container = null;
  }
  
  // ایجاد یک المنت برای تست
  container = document.createElement('div');
  container.id = 'test-runner-container';
  document.body.appendChild(container);
  
  testApp = createApp(TestRunner, {
    isOpen: true,
    'onUpdate:isOpen': (value: boolean) => {
      if (!value) {
        if (testApp) {
          testApp.unmount();
          testApp = null;
        }
        if (container) {
          container.remove();
          container = null;
        }
      }
    }
  });
  
  testApp.mount(container);
}

// اضافه کردن به window برای دسترسی آسان
(window as any).openTestRunner = openTestRunner;

console.log('🧪 تست فرانت‌اند آماده است!');
console.log('📝 برای اجرا در کنسول تایپ کنید: openTestRunner()');