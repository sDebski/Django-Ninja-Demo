import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField


class Location(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from="name")
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
