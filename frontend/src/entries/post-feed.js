import { createApp } from 'vue'
import PostFeed from '@/islands/PostFeed.vue'

const el = document.getElementById('post-feed-island')
if (el) createApp(PostFeed).mount(el)
