from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Site

from apps.blog.models import BlogIndexPage
from apps.cms.models import HomePage


class Command(BaseCommand):
    help = "Create default CMS pages if they don't exist."

    @transaction.atomic
    def handle(self, *args, **options):
        self._ensure_home_page()
        self._ensure_blog_index()
        self.stdout.write(self.style.SUCCESS("CMS pages loaded."))

    def _ensure_home_page(self):
        if HomePage.objects.exists():
            return

        site = Site.objects.get(is_default_site=True)
        old_root = site.root_page
        tree_root = old_root.get_parent()
        old_root.delete()

        home_page = tree_root.add_child(
            instance=HomePage(title="Home", slug="home", live=True)
        )
        site.root_page = home_page
        site.save()

    def _ensure_blog_index(self):
        if BlogIndexPage.objects.exists():
            return

        root_page = Site.objects.get(is_default_site=True).root_page
        root_page.add_child(
            instance=BlogIndexPage(title="Blog", slug="blog", live=True)
        )
