"""
Unit tests for User services
"""

import pytest
from django.test import TestCase
from apps.core.exceptions import ValidationError
from apps.users import services, selectors
from apps.users.models import User


@pytest.mark.django_db
class TestUserServices:
    """Test User service layer"""
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user = services.user_create(
            email='test@example.com',
            password='password123',
            full_name='Test User'
        )
        
        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'
        assert user.check_password('password123')
        assert user.is_active
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email raises error"""
        services.user_create(
            email='test@example.com',
            password='password123'
        )
        
        with pytest.raises(ValidationError, match="Email already registered"):
            services.user_create(
                email='test@example.com',
                password='password456'
            )
    
    def test_update_user_success(self):
        """Test successful user update"""
        user = services.user_create(
            email='old@example.com',
            password='password123',
            full_name='Old Name'
        )
        
        updated_user = services.user_update(
            user_id=user.id,
            email='new@example.com',
            full_name='New Name'
        )
        
        assert updated_user.email == 'new@example.com'
        assert updated_user.full_name == 'New Name'
    
    def test_update_user_duplicate_email(self):
        """Test updating user with existing email raises error"""
        services.user_create(email='existing@example.com', password='pass')
        user = services.user_create(email='user@example.com', password='pass')
        
        with pytest.raises(ValidationError, match="Email already in use"):
            services.user_update(user_id=user.id, email='existing@example.com')
    
    def test_update_user_not_found(self):
        """Test updating non-existent user raises error"""
        with pytest.raises(ValidationError, match="User not found"):
            services.user_update(user_id=999, full_name='New Name')
    
    def test_delete_user_success(self):
        """Test successful user deletion"""
        user = services.user_create(email='delete@example.com', password='pass')
        
        services.user_delete(user_id=user.id)
        
        assert selectors.user_get_by_id(user_id=user.id) is None
    
    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        services.user_create(email='auth@example.com', password='password123')
        
        user = services.user_authenticate(
            email='auth@example.com',
            password='password123'
        )
        
        assert user is not None
        assert user.email == 'auth@example.com'
    
    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        services.user_create(email='auth@example.com', password='password123')
        
        user = services.user_authenticate(
            email='auth@example.com',
            password='wrongpassword'
        )
        
        assert user is None
