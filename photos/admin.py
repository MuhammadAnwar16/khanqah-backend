from django.contrib import admin
from .models import Collection, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ur", "created_at")
    fields = ("name_en", "name_ur", "created_at")  # shows date picker
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("collection", "image")  # ✅ removed created_at
    fields = ("collection", "image")        # ✅ removed created_at
