from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Publication
from core.validators import validate_file_mime_type, sanitize_filename
import os
import logging

logger = logging.getLogger(__name__)

# File size limits (in bytes)
MAX_PDF_SIZE = 50 * 1024 * 1024  # 50MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

ALLOWED_PDF_EXTENSIONS = ['.pdf']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


class PublicationSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = "__all__"
        read_only_fields = ['id']

    def validate_file(self, value):
        """Validate PDF file upload with comprehensive security checks"""
        if value:
            # Sanitize filename
            value.name = sanitize_filename(value.name)
            
            # Check file extension
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ALLOWED_PDF_EXTENSIONS:
                logger.warning(f"Invalid file extension attempted: {ext} for file: {value.name}")
                raise serializers.ValidationError(
                    f"Only PDF files are allowed. Got: {ext}"
                )
            
            # Check file size
            if value.size > MAX_PDF_SIZE:
                logger.warning(f"File too large: {value.size} bytes for file: {value.name}")
                raise serializers.ValidationError(
                    f"File size too large. Maximum size is {MAX_PDF_SIZE / (1024*1024):.0f}MB"
                )
            
            # Validate MIME type matches extension
            try:
                validate_file_mime_type(value, ALLOWED_PDF_EXTENSIONS)
            except ValidationError as e:
                logger.warning(f"MIME type validation failed for {value.name}: {e}")
                raise serializers.ValidationError(str(e))
            
            logger.info(f"PDF file validated successfully: {value.name} ({value.size} bytes)")
        
        return value

    def validate_cover(self, value):
        """Validate cover image upload with comprehensive security checks"""
        if value:
            # Sanitize filename
            value.name = sanitize_filename(value.name)
            
            # Check file extension
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                logger.warning(f"Invalid image extension attempted: {ext} for file: {value.name}")
                raise serializers.ValidationError(
                    f"Only image files (JPG, PNG, WebP) are allowed. Got: {ext}"
                )
            
            # Check file size
            if value.size > MAX_IMAGE_SIZE:
                logger.warning(f"Image too large: {value.size} bytes for file: {value.name}")
                raise serializers.ValidationError(
                    f"Image size too large. Maximum size is {MAX_IMAGE_SIZE / (1024*1024):.0f}MB"
                )
            
            # Validate MIME type matches extension
            try:
                validate_file_mime_type(value, ALLOWED_IMAGE_EXTENSIONS)
            except ValidationError as e:
                logger.warning(f"MIME type validation failed for {value.name}: {e}")
                raise serializers.ValidationError(str(e))
            
            logger.info(f"Cover image validated successfully: {value.name} ({value.size} bytes)")
        
        return value

    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_file(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
