from django.contrib import admin
from .models import AboutSection, AboutSubSection, CurrentNasheen, PreviousNasheen


class AboutSubSectionInline(admin.TabularInline):
    model = AboutSubSection
    extra = 1
    fields = ('title_en', 'title_ur', 'content_en', 'content_ur', 'order', 'is_active')
    ordering = ('order',)


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_ur', 'order', 'default_open', 'is_active', 'created_at')
    list_filter = ('is_active', 'default_open', 'created_at')
    search_fields = ('title_en', 'title_ur', 'content_en', 'content_ur')
    ordering = ('order', 'id')
    inlines = [AboutSubSectionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_ur')
        }),
        ('Content', {
            'fields': ('content_en', 'content_ur'),
            'description': 'Main content for this section. Leave blank if using sub-sections.'
        }),
        ('Display Settings', {
            'fields': ('order', 'default_open', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AboutSubSection)
class AboutSubSectionAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'section', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'section', 'created_at')
    search_fields = ('title_en', 'title_ur', 'content_en', 'content_ur')
    ordering = ('section__order', 'order', 'id')
    fieldsets = (
        ('Basic Information', {
            'fields': ('section', 'title_en', 'title_ur')
        }),
        ('Content', {
            'fields': ('content_en', 'content_ur')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CurrentNasheen)
class CurrentNasheenAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ur', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_en', 'name_ur', 'description_en', 'description_ur')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_en', 'name_ur')
        }),
        ('Biography', {
            'fields': ('description_en', 'description_ur')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('is_active',),
            'description': 'Only one record should have is_active=True. This will be shown as the current Nasheen.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PreviousNasheen)
class PreviousNasheenAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_en', 'name_ur', 'is_present', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_present', 'created_at')
    search_fields = ('name_en', 'name_ur')
    ordering = ('order', 'id')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_en', 'name_ur', 'order')
        }),
        ('Display Settings', {
            'fields': ('is_present', 'is_active'),
            'description': 'is_present: Mark if this is the current Nasheen. is_active: Show in lineage tree.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

