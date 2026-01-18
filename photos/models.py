from django.db import models
from django.utils import timezone


class Collection(models.Model):
    name_en = models.CharField(max_length=255)
    name_ur = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now, null=True, blank=True)  # editable in admin

    def __str__(self):
        return self.name_en


class Photo(models.Model):
    collection = models.ForeignKey(
        Collection,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="photos/")  # saves to MEDIA_ROOT/photos/

    def __str__(self):
        return f"{self.collection.name_en} - {self.id}"
