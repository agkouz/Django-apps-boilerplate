"""
Main URL configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Create main router
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.orders.urls')),
]
