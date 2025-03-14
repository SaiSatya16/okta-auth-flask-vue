<template>
  <div class="home">
    <h1>Welcome to Okta Auth App</h1>
    <div v-if="isLoggedIn">
      <p>You are logged in!</p>
      <router-link to="/profile">Go to Profile</router-link>
    </div>
    <div v-else>
      <p>Please log in to access your profile and MFA settings.</p>
      <router-link to="/login">Login</router-link> |
      <router-link to="/signup">Signup</router-link>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'HomeView',
  data() {
    return {
      isLoggedIn: false
    }
  },
  async created() {
    try {
      const response = await api.checkLoginStatus();
      this.isLoggedIn = response.data.loggedIn;
    } catch (error) {
      console.error('Error checking login status:', error);
    }
  }
}
</script>
