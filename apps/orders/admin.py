"""
Order admin configuration
"""

from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model
    """
    list_display = ['id', 'user', 'product_name', 'quantity', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product_name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'product_name', 'quantity', 'unit_price', 'total_amount')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
