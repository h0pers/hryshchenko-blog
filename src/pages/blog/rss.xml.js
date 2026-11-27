// RSS feed at /blog/rss.xml (same URL as the old Django feed): latest 20 posts.
import rss from '@astrojs/rss'
import site from '@/data/site.json'
import { getPublishedPosts } from '@/lib/posts'
import { postUrl, url } from '@/lib/urls'

const FEED_LIMIT = 20

export async function GET(context) {
  const posts = (await getPublishedPosts()).slice(0, FEED_LIMIT)
  return rss({
    title: site.title,
    description: site.description,
    site: new URL(url('/'), context.site),
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.excerpt,
      link: postUrl(post),
      pubDate: post.data.date,
      author: site.author,
      categories: post.data.tags,
    })),
  })
}
