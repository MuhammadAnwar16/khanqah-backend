"""
URL configuration for khanqah_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI Schema Configuration
schema_view = get_schema_view(
   openapi.Info(
      title="Khanqah Yaseen Zai API",
      default_version='v1',
      description="API documentation for Khanqah Yaseen Zai website. This API provides endpoints for publications, gallery, photos, videos, audios, and contact form.",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@khanqah.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,  # Set to False if you want to require authentication
   permission_classes=(permissions.AllowAny,),  # Allow public access to docs
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation (Swagger UI and ReDoc)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('core.urls')),
    path("api/", include("gallery.urls")),
    path('api/publications/', include('publications.urls')),
    path("api/photos/", include("photos.urls")),
    path('api/video-audios/', include('video_audios.urls')),
    path('contact/', include('contact.urls')),
    path('api/about/', include('about.urls')),
    path('api/events/', include('events.urls')),
]

# In development, serve media files through custom view (allows iframe embedding)
# In production, use a proper web server (nginx/apache) to serve media files
if settings.DEBUG:
    # Use custom view for media files to allow iframe embedding
    from core.views import serve_media_file
    urlpatterns += [
        path('media/<path:file_path>', serve_media_file, name='serve-media-file'),
    ]
    # Also keep static file serving for other static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



