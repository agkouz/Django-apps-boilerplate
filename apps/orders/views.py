"""
Order views - API endpoints using Django REST Framework
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.exceptions import ValidationError

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer
from . import services, selectors


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations
    
    Router layer - handles HTTP only
    """
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """
        Get queryset using selector
        """
        filters = {}
        
        # Parse query parameters
        if self.request.query_params.get('user_id'):
            filters['user_id'] = int(self.request.query_params['user_id'])
        
        if self.request.query_params.get('status'):
            filters['status'] = self.request.query_params['status']
        
        return selectors.order_list(filters=filters)
    
    def create(self, request):
        """
        Create new order
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get user_id from query params
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id query parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = services.order_create(
                user_id=int(user_id),
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, pk=None):
        """
        Get order by ID
        """
        order = selectors.order_get_by_id(order_id=int(pk))
        
        if not order:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(OrderSerializer(order).data)
    
    def update(self, request, pk=None):
        """
        Update order (full update)
        """
        serializer = OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = services.order_update(
                order_id=int(pk),
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(OrderSerializer(order).data)
    
    def partial_update(self, request, pk=None):
        """
        Partial update order (PATCH)
        """
        serializer = OrderUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = services.order_update(
                order_id=int(pk),
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(OrderSerializer(order).data)
    
    def destroy(self, request, pk=None):
        """
        Delete order
        """
        try:
            services.order_delete(order_id=int(pk))
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark order as completed
        """
        try:
            order = services.order_complete(order_id=int(pk))
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order
        """
        try:
            order = services.order_cancel(order_id=int(pk))
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_orders(self, request, user_id=None):
        """
        Get all orders for a specific user
        """
        status_filter = request.query_params.get('status')
        
        orders = selectors.order_list_by_user(
            user_id=int(user_id),
            status=status_filter
        )
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)/statistics')
    def user_statistics(self, request, user_id=None):
        """
        Get order statistics for a user
        """
        try:
            stats = selectors.order_get_user_statistics(user_id=int(user_id))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(stats)
