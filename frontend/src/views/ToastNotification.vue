<template>
    <transition name="toast">
      <div v-if="visible" class="toast" :class="type">
        <div class="toast-icon">
          <svg v-if="type === 'success'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <svg v-else-if="type === 'error'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
        <div class="toast-content">
          <p>{{ message }}</p>
        </div>
        <button class="toast-close" @click="close">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    name: 'ToastNotification',
    props: {
      message: {
        type: String,
        required: true
      },
      type: {
        type: String,
        default: 'info',
        validator: (value) => ['success', 'error', 'info', 'warning'].includes(value)
      },
      duration: {
        type: Number,
        default: 3000
      }
    },
    data() {
      return {
        visible: true,
        timeout: null
      }
    },
    mounted() {
      this.timeout = setTimeout(() => {
        this.visible = false;
      }, this.duration);
    },
    beforeUnmount() {
      clearTimeout(this.timeout);
    },
    methods: {
      close() {
        this.visible = false;
      }
    }
  }
  </script>
  
  <style scoped>
  .toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-width: 350px;
    z-index: 9999;
    animation: slideIn 0.3s ease-out;
  }
  
  .toast.success {
    background-color: #d4edda;
    color: #155724;
  }
  
  .toast.error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .toast.info {
    background-color: #d1ecf1;
    color: #0c5460;
  }
  
  .toast.warning {
    background-color: #fff3cd;
    color: #856404;
  }
  
  .toast-icon {
    margin-right: 0.8rem;
    display: flex;
    align-items: center;
  }
  
  .toast-content {
    flex: 1;
  }
  
  .toast-content p {
    margin: 0;
  }
  
  .toast-close {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.3rem;
    margin-left: 0.8rem;
    opacity: 0.6;
    transition: opacity 0.3s;
  }
  
  .toast-close:hover {
    opacity: 1;
  }
  
  .toast-enter-active, .toast-leave-active {
    transition: all 0.3s ease;
  }
  
  .toast-enter-from, .toast-leave-to {
    opacity: 0;
    transform: translateX(30px);
  }
  
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
  }
  </style>
  