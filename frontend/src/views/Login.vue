<template>
    <div class="login">
      <h1>Login</h1>
      <button @click="login" class="login-button">Login with Okta</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginView',
    methods: {
     // In your Vue frontend
async login() {
  try {
    window.location.href = 'http://localhost:5000/login';
  } catch (error) {
    console.error('Login error:', error);
    // If error contains "not allowed to access this app", retry after a short delay
    if (error.toString().includes('not allowed to access this app')) {
      setTimeout(() => {
        window.location.href = 'http://localhost:5000/login';
      }, 2000);
    }
  }
}
,
    }
  }
  </script>
  