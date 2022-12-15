from django.contrib import admin
from .models import UserOtp, User

# Register your models here.
@admin.register(UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = ["mobile","otp","expires_on","attempts"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["mobile","display_name","email"]