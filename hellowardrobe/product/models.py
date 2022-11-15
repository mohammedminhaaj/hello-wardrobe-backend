from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Create your models here.

class PrimaryCategory(models.Model):
    name = models.CharField(max_length = 20)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Primary Category'
        verbose_name_plural = 'Primary Categories'
        db_table = 'primary_category'
        ordering = ['name'] 

class SecondaryCategory(models.Model):
    name = models.CharField(max_length = 20)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Seconday Category'
        verbose_name_plural = 'Secondary Categories'
        db_table = 'secondary_category'
        ordering = ['name']

class Size(models.Model):
    name = models.CharField(max_length = 5)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        db_table = 'size'

class TagMaster(models.Model):
    name = models.CharField(max_length= 50)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Tag Master'
        verbose_name_plural = 'Tags Master'
        db_table = 'tag_master'


class Tag(models.Model):
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(TagMaster, on_delete=models.CASCADE, limit_choices_to=Q(is_active = True))
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tag'

class Product(models.Model):
    name = models.CharField(max_length = 50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    primary_category = models.ForeignKey(PrimaryCategory, on_delete=models.CASCADE, limit_choices_to=Q(is_active=True))
    secondary_category = models.ForeignKey(SecondaryCategory, on_delete=models.CASCADE, limit_choices_to=Q(is_active=True))
    size = models.ManyToManyField(Size, limit_choices_to=Q(is_active=True))
    tags = models.ManyToManyField(Tag, limit_choices_to=Q(is_active=True))
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    updated_on = models.DateTimeField(auto_now = True, editable = False)
    is_active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
        ordering = ['name']


