"""
Custom exception handlers for standardized error responses
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    
    Returns standardized error format:
    {
        "status": "error",
        "message": "Human-readable error message",
        "errors": {...}  # Optional: detailed validation errors
    }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it means an unhandled exception occurred
    if response is None:
        # Log the exception for debugging
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        # Return a generic error response (don't leak internal details in production)
        return Response(
            {
                "status": "error",
                "message": "An unexpected error occurred. Please try again later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize the response data format
    custom_response_data = {
        "status": "error",
        "message": None,
        "errors": {}
    }
    
    # Handle different error types
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            # Validation errors - multiple fields
            custom_response_data["errors"] = exc.detail
            custom_response_data["message"] = "Validation failed. Please check the errors below."
        elif isinstance(exc.detail, list):
            # Non-field errors
            custom_response_data["errors"] = {"non_field_errors": exc.detail}
            custom_response_data["message"] = exc.detail[0] if exc.detail else "An error occurred."
        elif isinstance(exc.detail, str):
            # Simple string error
            custom_response_data["message"] = exc.detail
        else:
            custom_response_data["message"] = str(exc.detail)
    else:
        custom_response_data["message"] = "An error occurred."
    
    # Set default messages for common status codes if not already set
    if not custom_response_data["message"]:
        status_code = response.status_code
        if status_code == 400:
            custom_response_data["message"] = "Bad request. Please check your input."
        elif status_code == 401:
            custom_response_data["message"] = "Authentication required."
        elif status_code == 403:
            custom_response_data["message"] = "You don't have permission to perform this action."
        elif status_code == 404:
            custom_response_data["message"] = "Resource not found."
        elif status_code == 405:
            custom_response_data["message"] = "Method not allowed."
        elif status_code == 429:
            custom_response_data["message"] = "Too many requests. Please slow down."
        elif status_code >= 500:
            custom_response_data["message"] = "Server error. Please try again later."
        else:
            custom_response_data["message"] = "An error occurred."
    
    response.data = custom_response_data
    
    return response

