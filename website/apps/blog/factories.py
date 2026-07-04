"""wagtail-factories / factory_boy factories for blog models.

``wagtail_factories.PageFactory`` inserts pages into the Wagtail page tree,
so callers create posts with ``BlogPostPageFactory(parent=blog_index)``.
"""

import factory
import wagtail_factories
from django.utils import timezone
from django.utils.html import format_html_join
from django.utils.text import slugify
from wagtail.rich_text import RichText

from apps.blog.models import BlogPostPage


class BlogPostPageFactory(wagtail_factories.PageFactory):
    """Live blog posts with realistic-looking content."""

    class Meta:
        model = BlogPostPage

    class Params:
        paragraphs = factory.Faker("paragraphs", nb=6)
        uid = factory.Faker("uuid4")

    title = factory.Faker("sentence", nb_words=6)
    slug = factory.LazyAttribute(
        lambda post: f"{slugify(post.title)[:40]}-{post.uid[:4]}"
    )
    date = factory.Faker(
        "date_time_between",
        start_date="-2y",
        tzinfo=timezone.get_current_timezone(),
    )
    excerpt = factory.Faker("paragraph", nb_sentences=3)
    body = factory.LazyAttribute(
        lambda post: [
            (
                "rich_text",
                RichText(
                    format_html_join("", "<p>{}</p>", ((p,) for p in post.paragraphs))
                ),
            )
        ]
    )
    live = True

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create and extracted:
            self.tags.add(*extracted)
