import { defineConfig, loadEnv } from 'vite'
import { convertEnv, getSrcPath, getRootPath } from './build/utils.js'
import { viteDefine } from './build/config/index.js'
import { createVitePlugins } from './build/plugin/index.js'
import { OUTPUT_DIR, PROXY_CONFIG } from './build/constant.js'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ command, mode }) => {
  const srcPath = getSrcPath()
  const rootPath = getRootPath()
  const isBuild = command === 'build'

  const env = loadEnv(mode, process.cwd())
  const viteEnv = convertEnv(env)
  const { VITE_PORT, VITE_PUBLIC_PATH, VITE_USE_PROXY, VITE_BASE_API } = viteEnv

  return {
    base: VITE_PUBLIC_PATH || '/',
    resolve: {
      alias: {
        '~': rootPath,
        '@': srcPath,
      },
    },
    define: viteDefine,
    plugins: [
      ...(!isBuild ? [vueDevTools()] : []),
      ...createVitePlugins(viteEnv, isBuild)
    ],
    server: {
      host: '0.0.0.0',
      port: VITE_PORT,
      open: true,
      proxy: VITE_USE_PROXY
        ? {
            [VITE_BASE_API]: PROXY_CONFIG[VITE_BASE_API],
          }
        : undefined,
    },
    build: {
      target: 'es2015',
      outDir: OUTPUT_DIR || 'dist',
      reportCompressedSize: false,
      chunkSizeWarningLimit: 1024,
    },
  }
})

