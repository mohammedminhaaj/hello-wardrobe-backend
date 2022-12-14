from django.contrib import admin
from .models import UserOtp, User

# Register your models here.
@admin.register(UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = ["mobile","otp","expires_on"]

@admin.register(User)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = ["mobile","display_name","email"]