from django.contrib import admin

from .models import PrimaryCategory, SecondaryCategory, Product, Size, Tag

# Register your models here.

admin.site.site_header = 'Hello Wardrobe Admin'
admin.site.site_title = 'Hello Wardrobe Admin'
admin.site.index_title = 'Admin Portal'

admin.site.register(PrimaryCategory)
admin.site.register(SecondaryCategory)
admin.site.register(Product)
admin.site.register(Size)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
