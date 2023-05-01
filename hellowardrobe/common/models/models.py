from django.db import models
from .base import AuditedModel, SoftDeleteModel
from .managers import SoftDeleteManager, RestorableManager

# Create your models here.
class Region(AuditedModel, SoftDeleteModel):
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length = 30)

    objects = SoftDeleteManager()
    all_objects = RestorableManager()

    def __str__(self) -> str:
        return self.display_name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        db_table = 'region'
        ordering = ['name']
