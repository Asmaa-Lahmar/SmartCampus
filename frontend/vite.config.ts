import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // En développement, /api est relayé vers l'API FastAPI (uvicorn sur le port 8000)
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
