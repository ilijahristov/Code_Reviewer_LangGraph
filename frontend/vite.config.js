import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The dev server proxies API calls to the FastAPI backend on :8000,
// so the frontend can use relative URLs and avoid CORS during development.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/review': 'http://127.0.0.1:8000',
      '/repositories': 'http://127.0.0.1:8000',
    },
  },
})
