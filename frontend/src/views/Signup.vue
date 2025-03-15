<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1 class="signup-title">Create Account</h1>
      <form @submit.prevent="signup" class="signup-form">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input type="text" id="firstName" v-model="user.firstName" required>
        </div>
        
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input type="text" id="lastName" v-model="user.lastName" required>
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="user.email" required>
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="user.password" required>
        </div>
        
        <button type="submit" :disabled="loading" class="signup-button">
          <span v-if="loading" class="spinner"></span>
          <span>{{ loading ? 'Creating Account...' : 'Sign Up' }}</span>
        </button>
        
        <div v-if="error" class="error-message">{{ error }}</div>
      </form>
      
      <div class="signup-footer">
        Already have an account? <router-link to="/login">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';
import toast from '../services/toast';
export default {
  name: 'SignupView',
  data() {
    return {
      user: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        subscription: 'basic'
      },
      loading: false,
      error: null
    }
  },
  methods: {
    async signup() {
      this.loading = true;
      this.error = null;
      
      try {
        await api.signup(this.user);
        toast.success('Account created successfully');
        this.$router.push('/login');
      } catch (error) {
        toast.error(error.response?.data?.error || 'Failed to create account');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.signup-container {
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

.signup-card {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 2.5rem;
  width: 100%;
  max-width: 500px;
  transition: all 0.3s ease;
}

.signup-title {
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.8rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.signup-button {
  margin-top: 1rem;
  padding: 0.8rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.signup-button:hover:not(:disabled) {
  background-color: #3b78e7;
}

.signup-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: var(--accent-color);
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: center;
}

.signup-footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.signup-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.signup-footer a:hover {
  text-decoration: underline;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
