"""
User selectors - all READ operations and queries
"""

from django.db.models import QuerySet
from typing import Optional
from .models import User


def user_get_by_id(*, user_id: int) -> Optional[User]:
    """
    Get user by ID
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def user_get_by_email(*, email: str) -> Optional[User]:
    """
    Get user by email
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def user_list(*, filters: dict = None) -> QuerySet[User]:
    """
    Get list of users with optional filters
    
    Supported filters:
    - is_active: bool
    - email_contains: str
    """
    qs = User.objects.all()
    
    if filters:
        if 'is_active' in filters:
            qs = qs.filter(is_active=filters['is_active'])
        
        if 'email_contains' in filters:
            qs = qs.filter(email__icontains=filters['email_contains'])
    
    return qs.order_by('-created_at')


def user_exists(*, email: str) -> bool:
    """
    Check if user exists by email
    """
    return User.objects.filter(email=email).exists()
