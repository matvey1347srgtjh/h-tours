from django.contrib import admin
from .models import Jewelry
from allauth.socialaccount.models import SocialApp
from unfold.admin import ModelAdmin
from .models import Favorite
from account1.models import Avatar
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import Slide, Review
from django.contrib import admin
from chat.models import ChatSession, Message


admin.site.register(ChatSession)
admin.site.register(Message)




@admin.register(Jewelry)
class AdminJewelery(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    
    
@admin.register(Review)
class AdminReview(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }


@admin.register(Slide)
class Adminslide(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }



@admin.register(Avatar)
class AdminAvatar(ModelAdmin):
    pass




class SotialAppAdmin(admin.ModelAdmin):
    model = SocialApp
    menu_icon = 'placeholder'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'provider')
    

@admin.register(Favorite)
class AdminFavorite(ModelAdmin):
    pass


