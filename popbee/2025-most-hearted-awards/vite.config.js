import { build, defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { imagetools } from 'vite-imagetools'
import path from 'path'
import webfontDownload from 'vite-plugin-webfont-dl'

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '~': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        preview: path.resolve(__dirname, 'preview.html'),
        result: path.resolve(__dirname, 'result.html'),
      },
    },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.includes('swiper'),
        },
      },
    }),
    tailwindcss(),
    imagetools(),
    webfontDownload([
      'https://use.typekit.net/osq3vkm.css',
      'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500&display=swap',
    ]),
  ],
})
