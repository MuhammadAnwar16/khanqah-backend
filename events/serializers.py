from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model
    Returns data in a format compatible with the frontend EventCalendar component
    """
    # Format for frontend compatibility
    title = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'date',
            'description',
            'recurring_type',
            'day_of_week',
            'week_of_month',
            'event_date',
            'event_time',
            'priority',
            'order',
        ]
    
    def get_title(self, obj):
        """Return title in format expected by frontend"""
        return {
            'english': obj.title_en,
            'urdu': obj.title_ur,
        }
    
    def get_date(self, obj):
        """Return date in format expected by frontend"""
        # Use date_text if available, otherwise generate from recurring_type
        if obj.date_text_en and obj.date_text_ur:
            return {
                'english': obj.date_text_en,
                'urdu': obj.date_text_ur,
            }
        
        # Fallback: generate date text from recurring_type
        date_en = obj.date_text_en or self._generate_date_text_en(obj)
        date_ur = obj.date_text_ur or self._generate_date_text_ur(obj)
        
        return {
            'english': date_en,
            'urdu': date_ur,
        }
    
    def get_description(self, obj):
        """Return description in format expected by frontend"""
        return {
            'english': obj.description_en or '',
            'urdu': obj.description_ur or '',
        }
    
    def _generate_date_text_en(self, obj):
        """Generate English date text from recurring_type"""
        if obj.recurring_type == 'daily':
            return 'Daily'
        elif obj.recurring_type == 'weekly':
            if obj.day_of_week is not None:
                if obj.day_of_week == 4:  # Thursday
                    return 'Every Thursday'
                days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                if 0 <= obj.day_of_week < len(days):
                    return f'Every {days[obj.day_of_week]}'
            return 'Weekly'
        elif obj.recurring_type == 'monthly':
            if obj.day_of_week is not None and obj.week_of_month is not None:
                if obj.day_of_week == 4 and obj.week_of_month == 1:
                    return 'First Thursday of every month'
                elif obj.day_of_week == 4:
                    return 'Thursday of every month'
            return 'Monthly'
        elif obj.recurring_type == 'one_time' and obj.event_date:
            return obj.event_date.strftime('%B %d, %Y')
        return 'Ongoing'
    
    def _generate_date_text_ur(self, obj):
        """Generate Urdu date text from recurring_type"""
        if obj.recurring_type == 'daily':
            return 'روزانہ'
        elif obj.recurring_type == 'weekly':
            if obj.day_of_week is not None:
                if obj.day_of_week == 4:  # Thursday
                    return 'ہر جمعرات'
                days_ur = ['اتوار', 'پیر', 'منگل', 'بدھ', 'جمعرات', 'جمعہ', 'ہفتہ']
                if 0 <= obj.day_of_week < len(days_ur):
                    return f'ہر {days_ur[obj.day_of_week]}'
            return 'ہفتہ وار'
        elif obj.recurring_type == 'monthly':
            if obj.day_of_week is not None and obj.week_of_month is not None:
                if obj.day_of_week == 4 and obj.week_of_month == 1:
                    return 'ہر مہینے کی پہلی جمعرات'
                elif obj.day_of_week == 4:
                    return 'ہر مہینے کا جمعرات'
            return 'ماہانہ'
        elif obj.recurring_type == 'one_time' and obj.event_date:
            # Simple date format for Urdu
            return f'{obj.event_date.strftime("%d/%m/%Y")}'
        return 'جاری'
