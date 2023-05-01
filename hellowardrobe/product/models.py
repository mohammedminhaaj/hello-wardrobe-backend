from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from common.models import Region, AuditedModel, SoftDeleteModel, SoftDeleteManager, RestorableManager

# Create your models here.


class PrimaryCategory(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Primary Category'
        verbose_name_plural = 'Primary Categories'
        db_table = 'primary_category'
        ordering = ['display_name']


class SecondaryCategory(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Seconday Category'
        verbose_name_plural = 'Secondary Categories'
        db_table = 'secondary_category'
        ordering = ['display_name']


class Size(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=5)
    display_name = models.CharField(max_length=5)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        db_table = 'size'


class TagMaster(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Tag Master'
        verbose_name_plural = 'Tags Master'
        db_table = 'tag_master'


class Tag(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=50)
    display_name = models.CharField(
        max_length=50)
    category = models.ForeignKey(
        TagMaster, on_delete=models.CASCADE)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tag'


class Product(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=50)
    url_name = models.SlugField(db_index=True, max_length=60, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=1000)
    highlights = models.CharField(max_length=256, help_text=_(
        'Separate each list item with a semicolon (;)'))
    details = models.CharField(max_length=256)
    original_price = models.DecimalField(max_digits=7, decimal_places=2)
    primary_category = models.ForeignKey(
        PrimaryCategory, on_delete=models.CASCADE)
    secondary_category = models.ForeignKey(
        SecondaryCategory, on_delete=models.CASCADE)
    size = models.ManyToManyField(Size)
    tags = models.ManyToManyField(Tag)
    is_featured = models.BooleanField(
        default=False, verbose_name=_("Is Featured?"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
        ordering = ['name']
