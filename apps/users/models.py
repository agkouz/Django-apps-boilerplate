"""
User models
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    # Override username to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
