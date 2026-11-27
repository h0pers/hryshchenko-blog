# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### Common commands

```bash
npm run dev            # dev server with hot reload (http://localhost:4321)
npm run build          # static build into dist/
npm run preview        # serve dist/
npm run check          # astro check (types)
npm run format         # prettier --write src
npm run format:check   # what CI runs
```

There is no test suite; CI (`.github/workflows/pages.yml`) runs `format:check`, `check` and `build`.

### Architecture

Static Astro site deployed to GitHub Pages. It replaced a Django + Wagtail app (removed; see git history before the Astro migration), keeping its design, URLs (`/blog/<slug>/`, `/blog/rss.xml`) and Vue islands.

- `src/content.config.ts` — content collections: `blog` (one Markdown file per post, file name = slug) and `home` (single `src/content/home/index.md`: name, picture, bio).
- `src/data/site.json` — site title, author, email, footer links (formerly Wagtail `SiteSettings`).
- `src/lib/posts.js` — `getPublishedPosts()` (drops drafts and future-dated posts, newest first) and `paginate()` with `POSTS_PER_PAGE`. Always use these rather than `getCollection('blog')` directly.
- `src/lib/urls.js` — every internal link must go through `url()` / `postUrl()` / `listingUrl()` so the configured `base` is applied (the site may be served from `/<repo>/`).
- Listing: `pages/index.astro` renders page 1, `pages/page/[page].astro` renders pages 2..N. `PostList.astro` puts the next page URL in `data-next-page`; the `PostFeed.vue` island fetches that page and appends its `[data-post-card]` elements (infinite scroll). Keep those data attributes intact.
- Vue islands in `src/islands/`: `ThemeToggle` (`client:only`, touches `document`), `PostFeed` (`client:visible`), `RssLink` (no directive, rendered to static HTML). `src/components/ui/` is shadcn-vue generated code.
- Plain scripts in `src/scripts/` (`main.js` page loader, `home.js` parallax + sticky footer) are bundled via `<script>` tags in the layout/page.
- Sveltia CMS (npm `@sveltia/cms`, version pinned by the lockfile) is mounted by the bare page `src/pages/admin/index.astro` with the typed config in `src/cms/config.ts` (`load_config_file: false`, so there is no `config.yml`). When changing a content schema in `content.config.ts`, update the matching CMS fields too. Collection `media_folder`s are relative to the entry file (`../../assets/...`) so uploaded images land where Astro's `image()` resolves them. `/admin/` is excluded from the sitemap.
- `astro.config.mjs` reads `SITE_URL` / `BASE_PATH` env vars, which the workflow fills from `actions/configure-pages`.

### Code style

Prettier (`.prettierrc`: no semicolons, single quotes, 120 columns, `prettier-plugin-astro`). `src/components/ui/` is excluded via `.prettierignore`.
