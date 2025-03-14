<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link> |
      <router-link v-if="!isLoggedIn" to="/signup">Signup</router-link> |
      <router-link v-if="isLoggedIn" to="/profile">Profile</router-link> |
      <a v-if="isLoggedIn" href="#" @click.prevent="logout">Logout</a>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import api from './services/api';

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false
    }
  },
  // In App.vue or where you check login status
async created() {
  try {
    const response = await api.checkLoginStatus();
    this.isLoggedIn = response.data.loggedIn;
    if (this.isLoggedIn) {
      // Store user info if needed
      this.userInfo = response.data.userInfo;
    }
  } catch (error) {
    console.error('Error checking login status:', error);
    this.isLoggedIn = false;
  }
}
,
  methods: {
    logout() {
      window.location.href = 'http://localhost:5000/logout';
    }
  }
}
</script>
