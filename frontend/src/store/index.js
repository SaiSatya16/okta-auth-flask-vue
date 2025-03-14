import { createStore } from 'vuex';
import api from '../services/api';

export default createStore({
  state: {
    user: null,
    mfa: {
      available: [],
      enrolled: []
    },
    isAuthenticated: false,
    loading: false,
    error: null
  },
  
  getters: {
    user: state => state.user,
    mfa: state => state.mfa,
    isAuthenticated: state => state.isAuthenticated,
    loading: state => state.loading,
    error: state => state.error
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_MFA(state, mfa) {
      state.mfa = mfa;
    },
    SET_AUTH_STATUS(state, status) {
      state.isAuthenticated = status;
    },
    SET_LOADING(state, status) {
      state.loading = status;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    ADD_ENROLLED_FACTOR(state, factor) {
      if (!state.mfa.enrolled.includes(factor)) {
        state.mfa.enrolled.push(factor);
      }
    }
  },
  
  actions: {
    async checkAuth({ commit }) {
      try {
        const response = await api.checkLoginStatus();
        commit('SET_AUTH_STATUS', response.data.loggedIn);
        return response.data.loggedIn;
      } catch (error) {
        commit('SET_AUTH_STATUS', false);
        return false;
      }
    },
    
    async fetchUserProfile({ commit }) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await api.getProfile();
        commit('SET_USER', response.data.profile);
        commit('SET_MFA', response.data.mfa);
      } catch (error) {
        commit('SET_ERROR', 'Failed to load user profile');
        console.error(error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async updateProfile({ commit }, profileData) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        await api.updateProfile(profileData);
        commit('SET_USER', { ...this.state.user, ...profileData });
        return true;
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to update profile';
        commit('SET_ERROR', errorMsg);
        return false;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async enrollFactor({ commit }, factorType) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        await api.enrollFactor(factorType);
        commit('ADD_ENROLLED_FACTOR', factorType);
        return true;
      } catch (error) {
        const errorMsg = error.response?.data?.error || `Failed to enroll in ${factorType}`;
        commit('SET_ERROR', errorMsg);
        return false;
      } finally {
        commit('SET_LOADING', false);
      }
    }
  }
});
