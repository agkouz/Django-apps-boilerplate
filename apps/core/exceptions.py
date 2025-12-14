"""
Custom exceptions for the application
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class BusinessLogicError(Exception):
    """Base exception for business logic errors"""
    pass


class ValidationError(BusinessLogicError):
    """Raised when business validation fails"""
    pass


class NotFoundError(BusinessLogicError):
    """Raised when resource is not found"""
    pass


class PermissionDeniedError(BusinessLogicError):
    """Raised when user doesn't have permission"""
    pass
