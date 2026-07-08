// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/views/MainLayout.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import ForgotPassword from '@/views/ForgotPassword.vue';

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
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword,
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

// ===== Navigation Guard =====
router.beforeEach(async (to, from, next) => {
  // بررسی توکن از Cookie
  const getTokenFromCookie = (): string | null => {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'access_token') {
        return value;
      }
    }
    return null;
  };

  const token = getTokenFromCookie() || localStorage.getItem('access_token');
  const isAuthenticated = !!token;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
    return;
  }

  if (isAuthenticated && (to.path === '/login' || to.path === '/register' || to.path === '/forgot-password')) {
    next('/');
    return;
  }

  next();
});

export default router;