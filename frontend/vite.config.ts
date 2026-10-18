
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],

  server: {
    proxy: {
      '/requests': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/orders': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/inventory': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/suppliers': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/policies': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
