from typing import Any
from django.db import models
from django.conf import settings
from product.models import Product, ProductSize
from django.core.exceptions import ValidationError
from common.models import AuditedModel, SoftDeleteModel, SoftDeleteManager, RestorableManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TimeMaster(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return f"{self.display_name}"

    class Meta:
        verbose_name = 'Time Master'
        verbose_name_plural = 'Time Master'
        db_table = 'time_master'
        ordering = ['id']

class CartWishlistManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product__deleted_at__isnull = True, product__deleted_by__isnull = True)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_date = models.DateField()
    deliver_at = models.ForeignKey(
        TimeMaster, on_delete=models.CASCADE, related_name="cart_deliver_at")
    to_date = models.DateField()
    return_by = models.ForeignKey(
        TimeMaster, on_delete=models.CASCADE, related_name="cart_return_by")
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} - {self.product}"
    
    objects = CartWishlistManager()

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        db_table = 'cart'
        ordering = ['id']
        constraints = [models.UniqueConstraint(fields=(
            "user", "product", "size"), name="unique_user_product_size_mapping", violation_error_message=_("Cannot add same product with same size"))]

    def clean(self):
        if self.size.product != self.product:
            raise ValidationError(
                "Cannot select a size of a different product")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} - {self.product}"
    
    objects = CartWishlistManager()

    class Meta:
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        db_table = 'wishlist'
        ordering = ['id']
        constraints = [models.UniqueConstraint(fields=(
            "user", "product"), name="unique_user_product_mapping")]
