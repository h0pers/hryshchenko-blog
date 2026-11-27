// Global script, bundled into every page by layouts/BaseLayout.astro.
// The .js and .dark root classes are set by the critical inline script in
// BaseLayout so they exist before first paint; this script only cleans up.

// Fade the loader out once the document and its resources are fully loaded.
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader')
  if (!loader) return
  loader.classList.add('page-loader-done')
  loader.addEventListener('transitionend', () => loader.remove(), { once: true })
})
