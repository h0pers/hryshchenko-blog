from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtailmetadata.models import MetadataPageMixin


class HomePage(MetadataPageMixin, Page):
    """The site's landing page: profile hero plus the blog post list."""

    is_creatable = False

    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        help_text=_(
            "Name displayed in the hero section (the page title stays 'Home')."
        ),
    )
    picture = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("picture"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Profile photo shown in the hero section."),
    )
    body = RichTextField(
        _("bio"),
        blank=True,
        help_text=_("Short introduction shown next to the picture."),
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("name"),
        FieldPanel("picture"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        from apps.cms.contexts import home_page_context

        return home_page_context(self, request, *args, **kwargs)

    def get_meta_image(self):
        return self.search_image or self.picture

    class Meta:
        verbose_name = _("home page")


@register_setting
class SiteSettings(ClusterableModel, BaseGenericSetting):
    """Site-wide contact details and links, editable under Settings > Site."""

    email = models.EmailField(
        _("email"),
        blank=True,
        help_text=_("Contact email for the website."),
    )

    panels = [
        FieldPanel("email"),
        InlinePanel("links", label=_("links")),
    ]

    class Meta:
        verbose_name = _("site")


class SiteLink(Orderable):
    """A single external link for the site (e.g. LinkedIn, GitHub)."""

    setting = ParentalKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name="links",
    )
    label = models.CharField(_("label"), max_length=50)
    url = models.URLField(_("URL"))

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
    ]
