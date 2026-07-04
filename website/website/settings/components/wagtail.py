"""
Wagtail CMS settings.
"""

from website.settings import env

WAGTAIL_SITE_NAME = env.str("WAGTAIL_SITE_NAME", default="hryshchenko-blog")

WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", default="http://localhost")

WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# Social share image rendition used by wagtail-metadata (og:image and
# twitter:image). 1200x630 is the recommended Open Graph size.
WAGTAILMETADATA_IMAGE_FILTER = "fill-1200x630"

# wagtailcodeblock loads PrismJS and this theme from its CDN on pages that
# contain a code block. Options: None (default), "coy", "dark", "funky",
# "okaidia", "solarizedlight", "twilight".
WAGTAIL_CODE_BLOCK_THEME = "okaidia"
