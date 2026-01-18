from django.db import models

class GalleryCollection(models.Model):
    name_en = models.CharField(max_length=255)
    name_ur = models.CharField(max_length=255)

    def __str__(self):
        return self.name_en

class GalleryImage(models.Model):
    collection = models.ForeignKey(GalleryCollection, related_name='images', on_delete=models.CASCADE, null=True, blank=True)

    image = models.ImageField(upload_to='gallery/images/')

    def __str__(self):
        return f"{self.collection.name_en} - {self.id}"
