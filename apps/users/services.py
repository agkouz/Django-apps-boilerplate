"""
User services - all business logic and WRITE operations
"""

from typing import Optional
from django.db import transaction
from django.contrib.auth.hashers import make_password
from apps.core.exceptions import ValidationError
from .models import User
from .selectors import user_get_by_email, user_get_by_id


@transaction.atomic
def user_create(*, email: str, password: str, full_name: str = None) -> User:
    """
    Create a new user with business logic
    
    Business rules:
    - Email must be unique
    - Password is hashed before storage
    """
    # Business rule: Email must be unique
    if user_get_by_email(email=email):
        raise ValidationError("Email already registered")
    
    # Create user with hashed password
    user = User.objects.create(
        username=email,  # Using email as username
        email=email,
        password=make_password(password),
        full_name=full_name or '',
    )
    
    return user


@transaction.atomic
def user_update(*, user_id: int, email: str = None, full_name: str = None, password: str = None) -> User:
    """
    Update user with business logic
    
    Business rules:
    - User must exist
    - If email is being changed, new email must be unique
    - Password is hashed before storage
    """
    user = user_get_by_id(user_id=user_id)
    if not user:
        raise ValidationError("User not found")
    
    # Business rule: If email is being changed, check uniqueness
    if email and email != user.email:
        if user_get_by_email(email=email):
            raise ValidationError("Email already in use")
        user.email = email
        user.username = email  # Keep username in sync
    
    # Update full name if provided
    if full_name is not None:
        user.full_name = full_name
    
    # Business logic: Hash new password if provided
    if password:
        user.password = make_password(password)
    
    user.save()
    return user


@transaction.atomic
def user_delete(*, user_id: int) -> None:
    """
    Delete user
    """
    user = user_get_by_id(user_id=user_id)
    if not user:
        raise ValidationError("User not found")
    
    user.delete()


def user_authenticate(*, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    
    Returns User if credentials are valid, None otherwise
    """
    from django.contrib.auth import authenticate
    
    user = authenticate(username=email, password=password)
    return user
