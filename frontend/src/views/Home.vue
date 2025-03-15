<template>
  <div class="home-container">
    <div class="home-content">
      <h1 class="home-title">Welcome to Okta Auth App</h1>
      <p class="home-description">Secure authentication with multi-factor options</p>
      
      <div class="home-cards">
        <div class="feature-card">
          <div class="icon-container">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <h3>Secure Authentication</h3>
          <p>Login securely with Okta's enterprise-grade authentication</p>
        </div>
        
        <div class="feature-card">
          <div class="icon-container">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <h3>Multi-Factor Auth</h3>
          <p>Add extra layers of security with multiple authentication factors</p>
        </div>
        
        <div class="feature-card">
          <div class="icon-container">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
          </div>
          <h3>User Management</h3>
          <p>Easy profile management and subscription options</p>
        </div>
      </div>
      
      <div class="home-actions">
        <div v-if="isLoggedIn" class="action-container">
          <p>You are logged in as a user!</p>
          <router-link to="/profile" class="action-button primary">Go to Profile</router-link>
        </div>
        <div v-else class="action-container">
          <p>Please log in to access your profile and MFA settings.</p>
          <div class="button-group">
            <router-link to="/login" class="action-button primary">Login</router-link>
            <router-link to="/signup" class="action-button secondary">Sign Up</router-link>
          </div>
        </div>
      </div>
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

<style scoped>
.home-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.home-content {
  text-align: center;
}

.home-title {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.home-description {
  font-size: 1.2rem;
  color: var(--text-color);
  opacity: 0.8;
  margin-bottom: 3rem;
}

.home-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  margin-bottom: 3rem;
}

.feature-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  flex: 1;
  min-width: 250px;
  max-width: 350px;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.icon-container {
  background-color: var(--hover-color);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.icon-container svg {
  color: var(--primary-color);
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: var(--text-color);
}

.feature-card p {
  color: var(--text-color);
  opacity: 0.8;
}

.home-actions {
  margin-top: 3rem;
}

.action-container {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: var(--shadow);
}

.action-container p {
  margin-bottom: 1.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.action-button {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s;
}

.action-button.primary {
  background-color: var(--primary-color);
  color: white;
}

.action-button.primary:hover {
  background-color: #3b78e7;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-button.secondary {
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.action-button.secondary:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .home-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-card {
    max-width: 100%;
  }
  
  .button-group {
    flex-direction: column;
  }
}
</style>
