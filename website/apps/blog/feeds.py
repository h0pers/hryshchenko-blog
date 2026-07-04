"""RSS feed for blog posts, built on Django's syndication framework."""

from datetime import datetime

from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.blog.models import BlogPostPage
from apps.blog.services import BlogPostService

FEED_LIMIT = 20


class BlogPostFeed(Feed):
    """Latest live blog posts, newest first."""

    title = _("Dmytro Hryshchenko - blog")
    link = "/"
    description = _("Latest blog posts.")

    def items(self) -> QuerySet[BlogPostPage]:
        return BlogPostService.get_recent_posts()[:FEED_LIMIT]

    def item_title(self, item: BlogPostPage) -> str:
        return item.title

    def item_description(self, item: BlogPostPage) -> str:
        return item.excerpt

    def item_link(self, item: BlogPostPage) -> str:
        return item.url

    def item_pubdate(self, item: BlogPostPage) -> datetime:
        return item.date

    def item_author_name(self, item: BlogPostPage) -> str | None:
        if item.owner is None:
            return None
        return item.owner.get_full_name() or item.owner.get_username()
