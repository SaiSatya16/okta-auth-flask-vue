<template>
    <div class="loading-container" :class="{ overlay: overlay }">
      <div class="spinner-container">
        <div class="spinner"></div>
        <p v-if="message" class="loading-message">{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingSpinner',
    props: {
      message: {
        type: String,
        default: 'Loading...'
      },
      overlay: {
        type: Boolean,
        default: false
      }
    }
  }
  </script>
  
  <style scoped>
  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
  }
  
  .loading-container.overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
  }
  
  .spinner-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: var(--card-background);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(66, 133, 244, 0.2);
    border-radius: 50%;
    border-top-color: var(--primary-color);
    animation: spin 1s linear infinite;
  }
  
  .loading-message {
    margin-top: 1rem;
    color: var(--text-color);
    font-weight: 500;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  </style>
  