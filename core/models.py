from django.db import models

class Publication(models.Model):
    title_en = models.CharField(max_length=255)
    title_ur = models.CharField(max_length=255)
    description_en = models.TextField(blank=True)
    description_ur = models.TextField(blank=True)
    file = models.FileField(upload_to='publications/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_en
