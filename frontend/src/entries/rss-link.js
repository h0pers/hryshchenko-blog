import { createApp } from 'vue'
import RssLink from '@/islands/RssLink.vue'

const el = document.getElementById('rss-link-island')
if (el) createApp(RssLink, { url: el.dataset.feedUrl }).mount(el)
