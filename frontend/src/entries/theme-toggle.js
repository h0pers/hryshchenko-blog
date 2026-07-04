import { createApp } from 'vue'
import ThemeToggle from '@/islands/ThemeToggle.vue'

const el = document.getElementById('theme-toggle-island')
if (el) createApp(ThemeToggle).mount(el)
