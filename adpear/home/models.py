from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from rest_framework.fields import Field

from streams import blocks


class HomePageCarouselImages(Orderable):
    """ Between 1 and 5 images for carousel"""
    
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    
    panels = [
        ImageChooserPanel("carousel_image"),
    ]
    
    api_fields = [
        APIField("carousel_image"),
    ]

class BannerCTASerializer(Field):
    def to_representation(self, page):
        return {
            'id': page.id,
            'title': page.title,
            'first_published_at': page.first_published_at,
            'owner': page.owner.username,
            'slug': page.slug,
            'url': page.url,
        }


class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    templates = "home/home_page.html"
    # max_count = 1
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    parent_page_type = [
        'wagtailcore.Page'
    ]

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock() ),
            ("full_richtext", blocks.RichtextBlock() ),
            ("simple_richtext", blocks.SimpleRichtextBlock() ),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta", serializer=BannerCTASerializer()),
        APIField("carousel_images"),
        APIField("content"),
        APIField("a_custom_api_response"),
    ]
    
    @property
    def a_custom_api_response(self):
        # return ["SOMETHING CUSTOM", 3.14, [1, 2, 3, 'a', 'b', 'c']]
        # logic goes in here
        return f"Banner Title Is: {self.banner_title}"

    content_panels = Page.content_panels + [
        
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Add an Image"),
        ], heading = "Carousel Images"),
        StreamFieldPanel("content"),
    ]
    
    # This is how you'd normally hide promote and settings tabs
    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ImageChooserPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading ="Banner options",),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(banner_panels, heading="Banner Settings"),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading='Settings Stuff'),
        ]
    )



    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)

    def get_admin_display_title(self):
        return "Custom Home Page Title"


# # This will change the "title" field 's verbose name to "Custom Name".
# # But you'd still reference it in the template as `page.title`
# HomePage._meta.get_field("title").verbose_name = "Custom Name"
# # Here we are removing the help text. But to change it, simply change None to a string.
# HomePage._meta.get_field("title").help_text = None
# # Below is the new default title for a Home Page.
# # This only appears when you create a new page.
# HomePage._meta.get_field("title").default = "Default HomePage Title"
# # Lastly, we're adding a default `slug` value to the page.
# # This does not need to reflect the same (or similar) value that the `title` field has.
# HomePage._meta.get_field("slug").default = "default-homepage-title"

