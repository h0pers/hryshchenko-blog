// Global entry, loaded on every page from the Django base template. No Vue
// app is mounted here; interactive widgets ship as separate island entries.
// The .js and .dark root classes are set by the critical inline script in
// base.html so they exist before first paint; this entry only cleans up.
import '@/assets/styles/style.css'

// Fade the loader out once the document and its resources are fully loaded.
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader')
  if (!loader) return
  loader.classList.add('page-loader-done')
  loader.addEventListener('transitionend', () => loader.remove(), { once: true })
})
