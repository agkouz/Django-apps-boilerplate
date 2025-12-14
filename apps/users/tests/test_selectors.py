"""
Unit tests for User selectors
"""

import pytest
from apps.users import services, selectors


@pytest.mark.django_db
class TestUserSelectors:
    """Test User selector layer"""
    
    def test_user_get_by_id(self):
        """Test getting user by ID"""
        user = services.user_create(email='test@example.com', password='pass')
        
        found_user = selectors.user_get_by_id(user_id=user.id)
        
        assert found_user is not None
        assert found_user.email == 'test@example.com'
    
    def test_user_get_by_id_not_found(self):
        """Test getting non-existent user returns None"""
        user = selectors.user_get_by_id(user_id=999)
        
        assert user is None
    
    def test_user_get_by_email(self):
        """Test getting user by email"""
        services.user_create(email='test@example.com', password='pass')
        
        user = selectors.user_get_by_email(email='test@example.com')
        
        assert user is not None
        assert user.email == 'test@example.com'
    
    def test_user_list_no_filters(self):
        """Test listing all users"""
        services.user_create(email='user1@example.com', password='pass')
        services.user_create(email='user2@example.com', password='pass')
        
        users = selectors.user_list()
        
        assert users.count() == 2
    
    def test_user_list_with_is_active_filter(self):
        """Test listing users with is_active filter"""
        user = services.user_create(email='active@example.com', password='pass')
        inactive_user = services.user_create(email='inactive@example.com', password='pass')
        
        # Deactivate one user
        inactive_user.is_active = False
        inactive_user.save()
        
        active_users = selectors.user_list(filters={'is_active': True})
        
        assert active_users.count() == 1
        assert active_users.first().email == 'active@example.com'
    
    def test_user_exists(self):
        """Test checking if user exists"""
        services.user_create(email='exists@example.com', password='pass')
        
        assert selectors.user_exists(email='exists@example.com')
        assert not selectors.user_exists(email='notexists@example.com')
