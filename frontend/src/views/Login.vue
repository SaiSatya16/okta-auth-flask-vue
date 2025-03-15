<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">Welcome Back</h1>
      <p class="login-subtitle">Sign in to access your account</p>
      
      <button @click="login" class="login-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
          <polyline points="10 17 15 12 10 7"></polyline>
          <line x1="15" y1="12" x2="3" y2="12"></line>
        </svg>
        <span>Login with Okta</span>
      </button>
      
      <div class="login-footer">
        Don't have an account? <router-link to="/signup">Sign up</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  methods: {
    async login() {
      try {
        window.location.href = 'http://localhost:5000/login';
      } catch (error) {
        console.error('Login error:', error);
        if (error.toString().includes('not allowed to access this app')) {
          setTimeout(() => {
            window.location.href = 'http://localhost:5000/login';
          }, 2000);
        }
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.login-card {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
  transition: all 0.3s ease;
}

.login-title {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}

.login-subtitle {
  color: var(--text-color);
  margin-bottom: 2rem;
  opacity: 0.8;
}

.login-button {
  width: 100%;
  padding: 0.8rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.8rem;
}

.login-button:hover {
  background-color: #3b78e7;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  margin-top: 2rem;
  font-size: 0.9rem;
}

.login-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
