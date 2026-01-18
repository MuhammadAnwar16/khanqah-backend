# publications/admin.py
from django.contrib import admin
from .models import Publication

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'file', 'cover')
    list_filter = ('category',)
    search_fields = ('title_en', 'title_ur', 'description_en', 'description_ur')
    readonly_fields = ('cover_preview',)

    # Optional: show a small preview of the cover image in admin
    def cover_preview(self, obj):
        if obj.cover:
            return f'<img src="{obj.cover.url}" width="100" />'
        return "-"
    cover_preview.allow_tags = True
    cover_preview.short_description = 'Cover Preview'
