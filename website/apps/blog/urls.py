"""URL patterns for the blog app."""

from django.urls import path

from apps.blog.feeds import BlogPostFeed

app_name = "blog"

urlpatterns = [
    path("rss.xml", BlogPostFeed(), name="feed"),
]
