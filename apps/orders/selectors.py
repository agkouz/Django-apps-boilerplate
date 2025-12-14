"""
Order selectors - all READ operations and queries
"""

from django.db.models import QuerySet, Sum, Count, Q
from typing import Optional
from .models import Order


def order_get_by_id(*, order_id: int) -> Optional[Order]:
    """
    Get order by ID with related user
    """
    try:
        return Order.objects.select_related('user').get(id=order_id)
    except Order.DoesNotExist:
        return None


def order_list(*, filters: dict = None) -> QuerySet[Order]:
    """
    Get list of orders with optional filters
    
    Supported filters:
    - status: str
    - user_id: int
    """
    qs = Order.objects.select_related('user').all()
    
    if filters:
        if 'status' in filters:
            qs = qs.filter(status=filters['status'])
        
        if 'user_id' in filters:
            qs = qs.filter(user_id=filters['user_id'])
    
    return qs.order_by('-created_at')


def order_list_by_user(*, user_id: int, status: str = None) -> QuerySet[Order]:
    """
    Get all orders for a specific user
    """
    qs = Order.objects.filter(user_id=user_id)
    
    if status:
        qs = qs.filter(status=status)
    
    return qs.select_related('user').order_by('-created_at')


def order_list_by_status(*, status: str) -> QuerySet[Order]:
    """
    Get orders by status
    """
    return Order.objects.select_related('user').filter(status=status).order_by('-created_at')


def order_count_by_user(*, user_id: int) -> int:
    """
    Count total orders for a user
    """
    return Order.objects.filter(user_id=user_id).count()


def order_get_user_total_spent(*, user_id: int) -> float:
    """
    Calculate total amount spent by user (completed orders only)
    """
    result = Order.objects.filter(
        user_id=user_id,
        status='completed'
    ).aggregate(total=Sum('total_amount'))
    
    return float(result['total'] or 0)


def order_get_user_statistics(*, user_id: int) -> dict:
    """
    Get comprehensive order statistics for a user
    """
    stats = Order.objects.filter(user_id=user_id).aggregate(
        total_orders=Count('id'),
        pending_orders=Count('id', filter=Q(status='pending')),
        completed_orders=Count('id', filter=Q(status='completed')),
        total_spent=Sum('total_amount', filter=Q(status='completed'))
    )
    
    from apps.users.selectors import user_get_by_id
    user = user_get_by_id(user_id=user_id)
    
    total_spent = float(stats['total_spent'] or 0)
    total_orders = stats['total_orders'] or 0
    
    return {
        'user_id': user_id,
        'user_email': user.email if user else None,
        'total_orders': total_orders,
        'pending_orders': stats['pending_orders'] or 0,
        'completed_orders': stats['completed_orders'] or 0,
        'total_spent': total_spent,
        'average_order_value': total_spent / total_orders if total_orders > 0 else 0
    }
