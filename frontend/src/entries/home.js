// Home-page-only entry, loaded from cms/home_page.html.
// Carries the page stylesheet, the hero-scroll footer behavior and the
// hero image parallax effect.
import Parallax from 'parallax-js'
import '@/assets/styles/home.css'

// Mouse-follow parallax on the hero picture: parallax-js moves each
// [data-depth] layer toward the cursor (and uses the gyroscope on phones).
// The dot layer sits deeper than the image so they drift at different rates.
const heroImage = document.querySelector('[data-hero-image]')
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')

if (heroImage && !reducedMotion.matches) {
  new Parallax(heroImage, { limitX: 40, limitY: 40 })
}

// Scroll-linked lift on the hero picture: while the hero scrolls out, the
// image translates up over the title, capped at the section top. The shift
// is a pure function of scrollY, so scrolling back restores every position.
// Desktop only: below lg the picture already sits above the title.
const heroSection = document.querySelector('[data-hero]')
const desktop = window.matchMedia('(min-width: 1024px)')

if (heroImage && heroSection && !reducedMotion.matches) {
  let maxShift = 0
  let ticking = false

  const measure = () => {
    maxShift = heroImage.offsetTop - heroSection.offsetTop
    apply()
  }

  const apply = () => {
    const shift = desktop.matches ? Math.min(window.scrollY * 0.5, maxShift) : 0
    heroImage.style.transform = `translateY(${-shift}px)`
  }

  window.addEventListener(
    'scroll',
    () => {
      if (!ticking) {
        ticking = true
        requestAnimationFrame(() => {
          apply()
          ticking = false
        })
      }
    },
    { passive: true },
  )
  window.addEventListener('resize', measure)
  desktop.addEventListener('change', measure)
  measure()
}

// The footer becomes sticky only after the hero section is scrolled past,
// and releases again when the hero comes back into view. Other pages never
// load this entry, so their footer stays a normal end-of-page footer.
const hero = document.querySelector('[data-hero]')
const footer = document.querySelector('[data-site-footer]')

if (hero && footer) {
  footer.classList.add('footer-sticky')
  const observer = new IntersectionObserver(([entry]) => {
    const crossed = !entry.isIntersecting && entry.boundingClientRect.bottom < 0
    footer.classList.toggle('footer-sticky-visible', crossed)
  })
  observer.observe(hero)
}
