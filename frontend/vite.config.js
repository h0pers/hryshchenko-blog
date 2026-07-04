import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  base: '/static/dist/',
  build: {
    outDir: resolve(__dirname, '../website/static/dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      // One entry per Vue island plus the global stylesheet; django-vite
      // loads each via {% vite_asset %} so pages only ship the JS they use.
      input: {
        main: resolve(__dirname, 'src/entries/main.js'),
        home: resolve(__dirname, 'src/entries/home.js'),
        'post-feed': resolve(__dirname, 'src/entries/post-feed.js'),
        'rss-link': resolve(__dirname, 'src/entries/rss-link.js'),
        'theme-toggle': resolve(__dirname, 'src/entries/theme-toggle.js'),
      },
    },
  },
  server: {
    origin: 'http://localhost:5173',
  },
})