"""
User serializers for API validation and serialization
"""

from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.Serializer):
    """Serializer for creating a new user"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(required=False, allow_blank=True)


class UserUpdateSerializer(serializers.Serializer):
    """Serializer for updating user"""
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, min_length=8)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User responses"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
