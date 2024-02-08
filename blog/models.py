from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from streams import blocks
from wagtail.admin.panels import FieldPanel

# Create your models here.

class BlogListingPage(Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        return context

class BlogDetailPage(Page):
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    ) 

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("blog_image"),
        FieldPanel("content"),
    ]