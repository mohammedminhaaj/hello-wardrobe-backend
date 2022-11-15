from django.contrib import admin

from .models import PrimaryCategory, SecondaryCategory, Product, Size, Tag, TagMaster

# Register your models here.

admin.site.site_header = 'Hello Wardrobe Admin'
admin.site.site_title = 'Hello Wardrobe Admin'
admin.site.index_title = 'Admin Portal'

admin.site.register(PrimaryCategory)
admin.site.register(SecondaryCategory)
admin.site.register(Size)
admin.site.register(TagMaster)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url_name': ('name',)}
    list_display = ['name', 'url_name', 'price', 'primary_category',
                    'secondary_category', 'is_active']
