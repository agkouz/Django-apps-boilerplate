"""
Order services - all business logic and WRITE operations
"""

from decimal import Decimal
from django.db import transaction
from django.conf import settings
from apps.core.exceptions import ValidationError
from apps.users.selectors import user_get_by_id
from .models import Order
from .selectors import order_get_by_id


@transaction.atomic
def order_create(
    *,
    user_id: int,
    product_name: str,
    quantity: int,
    unit_price: Decimal
) -> Order:
    """
    Create new order with business logic
    
    Business rules:
    - User must exist and be active
    - Maximum quantity: 1000 units
    - Minimum order value: $1.00
    - Total amount calculated automatically
    """
    # Business rule: User must exist and be active
    user = user_get_by_id(user_id=user_id)
    if not user:
        raise ValidationError("User not found")
    
    if not user.is_active:
        raise ValidationError("User account is not active")
    
    # Business rule: Maximum quantity
    max_quantity = getattr(settings, 'MAX_ORDER_QUANTITY', 1000)
    if quantity > max_quantity:
        raise ValidationError(f"Quantity cannot exceed {max_quantity} units per order")
    
    # Business logic: Calculate total amount
    total_amount = Decimal(str(quantity)) * unit_price
    
    # Business rule: Minimum order value
    min_value = Decimal(str(getattr(settings, 'MIN_ORDER_VALUE', 1.0)))
    if total_amount < min_value:
        raise ValidationError(f"Order total must be at least ${min_value}")
    
    # Create order
    order = Order.objects.create(
        user=user,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        total_amount=total_amount,
        status='pending'
    )
    
    return order


@transaction.atomic
def order_update(
    *,
    order_id: int,
    product_name: str = None,
    quantity: int = None,
    unit_price: Decimal = None,
    status: str = None
) -> Order:
    """
    Update order with business logic
    
    Business rules:
    - Cannot update completed or cancelled orders
    - Recalculate total if quantity or price changed
    - Validate status transitions
    """
    order = order_get_by_id(order_id=order_id)
    if not order:
        raise ValidationError("Order not found")
    
    # Business rule: Cannot update completed or cancelled orders
    if order.status in ['completed', 'cancelled']:
        raise ValidationError(f"Cannot update {order.status} orders")
    
    # Update fields if provided
    if product_name is not None:
        order.product_name = product_name
    
    if quantity is not None:
        max_quantity = getattr(settings, 'MAX_ORDER_QUANTITY', 1000)
        if quantity > max_quantity:
            raise ValidationError(f"Quantity cannot exceed {max_quantity}")
        order.quantity = quantity
    
    if unit_price is not None:
        order.unit_price = unit_price
    
    # Recalculate total if quantity or price changed
    if quantity is not None or unit_price is not None:
        order.total_amount = Decimal(str(order.quantity)) * order.unit_price
        
        min_value = Decimal(str(getattr(settings, 'MIN_ORDER_VALUE', 1.0)))
        if order.total_amount < min_value:
            raise ValidationError(f"Order total must be at least ${min_value}")
    
    # Update status with validation
    if status is not None:
        # Business rule: Status transition validation
        valid_transitions = {
            'pending': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': []
        }
        
        if status not in valid_transitions.get(order.status, []):
            raise ValidationError(
                f"Invalid status transition from {order.status} to {status}"
            )
        
        order.status = status
    
    order.save()
    return order


@transaction.atomic
def order_cancel(*, order_id: int) -> Order:
    """
    Cancel an order
    
    Business rules:
    - Cannot cancel completed orders
    - Order must exist
    """
    order = order_get_by_id(order_id=order_id)
    if not order:
        raise ValidationError("Order not found")
    
    if order.status == 'completed':
        raise ValidationError("Cannot cancel completed orders")
    
    if order.status == 'cancelled':
        raise ValidationError("Order is already cancelled")
    
    order.status = 'cancelled'
    order.save()
    
    return order


@transaction.atomic
def order_complete(*, order_id: int) -> Order:
    """
    Mark order as completed
    
    Business rules:
    - Only pending orders can be completed
    """
    order = order_get_by_id(order_id=order_id)
    if not order:
        raise ValidationError("Order not found")
    
    if order.status != 'pending':
        raise ValidationError("Only pending orders can be completed")
    
    order.status = 'completed'
    order.save()
    
    return order


@transaction.atomic
def order_delete(*, order_id: int) -> None:
    """
    Delete an order
    
    Business rules:
    - Cannot delete completed orders
    """
    order = order_get_by_id(order_id=order_id)
    if not order:
        raise ValidationError("Order not found")
    
    if order.status == 'completed':
        raise ValidationError("Cannot delete completed orders")
    
    order.delete()
