"""Context builders for CMS pages.

Called from a page's ``get_context``. Keeping this logic here (instead of on the
model) lets page models stay thin while the ORM/business logic stays in the
service layer.
"""

from wagtail.models import Page

from apps.blog.paginator import BlogPaginator
from apps.blog.services import BlogPostService


def home_page_context(page, request, *args, **kwargs):
    """Build the :class:`HomePage` context: base context + paginated recent posts."""
    context = Page.get_context(page, request, *args, **kwargs)
    posts = BlogPostService.get_recent_posts()
    context["posts"] = BlogPaginator(posts).get_page(request.GET.get("page"))
    return context
