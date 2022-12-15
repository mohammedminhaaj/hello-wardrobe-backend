from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(models.Model):
    mobile = models.CharField(
        max_length=10, verbose_name=_("Mobile Number"), unique=True)
    display_name = models.CharField(
        max_length=64, verbose_name=_("Display Name"))
    email = models.EmailField(verbose_name=_(
        "Email Address"), blank=True, null=True)
    last_login = models.DateTimeField(verbose_name=_("Last Login Time"))
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.mobile

    class Meta:
        verbose_name_plural = "Users"
        db_table = "user"
        ordering = ["display_name"]


class UserOtp(models.Model):
    mobile = models.CharField(max_length=10, verbose_name=_("Mobile Number"))
    otp = models.CharField(max_length=256, verbose_name=_("OTP"))
    expires_on = models.DateTimeField(verbose_name=_("OTP Expires on"))
    attempts = models.PositiveSmallIntegerField(
        verbose_name=_("Attempts"), default=0)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.mobile

    class Meta:
        db_table = "user_otp"
        ordering = ["-id"]
