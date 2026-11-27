import { defineCollection } from 'astro:content'
import { glob } from 'astro/loaders'
import { z } from 'astro/zod'

// One Markdown file per post: src/content/blog/<slug>.md. The file name is
// the URL slug, so a post lives at /blog/<slug>/ just like on the old site.
const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      excerpt: z.string().max(500).optional(),
      tags: z.array(z.string()).default([]),
      heroImage: image().optional(),
      // Search-engine overrides; fall back to title / excerpt / heroImage.
      seoTitle: z.string().optional(),
      description: z.string().optional(),
      draft: z.boolean().default(false),
    }),
})

// The landing page: a single file, src/content/home/index.md, whose body is
// the bio shown next to the picture.
const home = defineCollection({
  loader: glob({ base: './src/content/home', pattern: 'index.md' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      name: z.string().optional(),
      picture: image().optional(),
      description: z.string().optional(),
    }),
})

export const collections = { blog, home }
