"""Custom paginator for the blog.

Encapsulates the blog's default page size and forgiving page lookup so callers
don't repeat that policy. ``get_page`` already tolerates invalid/out-of-range
page numbers (first page for non-integers, last page when out of range).
"""

from django.core.paginator import Paginator


class BlogPaginator(Paginator):
    """Paginator preset with the blog listing page size."""

    default_per_page = 1

    def __init__(self, object_list, per_page=None, **kwargs):
        super().__init__(object_list, per_page or self.default_per_page, **kwargs)
