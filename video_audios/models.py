from django.db import models

CATEGORY_CHOICES = [
    ("Bayaan", "Bayaan"),
    ("Dhikr", "Dhikr"),
    ("Event", "Event"),
]

class Audio(models.Model):
    english_title = models.CharField(max_length=255)
    urdu_title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="audios/")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.english_title

class Video(models.Model):
    english_title = models.CharField(max_length=255)
    urdu_title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.english_title
