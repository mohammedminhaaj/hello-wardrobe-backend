from django.contrib import admin

from .models import PrimaryCategory, SecondaryCategory, Product, Size, Tag, TagMaster

from common.admin import AuditedAdminMixin

# Register your models here.

@admin.register(PrimaryCategory)
class PrimaryCategoryAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name']


@admin.register(SecondaryCategory)
class SecondaryCategoryAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name']


@admin.register(Size)
class SizeAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name']


@admin.register(TagMaster)
class TagMasterAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name']


@admin.register(Tag)
class TagAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name', 'category']


@admin.register(Product)
class ProductAdmin(AuditedAdminMixin):
    prepopulated_fields = {'url_name': ('name',)}
    list_display = ['name', 'url_name', 'price', 'primary_category',
                    'secondary_category', 'is_featured', 'region']
