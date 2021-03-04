""" Streamfields live in here"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""
    
    title = blocks.CharBlock(required=True, help_text='Add your Title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')
    
    class Meta: #noqa
        template ="streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
        
class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""
    
    title = blocks.CharBlock(required=True, help_text='Add your Title')
    
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required= False)),
                ("button_url", blocks.URLBlock(required=False, help_text="Page button will be shown first on left or above")),
                
            ]
        )
    )
    
    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"

class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features"""
    
    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full Richtext"
        
class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext with some the features"""
    
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "itlaic",
            "link",
        ]
    
    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple Richtext"        

class CTABlock(blocks.StructBlock):
    """A simple call to action"""
    
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["blod", "Italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)
    
    class Meta: #noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"
        
        
class LinkStructValue(blocks.StructValue):
    """Additional logic for our url"""
    
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        
        return None
    
    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]
            
        
        
class ButtonBlock(blocks.StructBlock):
    """An external or internal URL"""
    
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url wil be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url wil be used secondarily to the button page')    
    
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context
    
    class Meta: #noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single button"
        value_class = LinkStructValue
