<template>
    <div class="signup">
      <h1>Create Account</h1>
      <form @submit.prevent="signup">
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
        
        <div class="form-group">
          <label for="subscription">Subscription</label>
          <select id="subscription" v-model="user.subscription">
            <option value="basic">Basic</option>
            <option value="premium">Premium</option>
            <option value="premium+">Premium+</option>
          </select>
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </template>
  
  <script>
  import api from '../services/api';
  
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
          this.$router.push('/login');
        } catch (error) {
          this.error = error.response?.data?.error || 'Failed to create account';
        } finally {
          this.loading = false;
        }
      }
    }
  }
  </script>
  