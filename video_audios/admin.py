from django.contrib import admin
from .models import Audio, Video

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ("english_title", "urdu_title", "category", "date")
    list_filter = ("category", "date")
    search_fields = ("english_title", "urdu_title")

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("english_title", "urdu_title", "category", "date")
    list_filter = ("category", "date")
    search_fields = ("english_title", "urdu_title")
