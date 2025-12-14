"""
User views - API endpoints using Django REST Framework
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.exceptions import ValidationError

from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from . import services, selectors


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations
    
    Router layer - handles HTTP only:
    - Receives requests
    - Validates with serializers
    - Calls services (write) or selectors (read)
    - Returns HTTP responses
    """
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """
        Get queryset using selector
        """
        filters = {}
        
        # Parse query parameters
        if self.request.query_params.get('is_active'):
            filters['is_active'] = self.request.query_params['is_active'] == 'true'
        
        if self.request.query_params.get('email_contains'):
            filters['email_contains'] = self.request.query_params['email_contains']
        
        return selectors.user_list(filters=filters)
    
    def create(self, request):
        """
        Create new user
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = services.user_create(**serializer.validated_data)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, pk=None):
        """
        Get user by ID
        """
        user = selectors.user_get_by_id(user_id=int(pk))
        
        if not user:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(UserSerializer(user).data)
    
    def update(self, request, pk=None):
        """
        Update user (full update)
        """
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = services.user_update(
                user_id=int(pk),
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(UserSerializer(user).data)
    
    def partial_update(self, request, pk=None):
        """
        Partial update user (PATCH)
        """
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = services.user_update(
                user_id=int(pk),
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(UserSerializer(user).data)
    
    def destroy(self, request, pk=None):
        """
        Delete user
        """
        try:
            services.user_delete(user_id=int(pk))
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
