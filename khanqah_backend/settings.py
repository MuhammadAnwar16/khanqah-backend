from pathlib import Path
from datetime import timedelta
import os

from decouple import config
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

# Comma-separated in env: "example.com,api.example.com"
# Vercel deployments use .vercel.app domain, so include it by default
default_hosts = ".vercel.app,localhost,127.0.0.1"
ALLOWED_HOSTS = [h.strip() for h in config("ALLOWED_HOSTS", default=default_hosts).split(",") if h.strip()]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',  # API documentation (Swagger/OpenAPI)
    'cloudinary',  # Cloudinary storage for media files
    'cloudinary_storage',  # Django Cloudinary storage backend

    # Local apps
    'core',
    'gallery',
    'publications',
    'photos',
    'video_audios',
    'contact',
    'about',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # XFrameOptionsMiddleware: Prevents clickjacking by setting X-Frame-Options header
    # If you need to embed backend pages in frontend iframe during development,
    # you can comment out this line temporarily (NOT recommended for production)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom security middleware for logging and monitoring
    #'core.middleware.SecurityMiddleware',
    # Security headers middleware (adds security headers to all responses)
    'core.security_headers.SecurityHeadersMiddleware',
    # Cache control headers middleware (adds Cache-Control headers)
    'core.middleware.CacheControlHeadersMiddleware',
]

ROOT_URLCONF = 'khanqah_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'khanqah_backend.wsgi.application'

# Database
# Support both DATABASE_URL (for Neon/Render) and individual settings (for local dev)
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Use DATABASE_URL (production - Neon/Render)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, conn_health_checks=True)
    }
else:
    # Use individual settings (local development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME', default='khanqah_db'),
            'USER': config('DATABASE_USER', default='postgres'),
            'PASSWORD': config('DATABASE_PASSWORD', default=''),
            'HOST': config('DATABASE_HOST', default='localhost'),
            'PORT': config('DATABASE_PORT', default='5432'),
        }
    }

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files Configuration
# Use Cloudinary for media storage if credentials are provided, otherwise use local storage
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default=None)

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    # Use Cloudinary for media storage (production)
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
    # Cloudinary will handle file storage
else:
    # Use local storage (development)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Caching Configuration
# Supports Redis (if REDIS_URL is set) or in-memory cache (default)
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    # Use Redis for caching (production)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'khanqah',
            'TIMEOUT': 300,  # Default timeout: 5 minutes
        }
    }
else:
    # Use in-memory cache (development)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }

# REST Framework & JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # General anonymous rate limit
        'user': '1000/hour'  # Authenticated users
    },
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',  # Custom error handler for standardized responses
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS for React
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in config("CORS_ALLOWED_ORIGINS", default="http://localhost:5173,http://127.0.0.1:5173").split(",")
    if o.strip()
]
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in config("CSRF_TRUSTED_ORIGINS", default="http://localhost:5173,http://127.0.0.1:5173").split(",")
    if o.strip()
]

# If you REALLY need to open it up during local dev, set CORS_ALLOW_ALL_ORIGINS=True explicitly
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)

# X-Frame-Options: Controls iframe embedding
# This prevents clickjacking attacks by blocking embedding in iframes
# 
# If you're getting "Refused to display in a frame" error:
# - For API-only backend: This is NORMAL and EXPECTED. Your frontend should use fetch/axios, not iframes.
# - If you need to embed Django admin or other pages in iframe during development:
#   1. Comment out 'XFrameOptionsMiddleware' in MIDDLEWARE above, OR
#   2. Set X_FRAME_OPTIONS = 'ALLOWALL' below (⚠️ ONLY for local dev, NEVER in production!)
#
# Options: 'DENY' (no embedding), 'SAMEORIGIN' (same origin only)
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default="SAMEORIGIN")

# For development: If you need to embed backend pages in frontend iframe
# Uncomment the line below (⚠️ ONLY for local development!)
# if DEBUG:
#     X_FRAME_OPTIONS = 'ALLOWALL'  # ⚠️ SECURITY RISK - Only use in local dev!

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Contact form recipient (can be different from sender)
CONTACT_RECIPIENT_EMAIL = config('CONTACT_RECIPIENT_EMAIL', default=EMAIL_HOST_USER)

# Internationalization
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='Asia/Karachi')
USE_I18N = True
USE_TZ = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Headers (applied to all responses)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY', default='strict-origin-when-cross-origin')

# Content Security Policy (CSP) - adjust based on your needs
# For development, you may want to relax this
CSP_DEFAULT_SRC = config('CSP_DEFAULT_SRC', default="'self'", cast=str)
CSP_SCRIPT_SRC = config('CSP_SCRIPT_SRC', default="'self' 'unsafe-inline'", cast=str)  # 'unsafe-inline' needed for Django admin
CSP_STYLE_SRC = config('CSP_STYLE_SRC', default="'self' 'unsafe-inline'", cast=str)
CSP_IMG_SRC = config('CSP_IMG_SRC', default="'self' data: https:", cast=str)
CSP_FONT_SRC = config('CSP_FONT_SRC', default="'self' data:", cast=str)
CSP_CONNECT_SRC = config('CSP_CONNECT_SRC', default="'self'", cast=str)
CSP_FRAME_SRC = config('CSP_FRAME_SRC', default="'self' https://www.youtube.com https://www.google.com", cast=str)
# Default CSP_FRAME_ANCESTORS - will be overridden based on DEBUG mode
CSP_FRAME_ANCESTORS = config('CSP_FRAME_ANCESTORS', default="'self'", cast=str)

# Security settings (production)
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
    X_FRAME_OPTIONS = 'DENY'
    
    # Stricter CSP in production
    CSP_DEFAULT_SRC = "'self'"
    CSP_SCRIPT_SRC = "'self'"  # Remove 'unsafe-inline' in production if possible
    CSP_STYLE_SRC = "'self' 'unsafe-inline'"  # Django admin needs this
    CSP_FRAME_ANCESTORS = "'self'"  # Only allow same origin in production
else:
    # Development: More permissive settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    
    # In development, allow frontend origins to embed backend in iframes
    # This is needed for PDF previews and other embedded content
    frontend_origins = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:3000',  # Common React dev port
        'http://127.0.0.1:3000',
    ]
    # Allow 'self' and frontend origins for frame-ancestors in development
    CSP_FRAME_ANCESTORS = "'self' " + " ".join(frontend_origins)

# Logging
#import os
#LOGS_DIR = BASE_DIR / 'logs'
#LOGS_DIR.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist

# LOGGING CONFIGURATION
# In production (Vercel), we cannot write to files.
# We must log to the console (StreamHandler).

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
