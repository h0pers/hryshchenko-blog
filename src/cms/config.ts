// Sveltia CMS configuration, served at /admin/. Every save in the editor is
// a commit to `master`, which triggers the Pages workflow to rebuild the site.
// Fields mirror the content schemas in src/content.config.ts: keep both in sync.
import type { CmsConfig } from '@sveltia/cms'

// Paths are relative to the edited file (src/content/<collection>/...), so the
// stored values are the ../../assets/... paths Astro's image() schema expects.
const BLOG_MEDIA = '../../assets/blog'
const HOME_MEDIA = '../../assets/home'

export function cmsConfig(siteUrl: string): CmsConfig {
  return {
    load_config_file: false,
    app_title: 'hryshchenko - admin',
    site_url: siteUrl,
    backend: {
      name: 'github',
      repo: 'h0pers/hryshchenko-blog',
      branch: 'master',
      // Sign in with a fine-grained personal access token (Contents: read and
      // write on this repository only); GitHub OAuth would need a proxy server.
      auth_methods: ['token'],
    },
    // Fallback for media not covered by a collection; every collection below
    // stores images under src/assets/ so Astro optimizes them.
    media_folder: 'public/uploads',
    public_folder: '/uploads',
    collections: [
      {
        name: 'blog',
        label: 'Posts',
        label_singular: 'Post',
        folder: 'src/content/blog',
        extension: 'md',
        format: 'frontmatter',
        create: true,
        // The file name is the slug, i.e. the post URL /blog/<slug>/.
        slug: '{{slug}}',
        media_folder: BLOG_MEDIA,
        public_folder: BLOG_MEDIA,
        sortable_fields: ['date', 'title'],
        summary: '{{title}} ({{date}})',
        fields: [
          { name: 'title', label: 'Title', widget: 'string' },
          { name: 'date', label: 'Post date', widget: 'datetime', type: 'date', default: '{{now}}' },
          {
            name: 'excerpt',
            label: 'Excerpt',
            widget: 'text',
            required: false,
            maxlength: 500,
            hint: 'Short summary shown in listings, RSS and search results.',
          },
          { name: 'tags', label: 'Tags', widget: 'list', required: false, default: [] },
          { name: 'heroImage', label: 'Hero image', widget: 'image', required: false },
          {
            name: 'draft',
            label: 'Draft',
            widget: 'boolean',
            default: false,
            hint: 'Drafts are kept out of the site.',
          },
          {
            name: 'seoTitle',
            label: 'SEO title',
            widget: 'string',
            required: false,
            hint: 'Overrides the title in search and social previews.',
          },
          {
            name: 'description',
            label: 'SEO description',
            widget: 'text',
            required: false,
            hint: 'Overrides the excerpt in search and social previews.',
          },
          { name: 'body', label: 'Body', widget: 'markdown' },
        ],
      },
      {
        name: 'pages',
        label: 'Pages',
        files: [
          {
            name: 'home',
            label: 'Home page',
            file: 'src/content/home/index.md',
            media_folder: HOME_MEDIA,
            public_folder: HOME_MEDIA,
            fields: [
              { name: 'title', label: 'Page title', widget: 'string' },
              { name: 'name', label: 'Name', widget: 'string', required: false, hint: 'Shown in the hero.' },
              { name: 'picture', label: 'Picture', widget: 'image', required: false },
              {
                name: 'description',
                label: 'SEO description',
                widget: 'text',
                required: false,
              },
              { name: 'body', label: 'Bio', widget: 'markdown', required: false },
            ],
          },
          {
            name: 'site',
            label: 'Site settings',
            file: 'src/data/site.json',
            format: 'json',
            fields: [
              { name: 'title', label: 'Site title', widget: 'string', hint: 'Used for RSS and social previews.' },
              { name: 'description', label: 'Site description', widget: 'string' },
              { name: 'author', label: 'Author', widget: 'string' },
              { name: 'email', label: 'Contact email', widget: 'string', required: false },
              {
                name: 'links',
                label: 'Footer links',
                widget: 'list',
                required: false,
                fields: [
                  { name: 'label', label: 'Label', widget: 'string' },
                  { name: 'url', label: 'URL', widget: 'string' },
                ],
              },
            ],
          },
        ],
      },
    ],
  }
}
