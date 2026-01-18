"""
Cache utilities for API views
Provides decorators and mixins for caching API responses
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
import hashlib
import json


def cache_api_response(timeout=300, key_prefix='api'):
    """
    Decorator to cache API view responses.
    
    Usage:
        @cache_api_response(timeout=3600)
        def my_view(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Generate cache key from request path and query params
            query_string = request.GET.urlencode()
            cache_key_data = f"{request.path}?{query_string}"
            cache_key = f"{key_prefix}:{hashlib.md5(cache_key_data.encode()).hexdigest()}"
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Call the view function
            response = func(request, *args, **kwargs)
            
            # Cache successful responses only
            if response.status_code == 200:
                # Store response data (serialize if needed)
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


class CacheMixin:
    """
    Mixin for ViewSets to enable caching.
    
    Usage:
        class MyViewSet(CacheMixin, viewsets.ModelViewSet):
            cache_timeout = 3600  # 1 hour
            cache_key_prefix = 'myapp'
    """
    cache_timeout = 300  # Default: 5 minutes
    cache_key_prefix = 'api'
    
    def get_cache_key(self):
        """Generate cache key for this request"""
        querystring = self.request.GET.urlencode()
        path = self.request.path
        cache_key_data = f"{path}?{querystring}"
        return f"{self.cache_key_prefix}:{hashlib.md5(cache_key_data.encode()).hexdigest()}"
    
    def list(self, request, *args, **kwargs):
        """Override list to use cache"""
        if not self.cache_timeout:
            return super().list(request, *args, **kwargs)
        
        cache_key = self.get_cache_key()
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            from rest_framework.response import Response
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        
        if response.status_code == 200:
            cache.set(cache_key, response.data, self.cache_timeout)
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use cache"""
        if not self.cache_timeout:
            return super().retrieve(request, *args, **kwargs)
        
        cache_key = f"{self.get_cache_key()}:{kwargs.get('pk')}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            from rest_framework.response import Response
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        
        if response.status_code == 200:
            cache.set(cache_key, response.data, self.cache_timeout)
        
        return response
    
    def invalidate_cache(self, pattern=None):
        """Invalidate cache for this viewset"""
        # Note: This is a simple implementation
        # For Redis, you could use keys() pattern matching
        # For now, we'll just clear all cache (or implement pattern matching)
        if pattern:
            # In production with Redis, implement pattern-based deletion
            pass
        else:
            # Clear cache when data changes
            cache.clear()

