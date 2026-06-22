// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/views/MainLayout.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'home',
      component: MainLayout,
      meta: { requiresAuth: true }
    }
  ]
});

// ===== Navigation Guard (محافظت از مسیرها) =====
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token');
  const isAuthenticated = !!token;

  // اگر مسیر نیاز به احراز هویت دارد و کاربر لاگین نیست
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
    return;
  }

  // اگر کاربر لاگین است و به صفحه لاگین یا ثبت‌نام می‌رود
  if (isAuthenticated && (to.path === '/login' || to.path === '/register')) {
    next('/');
    return;
  }

  next();
});

export default router;