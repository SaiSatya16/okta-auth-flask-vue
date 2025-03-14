// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

// In vue.config.js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/login': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/oidc': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/logout': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}
