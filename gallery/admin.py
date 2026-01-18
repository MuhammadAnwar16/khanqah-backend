from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GalleryCollection, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

@admin.register(GalleryCollection)
class GalleryCollectionAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ['name_en', 'name_ur']

admin.site.register(GalleryImage)
