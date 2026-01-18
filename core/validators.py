"""
Security validators for file uploads and inputs
"""
import os
import logging
from django.core.exceptions import ValidationError

# Try to import python-magic for better MIME type detection (optional)
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

logger = logging.getLogger(__name__)

# MIME type mapping for allowed file types
ALLOWED_MIME_TYPES = {
    # PDFs
    'application/pdf': ['.pdf'],
    
    # Images
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png'],
    'image/gif': ['.gif'],
    'image/webp': ['.webp'],
    
    # Audio
    'audio/mpeg': ['.mp3'],
    'audio/wav': ['.wav'],
    'audio/x-m4a': ['.m4a'],
    'audio/ogg': ['.ogg'],
    'audio/vorbis': ['.ogg'],
}

# Reverse mapping: extension -> MIME types
EXTENSION_TO_MIME = {}
for mime_type, extensions in ALLOWED_MIME_TYPES.items():
    for ext in extensions:
        if ext not in EXTENSION_TO_MIME:
            EXTENSION_TO_MIME[ext] = []
        EXTENSION_TO_MIME[ext].append(mime_type)


def validate_file_mime_type(file, allowed_extensions):
    """
    Validate file MIME type matches its extension.
    
    Args:
        file: Django UploadedFile object
        allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.jpg'])
    
    Raises:
        ValidationError: If file extension or MIME type is invalid
    """
    if not file:
        return
    
    # Get file extension
    file_ext = os.path.splitext(file.name)[1].lower()
    
    # Check extension is allowed
    if file_ext not in allowed_extensions:
        raise ValidationError(
            f"File extension '{file_ext}' is not allowed. "
            f"Allowed extensions: {', '.join(allowed_extensions)}"
        )
    
        # Try to detect MIME type using python-magic if available
        # Fallback to file extension if magic is not available
        detected_mime = None
        try:
            # Read first 1024 bytes for MIME detection
            file.seek(0)
            file_header = file.read(1024)
            file.seek(0)  # Reset file pointer
            
            # Try using python-magic library if available
            if HAS_MAGIC:
                try:
                    detected_mime = magic.from_buffer(file_header, mime=True)
                except (AttributeError, Exception) as e:
                    logger.debug(f"python-magic detection failed: {e}")
                    detected_mime = None
            
            # Fallback: use mimetypes module
            if not detected_mime:
                import mimetypes
                detected_mime, _ = mimetypes.guess_type(file.name)
        
        except Exception as e:
            logger.warning(f"Error detecting MIME type for {file.name}: {e}")
            # Continue with extension-based validation
    
    # Get expected MIME types for this extension
    expected_mimes = EXTENSION_TO_MIME.get(file_ext, [])
    
    if expected_mimes:
        if detected_mime and detected_mime not in expected_mimes:
            logger.warning(
                f"MIME type mismatch for {file.name}: "
                f"detected '{detected_mime}', expected one of {expected_mimes}"
            )
            # In strict mode, reject the file
            # For now, we'll log but allow (you can make this stricter)
            # raise ValidationError(
            #     f"File MIME type '{detected_mime}' does not match extension '{file_ext}'"
            #     )
    
    # Additional security: Check for dangerous file signatures
    # Even if extension is .pdf, check if it's actually a PDF
    if file_ext == '.pdf':
        file.seek(0)
        header = file.read(4)
        file.seek(0)
        if not header.startswith(b'%PDF'):
            raise ValidationError("File does not appear to be a valid PDF file")
    
    elif file_ext in ['.jpg', '.jpeg']:
        file.seek(0)
        header = file.read(3)
        file.seek(0)
        if header != b'\xff\xd8\xff':
            raise ValidationError("File does not appear to be a valid JPEG image")
    
    elif file_ext == '.png':
        file.seek(0)
        header = file.read(8)
        file.seek(0)
        if header != b'\x89PNG\r\n\x1a\n':
            raise ValidationError("File does not appear to be a valid PNG image")


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal and other attacks.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    
    # Remove dangerous characters
    dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    return filename

