"""
Unit tests for Order services
"""

import pytest
from decimal import Decimal
from apps.core.exceptions import ValidationError
from apps.users import services as user_services
from apps.orders import services, selectors


@pytest.mark.django_db
class TestOrderServices:
    """Test Order service layer"""
    
    def test_create_order_success(self):
        """Test successful order creation"""
        user = user_services.user_create(email='test@example.com', password='pass')
        
        order = services.order_create(
            user_id=user.id,
            product_name='Test Product',
            quantity=5,
            unit_price=Decimal('10.00')
        )
        
        assert order.product_name == 'Test Product'
        assert order.quantity == 5
        assert order.total_amount == Decimal('50.00')
        assert order.status == 'pending'
    
    def test_create_order_user_not_found(self):
        """Test order creation with non-existent user"""
        with pytest.raises(ValidationError, match="User not found"):
            services.order_create(
                user_id=999,
                product_name='Product',
                quantity=1,
                unit_price=Decimal('10.00')
            )
    
    def test_create_order_inactive_user(self):
        """Test order creation for inactive user"""
        user = user_services.user_create(email='test@example.com', password='pass')
        user.is_active = False
        user.save()
        
        with pytest.raises(ValidationError, match="User account is not active"):
            services.order_create(
                user_id=user.id,
                product_name='Product',
                quantity=1,
                unit_price=Decimal('10.00')
            )
    
    def test_create_order_exceeds_max_quantity(self):
        """Test order creation exceeding max quantity"""
        user = user_services.user_create(email='test@example.com', password='pass')
        
        with pytest.raises(ValidationError, match="Quantity cannot exceed"):
            services.order_create(
                user_id=user.id,
                product_name='Product',
                quantity=1001,
                unit_price=Decimal('10.00')
            )
    
    def test_create_order_below_minimum_value(self):
        """Test order creation below minimum value"""
        user = user_services.user_create(email='test@example.com', password='pass')
        
        with pytest.raises(ValidationError, match="Order total must be at least"):
            services.order_create(
                user_id=user.id,
                product_name='Product',
                quantity=1,
                unit_price=Decimal('0.50')
            )
    
    def test_cancel_order_success(self):
        """Test successful order cancellation"""
        user = user_services.user_create(email='test@example.com', password='pass')
        order = services.order_create(
            user_id=user.id,
            product_name='Product',
            quantity=1,
            unit_price=Decimal('10.00')
        )
        
        cancelled_order = services.order_cancel(order_id=order.id)
        
        assert cancelled_order.status == 'cancelled'
    
    def test_cancel_completed_order(self):
        """Test cancelling a completed order fails"""
        user = user_services.user_create(email='test@example.com', password='pass')
        order = services.order_create(
            user_id=user.id,
            product_name='Product',
            quantity=1,
            unit_price=Decimal('10.00')
        )
        
        # Complete the order
        services.order_complete(order_id=order.id)
        
        # Try to cancel
        with pytest.raises(ValidationError, match="Cannot cancel completed"):
            services.order_cancel(order_id=order.id)
    
    def test_complete_order_success(self):
        """Test successful order completion"""
        user = user_services.user_create(email='test@example.com', password='pass')
        order = services.order_create(
            user_id=user.id,
            product_name='Product',
            quantity=1,
            unit_price=Decimal('10.00')
        )
        
        completed_order = services.order_complete(order_id=order.id)
        
        assert completed_order.status == 'completed'
    
    def test_update_order_recalculates_total(self):
        """Test updating order recalculates total"""
        user = user_services.user_create(email='test@example.com', password='pass')
        order = services.order_create(
            user_id=user.id,
            product_name='Product',
            quantity=5,
            unit_price=Decimal('10.00')
        )
        
        updated_order = services.order_update(
            order_id=order.id,
            quantity=10
        )
        
        assert updated_order.quantity == 10
        assert updated_order.total_amount == Decimal('100.00')
