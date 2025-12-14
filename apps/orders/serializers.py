"""
Order serializers for API validation and serialization
"""

from rest_framework import serializers
from .models import Order


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating a new order"""
    product_name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField(min_value=1, max_value=1000)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class OrderUpdateSerializer(serializers.Serializer):
    """Serializer for updating order"""
    product_name = serializers.CharField(max_length=200, required=False)
    quantity = serializers.IntegerField(min_value=1, max_value=1000, required=False)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, required=False)
    status = serializers.ChoiceField(choices=['pending', 'completed', 'cancelled'], required=False)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order responses"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user_id', 'user_email', 'user_name',
            'product_name', 'quantity', 'unit_price', 'total_amount',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']
