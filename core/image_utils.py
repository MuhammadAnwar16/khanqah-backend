"""
Image processing utilities for optimization and thumbnail generation
"""
from PIL import Image
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def optimize_image(image_path, quality=85, max_size=(1920, 1920), format='JPEG'):
    """
    Optimize image by resizing and compressing.
    
    Args:
        image_path: Path to the image file
        quality: JPEG quality (1-100), default 85
        max_size: Maximum dimensions (width, height), default (1920, 1920)
        format: Output format ('JPEG', 'PNG', 'WEBP'), default 'JPEG'
    
    Returns:
        Path to optimized image (same path if optimization succeeded)
    """
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB for JPEG
            if format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB' and format != 'PNG':
                img = img.convert('RGB')
            
            # Resize if image is larger than max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized image {image_path} to {img.size}")
            
            # Save optimized image
            if format == 'WEBP':
                output_path = str(image_path).rsplit('.', 1)[0] + '.webp'
                img.save(output_path, format='WEBP', quality=quality, method=6)
            else:
                img.save(image_path, format=format, quality=quality, optimize=True)
            
            logger.info(f"Optimized image {image_path} with quality {quality}")
            return image_path
            
    except Exception as e:
        logger.error(f"Error optimizing image {image_path}: {str(e)}")
        return image_path  # Return original path on error


def generate_thumbnail(image_path, size=(300, 300), quality=75):
    """
    Generate a thumbnail of an image.
    
    Args:
        image_path: Path to the original image
        size: Thumbnail size (width, height), default (300, 300)
        quality: JPEG quality (1-100), default 75
    
    Returns:
        Path to thumbnail file
    """
    try:
        with Image.open(image_path) as img:
            # Create thumbnail (maintains aspect ratio)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Generate thumbnail path
            path_obj = Path(image_path)
            thumbnail_path = path_obj.parent / f"{path_obj.stem}_thumb{path_obj.suffix}"
            
            # Convert RGBA to RGB for JPEG
            if thumbnail_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB' and thumbnail_path.suffix.lower() not in ['.png', '.webp']:
                img = img.convert('RGB')
            
            # Save thumbnail
            img.save(thumbnail_path, quality=quality, optimize=True)
            logger.info(f"Generated thumbnail {thumbnail_path} from {image_path}")
            
            return str(thumbnail_path)
            
    except Exception as e:
        logger.error(f"Error generating thumbnail for {image_path}: {str(e)}")
        return None


def get_image_dimensions(image_path):
    """Get image dimensions without loading full image."""
    try:
        with Image.open(image_path) as img:
            return img.size  # (width, height)
    except Exception as e:
        logger.error(f"Error getting dimensions for {image_path}: {str(e)}")
        return None

