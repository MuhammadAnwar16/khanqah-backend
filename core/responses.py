"""
Utility functions for standardized API responses
"""
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Standardized success response format
    
    Args:
        data: Response data (dict, list, etc.)
        message: Human-readable success message
        status_code: HTTP status code
    
    Returns:
        Response object with standardized format:
        {
            "status": "success",
            "message": "...",
            "data": {...}
        }
    """
    response_data = {
        "status": "success",
        "message": message,
    }
    
    if data is not None:
        response_data["data"] = data
    
    return Response(response_data, status=status_code)


def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standardized error response format
    
    Args:
        message: Human-readable error message
        errors: Optional dict of field-specific errors (for validation errors)
        status_code: HTTP status code
    
    Returns:
        Response object with standardized format:
        {
            "status": "error",
            "message": "...",
            "errors": {...}  # Optional
        }
    """
    response_data = {
        "status": "error",
        "message": message,
    }
    
    if errors:
        response_data["errors"] = errors
    
    return Response(response_data, status=status_code)

