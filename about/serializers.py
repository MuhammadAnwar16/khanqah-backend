from rest_framework import serializers
from .models import AboutSection, AboutSubSection, CurrentNasheen, PreviousNasheen


class AboutSubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSubSection
        fields = ['id', 'title_en', 'title_ur', 'content_en', 'content_ur', 'order']


class AboutSectionSerializer(serializers.ModelSerializer):
    subsections = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutSection
        fields = ['id', 'title_en', 'title_ur', 'content_en', 'content_ur', 'order', 'default_open', 'subsections']
    
    def get_subsections(self, obj):
        # Filter active subsections and order them
        active_subsections = obj.subsections.filter(is_active=True).order_by('order', 'id')
        return AboutSubSectionSerializer(active_subsections, many=True).data


class CurrentNasheenSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = CurrentNasheen
        fields = ['id', 'name_en', 'name_ur', 'description_en', 'description_ur', 'image']
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class PreviousNasheenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousNasheen
        fields = ['id', 'name_en', 'name_ur', 'order', 'is_present']

