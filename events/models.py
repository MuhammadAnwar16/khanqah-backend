from django.db import models


class Event(models.Model):
    """
    Spiritual events model for the events section
    Supports both recurring and one-time events
    """
    # Event Type Choices
    RECURRING_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ]
    
    DAY_OF_WEEK_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]
    
    # Basic Information
    title_en = models.CharField(max_length=255, help_text="Event title in English")
    title_ur = models.CharField(max_length=255, help_text="Event title in Urdu")
    description_en = models.TextField(blank=True, help_text="Event description in English")
    description_ur = models.TextField(blank=True, help_text="Event description in Urdu")
    
    # Date/Time Information
    recurring_type = models.CharField(
        max_length=20,
        choices=RECURRING_TYPE_CHOICES,
        default='one_time',
        help_text="Type of recurring event"
    )
    
    # For recurring events
    day_of_week = models.IntegerField(
        null=True,
        blank=True,
        choices=DAY_OF_WEEK_CHOICES,
        help_text="Day of week for weekly/monthly recurring events (0=Sunday, 4=Thursday)"
    )
    week_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text="Week of month (1-4) for monthly recurring events (e.g., 1 = first Thursday)"
    )
    
    # For one-time events
    event_date = models.DateField(
        null=True,
        blank=True,
        help_text="Specific date for one-time events"
    )
    event_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of the event"
    )
    
    # Display Settings
    date_text_en = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable date text in English (e.g., 'First Thursday of every month')"
    )
    date_text_ur = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable date text in Urdu (e.g., 'ہر مہینے کی پہلی جمعرات')"
    )
    
    # Priority/Color for visual distinction
    PRIORITY_CHOICES = [
        ('high', 'High (Red)'),
        ('medium', 'Medium (Blue)'),
        ('low', 'Low (Green)'),
        ('default', 'Default (Blue)'),
    ]
    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='default',
        help_text="Event priority determines the color indicator on calendar"
    )
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Show this event on the website")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.title_en} ({self.recurring_type})"
    
    def get_date_pattern(self):
        """
        Returns a date pattern string for calendar matching
        """
        if self.recurring_type == 'daily':
            return 'daily'
        elif self.recurring_type == 'weekly' and self.day_of_week == 4:  # Thursday
            return 'thursday' if not self.week_of_month else f'first_thursday'
        elif self.recurring_type == 'monthly' and self.day_of_week == 4 and self.week_of_month == 1:
            return 'first_thursday'
        elif self.day_of_week == 4:
            return 'thursday'
        return None
