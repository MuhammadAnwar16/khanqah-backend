from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Audio, Video
import os

# File size limits (in bytes)
MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg']


class AudioSerializer(serializers.ModelSerializer):
    audioUrl = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ["id", "english_title", "urdu_title", "audioUrl", "category", "date"]
        read_only_fields = ['id']

    def validate_audio_file(self, value):
        """Validate audio file upload"""
        if value:
            # Check file extension
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ALLOWED_AUDIO_EXTENSIONS:
                raise serializers.ValidationError(
                    f"Only audio files (MP3, WAV, M4A, OGG) are allowed. Got: {ext}"
                )
            
            # Check file size
            if value.size > MAX_AUDIO_SIZE:
                raise serializers.ValidationError(
                    f"Audio file too large. Maximum size is {MAX_AUDIO_SIZE / (1024*1024):.0f}MB"
                )
        return value

    def get_audioUrl(self, obj):
        request = self.context.get("request")
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url)
        return ""


class VideoSerializer(serializers.ModelSerializer):
    youtubeUrl = serializers.CharField(source="youtube_url")

    class Meta:
        model = Video
        fields = ["id", "english_title", "urdu_title", "youtubeUrl", "category", "date"]
        read_only_fields = ['id']

    def validate_youtube_url(self, value):
        """Validate YouTube URL format"""
        if value:
            valid_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
            if not any(domain in value for domain in valid_domains):
                raise serializers.ValidationError(
                    "Please provide a valid YouTube URL"
                )
        return value
