"""
Order signals - handle order-related events
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    """
    Handle order creation event
    
    In a real application, this would:
    - Send confirmation email
    - Update inventory
    - Trigger notifications
    """
    if created:
        # Placeholder for order creation logic
        print(f"Order {instance.id} created for {instance.user.email}")


@receiver(post_save, sender=Order)
def order_completed_handler(sender, instance, created, **kwargs):
    """
    Handle order completion event
    """
    if not created and instance.status == 'completed':
        # Placeholder for completion logic
        print(f"Order {instance.id} completed")
