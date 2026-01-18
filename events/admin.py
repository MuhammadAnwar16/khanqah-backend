from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'recurring_type', 'is_active', 'order', 'created_at']
    list_filter = ['recurring_type', 'is_active', 'day_of_week']
    search_fields = ['title_en', 'title_ur', 'description_en', 'description_ur']
    ordering = ['order', 'id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_ur', 'description_en', 'description_ur')
        }),
        ('Recurring Settings', {
            'fields': ('recurring_type', 'day_of_week', 'week_of_month')
        }),
        ('One-Time Event Settings', {
            'fields': ('event_date', 'event_time'),
            'description': 'Only used for one-time events'
        }),
        ('Display Settings', {
            'fields': ('priority', 'date_text_en', 'date_text_ur', 'order', 'is_active'),
            'description': 'Priority determines the color indicator on calendar (High=Red, Medium=Blue, Low=Green)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
