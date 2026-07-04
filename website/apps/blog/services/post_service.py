"""Class-based service encapsulating blog listing queries.

All ORM access and business logic for blog posts lives here. Views call these
static methods; models never import this package, keeping the dependency
direction one-way (services -> models).
"""

from django.db.models import QuerySet

from apps.blog.models import BlogIndexPage, BlogPostPage


class BlogPostService:
    """Queries for blog posts."""

    @staticmethod
    def get_blog_index() -> BlogIndexPage | None:
        """Return the first live blog index page, or ``None`` if none exists yet."""
        return BlogIndexPage.objects.live().first()

    @staticmethod
    def get_live_posts(index_page: BlogIndexPage) -> QuerySet[BlogPostPage]:
        """Live posts under ``index_page``, newest first.

        Related objects are prefetched to keep listing rendering free of N+1
        queries.
        """
        return (
            BlogPostPage.objects.child_of(index_page)
            .live()
            .order_by("-date")
            .select_related("hero_image", "owner")
            .prefetch_related("tags")
        )

    @staticmethod
    def get_recent_posts() -> QuerySet[BlogPostPage]:
        """Live posts, newest first, for listings that aren't the blog index
        itself (e.g. the home page). Empty queryset if no blog index exists yet.
        """
        index_page = BlogPostService.get_blog_index()
        if index_page is None:
            return BlogPostPage.objects.none()
        return BlogPostService.get_live_posts(index_page)
