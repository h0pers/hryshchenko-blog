// @ts-check
import { defineConfig } from 'astro/config'
import vue from '@astrojs/vue'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'

// SITE_URL / BASE_PATH are filled in by the Pages workflow from
// actions/configure-pages, so the build works on both a custom domain
// (base "/") and the default <user>.github.io/<repo>/ project URL.
const site = process.env.SITE_URL || 'http://localhost:4321'
const base = process.env.BASE_PATH || '/'

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  integrations: [vue(), sitemap({ filter: (page) => !page.includes('/admin/') })],
  markdown: {
    shikiConfig: {
      // Closest Shiki match to the Prism "okaidia" theme the Wagtail site used.
      theme: 'monokai',
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
})
