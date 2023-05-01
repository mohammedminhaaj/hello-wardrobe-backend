from django.contrib import admin
from ..models import Region
from .base import AuditedAdminMixin
# Register your models here.


@admin.register(Region)
class RegionAdmin(AuditedAdminMixin):
    list_display = ['name', 'display_name']
