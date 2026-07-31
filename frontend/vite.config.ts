// frontend/vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    host: true,  // ✅ برای Docker
    open: false  // ✅ باز نشدن خودکار در production
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,  // ✅ غیرفعال برای production
    minify: 'esbuild', // ✅ مینی‌فای کردن
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          vendor: ['axios']
        }
      }
    }
  },
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "@/assets/styles/fonts.css";`
      }
    }
  }
});