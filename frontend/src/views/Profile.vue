<template>
    <div class="profile" v-if="profile">
      <h1>Your Profile</h1>
      
      <div v-if="!editing">
        <div class="profile-info">
          <p><strong>Name:</strong> {{ profile.firstName }} {{ profile.lastName }}</p>
          <p><strong>Email:</strong> {{ profile.email }}</p>
          <p><strong>Subscription:</strong> {{ profile.subscription }}</p>
          <p><strong>Source:</strong> {{ profile.source }}</p>
        </div>
        
        <button @click="editing = true">Edit Profile</button>
      </div>
      
      <form v-else @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input type="text" id="firstName" v-model="editForm.firstName">
        </div>
        
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input type="text" id="lastName" v-model="editForm.lastName">
        </div>
        
        <div class="form-group">
          <label for="subscription">Subscription</label>
          <select id="subscription" v-model="editForm.subscription">
            <option value="basic">Basic</option>
            <option value="premium">Premium</option>
            <option value="premium+">Premium+</option>
          </select>
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="updating">Save</button>
          <button type="button" @click="editing = false">Cancel</button>
        </div>
      </form>
      
      <div class="mfa-section">
        <h2>Multi-Factor Authentication</h2>
        
        <div v-if="mfa.available.length > 0">
          <p>Available factors for your subscription:</p>
          <ul>
            <li v-for="factor in mfa.available" :key="factor">
              {{ getFriendlyFactorName(factor) }}
              <button 
                v-if="!isFactorEnrolled(factor)" 
                @click="enrollFactor(factor)"
                :disabled="enrolling === factor"
              >
                {{ enrolling === factor ? 'Enrolling...' : 'Enroll' }}
              </button>
              <span v-else class="enrolled">Enrolled</span>
            </li>
          </ul>
        </div>
        
        <div v-else>
          <p>No MFA factors available for your subscription level.</p>
        </div>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
    </div>
    <div v-else class="loading">
      Loading profile...
    </div>
  </template>
  
  <script>
  import api from '../services/api';
  
  export default {
    name: 'ProfileView',
    data() {
      return {
        profile: null,
        mfa: {
          available: [],
          enrolled: []
        },
        editing: false,
        editForm: {
          firstName: '',
          lastName: '',
          subscription: ''
        },
        updating: false,
        enrolling: null,
        error: null
      }
    },
    async created() {
      try {
        const response = await api.getProfile();
        this.profile = response.data.profile;
        this.mfa = response.data.mfa;
        
        // Initialize edit form
        this.editForm = {
          firstName: this.profile.firstName,
          lastName: this.profile.lastName,
          subscription: this.profile.subscription
        };
      } catch (error) {
        this.error = 'Failed to load profile data';
        console.error(error);
      }
    },
    methods: {
      async updateProfile() {
        this.updating = true;
        this.error = null;
        
        try {
          await api.updateProfile(this.editForm);
          
          // Update local profile data
          this.profile.firstName = this.editForm.firstName;
          this.profile.lastName = this.editForm.lastName;
          this.profile.subscription = this.editForm.subscription;
          
          // Exit edit mode
          this.editing = false;
          
          // If subscription changed, refresh MFA options
          await this.refreshMfaOptions();
        } catch (error) {
          this.error = error.response?.data?.error || 'Failed to update profile';
        } finally {
          this.updating = false;
        }
      },
      
      async enrollFactor(factorType) {
        this.enrolling = factorType;
        this.error = null;
        
        try {
          await api.enrollFactor(factorType);
          
          // Add to enrolled factors
          this.mfa.enrolled.push(factorType);
        } catch (error) {
          this.error = error.response?.data?.error || `Failed to enroll in ${this.getFriendlyFactorName(factorType)}`;
        } finally {
          this.enrolling = null;
        }
      },
      
      async refreshMfaOptions() {
        try {
          const response = await api.getMfaFactors();
          this.mfa.available = response.data.available_factors;
        } catch (error) {
          console.error('Failed to refresh MFA options:', error);
        }
      },
      
      isFactorEnrolled(factor) {
        return this.mfa.enrolled.includes(factor);
      },
      
      getFriendlyFactorName(factor) {
        const names = {
          'oktaverify': 'Okta Verify',
          'google': 'Google Authenticator',
          'phone': 'Phone Authentication'
        };
        
        return names[factor] || factor;
      }
    }
  }
  </script>
  
  <style scoped>
  .profile {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .profile-info {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-actions {
    margin-top: 20px;
  }
  
  button {
    padding: 8px 16px;
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .mfa-section {
    margin-top: 30px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .enrolled {
    color: green;
    font-weight: bold;
    margin-left: 10px;
  }
  
  .error {
    color: red;
    margin-top: 15px;
  }
  
  .loading {
    text-align: center;
    padding: 30px;
  }
  </style>
  