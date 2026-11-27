// Site-relative URLs that respect Astro's `base` (a non-root base is used
// when the site is served from <user>.github.io/<repo>/).
const base = import.meta.env.BASE_URL.replace(/\/$/, '')

/** Prefix a root-relative path such as "/blog/foo/" with the configured base. */
export function url(path = '/') {
  return `${base}${path}`
}

export const postUrl = (post) => url(`/blog/${post.id}/`)

/** URL of listing page `n` (page 1 is the home page). */
export const listingUrl = (n) => (n <= 1 ? url('/') : url(`/page/${n}/`))

export const feedUrl = url('/blog/rss.xml')

const dateFormat = new Intl.DateTimeFormat('en-US', { dateStyle: 'long', timeZone: 'UTC' })

/** "November 27, 2026": matches Django's default DATE_FORMAT ("N j, Y"). */
export const formatDate = (date) => dateFormat.format(date)

/** "2026-11-27", for <time datetime>. */
export const isoDate = (date) => date.toISOString().slice(0, 10)
