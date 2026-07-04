import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.blog.factories import BlogPostPageFactory
from apps.blog.services import BlogPostService

TAG_POOL = [
    "python",
    "django",
    "vue",
    "docker",
    "postgres",
    "linux",
    "devops",
    "testing",
]


class Command(BaseCommand):
    help = "Create fake blog posts for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=25,
            help="Number of posts to create (default: 25).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        index = BlogPostService.get_blog_index()
        if index is None:
            raise CommandError("No blog index page found. Run load_cms_pages first.")

        count = options["count"]
        for _ in range(count):
            BlogPostPageFactory(
                parent=index,
                tags=random.sample(TAG_POOL, k=random.randint(1, 3)),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {count} fake blog posts."))
