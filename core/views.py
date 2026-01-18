from rest_framework import generics
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.text import get_valid_filename
import os
import logging
import mimetypes
from pathlib import Path

from .models import Publication
from .serializers import PublicationSerializer

logger = logging.getLogger(__name__)

# Allowed file extensions for security
ALLOWED_MEDIA_EXTENSIONS = {
    '.pdf': 'application/pdf',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/x-m4a',
    '.ogg': 'audio/ogg',
}


class PublicationList(generics.ListAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


@xframe_options_exempt
@require_http_methods(["GET", "HEAD"])
def serve_media_file(request, file_path):
    """
    Securely serve media files (PDFs, images, audio, etc.) with X-Frame-Options exempted
    to allow embedding in iframes from the frontend.
    
    Security features:
    - Directory traversal protection
    - File extension validation
    - MIME type validation
    - Request logging
    - File existence checks
    """
    try:
        # Normalize and sanitize file path
        file_path = file_path.strip().lstrip('/')
        
        # Prevent empty or malicious paths
        if not file_path or '..' in file_path:
            logger.warning(f"Invalid file path attempted: {file_path} from IP: {request.META.get('REMOTE_ADDR')}")
            raise Http404("Invalid file path")
        
        # Get absolute paths for comparison
        media_root = os.path.abspath(settings.MEDIA_ROOT)
        full_path = os.path.abspath(os.path.join(media_root, file_path))
        
        # Prevent directory traversal attacks - ensure file is within MEDIA_ROOT
        if not full_path.startswith(media_root):
            logger.warning(f"Directory traversal attempt detected: {file_path} from IP: {request.META.get('REMOTE_ADDR')}")
            raise Http404("Invalid file path")
        
        # Check if file exists
        if not os.path.exists(full_path):
            logger.info(f"File not found: {file_path} from IP: {request.META.get('REMOTE_ADDR')}")
            raise Http404("File not found")
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(full_path):
            logger.warning(f"Path is not a file: {file_path} from IP: {request.META.get('REMOTE_ADDR')}")
            raise Http404("Invalid file path")
        
        # Validate file extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in ALLOWED_MEDIA_EXTENSIONS:
            logger.warning(f"Disallowed file extension attempted: {file_ext} for {file_path} from IP: {request.META.get('REMOTE_ADDR')}")
            raise Http404("File type not allowed")
        
        # Get content type from allowed extensions
        content_type = ALLOWED_MEDIA_EXTENSIONS.get(file_ext)
        
        # Double-check MIME type using mimetypes (additional security layer)
        detected_mime, _ = mimetypes.guess_type(full_path)
        if detected_mime and detected_mime != content_type:
            # Log mismatch but use our whitelist (more secure)
            logger.debug(f"MIME type mismatch for {file_path}: detected {detected_mime}, using {content_type}")
        
        # Get file size for logging
        file_size = os.path.getsize(full_path)
        
        # Log successful file access (for monitoring)
        logger.info(f"Media file served: {file_path} ({file_size} bytes) to IP: {request.META.get('REMOTE_ADDR')}")
        
        # Open file in binary mode and serve
        try:
            file_handle = open(full_path, 'rb')
            response = FileResponse(
                file_handle,
                content_type=content_type,
                filename=os.path.basename(file_path)
            )
            # Add security headers
            response['Content-Disposition'] = f'inline; filename="{get_valid_filename(os.path.basename(file_path))}"'
            response['X-Content-Type-Options'] = 'nosniff'
            return response
        except IOError as e:
            logger.error(f"Error opening file {file_path}: {e}")
            raise Http404("Error reading file")
            
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Unexpected error serving media file {file_path}: {e}", exc_info=True)
        raise Http404("Error serving file")
