from django.db import models

class Publication(models.Model):
    CATEGORY_CHOICES = [
        ("book", "Book"),
        ("risala", "Risala"),
        ("other", "Other"),
    ]
    
    title_en = models.CharField(max_length=255)
    title_ur = models.CharField(max_length=255)
    file = models.FileField(upload_to="publications/")
    cover = models.ImageField(
    upload_to="publications/covers/",
    default="publications/covers/default.png"
)
    description_en = models.TextField()
    description_ur = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title_en
