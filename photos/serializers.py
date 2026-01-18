from rest_framework import serializers
from .models import Collection, Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image"]


class CollectionSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "name_en", "name_ur", "created_at", "images"]
