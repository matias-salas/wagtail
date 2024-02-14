from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from streams import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
# snipet
from wagtail.snippets.models import register_snippet
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import render
# Create your models here.
@register_snippet
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
        # Get all posts
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        context["posts"] = BlogDetailPage.objects.live().public()
        context["posts"] = posts
        return context
    
    @route(r'^latest/?$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][::-1]
        return render(request, "blog/latest_posts.html", context)

    def serve(self, request, *args, **kwargs):
        print("A: ", request.user)
        if request.user.is_authenticated:
            print("A: ", request.user)
            return super().serve(request, *args, **kwargs)
        else:
            return render(request, 'users/login.html', {'page': self})
        
        
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


    def serve(self, request, *args, **kwargs):
        print("A: ", request.user)
        if request.user.is_authenticated:
            print("A: ", request.user)
            return super().serve(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (reverse('users:login'), request.path))
        