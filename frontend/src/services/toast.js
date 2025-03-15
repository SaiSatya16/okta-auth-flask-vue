import { createApp } from 'vue';
import ToastNotification from '../views/ToastNotification.vue';

const toast = {
  show(message, type = 'info', duration = 3000) {
    const mountPoint = document.createElement('div');
    document.body.appendChild(mountPoint);
    
    const toastApp = createApp(ToastNotification, {
      message,
      type,
      duration,
      onClose: () => {
        toastApp.unmount();
        document.body.removeChild(mountPoint);
      }
    });
    
    toastApp.mount(mountPoint);
    
    setTimeout(() => {
      toastApp.unmount();
      document.body.removeChild(mountPoint);
    }, duration + 300); // Add a little extra time for the animation
  },
  
  success(message, duration) {
    this.show(message, 'success', duration);
  },
  
  error(message, duration) {
    this.show(message, 'error', duration);
  },
  
  info(message, duration) {
    this.show(message, 'info', duration);
  },
  
  warning(message, duration) {
    this.show(message, 'warning', duration);
  }
};

export default toast;
