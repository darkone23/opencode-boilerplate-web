import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 43210,
    proxy: {
      '/api': {
        target: 'http://localhost:43280',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
})
