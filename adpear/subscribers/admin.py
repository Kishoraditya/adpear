
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from .models import Subscribers

class SubscriberAdmin(ModelAdmin):
    """Subscriber Admin"""
    
    model = Subscribers
    menu_label = "Subscriber"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "full_name",)
    search_fields = ("email", "full_name",)

modeladmin_register(SubscriberAdmin)