from django.contrib import admin
from .models import Product, Favorite

admin.site.register(Product)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    """
    search_fields = ['pk', 'user__username']
    """
    important :search_fields = ['foreign_key__related_fieldname']
    exemple: search_fields = ['user__email']
    """
    