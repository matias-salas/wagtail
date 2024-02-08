from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
#import richtext
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from streams import blocks
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey

class HomePageCarouselImages(Orderable):
    """
        Entre 1 y 5 imagenes para el carrousel de la home
    """

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
    )
    caption = models.CharField(max_length=100, blank=True, null=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

class HomePage(Page):
    """
        Home page model
    """

    template = "home/home_page.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=True, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic", "link"], blank=True, null=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=False,
        null=True,
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            FieldPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading="Banner Options"),
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
        heading="Carrousel Images"),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"