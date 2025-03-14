import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import LoginView from '../views/Login.vue';
import SignupView from '../views/Signup.vue';
import ProfileView from '../views/Profile.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: {
      requiresAuth: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Navigation guard
// In router/index.js
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      const response = await fetch('http://localhost:5000/api/login-status', {
        credentials: 'include'
      });
      const data = await response.json();
      
      if (!data.loggedIn) {
        window.location.href = 'http://localhost:5000/login';
        return;
      }
      next();
    } catch (error) {
      console.error('Auth check failed:', error);
      next('/login');
    }
  } else {
    next();
  }
});



export default router;
