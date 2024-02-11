from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from streams import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
# snipet
from wagtail.snippets.models import register_snippet

from django.shortcuts import render
# Create your models here.

class BlogTenant(models.Model):
    """Blog Tenant Model"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("image"),],
            heading="Tenant Information"
        ),
        MultiFieldPanel([
            FieldPanel("website"),],
            heading="Tenant Link"
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Tenant"
        verbose_name_plural = "Blog Tenants"

register_snippet(BlogTenant)

class BlogListingPage(RoutablePageMixin, Page):
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
    
    @route(r'^latest/?$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][::-1]
        return render(request, "blog/latest_posts.html", context)
  
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