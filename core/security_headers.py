"""
Middleware to add security headers to all responses
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all HTTP responses
    """
    
    def process_response(self, request, response):
        # X-Content-Type-Options: Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-XSS-Protection: Enable browser XSS filter
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy: Control referrer information
        if hasattr(settings, 'SECURE_REFERRER_POLICY'):
            response['Referrer-Policy'] = settings.SECURE_REFERRER_POLICY
        
        # Permissions-Policy: Control browser features
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(), '
            'usb=()'
        )
        
        # Production-only headers
        if not settings.DEBUG:
            # Strict-Transport-Security (HSTS)
            if hasattr(settings, 'SECURE_HSTS_SECONDS'):
                hsts_value = f'max-age={settings.SECURE_HSTS_SECONDS}'
                if getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False):
                    hsts_value += '; includeSubDomains'
                if getattr(settings, 'SECURE_HSTS_PRELOAD', False):
                    hsts_value += '; preload'
                response['Strict-Transport-Security'] = hsts_value
        
        # Content Security Policy (CSP) - if configured
        # Skip CSP for media files served by our custom view (they need to be embeddable)
        if hasattr(settings, 'CSP_DEFAULT_SRC') and not request.path.startswith('/media/'):
            csp_parts = []
            if hasattr(settings, 'CSP_DEFAULT_SRC'):
                csp_parts.append(f"default-src {settings.CSP_DEFAULT_SRC}")
            if hasattr(settings, 'CSP_SCRIPT_SRC'):
                csp_parts.append(f"script-src {settings.CSP_SCRIPT_SRC}")
            if hasattr(settings, 'CSP_STYLE_SRC'):
                csp_parts.append(f"style-src {settings.CSP_STYLE_SRC}")
            if hasattr(settings, 'CSP_IMG_SRC'):
                csp_parts.append(f"img-src {settings.CSP_IMG_SRC}")
            if hasattr(settings, 'CSP_FONT_SRC'):
                csp_parts.append(f"font-src {settings.CSP_FONT_SRC}")
            if hasattr(settings, 'CSP_CONNECT_SRC'):
                csp_parts.append(f"connect-src {settings.CSP_CONNECT_SRC}")
            if hasattr(settings, 'CSP_FRAME_SRC'):
                csp_parts.append(f"frame-src {settings.CSP_FRAME_SRC}")
            if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
                csp_parts.append(f"frame-ancestors {settings.CSP_FRAME_ANCESTORS}")
            
            if csp_parts:
                response['Content-Security-Policy'] = '; '.join(csp_parts)
        
        return response

