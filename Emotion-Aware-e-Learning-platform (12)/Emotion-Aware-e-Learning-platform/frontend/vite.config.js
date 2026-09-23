import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

// __dirname is not available in ES modules — reconstruct it
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendHost = env.VITE_BACKEND_HOST || 'localhost'

  // Load self-signed cert from certs/ folder (needed for camera on LAN)
  let httpsConfig = undefined
  const certPath = resolve(__dirname, 'certs/localhost-cert.pem')
  const keyPath  = resolve(__dirname, 'certs/localhost-key.pem')
  if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
    httpsConfig = { cert: fs.readFileSync(certPath), key: fs.readFileSync(keyPath) }
    console.log('✓ HTTPS enabled with local cert')
  } else {
    console.warn('⚠ certs/ not found — running HTTP (camera may be blocked on LAN)')
  }

  return {
    plugins: [react()],
    server: {
      host: true,
      port: 5173,
      https: httpsConfig,
      proxy: {
        '/api': {
          target: `http://${backendHost}:5000`,
          changeOrigin: true,
          rewrite: (p) => p.replace(/^\/api/, ''),
        },
      },
    },
  }
})