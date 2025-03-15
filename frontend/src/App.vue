<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-logo">
          <router-link to="/">
            <span class="logo-text">Okta Auth App</span>
          </router-link>
        </div>
        
        <div class="navbar-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
          <router-link v-if="!isLoggedIn" to="/signup" class="nav-link">Signup</router-link>
          <router-link v-if="isLoggedIn" to="/profile" class="nav-link">Profile</router-link>
        </div>
        
        <div class="navbar-actions">
          <ThemeToggle />
          <button v-if="isLoggedIn" @click="logout" class="logout-btn">
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
    </main>
    
    <footer class="footer">
      <p>© 2025 Okta Auth App. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import ThemeToggle from './views/ThemeToggle.vue';
import api from './services/api';

export default {
  name: 'App',
  components: {
    ThemeToggle
  },
  data() {
    return {
      isLoggedIn: false
    }
  },
  async created() {
    try {
      const response = await api.checkLoginStatus();
      this.isLoggedIn = response.data.loggedIn;
      if (this.isLoggedIn) {
        this.userInfo = response.data.userInfo;
      }
    } catch (error) {
      console.error('Error checking login status:', error);
      this.isLoggedIn = false;
    }
  },
  methods: {
    async logout() {
      try {
        this.$store.commit('SET_AUTH_STATUS', false);
        this.$store.commit('SET_USER', null);
        window.location.href = 'http://localhost:5000/logout';
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
  }
}
</script>

<style>
/* Base styles */
:root {
  --background-color: #ffffff;
  --card-background: #f8f9fa;
  --text-color: #333333;
  --border-color: #dee2e6;
  --primary-color: #4285f4;
  --secondary-color: #34a853;
  --accent-color: #ea4335;
  --hover-color: rgba(66, 133, 244, 0.1);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
  --background-color: #121212;
  --card-background: #1e1e1e;
  --text-color: #e0e0e0;
  --border-color: #333333;
  --primary-color: #5c9aff;
  --secondary-color: #4cc265;
  --accent-color: #ff6b6b;
  --hover-color: rgba(92, 154, 255, 0.2);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar styles */
.navbar {
  background-color: var(--card-background);
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.navbar-logo a {
  text-decoration: none;
  color: var(--primary-color);
  font-weight: bold;
  font-size: 1.5rem;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  transition: color 0.3s;
}

.nav-link:hover {
  color: var(--primary-color);
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--primary-color);
  transition: width 0.3s;
}

.nav-link:hover::after,
.router-link-active::after {
  width: 100%;
}

.router-link-active {
  color: var(--primary-color);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #d03b2b;
}

/* Main content */
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 2rem auto;
  padding: 0 1rem;
}

/* Footer */
.footer {
  background-color: var(--card-background);
  padding: 1.5rem;
  text-align: center;
  margin-top: auto;
  transition: background-color 0.3s ease;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .navbar-links {
    width: 100%;
    justify-content: center;
  }
  
  .navbar-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>
