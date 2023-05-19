from django.contrib import admin
from .models import Cart, Wishlist, TimeMaster

# Register your models here.

@admin.register(TimeMaster)
class TimeMasterAdmin(admin.ModelAdmin):
    list_display = ["name", "display_name"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "from_date", "to_date", "size"]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]