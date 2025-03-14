import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  // Auth
  checkLoginStatus() {
    return apiClient.get('/login-status');
  },
  
  // User
  signup(userData) {
    return apiClient.post('/signup', userData);
  },
  
  getProfile() {
    return apiClient.get('/profile');
  },
  
  updateProfile(profileData) {
    return apiClient.put('/profile', profileData);
  },
  
  // MFA
  getMfaFactors() {
    return apiClient.get('/mfa');
  },
  
  enrollFactor(factorType) {
    return apiClient.post('/mfa', { factor_type: factorType });
  }
};
