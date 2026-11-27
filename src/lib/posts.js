// Blog listing queries: the static-site counterpart of the old
// BlogPostService + BlogPaginator.
import { getCollection } from 'astro:content'

export const POSTS_PER_PAGE = 10

/** Published posts (drafts and future-dated posts excluded), newest first. */
export async function getPublishedPosts() {
  const now = new Date()
  const posts = await getCollection('blog', ({ data }) => !data.draft && data.date <= now)
  return posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime())
}

/** Split posts into listing pages of POSTS_PER_PAGE (always at least one page). */
export function paginate(posts) {
  const pages = []
  for (let i = 0; i < posts.length; i += POSTS_PER_PAGE) {
    pages.push(posts.slice(i, i + POSTS_PER_PAGE))
  }
  return pages.length ? pages : [[]]
}
