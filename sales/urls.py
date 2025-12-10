from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'orders', SalesOrderViewSet, basename='sales-order')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]