<template>
    <div class="profile" v-if="profile">
    <h1>Your Profile</h1>
    
    <div v-if="!editing">
      <div class="profile-info">
        <p><strong>Name:</strong> {{ profile.firstName }} {{ profile.lastName }}</p>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>Subscription:</strong> {{ profile.subscription }}</p>
        <p><strong>Source:</strong> {{ profile.source }}</p>
        
        <!-- Show additional details if they exist -->
        <div v-if="hasAdditionalDetails" class="additional-details">
          <h3>Additional Details</h3>
          <p v-if="profile.mobilePhone"><strong>Mobile Phone:</strong> {{ profile.mobilePhone }}</p>
          <p v-if="profile.secondEmail"><strong>Secondary Email:</strong> {{ profile.secondEmail }}</p>
          <p v-if="profile.city"><strong>City:</strong> {{ profile.city }}</p>
          <p v-if="profile.state"><strong>State:</strong> {{ profile.state }}</p>
          <p v-if="profile.countryCode"><strong>Country Code:</strong> {{ profile.countryCode }}</p>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="editing = true" class="edit-button">Edit Profile</button>
        <button @click="showAdditionalFields = !showAdditionalFields" class="details-button">
          {{ showAdditionalFields ? 'Hide Additional Details' : 'Add More Details' }}
        </button>
      </div>
      
      <!-- Additional fields form when not in edit mode -->
      <div v-if="showAdditionalFields && !editing" class="additional-fields-form slide-up">
        <h3>Additional Details</h3>
        <form @submit.prevent="updateAdditionalDetails">
          <div class="form-group">
            <label for="mobilePhone">Mobile Phone</label>
            <input type="tel" id="mobilePhone" v-model="additionalDetails.mobilePhone">
          </div>
          
          <div class="form-group">
            <label for="secondEmail">Secondary Email</label>
            <input type="email" id="secondEmail" v-model="additionalDetails.secondEmail">
          </div>
          
          <div class="form-group">
            <label for="city">City</label>
            <input type="text" id="city" v-model="additionalDetails.city">
          </div>
          
          <div class="form-group">
            <label for="state">State</label>
            <input type="text" id="state" v-model="additionalDetails.state">
          </div>
          
          <div class="form-group">
            <label for="countryCode">Country Code</label>
            <select id="countryCode" v-model="additionalDetails.countryCode">
              <option value="">Select Country</option>
              <option value="US">United States</option>
              <option value="CA">Canada</option>
              <option value="UK">United Kingdom</option>
              <option value="AU">Australia</option>
              <option value="IN">India</option>
              <!-- Add more countries as needed -->
            </select>
          </div>
          
          <div class="form-actions">
            <button type="submit" :disabled="updatingDetails">
              {{ updatingDetails ? 'Saving...' : 'Save Details' }}
            </button>
            <button type="button" @click="showAdditionalFields = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Main edit form -->
    <form v-else @submit.prevent="updateProfile" class="edit-form">
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="text" id="firstName" v-model="editForm.firstName">
      </div>
      
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input type="text" id="lastName" v-model="editForm.lastName">
      </div>
      
      <!-- Include additional fields in the main edit form -->
      <div class="additional-fields">
        <h3>Additional Details</h3>
        
        <div class="form-group">
          <label for="editMobilePhone">Mobile Phone</label>
          <input type="tel" id="editMobilePhone" v-model="editForm.mobilePhone">
        </div>
        
        <div class="form-group">
          <label for="editsecondEmail">Secondary Email</label>
          <input type="email" id="editsecondEmail" v-model="editForm.secondEmail">
        </div>
        
        <div class="form-group">
          <label for="editCity">City</label>
          <input type="text" id="editCity" v-model="editForm.city">
        </div>
        
        <div class="form-group">
          <label for="editState">State</label>
          <input type="text" id="editState" v-model="editForm.state">
        </div>
        
        <div class="form-group">
          <label for="editCountryCode">Country Code</label>
          <select id="editCountryCode" v-model="editForm.countryCode">
            <option value="">Select Country</option>
            <option value="US">United States</option>
            <option value="CA">Canada</option>
            <option value="UK">United Kingdom</option>
            <option value="AU">Australia</option>
            <option value="IN">India</option>
            <!-- Add more countries as needed -->
          </select>
        </div>
      </div>
      
      <div class="form-actions">
        <button type="submit" :disabled="updating">Save</button>
        <button type="button" @click="cancelEdit">Cancel</button>
      </div>
    </form>
    
    <div class="subscription-section">
      <h2>Subscription Management</h2>
      <p>Your current subscription: <strong>{{ profile.subscription }}</strong></p>
      
      <div class="subscription-plans">
        <div class="plan" :class="{ 'current': profile.subscription === 'basic' }">
          <h3>Basic Plan</h3>
          <p class="price">Free</p>
          <ul class="benefits">
            <li>Okta Verify authentication</li>
          </ul>
          <button v-if="profile.subscription !== 'basic'" 
                  @click="updateSubscription('basic')"
                  :disabled="updating">
            Select Plan
          </button>
          <span v-else class="current-plan">Current Plan</span>
        </div>
        
        <div class="plan" :class="{ 'current': profile.subscription === 'premium' }">
          <h3>Premium Plan</h3>
          <p class="price">$10/month</p>
          <ul class="benefits">
            <li>Okta Verify authentication</li>
            <li>Google Authenticator support</li>
          </ul>
          <button v-if="profile.subscription !== 'premium'" 
                  @click="updateSubscription('premium')"
                  :disabled="updating">
            Upgrade Now
          </button>
          <span v-else class="current-plan">Current Plan</span>
        </div>
        
        <div class="plan" :class="{ 'current': profile.subscription === 'premium+' }">
          <h3>Premium+ Plan</h3>
          <p class="price">$20/month</p>
          <ul class="benefits">
            <li>Okta Verify authentication</li>
            <li>Google Authenticator support</li>
            <li>Phone Authentication</li>
          </ul>
          <button v-if="profile.subscription !== 'premium+'" 
                  @click="updateSubscription('premium+')"
                  :disabled="updating">
            Upgrade Now
          </button>
          <span v-else class="current-plan">Current Plan</span>
        </div>
      </div>
    </div>
    
    <div class="mfa-section">
      <h2>Multi-Factor Authentication</h2>
      
      <div v-if="refreshingMfa" class="mfa-loading">
        <p>Refreshing available MFA options...</p>
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="mfa.available.length > 0">
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
  <LoadingSpinner v-else message="Loading profile..." />

</template>

<script>
import api from '../services/api';
import toast from '../services/toast';
import LoadingSpinner from '../views/LoadingSpinner.vue';
export default {
  name: 'ProfileView',
  components: {
    LoadingSpinner
  },
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
        subscription: '',
        mobilePhone: '',
        secondEmail: '',
        city: '',
        state: '',
        countryCode: ''
      },
      additionalDetails: {
        mobilePhone: '',
        secondEmail: '',
        city: '',
        state: '',
        countryCode: ''
      },
      showAdditionalFields: false,
      updating: false,
      updatingDetails: false,
      enrolling: null,
      error: null,
      refreshingMfa: false,
    }},
    computed: {
    hasAdditionalDetails() {
      return this.profile && (
        this.profile.mobilePhone || 
        this.profile.secondEmail || 
        this.profile.city || 
        this.profile.state || 
        this.profile.countryCode
      );
    }
  },
  async created() {
    try {
      const response = await api.getProfile();
      this.profile = response.data.profile;
      this.mfa = response.data.mfa;
      
      // Initialize edit form with all fields
      this.initializeEditForm();
      
      // Initialize additional details form
      this.initializeAdditionalDetails();
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
        
        // Update local profile data with all fields
        this.profile.firstName = this.editForm.firstName;
        this.profile.lastName = this.editForm.lastName;
        this.profile.subscription = this.editForm.subscription;
        this.profile.mobilePhone = this.editForm.mobilePhone;
        this.profile.secondEmail = this.editForm.secondEmail;
        this.profile.city = this.editForm.city;
        this.profile.state = this.editForm.state;
        this.profile.countryCode = this.editForm.countryCode;
        
        // Exit edit mode
        this.editing = false;
        toast.success('Profile updated successfully');
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update profile';
        toast.error(this.error);
      } finally {
        this.updating = false;
      }
    },
    
    async updateAdditionalDetails() {
      this.updatingDetails = true;
      this.error = null;
      
      try {
        // Create an update object that includes only the additional details
        const updateData = {
          firstName: this.profile.firstName,
          lastName: this.profile.lastName,
          subscription: this.profile.subscription,
          ...this.additionalDetails
        };
        
        await api.updateProfile(updateData);
        
        // Update local profile data with additional details
        this.profile.mobilePhone = this.additionalDetails.mobilePhone;
        this.profile.secondEmail = this.additionalDetails.secondEmail;
        this.profile.city = this.additionalDetails.city;
        this.profile.state = this.additionalDetails.state;
        this.profile.countryCode = this.additionalDetails.countryCode;
        
        // Hide the additional fields form
        this.showAdditionalFields = false;
        toast.success('Additional details updated successfully');
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update additional details';
        toast.error(this.error);
      } finally {
        this.updatingDetails = false;
      }
    },
    
    async updateSubscription(newSubscription) {
      this.updating = true;
      this.error = null;
      this.editForm = {
        firstName: this.profile.firstName,
        lastName: this.profile.lastName,
        subscription: newSubscription
      };
      
      try {
        await api.updateProfile(this.editForm);
        
        // Update local profile data
        this.profile.subscription = newSubscription;
        
        this.refreshingMfa = true;
        // Add a small delay before refreshing MFA options to allow Okta to process the update
        toast.success('Profile updated successfully');
        setTimeout(async () => {
          await this.refreshMfaOptions();
          this.refreshingMfa = false;
        }, 1000);
      } catch (error) {
        toast.error(error.response?.data?.error || 'Failed to update subscription');
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
      this.error = null;
      try {
        // First check if user is still authenticated
        const authStatus = await api.checkLoginStatus();
        if (!authStatus.data.loggedIn) {
          // Redirect to login if not authenticated
          window.location.href = 'http://localhost:5000/login';
          return;
        }
        
        const response = await api.getMfaFactors();
        this.mfa.available = response.data.available_factors;
        this.mfa.enrolled = response.data.enrolled_factors || [];
      } catch (error) {
        console.error('Failed to refresh MFA options:', error);
        if (error.response && error.response.status === 400) {
          // If session expired, redirect to login
          if (error.response.data.error && error.response.data.error.includes('session')) {
            window.location.href = 'http://localhost:5000/login';
            return;
          }
          this.error = 'Failed to load MFA options. Please try logging in again.';
        }
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
    },

    initializeEditForm() {
      this.editForm = {
        firstName: this.profile.firstName || '',
        lastName: this.profile.lastName || '',
        subscription: this.profile.subscription || 'basic',
        mobilePhone: this.profile.mobilePhone || '',
        secondEmail: this.profile.secondEmail || '',
        city: this.profile.city || '',
        state: this.profile.state || '',
        countryCode: this.profile.countryCode || ''
      };
    },
    
    initializeAdditionalDetails() {
      this.additionalDetails = {
        mobilePhone: this.profile.mobilePhone || '',
        secondEmail: this.profile.secondEmail || '',
        city: this.profile.city || '',
        state: this.profile.state || '',
        countryCode: this.profile.countryCode || ''
      };
    },
    cancelEdit() {
      this.editing = false;
      this.initializeEditForm();
    },
  }
}
</script>

<style scoped>
.profile {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

h1 {
  color: var(--primary-color);
  margin-bottom: 2rem;
  text-align: center;
  font-size: 2rem;
}

h2 {
  color: var(--text-color);
  margin: 2rem 0 1rem;
  font-size: 1.5rem;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.profile-info {
  background-color: var(--card-background);
  margin-bottom: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.profile-info p {
  margin-bottom: 0.8rem;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.8rem;
}

.profile-info p:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

button {
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

button[type="submit"] {
  background-color: var(--primary-color);
  color: white;
}

button[type="submit"]:hover:not(:disabled) {
  background-color: #3b78e7;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

button[type="button"] {
  background-color: var(--card-background);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

button[type="button"]:hover {
  background-color: var(--hover-color);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.subscription-section, .mfa-section {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.subscription-plans {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.plan {
  flex: 1;
  min-width: 220px;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid var(--border-color);
  text-align: center;
  transition: all 0.3s ease;
}

.plan:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.plan.current {
  border-color: var(--primary-color);
  background-color: var(--hover-color);
}

.plan h3 {
  margin-top: 0;
  color: var(--primary-color);
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  margin: 1rem 0;
}

.benefits {
  text-align: left;
  margin: 1.5rem 0;
  padding-left: 1.5rem;
}

.benefits li {
  margin-bottom: 0.8rem;
  position: relative;
}

.benefits li::before {
  content: "✓";
  color: var(--secondary-color);
  position: absolute;
  left: -1.2rem;
  font-weight: bold;
}

.current-plan {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border-radius: 4px;
  font-weight: 500;
}

.mfa-section ul {
  list-style: none;
  padding: 0;
}

.mfa-section li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.mfa-section li:last-child {
  border-bottom: none;
}

.enrolled {
  background-color: var(--secondary-color);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.error {
  background-color: rgba(234, 67, 53, 0.1);
  color: var(--accent-color);
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1.5rem;
  text-align: center;
}

.loading, .mfa-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.spinner {
  border: 4px solid rgba(66, 133, 244, 0.1);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 1.5rem auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.profile-card {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 2rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.tab-navigation {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.tab {
  padding: 1rem 1.5rem;
  cursor: pointer;
  position: relative;
  font-weight: 500;
  color: var(--text-color);
  opacity: 0.7;
  transition: all 0.3s ease;
}

.tab.active {
  color: var(--primary-color);
  opacity: 1;
}

.tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 3px;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

.tab.active::after {
  width: 100%;
}

.tab:hover {
  opacity: 1;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
}

.badge-premium {
  background-color: var(--primary-color);
  color: white;
}

.badge-basic {
  background-color: var(--border-color);
  color: var(--text-color);
}

.badge-premium-plus {
  background-color: var(--accent-color);
  color: white;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.edit-button, .details-button {
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.details-button {
  background-color: var(--card-background);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.edit-button:hover {
  background-color: #3b78e7;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.details-button:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
}

.additional-fields-form {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
}

.additional-details {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.additional-details h3 {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.slide-up {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

