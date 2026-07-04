"""Page types for the blog: a listing index and individual posts.

These models hold data and admin configuration only. All querying, pagination
and business logic lives in ``apps.blog.services`` and is consumed by views.
"""

from django.db import models
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock
from wagtailmetadata.models import MetadataPageMixin

RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
    "blockquote",
    "code",
    "superscript",
    "subscript",
    "strikethrough",
]


class BlogIndexPage(Page):
    """
    Blog root page. Not user-visible: it exists only so ``BlogPostPage``
    children get their ``/blog/<post>/`` URLs. Direct requests 404.
    """

    is_creatable = False

    # Only blog posts may live under the index.
    subpage_types = ["blog.BlogPostPage"]

    def serve(self, request, *args, **kwargs):
        raise Http404

    def get_sitemap_urls(self, request=None):
        """Keep this page out of sitemap.xml, since it 404s (see ``serve``)."""
        return []

    class Meta:
        verbose_name = _("blog")


class BlogPostTag(TaggedItemBase):
    """Through model linking free-form tags to a :class:`BlogPostPage`."""

    content_object = ParentalKey(
        "blog.BlogPostPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class BlogPostPage(MetadataPageMixin, Page):
    """A single blog article."""

    date = models.DateTimeField(_("post date"))
    excerpt = models.TextField(
        _("excerpt"),
        blank=True,
        max_length=500,
        help_text=_("Short summary shown in listings and search results."),
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("hero image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("rich_text", RichTextBlock(features=RICH_TEXT_FEATURES)),
            ("code", CodeBlock(label=_("code"))),
            ("table", TableBlock()),
        ],
        blank=True,
    )

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
            ],
        ),
        FieldPanel("hero_image"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
    ]

    search_fields = [
        *Page.search_fields,
        index.SearchField("excerpt"),
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    # Posts may only be created under a blog index.
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    def get_meta_description(self):
        return self.search_description or self.excerpt

    def get_meta_image(self):
        return self.search_image or self.hero_image

    class Meta:
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")
