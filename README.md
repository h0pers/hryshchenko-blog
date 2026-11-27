# hryshchenko blog

A static personal blog built with [Astro](https://astro.build), Vue islands and Tailwind CSS, hosted on GitHub Pages.

## Local development

Requires Node 24 (see `.nvmrc`).

```bash
npm install
npm run dev        # http://localhost:4321 with hot reload
npm run build      # static site into dist/
npm run preview    # serve dist/ locally
npm run check      # type-check .astro / .ts files
npm run format     # prettier
```

## Writing in the browser (Sveltia CMS)

The site has an editor at `/admin/` (e.g. `https://<your-site>/admin/`). It edits posts, the home page and site settings, and every save is a commit to `master`, which redeploys the site in a minute or two.

Sign in with **Sign In Using Access Token**. Create the token once at GitHub → **Settings → Developer settings → Fine-grained tokens**:

- Repository access: only `h0pers/hryshchenko-blog`
- Permissions: **Contents: Read and write** (Metadata: read is added automatically)

The token stays in that browser's local storage; sign out on shared computers. When running `npm run dev` locally in Chrome or Edge, **Work with Local Repository** edits the files on disk instead, without a token or commits.

The CMS config is `src/cms/config.ts`; its fields must match the schemas in `src/content.config.ts`.

## Writing a post by hand

Add a Markdown file to `src/content/blog/`. The file name becomes the URL: `src/content/blog/my-post.md` is served at `/blog/my-post/`.

```markdown
---
title: My post
date: 2026-12-01
excerpt: Short summary shown in the listing, RSS and search results.
tags: [django, astro]
heroImage: ../../assets/blog/my-post-hero.jpg # optional
draft: false # true keeps it off the site
---

Post body in Markdown. Code blocks, tables and images are supported.
```

- Put images in `src/assets/blog/` and reference them with a relative path; they are resized and converted at build time.
- Posts with a future `date` are hidden until that day (the deploy workflow rebuilds the site daily).
- Optional `seoTitle` and `description` override the title and excerpt in search/social previews.
- The `sample-*.md` posts are placeholders; delete them once real posts exist.

## Other content

- Home page name, picture and bio: `src/content/home/index.md`.
- Site title, author, contact email and footer links: `src/data/site.json`.

## Deployment

`.github/workflows/pages.yml` checks formatting and types on every push and pull request, builds the site, and on `master` deploys it to GitHub Pages. It also runs daily for scheduled posts.

One-time setup: in the repository's **Settings → Pages**, set **Source** to **GitHub Actions**. For a custom domain, add it under the same page and create the DNS records GitHub shows; the build picks up the domain automatically.
