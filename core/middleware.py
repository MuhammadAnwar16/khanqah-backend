"""
Custom middleware for caching and performance
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class CacheControlHeadersMiddleware(MiddlewareMixin):
    """
    Add Cache-Control headers to API responses for better performance.
    Different cache strategies for different endpoints.
    """
    
    # Cache settings (in seconds)
    CACHE_TIMES = {
        # Static/rarely changing content - 1 hour
        '/api/about/': 3600,
        '/api/publications/': 3600,
        '/api/photos/collections/': 3600,
        '/api/gallery/': 3600,
        # Media URLs - 1 day (304 Not Modified will be used)
        '/media/': 86400,
        # Admin - no cache
        '/admin/': 0,
        # API docs - 1 hour
        '/swagger/': 3600,
        '/redoc/': 3600,
    }
    
    # Default cache time for API endpoints (5 minutes)
    DEFAULT_API_CACHE = 300
    
    # No-cache paths
    NO_CACHE_PATHS = [
        '/admin/',
        '/contact/send-message/',
        '/api/token/',
        '/api/token/refresh/',
    ]
    
    def process_response(self, request, response):
        """Add Cache-Control headers based on request path"""
        
        # Skip for non-2xx responses (except 304 Not Modified)
        if response.status_code not in [200, 304]:
            return response
        
        # Skip for authenticated requests that might have user-specific data
        if request.user.is_authenticated and request.path.startswith('/api/'):
            # Still cache but with shorter time
            if not any(path in request.path for path in self.NO_CACHE_PATHS):
                response['Cache-Control'] = 'private, max-age=60'  # 1 minute for authenticated
            return response
        
        path = request.path
        
        # Check no-cache paths first
        if any(no_cache_path in path for no_cache_path in self.NO_CACHE_PATHS):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        
        # Check specific cache times
        cache_time = None
        for cache_path, time in self.CACHE_TIMES.items():
            if path.startswith(cache_path):
                cache_time = time
                break
        
        # Use default for API endpoints
        if cache_time is None and path.startswith('/api/'):
            cache_time = self.DEFAULT_API_CACHE
        
        # Set cache headers
        if cache_time and cache_time > 0:
            if cache_time >= 3600:  # 1 hour or more - public cache
                response['Cache-Control'] = f'public, max-age={cache_time}, must-revalidate'
            else:  # Less than 1 hour - private cache
                response['Cache-Control'] = f'private, max-age={cache_time}, must-revalidate'
            
            # ETag will be handled by Django automatically if enabled
        elif cache_time == 0:
            response['Cache-Control'] = 'no-cache, must-revalidate'
        
        return response
