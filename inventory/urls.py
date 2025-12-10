from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StockLogViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'logs', StockLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]